#!/usr/bin/env python3
"""
Script final simplifié pour peupler la base de données avec des données essentielles
Créé pour tester le dashboard étudiant avec les données de base
"""

import os
import sys
from datetime import datetime, timedelta
import random

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import SessionLocal
from models import *

def populate_database_final():
    """Peuple la base de données avec des données essentielles"""
    print("🚀 Démarrage du peuplement final de la base de données...")
    
    db = SessionLocal()
    try:
        # 1. CRÉER LES UTILISATEURS
        print("👥 Création des utilisateurs...")
        users = create_users_final(db)
        
        # 2. CRÉER LES CATÉGORIES
        print("📚 Création des catégories...")
        categories = create_categories_final(db)
        
        # 3. CRÉER LES QUIZZES ET QUESTIONS
        print("❓ Création des quiz et questions...")
        quizzes, questions = create_quizzes_final(db, categories, users)
        
        # 4. CRÉER LES RÉSULTATS DE QUIZ
        print("📊 Création des résultats de quiz...")
        create_quiz_results_final(db, users, quizzes, questions)
        
        # 5. CRÉER LES CONTENUS
        print("📖 Création des contenus...")
        create_contents_final(db, categories, users)
        
        # 6. CRÉER LES NOTIFICATIONS
        print("🔔 Création des notifications...")
        create_notifications_final(db, users)
        
        print("\n✅ Base de données peuplée avec succès !")
        print(f"📊 {len(users)} utilisateurs créés")
        print(f"📚 {len(quizzes)} quiz créés")
        print(f"❓ {len(questions)} questions créées")
        print("🎯 Vous pouvez maintenant tester votre dashboard étudiant !")
        
    except Exception as e:
        print(f"❌ Erreur lors du peuplement: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def create_users_final(db):
    """Crée des utilisateurs de test finaux"""
    users = []
    
    # Admin
    admin = User(
        email="admin@najah.ai",
        username="admin",
        first_name="Admin",
        last_name="Najah",
        role=UserRole.admin,
        is_active=True,
        hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.i8i"
    )
    users.append(admin)
    
    # Enseignants
    teachers = [
        User(email="teacher1@najah.ai", username="prof_math", first_name="Marie", last_name="Dupont", role=UserRole.teacher, is_active=True),
        User(email="teacher2@najah.ai", username="prof_fr", first_name="Jean", last_name="Martin", role=UserRole.teacher, is_active=True)
    ]
    users.extend(teachers)
    
    # Étudiants
    students = [
        User(email="student1@najah.ai", username="etudiant1", first_name="Lucas", last_name="Petit", role=UserRole.student, is_active=True),
        User(email="student2@najah.ai", username="etudiant2", first_name="Emma", last_name="Rousseau", role=UserRole.student, is_active=True),
        User(email="student3@najah.ai", username="etudiant3", first_name="Hugo", last_name="Moreau", role=UserRole.student, is_active=True)
    ]
    users.extend(students)
    
    # Ajouter tous les utilisateurs
    for user in users:
        if not db.query(User).filter(User.email == user.email).first():
            db.add(user)
    
    db.flush()  # Générer les IDs
    db.commit()
    
    # Récupérer les utilisateurs avec leurs IDs
    created_users = []
    for user in users:
        created_user = db.query(User).filter(User.email == user.email).first()
        if created_user:
            created_users.append(created_user)
    
    print(f"✅ {len(created_users)} utilisateurs créés")
    return created_users

def create_categories_final(db):
    """Crée des catégories de contenu finales"""
    categories = [
        Category(name="Mathématiques", description="Algèbre, géométrie, calcul"),
        Category(name="Français", description="Grammaire, littérature, expression"),
        Category(name="Histoire", description="Histoire de France, géographie"),
        Category(name="Sciences", description="Physique, chimie, biologie")
    ]
    
    for category in categories:
        if not db.query(Category).filter(Category.name == category.name).first():
            db.add(category)
    
    db.commit()
    print(f"✅ {len(categories)} catégories créées")
    return categories

def create_quizzes_final(db, categories, users):
    """Crée des quiz et questions finaux"""
    quizzes = []
    questions = []
    
    # Quiz de mathématiques
    math_quiz = Quiz(
        title="Quiz Mathématiques - Niveau 1",
        description="Testez vos connaissances en mathématiques",
        subject="Mathématiques",
        level="6ème",
        difficulty="medium",
        time_limit=30,
        max_score=100,
        is_active=True,
        created_by=users[0].id  # Admin
    )
    db.add(math_quiz)
    db.flush()
    quizzes.append(math_quiz)
    
    # Questions pour le quiz de math
    math_questions = [
        Question(
            quiz_id=math_quiz.id,
            question_text="Quel est le résultat de 15 + 27 ?",
            question_type="multiple_choice",
            points=10,
            correct_answer="42"
        ),
        Question(
            quiz_id=math_quiz.id,
            question_text="Quelle est la racine carrée de 64 ?",
            question_type="multiple_choice",
            points=10,
            correct_answer="8"
        ),
        Question(
            quiz_id=math_quiz.id,
            question_text="Combien font 7 x 8 ?",
            question_type="multiple_choice",
            points=10,
            correct_answer="56"
        )
    ]
    
    for q in math_questions:
        db.add(q)
        questions.append(q)
    
    # Quiz de français
    fr_quiz = Quiz(
        title="Quiz Français - Grammaire",
        description="Testez votre grammaire française",
        subject="Français",
        level="6ème",
        difficulty="medium",
        time_limit=25,
        max_score=100,
        is_active=True,
        created_by=users[0].id  # Admin
    )
    db.add(fr_quiz)
    db.flush()
    quizzes.append(fr_quiz)
    
    # Questions pour le quiz de français
    fr_questions = [
        Question(
            quiz_id=fr_quiz.id,
            question_text="Quel est le pluriel de 'cheval' ?",
            question_type="multiple_choice",
            points=10,
            correct_answer="chevaux"
        ),
        Question(
            quiz_id=fr_quiz.id,
            question_text="Conjuguez 'être' à la 3ème personne du singulier au présent",
            question_type="multiple_choice",
            points=10,
            correct_answer="est"
        )
    ]
    
    for q in fr_questions:
        db.add(q)
        questions.append(q)
    
    db.commit()
    print(f"✅ {len(quizzes)} quiz créés avec {len(questions)} questions")
    return quizzes, questions

def create_quiz_results_final(db, users, quizzes, questions):
    """Crée des résultats de quiz finaux pour les étudiants"""
    students = [u for u in users if u.role == UserRole.student]
    
    for student in students:
        for quiz in quizzes:
            # Créer un résultat de quiz
            score = random.randint(60, 100)
            completed = random.choice([True, False])
            
            quiz_result = QuizResult(
                user_id=student.id,
                student_id=student.id,
                quiz_id=quiz.id,
                score=score,
                max_score=100,
                percentage=score,
                is_completed=completed,
                completed_at=datetime.now() - timedelta(days=random.randint(0, 29)) if completed else None
            )
            db.add(quiz_result)
            db.flush()
            
            # Créer des réponses aux questions
            for question in questions:
                if question.quiz_id == quiz.id:
                    is_correct = random.choice([True, False])
                    answer = question.correct_answer if is_correct else "Réponse incorrecte"
                    
                    quiz_answer = QuizAnswer(
                        result_id=quiz_result.id,
                        question_id=question.id,
                        answer_text=answer,
                        is_correct=is_correct,
                        points_earned=question.points if is_correct else 0
                    )
                    db.add(quiz_answer)
    
    db.commit()
    print("✅ Résultats de quiz créés")

def create_contents_final(db, categories, users):
    """Crée des contenus d'apprentissage finaux"""
    for category in categories:
        for i in range(2):  # 2 contenus par catégorie
            content = Content(
                title=f"Contenu {category.name} - Partie {i+1}",
                description=f"Description du contenu {category.name} partie {i+1}",
                content_type="text",
                subject=category.name,
                level="beginner",
                difficulty=random.uniform(1.0, 5.0),
                estimated_time=random.randint(15, 45),
                content_data=f"Contenu détaillé pour {category.name} partie {i+1}",
                category_id=category.id,
                created_by=users[0].id,  # Admin
                is_active=True
            )
            db.add(content)
    
    db.commit()
    print("✅ Contenus créés")

def create_notifications_final(db, users):
    """Crée des notifications finales"""
    for user in users:
        for i in range(random.randint(2, 4)):
            notification = Notification(
                user_id=user.id,
                title=f"Notification {i+1}",
                message=f"Message de notification {i+1} pour {user.username}",
                notification_type=random.choice(["info", "success", "warning"]),
                is_read=random.choice([True, False]),
                created_at=datetime.now() - timedelta(days=random.randint(0, 7))
            )
            db.add(notification)
    
    db.commit()
    print("✅ Notifications créées")

if __name__ == "__main__":
    print("🚀 Démarrage du peuplement final de la base de données...")
    populate_database_final()
    print("\n🎉 Base de données finale peuplée !")
    print("📊 Vous pouvez maintenant tester votre dashboard étudiant !")

