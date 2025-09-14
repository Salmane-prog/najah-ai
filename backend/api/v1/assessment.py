from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from core.database import get_db
from core.security import get_current_user, require_role
from models.user import User, UserRole
from models.quiz import Quiz, Question, QuizResult, QuizAnswer
from models.assessment import Assessment, AssessmentQuestion, AssessmentResult
from datetime import datetime
import json

router = APIRouter(tags=["assessment"])

@router.get("/test", response_model=dict)
def test_endpoint():
    """Endpoint de test simple."""
    return {"message": "Test endpoint works!"}

@router.get("/student/{student_id}/assessments")
def get_student_assessments(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student', 'teacher']))
):
    """Récupérer toutes les évaluations d'un étudiant"""
    # Vérifier l'accès
    if current_user.role != UserRole.teacher and current_user.id != student_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès non autorisé"
        )
    
    assessments = db.query(Assessment).filter(
        Assessment.student_id == student_id
    ).order_by(Assessment.created_at.desc()).all()
    
    return assessments

@router.get("/assessments/student/{student_id}")
def get_student_assessments_simple(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student', 'teacher']))
):
    """Endpoint simple pour récupérer les évaluations d'un étudiant"""
    # Vérifier l'accès
    if current_user.role != UserRole.teacher and current_user.id != student_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès non autorisé"
        )
    
    assessments = db.query(Assessment).filter(
        Assessment.student_id == student_id
    ).order_by(Assessment.created_at.desc()).all()
    
    return assessments 