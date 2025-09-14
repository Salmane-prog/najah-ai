from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from core.database import get_db
from core.security import get_current_user
from models.user import User
from models.ai_models import ModelTrainingSession

router = APIRouter(prefix="/training_sessions", tags=["training-sessions"])

# ============================================================================
# ENDPOINTS PRINCIPAUX
# ============================================================================

@router.get("/")
async def get_training_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère toutes les sessions d'entraînement
    """
    try:
        if current_user.role not in ["teacher", "admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès réservé aux professeurs et administrateurs"
            )

        sessions = db.query(ModelTrainingSession).all()
        
        # Calculer les statistiques
        total_sessions = len(sessions)
        active_sessions = len([s for s in sessions if s.status == "running"])
        completed_sessions = len([s for s in sessions if s.status == "completed"])
        failed_sessions = len([s for s in sessions if s.status == "failed"])
        
        # Calculer la durée moyenne
        completed_sessions_with_duration = [s for s in sessions if s.completed_at and s.started_at]
        average_duration = 0
        if completed_sessions_with_duration:
            total_duration = sum((s.completed_at - s.started_at).total_seconds() for s in completed_sessions_with_duration)
            average_duration = total_duration / len(completed_sessions_with_duration)
        
        # Calculer le taux de succès
        success_rate = (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0

        return {
            "sessions": [
                {
                    "id": session.id,
                    "model_id": session.model_id,
                    "session_name": session.session_name,
                    "training_data_source": session.training_data_source,
                    "training_data_size": session.training_data_size,
                    "validation_data_size": session.validation_data_size,
                    "epochs": session.epochs,
                    "batch_size": session.batch_size,
                    "learning_rate": session.learning_rate,
                    "optimizer": session.optimizer,
                    "loss_function": session.loss_function,
                    "training_accuracy": session.training_accuracy,
                    "validation_accuracy": session.validation_accuracy,
                    "training_loss": session.training_loss,
                    "validation_loss": session.validation_loss,
                    "status": session.status,
                    "started_at": session.started_at,
                    "completed_at": session.completed_at
                }
                for session in sessions
            ],
            "total_sessions": total_sessions,
            "active_sessions": active_sessions,
            "completed_sessions": completed_sessions,
            "failed_sessions": failed_sessions,
            "average_duration": round(average_duration, 2),
            "success_rate": round(success_rate, 1)
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des sessions: {str(e)}"
        )

@router.get("/{session_id}")
async def get_training_session_details(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère les détails d'une session d'entraînement
    """
    try:
        if current_user.role not in ["teacher", "admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès réservé aux professeurs et administrateurs"
            )

        session = db.query(ModelTrainingSession).filter(
            ModelTrainingSession.id == session_id
        ).first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session d'entraînement non trouvée"
            )

        return {
            "id": session.id,
            "model_id": session.model_id,
            "session_name": session.session_name,
            "training_data_source": session.training_data_source,
            "training_data_size": session.training_data_size,
            "validation_data_size": session.validation_data_size,
            "epochs": session.epochs,
            "batch_size": session.batch_size,
            "learning_rate": session.learning_rate,
            "optimizer": session.optimizer,
            "loss_function": session.loss_function,
            "training_accuracy": session.training_accuracy,
            "validation_accuracy": session.validation_accuracy,
            "training_loss": session.training_loss,
            "validation_loss": session.validation_loss,
            "status": session.status,
            "started_at": session.started_at,
            "completed_at": session.completed_at
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des détails: {str(e)}"
        )

# ============================================================================
# ENDPOINTS DE CONTRÔLE
# ============================================================================

@router.post("/start")
async def start_training_session(
    training_config: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Démarre une nouvelle session d'entraînement
    """
    try:
        if current_user.role not in ["teacher", "admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès réservé aux professeurs et administrateurs"
            )

        # Créer une nouvelle session d'entraînement
        new_session = ModelTrainingSession(
            model_id=training_config.get("model_id"),
            session_name=training_config.get("session_name", f"Session - {datetime.now().strftime('%Y-%m-%d %H:%M')}"),
            training_data_source=training_config.get("training_data_source", "default"),
            training_data_size=training_config.get("training_data_size", 1000),
            validation_data_size=training_config.get("validation_data_size", 200),
            epochs=training_config.get("epochs", 100),
            batch_size=training_config.get("batch_size", 32),
            learning_rate=training_config.get("learning_rate", 0.001),
            optimizer=training_config.get("optimizer", "adam"),
            loss_function=training_config.get("loss_function", "categorical_crossentropy"),
            status="running",
            started_at=datetime.now()
        )

        db.add(new_session)
        db.commit()
        db.refresh(new_session)

        return {
            "id": new_session.id,
            "model_id": new_session.model_id,
            "session_name": new_session.session_name,
            "status": new_session.status,
            "started_at": new_session.started_at
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors du démarrage de la session: {str(e)}"
        )

@router.put("/{session_id}/pause")
async def pause_training_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Met en pause une session d'entraînement
    """
    try:
        if current_user.role not in ["teacher", "admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès réservé aux professeurs et administrateurs"
            )

        session = db.query(ModelTrainingSession).filter(
            ModelTrainingSession.id == session_id
        ).first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session d'entraînement non trouvée"
            )

        if session.status != "running":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Seules les sessions en cours peuvent être mises en pause"
            )

        session.status = "paused"
        db.commit()

        return {"message": "Session mise en pause avec succès"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la pause: {str(e)}"
        )

@router.put("/{session_id}/resume")
async def resume_training_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Reprend une session d'entraînement
    """
    try:
        if current_user.role not in ["teacher", "admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès réservé aux professeurs et administrateurs"
            )

        session = db.query(ModelTrainingSession).filter(
            ModelTrainingSession.id == session_id
        ).first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session d'entraînement non trouvée"
            )

        if session.status != "paused":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Seules les sessions en pause peuvent être reprises"
            )

        session.status = "running"
        db.commit()

        return {"message": "Session reprise avec succès"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la reprise: {str(e)}"
        )

@router.put("/{session_id}/cancel")
async def cancel_training_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Annule une session d'entraînement
    """
    try:
        if current_user.role not in ["teacher", "admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès réservé aux professeurs et administrateurs"
            )

        session = db.query(ModelTrainingSession).filter(
            ModelTrainingSession.id == session_id
        ).first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session d'entraînement non trouvée"
            )

        if session.status in ["completed", "failed", "cancelled"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cette session ne peut plus être annulée"
            )

        session.status = "cancelled"
        session.completed_at = datetime.now()
        db.commit()

        return {"message": "Session annulée avec succès"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'annulation: {str(e)}"
        )

# ============================================================================
# ENDPOINTS TEMPS RÉEL
# ============================================================================

@router.get("/{session_id}/realtime")
async def get_real_time_training_updates(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère les mises à jour en temps réel d'une session
    """
    try:
        if current_user.role not in ["teacher", "admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès réservé aux professeurs et administrateurs"
            )

        session = db.query(ModelTrainingSession).filter(
            ModelTrainingSession.id == session_id
        ).first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session d'entraînement non trouvée"
            )

        # Simuler des mises à jour en temps réel
        realtime_data = {
            "session_id": session.id,
            "status": session.status,
            "training_accuracy": session.training_accuracy,
            "validation_accuracy": session.validation_accuracy,
            "training_loss": session.training_loss,
            "validation_loss": session.validation_loss,
            "last_update": datetime.now().isoformat(),
            "estimated_completion": None
        }

        # Calculer le temps de completion estimé
        if session.status == "running" and session.started_at:
            elapsed_time = (datetime.now() - session.started_at).total_seconds()
            if session.epochs and session.epochs > 0:
                # Estimation basée sur les epochs
                estimated_total = elapsed_time * (100 / 50)  # Supposons 50% de progression
                remaining_time = estimated_total - elapsed_time
                realtime_data["estimated_completion"] = datetime.now() + timedelta(seconds=remaining_time)

        return realtime_data

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des mises à jour: {str(e)}"
        )
