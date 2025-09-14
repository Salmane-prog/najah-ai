from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import json

from core.database import get_db
from api.v1.users import get_current_user
from api.v1.auth import require_role
from models.user import User
from models.assessment import Assessment, AssessmentAssignment

router = APIRouter()

# Endpoint de test sans authentification
@router.get("/test-homework")
def get_test_homework(db: Session = Depends(get_db)):
    """Endpoint de test pour récupérer les devoirs sans authentification."""
    try:
        # Importer le modèle Homework
        from models.organization import Homework
        
        # Récupérer tous les devoirs depuis la table homework
        homeworks = db.query(Homework).all()
        
        homework_list = []
        for homework in homeworks:
            homework_list.append({
                "id": homework.id,
                "title": homework.title,
                "description": homework.description,
                "subject": homework.subject,
                "class_id": homework.class_id,
                "assigned_by": homework.assigned_by,
                "assigned_to": homework.assigned_to,
                "due_date": homework.due_date.isoformat() if homework.due_date else None,
                "status": homework.status,
                "priority": homework.priority,
                "estimated_time": homework.estimated_time,
                "created_at": homework.created_at.isoformat() if homework.created_at else None
            })
        
        return homework_list
        
    except Exception as e:
        print(f"Erreur dans get_test_homework: {str(e)}")
        return []

# Endpoint de test pour les sessions d'étude sans authentification
@router.get("/test-study-sessions")
def get_test_study_sessions(db: Session = Depends(get_db)):
    """Endpoint de test pour récupérer les sessions d'étude sans authentification."""
    try:
        # Importer le modèle StudySession
        from models.organization import StudySession
        
        # Récupérer toutes les sessions d'étude
        sessions = db.query(StudySession).all()
        
        session_list = []
        for session in sessions:
            session_list.append({
                "id": session.id,
                "title": session.topic,
                "description": session.notes,
                "subject": session.subject,
                "start_time": session.start_time.isoformat() if session.start_time else None,
                "end_time": session.end_time.isoformat() if session.end_time else None,
                "duration": session.planned_duration or 0,
                "goals": [],
                "notes": session.notes,
                "completed": session.status == "completed",
                "student_id": session.user_id,
                "created_at": session.created_at.isoformat() if session.created_at else None
            })
        
        return session_list
        
    except Exception as e:
        print(f"Erreur dans get_test_study_sessions: {str(e)}")
        return []

@router.get("/homework")
def get_student_homework(
    status_filter: Optional[str] = Query(None, description="Filtrer par statut"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Récupérer les devoirs d'un étudiant."""
    try:
        # Importer le modèle Homework
        from models.organization import Homework
        
        # Récupérer les devoirs assignés à l'étudiant depuis la table homework
        query = db.query(Homework).filter(
            Homework.assigned_to == current_user.id
        )
        
        if status_filter:
            if status_filter == 'overdue':
                # Devoirs en retard
                query = query.filter(
                    Homework.due_date < datetime.utcnow(),
                    Homework.status != 'completed'
                )
            elif status_filter == 'pending':
                # Devoirs en attente
                query = query.filter(
                    Homework.status == 'pending'
                )
            elif status_filter == 'completed':
                # Devoirs terminés
                query = query.filter(
                    Homework.status == 'completed'
                )
        
        homeworks = query.order_by(Homework.due_date).all()
        
        # Convertir en format de réponse
        homework_list = []
        for homework in homeworks:
            homework_list.append({
                "id": homework.id,
                "title": homework.title,
                "description": homework.description,
                "subject": homework.subject,
                "class_id": homework.class_id,
                "assigned_by": homework.assigned_by,
                "assigned_to": homework.assigned_to,
                "due_date": homework.due_date.isoformat() if homework.due_date else None,
                "status": homework.status,
                "priority": homework.priority,
                "estimated_time": homework.estimated_time,
                "created_at": homework.created_at.isoformat() if homework.created_at else None
            })
        
        return homework_list
        
    except Exception as e:
        print(f"Erreur dans get_student_homework: {str(e)}")
        return []

# Endpoints pour les sessions d'étude
@router.get("/study-sessions")
def get_study_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Récupérer les sessions d'étude d'un étudiant."""
    try:
        # Importer le modèle StudySession
        from models.organization import StudySession
        
        # Récupérer les sessions d'étude de l'étudiant
        sessions = db.query(StudySession).filter(
            StudySession.user_id == current_user.id
        ).order_by(StudySession.start_time).all()
        
        # Convertir en format de réponse
        session_list = []
        for session in sessions:
            session_list.append({
                "id": session.id,
                "title": session.topic,  # Utiliser topic comme titre
                "description": session.notes,  # Utiliser notes comme description
                "subject": session.subject,
                "start_time": session.start_time.isoformat() if session.start_time else None,
                "end_time": session.end_time.isoformat() if session.end_time else None,
                "duration": session.planned_duration or 0,
                "goals": [],  # Pas de goals dans le modèle actuel
                "notes": session.notes,
                "completed": session.status == "completed",
                "student_id": session.user_id,
                "created_at": session.created_at.isoformat() if session.created_at else None
            })
        
        return session_list
        
    except Exception as e:
        print(f"Erreur dans get_study_sessions: {str(e)}")
        return []

@router.post("/study-sessions")
def create_study_session(
    session_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Créer une nouvelle session d'étude."""
    try:
        # Importer le modèle StudySession
        from models.organization import StudySession
        
        # Créer la nouvelle session
        new_session = StudySession(
            topic=session_data.get("title"),  # Utiliser topic pour le titre
            subject=session_data.get("subject"),
            start_time=datetime.fromisoformat(session_data.get("start_time")),
            end_time=datetime.fromisoformat(session_data.get("end_time")),
            planned_duration=session_data.get("duration"),
            notes=session_data.get("notes"),
            status="planned",
            user_id=current_user.id,
            created_at=datetime.utcnow()
        )
        
        db.add(new_session)
        db.commit()
        
        # Retourner la réponse sans refresh
        return {
            "id": new_session.id,
            "title": new_session.topic,
            "description": new_session.notes,
            "subject": new_session.subject,
            "start_time": new_session.start_time.isoformat() if new_session.start_time else None,
            "end_time": new_session.end_time.isoformat() if new_session.end_time else None,
            "duration": new_session.planned_duration or 0,
            "goals": [],  # Pas de goals dans le modèle actuel
            "notes": new_session.notes,
            "completed": new_session.status == "completed",
            "student_id": new_session.user_id,
            "created_at": new_session.created_at.isoformat() if new_session.created_at else None
        }
        
    except Exception as e:
        db.rollback()
        print(f"Erreur dans create_study_session: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création de la session: {str(e)}")

@router.put("/study-sessions/{session_id}/complete")
def complete_study_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Marquer une session d'étude comme terminée."""
    try:
        # Importer le modèle StudySession
        from models.organization import StudySession
        
        # Trouver la session
        session = db.query(StudySession).filter(
            StudySession.id == session_id,
            StudySession.user_id == current_user.id
        ).first()
        
        if not session:
            raise HTTPException(status_code=404, detail="Session non trouvée")
        
        # Marquer comme terminée
        session.status = "completed"
        db.commit()
        
        return {"message": "Session marquée comme terminée"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Erreur dans complete_study_session: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la mise à jour de la session: {str(e)}")

@router.put("/homework/{homework_id}/complete")
def complete_homework(
    homework_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Marquer un devoir comme terminé."""
    try:
        # Vérifier que le devoir appartient à l'étudiant
        assignment = db.query(AssessmentAssignment).filter(
            AssessmentAssignment.id == homework_id,
            AssessmentAssignment.student_id == current_user.id
        ).first()
        
        if not assignment:
            raise HTTPException(status_code=404, detail="Devoir non trouvé")
        
        # Marquer comme terminé
        assignment.status = 'completed'
        assignment.completed_at = datetime.utcnow()
        db.commit()
        
        return {"message": "Devoir marqué comme terminé"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Erreur dans complete_homework: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur lors de la mise à jour du devoir")

@router.get("/homework/overdue")
def get_overdue_homework(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Récupérer les devoirs en retard."""
    try:
        overdue_assignments = db.query(AssessmentAssignment).filter(
            AssessmentAssignment.student_id == current_user.id,
            AssessmentAssignment.due_date < datetime.utcnow(),
            AssessmentAssignment.status != 'completed'
        ).all()
        
        overdue_list = []
        for assignment in overdue_assignments:
            assessment = db.query(Assessment).filter(Assessment.id == assignment.assessment_id).first()
            if assessment:
                overdue_list.append({
                    "id": assignment.id,
                    "title": assessment.title,
                    "description": assessment.description,
                    "subject": assessment.subject,
                    "due_date": assignment.due_date.isoformat() if assignment.due_date else None,
                    "status": assignment.status,
                    "priority": assessment.priority if hasattr(assessment, 'priority') else 'high',
                    "estimated_time": assessment.estimated_time if hasattr(assessment, 'estimated_time') else 60
                })
        
        return overdue_list
        
    except Exception as e:
        print(f"Erreur dans get_overdue_homework: {str(e)}")
        return []

@router.get("/homework/pending")
def get_pending_homework(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Récupérer les devoirs en attente."""
    try:
        pending_assignments = db.query(AssessmentAssignment).filter(
            AssessmentAssignment.student_id == current_user.id,
            AssessmentAssignment.status == 'pending'
        ).all()
        
        pending_list = []
        for assignment in pending_assignments:
            assessment = db.query(Assessment).filter(Assessment.id == assignment.assessment_id).first()
            if assessment:
                pending_list.append({
                    "id": assignment.id,
                    "title": assessment.title,
                    "description": assessment.description,
                    "subject": assessment.subject,
                    "due_date": assignment.due_date.isoformat() if assignment.due_date else None,
                    "status": assignment.status,
                    "priority": assessment.priority if hasattr(assessment, 'priority') else 'medium',
                    "estimated_time": assessment.estimated_time if hasattr(assessment, 'estimated_time') else 60
                })
        
        return pending_list
        
    except Exception as e:
        print(f"Erreur dans get_pending_homework: {str(e)}")
        return []

@router.get("/homework/completed")
def get_completed_homework(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Récupérer les devoirs terminés."""
    try:
        completed_assignments = db.query(AssessmentAssignment).filter(
            AssessmentAssignment.student_id == current_user.id,
            AssessmentAssignment.status == 'completed'
        ).all()
        
        completed_list = []
        for assignment in completed_assignments:
            assessment = db.query(Assessment).filter(Assessment.id == assignment.assessment_id).first()
            if assessment:
                completed_list.append({
                    "id": assignment.id,
                    "title": assessment.title,
                    "description": assessment.description,
                    "subject": assessment.subject,
                    "due_date": assignment.due_date.isoformat() if assignment.due_date else None,
                    "status": assignment.status,
                    "priority": assessment.priority if hasattr(assessment, 'priority') else 'medium',
                    "estimated_time": assessment.estimated_time if hasattr(assessment, 'estimated_time') else 60,
                    "completed_at": assignment.completed_at.isoformat() if assignment.completed_at else None
                })
        
        return completed_list
        
    except Exception as e:
        print(f"Erreur dans get_completed_homework: {str(e)}")
        return [] 