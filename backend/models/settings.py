from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from core.database import Base

class UserSettings(Base):
    __tablename__ = "user_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # Thème et langue
    theme = Column(String(20), default="light")  # light, dark
    language = Column(String(10), default="fr")  # fr, en, ar
    
    # Notifications
    notifications_enabled = Column(Boolean, default=True)
    email_notifications = Column(Boolean, default=True)
    push_notifications = Column(Boolean, default=True)
    study_reminders = Column(Boolean, default=True)
    
    # Confidentialité
    privacy_level = Column(String(20), default="public")  # public, private, friends
    show_progress = Column(Boolean, default=True)
    show_leaderboard = Column(Boolean, default=True)
    
    # Objectifs d'étude
    daily_goal = Column(Integer, default=30)  # minutes
    weekly_goal = Column(Integer, default=180)  # minutes
    difficulty_preference = Column(String(20), default="adaptive")  # easy, medium, hard, adaptive
    
    # Autres paramètres
    auto_save = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 