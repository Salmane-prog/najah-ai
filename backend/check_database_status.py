#!/usr/bin/env python3
"""
Script pour vérifier l'état actuel de la base de données
et les données réelles pour l'interface enseignant avancée
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import get_db
from models.user import User
from models.class_group import ClassGroup, ClassStudent
from models.learning_path import LearningPath
from models.quiz import QuizResult
from models.advanced_learning import (
    LearningPathStep, StudentProgress, ClassAnalytics, 
    StudentAnalytics, RealTimeActivity
)
from sqlalchemy.orm import Session
from sqlalchemy import func

def check_database_status():
    """Vérifier l'état de la base de données"""
    print("🔍 VÉRIFICATION DE L'ÉTAT DE LA BASE DE DONNÉES")
    print("=" * 60)
    
    db = next(get_db())
    
    try:
        # Vérifier les utilisateurs
        users_count = db.query(User).count()
        teachers = db.query(User).filter(User.role == 'teacher').all()
        students = db.query(User).filter(User.role == 'student').all()
        
        print(f"👥 Utilisateurs totaux: {users_count}")
        print(f"👨‍🏫 Enseignants: {len(teachers)}")
        print(f"👨‍🎓 Étudiants: {len(students)}")
        
        # Vérifier les classes
        classes_count = db.query(ClassGroup).count()
        active_classes = db.query(ClassGroup).filter(ClassGroup.is_active == True).count()
        
        print(f"\n🏫 Classes totales: {classes_count}")
        print(f"✅ Classes actives: {active_classes}")
        
        # Vérifier les parcours
        paths_count = db.query(LearningPath).count()
        adaptive_paths = db.query(LearningPath).filter(LearningPath.is_adaptive == True).count()
        
        print(f"\n📚 Parcours totaux: {paths_count}")
        print(f"🔄 Parcours adaptatifs: {adaptive_paths}")
        
        # Vérifier les étapes de parcours
        steps_count = db.query(LearningPathStep).count()
        print(f"📝 Étapes de parcours: {steps_count}")
        
        # Vérifier les assignations d'étudiants
        student_assignments = db.query(ClassStudent).count()
        print(f"👥 Assignations étudiants: {student_assignments}")
        
        # Vérifier les résultats de quiz
        quiz_results = db.query(QuizResult).count()
        completed_quizzes = db.query(QuizResult).filter(QuizResult.is_completed == True).count()
        
        print(f"\n📊 Résultats de quiz: {quiz_results}")
        print(f"✅ Quiz complétés: {completed_quizzes}")
        
        # Vérifier les nouvelles tables avancées
        progress_count = db.query(StudentProgress).count()
        analytics_count = db.query(ClassAnalytics).count()
        student_analytics_count = db.query(StudentAnalytics).count()
        realtime_count = db.query(RealTimeActivity).count()
        
        print(f"\n📈 Progression étudiants: {progress_count}")
        print(f"📊 Analytics classes: {analytics_count}")
        print(f"📊 Analytics étudiants: {student_analytics_count}")
        print(f"⏰ Activités temps réel: {realtime_count}")
        
        # Afficher quelques exemples de données
        print(f"\n📋 EXEMPLES DE DONNÉES:")
        print("-" * 40)
        
        # Classes avec leurs étudiants
        classes = db.query(ClassGroup).limit(3).all()
        for class_group in classes:
            students = db.query(ClassStudent).filter(ClassStudent.class_id == class_group.id).count()
            print(f"Classe '{class_group.name}': {students} étudiants")
        
        # Parcours avec leurs étapes
        paths = db.query(LearningPath).limit(3).all()
        for path in paths:
            steps = db.query(LearningPathStep).filter(LearningPathStep.learning_path_id == path.id).count()
            print(f"Parcours '{path.name}': {steps} étapes")
        
        # Résultats de quiz récents
        recent_quizzes = db.query(QuizResult).order_by(QuizResult.completed_at.desc()).limit(5).all()
        if recent_quizzes:
            print(f"\n📊 Quiz récents:")
            for quiz in recent_quizzes:
                student = db.query(User).filter(User.id == quiz.student_id).first()
                print(f"  - {student.username if student else 'Unknown'}: {quiz.score}% ({quiz.sujet})")
        
        print(f"\n✅ Vérification terminée!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    check_database_status() 