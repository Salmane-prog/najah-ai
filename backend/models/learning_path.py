from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

class LearningPath(Base):
    __tablename__ = "learning_paths"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    objectives = Column(Text, nullable=True)
    subject = Column(String, nullable=True)
    level = Column(String, nullable=True)  # 'beginner', 'intermediate', 'advanced'
    difficulty = Column(String, nullable=True)
    estimated_duration = Column(Integer, default=30)  # en jours
    is_adaptive = Column(Boolean, default=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    assignments = relationship("StudentLearningPath", foreign_keys="StudentLearningPath.learning_path_id", viewonly=True)
    steps = relationship("LearningPathStep", foreign_keys="LearningPathStep.learning_path_id", viewonly=True)
    creator = relationship("User", foreign_keys=[created_by], viewonly=True)