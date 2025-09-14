from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class Assessment(Base):
    __tablename__ = "assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assessment_type = Column(String, nullable=False)  # "initial", "progress", "final", "homework"
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    subject = Column(String, nullable=True)  # Matière du devoir
    priority = Column(String, default="medium")  # "low", "medium", "high"
    estimated_time = Column(Integer, nullable=True)  # Temps estimé en minutes
    status = Column(String, default="in_progress")  # "in_progress", "completed", "cancelled"
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)  # Professeur qui a créé le devoir
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    student = relationship("User", foreign_keys=[student_id], viewonly=True)
    teacher = relationship("User", foreign_keys=[created_by])
    questions = relationship("AssessmentQuestion", back_populates="assessment", order_by="AssessmentQuestion.order")
    results = relationship("AssessmentResult", back_populates="assessment")
    assignments = relationship("AssessmentAssignment", back_populates="assessment")

class AssessmentAssignment(Base):
    __tablename__ = "assessment_assignments"
    
    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("class_groups.id"), nullable=True)
    due_date = Column(DateTime, nullable=True)  # Date limite de rendu
    status = Column(String, default="pending")  # "pending", "in_progress", "completed", "overdue"
    assigned_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    assessment = relationship("Assessment", back_populates="assignments")
    student = relationship("User", foreign_keys=[student_id])
    teacher = relationship("User", foreign_keys=[teacher_id])
    class_group = relationship("ClassGroup")

class AssessmentQuestion(Base):
    __tablename__ = "assessment_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(String, nullable=False)  # "mcq", "text", "true_false"
    subject = Column(String, nullable=False)  # "Littérature", "Mathématiques", "Sciences"
    difficulty = Column(String, nullable=False)  # "beginner", "intermediate", "advanced"
    options = Column(Text, nullable=True)  # JSON string pour les QCM
    correct_answer = Column(String, nullable=False)
    points = Column(Float, default=1.0)
    order = Column(Integer, default=0)
    
    # Relations
    assessment = relationship("Assessment", back_populates="questions")

class AssessmentResult(Base):
    __tablename__ = "assessment_results"
    
    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_score = Column(Float, nullable=False)
    max_score = Column(Float, nullable=False)
    percentage = Column(Float, nullable=False)
    subject_scores = Column(Text, nullable=True)  # JSON string avec scores par sujet
    difficulty_scores = Column(Text, nullable=True)  # JSON string avec scores par difficulté
    completed_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    assessment = relationship("Assessment", back_populates="results")
    student = relationship("User") 