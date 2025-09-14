from pydantic import BaseModel
from datetime import datetime

class ReportBase(BaseModel):
    title: str
    content: str
    type: str

class ReportCreate(ReportBase):
    pass

class ReportRead(ReportBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True 