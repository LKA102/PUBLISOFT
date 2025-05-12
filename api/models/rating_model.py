from sqlalchemy import Table, Column, Float, Integer, String, DateTime, UUID
from database.db import Base
from datetime import datetime

rating_table = Table(
    "Rating",
    Base.metadata,
    Column("id_post", Integer, primary_key=True),
    Column("id_user", UUID, primary_key=True),
    Column("rating", Float, nullable=False),
)