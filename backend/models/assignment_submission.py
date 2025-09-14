from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

class AssignmentSubmission(Base):
    __tablename__ = "assignment_submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    submitted_file = Column(String, nullable=False)  # Chemin vers le fichier soumis
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="submitted")  # submitted, graded, returned
    grade = Column(Integer, nullable=True)  # Note sur 100
    feedback = Column(Text, nullable=True)  # Commentaires du professeur
    graded_at = Column(DateTime(timezone=True), nullable=True)
    graded_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relations
    assignment = relationship("Assignment", back_populates="submissions")
    student = relationship("User", foreign_keys=[student_id])
    grader = relationship("User", foreign_keys=[graded_by])
