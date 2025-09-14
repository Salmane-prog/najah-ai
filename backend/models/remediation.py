from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime

class RemediationResult(Base):
    __tablename__ = "remediation_results"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic = Column(String(255), nullable=False)
    exercise_type = Column(String(50), nullable=False)  # 'quiz', 'reading', 'practice'
    score = Column(Integer, nullable=False)
    max_score = Column(Integer, nullable=False)
    percentage = Column(Float, nullable=False)
    time_spent = Column(Integer)  # en secondes
    completed_at = Column(DateTime, default=datetime.utcnow)
    weak_areas_improved = Column(Text)  # JSON string
    
    # Relations
    student = relationship("User", back_populates="remediation_results")

class RemediationBadge(Base):
    __tablename__ = "remediation_badges"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    badge_type = Column(String(100), nullable=False)  # 'achievement', 'expertise', 'improvement'
    badge_name = Column(String(255), nullable=False)
    description = Column(Text)
    earned_at = Column(DateTime, default=datetime.utcnow)
    points = Column(Integer, default=0)
    
    # Relations
    student = relationship("User", back_populates="remediation_badges")

class RemediationProgress(Base):
    __tablename__ = "remediation_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic = Column(String(255), nullable=False)
    current_level = Column(Integer, default=1)  # 1-5
    previous_level = Column(Integer, default=1)
    improvement = Column(Float, default=0.0)
    exercises_completed = Column(Integer, default=0)
    total_exercises = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    student = relationship("User", back_populates="remediation_progress") 