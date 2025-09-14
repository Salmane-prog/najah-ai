#!/usr/bin/env python3
"""
API pour la gestion des parcours d'apprentissage des étudiants
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from core.database import get_db
from core.security import get_current_user
from models.user import User
from models.learning_path import LearningPath
from models.learning_path_step import LearningPathStep
from models.student_learning_path import StudentLearningPath
from schemas.learning_path import (
    LearningPathStart, LearningPathStepComplete, LearningPathProgress
)

router = APIRouter(tags=["learning_paths"])

@router.get("/student/{student_id}")
def get_student_learning_paths(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer tous les parcours d'apprentissage d'un étudiant"""
    # Récupérer tous les parcours disponibles
    all_paths = db.query(LearningPath).all()
    
    # Récupérer les parcours suivis par l'étudiant
    student_paths = db.query(StudentLearningPath).filter(
        StudentLearningPath.student_id == student_id
    ).all()
    
    # Créer un dictionnaire des parcours suivis
    followed_paths = {sp.learning_path_id: sp for sp in student_paths}
    
    # Construire la réponse
    learning_paths = []
    for path in all_paths:
        student_path = followed_paths.get(path.id)
        is_followed = student_path is not None
        
        path_data = {
            "id": path.id,
            "title": path.title,
            "description": path.description,
            "subject": path.subject,
            "level": path.level,
            "difficulty": path.difficulty,
            "estimated_duration": path.estimated_duration,
            "is_followed": is_followed
        }
        
        if is_followed:
            path_data.update({
                "progress": student_path.progress,
                "is_completed": student_path.is_completed,
                "started_at": student_path.started_at,
                "current_step": student_path.current_step,
                "total_steps": student_path.total_steps
            })
        
        learning_paths.append(path_data)
    
    return {"learning_paths": learning_paths}

@router.get("/student/{student_id}/active")
def get_active_learning_paths(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les parcours d'apprentissage actifs d'un étudiant"""
    active_paths = db.query(StudentLearningPath).filter(
        StudentLearningPath.student_id == student_id,
        StudentLearningPath.is_completed == False
    ).all()
    
    learning_paths = []
    for student_path in active_paths:
        path = db.query(LearningPath).filter(
            LearningPath.id == student_path.learning_path_id
        ).first()
        
        if path:
            learning_paths.append({
                "id": path.id,
                "title": path.title,
                "subject": path.subject,
                "progress": student_path.progress,
                "current_step": student_path.current_step,
                "total_steps": student_path.total_steps,
                "started_at": student_path.started_at
            })
    
    return {"learning_paths": learning_paths}

@router.get("/student/{student_id}/completed")
def get_completed_learning_paths(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les parcours d'apprentissage complétés d'un étudiant"""
    completed_paths = db.query(StudentLearningPath).filter(
        StudentLearningPath.student_id == student_id,
        StudentLearningPath.is_completed == True
    ).all()
    
    learning_paths = []
    for student_path in completed_paths:
        path = db.query(LearningPath).filter(
            LearningPath.id == student_path.learning_path_id
        ).first()
        
        if path:
            learning_paths.append({
                "id": path.id,
                "title": path.title,
                "subject": path.subject,
                "progress": student_path.progress,
                "completed_at": student_path.completed_at,
                "total_steps": student_path.total_steps
            })
    
    return {"learning_paths": learning_paths}

@router.get("/{learning_path_id}/steps")
def get_learning_path_steps(
    learning_path_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les étapes d'un parcours d'apprentissage"""
    # Vérifier que l'étudiant suit ce parcours
    student_path = db.query(StudentLearningPath).filter(
        StudentLearningPath.student_id == current_user.id,
        StudentLearningPath.learning_path_id == learning_path_id
    ).first()
    
    if not student_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parcours non trouvé ou non suivi"
        )
    
    # Récupérer les étapes
    steps = db.query(LearningPathStep).filter(
        LearningPathStep.learning_path_id == learning_path_id
    ).order_by(LearningPathStep.step_number).all()
    
    return {
        "learning_path": {
            "id": learning_path_id,
            "title": db.query(LearningPath).filter(
                LearningPath.id == learning_path_id
            ).first().title
        },
        "steps": [
            {
                "id": step.id,
                "step_number": step.step_number,
                "title": step.title,
                "description": step.description,
                "content_type": step.content_type,
                "estimated_duration": step.estimated_duration,
                "is_required": step.is_required,
                "is_active": step.is_active
            }
            for step in steps
        ]
    }

@router.get("/{learning_path_id}/progress")
def get_learning_path_progress(
    learning_path_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer le progrès d'un parcours d'apprentissage"""
    student_path = db.query(StudentLearningPath).filter(
        StudentLearningPath.student_id == current_user.id,
        StudentLearningPath.learning_path_id == learning_path_id
    ).first()
    
    if not student_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parcours non trouvé ou non suivi"
        )
    
    # Calculer le progrès détaillé
    total_steps = db.query(LearningPathStep).filter(
        LearningPathStep.learning_path_id == learning_path_id
    ).count()
    
    current_step = student_path.current_step or 1
    progress_percentage = (current_step / total_steps * 100) if total_steps > 0 else 0
    
    return {
        "learning_path_id": learning_path_id,
        "student_id": current_user.id,
        "progress": student_path.progress or 0.0,
        "progress_percentage": progress_percentage,
        "current_step": current_step,
        "total_steps": total_steps,
        "is_completed": student_path.is_completed,
        "started_at": student_path.started_at,
        "completed_at": student_path.completed_at
    }

@router.post("/{learning_path_id}/start")
def start_learning_path(
    learning_path_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Démarrer un parcours d'apprentissage"""
    # Vérifier que le parcours existe
    learning_path = db.query(LearningPath).filter(
        LearningPath.id == learning_path_id
    ).first()
    
    if not learning_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parcours d'apprentissage non trouvé"
        )
    
    # Vérifier que l'étudiant ne suit pas déjà ce parcours
    existing_path = db.query(StudentLearningPath).filter(
        StudentLearningPath.student_id == current_user.id,
        StudentLearningPath.learning_path_id == learning_path_id
    ).first()
    
    if existing_path:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vous suivez déjà ce parcours"
        )
    
    # Créer l'entrée de suivi
    student_learning_path = StudentLearningPath(
        student_id=current_user.id,
        learning_path_id=learning_path_id,
        progress=0.0,
        is_completed=False,
        started_at=datetime.utcnow(),
        current_step=1,
        total_steps=db.query(LearningPathStep).filter(
            LearningPathStep.learning_path_id == learning_path_id
        ).count()
    )
    
    db.add(student_learning_path)
    db.commit()
    
    return {
        "message": "Parcours d'apprentissage démarré avec succès",
        "learning_path_id": learning_path_id,
        "started_at": student_learning_path.started_at,
        "current_step": student_learning_path.current_step,
        "total_steps": student_learning_path.total_steps
    }

@router.post("/{learning_path_id}/complete-step")
def complete_learning_path_step(
    learning_path_id: int,
    step_data: LearningPathStepComplete,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Compléter une étape d'un parcours d'apprentissage"""
    # Vérifier que l'étudiant suit ce parcours
    student_path = db.query(StudentLearningPath).filter(
        StudentLearningPath.student_id == current_user.id,
        StudentLearningPath.learning_path_id == learning_path_id
    ).first()
    
    if not student_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parcours non trouvé ou non suivi"
        )
    
    # Vérifier que l'étape est valide
    total_steps = db.query(LearningPathStep).filter(
        LearningPathStep.learning_path_id == learning_path_id
    ).count()
    
    if step_data.step_number > total_steps:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Numéro d'étape invalide"
        )
    
    # Mettre à jour le progrès
    student_path.current_step = step_data.step_number + 1
    student_path.progress = (step_data.step_number / total_steps) * 100
    
    # Vérifier si le parcours est terminé
    if step_data.step_number >= total_steps:
        student_path.is_completed = True
        student_path.completed_at = datetime.utcnow()
        student_path.progress = 100.0
    
    db.commit()
    
    return {
        "message": "Étape complétée avec succès",
        "learning_path_id": learning_path_id,
        "current_step": student_path.current_step,
        "progress": student_path.progress,
        "is_completed": student_path.is_completed
    }

@router.get("/test")
def test_endpoint():
    """Endpoint de test"""
    return {"message": "Learning Paths API fonctionne correctement"}
