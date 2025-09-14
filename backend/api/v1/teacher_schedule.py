from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from models.user import User
from api.v1.users import get_current_user
from api.v1.auth import require_role
from typing import List, Dict, Any
from datetime import datetime, timedelta
from pydantic import BaseModel

router = APIRouter()

class ScheduleEvent(BaseModel):
    id: int
    title: str
    description: str
    start_time: datetime
    end_time: datetime
    event_type: str  # 'course', 'meeting', 'exam', 'reminder'
    class_id: int
    location: str
    color: str

class CreateScheduleEvent(BaseModel):
    title: str
    description: str
    start_time: datetime
    end_time: datetime
    event_type: str
    class_id: int
    location: str
    color: str = "#3B82F6"

@router.get("/schedule")
def get_teacher_schedule(
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher']))
):
    """Récupérer le planning du professeur."""
    try:
        from models.class_group import ClassGroup
        from models.schedule import ScheduleEvent as ScheduleEventModel
        
        # Récupérer les classes du professeur
        teacher_classes = db.query(ClassGroup).filter(
            ClassGroup.teacher_id == current_user.id
        ).all()
        
        class_ids = [c.id for c in teacher_classes]
        
        # Filtrer par dates si fournies
        query = db.query(ScheduleEventModel).filter(
            ScheduleEventModel.class_id.in_(class_ids)
        )
        
        if start_date:
            start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            query = query.filter(ScheduleEventModel.start_time >= start_dt)
        
        if end_date:
            end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            query = query.filter(ScheduleEventModel.end_time <= end_dt)
        
        events = query.order_by(ScheduleEventModel.start_time).all()
        
        return {
            "events": [
                {
                    "id": event.id,
                    "title": event.title,
                    "description": event.description,
                    "start_time": event.start_time.isoformat(),
                    "end_time": event.end_time.isoformat(),
                    "event_type": event.event_type,
                    "class_id": event.class_id,
                    "location": event.location,
                    "color": event.color
                }
                for event in events
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération du planning: {str(e)}")

@router.post("/schedule")
def create_schedule_event(
    event: CreateScheduleEvent,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher']))
):
    """Créer un nouvel événement dans le planning."""
    try:
        from models.class_group import ClassGroup
        from models.schedule import ScheduleEvent as ScheduleEventModel
        
        # Vérifier que la classe appartient au professeur
        class_group = db.query(ClassGroup).filter(
            ClassGroup.id == event.class_id,
            ClassGroup.teacher_id == current_user.id
        ).first()
        
        if not class_group:
            raise HTTPException(status_code=403, detail="Vous n'êtes pas autorisé à créer un événement pour cette classe")
        
        # Créer l'événement
        new_event = ScheduleEventModel(
            title=event.title,
            description=event.description,
            start_time=event.start_time,
            end_time=event.end_time,
            event_type=event.event_type,
            class_id=event.class_id,
            location=event.location,
            color=event.color,
            created_by=current_user.id,
            created_at=datetime.utcnow()
        )
        
        db.add(new_event)
        db.commit()
        db.refresh(new_event)
        
        return {
            "id": new_event.id,
            "title": new_event.title,
            "description": new_event.description,
            "start_time": new_event.start_time.isoformat(),
            "end_time": new_event.end_time.isoformat(),
            "event_type": new_event.event_type,
            "class_id": new_event.class_id,
            "location": new_event.location,
            "color": new_event.color
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création de l'événement: {str(e)}")

@router.put("/schedule/{event_id}")
def update_schedule_event(
    event_id: int,
    event: CreateScheduleEvent,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher']))
):
    """Modifier un événement du planning."""
    try:
        from models.class_group import ClassGroup
        from models.schedule import ScheduleEvent as ScheduleEventModel
        
        # Récupérer l'événement
        schedule_event = db.query(ScheduleEventModel).filter(
            ScheduleEventModel.id == event_id
        ).first()
        
        if not schedule_event:
            raise HTTPException(status_code=404, detail="Événement non trouvé")
        
        # Vérifier que la classe appartient au professeur
        class_group = db.query(ClassGroup).filter(
            ClassGroup.id == event.class_id,
            ClassGroup.teacher_id == current_user.id
        ).first()
        
        if not class_group:
            raise HTTPException(status_code=403, detail="Vous n'êtes pas autorisé à modifier cet événement")
        
        # Mettre à jour l'événement
        schedule_event.title = event.title
        schedule_event.description = event.description
        schedule_event.start_time = event.start_time
        schedule_event.end_time = event.end_time
        schedule_event.event_type = event.event_type
        schedule_event.class_id = event.class_id
        schedule_event.location = event.location
        schedule_event.color = event.color
        schedule_event.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(schedule_event)
        
        return {
            "id": schedule_event.id,
            "title": schedule_event.title,
            "description": schedule_event.description,
            "start_time": schedule_event.start_time.isoformat(),
            "end_time": schedule_event.end_time.isoformat(),
            "event_type": schedule_event.event_type,
            "class_id": schedule_event.class_id,
            "location": schedule_event.location,
            "color": schedule_event.color
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la modification de l'événement: {str(e)}")

@router.delete("/schedule/{event_id}")
def delete_schedule_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher']))
):
    """Supprimer un événement du planning."""
    try:
        from models.class_group import ClassGroup
        from models.schedule import ScheduleEvent as ScheduleEventModel
        
        # Récupérer l'événement
        schedule_event = db.query(ScheduleEventModel).filter(
            ScheduleEventModel.id == event_id
        ).first()
        
        if not schedule_event:
            raise HTTPException(status_code=404, detail="Événement non trouvé")
        
        # Vérifier que la classe appartient au professeur
        class_group = db.query(ClassGroup).filter(
            ClassGroup.id == schedule_event.class_id,
            ClassGroup.teacher_id == current_user.id
        ).first()
        
        if not class_group:
            raise HTTPException(status_code=403, detail="Vous n'êtes pas autorisé à supprimer cet événement")
        
        db.delete(schedule_event)
        db.commit()
        
        return {"message": "Événement supprimé avec succès"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la suppression de l'événement: {str(e)}")

@router.get("/schedule/upcoming")
def get_upcoming_events(
    days: int = 7,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher']))
):
    """Récupérer les événements à venir."""
    try:
        from models.class_group import ClassGroup
        from models.schedule import ScheduleEvent as ScheduleEventModel
        
        # Récupérer les classes du professeur
        teacher_classes = db.query(ClassGroup).filter(
            ClassGroup.teacher_id == current_user.id
        ).all()
        
        class_ids = [c.id for c in teacher_classes]
        
        # Calculer la date de fin
        end_date = datetime.utcnow() + timedelta(days=days)
        
        # Récupérer les événements à venir
        upcoming_events = db.query(ScheduleEventModel).filter(
            ScheduleEventModel.class_id.in_(class_ids),
            ScheduleEventModel.start_time >= datetime.utcnow(),
            ScheduleEventModel.start_time <= end_date
        ).order_by(ScheduleEventModel.start_time).all()
        
        return {
            "upcoming_events": [
                {
                    "id": event.id,
                    "title": event.title,
                    "description": event.description,
                    "start_time": event.start_time.isoformat(),
                    "end_time": event.end_time.isoformat(),
                    "event_type": event.event_type,
                    "class_id": event.class_id,
                    "location": event.location,
                    "color": event.color,
                    "days_until": (event.start_time - datetime.utcnow()).days
                }
                for event in upcoming_events
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des événements à venir: {str(e)}") 