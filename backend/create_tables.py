#!/usr/bin/env python3
"""
Script pour créer les tables nécessaires pour les évaluations et parcours d'apprentissage
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Configuration de la base de données
DATABASE_URL = "sqlite:///./data/app.db"

# Créer le moteur SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True
)

# Créer la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles
Base = declarative_base()

# Modèle User
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="student")  # student, teacher, admin
    is_active = Column(Boolean, default=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    avatar = Column(String(255))
    phone = Column(String(20))
    date_of_birth = Column(DateTime)
    bio = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

# Modèle Assessment
class Assessment(Base):
    __tablename__ = "assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    subject = Column(String(100), nullable=False)
    difficulty = Column(String(20), default="medium")  # easy, medium, hard
    estimated_time = Column(Integer)  # en minutes
    status = Column(String(20), default="pending")  # pending, in_progress, completed
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime)

# Modèle AssessmentResult
class AssessmentResult(Base):
    __tablename__ = "assessment_results"
    
    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    score = Column(Float, nullable=False)
    max_score = Column(Float, nullable=False)
    percentage = Column(Float, nullable=False)
    completed_at = Column(DateTime, default=datetime.utcnow)
    strengths = Column(Text)  # JSON string
    weaknesses = Column(Text)  # JSON string
    recommendations = Column(Text)  # JSON string

# Modèle LearningPath
class LearningPath(Base):
    __tablename__ = "learning_paths"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    subject = Column(String(100), nullable=False)
    difficulty = Column(String(20), default="medium")
    estimated_duration = Column(Integer)  # en minutes
    created_at = Column(DateTime, default=datetime.utcnow)

# Modèle LearningPathStep
class LearningPathStep(Base):
    __tablename__ = "learning_path_steps"
    
    id = Column(Integer, primary_key=True, index=True)
    learning_path_id = Column(Integer, ForeignKey("learning_paths.id"), nullable=False)
    step_number = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    content_type = Column(String(50))  # quiz, content, exercise, assessment
    estimated_duration = Column(Integer)  # en minutes
    is_required = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    is_completed = Column(Boolean, default=False)

# Modèle StudentLearningPath
class StudentLearningPath(Base):
    __tablename__ = "student_learning_paths"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    learning_path_id = Column(Integer, ForeignKey("learning_paths.id"), nullable=False)
    progress = Column(Float, default=0.0)  # pourcentage de progression
    current_step = Column(Integer, default=1)
    total_steps = Column(Integer, default=1)
    started_at = Column(DateTime, default=datetime.utcnow)
    is_completed = Column(Boolean, default=False)

def create_tables():
    """Créer toutes les tables"""
    print("=== CRÉATION DES TABLES ===")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables créées avec succès!")

def create_test_data():
    """Créer des données de test"""
    print("\n=== CRÉATION DE DONNÉES DE TEST ===")
    
    db = SessionLocal()
    try:
        # 1. Créer un utilisateur de test
        print("1. Création d'un utilisateur de test...")
        user = User(
            username='student30',
            email='student30@test.com',
            hashed_password='test123',
            role='student',
            first_name='Étudiant',
            last_name='Test'
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"✅ Utilisateur créé avec ID: {user.id}")
        
        # 2. Créer des évaluations de test
        print("2. Création d'évaluations de test...")
        assessment1 = Assessment(
            title='Évaluation Mathématiques',
            description='Test de connaissances en algèbre',
            subject='Mathématiques',
            difficulty='medium',
            estimated_time=30,
            status='pending',
            student_id=user.id
        )
        assessment2 = Assessment(
            title='Évaluation Physique',
            description='Test de mécanique',
            subject='Physique',
            difficulty='easy',
            estimated_time=25,
            status='completed',
            student_id=user.id
        )
        db.add(assessment1)
        db.add(assessment2)
        db.commit()
        print("✅ Évaluations créées")
        
        # 3. Créer des parcours d'apprentissage
        print("3. Création de parcours d'apprentissage...")
        path1 = LearningPath(
            title='Parcours Mathématiques',
            subject='Mathématiques',
            difficulty='medium',
            estimated_duration=120
        )
        path2 = LearningPath(
            title='Parcours Physique',
            subject='Physique',
            difficulty='easy',
            estimated_duration=90
        )
        db.add(path1)
        db.add(path2)
        db.commit()
        db.refresh(path1)
        db.refresh(path2)
        print("✅ Parcours créés")
        
        # 4. Créer des relations étudiant-parcours
        print("4. Création des relations étudiant-parcours...")
        student_path1 = StudentLearningPath(
            student_id=user.id,
            learning_path_id=path1.id,
            progress=25.0,
            current_step=2,
            total_steps=8,
            started_at=datetime(2024, 1, 15),
            is_completed=False
        )
        student_path2 = StudentLearningPath(
            student_id=user.id,
            learning_path_id=path2.id,
            progress=100.0,
            current_step=5,
            total_steps=5,
            started_at=datetime(2024, 1, 10),
            is_completed=True
        )
        db.add(student_path1)
        db.add(student_path2)
        db.commit()
        print("✅ Relations étudiant-parcours créées")
        
        # 5. Vérification des données créées
        print("5. Vérification des données créées...")
        assessments = db.query(Assessment).filter(Assessment.student_id == user.id).all()
        student_paths = db.query(StudentLearningPath).filter(StudentLearningPath.student_id == user.id).all()
        print(f"✅ Évaluations créées: {len(assessments)}")
        print(f"✅ Parcours étudiants créés: {len(student_paths)}")
        print(f"🎯 DONNÉES DE TEST CRÉÉES POUR L'UTILISATEUR {user.id}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des données: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_tables()
    create_test_data()
    print("\n🎉 SCRIPT TERMINÉ AVEC SUCCÈS!")



