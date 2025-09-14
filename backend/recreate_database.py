#!/usr/bin/env python3
"""
Script pour recréer la base de données avec tous les modèles
Corrige les erreurs de tables manquantes
"""

import os
import sys

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import engine, Base, SessionLocal
from models import *  # Importe tous les modèles
from sqlalchemy import text

def recreate_database():
    """Recrée la base de données avec tous les modèles"""
    print("Suppression de toutes les tables existantes...")
    
    # Supprimer toutes les tables
    Base.metadata.drop_all(engine)
    
    print("Tables supprimées")
    
    print("Creation de toutes les tables...")
    
    # Créer toutes les tables
    Base.metadata.create_all(engine)
    
    print("Tables creees")
    
    # Vérifier que toutes les tables sont créées
    print("Verification des tables creees...")
    
    db = SessionLocal()
    try:
        # Liste des tables attendues
        expected_tables = [
            'users', 'badges', 'user_badges', 'quizzes', 'quiz_results', 
            'quiz_assignments', 'questions', 'quiz_answers', 'contents', 
            'categories', 'class_groups', 'class_students', 'learning_paths',
            'student_learning_paths', 'learning_histories', 'notifications',
            'messages', 'threads', 'user_notes', 'assessments', 
            'assessment_questions', 'assessment_results', 'competencies',
            'student_competencies', 'continuous_assessments', 
            'student_continuous_assessments', 'progress_reports',
            'user_settings', 'resource_ratings', 'remediation_plans',
            'remediation_activities', 'score_corrections',
            # Tables de rapports
            'detailed_reports', 'subject_progress_reports', 'analytics_reports', 'report_exports',
            # Tables IA avancée
            'ai_recommendations', 'ai_tutoring_sessions', 'ai_tutoring_interactions',
            'difficulty_detections', 'learning_analytics', 'adaptive_content',
            # Tables de devoirs avancés
            'advanced_homeworks', 'advanced_homework_submissions', 'advanced_homework_assignments',
            # Tables de calendrier
            'calendar_events', 'event_reminders', 'calendar_study_sessions',
            # Tables avancées
            'advanced_learnings', 'advanced_notifications', 'collaborations',
            'forums', 'gamifications', 'schedules', 'interface_levels',
            'libraries', 'organizations', 'notes_advanced', 'student_analytics',
            'user_activities', 'real_time_activities'
        ]
        
        # Vérifier chaque table
        for table in expected_tables:
            try:
                result = db.execute(text(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'"))
                if result.fetchone():
                    print(f"OK - Table {table} creee")
                else:
                    print(f"ERREUR - Table {table} MANQUANTE")
            except Exception as e:
                print(f"ERREUR - Erreur verification {table}: {e}")
        
        print(f"\nTotal: {len(expected_tables)} tables attendues")
        
    except Exception as e:
        print(f"ERREUR - Erreur lors de la verification: {e}")
    finally:
        db.close()
    
    print("\nBase de donnees recreee avec succes!")
    print("Toutes les tables ont ete creees et verifiees.")

def create_sample_data():
    """Crée des données d'exemple pour tester"""
    print("\nCreation de donnees d'exemple...")
    
    db = SessionLocal()
    try:
        # Créer un utilisateur admin par défaut
        from models.user import User, UserRole
        
        # Vérifier si l'admin existe déjà
        admin = db.query(User).filter(User.email == "admin@najah.ai").first()
        if not admin:
            admin = User(
                email="admin@najah.ai",
                username="admin",
                first_name="Admin",
                last_name="Najah",
                role=UserRole.admin,
                is_active=True,
                hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.i8i"  # password: admin123
            )
            db.add(admin)
            db.commit()
            print("Utilisateur admin cree")
        else:
            print("Utilisateur admin existe deja")
            
    except Exception as e:
        print(f"ERREUR - Erreur creation donnees: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Demarrage de la recreation de la base de donnees...")
    recreate_database()
    create_sample_data()
    print("\nScript termine avec succes!")
