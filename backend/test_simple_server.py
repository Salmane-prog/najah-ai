#!/usr/bin/env python3
"""
Serveur simple pour tester l'endpoint gamification
"""

import os
import sys
import json
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Définir le chemin de la base de données
os.environ["SQLALCHEMY_DATABASE_URL"] = "sqlite:///F:/IMT/stage/Yancode/Najah__AI/data/app.db"

# Ajouter le répertoire backend au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import SessionLocal, get_db
from models.user import User
from models.gamification import UserLevel, UserAchievement, UserChallenge
from models.quiz import QuizResult
from sqlalchemy import text

app = FastAPI(title="Test Server", version="1.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/gamification/user/stats")
def get_user_gamification_stats(db: Session = Depends(get_db)):
    """Récupérer les statistiques de gamification de l'utilisateur connecté."""
    
    try:
        print(f"[DEBUG] get_user_gamification_stats appelé")
        
        # Récupérer le premier utilisateur (pour le test)
        user = db.query(User).first()
        if not user:
            raise HTTPException(status_code=404, detail="Aucun utilisateur trouvé")
        
        print(f"[DEBUG] Utilisateur trouvé: {user.username} (ID: {user.id})")
        
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
        
        print(f"[DEBUG] Résultat: {result}")
        return result
        
    except Exception as e:
        print(f"[ERROR] Erreur dans get_user_gamification_stats: {e}")
        import traceback
        traceback.print_exc()
        # Retourner des données par défaut en cas d'erreur
        return {
            "user_id": 1,
            "level": 1,
            "current_xp": 0,
            "total_xp": 0,
            "progress_percentage": 0,
            "badges_count": 0,
            "achievements_count": 0,
            "challenges_count": 0,
            "completed_challenges": 0,
            "total_quizzes": 0,
            "completed_quizzes": 0,
            "average_score": 0,
            "completion_rate": 0
        }

@app.get("/")
def read_root():
    return {"message": "Test server is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)