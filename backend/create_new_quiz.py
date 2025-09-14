#!/usr/bin/env python3
"""
Script pour créer un nouveau quiz avec 10 questions
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Imports des modèles dans l'ordre correct pour éviter les dépendances circulaires
from models.class_group import ClassGroup, ClassStudent
from models.badge import Badge, UserBadge
from models.user import User
from models.quiz import Quiz, Question, QuizAssignment
from core.database import SessionLocal
from core.security import get_password_hash

def create_new_quiz():
    db = SessionLocal()
    try:
        # Trouver un professeur pour créer le quiz
        teacher = db.query(User).filter(User.role == "teacher").first()
        if not teacher:
            print("❌ Aucun professeur trouvé")
            return None
        
        print(f"✅ Professeur trouvé: {teacher.email}")
        
        # Créer le nouveau quiz
        new_quiz = Quiz(
            title="Quiz Antigone - 10 Questions",
            description="Quiz sur Antigone avec 10 questions",
            subject="Antigone",
            level="medium",
            created_by=teacher.id,
            time_limit=20,
            total_points=20
        )
        
        db.add(new_quiz)
        db.commit()
        db.refresh(new_quiz)
        
        print(f"✅ Quiz créé: ID {new_quiz.id}")
        
        # Créer 10 questions
        questions_data = [
            {
                "question_text": "Qui est le personnage principal d'Antigone ?",
                "question_type": "mcq",
                "points": 2,
                "options": ["Antigone", "Créon", "Ismène", "Hémon"],
                "correct_answer": 0
            },
            {
                "question_text": "Quel est le conflit principal dans Antigone ?",
                "question_type": "mcq",
                "points": 2,
                "options": ["Amour vs Haine", "Loi divine vs Loi humaine", "Pouvoir vs Liberté", "Vie vs Mort"],
                "correct_answer": 1
            },
            {
                "question_text": "Qui a interdit l'enterrement de Polynice ?",
                "question_type": "mcq",
                "points": 2,
                "options": ["Antigone", "Créon", "Ismène", "Hémon"],
                "correct_answer": 1
            },
            {
                "question_text": "Quelle est la punition d'Antigone ?",
                "question_type": "mcq",
                "points": 2,
                "options": ["Exil", "Mort par lapidation", "Emprisonnement", "Mort par pendaison"],
                "correct_answer": 2
            },
            {
                "question_text": "Qui est le fils de Créon ?",
                "question_type": "mcq",
                "points": 2,
                "options": ["Polynice", "Étéocle", "Hémon", "Thésée"],
                "correct_answer": 2
            },
            {
                "question_text": "Quelle est la relation entre Antigone et Ismène ?",
                "question_type": "mcq",
                "points": 2,
                "options": ["Cousines", "Sœurs", "Mère et fille", "Amiés"],
                "correct_answer": 1
            },
            {
                "question_text": "Quel est le thème principal d'Antigone ?",
                "question_type": "mcq",
                "points": 2,
                "options": ["L'amour", "La justice", "La désobéissance", "La famille"],
                "correct_answer": 2
            },
            {
                "question_text": "Qui meurt en premier dans la pièce ?",
                "question_type": "mcq",
                "points": 2,
                "options": ["Antigone", "Hémon", "Eurydice", "Créon"],
                "correct_answer": 0
            },
            {
                "question_text": "Quel est le rôle de Tirésias dans la pièce ?",
                "question_type": "mcq",
                "points": 2,
                "options": ["Roi", "Prophète", "Garde", "Prêtre"],
                "correct_answer": 1
            },
            {
                "question_text": "Comment se termine la pièce ?",
                "question_type": "mcq",
                "points": 2,
                "options": ["Créon devient roi", "Antigone survit", "Créon se suicide", "Tout le monde meurt"],
                "correct_answer": 2
            }
        ]
        
        for i, q_data in enumerate(questions_data):
            question = Question(
                quiz_id=new_quiz.id,
                question_text=q_data["question_text"],
                question_type=q_data["question_type"],
                points=q_data["points"],
                order=i+1,
                options=q_data["options"],
                correct_answer=q_data["correct_answer"]
            )
            db.add(question)
        
        db.commit()
        
        print(f"✅ 10 questions créées pour le quiz {new_quiz.id}")
        print(f"📊 Quiz '{new_quiz.title}' créé avec succès!")
        print(f"   - ID: {new_quiz.id}")
        print(f"   - Sujet: {new_quiz.subject}")
        print(f"   - Niveau: {new_quiz.level}")
        print(f"   - Temps: {new_quiz.time_limit} min")
        print(f"   - Questions: 10")
        print(f"   - Points totaux: {new_quiz.total_points}")
        
        return new_quiz
        
    except Exception as e:
        print(f"❌ Erreur lors de la création du quiz: {e}")
        db.rollback()
        return None
    finally:
        db.close()

if __name__ == "__main__":
    print("🎯 Création d'un nouveau quiz avec 10 questions...")
    quiz = create_new_quiz()
    if quiz:
        print(f"\n✅ Quiz créé avec succès! ID: {quiz.id}")
        print(f"   Tu peux maintenant l'assigner depuis le dashboard prof.")
    else:
        print(f"\n❌ Échec de la création du quiz.") 