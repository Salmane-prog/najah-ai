from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, DateTime, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class FrenchLearningProfile(Base):
    """Profil d'apprentissage français d'un étudiant"""
    __tablename__ = "french_learning_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    learning_style = Column(String, nullable=False)  # "visual", "auditory", "kinesthetic"
    french_level = Column(String, nullable=False)    # "A1", "A2", "B1", "B2", "C1", "C2"
    preferred_pace = Column(String, nullable=False)  # "lent", "moyen", "rapide"
    strengths = Column(Text, nullable=True)          # JSON des forces
    weaknesses = Column(Text, nullable=True)         # JSON des faiblesses
    cognitive_profile = Column(Text, nullable=True)  # JSON du profil cognitif
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    student = relationship("User", foreign_keys=[student_id])
    competency_progress = relationship("FrenchCompetencyProgress", back_populates="profile")

class FrenchCompetency(Base):
    """Compétences françaises spécifiques"""
    __tablename__ = "french_competencies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)            # "Grammaire", "Vocabulaire", "Compréhension"
    category = Column(String, nullable=False)        # "Écrit", "Oral", "Compréhension"
    difficulty_level = Column(String, nullable=False) # "A1", "A2", "B1", "B2", "C1", "C2"
    description = Column(Text, nullable=True)
    prerequisites = Column(Text, nullable=True)      # JSON des prérequis
    estimated_hours = Column(Integer, default=2)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    progress_records = relationship("FrenchCompetencyProgress", back_populates="competency")
    remediation_plans = relationship("FrenchRemediation", back_populates="competency")

class FrenchCompetencyProgress(Base):
    """Progression des compétences françaises d'un étudiant"""
    __tablename__ = "french_competency_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    competency_id = Column(Integer, ForeignKey("french_competencies.id"), nullable=False)
    profile_id = Column(Integer, ForeignKey("french_learning_profiles.id"), nullable=True)  # Added missing foreign key
    current_level = Column(String, nullable=False)    # "A1", "A2", "B1", "B2", "C1", "C2"
    progress_percentage = Column(Float, default=0.0)
    last_assessed = Column(DateTime, nullable=True)
    next_assessment_date = Column(DateTime, nullable=True)
    attempts_count = Column(Integer, default=0)
    best_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    student = relationship("User", foreign_keys=[student_id])
    competency = relationship("FrenchCompetency", back_populates="progress_records")
    profile = relationship("FrenchLearningProfile", back_populates="competency_progress")

class FrenchAdaptiveTest(Base):
    """Tests adaptatifs français"""
    __tablename__ = "french_adaptive_tests"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    test_type = Column(String, nullable=False)       # "initial", "progress", "remediation"
    current_question_index = Column(Integer, default=0)
    total_questions = Column(Integer, nullable=True)  # Nullable pour le système adaptatif
    current_difficulty = Column(String, nullable=False) # "facile", "moyen", "difficile"
    status = Column(String, default="in_progress")   # "in_progress", "completed", "paused"
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    final_score = Column(Float, nullable=True)
    difficulty_progression = Column(Text, nullable=True)  # JSON de la progression de difficulté
    level_progression = Column(String, default="A1")     # Niveau de progression actuel
    current_level = Column(String, default="A1")         # Niveau actuel de l'étudiant
    
    # Relations
    student = relationship("User", foreign_keys=[student_id])

class FrenchLearningPath(Base):
    """Parcours d'apprentissage français personnalisé"""
    __tablename__ = "french_learning_paths"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    path_name = Column(String, nullable=False)       # "Parcours Débutant", "Parcours Intermédiaire"
    current_module = Column(Integer, default=1)
    total_modules = Column(Integer, nullable=False)
    completion_percentage = Column(Float, default=0.0)
    estimated_completion_date = Column(DateTime, nullable=True)
    status = Column(String, default="active")        # "active", "paused", "completed"
    difficulty_level = Column(String, nullable=False) # "A1", "A2", "B1", "B2", "C1", "C2"
    learning_objectives = Column(Text, nullable=True) # JSON des objectifs d'apprentissage
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    student = relationship("User", foreign_keys=[student_id])
    modules = relationship("FrenchLearningModule", back_populates="learning_path", order_by="FrenchLearningModule.module_order")

class FrenchLearningModule(Base):
    """Modules d'apprentissage français"""
    __tablename__ = "french_learning_modules"
    
    id = Column(Integer, primary_key=True, index=True)
    path_id = Column(Integer, ForeignKey("french_learning_paths.id"), nullable=False)
    module_name = Column(String, nullable=False)
    module_order = Column(Integer, nullable=False)
    difficulty_level = Column(String, nullable=False) # "A1", "A2", "B1", "B2", "C1", "C2"
    estimated_duration = Column(Integer, default=30)  # en minutes
    content_type = Column(String, nullable=False)     # "video", "text", "quiz", "exercise"
    content_data = Column(Text, nullable=True)        # JSON du contenu
    prerequisites = Column(Text, nullable=True)       # JSON des prérequis
    learning_outcomes = Column(Text, nullable=True)   # JSON des résultats d'apprentissage
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    learning_path = relationship("FrenchLearningPath", back_populates="modules")

class FrenchRemediation(Base):
    """Plans de remédiation française"""
    __tablename__ = "french_remediation"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    competency_id = Column(Integer, ForeignKey("french_competencies.id"), nullable=False)
    difficulty_type = Column(String, nullable=False)  # "grammar", "vocabulary", "comprehension"
    remediation_plan = Column(Text, nullable=False)  # Plan de remédiation détaillé
    exercises = Column(Text, nullable=True)          # JSON des exercices
    status = Column(String, default="active")        # "active", "completed", "paused"
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    effectiveness_score = Column(Float, nullable=True) # Score d'efficacité de la remédiation
    
    # Relations
    student = relationship("User", foreign_keys=[student_id])
    competency = relationship("FrenchCompetency", back_populates="remediation_plans")

class FrenchRecommendation(Base):
    """Recommandations françaises personnalisées"""
    __tablename__ = "french_recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recommendation_type = Column(String, nullable=False) # "content", "exercise", "quiz", "path"
    content_id = Column(Integer, nullable=True)         # ID du contenu recommandé
    content_type = Column(String, nullable=False)       # Type de contenu
    reason = Column(Text, nullable=False)               # Raison de la recommandation
    priority = Column(String, default="medium")         # "low", "medium", "high"
    status = Column(String, default="pending")          # "pending", "accepted", "dismissed"
    created_at = Column(DateTime, default=datetime.utcnow)
    accepted_at = Column(DateTime, nullable=True)
    dismissed_at = Column(DateTime, nullable=True)
    
    # Relations
    student = relationship("User", foreign_keys=[student_id])
