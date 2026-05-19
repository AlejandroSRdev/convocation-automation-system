from typing import Protocol


class AIRefinementProvider(Protocol):
    def refine(self, system_prompt: str, user_prompt: str) -> str: ...
