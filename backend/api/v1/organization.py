from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import json

from core.database import SessionLocal
from api.v1.users import get_current_user
from models.user import User
from models.organization import Homework, StudySession, Reminder, LearningGoal
from models.calendar import CalendarEvent, StudyTimeStats
from models.class_group import ClassGroup
from schemas.organization import (
    HomeworkCreate, HomeworkResponse, HomeworkUpdate,
    StudySessionCreate, StudySessionResponse, StudySessionUpdate,
    ReminderCreate, ReminderResponse, ReminderUpdate,
    LearningGoalCreate, LearningGoalResponse, LearningGoalUpdate
)
from schemas.calendar import (
    CalendarEventCreate, CalendarEventResponse, CalendarEventUpdate,
    StudyTimeStatsCreate, StudyTimeStatsResponse, StudyTimeStatsUpdate,
    OrganizationStatsResponse, StudyTimeStatsSummaryResponse
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/organization", tags=["Organization"])

# =====================================================
# ENDPOINTS POUR LES DEVOIRS
# =====================================================

@router.post("/homework", response_model=HomeworkResponse)
def create_homework(
    homework: HomeworkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer un nouveau devoir"""
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="Seuls les enseignants peuvent créer des devoirs")
    
    # Vérifier que la classe existe si spécifiée
    if homework.class_id:
        class_group = db.query(ClassGroup).filter(ClassGroup.id == homework.class_id).first()
        if not class_group:
            raise HTTPException(status_code=404, detail="Classe non trouvée")
    
    db_homework = Homework(
        **homework.dict(),
        assigned_by=current_user.id
    )
    db.add(db_homework)
    db.commit()
    db.refresh(db_homework)
    return db_homework

@router.get("/homework", response_model=List[HomeworkResponse])
def get_homework(
    assigned_to: Optional[int] = None,
    assigned_by: Optional[int] = None,
    status: Optional[str] = None,
    subject: Optional[str] = None,
    due_date_from: Optional[datetime] = None,
    due_date_to: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les devoirs avec filtres"""
    query = db.query(Homework)
    
    # Filtres selon le rôle de l'utilisateur
    if current_user.role == "student":
        query = query.filter(Homework.assigned_to == current_user.id)
    elif current_user.role == "teacher":
        query = query.filter(Homework.assigned_by == current_user.id)
    
    # Filtres optionnels
    if assigned_to:
        query = query.filter(Homework.assigned_to == assigned_to)
    if assigned_by:
        query = query.filter(Homework.assigned_by == assigned_by)
    if status:
        query = query.filter(Homework.status == status)
    if subject:
        query = query.filter(Homework.subject == subject)
    if due_date_from:
        query = query.filter(Homework.due_date >= due_date_from)
    if due_date_to:
        query = query.filter(Homework.due_date <= due_date_to)
    
    return query.order_by(Homework.due_date.asc()).all()

@router.get("/homework/{homework_id}", response_model=HomeworkResponse)
def get_homework_by_id(
    homework_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer un devoir spécifique"""
    homework = db.query(Homework).filter(Homework.id == homework_id).first()
    if not homework:
        raise HTTPException(status_code=404, detail="Devoir non trouvé")
    
    # Vérifier les permissions
    if current_user.role == "student" and homework.assigned_to != current_user.id:
        raise HTTPException(status_code=403, detail="Permission refusée")
    elif current_user.role == "teacher" and homework.assigned_by != current_user.id:
        raise HTTPException(status_code=403, detail="Permission refusée")
    
    return homework

@router.put("/homework/{homework_id}", response_model=HomeworkResponse)
def update_homework(
    homework_id: int,
    homework_update: HomeworkUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mettre à jour un devoir"""
    homework = db.query(Homework).filter(Homework.id == homework_id).first()
    if not homework:
        raise HTTPException(status_code=404, detail="Devoir non trouvé")
    
    # Vérifier les permissions
    if current_user.role == "student":
        if homework.assigned_to != current_user.id:
            raise HTTPException(status_code=403, detail="Permission refusée")
        # Les étudiants ne peuvent modifier que certains champs
        allowed_fields = ["status", "actual_time", "notes"]
        update_data = {k: v for k, v in homework_update.dict(exclude_unset=True).items() if k in allowed_fields}
    else:
        update_data = homework_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(homework, field, value)
    
    db.commit()
    db.refresh(homework)
    return homework

@router.delete("/homework/{homework_id}")
def delete_homework(
    homework_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Supprimer un devoir"""
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="Permission refusée")
    
    homework = db.query(Homework).filter(Homework.id == homework_id).first()
    if not homework:
        raise HTTPException(status_code=404, detail="Devoir non trouvé")
    
    if homework.assigned_by != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Permission refusée")
    
    db.delete(homework)
    db.commit()
    return {"message": "Devoir supprimé"}

# =====================================================
# ENDPOINTS POUR LES SESSIONS D'ÉTUDE
# =====================================================

@router.post("/study-sessions", response_model=StudySessionResponse)
def create_study_session(
    session: StudySessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer une nouvelle session d'étude"""
    db_session = StudySession(
        **session.dict(),
        user_id=current_user.id
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@router.get("/study-sessions", response_model=List[StudySessionResponse])
def get_study_sessions(
    subject: Optional[str] = None,
    status: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les sessions d'étude de l'utilisateur"""
    query = db.query(StudySession).filter(StudySession.user_id == current_user.id)
    
    if subject:
        query = query.filter(StudySession.subject == subject)
    if status:
        query = query.filter(StudySession.status == status)
    if date_from:
        query = query.filter(StudySession.start_time >= date_from)
    if date_to:
        query = query.filter(StudySession.start_time <= date_to)
    
    return query.order_by(StudySession.start_time.desc()).all()

@router.get("/study-sessions/{session_id}", response_model=StudySessionResponse)
def get_study_session_by_id(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer une session d'étude spécifique"""
    session = db.query(StudySession).filter(
        StudySession.id == session_id,
        StudySession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session d'étude non trouvée")
    
    return session

@router.put("/study-sessions/{session_id}", response_model=StudySessionResponse)
def update_study_session(
    session_id: int,
    session_update: StudySessionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mettre à jour une session d'étude"""
    session = db.query(StudySession).filter(
        StudySession.id == session_id,
        StudySession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session d'étude non trouvée")
    
    for field, value in session_update.dict(exclude_unset=True).items():
        setattr(session, field, value)
    
    db.commit()
    db.refresh(session)
    return session

@router.delete("/study-sessions/{session_id}")
def delete_study_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Supprimer une session d'étude"""
    session = db.query(StudySession).filter(
        StudySession.id == session_id,
        StudySession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session d'étude non trouvée")
    
    db.delete(session)
    db.commit()
    return {"message": "Session d'étude supprimée"}

# =====================================================
# ENDPOINTS POUR LES RAPPELS
# =====================================================

@router.post("/reminders", response_model=ReminderResponse)
def create_reminder(
    reminder: ReminderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer un nouveau rappel"""
    db_reminder = Reminder(
        **reminder.dict(),
        user_id=current_user.id
    )
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)
    return db_reminder

@router.get("/reminders", response_model=List[ReminderResponse])
def get_reminders(
    is_active: Optional[bool] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les rappels de l'utilisateur"""
    query = db.query(Reminder).filter(Reminder.user_id == current_user.id)
    
    if is_active is not None:
        query = query.filter(Reminder.is_active == is_active)
    if date_from:
        query = query.filter(Reminder.reminder_time >= date_from)
    if date_to:
        query = query.filter(Reminder.reminder_time <= date_to)
    
    return query.order_by(Reminder.reminder_time.asc()).all()

@router.get("/reminders/{reminder_id}", response_model=ReminderResponse)
def get_reminder_by_id(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer un rappel spécifique"""
    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.user_id == current_user.id
    ).first()
    
    if not reminder:
        raise HTTPException(status_code=404, detail="Rappel non trouvé")
    
    return reminder

@router.put("/reminders/{reminder_id}", response_model=ReminderResponse)
def update_reminder(
    reminder_id: int,
    reminder_update: ReminderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mettre à jour un rappel"""
    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.user_id == current_user.id
    ).first()
    
    if not reminder:
        raise HTTPException(status_code=404, detail="Rappel non trouvé")
    
    for field, value in reminder_update.dict(exclude_unset=True).items():
        setattr(reminder, field, value)
    
    db.commit()
    db.refresh(reminder)
    return reminder

@router.delete("/reminders/{reminder_id}")
def delete_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Supprimer un rappel"""
    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.user_id == current_user.id
    ).first()
    
    if not reminder:
        raise HTTPException(status_code=404, detail="Rappel non trouvé")
    
    db.delete(reminder)
    db.commit()
    return {"message": "Rappel supprimé"}

# =====================================================
# ENDPOINTS POUR LES OBJECTIFS D'APPRENTISSAGE
# =====================================================

@router.post("/learning-goals", response_model=LearningGoalResponse)
def create_learning_goal(
    goal: LearningGoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer un nouvel objectif d'apprentissage"""
    db_goal = LearningGoal(
        **goal.dict(),
        user_id=current_user.id
    )
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

@router.get("/learning-goals", response_model=List[LearningGoalResponse])
def get_learning_goals(
    subject: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les objectifs d'apprentissage de l'utilisateur"""
    query = db.query(LearningGoal).filter(LearningGoal.user_id == current_user.id)
    
    if subject:
        query = query.filter(LearningGoal.subject == subject)
    if status:
        query = query.filter(LearningGoal.status == status)
    
    return query.order_by(LearningGoal.target_date.asc()).all()

@router.get("/learning-goals/{goal_id}", response_model=LearningGoalResponse)
def get_learning_goal_by_id(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer un objectif d'apprentissage spécifique"""
    goal = db.query(LearningGoal).filter(
        LearningGoal.id == goal_id,
        LearningGoal.user_id == current_user.id
    ).first()
    
    if not goal:
        raise HTTPException(status_code=404, detail="Objectif d'apprentissage non trouvé")
    
    return goal

@router.put("/learning-goals/{goal_id}", response_model=LearningGoalResponse)
def update_learning_goal(
    goal_id: int,
    goal_update: LearningGoalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mettre à jour un objectif d'apprentissage"""
    goal = db.query(LearningGoal).filter(
        LearningGoal.id == goal_id,
        LearningGoal.user_id == current_user.id
    ).first()
    
    if not goal:
        raise HTTPException(status_code=404, detail="Objectif d'apprentissage non trouvé")
    
    for field, value in goal_update.dict(exclude_unset=True).items():
        setattr(goal, field, value)
    
    db.commit()
    db.refresh(goal)
    return goal

@router.delete("/learning-goals/{goal_id}")
def delete_learning_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Supprimer un objectif d'apprentissage"""
    goal = db.query(LearningGoal).filter(
        LearningGoal.id == goal_id,
        LearningGoal.user_id == current_user.id
    ).first()
    
    if not goal:
        raise HTTPException(status_code=404, detail="Objectif d'apprentissage non trouvé")
    
    db.delete(goal)
    db.commit()
    return {"message": "Objectif d'apprentissage supprimé"}

# =====================================================
# ENDPOINTS POUR LE CALENDRIER
# =====================================================

@router.post("/calendar", response_model=CalendarEventResponse)
def create_calendar_event(
    event: CalendarEventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer un nouvel événement du calendrier"""
    db_event = CalendarEvent(
        **event.dict(),
        user_id=current_user.id
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.get("/calendar", response_model=List[CalendarEventResponse])
def get_calendar_events(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    event_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les événements du calendrier avec filtres"""
    query = db.query(CalendarEvent).filter(CalendarEvent.user_id == current_user.id)
    
    if start_date:
        query = query.filter(CalendarEvent.start_date >= start_date)
    if end_date:
        query = query.filter(CalendarEvent.start_date <= end_date)
    if event_type:
        query = query.filter(CalendarEvent.event_type == event_type)
    
    return query.order_by(CalendarEvent.start_date.asc()).all()

@router.get("/calendar/{event_id}", response_model=CalendarEventResponse)
def get_calendar_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer un événement spécifique du calendrier"""
    event = db.query(CalendarEvent).filter(
        CalendarEvent.id == event_id,
        CalendarEvent.user_id == current_user.id
    ).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Événement non trouvé")
    
    return event

@router.put("/calendar/{event_id}", response_model=CalendarEventResponse)
def update_calendar_event(
    event_id: int,
    event_update: CalendarEventUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mettre à jour un événement du calendrier"""
    event = db.query(CalendarEvent).filter(
        CalendarEvent.id == event_id,
        CalendarEvent.user_id == current_user.id
    ).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Événement non trouvé")
    
    for field, value in event_update.dict(exclude_unset=True).items():
        setattr(event, field, value)
    
    event.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(event)
    return event

@router.delete("/calendar/{event_id}")
def delete_calendar_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Supprimer un événement du calendrier"""
    event = db.query(CalendarEvent).filter(
        CalendarEvent.id == event_id,
        CalendarEvent.user_id == current_user.id
    ).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Événement non trouvé")
    
    db.delete(event)
    db.commit()
    return {"message": "Événement supprimé avec succès"}

# =====================================================
# ENDPOINTS POUR LES STATISTIQUES
# =====================================================

@router.get("/stats", response_model=OrganizationStatsResponse)
def get_organization_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les statistiques d'organisation de l'utilisateur"""
    
    # Statistiques des devoirs
    total_homeworks = db.query(Homework).filter(Homework.assigned_to == current_user.id).count()
    
    # Statistiques des sessions d'étude
    total_study_sessions = db.query(StudySession).filter(StudySession.user_id == current_user.id).count()
    completed_sessions = db.query(StudySession).filter(
        StudySession.user_id == current_user.id,
        StudySession.completed == True
    ).count()
    
    # Statistiques des objectifs
    total_goals = db.query(LearningGoal).filter(LearningGoal.user_id == current_user.id).count()
    completed_goals = db.query(LearningGoal).filter(
        LearningGoal.user_id == current_user.id,
        LearningGoal.status == "completed"
    ).count()
    
    # Statistiques des rappels
    active_reminders = db.query(Reminder).filter(
        Reminder.user_id == current_user.id,
        Reminder.is_active == True
    ).count()
    
    # Statistiques du calendrier
    total_calendar_events = db.query(CalendarEvent).filter(CalendarEvent.user_id == current_user.id).count()
    upcoming_events = db.query(CalendarEvent).filter(
        CalendarEvent.user_id == current_user.id,
        CalendarEvent.start_date >= datetime.utcnow()
    ).count()
    
    return OrganizationStatsResponse(
        total_homeworks=total_homeworks,
        total_study_sessions=total_study_sessions,
        completed_sessions=completed_sessions,
        total_goals=total_goals,
        completed_goals=completed_goals,
        active_reminders=active_reminders,
        total_calendar_events=total_calendar_events,
        upcoming_events=upcoming_events
    )

@router.get("/study-time-stats", response_model=StudyTimeStatsSummaryResponse)
def get_study_time_stats(
    period: str = "week",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les statistiques de temps d'étude"""
    
    from datetime import timedelta
    
    # Calculer la période
    now = datetime.utcnow()
    if period == "week":
        start_date = now - timedelta(days=7)
    elif period == "month":
        start_date = now - timedelta(days=30)
    elif period == "year":
        start_date = now - timedelta(days=365)
    else:
        start_date = now - timedelta(days=7)
    
    # Récupérer les statistiques de la période
    stats = db.query(StudyTimeStats).filter(
        StudyTimeStats.user_id == current_user.id,
        StudyTimeStats.date >= start_date
    ).all()
    
    if not stats:
        return StudyTimeStatsSummaryResponse(
            total_time=0,
            average_per_session=0,
            sessions_count=0,
            subject_breakdown=[]
        )
    
    # Calculer les totaux
    total_time = sum(stat.duration_minutes for stat in stats)
    total_sessions = sum(stat.session_count for stat in stats)
    average_per_session = total_time / total_sessions if total_sessions > 0 else 0
    
    # Répartition par matière
    subject_breakdown = {}
    for stat in stats:
        if stat.subject not in subject_breakdown:
            subject_breakdown[stat.subject] = 0
        subject_breakdown[stat.subject] += stat.duration_minutes
    
    subject_list = [{"subject": subject, "time": time} for subject, time in subject_breakdown.items()]
    
    return StudyTimeStatsSummaryResponse(
        total_time=total_time,
        average_per_session=average_per_session,
        sessions_count=total_sessions,
        subject_breakdown=subject_list
    )

# =====================================================
# ENDPOINTS POUR LES STATISTIQUES DE TEMPS D'ÉTUDE
# =====================================================

@router.post("/study-time-stats", response_model=StudyTimeStatsResponse)
def create_study_time_stat(
    stat: StudyTimeStatsCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer une nouvelle statistique de temps d'étude"""
    db_stat = StudyTimeStats(
        **stat.dict(),
        user_id=current_user.id
    )
    db.add(db_stat)
    db.commit()
    db.refresh(db_stat)
    return db_stat

@router.get("/study-time-stats/detailed", response_model=List[StudyTimeStatsResponse])
def get_detailed_study_time_stats(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    subject: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les statistiques détaillées de temps d'étude"""
    query = db.query(StudyTimeStats).filter(StudyTimeStats.user_id == current_user.id)
    
    if start_date:
        query = query.filter(StudyTimeStats.date >= start_date)
    if end_date:
        query = query.filter(StudyTimeStats.date <= end_date)
    if subject:
        query = query.filter(StudyTimeStats.subject == subject)
    
    return query.order_by(StudyTimeStats.date.desc()).all()

# =====================================================
# ENDPOINTS DE TEST SANS AUTHENTIFICATION
# =====================================================

router_no_prefix = APIRouter(tags=["Organization - No Prefix"])

@router_no_prefix.get("/homework", response_model=List[dict])
def get_homework_test(db: Session = Depends(get_db)):
    """Récupérer les devoirs (test sans authentification)"""
    # Données de test
    test_homework = [
        {
            "id": 1,
            "title": "Devoir de mathématiques",
            "description": "Exercices sur les équations du second degré",
            "subject": "Mathématiques",
            "assigned_to": 1,
            "assigned_by": 2,
            "due_date": "2024-01-20T23:59:00",
            "status": "pending",
            "priority": "medium",
            "estimated_time": 60,
            "actual_time": None,
            "notes": "",
            "tags": ["maths", "équations", "devoir"],
            "created_at": "2024-01-15T10:00:00",
            "updated_at": "2024-01-15T10:00:00"
        },
        {
            "id": 2,
            "title": "Rédaction d'histoire",
            "description": "Rédiger un essai sur la Révolution française",
            "subject": "Histoire",
            "assigned_to": 1,
            "assigned_by": 3,
            "due_date": "2024-01-25T23:59:00",
            "status": "completed",
            "priority": "high",
            "estimated_time": 120,
            "actual_time": 90,
            "notes": "Bonne rédaction, bien structurée",
            "tags": ["histoire", "rédaction", "révolution"],
            "created_at": "2024-01-10T14:30:00",
            "updated_at": "2024-01-18T16:45:00"
        },
        {
            "id": 3,
            "title": "Exercices de physique",
            "description": "Problèmes sur la mécanique",
            "subject": "Physique",
            "assigned_to": 1,
            "assigned_by": 4,
            "due_date": "2024-01-22T23:59:00",
            "status": "overdue",
            "priority": "high",
            "estimated_time": 90,
            "actual_time": None,
            "notes": "",
            "tags": ["physique", "mécanique", "exercices"],
            "created_at": "2024-01-12T09:15:00",
            "updated_at": "2024-01-12T09:15:00"
        }
    ]
    
    return test_homework

@router_no_prefix.get("/study-sessions", response_model=List[dict])
def get_study_sessions_test(db: Session = Depends(get_db)):
    """Récupérer les sessions d'étude (test sans authentification)"""
    # Données de test
    test_sessions = [
        {
            "id": 1,
            "title": "Révision mathématiques",
            "subject": "Mathématiques",
            "start_time": "2024-01-15T14:00:00",
            "end_time": "2024-01-15T16:00:00",
            "planned_duration": 120,
            "actual_duration": 110,
            "status": "completed",
            "productivity_rating": 8,
            "notes": "Bonne session, bien concentré",
            "goals": ["Réviser les équations", "Faire les exercices 1-10", "Comprendre les formules"],
            "created_at": "2024-01-15T13:55:00",
            "updated_at": "2024-01-15T16:05:00"
        },
        {
            "id": 2,
            "title": "Étude histoire",
            "subject": "Histoire",
            "start_time": "2024-01-16T10:00:00",
            "end_time": "2024-01-16T11:30:00",
            "planned_duration": 90,
            "actual_duration": 90,
            "status": "completed",
            "productivity_rating": 7,
            "notes": "Lecture des chapitres 5-7",
            "goals": ["Lire les chapitres 5-7", "Prendre des notes", "Comprendre les événements"],
            "created_at": "2024-01-16T09:55:00",
            "updated_at": "2024-01-16T11:30:00"
        },
        {
            "id": 3,
            "title": "Exercices physique",
            "subject": "Physique",
            "start_time": "2024-01-17T15:00:00",
            "end_time": "2024-01-17T16:00:00",
            "planned_duration": 60,
            "actual_duration": 45,
            "status": "completed",
            "productivity_rating": 6,
            "notes": "Quelques difficultés sur les exercices",
            "goals": ["Faire les exercices 1-5", "Comprendre les formules", "Résoudre les problèmes"],
            "created_at": "2024-01-17T14:55:00",
            "updated_at": "2024-01-17T16:00:00"
        }
    ]
    
    return test_sessions

@router_no_prefix.get("/reminders", response_model=List[dict])
def get_reminders_test(db: Session = Depends(get_db)):
    """Récupérer les rappels (test sans authentification)"""
    # Données de test
    test_reminders = [
        {
            "id": 1,
            "title": "Rendre le devoir de maths",
            "description": "N'oubliez pas de rendre le devoir sur les équations",
            "reminder_time": "2024-01-20T08:00:00",
            "is_active": True,
            "priority": "high",
            "category": "homework",
            "created_at": "2024-01-15T10:00:00",
            "updated_at": "2024-01-15T10:00:00"
        },
        {
            "id": 2,
            "title": "Réunion avec le professeur",
            "description": "Discussion sur les progrès en physique",
            "reminder_time": "2024-01-22T14:00:00",
            "is_active": True,
            "priority": "medium",
            "category": "meeting",
            "created_at": "2024-01-16T09:30:00",
            "updated_at": "2024-01-16T09:30:00"
        },
        {
            "id": 3,
            "title": "Révision pour l'examen",
            "description": "Commencer les révisions pour l'examen de fin de semestre",
            "reminder_time": "2024-01-25T10:00:00",
            "is_active": True,
            "priority": "high",
            "category": "exam",
            "created_at": "2024-01-17T16:00:00",
            "updated_at": "2024-01-17T16:00:00"
        }
    ]
    
    return test_reminders

@router_no_prefix.get("/learning-goals", response_model=List[dict])
def get_learning_goals_test(db: Session = Depends(get_db)):
    """Récupérer les objectifs d'apprentissage (test sans authentification)"""
    # Données de test
    test_goals = [
        {
            "id": 1,
            "title": "Maîtriser les équations du second degré",
            "description": "Être capable de résoudre tous types d'équations du second degré",
            "subject": "Mathématiques",
            "target_date": "2024-02-15T23:59:00",
            "status": "in_progress",
            "progress": 75,
            "priority": "high",
            "milestones": [
                {
                    "id": 1,
                    "title": "Comprendre la forme générale",
                    "description": "Identifier ax² + bx + c = 0",
                    "completed": True
                },
                {
                    "id": 2,
                    "title": "Apprendre la formule",
                    "description": "Mémoriser x = (-b ± √(b² - 4ac)) / 2a",
                    "completed": True
                },
                {
                    "id": 3,
                    "title": "Pratiquer les exercices",
                    "description": "Résoudre 10 exercices différents",
                    "completed": False
                }
            ],
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-15T14:30:00"
        },
        {
            "id": 2,
            "title": "Améliorer la compréhension en physique",
            "description": "Mieux comprendre les concepts de mécanique",
            "subject": "Physique",
            "target_date": "2024-03-01T23:59:00",
            "status": "not_started",
            "progress": 0,
            "priority": "medium",
            "milestones": [
                {
                    "id": 1,
                    "title": "Lire les chapitres de base",
                    "description": "Comprendre les lois de Newton",
                    "completed": False
                },
                {
                    "id": 2,
                    "title": "Faire les exercices pratiques",
                    "description": "Résoudre les problèmes de mécanique",
                    "completed": False
                },
                {
                    "id": 3,
                    "title": "Réviser pour l'examen",
                    "description": "Consolider les connaissances",
                    "completed": False
                }
            ],
            "created_at": "2024-01-10T09:00:00",
            "updated_at": "2024-01-10T09:00:00"
        },
        {
            "id": 3,
            "title": "Terminer le projet d'histoire",
            "description": "Finaliser le projet sur la Révolution française",
            "subject": "Histoire",
            "target_date": "2024-01-30T23:59:00",
            "status": "completed",
            "progress": 100,
            "priority": "high",
            "milestones": [
                {
                    "id": 1,
                    "title": "Rechercher les sources",
                    "description": "Trouver les documents historiques",
                    "completed": True
                },
                {
                    "id": 2,
                    "title": "Rédiger le plan",
                    "description": "Structurer le projet",
                    "completed": True
                },
                {
                    "id": 3,
                    "title": "Finaliser la rédaction",
                    "description": "Terminer le projet complet",
                    "completed": True
                }
            ],
            "created_at": "2024-01-05T10:00:00",
            "updated_at": "2024-01-18T16:00:00"
        }
    ]
    
    return test_goals 