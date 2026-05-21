from typing import Protocol

from app.domain.entities.staff_member import StaffMember


class StaffRepository(Protocol):
    def get_active_by_ids(self, ids: list[int]) -> list[StaffMember]: ...
