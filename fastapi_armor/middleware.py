from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.types import ASGIApp
from fastapi_armor.presets import PRESETS


class ArmorMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, preset: str = None, **custom_headers):
        headers = PRESETS.get(preset, {}).copy() if preset else {}

        for key, value in custom_headers.items():
            if value is not None:
                headers[key] = value

        self.headers = headers
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        for header_name, header_value in self.headers.items():
            response.headers[header_name] = header_value

        return response
