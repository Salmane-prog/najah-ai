from pydantic import BaseModel

class NotificationPreferenceBase(BaseModel):
    user_id: int
    email_notifications: bool = True
    push_notifications: bool = True
    quiz_reminders: bool = True
    achievement_notifications: bool = True

class NotificationPreferenceCreate(NotificationPreferenceBase):
    pass

class NotificationPreferenceRead(NotificationPreferenceBase):
    id: int
    class Config:
        from_attributes = True 