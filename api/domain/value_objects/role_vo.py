from enums.role_enum import RoleEnum


class RoleVO:
    def __init__(self, description_role: str):
        if not description_role or not description_role.strip():
            raise ValueError("Role description cannot be empty")
        self.description_role = description_role.strip()

        if description_role not in [role.name for role in RoleEnum]:
            raise ValueError("Role description must be a valid role from RoleEnum")

    def __str__(self):
        return self.description_role
