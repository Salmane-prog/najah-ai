from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LearningHistoryBase(BaseModel):
    student_id: int
    content_id: Optional[int] = None
    path_id: Optional[int] = None
    action: str
    score: Optional[float] = None
    progression: Optional[float] = None
    details: Optional[str] = None

class LearningHistoryCreate(LearningHistoryBase):
    pass

class LearningHistoryRead(LearningHistoryBase):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True 