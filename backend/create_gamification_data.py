#!/usr/bin/env python3
"""
Script pour créer des données réelles de gamification
"""

import os
import sys
from datetime import datetime, timedelta
import random

# Définir le chemin de la base de données
os.environ["SQLALCHEMY_DATABASE_URL"] = "sqlite:///F:/IMT/stage/Yancode/Najah__AI/data/app.db"

# Ajouter le répertoire backend au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_gamification_data():
    """Créer des données réelles de gamification"""
    
    try:
        from core.database import SessionLocal
        from models.user import User, UserRole
        from models.class_group import ClassGroup, ClassStudent
        from models.quiz import Quiz, QuizResult
        from models.badge import Badge, UserBadge
        from models.gamification import Achievement, UserAchievement, Leaderboard, LeaderboardEntry
        from models.learning_path import LearningPath
        from models.learning_path_step import LearningPathStep
        from models.student_analytics import StudentProgress, StudentAnalytics
        from models.user_activity import UserActivity
        from models.notification import Notification
        from models.content import Content
        from models.category import Category
        from models.learning_history import LearningHistory
        from models.assessment import Assessment, AssessmentQuestion, AssessmentResult
        from sqlalchemy import text
        
        db = SessionLocal()
        
        print("🎮 Création des données de gamification...")
        
        # 1. Créer des badges avec SQL direct
        print("🏆 Création des badges...")
        badges_data = [
            ("Premier Quiz", "Compléter votre premier quiz", "achievement", "quiz_completed_1", 50),
            ("Quiz Master", "Compléter 10 quiz", "achievement", "quiz_completed_10", 100),
            ("Streak 7 jours", "7 jours consécutifs d'activité", "streak", "streak_7_days", 200),
            ("Niveau 5", "Atteindre le niveau 5", "level", "level_5", 300),
            ("Parfait Score", "Obtenir 100% sur un quiz", "achievement", "perfect_score", 150)
        ]
        
        for name, description, badge_type, criteria, xp_reward in badges_data:
            db.execute(text("""
                INSERT INTO badges (name, description, badge_type, criteria, xp_reward, secret, is_hidden)
                VALUES (:name, :description, :badge_type, :criteria, :xp_reward, 0, 0)
            """), {
                "name": name,
                "description": description,
                "badge_type": badge_type,
                "criteria": criteria,
                "xp_reward": xp_reward
            })
        db.commit()
        
        # 2. Créer des challenges avec SQL direct
        print("🎯 Création des challenges...")
        challenges_data = [
            ("Quiz Quotidien", "Compléter un quiz chaque jour", 50, "daily", "quiz_daily"),
            ("Révision Hebdomadaire", "Réviser 5 sujets cette semaine", 100, "weekly", "revision_weekly"),
            ("Explorateur", "Explorer 3 nouveaux parcours", 150, "achievement", "explorer_paths")
        ]
        
        for name, description, points, category, criteria in challenges_data:
            db.execute(text("""
                INSERT INTO challenges (name, description, points, category, criteria, is_active)
                VALUES (:name, :description, :points, :category, :criteria, 1)
            """), {
                "name": name,
                "description": description,
                "points": points,
                "category": category,
                "criteria": criteria
            })
        db.commit()
        
        # 3. Créer des achievements avec SQL direct
        print("🏅 Création des achievements...")
        achievements_data = [
            ("Débutant", "Compléter votre premier contenu", 25, "quiz", "first_quiz"),
            ("Étudiant Assidu", "Compléter 5 quiz", 75, "quiz", "five_quizzes"),
            ("Expert", "Atteindre un score moyen de 90%", 200, "quiz", "high_score")
        ]
        
        for name, description, points, category, criteria in achievements_data:
            db.execute(text("""
                INSERT INTO achievements (name, description, points, category, criteria, is_hidden)
                VALUES (:name, :description, :points, :category, :criteria, 0)
            """), {
                "name": name,
                "description": description,
                "points": points,
                "category": category,
                "criteria": criteria
            })
        db.commit()
        
        # 4. Créer des niveaux utilisateurs avec SQL direct
        print("📊 Création des niveaux utilisateurs...")
        
        # Récupérer les utilisateurs avec SQL direct
        users_result = db.execute(text("SELECT id FROM users")).fetchall()
        users = [user[0] for user in users_result]
        
        # Récupérer les badges avec SQL direct
        badges_result = db.execute(text("SELECT id FROM badges")).fetchall()
        badges = [badge[0] for badge in badges_result]
        
        # Récupérer les challenges avec SQL direct
        challenges_result = db.execute(text("SELECT id FROM challenges")).fetchall()
        challenges = [challenge[0] for challenge in challenges_result]
        
        # Récupérer les achievements avec SQL direct
        achievements_result = db.execute(text("SELECT id FROM achievements")).fetchall()
        achievements = [achievement[0] for achievement in achievements_result]
        
        for user_id in users:
            # Créer un niveau pour chaque utilisateur
            level = random.randint(1, 10)
            current_xp = random.randint(0, 999)
            total_xp = random.randint(100, 5000)
            
            db.execute(text("""
                INSERT OR IGNORE INTO user_levels (user_id, level, current_xp, total_xp, xp_to_next_level)
                VALUES (:user_id, :level, :current_xp, :total_xp, 1000)
            """), {
                "user_id": user_id,
                "level": level,
                "current_xp": current_xp,
                "total_xp": total_xp
            })
            
            # Attribuer quelques badges aléatoirement
            for badge_id in random.sample(badges, min(random.randint(1, 3), len(badges))):
                db.execute(text("""
                    INSERT OR IGNORE INTO user_badge (user_id, badge_id, progression)
                    VALUES (:user_id, :badge_id, :progression)
                """), {
                    "user_id": user_id,
                    "badge_id": badge_id,
                    "progression": random.uniform(0.5, 1.0)
                })
            
            # Attribuer quelques achievements aléatoirement
            for achievement_id in random.sample(achievements, min(random.randint(1, 2), len(achievements))):
                db.execute(text("""
                    INSERT OR IGNORE INTO user_achievements (user_id, achievement_id)
                    VALUES (:user_id, :achievement_id)
                """), {
                    "user_id": user_id,
                    "achievement_id": achievement_id
                })
            
            # Attribuer quelques challenges aléatoirement
            for challenge_id in random.sample(challenges, min(random.randint(1, 2), len(challenges))):
                db.execute(text("""
                    INSERT OR IGNORE INTO user_challenges (user_id, challenge_id, progress, is_completed)
                    VALUES (:user_id, :challenge_id, :progress, :is_completed)
                """), {
                    "user_id": user_id,
                    "challenge_id": challenge_id,
                    "progress": random.uniform(0.0, 1.0),
                    "is_completed": random.choice([True, False])
                })
        
        db.commit()
        
        print("✅ Données de gamification créées avec succès !")
        
        # Afficher les statistiques avec SQL direct
        total_users = db.execute(text("SELECT COUNT(*) FROM users")).scalar()
        total_badges = db.execute(text("SELECT COUNT(*) FROM badges")).scalar()
        total_challenges = db.execute(text("SELECT COUNT(*) FROM challenges")).scalar()
        total_achievements = db.execute(text("SELECT COUNT(*) FROM achievements")).scalar()
        
        print(f"\n📊 Statistiques créées :")
        print(f"   👥 Utilisateurs avec niveaux : {total_users}")
        print(f"   🏆 Badges créés : {total_badges}")
        print(f"   🎯 Challenges créés : {total_challenges}")
        print(f"   🏅 Achievements créés : {total_achievements}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des données : {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    create_gamification_data()