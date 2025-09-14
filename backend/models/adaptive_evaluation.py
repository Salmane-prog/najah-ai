from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

# Import temporairement supprimé pour résoudre le problème de ForeignKey

Base = declarative_base()

class AdaptiveTest(Base):
    """Modèle pour les tests adaptatifs"""
    __tablename__ = "adaptive_tests"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    subject = Column(String(100), nullable=False)
    description = Column(Text)
    difficulty_min = Column(Integer, default=1)
    difficulty_max = Column(Integer, default=10)
    estimated_duration = Column(Integer, default=30)  # en minutes
    total_questions = Column(Integer, default=20)
    adaptation_type = Column(String(50), default='hybrid')  # cognitive, performance, hybrid
    learning_objectives = Column(Text)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, nullable=True)  # Temporairement sans ForeignKey
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relations
    questions = relationship("AdaptiveQuestion", back_populates="test", cascade="all, delete-orphan")
    assignments = relationship("TestAssignment", back_populates="test", cascade="all, delete-orphan")
    attempts = relationship("TestAttempt", back_populates="test", cascade="all, delete-orphan")

class AdaptiveQuestion(Base):
    """Modèle pour les questions des tests adaptatifs"""
    __tablename__ = "adaptive_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("adaptive_tests.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50), default='multiple_choice')  # multiple_choice, open_ended, etc.
    difficulty_level = Column(Integer, nullable=False)
    learning_objective = Column(String(255))
    options = Column(Text)  # JSON des options pour QCM
    correct_answer = Column(Text)
    explanation = Column(Text)
    question_order = Column(Integer, default=0)  # Ajouté
    is_active = Column(Boolean, default=True)   # Ajouté
    
    # Relations
    test = relationship("AdaptiveTest", back_populates="questions")
    responses = relationship("QuestionResponse", back_populates="question", cascade="all, delete-orphan")

class TestAssignment(Base):
    """Modèle pour les assignations de tests"""
    __tablename__ = "test_assignments"
    
    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("adaptive_tests.id"), nullable=False)
    assignment_type = Column(String(20), nullable=False)  # 'class' ou 'student'
    target_id = Column(Integer, nullable=False)  # ID de la classe ou de l'étudiant
    assigned_by = Column(Integer, nullable=False)  # Temporairement sans ForeignKey
    assigned_at = Column(DateTime, default=func.now())
    due_date = Column(DateTime)
    status = Column(String(20), default='active')  # active, inactive, completed
    
    # Contraintes
    __table_args__ = (
        CheckConstraint(assignment_type.in_(['class', 'student']), name='valid_assignment_type'),
        CheckConstraint(status.in_(['active', 'inactive', 'completed']), name='valid_status'),
    )
    
    # Relations
    test = relationship("AdaptiveTest", back_populates="assignments")
    attempts = relationship("TestAttempt", back_populates="assignment", cascade="all, delete-orphan")

class TestAttempt(Base):
    """Modèle pour les tentatives de test des étudiants"""
    __tablename__ = "test_attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("adaptive_tests.id"), nullable=False)
    student_id = Column(Integer, nullable=False)  # Temporairement sans ForeignKey pour éviter l'erreur
    assignment_id = Column(Integer, ForeignKey("test_assignments.id"))
    started_at = Column(DateTime, default=func.now())
    completed_at = Column(DateTime)
    status = Column(String(20), default='in_progress')  # in_progress, completed, abandoned
    current_question_index = Column(Integer, default=0)
    total_score = Column(Float, default=0)
    max_score = Column(Float, default=0)
    
    # Contraintes
    __table_args__ = (
        CheckConstraint(status.in_(['in_progress', 'completed', 'abandoned']), name='valid_attempt_status'),
    )
    
    # Relations
    test = relationship("AdaptiveTest", back_populates="attempts")
    assignment = relationship("TestAssignment", back_populates="attempts")
    responses = relationship("QuestionResponse", back_populates="attempt", cascade="all, delete-orphan")
    competency_analyses = relationship("CompetencyAnalysis", back_populates="attempt", cascade="all, delete-orphan")

class QuestionResponse(Base):
    """Modèle pour les réponses aux questions"""
    __tablename__ = "question_responses"
    
    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("test_attempts.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("adaptive_questions.id"), nullable=False)
    student_answer = Column(Text)
    is_correct = Column(Boolean)
    score = Column(Float, default=0)
    response_time = Column(Integer)  # en secondes
    answered_at = Column(DateTime, default=func.now())
    
    # Relations
    attempt = relationship("TestAttempt", back_populates="responses")
    question = relationship("AdaptiveQuestion", back_populates="responses")

class CompetencyAnalysis(Base):
    """Modèle pour l'analyse des compétences par l'IA"""
    __tablename__ = "competency_analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("test_attempts.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    test_id = Column(Integer, ForeignKey("adaptive_tests.id"), nullable=False)
    competency_name = Column(String(255), nullable=False)
    competency_level = Column(Float, default=0)  # 0-100
    confidence_score = Column(Float, default=0)  # 0-100
    ai_recommendations = Column(Text)
    analyzed_at = Column(DateTime, default=func.now())
    
    # Relations
    attempt = relationship("TestAttempt", back_populates="competency_analyses")

class Class(Base):
    """Modèle pour les classes"""
    __tablename__ = "classes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # Relations
    adaptive_students = relationship("AdaptiveClassStudent", back_populates="class_", cascade="all, delete-orphan")

class AdaptiveClassStudent(Base):
    """Modèle pour la relation entre classes et étudiants dans l'évaluation adaptative"""
    __tablename__ = "adaptive_class_students"
    
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    joined_at = Column(DateTime, default=func.now())
    
    # Relations
    class_ = relationship("Class", back_populates="adaptive_students")
    
    # Contrainte d'unicité
    __table_args__ = (
        CheckConstraint('class_id != student_id', name='valid_adaptive_class_student'),
    )
