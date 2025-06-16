from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.common.session import Base

# This model does not inherit from BaseEntitySQLAlchemy because it does not need the created_at and updated_at fields.
class RoleSQLAlchemy(Base):
    __tablename__ = 'Roles'
    __table_args__ = {'schema': 'custom_auth'}

    role_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)

    users = relationship("UserModel", back_populates="role")  # Assuming UserModel has a role relationship



