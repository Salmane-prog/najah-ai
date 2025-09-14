from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, desc, asc
from core.database import get_db
from models.user import User, UserRole
from models.quiz import QuizResult
from models.learning_history import LearningHistory
from models.badge import UserBadge
from api.v1.auth import require_role
from api.v1.users import get_current_user
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json

router = APIRouter()

@router.get("/teacher-tasks")
async def get_teacher_tasks(
    current_user: User = Depends(require_role(['teacher'])),
    db: Session = Depends(get_db)
):
    """Récupérer les tâches pour un professeur"""
    try:
        # Récupérer les tâches du professeur
        # Pour l'instant, retournons des tâches simulées
        tasks = [
            {
                "id": 1,
                "title": "Corriger les quiz de la semaine",
                "description": "Vérifier et corriger les quiz soumis par les étudiants",
                "priority": "high",
                "due_date": (datetime.now() + timedelta(days=2)).isoformat(),
                "status": "pending",
                "type": "correction"
            },
            {
                "id": 2,
                "title": "Préparer le prochain cours",
                "description": "Créer le contenu pour le prochain cours de mathématiques",
                "priority": "medium",
                "due_date": (datetime.now() + timedelta(days=5)).isoformat(),
                "status": "in_progress",
                "type": "preparation"
            },
            {
                "id": 3,
                "title": "Évaluer les performances",
                "description": "Analyser les performances des étudiants et générer des rapports",
                "priority": "low",
                "due_date": (datetime.now() + timedelta(days=7)).isoformat(),
                "status": "pending",
                "type": "evaluation"
            }
        ]
        
        return {
            "teacher_id": current_user.id,
            "tasks": tasks,
            "total_count": len(tasks)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération des tâches: {str(e)}"
        )

@router.get("/user/{user_id}/recent")
def get_user_recent_activity(
    user_id: int,
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student', 'teacher', 'admin']))
):
    """Récupérer l'activité récente d'un utilisateur."""
    try:
        # Vérifier que l'utilisateur existe
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        
        # Récupérer les quiz récents
        recent_quizzes = db.query(QuizResult).filter(
            QuizResult.student_id == user_id
        ).order_by(desc(QuizResult.created_at)).limit(limit).all()
        
        # Récupérer l'historique d'apprentissage récent
        recent_learning = db.query(LearningHistory).filter(
            LearningHistory.student_id == user_id
        ).order_by(desc(LearningHistory.timestamp)).limit(limit).all()
        
        activities = []
        
        # Ajouter les quiz
        for quiz in recent_quizzes:
            activities.append({
                "id": quiz.id,
                "type": "quiz",
                "description": f"Quiz complété avec {quiz.score}%",
                "details": {
                    "quiz_id": quiz.quiz_id,
                    "score": quiz.score,
                    "duration": quiz.time_spent if hasattr(quiz, 'time_spent') else None
                },
                "created_at": quiz.created_at.isoformat(),
                "duration": quiz.time_spent if hasattr(quiz, 'time_spent') else 0,
                "score": quiz.score or 0,
                "quiz_title": f"Quiz #{quiz.quiz_id}",
                "subject": "Général"
            })
        
        # Ajouter l'historique d'apprentissage
        for learning in recent_learning:
            activities.append({
                "id": learning.id,
                "type": "learning",
                "description": f"Session d'apprentissage",
                "details": {
                    "content_id": learning.content_id,
                    "duration": 0  # Pas de colonne duration dans LearningHistory
                },
                "created_at": learning.timestamp.isoformat(),
                "duration": 0,  # Pas de colonne duration dans LearningHistory
                "score": learning.score or 0,
                "subject": "Général"
            })
        
        # Trier par date de création
        activities.sort(key=lambda x: x["created_at"], reverse=True)
        
        return {
            "user_id": user_id,
            "activities": activities[:limit],
            "total_count": len(activities)
        }
        
    except Exception as e:
        print(f"Erreur dans get_user_recent_activity: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération de l'activité: {str(e)}")

@router.get("/user/{user_id}/stats")
def get_user_activity_stats(
    user_id: int,
    period: str = Query("week", regex="^(day|week|month|year)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student', 'teacher', 'admin']))
):
    """Récupérer les statistiques d'activité d'un utilisateur."""
    try:
        # Vérifier que l'utilisateur existe
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        
        # Calculer la période
        now = datetime.utcnow()
        if period == "day":
            start_date = now - timedelta(days=1)
        elif period == "week":
            start_date = now - timedelta(weeks=1)
        elif period == "month":
            start_date = now - timedelta(days=30)
        else:  # year
            start_date = now - timedelta(days=365)
        
        # Statistiques des quiz
        quiz_stats = db.query(
            func.count(QuizResult.id).label('total_quizzes'),
            func.avg(QuizResult.score).label('average_score'),
            func.sum(QuizResult.time_spent).label('total_duration')
        ).filter(
            QuizResult.student_id == user_id,
            QuizResult.created_at >= start_date
        ).first()
        
        # Statistiques d'apprentissage
        learning_stats = db.query(
            func.count(LearningHistory.id).label('total_sessions'),
            func.sum(0).label('total_study_time')  # Pas de colonne duration dans LearningHistory
        ).filter(
            LearningHistory.student_id == user_id,
            LearningHistory.timestamp >= start_date
        ).first()
        
        # Activités quotidiennes
        daily_activities = []
        current_date = start_date.date()
        while current_date <= now.date():
            day_quizzes = db.query(QuizResult).filter(
                QuizResult.student_id == user_id,
                func.date(QuizResult.created_at) == current_date
            ).count()
            
            day_learning = db.query(LearningHistory).filter(
                LearningHistory.student_id == user_id,
                func.date(LearningHistory.timestamp) == current_date
            ).count()
            
            daily_activities.append({
                "date": current_date.isoformat(),
                "count": day_quizzes + day_learning
            })
            
            current_date += timedelta(days=1)
        
        return {
            "user_id": user_id,
            "period": period,
            "quiz_stats": {
                "total_quizzes": quiz_stats.total_quizzes or 0,
                "average_score": round(quiz_stats.average_score or 0, 1),
                "total_duration": quiz_stats.total_duration or 0
            },
            "learning_stats": {
                "total_sessions": learning_stats.total_sessions or 0,
                "total_study_time": learning_stats.total_study_time or 0
            },
            "daily_activities": daily_activities
        }
        
    except Exception as e:
        print(f"Erreur dans get_user_activity_stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des statistiques: {str(e)}")

@router.post("/user/{user_id}/log")
def log_user_activity(
    user_id: int,
    activity_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student', 'teacher', 'admin']))
):
    """Enregistrer une nouvelle activité utilisateur."""
    try:
        # Vérifier que l'utilisateur existe
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        
        # Créer une nouvelle entrée d'historique d'apprentissage
        new_activity = LearningHistory(
            student_id=user_id,
            content_id=activity_data.get("related_id"),
            action=activity_data.get("type", "general"),
            score=activity_data.get("score", 0),
            details=json.dumps(activity_data.get("details", {}))
        )
        
        db.add(new_activity)
        db.commit()
        db.refresh(new_activity)
        
        return {
            "id": new_activity.id,
            "user_id": user_id,
            "type": activity_data.get("type"),
            "description": activity_data.get("description"),
            "created_at": new_activity.timestamp.isoformat()
        }
        
    except Exception as e:
        print(f"Erreur dans log_user_activity: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'enregistrement de l'activité: {str(e)}")

@router.get("/user/{user_id}/timeline")
def get_user_activity_timeline(
    user_id: int,
    days: int = Query(7, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student', 'teacher', 'admin']))
):
    """Récupérer la timeline d'activité d'un utilisateur."""
    try:
        # Vérifier que l'utilisateur existe
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Récupérer toutes les activités
        activities = []
        
        # Quiz
        quizzes = db.query(QuizResult).filter(
            QuizResult.student_id == user_id,
            QuizResult.created_at >= start_date
        ).all()
        
        for quiz in quizzes:
            activities.append({
                "id": quiz.id,
                "type": "quiz",
                "description": f"Quiz complété avec {quiz.score}%",
                "timestamp": quiz.created_at.isoformat()
            })
        
        # Apprentissage
        learning = db.query(LearningHistory).filter(
            LearningHistory.student_id == user_id,
            LearningHistory.timestamp >= start_date
        ).all()
        
        for learn in learning:
            activities.append({
                "id": learn.id,
                "type": "learning",
                "description": "Session d'apprentissage",
                "timestamp": learn.timestamp.isoformat()
            })
        
        # Trier par date
        activities.sort(key=lambda x: x["timestamp"], reverse=True)
        
        # Grouper par jour
        timeline = {}
        for activity in activities:
            date = activity["timestamp"][:10]  # YYYY-MM-DD
            if date not in timeline:
                timeline[date] = []
            timeline[date].append(activity)
        
        return {
            "user_id": user_id,
            "timeline": timeline,
            "days": days
        }
        
    except Exception as e:
        print(f"Erreur dans get_user_activity_timeline: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération de la timeline: {str(e)}")

@router.get("/user/{user_id}/achievements")
def get_user_activity_achievements(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student', 'teacher', 'admin']))
):
    """Récupérer les achievements basés sur l'activité d'un utilisateur."""
    try:
        # Vérifier que l'utilisateur existe
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        
        achievements = []
        
        # Statistiques de base
        total_quizzes = db.query(QuizResult).filter(QuizResult.student_id == user_id).count()
        total_study_time = db.query(func.sum(0)).filter(
            LearningHistory.student_id == user_id
        ).scalar() or 0  # Pas de colonne duration dans LearningHistory
        
        # Achievement: Quiz Master
        if total_quizzes >= 10:
            achievements.append({
                "type": "quiz_master",
                "title": "Quiz Master",
                "description": f"Complété {total_quizzes} quiz",
                "achieved": True,
                "achieved_at": datetime.utcnow().isoformat(),
                "count": total_quizzes
            })
        else:
            achievements.append({
                "type": "quiz_master",
                "title": "Quiz Master",
                "description": f"Compléter 10 quiz ({10 - total_quizzes} restants)",
                "achieved": False,
                "count": total_quizzes
            })
        
        # Achievement: Study Time
        if total_study_time >= 3600:  # 1 heure
            achievements.append({
                "type": "study_time",
                "title": "Étudiant Assidu",
                "description": f"Accumulé {total_study_time // 60} minutes d'étude",
                "achieved": True,
                "achieved_at": datetime.utcnow().isoformat(),
                "study_time": total_study_time
            })
        else:
            achievements.append({
                "type": "study_time",
                "title": "Étudiant Assidu",
                "description": f"Accumuler 60 minutes d'étude ({60 - (total_study_time // 60)} restantes)",
                "achieved": False,
                "study_time": total_study_time
            })
        
        # Achievement: Streak (simulé)
        achievements.append({
            "type": "streak",
            "title": "Série Continue",
            "description": "Étudier 7 jours de suite",
            "achieved": False,
            "streak_days": 0
        })
        
        return {
            "user_id": user_id,
            "achievements": achievements,
            "total_achievements": len([a for a in achievements if a["achieved"]])
        }
        
    except Exception as e:
        print(f"Erreur dans get_user_activity_achievements: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des achievements: {str(e)}")

@router.delete("/user/{user_id}/activity/{activity_id}")
def delete_user_activity(
    user_id: int,
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student', 'teacher', 'admin']))
):
    """Supprimer une activité utilisateur."""
    try:
        # Vérifier que l'utilisateur existe
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        
        # Supprimer l'activité (LearningHistory)
        activity = db.query(LearningHistory).filter(
            LearningHistory.id == activity_id,
            LearningHistory.student_id == user_id
        ).first()
        
        if not activity:
            raise HTTPException(status_code=404, detail="Activité non trouvée")
        
        db.delete(activity)
        db.commit()
        
        return {"message": "Activité supprimée avec succès"}
        
    except Exception as e:
        print(f"Erreur dans delete_user_activity: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur lors de la suppression de l'activité: {str(e)}")
