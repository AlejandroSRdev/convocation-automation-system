from pydantic import BaseModel


class PlayerResponse(BaseModel):
    id: int
    name: str
    number: int | None
    active: bool
