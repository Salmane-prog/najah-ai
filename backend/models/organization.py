from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base
from datetime import datetime

class Homework(Base):
    __tablename__ = "homework"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    subject = Column(String(100))
    class_id = Column(Integer, ForeignKey("class_groups.id"))
    assigned_by = Column(Integer, ForeignKey("users.id"))
    assigned_to = Column(Integer, ForeignKey("users.id"))
    due_date = Column(DateTime, nullable=False)
    status = Column(String(20), default="pending")  # 'pending', 'in_progress', 'completed', 'overdue'
    priority = Column(String(20), default="medium")  # 'low', 'medium', 'high'
    estimated_time = Column(Integer)  # minutes
    actual_time = Column(Integer)     # minutes
    grade = Column(Float)            # Note sur 20
    feedback = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relations
    class_group = relationship("ClassGroup", foreign_keys=[class_id])
    assigned_by_user = relationship("User", foreign_keys=[assigned_by])
    assigned_to_user = relationship("User", foreign_keys=[assigned_to])

class StudySession(Base):
    __tablename__ = "study_sessions"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(255), nullable=False)  # Ajout du champ title
    description = Column(Text)  # Ajout du champ description
    subject = Column(String(100))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    duration = Column(Integer)  # minutes
    goals = Column(JSON)  # Liste des objectifs
    status = Column(String(20), default="planned")  # 'planned', 'in_progress', 'completed', 'cancelled'
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    user = relationship("User", foreign_keys=[user_id])

class Reminder(Base):
    __tablename__ = "reminders"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    reminder_time = Column(DateTime, nullable=False)
    is_recurring = Column(Boolean, default=False)
    recurrence_pattern = Column(JSON)  # {'type': 'daily', 'interval': 1, 'days': ['monday', 'wednesday']}
    is_active = Column(Boolean, default=True)
    notification_sent = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    user = relationship("User", foreign_keys=[user_id])

class LearningGoal(Base):
    __tablename__ = "learning_goals"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    subject = Column(String(100))
    target_date = Column(DateTime)
    progress = Column(Float, default=0.0)  # 0.0 to 1.0
    status = Column(String(20), default="active")  # 'active', 'completed', 'abandoned'
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)  # Qui a créé l'objectif
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    user = relationship("User", foreign_keys=[user_id])
    creator = relationship("User", foreign_keys=[created_by]) 