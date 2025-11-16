# flake8: noqa
# pyright: reportMissingImports=false
import logging
import uuid
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Optional

import google.generativeai as genai  # type: ignore
import openai  # type: ignore

# Configure structured logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class AIProviderError(Exception):
    """Base exception for AI provider errors"""

    def __init__(self, message: str, provider: str, error_type: str, trace_id: str):
        self.message = message
        self.provider = provider
        self.error_type = error_type
        self.trace_id = trace_id
        super().__init__(self.message)


class AIProvider(ABC):
    """Abstract base class for AI providers - enables model-agnostic
    architecture"""

    model: str  # Common attribute for all providers
    model_name: str  # Common attribute for all providers

    @abstractmethod
    async def generate_response(
        self, prompt: str, trace_id: Optional[str] = None
    ) -> str:
        """Generate AI response with error handling and logging"""
        pass

    def _log_request(self, prompt: str, trace_id: str, provider_name: str) -> None:
        """Log AI request with structured data for debugging"""
        logger.info(
            f"AI_REQUEST: Generating response | "
            f"provider={provider_name} | "
            f"prompt_length={len(prompt)} | "
            f"trace_id={trace_id} | "
            f"timestamp={datetime.now(timezone.utc).isoformat()}"
        )

    def _log_response(
        self, response: str, trace_id: str, provider_name: str, duration_ms: float
    ) -> None:
        """Log AI response with performance metrics"""
        logger.info(
            f"AI_RESPONSE: Response generated | "
            f"provider={provider_name} | "
            f"response_length={len(response)} | "
            f"duration_ms={duration_ms:.2f} | "
            f"trace_id={trace_id} | "
            f"timestamp={datetime.now(timezone.utc).isoformat()}"
        )

    def _log_error(self, error: Exception, trace_id: str, provider_name: str) -> None:
        """Log AI error with full context for debugging"""
        logger.error(
            f"AI_PROVIDER_ERROR: Failed to generate response | "
            f"provider={provider_name} | "
            f"error_type={type(error).__name__} | "
            f"error_message={str(error)} | "
            f"trace_id={trace_id} | "
            f"timestamp={datetime.now(timezone.utc).isoformat()}",
            exc_info=True,
        )


class OpenAIProvider(AIProvider):
    """OpenAI GPT provider implementation with error handling"""

    def __init__(self, api_key: str, model: str = "gpt-4"):
        if not api_key:
            raise ValueError("OpenAI API key is required")
        self.client = openai.AsyncOpenAI(api_key=api_key)
        self.model = model
        self.model_name = model  # Add for consistency with base class
        self.provider_name = "openai"
        logger.info(f"OpenAIProvider initialized | model={model}")

    async def generate_response(
        self, prompt: str, trace_id: Optional[str] = None
    ) -> str:
        trace_id = trace_id or str(uuid.uuid4())
        start_time = datetime.now(timezone.utc)

        try:
            self._log_request(prompt, trace_id, self.provider_name)

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2000,
            )

            content = response.choices[0].message.content
            if not content:
                raise AIProviderError(
                    "Empty response from OpenAI",
                    self.provider_name,
                    "EMPTY_RESPONSE",
                    trace_id,
                )

            duration_ms = (
                datetime.now(timezone.utc) - start_time
            ).total_seconds() * 1000
            self._log_response(content, trace_id, self.provider_name, duration_ms)

            return content

        except openai.RateLimitError as e:
            self._log_error(e, trace_id, self.provider_name)
            raise AIProviderError(
                f"OpenAI rate limit exceeded: {str(e)}",
                self.provider_name,
                "RATE_LIMIT",
                trace_id,
            )
        except openai.APIError as e:
            self._log_error(e, trace_id, self.provider_name)
            raise AIProviderError(
                f"OpenAI API error: {str(e)}", self.provider_name, "API_ERROR", trace_id
            )
        except Exception as e:
            self._log_error(e, trace_id, self.provider_name)
            raise AIProviderError(
                f"Unexpected error: {str(e)}",
                self.provider_name,
                "UNKNOWN_ERROR",
                trace_id,
            )


class GoogleAIProvider(AIProvider):
    """Google Gemini provider implementation with error handling"""

    def __init__(self, api_key: str, model: str = "gemini-pro"):
        if not api_key:
            raise ValueError("Google API key is required")
        genai.configure(api_key=api_key)
        self._model_obj = genai.GenerativeModel(model)
        self.model = model  # Store model name as string for base class
        self.model_name = model
        self.provider_name = "google"
        logger.info(f"GoogleAIProvider initialized | model={model}")

    async def generate_response(
        self, prompt: str, trace_id: Optional[str] = None
    ) -> str:
        trace_id = trace_id or str(uuid.uuid4())
        start_time = datetime.now(timezone.utc)

        try:
            self._log_request(prompt, trace_id, self.provider_name)

            response = await self._model_obj.generate_content_async(prompt)

            if not response.text:
                raise AIProviderError(
                    "Empty response from Google AI",
                    self.provider_name,
                    "EMPTY_RESPONSE",
                    trace_id,
                )

            duration_ms = (
                datetime.now(timezone.utc) - start_time
            ).total_seconds() * 1000
            self._log_response(response.text, trace_id, self.provider_name, duration_ms)

            return response.text

        except Exception as e:
            self._log_error(e, trace_id, self.provider_name)
            raise AIProviderError(
                f"Google AI error: {str(e)}", self.provider_name, "API_ERROR", trace_id
            )


def create_ai_provider(
    provider_type: str, api_key: str, model: Optional[str] = None
) -> AIProvider:
    """Factory function to create AI provider instances.

    Args:
        provider_type: 'openai' or 'google'
        api_key: API key for the provider
        model: Optional model name override

    Returns:
        AIProvider instance

    Raises:
        ValueError: If provider_type is not supported
    """
    provider_type = provider_type.lower().strip()

    logger.info(
        f"AI_PROVIDER_FACTORY: Creating provider | "
        f"provider_type={provider_type} | "
        f"model={model or 'default'} | "
        f"timestamp={datetime.now(timezone.utc).isoformat()}"
    )

    if provider_type == "openai":
        return OpenAIProvider(api_key, model or "gpt-4")
    elif provider_type == "google":
        return GoogleAIProvider(api_key, model or "gemini-pro")
    else:
        logger.error(
            f"AI_PROVIDER_FACTORY_ERROR: Unknown provider type | "
            f"provider_type={provider_type} | "
            f"timestamp={datetime.now(timezone.utc).isoformat()}"
        )
        raise ValueError(
            f"Unknown provider type: {provider_type}. Supported: 'openai', 'google'"
        )
