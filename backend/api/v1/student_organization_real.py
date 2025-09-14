from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel

from core.database import SessionLocal
from api.v1.users import get_current_user
from models.user import User, UserRole
from models.organization import Homework, StudySession, Reminder, LearningGoal
from models.class_group import ClassGroup, ClassStudent

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(tags=["Student Organization Real Data"])

# =====================================================
# SCHÉMAS PYDANTIC
# =====================================================

class HomeworkReal(BaseModel):
    id: int
    title: str
    description: str
    subject: str
    class_id: int
    assigned_by: int
    assigned_to: int
    due_date: datetime
    status: str
    priority: str
    estimated_time: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True

class StudySessionReal(BaseModel):
    id: int
    user_id: int
    title: str
    subject: str
    start_time: datetime
    end_time: Optional[datetime]
    duration: Optional[int]
    goals: List[str]
    notes: Optional[str]
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class ReminderReal(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    reminder_time: datetime
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class LearningGoalReal(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    subject: str
    target_date: datetime
    progress: float
    status: str
    milestones: List[dict]
    created_at: datetime
    
    class Config:
        from_attributes = True

# =====================================================
# ENDPOINTS POUR LES DEVOIRS RÉELS
# =====================================================

@router.get("/homework", response_model=List[HomeworkReal])
def get_student_homework(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    status_filter: Optional[str] = None
):
    """Récupérer les devoirs assignés à l'étudiant"""
    
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès non autorisé"
        )
    
    query = db.query(Homework).filter(Homework.assigned_to == current_user.id)
    
    if status_filter:
        query = query.filter(Homework.status == status_filter)
    
    # Mettre à jour le statut des devoirs en retard
    overdue_homeworks = query.filter(
        Homework.due_date < datetime.utcnow(),
        Homework.status != "completed"
    ).all()
    
    for homework in overdue_homeworks:
        homework.status = "overdue"
    
    db.commit()
    
    homeworks = query.order_by(Homework.due_date.asc()).all()
    return homeworks

@router.put("/homework/{homework_id}/complete")
def complete_homework(
    homework_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Marquer un devoir comme terminé"""
    
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès non autorisé"
        )
    
    homework = db.query(Homework).filter(
        Homework.id == homework_id,
        Homework.assigned_to == current_user.id
    ).first()
    
    if not homework:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Devoir non trouvé"
        )
    
    homework.status = "completed"
    db.commit()
    
    return {"message": "Devoir marqué comme terminé"}

# =====================================================
# ENDPOINTS POUR LES SESSIONS D'ÉTUDE RÉELLES
# =====================================================

@router.get("/study-sessions", response_model=List[StudySessionReal])
def get_student_study_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    days: int = 30
):
    """Récupérer les sessions d'étude de l'étudiant"""
    
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès non autorisé"
        )
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    sessions = db.query(StudySession).filter(
        StudySession.user_id == current_user.id,
        StudySession.start_time >= start_date
    ).order_by(StudySession.start_time.desc()).all()
    
    return sessions

@router.post("/study-sessions", response_model=StudySessionReal)
def create_study_session(
    session_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer une nouvelle session d'étude"""
    
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès non autorisé"
        )
    
    new_session = StudySession(
        user_id=current_user.id,
        title=session_data.get("title"),
        subject=session_data.get("subject"),
        start_time=datetime.utcnow(),
        goals=session_data.get("goals", []),
        notes=session_data.get("notes"),
        status="active"
    )
    
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    
    return new_session

@router.put("/study-sessions/{session_id}/end")
def end_study_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Terminer une session d'étude"""
    
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès non autorisé"
        )
    
    session = db.query(StudySession).filter(
        StudySession.id == session_id,
        StudySession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session non trouvée"
        )
    
    session.end_time = datetime.utcnow()
    session.duration = int((session.end_time - session.start_time).total_seconds() / 60)
    session.status = "completed"
    
    db.commit()
    
    return {"message": "Session terminée", "duration": session.duration}

# =====================================================
# ENDPOINTS POUR LES RAPPELS RÉELS
# =====================================================

@router.get("/reminders", response_model=List[ReminderReal])
def get_student_reminders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les rappels de l'étudiant"""
    
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès non autorisé"
        )
    
    reminders = db.query(Reminder).filter(
        Reminder.user_id == current_user.id,
        Reminder.is_active == True
    ).order_by(Reminder.reminder_time.asc()).all()
    
    return reminders

@router.post("/reminders", response_model=ReminderReal)
def create_reminder(
    reminder_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer un nouveau rappel"""
    
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès non autorisé"
        )
    
    new_reminder = Reminder(
        user_id=current_user.id,
        title=reminder_data.get("title"),
        description=reminder_data.get("description"),
        reminder_time=reminder_data.get("reminder_time"),
        is_active=True
    )
    
    db.add(new_reminder)
    db.commit()
    db.refresh(new_reminder)
    
    return new_reminder

@router.put("/reminders/{reminder_id}/toggle")
def toggle_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Activer/désactiver un rappel"""
    
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès non autorisé"
        )
    
    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.user_id == current_user.id
    ).first()
    
    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rappel non trouvé"
        )
    
    reminder.is_active = not reminder.is_active
    db.commit()
    
    return {"message": f"Rappel {'activé' if reminder.is_active else 'désactivé'}"}

# =====================================================
# ENDPOINTS POUR LES OBJECTIFS RÉELS
# =====================================================

@router.get("/learning-goals", response_model=List[LearningGoalReal])
def get_student_learning_goals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les objectifs d'apprentissage de l'étudiant"""
    
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès non autorisé"
        )
    
    goals = db.query(LearningGoal).filter(
        LearningGoal.user_id == current_user.id
    ).order_by(LearningGoal.target_date.asc()).all()
    
    return goals

@router.put("/learning-goals/{goal_id}/milestone/{milestone_id}")
def complete_milestone(
    goal_id: int,
    milestone_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Marquer une étape comme terminée"""
    
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès non autorisé"
        )
    
    goal = db.query(LearningGoal).filter(
        LearningGoal.id == goal_id,
        LearningGoal.user_id == current_user.id
    ).first()
    
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Objectif non trouvé"
        )
    
    # Mettre à jour la progression
    if goal.milestones:
        for milestone in goal.milestones:
            if milestone.get("id") == milestone_id:
                milestone["completed"] = True
                break
        
        # Calculer la nouvelle progression
        completed_milestones = sum(1 for m in goal.milestones if m.get("completed", False))
        total_milestones = len(goal.milestones)
        goal.progress = completed_milestones / total_milestones if total_milestones > 0 else 0
        
        # Mettre à jour le statut si terminé
        if goal.progress >= 1.0:
            goal.status = "completed"
    
    db.commit()
    
    return {"message": "Étape terminée", "progress": goal.progress}

# =====================================================
# ENDPOINTS POUR LES ANALYTICS RÉELS
# =====================================================

@router.get("/analytics/productivity")
def get_productivity_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    days: int = 30
):
    """Récupérer les analytics de productivité réels"""
    
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès non autorisé"
        )
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Calculer le temps d'étude total
    study_sessions = db.query(StudySession).filter(
        StudySession.user_id == current_user.id,
        StudySession.start_time >= start_date,
        StudySession.status == "completed"
    ).all()
    
    total_study_time = sum(session.duration or 0 for session in study_sessions)
    study_time_hours = total_study_time / 60
    
    # Calculer le taux de completion des devoirs
    total_homework = db.query(Homework).filter(
        Homework.assigned_to == current_user.id,
        Homework.created_at >= start_date
    ).count()
    
    completed_homework = db.query(Homework).filter(
        Homework.assigned_to == current_user.id,
        Homework.created_at >= start_date,
        Homework.status == "completed"
    ).count()
    
    homework_completion_rate = (completed_homework / total_homework * 100) if total_homework > 0 else 0
    
    # Calculer la productivité moyenne (basée sur les sessions et devoirs)
    sessions_count = len(study_sessions)
    avg_productivity = min(10, (study_time_hours * 2 + homework_completion_rate / 10) / 2)
    
    return {
        "study_time_hours": round(study_time_hours, 1),
        "avg_productivity": round(avg_productivity, 1),
        "homework_completion_rate": round(homework_completion_rate, 1),
        "sessions_count": sessions_count,
        "total_homework": total_homework,
        "completed_homework": completed_homework
    }

@router.get("/analytics/progress")
def get_progress_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les analytics de progression réels"""
    
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès non autorisé"
        )
    
    # Progression des objectifs
    goals = db.query(LearningGoal).filter(
        LearningGoal.user_id == current_user.id
    ).all()
    
    total_goals = len(goals)
    active_goals = len([g for g in goals if g.status == "active"])
    completed_goals = len([g for g in goals if g.status == "completed"])
    avg_progress = sum(g.progress for g in goals) / len(goals) if goals else 0
    
    # Statistiques par matière
    subjects = {}
    for goal in goals:
        if goal.subject not in subjects:
            subjects[goal.subject] = {"goals": 0, "progress": 0}
        subjects[goal.subject]["goals"] += 1
        subjects[goal.subject]["progress"] += goal.progress
    
    for subject in subjects:
        subjects[subject]["avg_progress"] = subjects[subject]["progress"] / subjects[subject]["goals"]
    
    return {
        "total_goals": total_goals,
        "active_goals": active_goals,
        "completed_goals": completed_goals,
        "average_progress": round(avg_progress * 100, 2),
        "subjects_progress": subjects
    }

# =====================================================
# ENDPOINTS POUR LES RECOMMANDATIONS RÉELLES
# =====================================================

@router.get("/recommendations/priority-tasks")
def get_priority_task_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Générer des recommandations basées sur les vraies données"""
    
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès non autorisé"
        )
    
    # Devoirs urgents
    urgent_homework = db.query(Homework).filter(
        Homework.assigned_to == current_user.id,
        Homework.status.in_(["pending", "in_progress"]),
        Homework.due_date <= datetime.utcnow() + timedelta(days=3)
    ).order_by(Homework.due_date.asc()).limit(5).all()
    
    # Objectifs avec peu de temps restant
    urgent_goals = db.query(LearningGoal).filter(
        LearningGoal.user_id == current_user.id,
        LearningGoal.status == "active",
        LearningGoal.target_date <= datetime.utcnow() + timedelta(days=7)
    ).order_by(LearningGoal.target_date.asc()).limit(3).all()
    
    recommendations = []
    
    # Ajouter les devoirs urgents
    for homework in urgent_homework:
        days_left = (homework.due_date - datetime.utcnow()).days
        priority = "critical" if days_left <= 1 else "high" if days_left <= 3 else "medium"
        
        recommendations.append({
            "id": f"homework_{homework.id}",
            "title": homework.title,
            "description": homework.description,
            "type": "homework",
            "priority": priority,
            "due_date": homework.due_date.isoformat(),
            "days_left": days_left
        })
    
    # Ajouter les objectifs urgents
    for goal in urgent_goals:
        days_left = (goal.target_date - datetime.utcnow()).days
        priority = "critical" if days_left <= 3 else "high" if days_left <= 7 else "medium"
        
        recommendations.append({
            "id": f"goal_{goal.id}",
            "title": goal.title,
            "description": goal.description,
            "type": "learning_goal",
            "priority": priority,
            "due_date": goal.target_date.isoformat(),
            "days_left": days_left,
            "progress": goal.progress
        })
    
    # Trier par priorité et date
    recommendations.sort(key=lambda x: (x["priority"] == "critical", x["days_left"]))
    
    return {
        "recommendations": recommendations[:5],
        "total_urgent": len([r for r in recommendations if r["priority"] == "critical"]),
        "total_high": len([r for r in recommendations if r["priority"] == "high"])
    }

# =====================================================
# ROUTER SANS PREFIX POUR COMPATIBILITÉ FRONTEND
# =====================================================

# Router sans prefix pour les appels directs du frontend
router_no_prefix = APIRouter(tags=["Student Organization Real Data - No Prefix"])

# Endpoint de test sans authentification pour déboguer
@router_no_prefix.get("/homework/test", response_model=List[HomeworkReal])
def get_student_homework_test(
    db: Session = Depends(get_db),
    status_filter: Optional[str] = None
):
    """Récupérer les devoirs assignés à l'étudiant (test sans auth)"""
    
    # Récupérer tous les devoirs pour l'étudiant ID 4 (Salmane)
    query = db.query(Homework).filter(Homework.assigned_to == 4)
    
    if status_filter:
        query = query.filter(Homework.status == status_filter)
    
    homeworks = query.order_by(Homework.due_date.asc()).all()
    return homeworks

# Copie des endpoints principaux pour compatibilité sans prefix
@router_no_prefix.get("/homework", response_model=List[HomeworkReal])
def get_student_homework_no_prefix(
    db: Session = Depends(get_db),
    status_filter: Optional[str] = None
):
    """Récupérer les devoirs assignés à l'étudiant (sans prefix)"""
    
    # Temporairement, utiliser l'étudiant ID 4 (Salmane) sans vérification d'auth
    # TODO: Réactiver l'authentification une fois que le frontend fonctionne
    student_id = 4  # current_user.id if current_user else 4
    
    query = db.query(Homework).filter(Homework.assigned_to == student_id)
    
    if status_filter:
        query = query.filter(Homework.status == status_filter)
    
    homeworks = query.order_by(Homework.due_date.asc()).all()
    return homeworks

@router_no_prefix.put("/homework/{homework_id}/complete")
def complete_homework_no_prefix(
    homework_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Marquer un devoir comme terminé (sans prefix)"""
    
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès non autorisé"
        )
    
    homework = db.query(Homework).filter(
        Homework.id == homework_id,
        Homework.assigned_to == current_user.id
    ).first()
    
    if not homework:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Devoir non trouvé"
        )
    
    homework.status = "completed"
    db.commit()
    
    return {"message": "Devoir marqué comme terminé"} 