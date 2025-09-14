from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy import func

from core.database import SessionLocal
from api.v1.users import get_current_user
from models.user import User
from models.organization import Homework, StudySession, Reminder, LearningGoal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(tags=["Organization Advanced"])

# =====================================================
# CALENDRIER INTELLIGENT
# =====================================================

@router.get("/calendar/events")
def get_calendar_events(
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer tous les événements du calendrier"""
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)
    
    events = []
    
    # Devoirs
    homeworks = db.query(Homework).filter(
        Homework.assigned_to == current_user.id,
        Homework.due_date.between(start, end)
    ).all()
    
    for hw in homeworks:
        events.append({
            "id": f"homework_{hw.id}",
            "title": hw.title,
            "start": hw.due_date.isoformat(),
            "end": (hw.due_date + timedelta(hours=1)).isoformat(),
            "type": "homework",
            "priority": hw.priority,
            "color": "#EF4444" if hw.priority == "high" else "#F59E0B"
        })
    
    return events

# =====================================================
# ANALYTICS DE PRODUCTIVITÉ
# =====================================================

@router.get("/analytics/productivity")
def get_productivity_analytics(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Analytics de productivité"""
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Sessions d'étude
    sessions = db.query(StudySession).filter(
        StudySession.user_id == current_user.id,
        StudySession.start_time >= start_date
    ).all()
    
    total_study_time = sum(s.actual_duration or 0 for s in sessions)
    avg_productivity = sum(s.productivity_rating or 0 for s in sessions) / len(sessions) if sessions else 0
    
    # Devoirs
    homeworks = db.query(Homework).filter(
        Homework.assigned_to == current_user.id,
        Homework.due_date >= start_date
    ).all()
    
    completed_homework = len([h for h in homeworks if h.status == "completed"])
    total_homework = len(homeworks)
    completion_rate = (completed_homework / total_homework * 100) if total_homework > 0 else 0
    
    return {
        "study_time_hours": round(total_study_time / 60, 2),
        "avg_productivity": round(avg_productivity, 2),
        "homework_completion_rate": round(completion_rate, 2),
        "sessions_count": len(sessions),
        "homework_count": total_homework
    }

# =====================================================
# RECOMMANDATIONS IA
# =====================================================

@router.get("/recommendations/priority-tasks")
def get_priority_task_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Recommandations pour les tâches prioritaires"""
    
    # Devoirs urgents
    urgent_homework = db.query(Homework).filter(
        Homework.assigned_to == current_user.id,
        Homework.status == "pending",
        Homework.due_date <= datetime.utcnow() + timedelta(days=3)
    ).order_by(Homework.due_date.asc()).limit(5).all()
    
    recommendations = []
    
    for hw in urgent_homework:
        days_left = (hw.due_date - datetime.utcnow()).days
        recommendations.append({
            "type": "urgent_homework",
            "title": hw.title,
            "priority": "critical" if days_left <= 1 else "high",
            "days_left": days_left,
            "estimated_time": hw.estimated_time
        })
    
    return {
        "recommendations": recommendations,
        "total_urgent": len(recommendations)
    }

# =====================================================
# GAMIFICATION
# =====================================================

@router.get("/gamification/achievements")
def get_user_achievements(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les achievements de l'utilisateur"""
    
    achievements = []
    
    # Achievement: Étudiant assidu
    total_study_time = db.query(StudySession).filter(
        StudySession.user_id == current_user.id,
        StudySession.actual_duration.isnot(None)
    ).with_entities(func.sum(StudySession.actual_duration)).scalar() or 0
    
    if total_study_time >= 1000:  # 1000 minutes = ~16h
        achievements.append({
            "id": "study_master",
            "title": "Étudiant Assidu",
            "description": "A étudié plus de 16 heures",
            "icon": "📚",
            "unlocked": True,
            "progress": min(total_study_time / 1000 * 100, 100)
        })
    
    return {
        "achievements": achievements,
        "total_unlocked": len([a for a in achievements if a["unlocked"]]),
        "total_available": len(achievements)
    }

# =====================================================
# ROUTER SANS AUTHENTIFICATION (POUR TESTS)
# =====================================================

router_no_prefix = APIRouter(tags=["Organization Advanced Test"])

@router_no_prefix.get("/analytics/productivity")
def get_productivity_analytics_test(days: int = 30):
    """Test des analytics de productivité (sans auth)"""
    return {
        "study_time_hours": 12.5,
        "avg_productivity": 8.2,
        "homework_completion_rate": 85.0,
        "sessions_count": 15,
        "homework_count": 8
    }

@router_no_prefix.get("/recommendations/priority-tasks")
def get_priority_task_recommendations_test():
    """Test des recommandations (sans auth)"""
    return {
        "recommendations": [
            {
                "type": "urgent_homework",
                "title": "Devoir de mathématiques - Équations du second degré",
                "priority": "critical",
                "days_left": 1,
                "estimated_time": 120
            },
            {
                "type": "urgent_homework", 
                "title": "Rédaction d'histoire - Révolution française",
                "priority": "high",
                "days_left": 2,
                "estimated_time": 180
            },
            {
                "type": "study_session",
                "title": "Révision physique - Mécanique",
                "priority": "medium",
                "days_left": 3,
                "estimated_time": 90
            }
        ],
        "total_urgent": 3
    }

@router_no_prefix.get("/gamification/achievements")
def get_user_achievements_test():
    """Test des achievements (sans auth)"""
    return {
        "achievements": [
            {
                "id": "study_master",
                "title": "Étudiant Assidu",
                "description": "A étudié plus de 16 heures",
                "icon": "📚",
                "unlocked": True,
                "progress": 100
            },
            {
                "id": "homework_completer",
                "title": "Organisé",
                "description": "A terminé 10 devoirs à temps",
                "icon": "✅",
                "unlocked": True,
                "progress": 100
            },
            {
                "id": "streak_master",
                "title": "Régulier",
                "description": "A étudié 7 jours de suite",
                "icon": "🔥",
                "unlocked": False,
                "progress": 60
            }
        ],
        "total_unlocked": 2,
        "total_available": 3
    }

@router_no_prefix.get("/calendar/events")
def get_calendar_events_test(start_date: str = None, end_date: str = None):
    """Test des événements du calendrier (sans auth)"""
    return [
        {
            "id": "homework_1",
            "title": "Devoir de mathématiques",
            "start": "2024-01-20T14:00:00",
            "end": "2024-01-20T15:00:00",
            "type": "homework",
            "priority": "high",
            "color": "#EF4444"
        },
        {
            "id": "session_1",
            "title": "Session d'étude - Physique",
            "start": "2024-01-21T09:00:00",
            "end": "2024-01-21T11:00:00",
            "type": "study_session",
            "priority": "medium",
            "color": "#3B82F6"
        }
    ] 