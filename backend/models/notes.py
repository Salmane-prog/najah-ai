#!/usr/bin/env python3
"""
Modèles pour les notes avancées
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base


class AdvancedNote(Base):
    __tablename__ = "advanced_notes"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    subject_id = Column(Integer, nullable=False)
    chapter_id = Column(Integer, nullable=True)
    tags = Column(JSON, default=list)
    color = Column(String(50), default="#3B82F6")
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_favorite = Column(Boolean, default=False)
    is_shared = Column(Boolean, default=False)
    shared_with = Column(JSON, default=list)
    version = Column(Integer, default=1)
    
    # Relations
    author = relationship("User", back_populates="advanced_notes")


class AdvancedSubject(Base):
    __tablename__ = "advanced_subjects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    color = Column(String(50), default="#3B82F6")
    note_count = Column(Integer, default=0)


class AdvancedChapter(Base):
    __tablename__ = "advanced_chapters"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    subject_id = Column(Integer, ForeignKey("advanced_subjects.id"), nullable=False)
    note_count = Column(Integer, default=0)
    
    # Relations
    subject = relationship("AdvancedSubject") 