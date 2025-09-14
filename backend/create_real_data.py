#!/usr/bin/env python3
"""
Script pour créer des données réelles pour tester l'interface enseignant avancée
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Forcer la configuration de la base de données
os.environ["SQLALCHEMY_DATABASE_URL"] = "sqlite:///F:/IMT/stage/Yancode/Najah__AI/data/app.db"

from core.database import get_db
from models.user import User
from models.class_group import ClassGroup, ClassStudent
from models.learning_path import LearningPath, StudentLearningPath
from models.quiz import Quiz, QuizResult
from models.advanced_learning import (
    LearningPathStep, StudentProgress, ClassAnalytics, 
    StudentAnalytics, RealTimeActivity
)
from core.security import get_password_hash
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import json

def create_real_data():
    """Créer des données réelles pour l'interface avancée"""
    print("🚀 CRÉATION DE DONNÉES RÉELLES POUR L'INTERFACE AVANCÉE")
    print("=" * 60)
    
    db = next(get_db())
    
    try:
        # 1. Créer des classes avancées
        print("📚 Création des classes avancées...")
        
        # Classe Mathématiques Avancées
        math_class = ClassGroup(
            name="Mathématiques Avancées",
            description="Cours de mathématiques pour niveau intermédiaire",
            teacher_id=1,  # marie.dubois@najah.ai
            level="intermediate",
            subject="Mathématiques",
            max_students=25,
            is_active=True
        )
        db.add(math_class)
        
        # Classe Français Littéraire
        french_class = ClassGroup(
            name="Français Littéraire",
            description="Étude de la littérature française",
            teacher_id=1,
            level="advanced",
            subject="Français",
            max_students=20,
            is_active=True
        )
        db.add(french_class)
        
        # Classe Sciences Expérimentales
        science_class = ClassGroup(
            name="Sciences Expérimentales",
            description="Physique et chimie pratiques",
            teacher_id=1,
            level="intermediate",
            subject="Sciences",
            max_students=30,
            is_active=True
        )
        db.add(science_class)
        
        db.commit()
        print("✅ Classes créées avec succès")
        
        # 2. Assigner des étudiants aux classes
        print("👥 Assignation des étudiants aux classes...")
        
        # Récupérer les étudiants existants
        students = db.query(User).filter(User.role == 'student').limit(6).all()
        
        # Assigner aux classes
        class_assignments = [
            (students[0].id, math_class.id),
            (students[1].id, math_class.id),
            (students[2].id, french_class.id),
            (students[3].id, french_class.id),
            (students[4].id, science_class.id),
            (students[5].id, science_class.id),
        ]
        
        for student_id, class_id in class_assignments:
            assignment = ClassStudent(
                class_id=class_id,
                student_id=student_id
            )
            db.add(assignment)
        
        db.commit()
        print("✅ Étudiants assignés aux classes")
        
        # 3. Créer des parcours d'apprentissage avancés
        print("📖 Création des parcours d'apprentissage...")
        
        # Parcours Mathématiques
        math_path = LearningPath(
            title="Parcours Mathématiques Intermédiaire",
            description="Apprentissage progressif des mathématiques",
            objectives="Maîtriser les concepts de base et intermédiaires",
            subject="Mathématiques",
            level="intermediate",
            difficulty="intermediate",
            estimated_duration=45,
            is_adaptive=True,
            created_by=1
        )
        db.add(math_path)
        
        # Parcours Français
        french_path = LearningPath(
            title="Littérature Française Moderne",
            description="Étude des œuvres littéraires modernes",
            objectives="Comprendre et analyser les textes littéraires",
            subject="Français",
            level="advanced",
            difficulty="advanced",
            estimated_duration=30,
            is_adaptive=False,
            created_by=1
        )
        db.add(french_path)
        
        db.commit()
        print("✅ Parcours d'apprentissage créés")
        
        # 4. Créer des étapes pour les parcours
        print("📝 Création des étapes de parcours...")
        
        # Étapes pour le parcours mathématiques
        math_steps = [
            {
                "title": "Introduction aux équations",
                "description": "Comprendre les bases des équations",
                "step_type": "content",
                "order": 1,
                "estimated_duration": 20,
                "is_required": True,
                "prerequisites": []
            },
            {
                "title": "Quiz Équations Basiques",
                "description": "Test sur les équations simples",
                "step_type": "quiz",
                "order": 2,
                "estimated_duration": 15,
                "is_required": True,
                "prerequisites": [1]
            },
            {
                "title": "Équations du Second Degré",
                "description": "Apprendre à résoudre les équations quadratiques",
                "step_type": "content",
                "order": 3,
                "estimated_duration": 25,
                "is_required": True,
                "prerequisites": [1, 2]
            }
        ]
        
        for step_data in math_steps:
            step = LearningPathStep(
                learning_path_id=math_path.id,
                title=step_data["title"],
                description=step_data["description"],
                step_type=step_data["step_type"],
                order=step_data["order"],
                estimated_duration=step_data["estimated_duration"],
                is_required=step_data["is_required"],
                prerequisites=json.dumps(step_data["prerequisites"])
            )
            db.add(step)
        
        db.commit()
        print("✅ Étapes de parcours créées")
        
        # 5. Créer des quiz et résultats
        print("📊 Création des quiz et résultats...")
        
        # Quiz Mathématiques
        math_quiz = Quiz(
            title="Quiz Équations Basiques",
            description="Test sur les équations du premier degré",
            subject="Mathématiques",
            level="intermediate",
            difficulty="medium",
            time_limit=20,
            max_score=100,
            created_by=1
        )
        db.add(math_quiz)
        
        # Quiz Français
        french_quiz = Quiz(
            title="Analyse Littéraire",
            description="Test sur l'analyse de textes",
            subject="Français",
            level="advanced",
            difficulty="advanced",
            time_limit=30,
            max_score=100,
            created_by=1
        )
        db.add(french_quiz)
        
        db.commit()
        
        # Créer des résultats de quiz
        quiz_results = [
            {"student_id": students[0].id, "quiz_id": math_quiz.id, "score": 85, "max_score": 100},
            {"student_id": students[1].id, "quiz_id": math_quiz.id, "score": 72, "max_score": 100},
            {"student_id": students[2].id, "quiz_id": french_quiz.id, "score": 90, "max_score": 100},
            {"student_id": students[3].id, "quiz_id": french_quiz.id, "score": 78, "max_score": 100},
        ]
        
        for result_data in quiz_results:
            result = QuizResult(
                quiz_id=result_data["quiz_id"],
                student_id=result_data["student_id"],
                score=result_data["score"],
                max_score=result_data["max_score"],
                time_taken=15,
                completed=True,
                sujet="Général"
            )
            db.add(result)
        
        db.commit()
        print("✅ Quiz et résultats créés")
        
        # 6. Créer des données de progression
        print("📈 Création des données de progression...")
        
        progress_data = [
            {"student_id": students[0].id, "learning_path_id": math_path.id, "progress_percentage": 75.0},
            {"student_id": students[1].id, "learning_path_id": math_path.id, "progress_percentage": 60.0},
            {"student_id": students[2].id, "learning_path_id": french_path.id, "progress_percentage": 85.0},
            {"student_id": students[3].id, "learning_path_id": french_path.id, "progress_percentage": 45.0},
        ]
        
        for progress_data_item in progress_data:
            progress = StudentProgress(
                student_id=progress_data_item["student_id"],
                learning_path_id=progress_data_item["learning_path_id"],
                progress_percentage=progress_data_item["progress_percentage"],
                completed_steps=json.dumps([1, 2]),
                is_active=True,
                last_activity=datetime.utcnow()
            )
            db.add(progress)
        
        db.commit()
        print("✅ Données de progression créées")
        
        # 7. Créer des analytics
        print("📊 Création des analytics...")
        
        # Analytics pour la classe mathématiques
        math_analytics = ClassAnalytics(
            class_id=math_class.id,
            total_students=2,
            active_students=2,
            average_progress=67.5,
            completed_quizzes=2,
            average_score=78.5,
            weak_subjects=json.dumps(["Géométrie"]),
            strong_subjects=json.dumps(["Algèbre"])
        )
        db.add(math_analytics)
        
        # Analytics pour la classe français
        french_analytics = ClassAnalytics(
            class_id=french_class.id,
            total_students=2,
            active_students=2,
            average_progress=65.0,
            completed_quizzes=2,
            average_score=84.0,
            weak_subjects=json.dumps(["Grammaire"]),
            strong_subjects=json.dumps(["Littérature"])
        )
        db.add(french_analytics)
        
        db.commit()
        print("✅ Analytics créés")
        
        # 8. Créer des activités temps réel
        print("⏰ Création des activités temps réel...")
        
        activities = [
            {
                "student_id": students[0].id,
                "activity_type": "quiz_start",
                "activity_data": json.dumps({"quiz_id": math_quiz.id}),
                "session_id": "session_001"
            },
            {
                "student_id": students[0].id,
                "activity_type": "quiz_complete",
                "activity_data": json.dumps({"quiz_id": math_quiz.id, "score": 85}),
                "session_id": "session_001"
            },
            {
                "student_id": students[2].id,
                "activity_type": "content_view",
                "activity_data": json.dumps({"content_id": 1}),
                "session_id": "session_002"
            }
        ]
        
        for activity_data in activities:
            activity = RealTimeActivity(
                student_id=activity_data["student_id"],
                activity_type=activity_data["activity_type"],
                activity_data=activity_data["activity_data"],
                session_id=activity_data["session_id"]
            )
            db.add(activity)
        
        db.commit()
        print("✅ Activités temps réel créées")
        
        print("\n🎉 DONNÉES RÉELLES CRÉÉES AVEC SUCCÈS!")
        print("=" * 60)
        print(f"📚 Classes créées: 3")
        print(f"👥 Étudiants assignés: 6")
        print(f"📖 Parcours créés: 2")
        print(f"📝 Étapes créées: 3")
        print(f"📊 Quiz créés: 2")
        print(f"📈 Progression: 4 enregistrements")
        print(f"📊 Analytics: 2 classes")
        print(f"⏰ Activités temps réel: 3")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des données: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_real_data() 