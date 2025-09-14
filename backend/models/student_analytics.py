from sqlalchemy import Column, Integer, DateTime, Float, Boolean, Text
from sqlalchemy.sql import func
from core.database import Base
from datetime import datetime

class StudentAnalytics(Base):
    __tablename__ = "student_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, nullable=False)
    class_id = Column(Integer)
    date = Column(DateTime(timezone=True), server_default=func.now())
    total_quizzes = Column(Integer, default=0)
    avg_score = Column(Float, default=0.0)
    total_time = Column(Integer, default=0)  # en minutes
    activities_count = Column(Integer, default=0)

class StudentProgress(Base):
    __tablename__ = "student_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, nullable=False)
    learning_path_id = Column(Integer, nullable=False)
    current_step_id = Column(Integer)
    completed_steps = Column(Text)  # JSON string pour stocker les IDs des étapes complétées
    progress_percentage = Column(Float, default=0.0)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    last_activity = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True) 