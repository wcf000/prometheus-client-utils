"""
Prometheus metrics middleware for FastAPI
"""
import time

from starlette.requests import Request
from starlette.routing import Match

from app.core.prometheus.config import PrometheusConfig
from app.core.prometheus.metrics import get_request_count, get_request_latency

# CREDITS_USED, VAPI_CALLS, VAPI_CREDITS, STRIPE_CALLS, STRIPE_LATENCY can remain for now, but REQUEST_COUNT and REQUEST_TIME are now accessed via their getter functions.

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
            with get_request_latency().labels(method, path).time():
                response = await self.app(scope, receive, send)
                VAPI_CALLS.labels(endpoint, method, response.status_code).inc()
                get_request_count().labels(method, path, response.status_code).inc()
                return response
        elif path.startswith('/stripe'):
            await self.dispatch(request, self.app)
            return
        else:
            with get_request_latency().labels(method, path).time():
                response = await self.app(scope, receive, send)
                get_request_count().labels(method, path, response.status_code).inc()
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
