import logging
from dataclasses import dataclass

from app.application.ports.staff_repository import StaffRepository
from app.domain.entities.staff_member import StaffMember

logger = logging.getLogger(__name__)


@dataclass
class GetStaffMembersResult:
    staff_members: list[StaffMember]


class GetStaffMembersUseCase:
    def __init__(self, staff_repository: StaffRepository) -> None:
        self._staff_repo = staff_repository

    def execute(self) -> GetStaffMembersResult:
        logger.info("get_staff_members.started")
        staff_members = self._staff_repo.get_active()
        logger.info("get_staff_members.completed", extra={"count": len(staff_members)})
        return GetStaffMembersResult(staff_members=staff_members)
