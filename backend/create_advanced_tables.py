#!/usr/bin/env python3
"""
Script pour créer les tables avancées de l'interface enseignant
"""
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from core.database import Base, engine
from models.advanced_learning import (
    LearningPathStep, StudentProgress, ClassAnalytics, 
    StudentAnalytics, RealTimeActivity, LearningPath, ClassGroup
)
from models.class_group import ClassStudent
from models.user import User
from models.quiz import Quiz, QuizResult
from models.content import Content

def create_advanced_tables():
    """Créer toutes les tables avancées"""
    print("🔧 Création des tables avancées pour l'interface enseignant...")
    
    try:
        # Créer toutes les tables
        Base.metadata.create_all(bind=engine)
        print("✅ Tables créées avec succès!")
        
        # Vérifier que les tables existent
        with engine.connect() as conn:
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
            tables = [row[0] for row in result]
            
            required_tables = [
                'learning_path_steps',
                'student_progress', 
                'class_analytics',
                'student_analytics',
                'real_time_activities'
            ]
            
            missing_tables = [table for table in required_tables if table not in tables]
            
            if missing_tables:
                print(f"❌ Tables manquantes: {missing_tables}")
                return False
            else:
                print("✅ Toutes les tables requises sont présentes")
                return True
                
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables: {e}")
        return False

def update_existing_tables():
    """Mettre à jour les tables existantes avec les nouveaux champs"""
    print("🔄 Mise à jour des tables existantes...")
    
    try:
        with engine.connect() as conn:
            # Vérifier si les colonnes existent déjà
            result = conn.execute(text("PRAGMA table_info(learning_paths);"))
            columns = [row[1] for row in result]
            
            # Ajouter les nouvelles colonnes si elles n'existent pas
            new_columns = [
                ("level", "TEXT"),
                ("estimated_duration", "INTEGER DEFAULT 30"),
                ("is_adaptive", "BOOLEAN DEFAULT 0"),
                ("created_by", "INTEGER"),
                ("created_at", "DATETIME"),
                ("updated_at", "DATETIME")
            ]
            
            for col_name, col_type in new_columns:
                if col_name not in columns:
                    conn.execute(text(f"ALTER TABLE learning_paths ADD COLUMN {col_name} {col_type};"))
                    print(f"✅ Colonne {col_name} ajoutée à learning_paths")
            
            # Mettre à jour la table class_groups
            result = conn.execute(text("PRAGMA table_info(class_groups);"))
            columns = [row[1] for row in result]
            
            new_class_columns = [
                ("level", "TEXT"),
                ("subject", "TEXT"),
                ("max_students", "INTEGER DEFAULT 30"),
                ("is_active", "BOOLEAN DEFAULT 1"),
                ("created_at", "DATETIME")
            ]
            
            for col_name, col_type in new_class_columns:
                if col_name not in columns:
                    conn.execute(text(f"ALTER TABLE class_groups ADD COLUMN {col_name} {col_type};"))
                    print(f"✅ Colonne {col_name} ajoutée à class_groups")
            
            conn.commit()
            print("✅ Tables existantes mises à jour")
            return True
            
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour des tables: {e}")
        return False

def create_sample_data():
    """Créer des données d'exemple pour tester"""
    print("📝 Création de données d'exemple...")
    
    try:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Créer un enseignant de test s'il n'existe pas
        teacher = db.query(User).filter(User.email == "teacher@test.com").first()
        if not teacher:
            teacher = User(
                username="teacher_test",
                email="teacher@test.com",
                hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj3bp.gS.Oe",  # password123
                role="teacher"
            )
            db.add(teacher)
            db.commit()
            db.refresh(teacher)
            print("✅ Enseignant de test créé")
        
        # Créer une classe de test
        test_class = db.query(ClassGroup).filter(ClassGroup.name == "Classe Test").first()
        if not test_class:
            test_class = ClassGroup(
                name="Classe Test",
                description="Classe de test pour l'interface avancée",
                teacher_id=teacher.id,
                level="middle",
                subject="Mathématiques",
                max_students=25
            )
            db.add(test_class)
            db.commit()
            db.refresh(test_class)
            print("✅ Classe de test créée")
        
        # Créer un parcours de test
        test_path = db.query(LearningPath).filter(LearningPath.name == "Parcours Test").first()
        if not test_path:
            test_path = LearningPath(
                name="Parcours Test",
                description="Parcours de test pour l'interface avancée",
                objectives="Tester les fonctionnalités avancées",
                level="intermediate",
                estimated_duration=15,
                is_adaptive=True,
                created_by=teacher.id
            )
            db.add(test_path)
            db.commit()
            db.refresh(test_path)
            print("✅ Parcours de test créé")
        
        # Créer des étapes de test
        test_steps = [
            {
                "title": "Introduction aux concepts",
                "description": "Première étape du parcours",
                "step_type": "content",
                "order": 1,
                "estimated_duration": 20
            },
            {
                "title": "Quiz de vérification",
                "description": "Quiz pour vérifier les acquis",
                "step_type": "quiz",
                "order": 2,
                "estimated_duration": 15
            },
            {
                "title": "Exercices pratiques",
                "description": "Application des concepts",
                "step_type": "activity",
                "order": 3,
                "estimated_duration": 30
            }
        ]
        
        for step_data in test_steps:
            existing_step = db.query(LearningPathStep).filter(
                LearningPathStep.learning_path_id == test_path.id,
                LearningPathStep.title == step_data["title"]
            ).first()
            
            if not existing_step:
                step = LearningPathStep(
                    learning_path_id=test_path.id,
                    title=step_data["title"],
                    description=step_data["description"],
                    step_type=step_data["step_type"],
                    order=step_data["order"],
                    estimated_duration=step_data["estimated_duration"]
                )
                db.add(step)
                print(f"✅ Étape '{step_data['title']}' créée")
        
        db.commit()
        print("✅ Données d'exemple créées avec succès")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des données d'exemple: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Fonction principale"""
    print("🚀 Configuration de l'interface enseignant avancée")
    print("=" * 60)
    
    # Créer les nouvelles tables
    if not create_advanced_tables():
        print("❌ Échec de la création des tables")
        return
    
    # Mettre à jour les tables existantes
    if not update_existing_tables():
        print("❌ Échec de la mise à jour des tables")
        return
    
    # Créer des données d'exemple
    create_sample_data()
    
    print("\n" + "=" * 60)
    print("✅ Configuration terminée avec succès!")
    print("\n📋 Fonctionnalités disponibles:")
    print("   • Gestion avancée des classes")
    print("   • Création de parcours avec étapes")
    print("   • Suivi temps réel des étudiants")
    print("   • Analytics détaillés")
    print("   • Rapports avancés")
    print("\n🔗 Endpoints disponibles:")
    print("   • GET /api/v1/teacher/classes/")
    print("   • POST /api/v1/teacher/classes/")
    print("   • GET /api/v1/teacher/classes/{class_id}/analytics")
    print("   • POST /api/v1/teacher/learning-paths/")
    print("   • GET /api/v1/teacher/realtime/dashboard")
    print("   • GET /api/v1/teacher/reports/student/{student_id}")
    print("   • GET /api/v1/teacher/reports/class/{class_id}")

if __name__ == "__main__":
    main() 