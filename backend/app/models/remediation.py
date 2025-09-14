from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class RemediationResult(Base):
    __tablename__ = "remediation_results"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic = Column(String(100), nullable=False)  # fondamentaux, conjugaison, vocabulaire
    exercise_type = Column(String(50), nullable=False)  # quiz, reading, practice
    score = Column(Integer, nullable=False)
    max_score = Column(Integer, nullable=False)
    percentage = Column(Float, nullable=False)
    time_spent = Column(Integer, nullable=False)  # en secondes
    weak_areas_improved = Column(JSON, nullable=True)  # liste des domaines améliorés
    difficulty_level = Column(String(20), default="medium")  # easy, medium, hard
    completed_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    student = relationship("User", back_populates="remediation_results")
    
    def __repr__(self):
        return f"<RemediationResult(id={self.id}, student_id={self.student_id}, topic='{self.topic}', score={self.score}/{self.max_score})>"

class RemediationBadge(Base):
    __tablename__ = "remediation_badges"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    badge_type = Column(String(100), nullable=False)  # first_quiz, perfect_score, speed_learner, etc.
    badge_name = Column(String(100), nullable=False)
    badge_description = Column(Text, nullable=True)
    badge_icon = Column(String(100), nullable=True)
    earned_at = Column(DateTime(timezone=True), server_default=func.now())
    metadata = Column(JSON, nullable=True)  # données supplémentaires (score, temps, etc.)
    
    # Relations
    student = relationship("User", back_populates="remediation_badges")
    
    def __repr__(self):
        return f"<RemediationBadge(id={self.id}, student_id={self.student_id}, badge='{self.badge_name}')>"

class RemediationProgress(Base):
    __tablename__ = "remediation_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic = Column(String(100), nullable=False)
    current_level = Column(Integer, default=0)
    previous_level = Column(Integer, default=0)
    improvement = Column(Integer, default=0)
    exercises_completed = Column(Integer, default=0)
    total_exercises = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)
    last_updated = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    student = relationship("User", back_populates="remediation_progress")
    
    def __repr__(self):
        return f"<RemediationProgress(id={self.id}, student_id={self.student_id}, topic='{self.topic}', level={self.current_level})>"








