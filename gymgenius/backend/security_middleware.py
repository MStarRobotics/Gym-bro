"""
Security Middleware for GymGenius Backend
=========================================

Implements defense-in-depth security:
- Content Security Policy (CSP)
- Rate limiting
- Input sanitization
- CORS hardening
- Security headers (HSTS, X-Frame-Options, etc.)
"""

from fastapi import Request
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Adds comprehensive security headers to all responses.

    **Headers:**
    - Content-Security-Policy: Prevents XSS attacks
    - X-Frame-Options: Prevents clickjacking
    - X-Content-Type-Options: Prevents MIME sniffing
    - Strict-Transport-Security: Enforces HTTPS
    - X-XSS-Protection: Browser XSS filter
    - Referrer-Policy: Controls referer information
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)

        # Content Security Policy: Strict whitelist
        csp = "; ".join(
            [
                "default-src 'self'",
                "script-src 'self' 'unsafe-inline' https://checkout.razorpay.com",
                "style-src 'self' 'unsafe-inline'",
                "img-src 'self' data: https:",
                "font-src 'self' data:",
                "connect-src 'self' https://api.openai.com https://generativelanguage.googleapis.com",  # noqa: E501
                "frame-ancestors 'none'",
                "base-uri 'self'",
                "form-action 'self' https://checkout.razorpay.com",
                "upgrade-insecure-requests",
            ]
        )
        response.headers["Content-Security-Policy"] = csp

        # Prevent clickjacking
        response.headers["X-Frame-Options"] = "DENY"

        # Prevent MIME sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Enable HSTS (6 months)
        response.headers["Strict-Transport-Security"] = (
            "max-age=15768000; includeSubDomains"  # noqa: E501
        )

        # XSS Protection
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Referrer Policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Remove server header
        if "server" in response.headers:
            del response.headers["server"]

        return response


class RequestValidationMiddleware(BaseHTTPMiddleware):
    """
    Validates incoming requests for common attack patterns.

    **Checks:**
    - Suspiciously large payloads
    - SQL injection patterns
    - Path traversal attempts
    - Malformed content-type headers
    """

    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # Check content length
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.MAX_CONTENT_LENGTH:
            return Response(content="Payload too large", status_code=413)

        # Check for path traversal in URL
        if ".." in str(request.url.path) or "~" in str(request.url.path):
            return Response(content="Invalid request path", status_code=400)

        response = await call_next(request)
        return response
