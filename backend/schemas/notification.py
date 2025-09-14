from pydantic import BaseModel

class NotificationBase(BaseModel):
    title: str
    message: str
    user_id: int

class NotificationCreate(NotificationBase):
    pass

class NotificationRead(NotificationBase):
    id: int
    class Config:
        from_attributes = True 