from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

class Assignment(Base):
    __tablename__ = "assignments"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    subject = Column(String(100), nullable=False)
    assignment_type = Column(String(20), nullable=False)  # "class" ou "student"
    target_ids = Column(JSON)  # IDs des classes ou étudiants cibles
    due_date = Column(DateTime(timezone=True), nullable=True)
    priority = Column(String(20), default="medium")  # "low", "medium", "high"
    estimated_time = Column(Integer, nullable=True)  # en minutes
    status = Column(String(20), default="pending")  # "pending", "in_progress", "completed", "overdue"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Champ pour le fichier attaché
    attachment = Column(JSON, nullable=True)  # Stocke les métadonnées du fichier
    
    # Relations
    creator = relationship("User", foreign_keys=[created_by])
    submissions = relationship("AssignmentSubmission", back_populates="assignment")
    student_assignments = relationship("StudentAssignment", back_populates="assignment")

