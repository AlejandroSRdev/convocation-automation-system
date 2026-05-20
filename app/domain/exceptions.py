class MatchNotFoundError(Exception):
    def __init__(self, match_id: str) -> None:
        super().__init__(f"Match not found: {match_id}")
