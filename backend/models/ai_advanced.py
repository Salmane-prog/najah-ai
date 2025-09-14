from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base
from datetime import datetime

class AIRecommendation(Base):
    __tablename__ = "ai_recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recommendation_type = Column(String(50), nullable=False)  # content, quiz, learning_path, study_session
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=True)
    learning_path_id = Column(Integer, ForeignKey("learning_paths.id"), nullable=True)
    confidence_score = Column(Float, default=0.0)  # 0.0 to 1.0
    reason = Column(Text, nullable=True)  # Pourquoi cette recommandation
    is_accepted = Column(Boolean, default=False)
    is_dismissed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    user = relationship("User", foreign_keys=[user_id])
    content = relationship("Content")
    quiz = relationship("Quiz")
    learning_path = relationship("LearningPath")

class AITutoringSession(Base):
    __tablename__ = "ai_tutoring_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject = Column(String(100), nullable=True)
    topic = Column(String(255), nullable=True)
    session_type = Column(String(50), default="general")  # general, specific_topic, problem_solving
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True), nullable=True)
    duration = Column(Integer, nullable=True)  # en minutes
    status = Column(String(20), default="active")  # active, completed, paused
    notes = Column(Text, nullable=True)
    
    # Relations
    user = relationship("User", foreign_keys=[user_id])
    interactions = relationship("AITutoringInteraction", back_populates="session")

class AITutoringInteraction(Base):
    __tablename__ = "ai_tutoring_interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("ai_tutoring_sessions.id"), nullable=False)
    user_message = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    interaction_type = Column(String(50), default="question")  # question, explanation, hint, feedback
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    user_satisfaction = Column(Integer, nullable=True)  # 1-5 rating
    
    # Relations
    session = relationship("AITutoringSession", back_populates="interactions")

class DifficultyDetection(Base):
    __tablename__ = "difficulty_detections"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject = Column(String(100), nullable=False)
    topic = Column(String(255), nullable=False)
    difficulty_level = Column(String(20), nullable=False)  # low, medium, high
    confidence_score = Column(Float, default=0.0)
    evidence = Column(JSON, nullable=True)  # Données supportant la détection
    detected_at = Column(DateTime(timezone=True), server_default=func.now())
    is_resolved = Column(Boolean, default=False)
    resolution_notes = Column(Text, nullable=True)
    
    # Relations
    user = relationship("User", foreign_keys=[user_id])



class AdaptiveContent(Base):
    __tablename__ = "adaptive_content"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=False)
    adaptation_type = Column(String(50), nullable=False)  # difficulty, format, pace, style
    original_content = Column(JSON, nullable=True)  # Contenu original
    adapted_content = Column(JSON, nullable=False)  # Contenu adapté
    adaptation_reason = Column(Text, nullable=True)  # Raison de l'adaptation
    effectiveness_score = Column(Float, nullable=True)  # Score d'efficacité
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    user = relationship("User", foreign_keys=[user_id])
    content = relationship("Content")
