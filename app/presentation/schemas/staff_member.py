from pydantic import BaseModel


class StaffMemberResponse(BaseModel):
    id: int
    name: str
    role: str
    active: bool
