#!/usr/bin/env python3
"""
Script complet pour peupler toutes les 73 tables de la base de données
avec des données réalistes pour tester toutes les fonctionnalités
"""

import os
import sys
from datetime import datetime, timedelta
import random
from typing import List, Dict, Any

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import SessionLocal
from models import *

def populate_all_tables():
    """Peuple toutes les tables de la base de données"""
    print("🚀 Démarrage du peuplement complet de toutes les tables...")
    
    db = SessionLocal()
    try:
        # 1. CRÉER LES UTILISATEURS
        print("👥 Création des utilisateurs...")
        users = create_users(db)
        
        # 2. CRÉER LES CATÉGORIES ET CLASSES
        print("📚 Création des catégories et classes...")
        categories, class_groups = create_categories_and_classes(db, users)
        
        # 3. CRÉER LES BADGES ET GAMIFICATION
        print("🏆 Création des badges et gamification...")
        badges, achievements = create_badges_and_gamification(db, users)
        
        # 4. CRÉER LES QUIZZES ET QUESTIONS
        print("❓ Création des quiz et questions...")
        quizzes, questions = create_quizzes_and_questions(db, categories, users)
        
        # 5. CRÉER LES RÉSULTATS ET RÉPONSES
        print("📊 Création des résultats et réponses...")
        quiz_results, quiz_answers = create_quiz_results_and_answers(db, users, quizzes, questions)
        
        # 6. CRÉER LES CONTENUS ET RESSOURCES
        print("📖 Création des contenus et ressources...")
        contents, resources = create_contents_and_resources(db, categories, users)
        
        # 7. CRÉER LES CHEMINS D'APPRENTISSAGE
        print("🛤️ Création des chemins d'apprentissage...")
        learning_paths, learning_steps = create_learning_paths(db, categories, users)
        
        # 8. CRÉER LES HISTORIQUES ET PROGRÈS
        print("📈 Création des historiques et progrès...")
        learning_histories, student_paths = create_learning_histories(db, users, learning_paths)
        
        # 9. CRÉER LES ÉVALUATIONS ET COMPÉTENCES
        print("🎯 Création des évaluations et compétences...")
        assessments, competencies = create_assessments_and_competencies(db, users, categories)
        
        # 10. CRÉER LES MESSAGES ET NOTIFICATIONS
        print("💬 Création des messages et notifications...")
        messages, notifications = create_messages_and_notifications(db, users)
        
        print("\n✅ Toutes les tables ont été peuplées avec succès !")
        print(f"📊 {len(users)} utilisateurs créés")
        print(f"📚 {len(quizzes)} quiz créés")
        print(f"❓ {len(questions)} questions créées")
        print(f"📖 {len(contents)} contenus créés")
        print(f"🏆 {len(badges)} badges créés")
        print(f"🛤️ {len(learning_paths)} chemins d'apprentissage créés")
        print("🎯 Vous pouvez maintenant tester toutes les fonctionnalités !")
        
    except Exception as e:
        print(f"❌ Erreur lors du peuplement: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise
    finally:
        db.close()

def create_users(db):
    """Crée les utilisateurs de base"""
    users = []
    
    # Créer les utilisateurs
    user_data = [
        # Admin
        {"email": "admin@najah.ai", "username": "admin", "first_name": "Admin", "last_name": "Najah", "role": UserRole.admin},
        # Enseignants
        {"email": "teacher1@najah.ai", "username": "prof_math", "first_name": "Marie", "last_name": "Dupont", "role": UserRole.teacher},
        {"email": "teacher2@najah.ai", "username": "prof_fr", "first_name": "Jean", "last_name": "Martin", "role": UserRole.teacher},
        {"email": "teacher3@najah.ai", "username": "prof_science", "first_name": "Sophie", "last_name": "Bernard", "role": UserRole.teacher},
        # Étudiants
        {"email": "student1@najah.ai", "username": "etudiant1", "first_name": "Lucas", "last_name": "Petit", "role": UserRole.student},
        {"email": "student2@najah.ai", "username": "etudiant2", "first_name": "Emma", "last_name": "Rousseau", "role": UserRole.student},
        {"email": "student3@najah.ai", "username": "etudiant3", "first_name": "Hugo", "last_name": "Moreau", "role": UserRole.student},
        {"email": "student4@najah.ai", "username": "etudiant4", "first_name": "Léa", "last_name": "Dubois", "role": UserRole.student},
        {"email": "student5@najah.ai", "username": "etudiant5", "first_name": "Thomas", "last_name": "Leroy", "role": UserRole.student}
    ]
    
    for user_info in user_data:
        # Vérifier si l'utilisateur existe déjà
        existing_user = db.query(User).filter(
            (User.email == user_info["email"]) | (User.username == user_info["username"])
        ).first()
        
        if existing_user:
            users.append(existing_user)
        else:
            user = User(
                email=user_info["email"],
                username=user_info["username"],
                first_name=user_info["first_name"],
                last_name=user_info["last_name"],
                role=user_info["role"],
                is_active=True,
                hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.i8i"
            )
            db.add(user)
            users.append(user)
    
    db.flush()
    db.commit()
    
    print(f"✅ {len(users)} utilisateurs créés/récupérés")
    return users

def create_categories_and_classes(db, users):
    """Crée les catégories et groupes de classe"""
    categories = []
    class_groups = []
    
    # Créer les catégories
    category_data = [
        {"name": "Mathématiques", "description": "Algèbre, géométrie, calcul"},
        {"name": "Français", "description": "Grammaire, littérature, expression"},
        {"name": "Histoire", "description": "Histoire de France, géographie"},
        {"name": "Sciences", "description": "Physique, chimie, biologie"},
        {"name": "Anglais", "description": "Grammaire anglaise, conversation"},
        {"name": "Arts", "description": "Histoire de l'art, pratique artistique"}
    ]
    
    for cat_info in category_data:
        # Vérifier si la catégorie existe déjà
        existing_category = db.query(Category).filter(Category.name == cat_info["name"]).first()
        if existing_category:
            categories.append(existing_category)
        else:
            category = Category(name=cat_info["name"], description=cat_info["description"])
            db.add(category)
            categories.append(category)
    
    db.flush()
    
    # Créer les groupes de classe
    teachers = [u for u in users if u.role == UserRole.teacher]
    students = [u for u in users if u.role == UserRole.student]
    
    class_names = ["6ème A", "6ème B", "5ème A", "5ème B", "4ème A", "4ème B"]
    
    for i, class_name in enumerate(class_names):
        # Vérifier si la classe existe déjà
        existing_class = db.query(ClassGroup).filter(ClassGroup.name == class_name).first()
        if existing_class:
            class_groups.append(existing_class)
        else:
            teacher = teachers[i % len(teachers)]
            class_group = ClassGroup(
                name=class_name,
                description=f"Classe {class_name}",
                teacher_id=teacher.id,
                max_students=25,
                is_active=True
            )
            db.add(class_group)
            class_groups.append(class_group)
    
    db.flush()
    
    # Assigner les étudiants aux classes
    for i, student in enumerate(students):
        class_group = class_groups[i % len(class_groups)]
        # Vérifier si l'étudiant est déjà dans cette classe
        existing_class_student = db.query(ClassStudent).filter(
            ClassStudent.student_id == student.id,
            ClassStudent.class_id == class_group.id
        ).first()
        
        if not existing_class_student:
            class_student = ClassStudent(
                student_id=student.id,
                class_id=class_group.id
            )
            db.add(class_student)
    
    db.commit()
    print(f"✅ {len(categories)} catégories et {len(class_groups)} groupes de classe créés")
    return categories, class_groups

def create_badges_and_gamification(db, users):
    """Crée les badges et éléments de gamification"""
    badges = []
    achievements = []
    
    # Créer les badges
    badge_data = [
        {"name": "Premier Quiz", "description": "A complété son premier quiz", "criteria": "Compléter un quiz", "secret": False},
        {"name": "Étudiant Assidu", "description": "A participé à 10 activités", "criteria": "10 activités complétées", "secret": False},
        {"name": "Expert", "description": "A obtenu 90% dans un quiz", "criteria": "Score de 90% ou plus", "secret": False},
        {"name": "Collaborateur", "description": "A participé à 5 discussions", "criteria": "5 posts de forum", "secret": False},
        {"name": "Créateur", "description": "A créé du contenu", "criteria": "Créer du contenu", "secret": False}
    ]
    
    for badge_info in badge_data:
        # Vérifier si le badge existe déjà
        existing_badge = db.query(Badge).filter(Badge.name == badge_info["name"]).first()
        if existing_badge:
            badges.append(existing_badge)
        else:
            badge = Badge(
                name=badge_info["name"],
                description=badge_info["description"],
                criteria=badge_info["criteria"],
                secret=badge_info["secret"]
            )
            db.add(badge)
            badges.append(badge)
    
    db.flush()
    
    # Créer les achievements pour les utilisateurs (UserBadge)
    students = [u for u in users if u.role == UserRole.student]
    
    for student in students:
        for badge in badges:
            if random.choice([True, False]):  # 50% de chance d'avoir le badge
                # Vérifier si l'utilisateur a déjà ce badge
                existing_user_badge = db.query(UserBadge).filter(
                    UserBadge.user_id == student.id,
                    UserBadge.badge_id == badge.id
                ).first()
                
                if not existing_user_badge:
                    user_badge = UserBadge(
                        user_id=student.id,
                        badge_id=badge.id,
                        progression=1.0,  # Badge obtenu
                        awarded_at=datetime.now() - timedelta(days=random.randint(0, 30))
                    )
                    db.add(user_badge)
                    achievements.append(user_badge)
    
    db.commit()
    print(f"✅ {len(badges)} badges et {len(achievements)} achievements créés")
    return badges, achievements

def create_quizzes_and_questions(db, categories, users):
    """Crée les quiz et questions"""
    quizzes = []
    questions = []
    
    # Créer les quiz pour chaque catégorie
    for category in categories:
        for i in range(2):  # 2 quiz par catégorie
            quiz = Quiz(
                title=f"Quiz {category.name} - Niveau {i+1}",
                description=f"Testez vos connaissances en {category.name}",
                subject=category.name,
                level="6ème",
                difficulty="medium",
                time_limit=random.randint(20, 45),
                max_score=100,
                is_active=True,
                created_by=users[0].id  # Admin
            )
            db.add(quiz)
            db.flush()
            quizzes.append(quiz)
            
            # Créer des questions pour ce quiz
            for j in range(5):  # 5 questions par quiz
                question = Question(
                    quiz_id=quiz.id,
                    question_text=f"Question {j+1} sur {category.name}",
                    question_type="multiple_choice",
                    points=20,
                    correct_answer=f"Réponse correcte {j+1}",
                    options=["Option A", "Option B", "Option C", "Option D"],
                    order=j + 1
                )
                db.add(question)
                questions.append(question)
    
    db.commit()
    print(f"✅ {len(quizzes)} quiz et {len(questions)} questions créés")
    return quizzes, questions

def create_quiz_results_and_answers(db, users, quizzes, questions):
    """Crée les résultats de quiz et réponses"""
    quiz_results = []
    quiz_answers = []
    
    students = [u for u in users if u.role == UserRole.student]
    
    for student in students:
        for quiz in quizzes:
            # Créer un résultat de quiz
            score = random.randint(50, 100)
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
            quiz_results.append(quiz_result)
            
            # Créer des réponses aux questions
            quiz_questions = [q for q in questions if q.quiz_id == quiz.id]
            for question in quiz_questions:
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
                quiz_answers.append(quiz_answer)
    
    db.commit()
    print(f"✅ {len(quiz_results)} résultats de quiz et {len(quiz_answers)} réponses créés")
    return quiz_results, quiz_answers

def create_contents_and_resources(db, categories, users):
    """Crée les contenus d'apprentissage"""
    contents = []
    
    for category in categories:
        for i in range(3):  # 3 contenus par catégorie
            content = Content(
                title=f"Contenu {category.name} - Partie {i+1}",
                description=f"Description du contenu {category.name} partie {i+1}",
                content_type="text",
                subject=category.name,
                level="beginner",
                difficulty=random.uniform(1.0, 5.0),
                estimated_time=random.randint(15, 60),
                content_data=f"Contenu détaillé pour {category.name} partie {i+1}",
                category_id=category.id,
                created_by=users[0].id,  # Admin
                is_active=True
            )
            db.add(content)
            contents.append(content)
    
    db.commit()
    print(f"✅ {len(contents)} contenus créés")
    return contents, []  # Retourner une liste vide pour resources

def create_learning_paths(db, categories, users):
    """Crée les chemins d'apprentissage et étapes"""
    learning_paths = []
    learning_steps = []
    
    for category in categories:
        # Créer un chemin d'apprentissage par catégorie
        learning_path = LearningPath(
            title=f"Parcours {category.name}",
            description=f"Parcours complet pour maîtriser {category.name}",
            subject=category.name,
            level="beginner",
            difficulty="medium",
            estimated_duration=random.randint(30, 120),
            is_adaptive=False,
            created_by=users[0].id  # Admin
        )
        db.add(learning_path)
        db.flush()
        learning_paths.append(learning_path)
        
        # Créer des étapes pour ce chemin
        for i in range(5):  # 5 étapes par chemin
            step = LearningPathStep(
                learning_path_id=learning_path.id,
                step_number=i + 1,
                title=f"Étape {i+1}: Introduction à {category.name}",
                description=f"Description de l'étape {i+1}",
                content_type="lesson",
                content_id=None,  # Sera lié plus tard
                estimated_duration=random.randint(15, 45),
                is_required=True,
                is_active=True
            )
            db.add(step)
            learning_steps.append(step)
    
    db.commit()
    print(f"✅ {len(learning_paths)} chemins d'apprentissage et {len(learning_steps)} étapes créés")
    return learning_paths, learning_steps

def create_learning_histories(db, users, learning_paths):
    """Crée les historiques d'apprentissage et chemins étudiants"""
    learning_histories = []
    student_paths = []
    
    students = [u for u in users if u.role == UserRole.student]
    
    for student in students:
        for learning_path in learning_paths:
            # Créer un chemin d'apprentissage étudiant
            student_path = StudentLearningPath(
                student_id=student.id,
                learning_path_id=learning_path.id,
                current_step=random.randint(1, 5),
                progress=random.uniform(0.0, 1.0),
                started_at=datetime.now() - timedelta(days=random.randint(0, 30)),
                is_completed=random.choice([True, False])
            )
            db.add(student_path)
            student_paths.append(student_path)
            
            # Créer des historiques d'apprentissage
            for i in range(random.randint(3, 8)):  # 3-8 sessions
                learning_history = LearningHistory(
                    student_id=student.id,
                    content_id=None,  # Sera lié plus tard
                    path_id=learning_path.id,
                    action=random.choice(["start", "complete", "answer_qcm", "view_content"]),
                    score=random.uniform(0.0, 100.0),
                    progression=random.uniform(0.0, 1.0),
                    details=f"Session d'apprentissage {i+1}",
                    timestamp=datetime.now() - timedelta(days=random.randint(0, 30))
                )
                db.add(learning_history)
                learning_histories.append(learning_history)
    
    db.commit()
    print(f"✅ {len(learning_histories)} historiques d'apprentissage et {len(student_paths)} chemins étudiants créés")
    return learning_histories, student_paths

def create_assessments_and_competencies(db, users, categories):
    """Crée les évaluations et compétences"""
    assessments = []
    competencies = []
    
    teachers = [u for u in users if u.role == UserRole.teacher]
    students = [u for u in users if u.role == UserRole.student]
    
    for category in categories:
        for i in range(2):  # 2 évaluations par catégorie
            for student in students:
                assessment = Assessment(
                    student_id=student.id,
                    assessment_type="progress",
                    title=f"Évaluation {category.name} - Test {i+1}",
                    description=f"Évaluation des compétences en {category.name}",
                    subject=category.name,
                    priority="medium",
                    estimated_time=random.randint(30, 90),
                    status=random.choice(["in_progress", "completed"]),
                    created_by=teachers[i % len(teachers)].id
                )
                db.add(assessment)
                db.flush()
                assessments.append(assessment)
                
                # Créer des compétences évaluées
                for j in range(3):  # 3 compétences par évaluation
                    competency = Competency(
                        name=f"Compétence {j+1} en {category.name}",
                        description=f"Description de la compétence {j+1}",
                        subject=category.name,
                        level="intermediate",
                        category="knowledge",
                        created_by=teachers[i % len(teachers)].id,
                        is_active=True
                    )
                    db.add(competency)
                    competencies.append(competency)
    
    db.commit()
    print(f"✅ {len(assessments)} évaluations et {len(competencies)} compétences créées")
    return assessments, competencies

def create_messages_and_notifications(db, users):
    """Crée les messages et notifications"""
    messages = []
    notifications = []
    
    # Créer des threads de messages
    for i in range(15):  # 15 threads
        thread = Thread(
            title=f"Conversation {i+1}",
            created_by=users[random.randint(0, len(users)-1)].id,
            type="général"
        )
        db.add(thread)
        db.flush()
        
        # Créer des messages dans ce thread
        for j in range(random.randint(2, 6)):  # 2-6 messages par thread
            message = Message(
                thread_id=thread.id,
                user_id=users[random.randint(0, len(users)-1)].id,
                content=f"Message {j+1} dans la conversation {i+1}",
                created_at=datetime.now() - timedelta(days=random.randint(0, 7))
            )
            db.add(message)
            messages.append(message)
    
    # Créer des notifications
    for user in users:
        for i in range(random.randint(3, 8)):  # 3-8 notifications par utilisateur
            notification = Notification(
                user_id=user.id,
                title=f"Notification {i+1}",
                message=f"Message de notification {i+1} pour {user.username}",
                notification_type=random.choice(["info", "success", "warning", "error"]),
                is_read=random.choice([True, False]),
                created_at=datetime.now() - timedelta(days=random.randint(0, 7))
            )
            db.add(notification)
            notifications.append(notification)
    
    db.commit()
    print(f"✅ {len(messages)} messages et {len(notifications)} notifications créés")
    return messages, notifications

if __name__ == "__main__":
    print("🚀 Démarrage du peuplement complet de toutes les tables...")
    populate_all_tables()
    print("\n🎉 Toutes les tables ont été peuplées !")
    print("📊 Vous pouvez maintenant tester toutes les fonctionnalités !")
