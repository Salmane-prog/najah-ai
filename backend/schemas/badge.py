from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BadgeBase(BaseModel):
    name: str
    description: str
    icon: Optional[str] = None
    criteria: Optional[str] = None
    points: int = 0

class BadgeCreate(BadgeBase):
    pass

class BadgeRead(BadgeBase):
    id: int
    class Config:
        from_attributes = True

class UserBadgeBase(BaseModel):
    user_id: int
    badge_id: int
    progression: float = 0.0

class UserBadgeCreate(UserBadgeBase):
    pass

class UserBadgeRead(UserBadgeBase):
    id: int
    awarded_at: Optional[datetime] = None
    class Config:
        from_attributes = True 