class RefinementValidationError(Exception):
    def __init__(self, missing_fragments: list[str]) -> None:
        self.missing_fragments = missing_fragments
        super().__init__(f"Missing required fragments: {missing_fragments}")


def validate_input(message: str, max_length: int = 5000) -> None:
    if not message or not message.strip():
        raise ValueError("Message must not be empty or whitespace-only")
    if len(message) > max_length:
        raise ValueError(f"Message exceeds maximum length of {max_length} characters")


def validate_output(refined: str, critical_fragments: list[str]) -> None:
    if not refined.strip():
        raise RefinementValidationError(missing_fragments=["<empty output>"])

    missing = [f for f in critical_fragments if f not in refined]
    if missing:
        raise RefinementValidationError(missing_fragments=missing)
