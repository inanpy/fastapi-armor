from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from typing import Optional


class ArmorMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        content_security_policy: Optional[str] = "default-src 'self';",
        frame_options: Optional[str] = "DENY",
        hsts: Optional[str] = "max-age=63072000; includeSubDomains; preload",
        x_content_type_options: Optional[str] = "nosniff",
        referrer_policy: Optional[str] = "no-referrer",
        permissions_policy: Optional[str] = "",
        dns_prefetch_control: Optional[str] = None,
        expect_ct: Optional[str] = None,
        origin_agent_cluster: Optional[str] = None,
        cross_origin_embedder_policy: Optional[str] = None,
        cross_origin_opener_policy: Optional[str] = None,
        cross_origin_resource_policy: Optional[str] = None,
    ):
        super().__init__(app)

        header_config = {
            "Content-Security-Policy": content_security_policy,
            "X-Frame-Options": frame_options,
            "Strict-Transport-Security": hsts,
            "X-Content-Type-Options": x_content_type_options,
            "Referrer-Policy": referrer_policy,
            "Permissions-Policy": permissions_policy,
            "X-DNS-Prefetch-Control": dns_prefetch_control,
            "Expect-CT": expect_ct,
            "Origin-Agent-Cluster": origin_agent_cluster,
            "Cross-Origin-Embedder-Policy": cross_origin_embedder_policy,
            "Cross-Origin-Opener-Policy": cross_origin_opener_policy,
            "Cross-Origin-Resource-Policy": cross_origin_resource_policy,
        }

        self.headers = {
            k: v for k, v in header_config.items() if v is not None
        }

    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        for header, value in self.headers.items():
            response.headers[header] = value
        return response
