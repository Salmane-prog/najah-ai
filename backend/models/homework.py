from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base
from datetime import datetime

class AdvancedHomework(Base):
    __tablename__ = "advanced_homeworks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    subject = Column(String(100), nullable=False)
    class_id = Column(Integer, ForeignKey("class_groups.id"), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)  # Professeur
    due_date = Column(DateTime(timezone=True), nullable=False)
    priority = Column(String(20), default="medium")  # low, medium, high
    estimated_time = Column(Integer, nullable=True)  # en minutes
    max_score = Column(Float, default=100.0)
    instructions = Column(Text, nullable=True)
    attachments = Column(JSON, nullable=True)  # Liste des fichiers attachés
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    creator = relationship("User", foreign_keys=[created_by])
    class_group = relationship("ClassGroup")
    submissions = relationship("AdvancedHomeworkSubmission", back_populates="homework")

class AdvancedHomeworkSubmission(Base):
    __tablename__ = "advanced_homework_submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    homework_id = Column(Integer, ForeignKey("advanced_homeworks.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    content = Column(Text, nullable=True)
    attachments = Column(JSON, nullable=True)  # Liste des fichiers soumis
    score = Column(Float, nullable=True)
    max_score = Column(Float, nullable=True)
    feedback = Column(Text, nullable=True)
    status = Column(String(20), default="submitted")  # submitted, graded, late
    graded_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    graded_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relations
    homework = relationship("AdvancedHomework", back_populates="submissions")
    student = relationship("User", foreign_keys=[student_id])
    grader = relationship("User", foreign_keys=[graded_by])

class AdvancedHomeworkAssignment(Base):
    __tablename__ = "advanced_homework_assignments"
    
    id = Column(Integer, primary_key=True, index=True)
    homework_id = Column(Integer, ForeignKey("advanced_homeworks.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_at = Column(DateTime(timezone=True), server_default=func.now())
    due_date = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relations
    homework = relationship("AdvancedHomework")
    student = relationship("User", foreign_keys=[student_id])
