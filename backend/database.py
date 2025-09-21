from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import os
from datetime import datetime

# Configuration de la base de données
DATABASE_URL = "sqlite:///./najah_ai.db"

# Créer le moteur SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False
)

# Créer la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles
Base = declarative_base()

# Modèles pour les nouvelles fonctionnalités avancées

class ExtendedQuestion(Base):
    """Table pour la banque de questions étendue"""
    __tablename__ = "extended_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50), nullable=False)  # multiple_choice, free_text, image
    subject = Column(String(100), nullable=False)
    difficulty = Column(Integer, nullable=False)  # 1-10
    competency = Column(String(200), nullable=True)
    learning_style = Column(String(100), nullable=True)  # visual, auditory, kinesthetic, reading_writing
    options = Column(JSON, nullable=True)  # Pour les questions QCM
    correct_answer = Column(Text, nullable=False)
    explanation = Column(Text, nullable=True)
    estimated_time = Column(Integer, nullable=True)  # en secondes
    cognitive_load = Column(Float, nullable=True)  # 0.0-1.0
    tags = Column(JSON, nullable=True)
    curriculum_standards = Column(Text, nullable=True)
    prerequisites = Column(Text, nullable=True)
    learning_objectives = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class QuestionMetadata(Base):
    """Métadonnées supplémentaires pour les questions"""
    __tablename__ = "question_metadata"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("extended_questions.id"), nullable=False)
    bloom_taxonomy_level = Column(String(50), nullable=True)  # remember, understand, apply, analyze, evaluate, create
    knowledge_type = Column(String(50), nullable=True)  # factual, conceptual, procedural, metacognitive
    cognitive_domain = Column(String(50), nullable=True)  # knowledge, comprehension, application, analysis, synthesis, evaluation
    difficulty_justification = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class QuestionTag(Base):
    """Tags pour catégoriser les questions"""
    __tablename__ = "question_tags"
    
    id = Column(Integer, primary_key=True, index=True)
    tag = Column(String(100), unique=True, nullable=False)
    category = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class QuestionTagRelation(Base):
    """Relation many-to-many entre questions et tags"""
    __tablename__ = "question_tag_relations"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("extended_questions.id"), nullable=False)
    tag_id = Column(Integer, ForeignKey("question_tags.id"), nullable=False)

class CognitiveProfile(Base):
    """Profils cognitifs des étudiants"""
    __tablename__ = "cognitive_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, nullable=False)
    learning_style = Column(String(100), nullable=False)
    strengths = Column(JSON, nullable=True)
    weaknesses = Column(JSON, nullable=True)
    recommendations = Column(JSON, nullable=True)
    confidence_level = Column(Float, nullable=True)  # 0.0-1.0
    generated_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ResponseAnalysis(Base):
    """Analyses des réponses des étudiants"""
    __tablename__ = "response_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, nullable=False)
    question_id = Column(Integer, nullable=False)
    response_time = Column(Integer, nullable=True)  # en millisecondes
    is_correct = Column(Boolean, nullable=False)
    time_analysis = Column(JSON, nullable=True)
    pattern = Column(String(100), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

class StudentAbility(Base):
    """Capacités estimées des étudiants (IRT)"""
    __tablename__ = "student_abilities"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, nullable=False)
    ability_level = Column(Float, nullable=False)  # niveau de capacité estimé
    confidence_interval = Column(JSON, nullable=True)  # intervalle de confiance
    estimated_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AdaptiveSession(Base):
    """Sessions d'évaluation adaptative"""
    __tablename__ = "adaptive_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, nullable=False)
    session_start = Column(DateTime, default=datetime.utcnow)
    session_end = Column(DateTime, nullable=True)
    initial_difficulty = Column(Integer, nullable=False)
    final_difficulty = Column(Integer, nullable=True)
    questions_answered = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    total_time = Column(Integer, nullable=True)  # en secondes
    cognitive_load_tracking = Column(JSON, nullable=True)
    adaptation_history = Column(JSON, nullable=True)

# Fonction pour obtenir la session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Fonction pour créer toutes les tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# Fonction pour vérifier la connexion
def check_connection():
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return True
    except Exception as e:
        print(f"Erreur de connexion à la base de données: {e}")
        return False

# Initialisation automatique des tables
if __name__ == "__main__":
    print("🔧 Création des tables de base de données...")
    create_tables()
    print("✅ Tables créées avec succès!")
    
    if check_connection():
        print("✅ Connexion à la base de données réussie!")
    else:
        print("❌ Erreur de connexion à la base de données!")















