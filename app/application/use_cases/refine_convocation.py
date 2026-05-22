import logging
from dataclasses import dataclass

from app.application.ports.ai_provider import AIRefinementProvider
from app.application.services.refinement_prompt_builder import build_initial_prompt, build_retry_prompt
from app.application.validators.refinement_validator import (
    RefinementValidationError,
    validate_input,
    validate_output,
)
from app.infrastructure.ai.openai_adapter import AIProviderError

logger = logging.getLogger(__name__)


@dataclass
class RefineConvocationResult:
    message: str
    was_refined: bool


class RefineConvocationUseCase:
    def __init__(self, provider: AIRefinementProvider) -> None:
        self._provider = provider

    def execute(
        self,
        message: str,
        critical_fragments: list[str],
        style: str | None = None,
    ) -> RefineConvocationResult:
        validate_input(message)

        logger.info(
            "refinement.started",
            extra={
                "style": style,
                "message_length": len(message),
                "critical_fragment_count": len(critical_fragments),
            },
        )

        # Initial attempt
        try:
            system_prompt, user_prompt = build_initial_prompt(message, style)
            logger.info(
                "refinement.provider_call",
                extra={"provider": "openai", "retry_attempt": 1},
            )
            raw = self._provider.refine(system_prompt, user_prompt)
        except AIProviderError:
            logger.warning(
                "refinement.fallback_original_returned",
                extra={"reason": "provider_error"},
            )
            return RefineConvocationResult(message=message, was_refined=False)

        logger.info(
            "refinement.raw_output_received",
            extra={"ai_output": raw, "output_length": len(raw), "retry_attempt": 1},
        )

        try:
            validate_output(raw, critical_fragments)
            logger.info(
                "refinement.completed",
                extra={"was_refined": True, "retry_needed": False, "output_length": len(raw)},
            )
            return RefineConvocationResult(message=raw, was_refined=True)
        except RefinementValidationError as e:
            missing_fragments = e.missing_fragments
            logger.warning(
                "refinement.validation_failed",
                extra={
                    "missing_fragments": missing_fragments,
                    "ai_output": raw,
                    "retry_attempt": 1,
                },
            )

        # Retry loop — maximum 2 retries (attempt 2, then attempt 3)
        for attempt in range(2, 4):
            logger.info(
                "refinement.retry_started",
                extra={"retry_attempt": attempt, "missing_fragments": missing_fragments},
            )

            try:
                system_prompt_r, user_prompt_r = build_retry_prompt(message, style, missing_fragments)
                logger.info(
                    "refinement.provider_call",
                    extra={"provider": "openai", "retry_attempt": attempt},
                )
                raw_retry = self._provider.refine(system_prompt_r, user_prompt_r)
            except AIProviderError:
                logger.warning(
                    "refinement.fallback_original_returned",
                    extra={"reason": "provider_error", "retry_attempt": attempt},
                )
                return RefineConvocationResult(message=message, was_refined=False)

            logger.info(
                "refinement.raw_output_received",
                extra={
                    "ai_output": raw_retry,
                    "output_length": len(raw_retry),
                    "retry_attempt": attempt,
                },
            )

            try:
                validate_output(raw_retry, critical_fragments)
                logger.info(
                    "refinement.completed",
                    extra={
                        "was_refined": True,
                        "retry_needed": True,
                        "retry_attempt": attempt,
                        "output_length": len(raw_retry),
                    },
                )
                return RefineConvocationResult(message=raw_retry, was_refined=True)
            except RefinementValidationError as e:
                missing_fragments = e.missing_fragments
                logger.warning(
                    "refinement.retry_failed",
                    extra={
                        "retry_output": raw_retry,
                        "retry_missing_fragments": missing_fragments,
                        "retry_attempt": attempt,
                    },
                )

        logger.warning(
            "refinement.fallback_original_returned",
            extra={"reason": "retries_exhausted"},
        )
        return RefineConvocationResult(message=message, was_refined=False)
