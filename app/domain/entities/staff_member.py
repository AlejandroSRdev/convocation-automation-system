from dataclasses import dataclass


@dataclass
class StaffMember:
    id: int
    name: str
    role: str
    active: bool
