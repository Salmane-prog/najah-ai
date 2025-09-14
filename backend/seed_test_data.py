#!/usr/bin/env python3
import sys
import os
sys.path.append('.')

try:
    from database import get_db, engine
    from models.user import User
    from models.quiz import Quiz
    from models.quiz_result import QuizResult
    from models.class_group import ClassGroup
    from sqlalchemy.orm import sessionmaker
    from datetime import datetime, timedelta
    import random
except ImportError as e:
    print(f"Erreur d'import: {e}")
    print("Vérifiez que vous êtes dans le bon répertoire (backend/)")
    sys.exit(1)

def seed_test_data():
    """Ajouter des données de test dans la base de données."""
    try:
        db = next(get_db())
        
        print("=== AJOUT DE DONNÉES DE TEST ===")
        
        # Vérifier si des données existent déjà
        existing_users = db.query(User).count()
        existing_quizzes = db.query(Quiz).count()
        
        if existing_users > 0 and existing_quizzes > 0:
            print("Des données existent déjà. Vérification...")
            return
        
        print("Création des données de test...")
        
        # Créer des étudiants de test
        students_data = [
            {"email": "etudiant1@test.com", "first_name": "Jean", "last_name": "Dupont", "role": "student"},
            {"email": "etudiant2@test.com", "first_name": "Marie", "last_name": "Martin", "role": "student"},
            {"email": "etudiant3@test.com", "first_name": "Pierre", "last_name": "Bernard", "role": "student"},
            {"email": "etudiant4@test.com", "first_name": "Sophie", "last_name": "Petit", "role": "student"},
            {"email": "etudiant5@test.com", "first_name": "Lucas", "last_name": "Robert", "role": "student"},
        ]
        
        students = []
        for student_data in students_data:
            student = User(**student_data)
            db.add(student)
            students.append(student)
        
        # Créer des quiz de test avec différentes matières
        quizzes_data = [
            {"title": "Quiz Mathématiques - Niveau 1", "subject": "Mathématiques", "description": "Quiz de base en mathématiques", "is_active": True},
            {"title": "Quiz Mathématiques - Niveau 2", "subject": "Mathématiques", "description": "Quiz intermédiaire en mathématiques", "is_active": True},
            {"title": "Quiz Français - Grammaire", "subject": "Français", "description": "Quiz de grammaire française", "is_active": True},
            {"title": "Quiz Français - Littérature", "subject": "Français", "description": "Quiz de littérature française", "is_active": True},
            {"title": "Quiz Sciences - Physique", "subject": "Sciences", "description": "Quiz de physique", "is_active": True},
            {"title": "Quiz Sciences - Chimie", "subject": "Sciences", "description": "Quiz de chimie", "is_active": True},
            {"title": "Quiz Histoire - Antiquité", "subject": "Histoire", "description": "Quiz sur l'antiquité", "is_active": True},
            {"title": "Quiz Histoire - Moyen Âge", "subject": "Histoire", "description": "Quiz sur le moyen âge", "is_active": True},
        ]
        
        quizzes = []
        for quiz_data in quizzes_data:
            quiz = Quiz(**quiz_data)
            db.add(quiz)
            quizzes.append(quiz)
        
        # Créer des résultats de quiz de test
        for student in students:
            for quiz in quizzes:
                # Générer un score aléatoire entre 40 et 95
                score = random.randint(40, 95)
                
                result = QuizResult(
                    student_id=student.id,
                    quiz_id=quiz.id,
                    score=score,
                    is_completed=True,
                    created_at=datetime.now() - timedelta(days=random.randint(1, 30))
                )
                db.add(result)
        
        # Créer des classes de test
        classes_data = [
            {"name": "Classe 6ème A", "description": "Classe de 6ème section A"},
            {"name": "Classe 5ème B", "description": "Classe de 5ème section B"},
            {"name": "Classe 4ème C", "description": "Classe de 4ème section C"},
        ]
        
        classes = []
        for class_data in classes_data:
            class_group = ClassGroup(**class_data)
            db.add(class_group)
            classes.append(class_group)
        
        # Commit des changements
        db.commit()
        
        print("✅ Données de test créées avec succès!")
        print(f"  - {len(students)} étudiants créés")
        print(f"  - {len(quizzes)} quiz créés")
        print(f"  - {len(classes)} classes créées")
        print(f"  - {len(students) * len(quizzes)} résultats de quiz créés")
        
        # Afficher les matières disponibles
        subjects = db.query(Quiz.subject).distinct().all()
        print(f"  - Matières disponibles: {[s[0] for s in subjects if s[0]]}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des données de test: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()

if __name__ == "__main__":
    seed_test_data() 