from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
import asyncio
import json

from core.database import SessionLocal
from api.v1.users import get_current_user
from models.user import User, UserRole
from models.organization import Homework, StudySession, Reminder, LearningGoal
from models.notification import Notification

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(tags=["Auto Notifications"])

# =====================================================
# SCHÉMAS PYDANTIC
# =====================================================

class NotificationCreate(BaseModel):
    user_id: int
    title: str
    message: str
    type: str  # homework, goal, reminder, achievement
    priority: str = "normal"  # low, normal, high, urgent
    data: Optional[dict] = None

class NotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    type: str
    priority: str
    is_read: bool
    created_at: datetime
    data: Optional[dict]
    
    class Config:
        from_attributes = True

# =====================================================
# FONCTIONS DE NOTIFICATION AUTOMATIQUE
# =====================================================

async def check_homework_deadlines(db: Session):
    """Vérifier les deadlines des devoirs et envoyer des notifications"""
    
    # Devoirs en retard
    overdue_homework = db.query(Homework).filter(
        Homework.due_date < datetime.utcnow(),
        Homework.status.in_(["pending", "in_progress"])
    ).all()
    
    for homework in overdue_homework:
        # Créer une notification urgente
        notification = Notification(
            user_id=homework.assigned_to,
            title="Devoir en retard !",
            message=f"Le devoir '{homework.title}' était à rendre le {homework.due_date.strftime('%d/%m/%Y')}",
            type="homework",
            priority="urgent",
            data={"homework_id": homework.id, "due_date": homework.due_date.isoformat()}
        )
        db.add(notification)
    
    # Devoirs à rendre dans les 24h
    tomorrow = datetime.utcnow() + timedelta(days=1)
    urgent_homework = db.query(Homework).filter(
        Homework.due_date <= tomorrow,
        Homework.due_date > datetime.utcnow(),
        Homework.status.in_(["pending", "in_progress"])
    ).all()
    
    for homework in urgent_homework:
        notification = Notification(
            user_id=homework.assigned_to,
            title="Devoir à rendre demain",
            message=f"Le devoir '{homework.title}' est à rendre le {homework.due_date.strftime('%d/%m/%Y')}",
            type="homework",
            priority="high",
            data={"homework_id": homework.id, "due_date": homework.due_date.isoformat()}
        )
        db.add(notification)
    
    db.commit()

async def check_goal_deadlines(db: Session):
    """Vérifier les deadlines des objectifs et envoyer des notifications"""
    
    # Objectifs avec peu de temps restant
    week_from_now = datetime.utcnow() + timedelta(days=7)
    urgent_goals = db.query(LearningGoal).filter(
        LearningGoal.target_date <= week_from_now,
        LearningGoal.target_date > datetime.utcnow(),
        LearningGoal.status == "active"
    ).all()
    
    for goal in urgent_goals:
        days_left = (goal.target_date - datetime.utcnow()).days
        priority = "urgent" if days_left <= 2 else "high"
        
        notification = Notification(
            user_id=goal.user_id,
            title=f"Objectif à terminer dans {days_left} jours",
            message=f"L'objectif '{goal.title}' doit être terminé le {goal.target_date.strftime('%d/%m/%Y')}",
            type="goal",
            priority=priority,
            data={"goal_id": goal.id, "target_date": goal.target_date.isoformat(), "progress": goal.progress}
        )
        db.add(notification)
    
    db.commit()

async def check_achievements(db: Session):
    """Vérifier les achievements et envoyer des notifications"""
    
    # Calculer les achievements basés sur les performances
    students = db.query(User).filter(User.role == UserRole.student).all()
    
    for student in students:
        # Achievement pour les devoirs terminés
        completed_homework = db.query(Homework).filter(
            Homework.assigned_to == student.id,
            Homework.status == "completed"
        ).count()
        
        if completed_homework >= 10:
            notification = Notification(
                user_id=student.id,
                title="Achievement débloqué !",
                message="Vous avez terminé 10 devoirs. Félicitations !",
                type="achievement",
                priority="normal",
                data={"achievement_type": "homework_completion", "count": completed_homework}
            )
            db.add(notification)
        
        # Achievement pour le temps d'étude
        study_sessions = db.query(StudySession).filter(
            StudySession.user_id == student.id,
            StudySession.status == "completed",
            StudySession.start_time >= datetime.utcnow() - timedelta(days=7)
        ).all()
        
        total_study_time = sum(session.duration or 0 for session in study_sessions)
        
        if total_study_time >= 300:  # 5 heures par semaine
            notification = Notification(
                user_id=student.id,
                title="Étudiant assidu !",
                message="Vous avez étudié plus de 5 heures cette semaine. Excellent travail !",
                type="achievement",
                priority="normal",
                data={"achievement_type": "study_time", "hours": total_study_time / 60}
            )
            db.add(notification)
    
    db.commit()

async def check_reminders(db: Session):
    """Vérifier les rappels et envoyer des notifications"""
    
    # Rappels actifs qui arrivent à échéance
    now = datetime.utcnow()
    active_reminders = db.query(Reminder).filter(
        Reminder.is_active == True,
        Reminder.reminder_time <= now + timedelta(hours=1),
        Reminder.reminder_time > now - timedelta(hours=1)
    ).all()
    
    for reminder in active_reminders:
        notification = Notification(
            user_id=reminder.user_id,
            title="Rappel",
            message=reminder.title,
            type="reminder",
            priority="normal",
            data={"reminder_id": reminder.id, "reminder_time": reminder.reminder_time.isoformat()}
        )
        db.add(notification)
    
    db.commit()

# =====================================================
# ENDPOINTS POUR LES NOTIFICATIONS
# =====================================================

@router.get("/notifications", response_model=List[NotificationResponse])
def get_user_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    unread_only: bool = False
):
    """Récupérer les notifications de l'utilisateur"""
    
    query = db.query(Notification).filter(Notification.user_id == current_user.id)
    
    if unread_only:
        query = query.filter(Notification.is_read == False)
    
    notifications = query.order_by(Notification.created_at.desc()).limit(50).all()
    return notifications

@router.put("/notifications/{notification_id}/read")
def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Marquer une notification comme lue"""
    
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification non trouvée"
        )
    
    notification.is_read = True
    db.commit()
    
    return {"message": "Notification marquée comme lue"}

@router.put("/notifications/read-all")
def mark_all_notifications_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Marquer toutes les notifications comme lues"""
    
    db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    ).update({"is_read": True})
    
    db.commit()
    
    return {"message": "Toutes les notifications marquées comme lues"}

@router.get("/notifications/unread-count")
def get_unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer le nombre de notifications non lues"""
    
    count = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    ).count()
    
    return {"unread_count": count}

# =====================================================
# ENDPOINTS POUR DÉCLENCHER LES VÉRIFICATIONS
# =====================================================

@router.post("/trigger-checks")
async def trigger_notification_checks(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Déclencher toutes les vérifications de notifications"""
    
    if current_user.role != UserRole.teacher:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seuls les professeurs peuvent déclencher les vérifications"
        )
    
    # Ajouter les tâches en arrière-plan
    background_tasks.add_task(check_homework_deadlines, db)
    background_tasks.add_task(check_goal_deadlines, db)
    background_tasks.add_task(check_achievements, db)
    background_tasks.add_task(check_reminders, db)
    
    return {"message": "Vérifications de notifications déclenchées"}

@router.post("/send-custom-notification")
def send_custom_notification(
    notification_data: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Envoyer une notification personnalisée"""
    
    if current_user.role != UserRole.teacher:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seuls les professeurs peuvent envoyer des notifications"
        )
    
    notification = Notification(
        user_id=notification_data.user_id,
        title=notification_data.title,
        message=notification_data.message,
        type=notification_data.type,
        priority=notification_data.priority,
        data=notification_data.data
    )
    
    db.add(notification)
    db.commit()
    db.refresh(notification)
    
    return {"message": "Notification envoyée", "notification_id": notification.id}

# =====================================================
# ENDPOINTS POUR LES STATISTIQUES DE NOTIFICATIONS
# =====================================================

@router.get("/notifications/stats")
def get_notification_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les statistiques des notifications"""
    
    total_notifications = db.query(Notification).filter(
        Notification.user_id == current_user.id
    ).count()
    
    unread_notifications = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    ).count()
    
    # Notifications par type
    notifications_by_type = db.query(
        Notification.type,
        db.func.count(Notification.id).label('count')
    ).filter(
        Notification.user_id == current_user.id
    ).group_by(Notification.type).all()
    
    # Notifications par priorité
    notifications_by_priority = db.query(
        Notification.priority,
        db.func.count(Notification.id).label('count')
    ).filter(
        Notification.user_id == current_user.id
    ).group_by(Notification.priority).all()
    
    return {
        "total_notifications": total_notifications,
        "unread_notifications": unread_notifications,
        "read_rate": round((total_notifications - unread_notifications) / total_notifications * 100, 2) if total_notifications > 0 else 0,
        "by_type": {nt.type: nt.count for nt in notifications_by_type},
        "by_priority": {np.priority: np.count for np in notifications_by_priority}
    } 