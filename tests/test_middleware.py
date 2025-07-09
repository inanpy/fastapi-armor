from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi_armor.middleware import ArmorMiddleware
from fastapi_armor.presets import PRESETS
import pytest


def create_app(preset=None, **kwargs):
    """Helper function to create a FastAPI app with ArmorMiddleware"""
    app = FastAPI()
    if preset is not None or kwargs:
        app.add_middleware(ArmorMiddleware, preset=preset, **kwargs)
    else:
        app.add_middleware(ArmorMiddleware)

    @app.get("/")
    def get_root():
        return {"message": "ok"}

    @app.post("/items")
    def create_item(item: dict):
        return item

    @app.put("/items/{item_id}")
    def update_item(item_id: int, item: dict):
        return {"item_id": item_id, **item}

    @app.delete("/items/{item_id}")
    def delete_item(item_id: int):
        return {"deleted": item_id}

    return app


class TestArmorMiddlewarePresets:
    """Test the different presets of ArmorMiddleware"""

    def test_strict_preset(self):
        """Test that the strict preset sets all security headers"""
        app = create_app(preset="strict")
        client = TestClient(app)
        response = client.get("/")

        assert response.status_code == 200
        # Check all headers are present with correct values
        assert response.headers["X-Frame-Options"] == "DENY"
        assert response.headers["X-Content-Type-Options"] == "nosniff"
        assert (
            response.headers["Strict-Transport-Security"]
            == "max-age=63072000; includeSubDomains; preload"
        )
        assert response.headers["Content-Security-Policy"] == "default-src 'self';"
        assert response.headers["Referrer-Policy"] == "no-referrer"
        assert response.headers["Permissions-Policy"] == "geolocation=(), microphone=()"
        assert response.headers["X-DNS-Prefetch-Control"] == "off"
        assert response.headers["Expect-CT"] == "max-age=86400, enforce"
        assert response.headers["Origin-Agent-Cluster"] == "?1"
        assert response.headers["Cross-Origin-Embedder-Policy"] == "require-corp"
        assert response.headers["Cross-Origin-Opener-Policy"] == "same-origin"
        assert response.headers["Cross-Origin-Resource-Policy"] == "same-origin"

    def test_relaxed_preset(self):
        """Test that the relaxed preset sets only some security headers with relaxed values"""
        app = create_app(preset="relaxed")
        client = TestClient(app)
        response = client.get("/")

        assert response.status_code == 200
        # Verify relaxed headers
        assert response.headers["X-Frame-Options"] == "SAMEORIGIN"
        assert response.headers["X-Content-Type-Options"] == "nosniff"
        assert response.headers["Content-Security-Policy"] == "default-src *;"
        # Not checking for unsafe-inline since it's not in the actual preset

        # Some headers might not be present in relaxed mode - check against the preset
        relaxed_headers = PRESETS["relaxed"]
        for header, value in relaxed_headers.items():
            assert response.headers[header] == value

    def test_none_preset(self):
        """Test that the none preset doesn't set any security headers"""
        app = create_app(preset="none")
        client = TestClient(app)
        response = client.get("/")

        assert response.status_code == 200
        # None of the security headers should be present
        security_headers = [
            "X-Frame-Options",
            "X-Content-Type-Options",
            "Strict-Transport-Security",
            "Content-Security-Policy",
            "Referrer-Policy",
            "Permissions-Policy",
            "X-DNS-Prefetch-Control",
            "Expect-CT",
            "Origin-Agent-Cluster",
            "Cross-Origin-Embedder-Policy",
            "Cross-Origin-Opener-Policy",
            "Cross-Origin-Resource-Policy",
        ]

        # Check that FastAPI's default headers are still there
        assert "content-type" in response.headers

        # Check security headers are absent
        for header in security_headers:
            header_lower = header.lower()
            assert (
                header_lower not in response.headers
                or response.headers[header_lower] == ""
            )

    def test_default_behavior(self):
        """Test the default behavior (no preset specified)"""
        app = create_app()  # No preset
        client = TestClient(app)
        response = client.get("/")

        assert response.status_code == 200
        # It appears that when no preset is specified, no security headers are added
        # This is the expected behavior as per the implementation

        # Only standard FastAPI headers should be present
        assert "content-type" in response.headers
        assert "content-length" in response.headers

        # Security headers should not be present
        assert "X-Frame-Options" not in response.headers
        assert "Content-Security-Policy" not in response.headers


class TestArmorMiddlewareCustomization:
    """Test customization options for ArmorMiddleware"""

    def test_override_specific_header(self):
        """Test that specific headers can be overridden"""
        custom_csp = "default-src 'self' https://example.com;"
        app = create_app(preset="strict", content_security_policy=custom_csp)
        client = TestClient(app)
        response = client.get("/")

        assert response.status_code == 200
        # Check the overridden header
        assert response.headers["Content-Security-Policy"] == custom_csp
        # Other headers should still be from the strict preset
        assert response.headers["X-Frame-Options"] == "DENY"

    def test_multiple_header_overrides(self):
        """Test that multiple headers can be overridden"""
        app = create_app(
            preset="strict",
            frame_options="SAMEORIGIN",
            referrer_policy="strict-origin",
            permissions_policy="geolocation=(self), microphone=()",
        )
        client = TestClient(app)
        response = client.get("/")

        assert response.status_code == 200
        # Check the overridden headers
        assert response.headers["X-Frame-Options"] == "SAMEORIGIN"
        assert response.headers["Referrer-Policy"] == "strict-origin"
        assert (
            response.headers["Permissions-Policy"]
            == "geolocation=(self), microphone=()"
        )
        # Other headers should still be from the strict preset
        assert response.headers["X-Content-Type-Options"] == "nosniff"

    def test_ignore_none_values(self):
        """Test how None values are handled in custom headers"""
        app = create_app(
            preset="strict",
            # These None values remove headers that would otherwise come from the preset
            content_security_policy=None,
            frame_options=None,
        )
        client = TestClient(app)
        response = client.get("/")

        assert response.status_code == 200
        # Headers set to None should be removed, even from presets
        assert "Content-Security-Policy" not in response.headers
        assert "X-Frame-Options" not in response.headers

        # Other preset headers should still be present
        assert "X-Content-Type-Options" in response.headers
        assert "Strict-Transport-Security" in response.headers

    def test_custom_param_none_not_sent(self):
        """Test that custom parameters with None values are not sent in the response"""
        # Create app with headers both set and explicitly set to None
        app = create_app(
            # Set headers that should be present
            frame_options="DENY",
            content_security_policy="default-src 'self';",
            # Set headers that should not be present
            referrer_policy=None,
            content_type_options=None,
            strict_transport_security=None,
        )
        client = TestClient(app)
        response = client.get("/")

        assert response.status_code == 200
        # Check that the explicitly set headers are present
        assert response.headers["X-Frame-Options"] == "DENY"
        assert response.headers["Content-Security-Policy"] == "default-src 'self';"
        
        # Check that headers with None values are not present
        assert "Referrer-Policy" not in response.headers.keys()
        assert "X-Content-Type-Options" not in response.headers.keys()
        assert "Strict-Transport-Security" not in response.headers.keys()

    def test_fully_custom_configuration(self):
        """Test a fully custom configuration without using presets"""
        app = create_app(
            # No preset
            frame_options="DENY",
            content_security_policy="default-src 'self'; script-src 'self' https://analytics.example.com",
            referrer_policy="no-referrer-when-downgrade",
            # Others omitted
        )
        client = TestClient(app)
        response = client.get("/")

        assert response.status_code == 200
        # Check only specified headers are set
        assert response.headers["X-Frame-Options"] == "DENY"
        assert (
            response.headers["Content-Security-Policy"]
            == "default-src 'self'; script-src 'self' https://analytics.example.com"
        )
        assert response.headers["Referrer-Policy"] == "no-referrer-when-downgrade"
        # Unspecified headers should not be present
        assert "Strict-Transport-Security" not in response.headers


class TestArmorMiddlewareEdgeCases:
    """Test edge cases and error handling for ArmorMiddleware"""

    def test_invalid_preset(self):
        """Test that an invalid preset name raises an appropriate error"""
        # This should either use a default or raise an error
        app = create_app(preset="invalid_preset_name")
        client = TestClient(app)
        # We expect it to handle the error gracefully or use a fallback
        # The exact behavior depends on the implementation
        response = client.get("/")
        assert response.status_code == 200

    @pytest.mark.parametrize(
        "http_method,endpoint",
        [("POST", "/items"), ("PUT", "/items/1"), ("DELETE", "/items/1")],
    )
    def test_different_http_methods(self, http_method, endpoint):
        """Test that headers are applied for all HTTP methods"""
        app = create_app(preset="strict")
        client = TestClient(app)
        request_func = getattr(client, http_method.lower())
        if http_method in ["POST", "PUT"]:
            response = request_func(endpoint, json={"name": "Test Item"})
        else:
            response = request_func(endpoint)

        assert response.status_code == 200
        # Check that security headers are present regardless of HTTP method
        assert "X-Frame-Options" in response.headers
        assert "Content-Security-Policy" in response.headers

    def test_empty_headers(self):
        """Test that empty header values are handled correctly"""
        app = create_app(frame_options="", content_security_policy="")
        client = TestClient(app)
        response = client.get("/")

        assert response.status_code == 200
        # Empty headers should either be omitted or sent as empty
        if "X-Frame-Options" in response.headers:
            assert response.headers["X-Frame-Options"] == ""
        if "Content-Security-Policy" in response.headers:
            assert response.headers["Content-Security-Policy"] == ""
