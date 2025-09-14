#!/usr/bin/env python3
"""
Modèles pour le forum d'entraide
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class ForumCategory(Base):
    __tablename__ = "forum_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    subject = Column(String(100), nullable=True)  # Matière (Mathématiques, Français, etc.)
    level = Column(String(50), nullable=True)     # Niveau (Débutant, Intermédiaire, Avancé)
    parent_id = Column(Integer, ForeignKey("forum_categories.id"), nullable=True)  # Catégorie parente
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    threads = relationship("ForumThread", back_populates="category")
    parent = relationship("ForumCategory", remote_side=[id], back_populates="children")
    children = relationship("ForumCategory", back_populates="parent")

class ForumThread(Base):
    __tablename__ = "forum_threads"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey("forum_categories.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tags = Column(Text, nullable=True)  # JSON string des tags
    is_pinned = Column(Boolean, default=False)
    is_locked = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    reply_count = Column(Integer, default=0)
    last_reply_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    category = relationship("ForumCategory", back_populates="threads")
    author = relationship("User", back_populates="forum_threads")
    replies = relationship("ForumReply", back_populates="thread", order_by="ForumReply.created_at")

class ForumReply(Base):
    __tablename__ = "forum_replies"
    
    id = Column(Integer, primary_key=True, index=True)
    thread_id = Column(Integer, ForeignKey("forum_threads.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    is_solution = Column(Boolean, default=False)  # Marquer comme solution
    is_edited = Column(Boolean, default=False)
    edited_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    thread = relationship("ForumThread", back_populates="replies")
    author = relationship("User", back_populates="forum_replies") 