from pydantic import BaseModel
from datetime import datetime, timezone

class RankingCreate(BaseModel):
    score: float
    student_id: str
    created_at: datetime = datetime.now(timezone.utc) # ISO format date string (e.g., "2023-10-01T12:00:00Z")