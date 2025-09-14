from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

class LearningPathStep(Base):
    __tablename__ = "learning_path_steps"
    
    id = Column(Integer, primary_key=True, index=True)
    learning_path_id = Column(Integer, ForeignKey("learning_paths.id"), nullable=False)
    step_number = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    content_type = Column(String, nullable=False)  # 'quiz', 'content', 'assessment'
    content_id = Column(Integer, nullable=True)  # ID du contenu associé
    estimated_duration = Column(Integer, default=15)  # en minutes
    is_required = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    
    # Métadonnées
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    learning_path = relationship("LearningPath", foreign_keys=[learning_path_id], viewonly=True)
