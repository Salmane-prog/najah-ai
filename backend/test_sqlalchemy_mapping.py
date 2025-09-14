#!/usr/bin/env python3
"""
Script de test pour vérifier les mappings SQLAlchemy
"""

import os
import sys

# Définir le chemin de la base de données
os.environ["SQLALCHEMY_DATABASE_URL"] = "sqlite:///F:/IMT/stage/Yancode/Najah__AI/data/app.db"

# Ajouter le répertoire backend au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_sqlalchemy_mapping():
    """Test des mappings SQLAlchemy"""
    
    print("🔍 Test des mappings SQLAlchemy...")
    
    try:
        # Importer les modèles
        from models.user import User, UserRole
        from models.class_group import ClassGroup, ClassStudent
        from models.quiz import Quiz, QuizResult
        from models.content import Content
        from models.category import Category
        from models.badge import Badge, UserBadge
        from models.learning_path import LearningPath
        from models.learning_path_step import LearningPathStep
        from models.student_learning_path import StudentLearningPath
        from models.learning_history import LearningHistory
        from models.notification import Notification
        from models.messages import Message
        from models.thread import Thread
        from models.forum import ForumCategory, ForumModeration, ForumVote, ForumTag, ThreadTag, ForumReport
        from models.notes import UserNote
        from models.assessment import Assessment, AssessmentQuestion, AssessmentResult
        from models.settings import UserSettings
        from models.ratings import ResourceRating
        from models.remediation import RemediationPlan, RemediationActivity
        from models.score_correction import ScoreCorrection
        from models.user_activity import UserActivity
        from models.homework import AdvancedHomework, AdvancedHomeworkSubmission, AdvancedHomeworkAssignment
        from models.student_analytics import StudentAnalytics, StudentProgress
        from models.schedule import ScheduleEvent
        from models.calendar import CalendarEvent, EventReminder, CalendarStudySession
        
        print("✅ Import des modèles réussi")
        
        # Test de création d'instances
        print("🔍 Test de création d'instances...")
        
        # Test User
        user = User(
            username="test_user",
            email="test@example.com",
            hashed_password="hashed_password",
            role="student"
        )
        print("✅ Instance User créée")
        
        # Test Badge
        badge = Badge(
            name="Test Badge",
            description="Test Description",
            secret=False
        )
        print("✅ Instance Badge créée")
        
        # Test UserBadge
        user_badge = UserBadge(
            user_id=1,
            badge_id=1,
            progression=1.0
        )
        print("✅ Instance UserBadge créée")
        
        # Test Quiz
        quiz = Quiz(
            title="Test Quiz",
            description="Test Description",
            level="beginner",
            created_by=1
        )
        print("✅ Instance Quiz créée")
        
        # Test ClassGroup
        class_group = ClassGroup(
            name="Test Class",
            description="Test Description",
            teacher_id=1,
            level="beginner",
            subject="Math"
        )
        print("✅ Instance ClassGroup créée")
        
        # Test LearningPath
        learning_path = LearningPath(
            title="Test Path",
            description="Test Description",
            level="beginner",
            subject="Math",
            created_by=1
        )
        print("✅ Instance LearningPath créée")
        
        print("🎉 Tous les mappings SQLAlchemy fonctionnent correctement !")
        
    except Exception as e:
        print(f"❌ Erreur lors du test des mappings : {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    test_sqlalchemy_mapping() 