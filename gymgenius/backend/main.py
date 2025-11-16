import html
import logging
import os
import re
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from ai_provider import AIProvider, AIProviderError, create_ai_provider
from fastapi import Body, Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Initialize FastAPI app with security headers
app = FastAPI(
    title="GymGenius Backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add rate limiter to app
app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded, _rate_limit_exceeded_handler  # type: ignore
)

# Configure CORS with security in mind
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)


# Input Sanitization Utility
class InputSanitizer:
    """Sanitize user input to prevent XSS and injection attacks"""

    @staticmethod
    def sanitize_text(text: str, max_length: int = 10000) -> str:
        """Sanitize text input by removing dangerous patterns"""
        if not text:
            return ""

        # Truncate to max length
        text = text[:max_length]

        # Remove potentially dangerous patterns first
        dangerous_patterns = [
            r"<script[^>]*>.*?</script>",
            r"javascript:",
            r"on\w+\s*=",
            r"<iframe[^>]*>.*?</iframe>",
        ]

        original_text = text
        for pattern in dangerous_patterns:
            text = re.sub(pattern, "", text, flags=re.IGNORECASE)

        # HTML escape the remaining content to prevent XSS
        text = html.escape(text)

        if text != original_text:
            logger.warning(
                f"INPUT_SANITIZATION: Potentially unsafe input cleaned | "
                f"original_length={len(original_text)} | "
                f"sanitized_length={len(text)} | "
                f"timestamp={datetime.now(timezone.utc).isoformat()}"
            )

        return text


# Request Models with Validation
class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=5000)
    provider_type: str = Field(default="google", pattern="^(google|openai)$")
    model: Optional[str] = Field(default=None, max_length=100)
    user_id: Optional[str] = Field(default=None, max_length=100)

    @validator("prompt")
    def sanitize_prompt(cls, v):
        return InputSanitizer.sanitize_text(v)

    @validator("model")
    def sanitize_model(cls, v):
        if v:
            return InputSanitizer.sanitize_text(v, max_length=100)
        return v


class ChatRequest(BaseModel):
    """Request model for /api/chat endpoint"""

    message: str = Field(..., min_length=1, max_length=5000)
    context: Optional[Dict[str, Any]] = None
    user_id: Optional[str] = Field(default=None, max_length=100)

    @validator("message")
    def sanitize_message(cls, v):
        return InputSanitizer.sanitize_text(v)


# Dependency Injection for AI Provider
def get_generate_request(
    generate_request: GenerateRequest = Body(...),
):
    """Dependency helper to bind GenerateRequest to request body

    This allows other dependencies (like `get_ai_provider`) to depend on
    this body binding without causing duplicated body parameters in
    OpenAPI schema generation.
    """
    return generate_request


def get_ai_provider(
    generate_request: GenerateRequest = Depends(get_generate_request),
) -> AIProvider:
    """Dependency injection factory for AI provider.

    Reads configuration from environment variables and creates
    the appropriate provider instance.
    """
    trace_id = str(uuid.uuid4())

    # Secure secrets management - load from environment only
    provider_type = generate_request.provider_type.lower()
    api_key = None

    if provider_type == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
    elif provider_type == "google":
        api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        logger.error(
            f"API_KEY_ERROR: API key not configured | "
            f"provider={provider_type} | "
            f"trace_id={trace_id} | "
            f"timestamp={datetime.now(timezone.utc).isoformat()}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "configuration_error",
                "message": "AI service temporarily unavailable",
                "user_message": (
                    "I'm having trouble connecting to my AI systems right "
                    "now. This is usually temporary. Please try again in "
                    "a moment!"
                ),
                "trace_id": trace_id,
            },
        )

    try:
        return create_ai_provider(
            provider_type, api_key, generate_request.model
        )
    except ValueError as e:
        logger.error(
            f"PROVIDER_CREATION_ERROR: {str(e)} | "
            f"trace_id={trace_id} | "
            f"timestamp={datetime.now(timezone.utc).isoformat()}"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "invalid_provider",
                "message": str(e),
                "trace_id": trace_id,
            },
        )


# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global error handler with empathetic user messaging"""
    trace_id = str(uuid.uuid4())

    logger.error(
        f"UNHANDLED_EXCEPTION: {type(exc).__name__} | "
        f"error={str(exc)} | "
        f"path={request.url.path} | "
        f"trace_id={trace_id} | "
        f"timestamp={datetime.now(timezone.utc).isoformat()}",
        exc_info=True,
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "internal_server_error",
            "message": "An unexpected error occurred",
            "user_message": (
                "Something unexpected happened on our end. Don't worry—your "
                "data is safe! Please try again, and if this continues, "
                "let us know."
            ),
            "trace_id": trace_id,
        },
    )


# Health Check Endpoint
@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "GymGenius Backend",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check with environment validation"""
    google_key_configured = bool(os.getenv("GOOGLE_API_KEY"))
    openai_key_configured = bool(os.getenv("OPENAI_API_KEY"))
    default_provider = os.getenv("AI_PROVIDER", "google")

    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "api_keys": {
            "google": (
                "configured" if google_key_configured else "not_configured"
            ),
            "openai": (
                "configured" if openai_key_configured else "not_configured"
            ),
        },
        "default_provider": default_provider,
    }


# AI Chat Endpoint (User-Facing)
@app.post("/api/chat", tags=["AI"])
@limiter.limit("20/minute")  # Rate limiting
async def chat(request: Request, chat_request: ChatRequest):
    """Main chatbot endpoint with empathetic error handling.

    This endpoint demonstrates the 'Genius Concierge' AI personality.
    """
    trace_id = str(uuid.uuid4())

    logger.info(
        f"CHAT_REQUEST: Received chat message | "
        f"user_id={chat_request.user_id or 'anonymous'} | "
        f"message_length={len(chat_request.message)} | "
        f"trace_id={trace_id} | "
        f"timestamp={datetime.now(timezone.utc).isoformat()}"
    )

    try:
        # Get AI provider from environment
        provider_type = os.getenv("AI_PROVIDER", "google")
        api_key = (
            os.getenv("OPENAI_API_KEY")
            if provider_type == "openai"
            else os.getenv("GOOGLE_API_KEY")
        )

        if not api_key:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error": "configuration_error",
                    "user_message": (
                        "I'm having trouble connecting right now. "
                        "Please try again in a moment!"
                    ),
                    "trace_id": trace_id,
                },
            )

        provider = create_ai_provider(provider_type, api_key)

        # Generate response
        response_text = await provider.generate_response(
            chat_request.message, trace_id=trace_id
        )

        return {
            "response": response_text,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "trace_id": trace_id,
        }

    except AIProviderError as e:
        logger.error(
            f"CHAT_AI_ERROR: {e.message} | "
            f"provider={e.provider} | "
            f"error_type={e.error_type} | "
            f"trace_id={e.trace_id}"
        )

        # Empathetic error message
        user_message = (
            "I'm taking a bit longer than usual to respond. "
            "This sometimes happens when I'm thinking really hard! "
            "Could you try asking again?"
        )

        if e.error_type == "RATE_LIMIT":
            user_message = (
                "Whoa, you're on fire with questions! Give me just a "
                "moment to catch up, then we can continue. 😊"
            )

        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "error": e.error_type.lower(),
                "user_message": user_message,
                "trace_id": e.trace_id,
            },
        )


# Generate Endpoint (Model-Agnostic Testing)
@app.post("/generate", tags=["AI"])
@limiter.limit("5/minute")
async def generate_response(
    request: Request,
    generate_request: GenerateRequest = Depends(),
    provider: AIProvider = Depends(get_ai_provider),
):
    """Model-agnostic generation endpoint for testing abstraction layer."""
    trace_id = str(uuid.uuid4())

    logger.info(
        f"GENERATE_REQUEST: Received generation request | "
        f"provider={generate_request.provider_type} | "
        f"model={generate_request.model or 'default'} | "
        f"trace_id={trace_id}"
    )

    try:
        response_text = await provider.generate_response(
            generate_request.prompt, trace_id=trace_id
        )

        return {
            "response": response_text,
            "provider": generate_request.provider_type,
            "model": generate_request.model,
            "trace_id": trace_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except AIProviderError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error": e.error_type,
                "message": e.message,
                "provider": e.provider,
                "trace_id": e.trace_id,
            },
        )
    except Exception as e:
        logger.error(
            f"GENERATE_ERROR: Unexpected error | "
            f"error={str(e)} | "
            f"trace_id={trace_id}",
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "internal_error",
                "message": str(e),
                "trace_id": trace_id,
            },
        )
