from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime

class Competency(Base):
    __tablename__ = "competencies"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    subject = Column(String(100), nullable=False)
    level = Column(String(50), nullable=False)  # 'beginner', 'intermediate', 'advanced'
    category = Column(String(100))  # 'knowledge', 'skills', 'attitudes'
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations
    created_by_user = relationship("User", foreign_keys=[created_by])
    student_competencies = relationship("StudentCompetency", back_populates="competency")

class StudentCompetency(Base):
    __tablename__ = "student_competencies"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    competency_id = Column(Integer, ForeignKey("competencies.id"), nullable=False)
    level_achieved = Column(String(50), default="not_started")  # 'not_started', 'beginner', 'intermediate', 'advanced', 'expert'
    progress_percentage = Column(Float, default=0.0)  # 0-100
    last_assessed = Column(DateTime)
    assessment_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations
    student = relationship("User", foreign_keys=[student_id])
    competency = relationship("Competency", back_populates="student_competencies")

class ContinuousAssessment(Base):
    __tablename__ = "continuous_assessments"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    assessment_type = Column(String(50), nullable=False)  # 'quiz', 'project', 'presentation', 'observation'
    subject = Column(String(100), nullable=False)
    class_id = Column(Integer, ForeignKey("class_groups.id"))
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    competencies_targeted = Column(JSON)  # Liste des IDs de compétences
    weight = Column(Float, default=1.0)  # Poids dans l'évaluation finale
    due_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations
    teacher = relationship("User", foreign_keys=[teacher_id])
    class_group = relationship("ClassGroup")
    student_assessments = relationship("StudentContinuousAssessment", back_populates="assessment")

class StudentContinuousAssessment(Base):
    __tablename__ = "student_continuous_assessments"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assessment_id = Column(Integer, ForeignKey("continuous_assessments.id"), nullable=False)
    score = Column(Float)  # Score obtenu
    max_score = Column(Float, nullable=False)  # Score maximum possible
    percentage = Column(Float)  # Pourcentage de réussite
    feedback = Column(Text)  # Feedback du professeur
    competencies_evaluated = Column(JSON)  # Compétences évaluées avec scores
    status = Column(String(50), default="pending")  # 'pending', 'completed', 'late'
    submitted_at = Column(DateTime)
    evaluated_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations
    student = relationship("User", foreign_keys=[student_id])
    assessment = relationship("ContinuousAssessment", back_populates="student_assessments")

class ProgressReport(Base):
    __tablename__ = "progress_reports"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("class_groups.id"))
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    period = Column(String(50), nullable=False)  # 'weekly', 'monthly', 'semester'
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    overall_progress = Column(Float)  # Progression globale (0-100)
    competencies_summary = Column(JSON)  # Résumé des compétences
    strengths = Column(JSON)  # Points forts identifiés
    weaknesses = Column(JSON)  # Points faibles identifiés
    recommendations = Column(JSON)  # Recommandations d'amélioration
    generated_at = Column(DateTime, default=datetime.utcnow)

    # Relations
    student = relationship("User", foreign_keys=[student_id])
    teacher = relationship("User", foreign_keys=[teacher_id])
    class_group = relationship("ClassGroup") 