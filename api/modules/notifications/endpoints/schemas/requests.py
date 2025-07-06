from pydantic import BaseModel
from uuid import UUID

class NotificationCreate(BaseModel):
    emisor_id: UUID
    message: str
    notification_type: str
    receptor_id: UUID
    title: str
    
class NotificationUpdateLeido(BaseModel):
    leido: bool
