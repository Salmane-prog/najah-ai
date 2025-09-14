from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from core.database import get_db
from models.user import User
from models.quiz import Quiz, QuizResult
from typing import List, Dict, Any
from datetime import datetime, timedelta
import json

router = APIRouter()

@router.get("/user/{user_id}/events")
def get_user_calendar_events(
    user_id: int,
    start_date: str = Query(None, description="Date de début (YYYY-MM-DD)"),
    end_date: str = Query(None, description="Date de fin (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Récupérer les événements du calendrier d'un utilisateur (version test sans auth)"""
    try:
        # Vérifier que l'utilisateur existe
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        
        # Déterminer la période
        if start_date:
            try:
                start = datetime.fromisoformat(start_date)
            except ValueError:
                start = datetime.utcnow() - timedelta(days=30)
        else:
            start = datetime.utcnow() - timedelta(days=30)
            
        if end_date:
            try:
                end = datetime.fromisoformat(end_date)
            except ValueError:
                end = datetime.utcnow() + timedelta(days=30)
        else:
            end = datetime.utcnow() + timedelta(days=30)
        
        # Récupérer les quiz assignés
        assigned_quizzes = db.query(Quiz).filter(
            Quiz.is_active == True
        ).all()
        
        # Récupérer les résultats de quiz
        quiz_results = db.query(QuizResult).filter(
            QuizResult.student_id == user_id,
            QuizResult.created_at >= start,
            QuizResult.created_at <= end
        ).all()
        
        # Formater les événements
        events = []
        
        # Ajouter les quiz assignés comme événements
        for quiz in assigned_quizzes[:5]:  # Limiter à 5 quiz
            events.append({
                "id": f"quiz_{quiz.id}",
                "title": f"Quiz: {quiz.title}",
                "type": "quiz_assignment",
                "start_date": (datetime.utcnow() + timedelta(days=7)).isoformat(),
                "end_date": (datetime.utcnow() + timedelta(days=7, hours=1)).isoformat(),
                "description": quiz.description or "Quiz assigné",
                "subject": quiz.subject or "Général",
                "difficulty": quiz.difficulty,
                "estimated_duration": quiz.time_limit or 30,
                "status": "pending"
            })
        
        # Ajouter les quiz complétés comme événements
        for result in quiz_results:
            events.append({
                "id": f"result_{result.id}",
                "title": f"Quiz complété: {result.sujet or 'Quiz'}",
                "type": "quiz_completed",
                "start_date": result.created_at.isoformat(),
                "end_date": (result.created_at + timedelta(minutes=30)).isoformat(),
                "description": f"Score: {result.score}%",
                "subject": result.sujet or "Général",
                "score": result.score,
                "time_spent": result.time_spent or 0,
                "status": "completed"
            })
        
        # Si aucun événement, créer des événements de test
        if not events:
            events = [
                {
                    "id": "test_1",
                    "title": "Quiz de Grammaire",
                    "type": "quiz_assignment",
                    "start_date": (datetime.utcnow() + timedelta(days=3)).isoformat(),
                    "end_date": (datetime.utcnow() + timedelta(days=3, hours=1)).isoformat(),
                    "description": "Quiz de grammaire française de base",
                    "subject": "Français",
                    "difficulty": "medium",
                    "estimated_duration": 30,
                    "status": "pending"
                },
                {
                    "id": "test_2",
                    "title": "Révision Vocabulaire",
                    "type": "study_session",
                    "start_date": (datetime.utcnow() + timedelta(days=5)).isoformat(),
                    "end_date": (datetime.utcnow() + timedelta(days=5, hours=2)).isoformat(),
                    "description": "Session de révision du vocabulaire A1",
                    "subject": "Français",
                    "difficulty": "easy",
                    "estimated_duration": 120,
                    "status": "scheduled"
                }
            ]
        
        # Trier par date de début
        events.sort(key=lambda x: x["start_date"])
        
        return {
            "user_id": user_id,
            "period": {
                "start": start.isoformat(),
                "end": end.isoformat()
            },
            "total_events": len(events),
            "events": events
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur get_user_calendar_events: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération: {str(e)}")

@router.get("/user/{user_id}/upcoming")
def get_upcoming_events(
    user_id: int,
    days: int = Query(7, description="Nombre de jours à venir"),
    db: Session = Depends(get_db)
):
    """Récupérer les événements à venir d'un utilisateur"""
    try:
        start_date = datetime.utcnow()
        end_date = start_date + timedelta(days=days)
        
        events = get_user_calendar_events(
            user_id, 
            start_date.strftime("%Y-%m-%d"), 
            end_date.strftime("%Y-%m-%d"), 
            db
        )
        
        # Filtrer seulement les événements à venir
        upcoming_events = [
            event for event in events["events"]
            if event["start_date"] > datetime.utcnow().isoformat()
        ]
        
        return {
            "user_id": user_id,
            "days_ahead": days,
            "total_upcoming": len(upcoming_events),
            "events": upcoming_events
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@router.get("/user/{user_id}/today")
def get_today_events(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Récupérer les événements d'aujourd'hui pour un utilisateur"""
    try:
        today = datetime.utcnow().date()
        start_date = datetime.combine(today, datetime.min.time())
        end_date = datetime.combine(today, datetime.max.time())
        
        events = get_user_calendar_events(
            user_id,
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d"),
            db
        )
        
        # Filtrer les événements d'aujourd'hui
        today_events = [
            event for event in events["events"]
            if start_date <= datetime.fromisoformat(event["start_date"]) <= end_date
        ]
        
        return {
            "user_id": user_id,
            "date": today.isoformat(),
            "total_events": len(today_events),
            "events": today_events
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}") 