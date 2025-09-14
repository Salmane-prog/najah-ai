#!/usr/bin/env python3
"""
Script d'initialisation complet de la base de données
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import Base, engine, SessionLocal
from models.user import User, UserRole
from models.badge import Badge, UserBadge
from models.class_group import ClassGroup
from models.content import Content
from models.learning_path import LearningPath, StudentLearningPath
from models.quiz import Quiz, Question, QuizResult, QuizAnswer
from models.thread import Thread
from models.message import Message
from core.security import get_password_hash
from datetime import datetime
import random

# Créer toutes les tables
Base.metadata.create_all(bind=engine)

def init_complete_database():
    """Initialise la base de données avec toutes les données de test."""
    db = SessionLocal()
    
    try:
        print("🚀 Initialisation complète de la base de données...")
        
        # 1. Créer les badges
        print("🏅 Création des badges...")
        badges = [
            Badge(name="Premier Quiz", description="A complété son premier quiz", image_url="🎯"),
            Badge(name="Excellence", description="Score parfait sur un quiz", image_url="⭐"),
            Badge(name="Persévérant", description="A complété 10 quiz", image_url="💪"),
            Badge(name="Curieux", description="A exploré 5 contenus différents", image_url="🔍"),
            Badge(name="Créatif", description="A créé un contenu original", image_url="🎨")
        ]
        for badge in badges:
            if not db.query(Badge).filter_by(name=badge.name).first():
                db.add(badge)
        db.commit()
        
        # 3. Créer les classes
        print("👥 Création des classes...")
        classes = [
            ClassGroup(name="6ème A", description="Classe de 6ème année A", teacher_id=4),  # teacher1
            ClassGroup(name="6ème B", description="Classe de 6ème année B", teacher_id=4),  # teacher1
            ClassGroup(name="5ème A", description="Classe de 5ème année A", teacher_id=4)   # teacher1
        ]
        for class_group in classes:
            if not db.query(ClassGroup).filter_by(name=class_group.name).first():
                db.add(class_group)
        db.commit()
        
        # 4. Créer les utilisateurs
        print("👤 Création des utilisateurs...")
        users = [
            User(username="student1", email="student1@example.com", hashed_password=get_password_hash("studentpass"), role=UserRole.student),
            User(username="student2", email="student2@example.com", hashed_password=get_password_hash("studentpass"), role=UserRole.student),
            User(username="student3", email="student3@example.com", hashed_password=get_password_hash("studentpass"), role=UserRole.student),
            User(username="teacher1", email="teacher1@example.com", hashed_password=get_password_hash("teacherpass"), role=UserRole.teacher),
            User(username="admin1", email="admin1@example.com", hashed_password=get_password_hash("adminpass"), role=UserRole.admin),
        ]
        for user in users:
            if not db.query(User).filter_by(username=user.username).first():
                db.add(user)
        db.commit()
        
        # 5. Créer les contenus (temporairement désactivé)
        print("📖 Création des contenus... (désactivé)")
        # contents = [
        #     Content(title="Introduction aux fractions", description="Apprendre les bases des fractions", subject="Mathématiques", level="beginner"),
        #     Content(title="La conjugaison du présent", description="Règles de conjugaison au présent", subject="Français", level="beginner"),
        #     Content(title="La Révolution française", description="Événements de la Révolution française", subject="Histoire", level="intermediate"),
        #     Content(title="Les cellules vivantes", description="Structure et fonctionnement des cellules", subject="Sciences", level="intermediate")
        # ]
        # for content in contents:
        #     if not db.query(Content).filter_by(title=content.title).first():
        #         db.add(content)
        # db.commit()
        
        # 7. Créer les parcours d'apprentissage
        print("🛤️ Création des parcours d'apprentissage...")
        learning_paths = [
            LearningPath(name="Parcours Mathématiques", description="Parcours complet en mathématiques"),
            LearningPath(name="Parcours Français", description="Parcours complet en français"),
            LearningPath(name="Parcours Histoire", description="Parcours complet en histoire")
        ]
        for path in learning_paths:
            if not db.query(LearningPath).filter_by(name=path.name).first():
                db.add(path)
        db.commit()
        
        # 8. Créer les quiz
        print("🎯 Création des quiz...")
        quizzes = [
            Quiz(title="Quiz Fractions", description="Test sur les fractions", subject="Mathématiques", level="beginner", time_limit=30),
            Quiz(title="Quiz Conjugaison", description="Test sur la conjugaison", subject="Français", level="beginner", time_limit=25),
            Quiz(title="Quiz Révolution", description="Test sur la Révolution française", subject="Histoire", level="intermediate", time_limit=35),
            Quiz(title="Quiz Cellules", description="Test sur les cellules", subject="Sciences", level="intermediate", time_limit=30)
        ]
        for quiz in quizzes:
            if not db.query(Quiz).filter_by(title=quiz.title).first():
                db.add(quiz)
        db.commit()
        
        # 9. Créer les questions pour chaque quiz
        print("❓ Création des questions...")
        questions_data = [
            # Questions pour le quiz Fractions
            {"quiz_title": "Quiz Fractions", "questions": [
                {"text": "Qu'est-ce qu'une fraction ?", "type": "multiple_choice", "options": ["Une division", "Une multiplication", "Une addition", "Une soustraction"], "correct_answer": "Une division"},
                {"text": "1/2 + 1/2 = ?", "type": "multiple_choice", "options": ["1/4", "1/2", "1", "2"], "correct_answer": "1"},
                {"text": "3/4 est-il plus grand que 1/2 ?", "type": "multiple_choice", "options": ["Oui", "Non", "Égal", "Impossible à dire"], "correct_answer": "Oui"}
            ]},
            # Questions pour le quiz Conjugaison
            {"quiz_title": "Quiz Conjugaison", "questions": [
                {"text": "Je (manger) au présent", "type": "multiple_choice", "options": ["mange", "manges", "mangent", "mangeons"], "correct_answer": "mange"},
                {"text": "Tu (finir) au présent", "type": "multiple_choice", "options": ["finis", "finit", "finissons", "finissez"], "correct_answer": "finis"},
                {"text": "Il (prendre) au présent", "type": "multiple_choice", "options": ["prend", "prends", "prennent", "prenons"], "correct_answer": "prend"}
            ]},
            # Questions pour le quiz Révolution
            {"quiz_title": "Quiz Révolution", "questions": [
                {"text": "En quelle année a eu lieu la prise de la Bastille ?", "type": "multiple_choice", "options": ["1789", "1790", "1788", "1791"], "correct_answer": "1789"},
                {"text": "Qui était le roi de France en 1789 ?", "type": "multiple_choice", "options": ["Louis XIV", "Louis XV", "Louis XVI", "Louis XVII"], "correct_answer": "Louis XVI"},
                {"text": "Qu'est-ce que les États généraux ?", "type": "multiple_choice", "options": ["Une prison", "Une assemblée", "Une armée", "Une école"], "correct_answer": "Une assemblée"}
            ]},
            # Questions pour le quiz Cellules
            {"quiz_title": "Quiz Cellules", "questions": [
                {"text": "Qu'est-ce qu'une cellule ?", "type": "multiple_choice", "options": ["Un organe", "L'unité de base du vivant", "Un tissu", "Un système"], "correct_answer": "L'unité de base du vivant"},
                {"text": "Quel organite produit l'énergie ?", "type": "multiple_choice", "options": ["Le noyau", "La mitochondrie", "Le réticulum", "Le lysosome"], "correct_answer": "La mitochondrie"},
                {"text": "Qu'est-ce que l'ADN ?", "type": "multiple_choice", "options": ["Un sucre", "Un acide nucléique", "Une protéine", "Un lipide"], "correct_answer": "Un acide nucléique"}
            ]}
        ]
        
        for quiz_data in questions_data:
            quiz = db.query(Quiz).filter_by(title=quiz_data["quiz_title"]).first()
            if quiz:
                for q_data in quiz_data["questions"]:
                    question = Question(
                        quiz_id=quiz.id,
                        question_text=q_data["text"],
                        question_type=q_data["type"],
                        options=q_data["options"],
                        correct_answer=q_data["correct_answer"]
                    )
                    db.add(question)
        db.commit()
        
        print("✅ Base de données initialisée avec succès !")
        print("   👤 Utilisateurs créés")
        print("   🏆 Badges et catégories créés")
        print("   👥 Classes créées")
        print("   📚 Contenus créés")
        print("   🛤️ Parcours d'apprentissage créés")
        print("   🎯 Quiz et questions créés")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_complete_database() 