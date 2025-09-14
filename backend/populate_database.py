#!/usr/bin/env python3
"""
Script pour peupler la base de données avec des données complètes
Créé pour tester le dashboard étudiant avec des données réalistes
"""

import os
import sys
from datetime import datetime, timedelta
import random

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import SessionLocal
from models import *

def populate_database():
    """Peuple toutes les tables avec des données complètes"""
    print("🚀 Démarrage du peuplement de la base de données...")
    
    db = SessionLocal()
    try:
        # 1. CRÉER LES UTILISATEURS
        print("👥 Création des utilisateurs...")
        users = create_users(db)
        
        # 2. CRÉER LES CATÉGORIES
        print("📚 Création des catégories...")
        categories = create_categories(db)
        
        # 3. CRÉER LES GROUPES DE CLASSE
        print("🏫 Création des groupes de classe...")
        class_groups = create_class_groups(db, users)
        
        # 4. CRÉER LES BADGES
        print("🏆 Création des badges...")
        badges = create_badges(db)
        
        # 5. CRÉER LES QUIZZES ET QUESTIONS
        print("❓ Création des quiz et questions...")
        quizzes, questions = create_quizzes_and_questions(db, categories)
        
        # 6. CRÉER LES RÉSULTATS DE QUIZ
        print("📊 Création des résultats de quiz...")
        create_quiz_results(db, users, quizzes, questions)
        
        # 7. CRÉER LES CONTENUS
        print("📖 Création des contenus...")
        contents = create_contents(db, categories)
        
        # 8. CRÉER LES CHEMINS D'APPRENTISSAGE
        print("🛤️ Création des chemins d'apprentissage...")
        learning_paths = create_learning_paths(db, categories)
        
        # 9. CRÉER LES HISTORIQUES D'APPRENTISSAGE
        print("📈 Création des historiques d'apprentissage...")
        create_learning_histories(db, users, contents, learning_paths)
        
        # 10. CRÉER LES NOTIFICATIONS
        print("🔔 Création des notifications...")
        create_notifications(db, users)
        
        # 11. CRÉER LES MESSAGES ET THREADS
        print("💬 Création des messages et threads...")
        create_messages_and_threads(db, users)
        
        # 12. CRÉER LES ÉVALUATIONS
        print("📝 Création des évaluations...")
        create_assessments(db, users, categories)
        
        # 13. CRÉER LES COMPÉTENCES
        print("🎯 Création des compétences...")
        create_competencies(db, users)
        
        # 14. CRÉER LES ACTIVITÉS AVANCÉES
        print("🚀 Création des activités avancées...")
        create_advanced_activities(db, users)
        
        # 15. CRÉER LES ÉVÉNEMENTS DE CALENDRIER
        print("📅 Création des événements de calendrier...")
        create_calendar_events(db, users)
        
        # 16. CRÉER LES ANALYTICS
        print("📊 Création des analytics...")
        create_analytics(db, users)
        
        # 17. CRÉER LES RECOMMANDATIONS IA
        print("🤖 Création des recommandations IA...")
        create_ai_recommendations(db, users, contents)
        
        # 18. CRÉER LES CORRECTIONS DE SCORE
        print("✏️ Création des corrections de score...")
        create_score_corrections(db, users, quizzes)
        
        # 19. CRÉER LES RAPPORTS
        print("📋 Création des rapports...")
        create_reports(db, users)
        
        # 20. CRÉER LES ACTIVITÉS EN TEMPS RÉEL
        print("⚡ Création des activités en temps réel...")
        create_real_time_activities(db, users)
        
        print("\n✅ Base de données peuplée avec succès !")
        print(f"📊 {len(users)} utilisateurs créés")
        print(f"📚 {len(quizzes)} quiz créés")
        print(f"❓ {len(questions)} questions créées")
        print(f"🏆 {len(badges)} badges créés")
        print(f"📖 {len(contents)} contenus créés")
        
    except Exception as e:
        print(f"❌ Erreur lors du peuplement: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def create_users(db):
    """Crée des utilisateurs de test"""
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
        User(email="teacher2@najah.ai", username="prof_fr", first_name="Jean", last_name="Martin", role=UserRole.teacher, is_active=True),
        User(email="teacher3@najah.ai", username="prof_hist", first_name="Sophie", last_name="Bernard", role=UserRole.teacher, is_active=True)
    ]
    users.extend(teachers)
    
    # Étudiants
    students = [
        User(email="student1@najah.ai", username="etudiant1", first_name="Lucas", last_name="Petit", role=UserRole.student, is_active=True),
        User(email="student2@najah.ai", username="etudiant2", first_name="Emma", last_name="Rousseau", role=UserRole.student, is_active=True),
        User(email="student3@najah.ai", username="etudiant3", first_name="Hugo", last_name="Moreau", role=UserRole.student, is_active=True),
        User(email="student4@najah.ai", username="etudiant4", first_name="Léa", last_name="Simon", role=UserRole.student, is_active=True),
        User(email="student5@najah.ai", username="etudiant5", first_name="Nathan", last_name="Michel", role=UserRole.student, is_active=True)
    ]
    users.extend(students)
    
    # Ajouter tous les utilisateurs
    for user in users:
        if not db.query(User).filter(User.email == user.email).first():
            db.add(user)
    
    db.commit()
    print(f"✅ {len(users)} utilisateurs créés")
    return users

def create_categories(db):
    """Crée des catégories de contenu"""
    categories = [
        Category(name="Mathématiques", description="Algèbre, géométrie, calcul"),
        Category(name="Français", description="Grammaire, littérature, expression"),
        Category(name="Histoire", description="Histoire de France, géographie"),
        Category(name="Sciences", description="Physique, chimie, biologie"),
        Category(name="Langues", description="Anglais, espagnol, allemand"),
        Category(name="Informatique", description="Programmation, algorithmes"),
        Category(name="Arts", description="Musique, peinture, cinéma"),
        Category(name="Sport", description="Éducation physique, santé")
    ]
    
    for category in categories:
        if not db.query(Category).filter(Category.name == category.name).first():
            db.add(category)
    
    db.commit()
    print(f"✅ {len(categories)} catégories créées")
    return categories

def create_class_groups(db, users):
    """Crée des groupes de classe"""
    teachers = [u for u in users if u.role == UserRole.teacher]
    students = [u for u in users if u.role == UserRole.student]
    
    class_groups = [
        ClassGroup(name="6ème A", description="Classe de 6ème année", teacher_id=teachers[0].id),
        ClassGroup(name="5ème B", description="Classe de 5ème année", teacher_id=teachers[1].id),
        ClassGroup(name="4ème C", description="Classe de 4ème année", teacher_id=teachers[2].id)
    ]
    
    for group in class_groups:
        if not db.query(ClassGroup).filter(ClassGroup.name == group.name).first():
            db.add(group)
    
    db.flush()  # Générer les IDs
    
    # Ajouter des étudiants aux groupes
    for i, student in enumerate(students):
        group = class_groups[i % len(class_groups)]
        class_student = ClassStudent(
            student_id=student.id,
            class_id=group.id
        )
        db.add(class_student)
    
    db.commit()
    print(f"✅ {len(class_groups)} groupes de classe créés")
    return class_groups

def create_badges(db):
    """Crée des badges de récompense"""
    badges = [
        Badge(name="Premier Quiz", description="A réussi son premier quiz", icon="🎯"),
        Badge(name="Étudiant Assidu", description="A complété 10 quiz", icon="📚"),
        Badge(name="Expert", description="Score moyen > 90%", icon="🏆"),
        Badge(name="Participatif", description="A participé à 5 discussions", icon="💬"),
        Badge(name="Créatif", description="A créé du contenu", icon="✨"),
        Badge(name="Mentor", description="A aidé d'autres étudiants", icon="🤝"),
        Badge(name="Régulier", description="Connexion quotidienne", icon="📅"),
        Badge(name="Innovateur", description="A proposé des améliorations", icon="💡")
    ]
    
    for badge in badges:
        if not db.query(Badge).filter(Badge.name == badge.name).first():
            db.add(badge)
    
    db.commit()
    print(f"✅ {len(badges)} badges créés")
    return badges

def create_quizzes_and_questions(db, categories):
    """Crée des quiz et questions"""
    quizzes = []
    questions = []
    
    # Quiz de mathématiques
    math_quiz = Quiz(
        title="Quiz Mathématiques - Niveau 1",
        description="Testez vos connaissances en mathématiques",
        category_id=categories[0].id,
        time_limit=30,
        passing_score=70,
        is_active=True
    )
    db.add(math_quiz)
    db.flush()
    quizzes.append(math_quiz)
    
    # Questions pour le quiz de math
    math_questions = [
        Question(
            quiz_id=math_quiz.id,
            text="Quel est le résultat de 15 + 27 ?",
            question_type="multiple_choice",
            points=10,
            correct_answer="42"
        ),
        Question(
            quiz_id=math_quiz.id,
            text="Quelle est la racine carrée de 64 ?",
            question_type="multiple_choice",
            points=10,
            correct_answer="8"
        ),
        Question(
            quiz_id=math_quiz.id,
            text="Combien font 7 x 8 ?",
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
        category_id=categories[1].id,
        time_limit=25,
        passing_score=75,
        is_active=True
    )
    db.add(fr_quiz)
    db.flush()
    quizzes.append(fr_quiz)
    
    # Questions pour le quiz de français
    fr_questions = [
        Question(
            quiz_id=fr_quiz.id,
            text="Quel est le pluriel de 'cheval' ?",
            question_type="multiple_choice",
            points=10,
            correct_answer="chevaux"
        ),
        Question(
            quiz_id=fr_quiz.id,
            text="Conjuguez 'être' à la 3ème personne du singulier au présent",
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

def create_quiz_results(db, users, quizzes, questions):
    """Crée des résultats de quiz pour les étudiants"""
    students = [u for u in users if u.role == UserRole.student]
    
    for student in students:
        for quiz in quizzes:
            # Créer un résultat de quiz
            score = random.randint(60, 100)
            completed = random.choice([True, False])
            
            quiz_result = QuizResult(
                student_id=student.id,
                quiz_id=quiz.id,
                score=score,
                completed=completed,
                started_at=datetime.now() - timedelta(days=random.randint(1, 30)),
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
                        quiz_result_id=quiz_result.id,
                        question_id=question.id,
                        student_answer=answer,
                        is_correct=is_correct,
                        points_earned=question.points if is_correct else 0
                    )
                    db.add(quiz_answer)
    
    db.commit()
    print("✅ Résultats de quiz créés")

def create_contents(db, categories):
    """Crée des contenus d'apprentissage"""
    contents = []
    
    for category in categories:
        for i in range(3):  # 3 contenus par catégorie
            content = Content(
                title=f"Contenu {category.name} - Partie {i+1}",
                description=f"Description du contenu {category.name} partie {i+1}",
                content_type="text",
                content_data=f"Contenu détaillé pour {category.name} partie {i+1}",
                category_id=category.id,
                difficulty_level=random.randint(1, 5),
                is_active=True
            )
            db.add(content)
            contents.append(content)
    
    db.commit()
    print(f"✅ {len(contents)} contenus créés")
    return contents

def create_learning_paths(db, categories):
    """Crée des chemins d'apprentissage"""
    learning_paths = []
    
    for category in categories:
        path = LearningPath(
            title=f"Parcours {category.name}",
            description=f"Parcours complet pour maîtriser {category.name}",
            category_id=category.id,
            difficulty_level=random.randint(1, 5),
            estimated_duration=random.randint(30, 120),
            is_active=True
        )
        db.add(path)
        learning_paths.append(path)
    
    db.commit()
    print(f"✅ {len(learning_paths)} chemins d'apprentissage créés")
    return learning_paths

def create_learning_histories(db, users, contents, learning_paths):
    """Crée des historiques d'apprentissage"""
    students = [u for u in users if u.role == UserRole.student]
    
    for student in students:
        for content in random.sample(contents, random.randint(3, 8)):
            history = LearningHistory(
                student_id=student.id,
                content_id=content.id,
                learning_path_id=random.choice(learning_paths).id,
                time_spent=random.randint(10, 60),
                progress_percentage=random.randint(20, 100),
                completed=random.choice([True, False]),
                started_at=datetime.now() - timedelta(days=random.randint(1, 30)),
                completed_at=datetime.now() - timedelta(days=random.randint(0, 29)) if random.choice([True, False]) else None
            )
            db.add(history)
    
    db.commit()
    print("✅ Historiques d'apprentissage créés")

def create_notifications(db, users):
    """Crée des notifications"""
    for user in users:
        for i in range(random.randint(2, 5)):
            notification = Notification(
                user_id=user.id,
                title=f"Notification {i+1}",
                message=f"Message de notification {i+1} pour {user.username}",
                notification_type=random.choice(["info", "success", "warning", "error"]),
                is_read=random.choice([True, False]),
                created_at=datetime.now() - timedelta(days=random.randint(0, 7))
            )
            db.add(notification)
    
    db.commit()
    print("✅ Notifications créées")

def create_messages_and_threads(db, users):
    """Crée des messages et threads de discussion"""
    students = [u for u in users if u.role == UserRole.student]
    teachers = [u for u in users if u.role == UserRole.teacher]
    
    # Créer des threads
    threads = []
    for i in range(5):
        thread = Thread(
            title=f"Discussion {i+1}",
            content=f"Contenu de la discussion {i+1}",
            author_id=random.choice(students + teachers).id,
            category_id=random.randint(1, 8),
            is_active=True
        )
        db.add(thread)
        threads.append(thread)
    
    db.flush()
    
    # Créer des messages dans les threads
    for thread in threads:
        for i in range(random.randint(3, 8)):
            message = Message(
                thread_id=thread.id,
                author_id=random.choice(students + teachers).id,
                content=f"Message {i+1} dans le thread {thread.title}",
                created_at=datetime.now() - timedelta(days=random.randint(0, 5))
            )
            db.add(message)
    
    db.commit()
    print("✅ Messages et threads créés")

def create_assessments(db, users, categories):
    """Crée des évaluations"""
    students = [u for u in users if u.role == UserRole.student]
    
    for category in categories:
        assessment = Assessment(
            title=f"Évaluation {category.name}",
            description=f"Évaluation complète pour {category.name}",
            category_id=category.id,
            total_points=100,
            passing_score=70,
            time_limit=60,
            is_active=True
        )
        db.add(assessment)
        db.flush()
        
        # Créer des questions d'évaluation
        for i in range(5):
            question = AssessmentQuestion(
                assessment_id=assessment.id,
                question_text=f"Question {i+1} de l'évaluation {category.name}",
                question_type="multiple_choice",
                points=20,
                correct_answer=f"Réponse {i+1}"
            )
            db.add(question)
        
        # Créer des résultats d'évaluation
        for student in random.sample(students, random.randint(2, len(students))):
            result = AssessmentResult(
                student_id=student.id,
                assessment_id=assessment.id,
                score=random.randint(50, 100),
                completed=random.choice([True, False]),
                started_at=datetime.now() - timedelta(days=random.randint(1, 20)),
                completed_at=datetime.now() - timedelta(days=random.randint(0, 19)) if random.choice([True, False]) else None
            )
            db.add(result)
    
    db.commit()
    print("✅ Évaluations créées")

def create_competencies(db, users):
    """Crée des compétences pour les étudiants"""
    students = [u for u in users if u.role == UserRole.student]
    
    competency_names = [
        "Résolution de problèmes", "Communication", "Travail en équipe",
        "Pensée critique", "Créativité", "Adaptabilité", "Leadership"
    ]
    
    for student in students:
        for competency_name in random.sample(competency_names, random.randint(3, 6)):
            competency = StudentCompetency(
                student_id=student.id,
                competency_name=competency_name,
                level=random.randint(1, 5),
                progress_percentage=random.randint(20, 100),
                last_updated=datetime.now() - timedelta(days=random.randint(1, 30))
            )
            db.add(competency)
    
    db.commit()
    print("✅ Compétences créées")

def create_advanced_activities(db, users):
    """Crée des activités avancées"""
    students = [u for u in users if u.role == UserRole.student]
    
    for student in students:
        # Apprentissages avancés
        advanced_learning = AdvancedLearning(
            student_id=student.id,
            learning_type="project_based",
            title=f"Projet avancé pour {student.username}",
            description="Projet d'apprentissage avancé",
            difficulty_level=random.randint(3, 5),
            estimated_duration=random.randint(60, 180),
            is_active=True
        )
        db.add(advanced_learning)
        
        # Notifications avancées
        advanced_notification = AdvancedNotification(
            user_id=student.id,
            title="Notification avancée",
            message="Notification avancée personnalisée",
            notification_type="advanced",
            priority=random.randint(1, 5),
            is_read=False
        )
        db.add(advanced_notification)
    
    db.commit()
    print("✅ Activités avancées créées")

def create_calendar_events(db, users):
    """Crée des événements de calendrier"""
    students = [u for u in users if u.role == UserRole.student]
    
    event_types = ["study_session", "quiz", "deadline", "meeting", "reminder"]
    
    for student in students:
        for i in range(random.randint(3, 8)):
            event_date = datetime.now() + timedelta(days=random.randint(-7, 30))
            event = CalendarEvent(
                user_id=student.id,
                title=f"Événement {i+1}",
                description=f"Description de l'événement {i+1}",
                event_type=random.choice(event_types),
                start_time=event_date,
                end_time=event_date + timedelta(hours=random.randint(1, 3)),
                is_all_day=False,
                location="Salle virtuelle",
                is_active=True
            )
            db.add(event)
    
    db.commit()
    print("✅ Événements de calendrier créés")

def create_analytics(db, users):
    """Crée des données d'analytics"""
    students = [u for u in users if u.role == UserRole.student]
    
    for student in students:
        analytics = StudentAnalytics(
            student_id=student.id,
            total_study_time=random.randint(100, 500),
            total_quizzes_taken=random.randint(5, 20),
            average_score=random.uniform(60.0, 95.0),
            total_contents_completed=random.randint(10, 30),
            learning_streak=random.randint(1, 15),
            last_activity=datetime.now() - timedelta(days=random.randint(0, 3))
        )
        db.add(analytics)
        
        # Activités utilisateur
        for i in range(random.randint(5, 15)):
            activity = UserActivity(
                user_id=student.id,
                activity_type=random.choice(["login", "quiz", "content", "message"]),
                description=f"Activité {i+1}",
                timestamp=datetime.now() - timedelta(hours=random.randint(1, 48))
            )
            db.add(activity)
    
    db.commit()
    print("✅ Analytics créés")

def create_ai_recommendations(db, users, contents):
    """Crée des recommandations IA"""
    students = [u for u in users if u.role == UserRole.student]
    
    for student in students:
        for i in range(random.randint(2, 5)):
            recommendation = AIRecommendation(
                student_id=student.id,
                content_id=random.choice(contents).id,
                recommendation_type=random.choice(["content", "quiz", "path"]),
                confidence_score=random.uniform(0.7, 1.0),
                reason="Basé sur l'historique d'apprentissage",
                is_implemented=random.choice([True, False]),
                created_at=datetime.now() - timedelta(days=random.randint(1, 7))
            )
            db.add(recommendation)
    
    db.commit()
    print("✅ Recommandations IA créées")

def create_score_corrections(db, users, quizzes):
    """Crée des corrections de score"""
    students = [u for u in users if u.role == UserRole.student]
    
    for student in students:
        for quiz in random.sample(quizzes, random.randint(1, 3)):
            correction = ScoreCorrection(
                student_id=student.id,
                quiz_id=quiz.id,
                original_score=random.randint(50, 80),
                corrected_score=random.randint(80, 100),
                correction_reason="Révision de la notation",
                corrected_by_id=random.choice([u for u in users if u.role == UserRole.teacher]).id,
                correction_date=datetime.now() - timedelta(days=random.randint(1, 10))
            )
            db.add(correction)
    
    db.commit()
    print("✅ Corrections de score créées")

def create_reports(db, users):
    """Crée des rapports"""
    students = [u for u in users if u.role == UserRole.student]
    
    for student in students:
        # Rapport détaillé
        detailed_report = DetailedReport(
            student_id=student.id,
            report_type="progress",
            title=f"Rapport de progression - {student.username}",
            content=f"Rapport détaillé de la progression de {student.username}",
            generated_at=datetime.now() - timedelta(days=random.randint(1, 7))
        )
        db.add(detailed_report)
        
        # Rapport de matière
        subject_report = SubjectProgressReport(
            student_id=student.id,
            subject="Mathématiques",
            progress_percentage=random.randint(60, 100),
            current_level=random.randint(1, 5),
            recommendations="Continuer les exercices quotidiens",
            generated_at=datetime.now() - timedelta(days=random.randint(1, 7))
        )
        db.add(subject_report)
    
    db.commit()
    print("✅ Rapports créés")

def create_real_time_activities(db, users):
    """Crée des activités en temps réel"""
    students = [u for u in users if u.role == UserRole.student]
    
    for student in students:
        activity = RealTimeActivity(
            user_id=student.id,
            activity_type="online",
            status="active",
            current_page="/dashboard/student",
            session_duration=random.randint(10, 120),
            last_activity=datetime.now()
        )
        db.add(activity)
    
    db.commit()
    print("✅ Activités en temps réel créées")

if __name__ == "__main__":
    print("🚀 Démarrage du peuplement de la base de données...")
    populate_database()
    print("\n🎉 Base de données entièrement peuplée !")
    print("📊 Vous pouvez maintenant tester votre dashboard étudiant avec des données complètes !")
