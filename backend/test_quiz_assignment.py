#!/usr/bin/env python3
"""
Script de test pour vérifier le flux d'assignation de quiz
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Imports des modèles dans l'ordre correct pour éviter les dépendances circulaires
from core.database import SessionLocal
from models.badge import Badge, UserBadge
from models.user import User, UserRole
from models.quiz import Quiz, Question, QuizAssignment
from models.class_group import ClassGroup, ClassStudent
from core.security import get_password_hash
import json

def test_quiz_assignment_flow():
    db = SessionLocal()
    try:
        print("🧪 Test du flux d'assignation de quiz...")
        
        # 1. Vérifier/créer un professeur
        teacher = db.query(User).filter(User.email == "prof@najah.ai").first()
        if not teacher:
            teacher = User(
                username="professeur",
                email="prof@najah.ai",
                hashed_password=get_password_hash("prof123"),
                role=UserRole.teacher
            )
            db.add(teacher)
            db.commit()
            db.refresh(teacher)
            print("✅ Professeur créé")
        else:
            print("✅ Professeur existant trouvé")
        
        # 2. Vérifier/créer un étudiant
        student = db.query(User).filter(User.email == "hajowjis47@gmail.com").first()
        if not student:
            student = User(
                username="etudiant_test",
                email="hajowjis47@gmail.com",
                hashed_password=get_password_hash("test123"),
                role=UserRole.student
            )
            db.add(student)
            db.commit()
            db.refresh(student)
            print("✅ Étudiant créé")
        else:
            print("✅ Étudiant existant trouvé")
        
        # 3. Vérifier/créer une classe
        class_group = db.query(ClassGroup).filter(ClassGroup.name == "Classe Test").first()
        if not class_group:
            class_group = ClassGroup(
                name="Classe Test",
                description="Classe pour les tests",
                teacher_id=teacher.id
            )
            db.add(class_group)
            db.commit()
            db.refresh(class_group)
            print("✅ Classe créée")
        else:
            print("✅ Classe existante trouvée")
        
        # 4. Ajouter l'étudiant à la classe
        class_student = db.query(ClassStudent).filter(
            ClassStudent.class_id == class_group.id,
            ClassStudent.student_id == student.id
        ).first()
        if not class_student:
            class_student = ClassStudent(
                class_id=class_group.id,
                student_id=student.id
            )
            db.add(class_student)
            db.commit()
            print("✅ Étudiant ajouté à la classe")
        else:
            print("✅ Étudiant déjà dans la classe")
        
        # 5. Vérifier/créer un quiz
        quiz = db.query(Quiz).filter(Quiz.title == "Quiz Test Assignation").first()
        if not quiz:
            quiz = Quiz(
                title="Quiz Test Assignation",
                description="Quiz pour tester l'assignation",
                subject="Test",
                level="medium",
                created_by=teacher.id,
                time_limit=15,
                total_points=10
            )
            db.add(quiz)
            db.commit()
            db.refresh(quiz)
            
            # Ajouter des questions
            questions_data = [
                {
                    "question_text": "Quelle est la capitale de la France ?",
                    "question_type": "mcq",
                    "points": 5,
                    "options": ["Paris", "Londres", "Berlin", "Madrid"],
                    "correct_answer": 0
                },
                {
                    "question_text": "2 + 2 = ?",
                    "question_type": "mcq",
                    "points": 5,
                    "options": ["3", "4", "5", "6"],
                    "correct_answer": 1
                }
            ]
            
            for q_data in questions_data:
                question = Question(
                    quiz_id=quiz.id,
                    question_text=q_data["question_text"],
                    question_type=q_data["question_type"],
                    points=q_data["points"],
                    options=q_data["options"],
                    correct_answer=q_data["correct_answer"]
                )
                db.add(question)
            
            db.commit()
            print("✅ Quiz créé avec questions")
        else:
            print("✅ Quiz existant trouvé")
        
        # 6. Assigner le quiz à l'étudiant
        assignment = db.query(QuizAssignment).filter(
            QuizAssignment.quiz_id == quiz.id,
            QuizAssignment.student_id == student.id
        ).first()
        
        if not assignment:
            assignment = QuizAssignment(
                quiz_id=quiz.id,
                student_id=student.id,
                class_id=class_group.id
            )
            db.add(assignment)
            db.commit()
            db.refresh(assignment)
            print("✅ Quiz assigné à l'étudiant")
        else:
            print("✅ Quiz déjà assigné")
        
        # 7. Vérifier que l'étudiant peut voir le quiz assigné
        student_assignments = db.query(QuizAssignment).filter(
            QuizAssignment.student_id == student.id
        ).all()
        
        print(f"\n📊 Résultats du test:")
        print(f"   - Professeur: {teacher.email} (ID: {teacher.id})")
        print(f"   - Étudiant: {student.email} (ID: {student.id})")
        print(f"   - Classe: {class_group.name} (ID: {class_group.id})")
        print(f"   - Quiz: {quiz.title} (ID: {quiz.id})")
        print(f"   - Questions dans le quiz: {len(quiz.questions)}")
        print(f"   - Assignations pour l'étudiant: {len(student_assignments)}")
        
        for assignment in student_assignments:
            print(f"     * Quiz ID {assignment.quiz_id} assigné le {assignment.assigned_at}")
        
        # 8. Test de l'endpoint /assigned/
        print(f"\n🔗 Test de l'endpoint /assigned/ pour l'étudiant {student.id}:")
        print(f"   GET /api/v1/quizzes/assigned/?student_id={student.id}")
        print(f"   Headers: Authorization: Bearer <token_etudiant>")
        
        return {
            "teacher_id": teacher.id,
            "student_id": student.id,
            "class_id": class_group.id,
            "quiz_id": quiz.id,
            "assignment_id": assignment.id,
            "success": True
        }
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        db.rollback()
        return {"success": False, "error": str(e)}
    finally:
        db.close()

if __name__ == "__main__":
    result = test_quiz_assignment_flow()
    if result["success"]:
        print(f"\n✅ Test réussi! Toutes les données sont en place.")
        print(f"   Tu peux maintenant tester l'assignation avec:")
        print(f"   - Prof: prof@najah.ai / prof123")
        print(f"   - Étudiant: hajowjis47@gmail.com / test123")
    else:
        print(f"\n❌ Test échoué: {result.get('error', 'Erreur inconnue')}") 