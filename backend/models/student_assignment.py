from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

class StudentAssignment(Base):
    __tablename__ = "student_assignments"
    
    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, default="assigned")  # assigned, in_progress, submitted, completed, overdue
    started_at = Column(DateTime(timezone=True), nullable=True)
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    time_spent = Column(Integer, nullable=True)  # Temps passé en minutes
    notes = Column(Text, nullable=True)  # Notes personnelles de l'étudiant
    
    # Relations
    assignment = relationship("Assignment", back_populates="student_assignments")
    student = relationship("User", foreign_keys=[student_id])
