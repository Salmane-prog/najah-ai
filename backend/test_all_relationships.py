#!/usr/bin/env python3
"""
Script de test pour vérifier toutes les relations SQLAlchemy
"""

import os
import sys

# Définir le chemin de la base de données
os.environ["SQLALCHEMY_DATABASE_URL"] = "sqlite:///F:/IMT/stage/Yancode/Najah__AI/data/app.db"

# Ajouter le répertoire backend au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_all_relationships():
    """Test de toutes les relations SQLAlchemy"""

    print("🔍 Test de toutes les relations SQLAlchemy...")

    try:
        # Importer tous les modèles
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

        print("✅ Import de tous les modèles réussi")

        # Test de création d'instances pour chaque modèle
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

        # Test Notification
        notification = Notification(
            user_id=1,
            title="Test Notification",
            message="Test message",
            notification_type="SYSTEM_ALERT"
        )
        print("✅ Instance Notification créée")

        # Test Assessment
        assessment = Assessment(
            student_id=1,
            assessment_type="initial",
            title="Test Assessment",
            description="Test description"
        )
        print("✅ Instance Assessment créée")

        # Test AssessmentQuestion
        assessment_question = AssessmentQuestion(
            assessment_id=1,
            question_text="Test question",
            question_type="mcq",
            subject="Mathématiques",
            difficulty="beginner",
            correct_answer="A"
        )
        print("✅ Instance AssessmentQuestion créée")

        # Test AssessmentResult
        assessment_result = AssessmentResult(
            assessment_id=1,
            student_id=1,
            total_score=80.0,
            max_score=100.0,
            percentage=80.0
        )
        print("✅ Instance AssessmentResult créée")

        # Test UserLevel
        user_level = UserLevel(
            user_id=1,
            level=1,
            current_xp=0
        )
        print("✅ Instance UserLevel créée")

        # Test Challenge
        challenge = Challenge(
            title="Test Challenge",
            description="Test description",
            challenge_type="daily",
            xp_reward=100
        )
        print("✅ Instance Challenge créée")

        # Test UserChallenge
        user_challenge = UserChallenge(
            user_id=1,
            challenge_id=1,
            progress=0.5
        )
        print("✅ Instance UserChallenge créée")

        # Test Achievement
        achievement = Achievement(
            title="Test Achievement",
            description="Test description",
            achievement_type="quiz",
            xp_reward=50
        )
        print("✅ Instance Achievement créée")

        # Test UserAchievement
        user_achievement = UserAchievement(
            user_id=1,
            achievement_id=1
        )
        print("✅ Instance UserAchievement créée")

        # Test Leaderboard
        leaderboard = Leaderboard(
            title="Test Leaderboard",
            description="Test description",
            leaderboard_type="global"
        )
        print("✅ Instance Leaderboard créée")

        # Test LeaderboardEntry
        leaderboard_entry = LeaderboardEntry(
            leaderboard_id=1,
            user_id=1,
            score=1000
        )
        print("✅ Instance LeaderboardEntry créée")

        # Test Quiz
        quiz = Quiz(
            title="Test Quiz",
            description="Test description",
            level="beginner",
            created_by=1
        )
        print("✅ Instance Quiz créée")

        # Test QuizResult
        quiz_result = QuizResult(
            quiz_id=1,
            student_id=1,
            score=85.0,
            max_score=100.0,
            time_taken=300,
            completed=True,
            sujet="Général"
        )
        print("✅ Instance QuizResult créée")

        # Test QuizAssignment
        quiz_assignment = QuizAssignment(
            quiz_id=1,
            student_id=1
        )
        print("✅ Instance QuizAssignment créée")

        # Test ClassGroup
        class_group = ClassGroup(
            name="Test Class",
            description="Test description",
            teacher_id=1,
            level="beginner",
            subject="Math"
        )
        print("✅ Instance ClassGroup créée")

        # Test ClassStudent
        class_student = ClassStudent(
            class_id=1,
            student_id=1
        )
        print("✅ Instance ClassStudent créée")

        # Test LearningPath
        learning_path = LearningPath(
            title="Test Path",
            description="Test description",
            level="beginner",
            subject="Math",
            created_by=1
        )
        print("✅ Instance LearningPath créée")

        # Test StudentLearningPath
        student_learning_path = StudentLearningPath(
            path_id=1,
            student_id=1
        )
        print("✅ Instance StudentLearningPath créée")

        # Test LearningPathStep
        learning_path_step = LearningPathStep(
            learning_path_id=1,
            title="Test Step",
            description="Test description",
            order=1
        )
        print("✅ Instance LearningPathStep créée")

        # Test StudentProgress
        student_progress = StudentProgress(
            student_id=1,
            learning_path_id=1,
            current_step_id=1
        )
        print("✅ Instance StudentProgress créée")

        # Test ClassAnalytics
        class_analytics = ClassAnalytics(
            class_id=1,
            total_students=25,
            average_score=85.0
        )
        print("✅ Instance ClassAnalytics créée")

        # Test StudentAnalytics
        student_analytics = StudentAnalytics(
            student_id=1,
            total_quizzes=10,
            time_spent=3600
        )
        print("✅ Instance StudentAnalytics créée")

        # Test RealTimeActivity
        real_time_activity = RealTimeActivity(
            student_id=1,
            activity_type="quiz_started",
            activity_data="Started math quiz"
        )
        print("✅ Instance RealTimeActivity créée")

        print("🎉 Toutes les relations SQLAlchemy fonctionnent correctement !")

    except Exception as e:
        print(f"❌ Erreur lors du test des relations : {e}")
        import traceback
        traceback.print_exc()
        return False

    return True

if __name__ == "__main__":
    test_all_relationships()