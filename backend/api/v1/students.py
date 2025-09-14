from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from models.user import User, UserRole
from models.assignment import Assignment
from models.class_group import ClassStudent
from api.v1.auth import get_current_user
from typing import List
from sqlalchemy import and_

router = APIRouter()

@router.get("/{student_id}/learning-goals")
def get_student_learning_goals(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les objectifs d'apprentissage d'un étudiant"""
    
    # Vérifier que l'utilisateur connecté est l'étudiant lui-même ou un enseignant
    if current_user.role == UserRole.student and current_user.id != student_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous ne pouvez voir que vos propres objectifs"
        )
    
    # Pour l'instant, retourner une liste vide (à implémenter plus tard)
    return []

@router.get("/{student_id}/study-sessions")
def get_student_study_sessions(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les sessions d'étude d'un étudiant"""
    
    # Vérifier que l'utilisateur connecté est l'étudiant lui-même ou un enseignant
    if current_user.role == UserRole.student and current_user.id != student_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous ne pouvez voir que vos propres sessions d'étude"
        )
    
    # Pour l'instant, retourner une liste vide (à implémenter plus tard)
    return []

@router.get("/{student_id}/assignments")
def get_student_assignments(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les devoirs assignés à un étudiant spécifique"""
    
    # Vérifier que l'utilisateur connecté est l'étudiant lui-même ou un enseignant
    if current_user.role == UserRole.student and current_user.id != student_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous ne pouvez voir que vos propres devoirs"
        )
    
    # Récupérer les devoirs assignés à l'étudiant
    assignments = db.query(Assignment).filter(
        and_(
            Assignment.assignment_type == "student",
            Assignment.target_ids.contains([student_id])
        )
    ).all()
    
    # Récupérer aussi les devoirs assignés aux classes dont l'étudiant fait partie
    student_classes = db.query(ClassStudent.class_id).filter(
        ClassStudent.student_id == student_id
    ).all()
    
    class_ids = [sc.class_id for sc in student_classes]
    class_assignments = db.query(Assignment).filter(
        and_(
            Assignment.assignment_type == "class",
            Assignment.target_ids.overlap(class_ids)
        )
    ).all()
    
    # Combiner et dédupliquer les devoirs
    all_assignments = assignments + class_assignments
    unique_assignments = {a.id: a for a in all_assignments}.values()
    
    result = []
    for assignment in unique_assignments:
        # Récupérer le nom de l'enseignant
        teacher = db.query(User).filter(User.id == assignment.created_by).first()
        teacher_name = f"{teacher.first_name or ''} {teacher.last_name or ''}".strip() or teacher.email if teacher else "Enseignant inconnu"
        
        result.append({
            "id": assignment.id,
            "title": assignment.title,
            "description": assignment.description,
            "subject": assignment.subject,
            "assignment_type": assignment.assignment_type,
            "target_ids": assignment.target_ids,
            "due_date": assignment.due_date,
            "priority": assignment.priority,
            "estimated_time": assignment.estimated_time,
            "status": assignment.status,
            "created_at": assignment.created_at,
            "created_by": assignment.created_by,
            "teacher_name": teacher_name
        })
    
    return result



