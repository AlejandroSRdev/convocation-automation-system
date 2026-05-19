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

        logger.info("refinement.started")

        try:
            system_prompt, user_prompt = build_initial_prompt(message, style)
            raw = self._provider.refine(system_prompt, user_prompt)
        except AIProviderError:
            logger.warning("refinement.fallback", extra={"reason": "provider_error"})
            return RefineConvocationResult(message=message, was_refined=False)

        try:
            validate_output(raw, critical_fragments)
            logger.info("refinement.completed", extra={"was_refined": True})
            return RefineConvocationResult(message=raw, was_refined=True)
        except RefinementValidationError as e:
            logger.warning(
                "refinement.validation_failed",
                extra={"missing_fragments": e.missing_fragments},
            )

        try:
            system_prompt_r, user_prompt_r = build_retry_prompt(message, style, e.missing_fragments)
            raw_retry = self._provider.refine(system_prompt_r, user_prompt_r)
            validate_output(raw_retry, critical_fragments)
            logger.info("refinement.completed", extra={"was_refined": True, "attempt": 2})
            return RefineConvocationResult(message=raw_retry, was_refined=True)
        except (RefinementValidationError, AIProviderError):
            logger.warning("refinement.fallback", extra={"reason": "semantic_retry_exhausted"})
            return RefineConvocationResult(message=message, was_refined=False)
