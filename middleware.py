"""
Prometheus metrics middleware for FastAPI
"""
import time
from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Match
from starlette.types import ASGIApp

# Import the function to get config instance instead of the class directly
from app.core.prometheus.config import get_prometheus_config
from app.core.prometheus.metrics import get_request_count, get_request_latency

# Get the config instance
prometheus_config = get_prometheus_config()

class PrometheusMiddleware(BaseHTTPMiddleware):
    """
    Middleware that collects Prometheus metrics for HTTP requests.
    Extends Starlette's BaseHTTPMiddleware for better compatibility.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if not prometheus_config.ENABLED:
            return await call_next(request)

        # Extract request information
        method = request.method
        endpoint = self.get_path(request)
        
        # Record timing
        start_time = time.time()
        
        # Process request and catch any errors to ensure metrics are recorded
        try:
            response = await call_next(request)
            status = response.status_code
        except Exception as exc:
            # If there's an exception, record it as a 500 error
            status = 500
            raise exc
        finally:
            # Calculate elapsed time
            elapsed = time.time() - start_time
            
            # Record metrics
            get_request_count().labels(method, endpoint, status).inc()
            get_request_latency().labels(method, endpoint, status).observe(elapsed)
        
        return response

    def get_path(self, request: Request) -> str:
        """
        Get the path template for this request, so that we can use it as a dimension.
        For example, we want /items/{item_id} instead of /items/123 to avoid high cardinality metrics.
        """
        # Check if there's an endpoint in the scope
        if hasattr(request, "scope") and "endpoint" in request.scope and request.scope["endpoint"]:
            return request.scope["route"].path
        
        # Otherwise, check all routes for a match
        for route in request.app.routes:
            match, child_scope = route.matches(request.scope)
            if match == Match.FULL:
                return route.path

        # Default to the raw URL path if no match found
        # This is less ideal as it could lead to high cardinality
        return request.url.path
