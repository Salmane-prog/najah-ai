from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base
from datetime import datetime

class Content(Base):
    __tablename__ = "contents"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    content_type = Column(String(50), nullable=False, default="text")  # 'text', 'video', 'audio', 'interactive'
    subject = Column(String(100), nullable=False)
    level = Column(String(50), nullable=False)  # 'beginner', 'intermediate', 'advanced'
    difficulty = Column(Float, default=1.0)  # 1-10 scale
    estimated_time = Column(Integer, default=15)  # minutes
    content_data = Column(Text, nullable=True)  # JSON data for interactive content
    file_url = Column(String(500), nullable=True)  # For video/audio files
    thumbnail_url = Column(String(500), nullable=True)
    
    # Métadonnées pour l'IA
    tags = Column(Text, nullable=True)  # JSON array of tags
    learning_objectives = Column(Text, nullable=True)  # JSON array
    prerequisites = Column(Text, nullable=True)  # JSON array
    skills_targeted = Column(Text, nullable=True)  # JSON array
    
    # Relations
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)  # Changé à nullable=True
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # updated_at = Column(DateTime(timezone=True), onupdate=func.now())  # Commenté temporairement
    is_active = Column(Boolean, default=True)
    
    # Nouveaux champs pour le partage et l'évaluation (commentés temporairement)
    # is_shared = Column(Boolean, default=False)
    # shared_description = Column(Text)
    # shared_at = Column(DateTime)
    # downloads_count = Column(Integer, default=0)
    # rating = Column(Float, default=0.0)  # Note moyenne
    
    # Relations - Commentées temporairement pour éviter les erreurs circulaires
    # creator = relationship("User", back_populates="contents")
    # category = relationship("Category", back_populates="contents")
    # learning_paths = relationship("LearningPath", secondary="learning_path_contents", back_populates="contents")
    
    # Relation avec les partages
    sharings = relationship("ContentSharing", back_populates="content")

class LearningPathContent(Base):
    __tablename__ = "learning_path_contents"
    
    id = Column(Integer, primary_key=True, index=True)
    learning_path_id = Column(Integer, ForeignKey("learning_paths.id"), nullable=False)
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=False)
    order = Column(Integer, nullable=False)
    estimated_time = Column(Integer, default=15)
    
    # Relations - Commentées temporairement
    # learning_path = relationship("LearningPath", back_populates="content_assignments")
    # content = relationship("Content") 