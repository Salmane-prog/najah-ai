from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from core.database import get_db
from models.user import User
from models.quiz import QuizResult
from models.score_correction import ScoreCorrection
from api.v1.users import get_current_user
from api.v1.auth import require_role
from typing import List, Dict, Any
from datetime import datetime
import json

router = APIRouter()

@router.get("/user/{user_id}/corrections")
def get_user_score_corrections(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Récupérer les corrections de scores d'un utilisateur."""
    
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    corrections = db.query(ScoreCorrection).filter(
        ScoreCorrection.user_id == user_id
    ).order_by(ScoreCorrection.created_at.desc()).all()
    
    return {
        "user_id": user_id,
        "corrections": corrections,
        "total_corrections": len(corrections)
    }

@router.get("/user/{user_id}/corrections/stats")
def get_correction_stats(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Récupérer les statistiques de corrections d'un utilisateur."""
    
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    # Statistiques des corrections
    total_corrections = db.query(ScoreCorrection).filter(
        ScoreCorrection.user_id == user_id
    ).count()
    
    # Moyenne des corrections
    avg_correction = db.query(func.avg(ScoreCorrection.score_adjustment)).filter(
        ScoreCorrection.user_id == user_id
    ).scalar() or 0
    
    # Corrections par sujet
    corrections_by_subject = db.query(
        ScoreCorrection.subject,
        func.count(ScoreCorrection.id).label("count"),
        func.avg(ScoreCorrection.score_adjustment).label("avg_adjustment")
    ).filter(
        ScoreCorrection.user_id == user_id
    ).group_by(ScoreCorrection.subject).all()
    
    return {
        "user_id": user_id,
        "total_corrections": total_corrections,
        "average_correction": float(avg_correction),
        "corrections_by_subject": [
            {
                "subject": item.subject,
                "count": item.count,
                "average_adjustment": float(item.avg_adjustment or 0)
            }
            for item in corrections_by_subject
        ]
    }

@router.post("/user/{user_id}/corrections")
def create_score_correction(
    user_id: int,
    correction_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Créer une correction de score."""
    
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    # Vérifier que le quiz existe
    quiz_result = db.query(QuizResult).filter(
        QuizResult.id == correction_data["quiz_result_id"],
        QuizResult.student_id == user_id
    ).first()
    
    if not quiz_result:
        raise HTTPException(status_code=404, detail="Résultat de quiz non trouvé")
    
    # Créer la correction
    correction = ScoreCorrection(
        user_id=user_id,
        quiz_result_id=correction_data["quiz_result_id"],
        original_score=quiz_result.score,
        corrected_score=correction_data["corrected_score"],
        score_adjustment=correction_data["corrected_score"] - quiz_result.score,
        reason=correction_data.get("reason", ""),
        subject=quiz_result.sujet,
        corrected_by=current_user.id
    )
    
    db.add(correction)
    
    # Mettre à jour le score du quiz
    quiz_result.score = correction_data["corrected_score"]
    quiz_result.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(correction)
    
    return {
        "message": "Correction de score créée avec succès",
        "correction": {
            "id": correction.id,
            "original_score": correction.original_score,
            "corrected_score": correction.corrected_score,
            "adjustment": correction.score_adjustment,
            "reason": correction.reason,
            "created_at": correction.created_at
        }
    }

@router.get("/user/{user_id}/corrections/{correction_id}")
def get_score_correction(
    user_id: int,
    correction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Récupérer une correction de score spécifique."""
    
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    correction = db.query(ScoreCorrection).filter(
        ScoreCorrection.id == correction_id,
        ScoreCorrection.user_id == user_id
    ).first()
    
    if not correction:
        raise HTTPException(status_code=404, detail="Correction non trouvée")
    
    return correction

@router.put("/user/{user_id}/corrections/{correction_id}")
def update_score_correction(
    user_id: int,
    correction_id: int,
    correction_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Mettre à jour une correction de score."""
    
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    correction = db.query(ScoreCorrection).filter(
        ScoreCorrection.id == correction_id,
        ScoreCorrection.user_id == user_id
    ).first()
    
    if not correction:
        raise HTTPException(status_code=404, detail="Correction non trouvée")
    
    # Mettre à jour les champs autorisés
    if "corrected_score" in correction_data:
        old_adjustment = correction.score_adjustment
        correction.corrected_score = correction_data["corrected_score"]
        correction.score_adjustment = correction_data["corrected_score"] - correction.original_score
        
        # Mettre à jour le score du quiz
        quiz_result = db.query(QuizResult).filter(
            QuizResult.id == correction.quiz_result_id
        ).first()
        if quiz_result:
            quiz_result.score = correction_data["corrected_score"]
            quiz_result.updated_at = datetime.utcnow()
    
    if "reason" in correction_data:
        correction.reason = correction_data["reason"]
    
    correction.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(correction)
    
    return {
        "message": "Correction mise à jour avec succès",
        "correction": correction
    }

@router.delete("/user/{user_id}/corrections/{correction_id}")
def delete_score_correction(
    user_id: int,
    correction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Supprimer une correction de score."""
    
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    correction = db.query(ScoreCorrection).filter(
        ScoreCorrection.id == correction_id,
        ScoreCorrection.user_id == user_id
    ).first()
    
    if not correction:
        raise HTTPException(status_code=404, detail="Correction non trouvée")
    
    # Restaurer le score original du quiz
    quiz_result = db.query(QuizResult).filter(
        QuizResult.id == correction.quiz_result_id
    ).first()
    if quiz_result:
        quiz_result.score = correction.original_score
        quiz_result.updated_at = datetime.utcnow()
    
    db.delete(correction)
    db.commit()
    
    return {"message": "Correction supprimée avec succès"}

@router.get("/user/{user_id}/corrections/quiz/{quiz_result_id}")
def get_quiz_corrections(
    user_id: int,
    quiz_result_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Récupérer toutes les corrections pour un quiz spécifique."""
    
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    corrections = db.query(ScoreCorrection).filter(
        ScoreCorrection.user_id == user_id,
        ScoreCorrection.quiz_result_id == quiz_result_id
    ).order_by(ScoreCorrection.created_at.desc()).all()
    
    return {
        "quiz_result_id": quiz_result_id,
        "corrections": corrections,
        "total_corrections": len(corrections)
    }

@router.get("/user/{user_id}/corrections/history")
def get_correction_history(
    user_id: int,
    subject: str = None,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Récupérer l'historique des corrections d'un utilisateur."""
    
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    query = db.query(ScoreCorrection).filter(ScoreCorrection.user_id == user_id)
    
    if subject:
        query = query.filter(ScoreCorrection.subject == subject)
    
    corrections = query.order_by(ScoreCorrection.created_at.desc()).limit(limit).all()
    
    # Enrichir avec les détails des quiz
    enriched_corrections = []
    for correction in corrections:
        quiz_result = db.query(QuizResult).filter(
            QuizResult.id == correction.quiz_result_id
        ).first()
        
        correction_data = {
            "id": correction.id,
            "quiz_title": quiz_result.quiz_title if quiz_result else "Quiz inconnu",
            "subject": correction.subject,
            "original_score": correction.original_score,
            "corrected_score": correction.corrected_score,
            "adjustment": correction.score_adjustment,
            "reason": correction.reason,
            "created_at": correction.created_at
        }
        
        enriched_corrections.append(correction_data)
    
    return {
        "user_id": user_id,
        "corrections": enriched_corrections,
        "total_count": len(enriched_corrections)
    } 