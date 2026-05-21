from fastapi import APIRouter, Depends

from app.application.use_cases.get_staff_members import GetStaffMembersUseCase
from app.presentation.dependencies import get_get_staff_members_use_case
from app.presentation.schemas.staff_member import StaffMemberResponse

router = APIRouter(prefix="/staff-members", tags=["staff-members"])


@router.get("/", response_model=list[StaffMemberResponse])
def list_staff_members(
    use_case: GetStaffMembersUseCase = Depends(get_get_staff_members_use_case),
) -> list[StaffMemberResponse]:
    result = use_case.execute()
    return [
        StaffMemberResponse(
            id=member.id,
            name=member.name,
            role=member.role,
            active=member.active,
        )
        for member in result.staff_members
    ]
