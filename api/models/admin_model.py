from sqlalchemy import Column, Integer, String, UUID
from database.db import Base


class AdminModel(Base):
    __tablename__ = "Administrator"

    id_admin = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(UUID, unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
