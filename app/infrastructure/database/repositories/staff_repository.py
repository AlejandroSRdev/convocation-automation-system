from sqlalchemy.orm import Session

from app.domain.entities.staff_member import StaffMember
from app.infrastructure.database.models.staff_member import StaffMemberModel


class SQLStaffRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_active(self) -> list[StaffMember]:
        models = (
            self._session.query(StaffMemberModel)
            .filter(StaffMemberModel.active == True)
            .order_by(StaffMemberModel.id.asc())
            .all()
        )
        return [
            StaffMember(id=m.id, name=m.name, role=m.role, active=m.active)
            for m in models
        ]

    def get_active_by_ids(self, ids: list[int]) -> list[StaffMember]:
        if not ids:
            return []
        models = (
            self._session.query(StaffMemberModel)
            .filter(
                StaffMemberModel.id.in_(ids),
                StaffMemberModel.active == True,
            )
            .all()
        )
        # Preserve input order
        model_map = {m.id: m for m in models}
        result = []
        for staff_id in ids:
            if staff_id in model_map:
                m = model_map[staff_id]
                result.append(StaffMember(id=m.id, name=m.name, role=m.role, active=m.active))
        return result
