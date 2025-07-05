from modules.users.domain.entities.admin import Admin
from modules.users.infrastructure.database.models.admins import AdminSQLAlchemy
from modules.users.infrastructure.database.models.base_entity import BaseEntitySQLAlchemy

class AdminMapper:
    @staticmethod
    def to_entity(admin_orm: AdminSQLAlchemy) -> Admin:
        # Convert ORM model to domain entity
        base_kwargs = BaseEntitySQLAlchemy.orm_to_base_entity(admin_orm)
        return Admin(
            name=admin_orm.name,
            last_name=admin_orm.last_name,
            faculty=admin_orm.faculty,
            **base_kwargs
        )

    @staticmethod
    def to_orm(admin: Admin, **kwargs) -> AdminSQLAlchemy:
        admin_orm = AdminSQLAlchemy()
        admin_orm.name = admin.name
        admin_orm.last_name = admin.last_name
        admin_orm.faculty = admin.faculty
        admin_orm.profile_image_path = kwargs.get('profile_image_path', None)
        AdminSQLAlchemy.base_entity_to_orm(admin, admin_orm)
        return admin_orm