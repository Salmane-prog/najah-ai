#!/usr/bin/env python3
"""
Script de debug pour identifier le problème dans student_analytics
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.user import User, UserRole
from models.learning_history import LearningHistory
from models.quiz import QuizResult
from models.class_group import ClassGroup, ClassStudent

def debug_student_analytics():
    """Debug de l'endpoint student_analytics."""
    db = SessionLocal()
    
    try:
        print("=== DEBUG STUDENT ANALYTICS ===")
        
        # 1. Vérifier les étudiants
        students = db.query(User).filter(User.role == UserRole.student).all()
        print(f"Étudiants trouvés: {len(students)}")
        
        for student in students:
            print(f"  - {student.username} (ID: {student.id})")
        
        # 2. Vérifier l'historique d'apprentissage
        learning_history = db.query(LearningHistory).all()
        print(f"Historique d'apprentissage: {len(learning_history)} entrées")
        
        # 3. Vérifier les résultats de quiz
        quiz_results = db.query(QuizResult).all()
        print(f"Résultats de quiz: {len(quiz_results)} entrées")
        
        # 4. Vérifier les classes
        classes = db.query(ClassGroup).all()
        print(f"Classes: {len(classes)} entrées")
        
        # 5. Vérifier les relations étudiants-classes
        class_students = db.query(ClassStudent).all()
        print(f"Relations étudiants-classes: {len(class_students)} entrées")
        
        # 6. Test avec un étudiant spécifique
        if students:
            student = students[0]
            print(f"\n=== TEST AVEC ÉTUDIANT {student.username} ===")
            
            # Historique de cet étudiant
            student_history = db.query(LearningHistory).filter(
                LearningHistory.student_id == student.id
            ).all()
            print(f"Historique de {student.username}: {len(student_history)} entrées")
            
            # Quiz de cet étudiant
            student_quizzes = db.query(QuizResult).filter(
                QuizResult.student_id == student.id
            ).all()
            print(f"Quiz de {student.username}: {len(student_quizzes)} entrées")
            
            # Classes de cet étudiant
            student_classes = db.query(ClassGroup).join(ClassStudent).filter(
                ClassStudent.student_id == student.id
            ).all()
            print(f"Classes de {student.username}: {len(student_classes)} entrées")
            
    except Exception as e:
        print(f"Erreur: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    debug_student_analytics() 