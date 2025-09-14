from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

class StudentLearningPath(Base):
    __tablename__ = "student_learning_paths"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    learning_path_id = Column(Integer, ForeignKey("learning_paths.id"), nullable=False)
    progress = Column(Float, default=0.0)  # 0.0 à 1.0
    is_completed = Column(Boolean, default=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    current_step = Column(Integer, default=1)
    total_steps = Column(Integer, default=1)
    
    # Relations
    student = relationship("User", foreign_keys=[student_id], viewonly=True)
    learning_path = relationship("LearningPath", back_populates="assignments")
    
    def __repr__(self):
        return f"<StudentLearningPath(id={self.id}, student_id={self.student_id}, progress={self.progress})>" 