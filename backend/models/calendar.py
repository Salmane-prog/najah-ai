#!/usr/bin/env python3
"""
Modèles pour le calendrier et les événements
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base
from datetime import datetime

class CalendarEvent(Base):
    __tablename__ = "calendar_events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    event_type = Column(String(50), nullable=False)  # 'homework', 'study_session', 'reminder', 'goal', 'exam', 'meeting'
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=True)
    all_day = Column(Boolean, default=False)
    color = Column(String(7), default="#3B82F6")  # Couleur hexadécimale
    priority = Column(String(20), default="medium")  # 'low', 'medium', 'high'
    location = Column(String(255), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    related_id = Column(Integer, nullable=True)  # ID de l'élément lié (devoir, session, etc.)
    related_type = Column(String(50), nullable=True)  # Type de l'élément lié
    recurrence = Column(String(20), default="none")  # 'none', 'daily', 'weekly', 'monthly', 'yearly'
    recurrence_end = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    user = relationship("User", back_populates="calendar_events")

class StudyTimeStats(Base):
    __tablename__ = "study_time_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    subject = Column(String(100), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    session_count = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    user = relationship("User", back_populates="study_time_stats")
