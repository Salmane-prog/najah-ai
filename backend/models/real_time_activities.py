from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from core.database import Base

class RealTimeActivities(Base):
    __tablename__ = "real_time_activities"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, nullable=False)
    activity_type = Column(Text, nullable=False)
    activity_data = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now()) 