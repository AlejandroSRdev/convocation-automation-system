import logging
import time

import openai

logger = logging.getLogger(__name__)

_RETRYABLE_ERRORS = (
    openai.APITimeoutError,
    openai.RateLimitError,
    openai.APIConnectionError,
    openai.APIStatusError,
)


class AIProviderError(Exception):
    pass


class OpenAIAdapter:
    def __init__(self, api_key: str) -> None:
        self._client = openai.OpenAI(api_key=api_key)

    def refine(self, system_prompt: str, user_prompt: str) -> str:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        model = "gpt-4o-mini"
        max_tokens = 800

        try:
            response = self._client.chat.completions.create(
                model=model,
                temperature=0.3,
                max_tokens=max_tokens,
                messages=messages,
            )
        except _RETRYABLE_ERRORS as first_error:
            logger.warning("refinement.provider_retry", extra={"attempt": 2})
            time.sleep(1)
            try:
                response = self._client.chat.completions.create(
                    model=model,
                    temperature=0.3,
                    max_tokens=max_tokens,
                    messages=messages,
                )
            except _RETRYABLE_ERRORS as second_error:
                logger.error("refinement.provider_error", extra={"error": str(second_error)})
                raise AIProviderError(f"Provider failed after retry: {second_error}") from second_error

        content = response.choices[0].message.content.strip()
        if not content:
            raise AIProviderError("Provider returned empty response")

        return content
