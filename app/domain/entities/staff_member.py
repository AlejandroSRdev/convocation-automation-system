import uuid
from dataclasses import dataclass


@dataclass
class StaffMember:
    id: uuid.UUID
    name: str
    role: str
    active: bool
