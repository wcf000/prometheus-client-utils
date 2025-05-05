"""
Prometheus metrics middleware for FastAPI
"""
import time

from prometheus_client import Counter, Histogram
from starlette.requests import Request
from starlette.routing import Match

from app.core.prometheus.config import PrometheusConfig

REQUEST_COUNT = Counter(
    "requests_total",
    "Total requests by method, path and status",
    ["method", "path", "status_code"]
)

REQUEST_TIME = Histogram(
    "request_duration_seconds",
    "Request duration by method and path",
    ["method", "path"]
)

CREDITS_USED = Counter(
    "credits_used_total",
    "Credits used by user and type",
    ["user_id", "credit_type"]
)

VAPI_CALLS = Counter(
    'vapi_calls_total',
    'VAPI calls by endpoint',
    ['endpoint', 'method', 'status']
)

VAPI_CREDITS = Counter(
    'vapi_credits_total',
    'Credits used by endpoint',
    ['endpoint', 'user_tier']
)

STRIPE_CALLS = Counter(
    'stripe_api_calls_total', 
    'Total Stripe API calls',
    ['method', 'endpoint', 'status']
)
STRIPE_LATENCY = Histogram(
    'stripe_api_latency_seconds',
    'Stripe API call latency',
    ['method', 'endpoint']
)

class PrometheusMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or not PrometheusConfig.ENABLED:
            return await self.app(scope, receive, send)

        request = Request(scope)
        method = request.method
        path = self.get_path(request)

        if path.startswith('/vapi/'):
            endpoint = path.split('/')[2]  # Get endpoint type (voice, assistants, etc)
            with REQUEST_TIME.labels(method, path).time():
                response = await self.app(scope, receive, send)
                VAPI_CALLS.labels(endpoint, method, response.status_code).inc()
                REQUEST_COUNT.labels(method, path, response.status_code).inc()
                return response
        elif path.startswith('/stripe'):
            await self.dispatch(request, self.app)
            return
        else:
            with REQUEST_TIME.labels(method, path).time():
                response = await self.app(scope, receive, send)
                REQUEST_COUNT.labels(method, path, response.status_code).inc()
                return response

    async def dispatch(self, request: Request, call_next):
        method = request.method
        endpoint = request.url.path.split('/')[-1]
        start_time = time.time()
        
        try:
            response = await call_next(request)
            STRIPE_CALLS.labels(
                method=method,
                endpoint=endpoint,
                status=response.status_code
            ).inc()
            STRIPE_LATENCY.labels(
                method=method,
                endpoint=endpoint
            ).observe(time.time() - start_time)
            return response
            
        except Exception as e:
            STRIPE_CALLS.labels(
                method=method,
                endpoint=endpoint,
                status='500'
            ).inc()
            raise

    def get_path(self, request: Request) -> str:
        for route in request.app.routes:
            match, _ = route.matches(request.scope)
            if match == Match.FULL:
                path = route.path
                if path.startswith('/vapi/'):
                    return f"vapi/{path.split('/')[2]}"  # Returns 'vapi/voice', 'vapi/assistants' etc.
                return path
        path = request.url.path
        if path.startswith('/vapi/'):
            return f"vapi/{path.split('/')[2]}"  # Returns 'vapi/voice', 'vapi/assistants' etc.
        return path
