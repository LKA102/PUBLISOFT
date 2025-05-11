from sqlalchemy import Column, Float, Integer, String, DateTime
from database.db import Base
from datetime import datetime

class NotificationModel(Base):
    __tablename__ = 'Notification'

    id_notification = Column(Integer, primary_key=True, autoincrement=True)
    id_sender_user = Column(Integer, unique=True, nullable=False)
    id_receiver_user = Column(Integer, unique=True, nullable=False)
    id_post = Column(Integer, unique=True, nullable=False)
    title = Column(String(255), nullable=True)
    message = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(datetime.timezone.utc))