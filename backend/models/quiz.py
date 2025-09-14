from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base
import enum
from datetime import datetime

class QuizType(enum.Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"
    ESSAY = "essay"
    MATCHING = "matching"

class Quiz(Base):
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    subject = Column(String(100), nullable=True)
    level = Column(String(50), nullable=True)
    difficulty = Column(String(50), default="medium")
    time_limit = Column(Integer, nullable=True)  # en minutes
    max_score = Column(Integer, default=100)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    creator = relationship("User", foreign_keys=[created_by], viewonly=True)
    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")
    results = relationship("QuizResult", back_populates="quiz", cascade="all, delete-orphan")
    assignments = relationship("QuizAssignment", back_populates="quiz", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Quiz(id={self.id}, title='{self.title}', subject='{self.subject}')>"

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50), default="multiple_choice")
    options = Column(JSON, nullable=True)  # Pour les questions à choix multiples
    correct_answer = Column(String(255), nullable=True)
    points = Column(Integer, default=1)
    order = Column(Integer, default=0)
    
    # Relations
    quiz = relationship("Quiz", back_populates="questions")
    answers = relationship("QuizAnswer", back_populates="question", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Question(id={self.id}, quiz_id={self.quiz_id}, text='{self.question_text[:50]}...')>"

class QuizResult(Base):
    __tablename__ = "quiz_results"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    score = Column(Float, nullable=False)
    max_score = Column(Float, nullable=False)
    percentage = Column(Float, nullable=False)
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, default=datetime.utcnow)
    sujet = Column(String(100), nullable=True)
    answers = Column(Text)  # JSON string des réponses
    time_spent = Column(Integer)  # en secondes
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    quiz = relationship("Quiz", back_populates="results")
    student = relationship("User", foreign_keys=[student_id], viewonly=True)
    quiz_answers = relationship("QuizAnswer", back_populates="result", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<QuizResult(id={self.id}, quiz_id={self.quiz_id}, student_id={self.student_id}, score={self.score})>"

class QuizAnswer(Base):
    __tablename__ = "quiz_answers"
    
    id = Column(Integer, primary_key=True, index=True)
    result_id = Column(Integer, ForeignKey("quiz_results.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    answer_text = Column(Text, nullable=True)
    is_correct = Column(Boolean, nullable=True)
    points_earned = Column(Float, default=0.0)
    
    # Relations
    result = relationship("QuizResult", back_populates="quiz_answers")
    question = relationship("Question", back_populates="answers")
    
    def __repr__(self):
        return f"<QuizAnswer(id={self.id}, result_id={self.result_id}, question_id={self.question_id})>"

class QuizAssignment(Base):
    __tablename__ = "quiz_assignments"
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("class_groups.id"), nullable=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Peut être null si assigné à une classe
    assigned_by = Column(Integer, ForeignKey("users.id"), nullable=False)  # Qui a assigné le quiz
    due_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(50), default="assigned")  # assigned, in_progress, completed, overdue
    score = Column(Integer, nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    feedback = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relations
    quiz = relationship("Quiz", back_populates="assignments")
    student = relationship("User", foreign_keys=[student_id], viewonly=True)
    teacher = relationship("User", foreign_keys=[assigned_by], viewonly=True)
    
    def __repr__(self):
        return f"<QuizAssignment(id={self.id}, quiz_id={self.quiz_id}, class_id={self.class_id}, student_id={self.student_id})>" 