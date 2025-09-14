from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class QuizAssignment(Base):
    __tablename__ = "quiz_assignments"
    
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_at = Column(DateTime(timezone=True), server_default=func.now())
    due_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(50), default="assigned")  # assigned, in_progress, completed, overdue
    score = Column(Integer, nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    feedback = Column(Text, nullable=True)
    
    # Relations
    quiz = relationship("Quiz", back_populates="assignments")
    student = relationship("User", foreign_keys=[student_id], back_populates="quiz_assignments")
    teacher = relationship("User", foreign_keys=[assigned_by], back_populates="quiz_assignments_created")
