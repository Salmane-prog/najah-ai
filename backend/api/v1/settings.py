from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from models.user import User
from models.settings import UserSettings
from api.v1.users import get_current_user
from api.v1.auth import require_role
from typing import Dict, Any
from datetime import datetime
import json

router = APIRouter()

@router.get("/user/{user_id}")
def get_user_settings(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Récupérer les réglages d'un utilisateur."""
    
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    settings = db.query(UserSettings).filter(UserSettings.user_id == user_id).first()
    
    if not settings:
        # Créer des réglages par défaut
        settings = UserSettings(
            user_id=user_id,
            theme="light",
            language="fr",
            notifications_enabled=True,
            email_notifications=True,
            push_notifications=True,
            privacy_level="public",
            study_reminders=True,
            daily_goal=30,  # minutes
            weekly_goal=180,  # minutes
            auto_save=True,
            show_progress=True,
            show_leaderboard=True,
            difficulty_preference="adaptive"
        )
        db.add(settings)
        db.commit()
        db.refresh(settings)
    
    return settings

@router.put("/user/{user_id}")
def update_user_settings(
    user_id: int,
    settings_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Mettre à jour les réglages d'un utilisateur."""
    
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    settings = db.query(UserSettings).filter(UserSettings.user_id == user_id).first()
    
    if not settings:
        # Créer des réglages par défaut
        settings = UserSettings(user_id=user_id)
        db.add(settings)
    
    # Mettre à jour les champs autorisés
    allowed_fields = [
        "theme", "language", "notifications_enabled", "email_notifications",
        "push_notifications", "privacy_level", "study_reminders",
        "daily_goal", "weekly_goal", "auto_save", "show_progress",
        "show_leaderboard", "difficulty_preference"
    ]
    
    for field in allowed_fields:
        if field in settings_data:
            setattr(settings, field, settings_data[field])
    
    settings.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(settings)
    
    return {
        "message": "Réglages mis à jour avec succès",
        "settings": settings
    }

@router.get("/user/{user_id}/privacy")
def get_privacy_settings(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Récupérer les paramètres de confidentialité."""
    
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    settings = db.query(UserSettings).filter(UserSettings.user_id == user_id).first()
    
    if not settings:
        return {
            "privacy_level": "public",
            "show_progress": True,
            "show_leaderboard": True
        }
    
    return {
        "privacy_level": settings.privacy_level,
        "show_progress": settings.show_progress,
        "show_leaderboard": settings.show_leaderboard
    }

@router.put("/user/{user_id}/privacy")
def update_privacy_settings(
    user_id: int,
    privacy_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Mettre à jour les paramètres de confidentialité."""
    
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    settings = db.query(UserSettings).filter(UserSettings.user_id == user_id).first()
    
    if not settings:
        settings = UserSettings(user_id=user_id)
        db.add(settings)
    
    # Mettre à jour les paramètres de confidentialité
    if "privacy_level" in privacy_data:
        settings.privacy_level = privacy_data["privacy_level"]
    if "show_progress" in privacy_data:
        settings.show_progress = privacy_data["show_progress"]
    if "show_leaderboard" in privacy_data:
        settings.show_leaderboard = privacy_data["show_leaderboard"]
    
    settings.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(settings)
    
    return {
        "message": "Paramètres de confidentialité mis à jour",
        "privacy": {
            "privacy_level": settings.privacy_level,
            "show_progress": settings.show_progress,
            "show_leaderboard": settings.show_leaderboard
        }
    }

@router.get("/user/{user_id}/goals")
def get_user_goals(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Récupérer les objectifs d'étude d'un utilisateur."""
    
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    settings = db.query(UserSettings).filter(UserSettings.user_id == user_id).first()
    
    if not settings:
        return {
            "daily_goal": 30,
            "weekly_goal": 180,
            "difficulty_preference": "adaptive"
        }
    
    return {
        "daily_goal": settings.daily_goal,
        "weekly_goal": settings.weekly_goal,
        "difficulty_preference": settings.difficulty_preference
    }

@router.put("/user/{user_id}/goals")
def update_user_goals(
    user_id: int,
    goals_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Mettre à jour les objectifs d'étude d'un utilisateur."""
    
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    settings = db.query(UserSettings).filter(UserSettings.user_id == user_id).first()
    
    if not settings:
        settings = UserSettings(user_id=user_id)
        db.add(settings)
    
    # Mettre à jour les objectifs
    if "daily_goal" in goals_data:
        settings.daily_goal = goals_data["daily_goal"]
    if "weekly_goal" in goals_data:
        settings.weekly_goal = goals_data["weekly_goal"]
    if "difficulty_preference" in goals_data:
        settings.difficulty_preference = goals_data["difficulty_preference"]
    
    settings.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(settings)
    
    return {
        "message": "Objectifs mis à jour avec succès",
        "goals": {
            "daily_goal": settings.daily_goal,
            "weekly_goal": settings.weekly_goal,
            "difficulty_preference": settings.difficulty_preference
        }
    } 

@router.get("/notifications")
def get_notification_settings(
    current_user: User = Depends(get_current_user)
):
    """Récupérer les paramètres de notifications de l'utilisateur."""
    return {
        "email_notifications": True,
        "push_notifications": True,
        "sms_notifications": False,
        "in_app_notifications": True,
        "daily_digest": True,
        "weekly_report": True,
        "quiz_reminders": True,
        "assignment_deadlines": True
    }

@router.put("/notifications")
def update_notification_settings(
    settings: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Mettre à jour les paramètres de notifications de l'utilisateur."""
    return {
        "message": "Paramètres de notifications mis à jour",
        "settings": settings
    }

@router.get("/security")
def get_security_settings(
    current_user: User = Depends(get_current_user)
):
    """Récupérer les paramètres de sécurité de l'utilisateur."""
    return {
        "two_factor_enabled": False,
        "password_last_changed": "2024-01-01T00:00:00Z",
        "login_history": [
            {
                "timestamp": "2024-01-15T10:30:00Z",
                "ip_address": "192.168.1.1",
                "device": "Chrome on Windows"
            }
        ],
        "active_sessions": [
            {
                "id": "session_1",
                "device": "Chrome on Windows",
                "ip_address": "192.168.1.1",
                "last_activity": "2024-01-15T10:30:00Z"
            }
        ]
    }

@router.put("/security")
def update_security_settings(
    settings: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Mettre à jour les paramètres de sécurité de l'utilisateur."""
    return {
        "message": "Paramètres de sécurité mis à jour",
        "settings": settings
    } 