from typing import Set, Optional
from modules.users.domain.entities.admin import Admin
from modules.users.domain.repositories.interface_admin_repository import IAdminRepository
from modules.users.infrastructure.database.models.admins import AdminSQLAlchemy
from modules.users.infrastructure.database.mappers.admin_mapper import AdminMapper
from uuid import UUID

class AdminRepositorySQLAlchemy(IAdminRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _save(self, admin: Admin) -> Admin:
        admin_orm = AdminMapper.to_orm(admin, self.session)
        self.session.add(admin_orm)
        return admin

    def _load(self, admin_id: UUID) -> Optional[Admin]:
        admin_orm = self.session.query(AdminSQLAlchemy).filter_by(id=admin_id).first()
        if not admin_orm:
            return None
        return AdminMapper.to_entity(admin_orm)

    def _load_all(self) -> Set[Admin]:
        admins_orm = self.session.query(AdminSQLAlchemy).all()
        return {AdminMapper.to_entity(admin_orm) for admin_orm in admins_orm}

    def _update(self, admin: Admin) -> Optional[Admin]:
        admin_orm = AdminMapper.to_orm(admin, self.session)
        existing_admin_orm = self.session.query(AdminSQLAlchemy).filter_by(id=admin.id).first()
        if existing_admin_orm:
            existing_admin_orm.name = admin_orm.name
            existing_admin_orm.email = admin_orm.email
            existing_admin_orm.state = admin_orm.state
            existing_admin_orm.admin_code = admin_orm.admin_code
            AdminSQLAlchemy.base_entity_to_orm(admin, existing_admin_orm)
            return AdminMapper.to_entity(existing_admin_orm)
        else:
            return None