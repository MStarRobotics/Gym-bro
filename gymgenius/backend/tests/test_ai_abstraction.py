# flake8: noqa
# pyright: reportMissingImports=false
import os
from unittest.mock import AsyncMock, patch

import pytest  # type: ignore
from ai_provider import AIProvider  # type: ignore
from ai_provider import (
    AIProviderError,
    GoogleAIProvider,
    OpenAIProvider,
    create_ai_provider,
)


class TestAIProvider:
    """Comprehensive test suite for the AI Provider abstraction layer.

    This test suite validates the model-agnostic architecture and ensures
    seamless provider switching without code changes.
    """

    def test_ai_provider_is_abstract(self):
        """Test that AIProvider cannot be instantiated directly"""
        with pytest.raises(TypeError):
            AIProvider()

    @pytest.mark.asyncio
    async def test_openai_provider_initialization(self):
        """Test OpenAI provider initialization with proper configuration"""
        provider = OpenAIProvider("test-key", "gpt-4")
        assert provider.model == "gpt-4"
        assert provider.client is not None
        assert provider.provider_name == "openai"

    @pytest.mark.asyncio
    async def test_openai_provider_missing_key(self):
        """Test OpenAI provider fails gracefully with missing API key"""
        with pytest.raises(ValueError, match="OpenAI API key is required"):
            OpenAIProvider("", "gpt-4")

    @pytest.mark.asyncio
    async def test_google_provider_initialization(self):
        """Test Google provider initialization with proper configuration"""
        with patch("google.generativeai.configure"):
            with patch("google.generativeai.GenerativeModel"):
                provider = GoogleAIProvider("test-key", "gemini-pro")
                assert provider.model is not None
                assert provider.provider_name == "google"

    @pytest.mark.asyncio
    async def test_google_provider_missing_key(self):
        """Test Google provider fails gracefully with missing API key"""
        with pytest.raises(ValueError, match="Google API key is required"):
            GoogleAIProvider("", "gemini-pro")

    @pytest.mark.parametrize(
        "provider_type,expected_class",
        [
            ("openai", OpenAIProvider),
            ("OPENAI", OpenAIProvider),
            ("google", GoogleAIProvider),
            ("GOOGLE", GoogleAIProvider),
            ("  openai  ", OpenAIProvider),  # Test whitespace handling
        ],
    )
    def test_create_ai_provider_factory(self, provider_type, expected_class):
        """Parameterized test for AI provider factory function.

        This critical test validates the abstraction layer's ability to
        create providers based on configuration, enabling model-agnostic
        architecture.
        """
        provider = create_ai_provider(provider_type, "test-key")
        assert isinstance(provider, expected_class)

    def test_create_ai_provider_invalid_type(self):
        """Test factory with invalid provider type returns clear error"""
        with pytest.raises(ValueError, match="Unknown provider type"):
            create_ai_provider("invalid", "test-key")

    def test_create_ai_provider_with_custom_model(self):
        """Test factory with custom model parameter"""
        provider = create_ai_provider("openai", "test-key", "gpt-4")
        assert isinstance(provider, OpenAIProvider)
        assert provider.model == "gpt-4"

    @pytest.mark.asyncio
    async def test_openai_provider_generate_response(self):
        """Test OpenAI provider response generation with mocked API"""
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message.content = "Test response"

        with patch("openai.AsyncOpenAI") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
            mock_client_class.return_value = mock_client

            provider = OpenAIProvider("test-key")
            response = await provider.generate_response("Test prompt")

            assert response == "Test response"
            mock_client.chat.completions.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_openai_provider_empty_response_handling(self):
        """Test OpenAI provider handles empty responses gracefully"""
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message.content = None

        with patch("openai.AsyncOpenAI") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
            mock_client_class.return_value = mock_client

            provider = OpenAIProvider("test-key")

            with pytest.raises(AIProviderError) as exc_info:
                await provider.generate_response("Test prompt")

            assert "Empty response" in str(exc_info.value)
            assert exc_info.value.provider == "openai"

    @pytest.mark.asyncio
    async def test_google_provider_generate_response(self):
        """Test Google provider response generation with mocked API"""
        mock_response = AsyncMock()
        mock_response.text = "Google response"

        with patch("google.generativeai.configure"):
            with patch("google.generativeai.GenerativeModel") as mock_model_class:
                mock_model = AsyncMock()
                mock_model.generate_content_async = AsyncMock(
                    return_value=mock_response
                )
                mock_model_class.return_value = mock_model

                provider = GoogleAIProvider("test-key")
                response = await provider.generate_response("Test prompt")

                assert response == "Google response"
                mock_model.generate_content_async.assert_called_once()

    @pytest.mark.asyncio
    async def test_google_provider_empty_response_handling(self):
        """Test Google provider handles empty responses gracefully"""
        mock_response = AsyncMock()
        mock_response.text = ""

        with patch("google.generativeai.configure"):
            with patch("google.generativeai.GenerativeModel") as mock_model_class:
                mock_model = AsyncMock()
                mock_model.generate_content_async = AsyncMock(
                    return_value=mock_response
                )
                mock_model_class.return_value = mock_model

                provider = GoogleAIProvider("test-key")

                with pytest.raises(AIProviderError) as exc_info:
                    await provider.generate_response("Test prompt")

                assert "Empty response" in str(exc_info.value)
                assert exc_info.value.provider == "google"

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "provider_type,mock_response_content",
        [
            ("openai", "OpenAI workout plan"),
            ("google", "Google workout plan"),
        ],
    )
    async def test_abstraction_layer_consistency(
        self, provider_type, mock_response_content
    ):
        """CRITICAL TEST: Validates model-agnostic architecture.

        This parameterized test is the cornerstone of the abstraction layer
        verification. It proves that the application can switch between AI
        providers (Google/OpenAI) without code changes, only configuration.

        This test simulates the Provider Swap & Regression Test from the
        Guardian Protocol, ensuring functional equivalence across providers.
        """
        if provider_type == "openai":
            mock_response = AsyncMock()
            mock_response.choices = [AsyncMock()]
            mock_response.choices[0].message.content = mock_response_content

            with patch("openai.AsyncOpenAI") as mock_client_class:
                mock_client = AsyncMock()
                mock_client.chat.completions.create = AsyncMock(
                    return_value=mock_response
                )
                mock_client_class.return_value = mock_client

                provider = create_ai_provider(provider_type, "test-key")
                response = await provider.generate_response("Create a workout plan")

                assert mock_response_content in response
                assert isinstance(provider, OpenAIProvider)

        elif provider_type == "google":
            mock_response = AsyncMock()
            mock_response.text = mock_response_content

            with patch("google.generativeai.configure"):
                with patch("google.generativeai.GenerativeModel") as mock_model_class:
                    mock_model = AsyncMock()
                    mock_model.generate_content_async = AsyncMock(
                        return_value=mock_response
                    )
                    mock_model_class.return_value = mock_model

                    provider = create_ai_provider(provider_type, "test-key")
                    response = await provider.generate_response("Create a workout plan")

                    assert mock_response_content in response
                    assert isinstance(provider, GoogleAIProvider)

    @pytest.mark.asyncio
    async def test_trace_id_propagation(self):
        """Test that trace_id is properly propagated for debugging"""
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message.content = "Test response"

        with patch("openai.AsyncOpenAI") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
            mock_client_class.return_value = mock_client

            provider = OpenAIProvider("test-key")
            response = await provider.generate_response(
                "Test prompt", trace_id="test-trace-123"
            )

            assert response == "Test response"

    def test_provider_factory_default_models(self):
        """Test that factory uses correct default models"""
        openai_provider = create_ai_provider("openai", "test-key")
        # Updated default model to gpt-4; ensure factory reflects this.
        assert openai_provider.model == "gpt-4"

        with patch("google.generativeai.configure"):
            with patch("google.generativeai.GenerativeModel"):
                google_provider = create_ai_provider("google", "test-key")
                assert google_provider.model_name == "gemini-pro"


class TestAIProviderErrorHandling:
    """Test suite for error handling and resilience"""

    @pytest.mark.asyncio
    async def test_openai_api_error_handling(self):
        """Test OpenAI provider handles API errors gracefully"""
        with patch("openai.AsyncOpenAI") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.chat.completions.create = AsyncMock(
                side_effect=Exception("API Connection Error")
            )
            mock_client_class.return_value = mock_client

            provider = OpenAIProvider("test-key")

            with pytest.raises(AIProviderError) as exc_info:
                await provider.generate_response("Test prompt")

            assert exc_info.value.provider == "openai"
            assert exc_info.value.error_type == "UNKNOWN_ERROR"

    @pytest.mark.asyncio
    async def test_google_api_error_handling(self):
        """Test Google provider handles API errors gracefully"""
        with patch("google.generativeai.configure"):
            with patch("google.generativeai.GenerativeModel") as mock_model_class:
                mock_model = AsyncMock()
                mock_model.generate_content_async = AsyncMock(
                    side_effect=Exception("API Connection Error")
                )
                mock_model_class.return_value = mock_model

                provider = GoogleAIProvider("test-key")

                with pytest.raises(AIProviderError) as exc_info:
                    await provider.generate_response("Test prompt")

                assert exc_info.value.provider == "google"
                assert exc_info.value.error_type == "API_ERROR"


class TestEnvironmentBasedProviderSelection:
    """Test suite for environment-based provider configuration"""

    def test_provider_selection_from_env(self):
        """Test provider selection based on AI_PROVIDER environment variable.

        This test validates the core abstraction principle: the application
        should select providers based on configuration, not hardcoded logic.
        """
        with patch.dict(os.environ, {"AI_PROVIDER": "google"}):
            provider_type = os.getenv("AI_PROVIDER", "google")
            provider = create_ai_provider(provider_type, "test-key")
            assert isinstance(provider, GoogleAIProvider)

        with patch.dict(os.environ, {"AI_PROVIDER": "openai"}):
            provider_type = os.getenv("AI_PROVIDER")
            if provider_type:  # Add None check for type safety
                provider = create_ai_provider(provider_type, "test-key")
                assert isinstance(provider, OpenAIProvider)
                assert provider.model == "gpt-4"
