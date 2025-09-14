from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from core.database import Base

class UserActivity(Base):
    __tablename__ = "user_activity"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    activity_type = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    details = Column(Text)
    duration = Column(Integer)
    timestamp = Column(DateTime(timezone=True), server_default=func.now()) 