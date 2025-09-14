from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base
from datetime import datetime

class UserInterfacePreference(Base):
    __tablename__ = "user_interface_preferences"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    interface_level = Column(String(20), nullable=False)  # 'primary', 'middle', 'high', 'university'
    theme = Column(String(20), default="default")  # 'default', 'dark', 'light', 'colorful'
    font_size = Column(String(10), default="medium")  # 'small', 'medium', 'large'
    animations_enabled = Column(Boolean, default=True)
    sound_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relations
    user = relationship("User", foreign_keys=[user_id])

class LevelObjective(Base):
    __tablename__ = "level_objectives"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(20), nullable=False)  # 'primary', 'middle', 'high', 'university'
    subject = Column(String(100))
    objective_title = Column(String(255), nullable=False)
    description = Column(Text)
    difficulty = Column(Integer)  # 1-5
    estimated_time = Column(Integer)  # minutes
    prerequisites = Column(Text)  # JSON array of prerequisite objective IDs
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class UserObjectiveProgress(Base):
    __tablename__ = "user_objective_progress"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    objective_id = Column(Integer, ForeignKey("level_objectives.id"))
    progress = Column(Float, default=0.0)  # 0.0 to 1.0
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    
    # Relations
    user = relationship("User", foreign_keys=[user_id])
    objective = relationship("LevelObjective", foreign_keys=[objective_id]) 