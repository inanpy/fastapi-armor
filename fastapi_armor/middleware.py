from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.types import ASGIApp
from fastapi_armor.presets import PRESETS
from fastapi_armor.header_map import PARAM_TO_HEADER


class ArmorMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, preset: str = None, **custom_headers):
        headers = PRESETS.get(preset, {}).copy() if preset else {}

        for param_name, value in custom_headers.items():
            if param_name not in PARAM_TO_HEADER:
                continue
            header_name = PARAM_TO_HEADER[param_name]
            if value is None:
                headers.pop(header_name, None)
            else:
                headers[header_name] = value

        self.headers = headers
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        for header_name, header_value in self.headers.items():
            response.headers[header_name] = header_value

        return response
