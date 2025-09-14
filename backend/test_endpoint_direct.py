#!/usr/bin/env python3
"""
Test direct de l'endpoint gamification sans serveur
"""

import os
import sys
import json

# Définir le chemin de la base de données
os.environ["SQLALCHEMY_DATABASE_URL"] = "sqlite:///F:/IMT/stage/Yancode/Najah__AI/data/app.db"

# Ajouter le répertoire backend au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_gamification_direct():
    """Tester l'endpoint gamification directement"""
    
    try:
        from core.database import SessionLocal
        from models.user import User
        from models.gamification import UserLevel, UserAchievement, UserChallenge
        from models.quiz import QuizResult
        from sqlalchemy import text
        
        print("🔍 Test direct de l'endpoint gamification...")
        
        # Créer une session
        db = SessionLocal()
        
        # Récupérer un utilisateur
        user = db.query(User).first()
        if not user:
            print("❌ Aucun utilisateur trouvé")
            return
        
        print(f"👤 Utilisateur: {user.username} (ID: {user.id})")
        
        # Récupérer le niveau de l'utilisateur
        user_level = db.query(UserLevel).filter(UserLevel.user_id == user.id).first()
        
        # Créer un niveau par défaut si l'utilisateur n'en a pas
        if not user_level:
            user_level = UserLevel(
                user_id=user.id,
                level=1,
                current_xp=0,
                total_xp=0,
                xp_to_next_level=1000
            )
            db.add(user_level)
            db.commit()
            db.refresh(user_level)
            print("✅ Niveau utilisateur créé")
        
        # Récupérer les badges (via SQL direct)
        badges_count = db.execute(text("SELECT COUNT(*) FROM user_badge WHERE user_id = :user_id"), {"user_id": user.id}).scalar()
        
        # Récupérer les achievements
        user_achievements = db.query(UserAchievement).filter(UserAchievement.user_id == user.id).count()
        
        # Récupérer les challenges
        user_challenges = db.query(UserChallenge).filter(UserChallenge.user_id == user.id).count()
        completed_challenges = db.query(UserChallenge).filter(
            UserChallenge.user_id == user.id,
            UserChallenge.is_completed == True
        ).count()
        
        # Récupérer les résultats de quiz
        quiz_results = db.query(QuizResult).filter(QuizResult.student_id == user.id).all()
        total_quizzes = len(quiz_results)
        completed_quizzes = len([r for r in quiz_results if r.is_completed])
        avg_score = sum(r.score for r in quiz_results if r.score) / len(quiz_results) if quiz_results else 0
        
        # Calculer le pourcentage de progression
        progress_percentage = (user_level.current_xp / 1000) * 100 if user_level else 0
        
        result = {
            "user_id": user.id,
            "level": user_level.level if user_level else 1,
            "current_xp": user_level.current_xp if user_level else 0,
            "total_xp": user_level.total_xp if user_level else 0,
            "progress_percentage": progress_percentage,
            "badges_count": badges_count,
            "achievements_count": user_achievements,
            "challenges_count": user_challenges,
            "completed_challenges": completed_challenges,
            "total_quizzes": total_quizzes,
            "completed_quizzes": completed_quizzes,
            "average_score": round(avg_score, 2),
            "completion_rate": round((completed_quizzes / total_quizzes * 100) if total_quizzes > 0 else 0, 2)
        }
        
        print("✅ Données gamification récupérées:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        db.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gamification_direct()