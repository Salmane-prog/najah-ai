from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ThreadBase(BaseModel):
    title: str
    description: Optional[str] = None
    type: Optional[str] = None

class ThreadCreate(ThreadBase):
    created_by: int

class ThreadRead(ThreadBase):
    id: int
    created_by: int
    created_at: datetime
    
    class Config:
        from_attributes = True 