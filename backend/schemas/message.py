from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MessageBase(BaseModel):
    thread_id: Optional[int] = None
    user_id: int
    content: str

class MessageCreate(MessageBase):
    pass

class MessageRead(MessageBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True 