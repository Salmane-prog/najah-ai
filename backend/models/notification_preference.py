from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from core.database import Base

class NotificationPreference(Base):
    __tablename__ = "notification_preferences"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    notif_type = Column(String, nullable=False)  # ex: badge, report, admin, group_invite
    channel = Column(String, nullable=False)  # websocket, email, etc.
    enabled = Column(Boolean, default=True, nullable=False) 