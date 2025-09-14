from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ContentBase(BaseModel):
    title: str
    description: Optional[str] = None
    content_type: str
    subject: str
    level: str
    difficulty: float = 1.0
    estimated_time: int = 15
    content_data: Optional[str] = None
    file_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    tags: Optional[str] = None
    learning_objectives: Optional[str] = None
    prerequisites: Optional[str] = None
    skills_targeted: Optional[str] = None

class ContentCreate(ContentBase):
    pass

class ContentRead(ContentBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_active: bool = True

    class Config:
        from_attributes = True

class NoteBase(BaseModel):
    text: str
    timestamp: int = 0

class NoteCreate(NoteBase):
    pass

class NoteRead(NoteBase):
    id: int
    content_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ContentProgress(BaseModel):
    content_id: int
    user_id: int
    progress: float
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True 