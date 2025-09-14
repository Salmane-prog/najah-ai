#!/usr/bin/env python3
import sys
import os
sys.path.append('backend')

from backend.database import get_db
from backend.models.user import User
from backend.models.quiz import Quiz
from backend.models.quiz_result import QuizResult
from sqlalchemy import func

def check_database_data():
    try:
        db = next(get_db())
        
        print("=== VÉRIFICATION DES DONNÉES DE LA BASE ===")
        
        # Vérifier les utilisateurs
        total_users = db.query(User).count()
        students = db.query(User).filter(User.role == "student").all()
        teachers = db.query(User).filter(User.role == "teacher").all()
        
        print(f"Total utilisateurs: {total_users}")
        print(f"Étudiants: {len(students)}")
        print(f"Enseignants: {len(teachers)}")
        
        if students:
            print("\nÉtudiants disponibles:")
            for student in students:
                name = f"{student.first_name} {student.last_name}" if student.first_name and student.last_name else student.email
                print(f"  - ID: {student.id}, Nom: {name}")
        
        # Vérifier les quiz
        total_quizzes = db.query(Quiz).count()
        print(f"\nTotal quiz: {total_quizzes}")
        
        if total_quizzes > 0:
            subjects = db.query(Quiz.subject).distinct().all()
            print("Matières disponibles:")
            for subject in subjects:
                if subject[0]:
                    print(f"  - {subject[0]}")
        
        # Vérifier les résultats de quiz
        total_results = db.query(QuizResult).count()
        print(f"\nTotal résultats de quiz: {total_results}")
        
        if total_results > 0:
            avg_score = db.query(func.avg(QuizResult.score)).scalar() or 0
            print(f"Score moyen: {avg_score:.2f}%")
        
        print("\n=== FIN DE LA VÉRIFICATION ===")
        
    except Exception as e:
        print(f"Erreur lors de la vérification: {e}")

if __name__ == "__main__":
    check_database_data() 