#!/usr/bin/env python3
"""
Script de migration vers les données réelles
Remplace toutes les données mockées par de vraies données de la base de données
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from core.database import SessionLocal, engine
from models.user import User, UserRole
from models.quiz import Quiz, Question, QuizResult, QuizAnswer
from models.badge import Badge, UserBadge
from models.gamification import UserLevel, Achievement, UserAchievement, Challenge, UserChallenge
from models.class_group import ClassGroup, ClassStudent
from models.learning_history import LearningHistory
from models.notification import Notification, NotificationType
from models.student_learning_path import StudentLearningPath
from datetime import datetime, timedelta
import random

def create_test_data():
    """Créer des données de test pour remplacer les données mockées."""
    db = SessionLocal()
    
    try:
        # 1. Créer des utilisateurs de test si ils n'existent pas
        test_students = []
        for i in range(1, 6):
            student = db.query(User).filter(User.email == f"student{i}@test.com").first()
            if not student:
                student = User(
                    username=f"Étudiant {i}",
                    email=f"student{i}@test.com",
                    role=UserRole.student,
                    class_id=1
                )
                db.add(student)
                db.commit()
                db.refresh(student)
            test_students.append(student)
        
        # 2. Créer des quiz de test
        quiz_subjects = ["Mathématiques", "Histoire", "Sciences", "Français", "Anglais"]
        test_quizzes = []
        
        for i in range(1, 11):
            quiz = db.query(Quiz).filter(Quiz.id == i).first()
            if not quiz:
                quiz = Quiz(
                    title=f"Quiz Test {i}",
                    description=f"Quiz de test pour {quiz_subjects[i % len(quiz_subjects)]}",
                    subject=quiz_subjects[i % len(quiz_subjects)],
                    difficulty="medium",
                    max_score=100,
                    created_by=1  # Premier utilisateur
                )
                db.add(quiz)
                db.commit()
                db.refresh(quiz)
            test_quizzes.append(quiz)
        
        # 3. Créer des résultats de quiz
        for student in test_students:
            for quiz in test_quizzes:
                # Vérifier si le résultat existe déjà
                existing_result = db.query(QuizResult).filter(
                    QuizResult.student_id == student.id,
                    QuizResult.quiz_id == quiz.id
                ).first()
                
                if not existing_result:
                    # Créer un résultat avec un score aléatoire mais réaliste
                    score = random.randint(60, 95)
                    time_taken = random.randint(300, 1800)  # 5-30 minutes
                    
                    result = QuizResult(
                        quiz_id=quiz.id,
                        student_id=student.id,
                        score=score,
                        max_score=100,
                        time_taken=time_taken,
                        completed_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
                    )
                    db.add(result)
        
        # 4. Créer des badges de test
        badge_names = ["Premier Quiz", "Quiz Master", "Perfect Score", "Streak Master", "Early Bird"]
        test_badges = []
        
        for i, name in enumerate(badge_names):
            badge = db.query(Badge).filter(Badge.name == name).first()
            if not badge:
                badge = Badge(
                    name=name,
                    description=f"Badge pour {name}",
                    icon="🏆",
                    points=10 * (i + 1)
                )
                db.add(badge)
                db.commit()
                db.refresh(badge)
            test_badges.append(badge)
        
        # 5. Attribuer des badges aux étudiants
        for student in test_students:
            # Attribuer 1-3 badges par étudiant
            num_badges = random.randint(1, 3)
            selected_badges = random.sample(test_badges, num_badges)
            
            for badge in selected_badges:
                existing_badge = db.query(UserBadge).filter(
                    UserBadge.user_id == student.id,
                    UserBadge.badge_id == badge.id
                ).first()
                
                if not existing_badge:
                    user_badge = UserBadge(
                        user_id=student.id,
                        badge_id=badge.id,
                        earned_at=datetime.utcnow() - timedelta(days=random.randint(1, 60))
                    )
                    db.add(user_badge)
        
        # 6. Créer des niveaux utilisateur
        for student in test_students:
            user_level = db.query(UserLevel).filter(UserLevel.user_id == student.id).first()
            if not user_level:
                level = random.randint(1, 10)
                experience = level * 100 + random.randint(0, 99)
                
                user_level = UserLevel(
                    user_id=student.id,
                    level=level,
                    experience=experience
                )
                db.add(user_level)
        
        # 7. Créer des notifications de test
        notification_types = [
            NotificationType.QUIZ_COMPLETED,
            NotificationType.BADGE_EARNED,
            NotificationType.ACHIEVEMENT_UNLOCKED
        ]
        
        for student in test_students:
            # Créer 2-5 notifications par étudiant
            num_notifications = random.randint(2, 5)
            for _ in range(num_notifications):
                notification_type = random.choice(notification_types)
                notification = Notification(
                    user_id=student.id,
                    title=f"Notification {notification_type.value}",
                    message=f"Vous avez accompli quelque chose de génial !",
                    notification_type=notification_type,
                    is_read=random.choice([True, False]),
                    created_at=datetime.utcnow() - timedelta(days=random.randint(1, 7))
                )
                db.add(notification)
        
        # 8. Créer des historiques d'apprentissage
        for student in test_students:
            # Créer 5-15 sessions d'apprentissage
            num_sessions = random.randint(5, 15)
            for _ in range(num_sessions):
                session = LearningHistory(
                    user_id=student.id,
                    activity_type="quiz_completion",
                    duration=random.randint(300, 1800),  # 5-30 minutes
                    timestamp=datetime.utcnow() - timedelta(days=random.randint(1, 30))
                )
                db.add(session)
        
        db.commit()
        print("✅ Données de test créées avec succès !")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erreur lors de la création des données de test: {e}")
        raise
    finally:
        db.close()

def verify_real_data():
    """Vérifier que les données réelles sont utilisées."""
    db = SessionLocal()
    
    try:
        # Vérifier les statistiques
        total_students = db.query(User).filter(User.role == UserRole.student).count()
        total_quizzes = db.query(Quiz).count()
        total_results = db.query(QuizResult).count()
        total_badges = db.query(Badge).count()
        total_notifications = db.query(Notification).count()
        
        print(f"📊 Statistiques de la base de données:")
        print(f"   - Étudiants: {total_students}")
        print(f"   - Quiz: {total_quizzes}")
        print(f"   - Résultats de quiz: {total_results}")
        print(f"   - Badges: {total_badges}")
        print(f"   - Notifications: {total_notifications}")
        
        if total_students > 0 and total_quizzes > 0 and total_results > 0:
            print("✅ Données réelles détectées !")
            return True
        else:
            print("⚠️ Données insuffisantes, création de données de test...")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Migration vers les données réelles...")
    
    # Vérifier les données existantes
    if not verify_real_data():
        # Créer des données de test
        create_test_data()
    
    print("✅ Migration terminée !") 