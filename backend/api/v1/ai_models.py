from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from core.database import get_db
from core.security import get_current_user
from models.user import User
from models.ai_models import AIModel, ModelTrainingSession, AIModelPrediction, ModelDeployment

router = APIRouter(prefix="/ai_models", tags=["ai-models"])

# ============================================================================
# ENDPOINTS PRINCIPAUX
# ============================================================================

@router.get("/")
async def get_ai_models(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère tous les modèles IA
    """
    try:
        # Vérifier les permissions
        if current_user.role not in ["teacher", "admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès réservé aux professeurs et administrateurs"
            )

        # Récupérer tous les modèles IA
        models = db.query(AIModel).all()
        
        # Calculer les statistiques
        total_models = len(models)
        active_models = len([m for m in models if m.is_active])
        training_models = len([m for m in models if m.is_active])
        deployed_models = len([m for m in models if m.is_active])
        
        # Calculer la performance moyenne
        trained_models = [m for m in models if m.accuracy is not None]
        average_performance = sum(m.accuracy for m in trained_models) / len(trained_models) if trained_models else 0

        return {
            "models": [
                {
                    "id": model.id,
                    "name": model.name,
                    "description": model.description,
                    "model_type": model.model_type,
                    "algorithm": model.algorithm,
                    "version": model.version,
                    "accuracy": model.accuracy,
                    "precision": model.precision,
                    "recall": model.recall,
                    "f1_score": model.f1_score,
                    "mse": model.mse,
                    "training_duration": model.training_duration,
                    "training_data_size": model.training_data_size,
                    "is_active": model.is_active,
                    "created_at": model.created_at,
                    "updated_at": model.updated_at,
                    "hyperparameters": model.hyperparameters,
                    "model_config": model.model_config
                }
                for model in models
            ],
            "total_models": total_models,
            "active_models": active_models,
            "training_models": training_models,
            "deployed_models": deployed_models,
            "average_performance": round(average_performance, 2)
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des modèles IA: {str(e)}"
        )

@router.get("/{model_id}")
async def get_model_details(
    model_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère les détails d'un modèle IA spécifique
    """
    try:
        if current_user.role not in ["teacher", "admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès réservé aux professeurs et administrateurs"
            )

        model = db.query(AIModel).filter(AIModel.id == model_id).first()
        if not model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Modèle IA non trouvé"
            )

        return {
            "id": model.id,
            "name": model.name,
            "description": model.description,
            "model_type": model.model_type,
            "algorithm": model.algorithm,
            "version": model.version,
            "accuracy": model.accuracy,
            "precision": model.precision,
            "recall": model.recall,
            "f1_score": model.f1_score,
            "mse": model.mse,
            "training_duration": model.training_duration,
            "training_data_size": model.training_data_size,
            "is_active": model.is_active,
            "created_at": model.created_at,
            "updated_at": model.updated_at,
            "hyperparameters": model.hyperparameters,
            "model_config": model.model_config
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération du modèle: {str(e)}"
        )

@router.get("/training-sessions/")
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

        sessions = db.query(TrainingSession).all()
        
        return [
            {
                "id": session.id,
                "model_id": session.model_id,
                "model_name": session.model_name,
                "session_name": session.session_name,
                "status": session.status,
                "start_time": session.start_time,
                "end_time": session.end_time,
                "duration": session.duration,
                "progress": session.progress,
                "current_epoch": session.current_epoch,
                "total_epochs": session.total_epochs,
                "current_loss": session.current_loss,
                "current_accuracy": session.current_accuracy,
                "logs": session.logs,
                "metrics": session.metrics,
                "created_by": session.created_by,
                "created_at": session.created_at
            }
            for session in sessions
        ]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des sessions d'entraînement: {str(e)}"
        )

@router.get("/predictions/")
async def get_model_predictions(
    model_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère les prédictions des modèles
    """
    try:
        if current_user.role not in ["teacher", "admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès réservé aux professeurs et administrateurs"
            )

        query = db.query(ModelPrediction)
        if model_id:
            query = query.filter(ModelPrediction.model_id == model_id)

        predictions = query.all()
        
        return [
            {
                "id": pred.id,
                "model_id": pred.model_id,
                "model_name": pred.model_name,
                "input_data": pred.input_data,
                "prediction": pred.prediction,
                "confidence": pred.confidence,
                "processing_time": pred.processing_time,
                "timestamp": pred.timestamp,
                "user_id": pred.user_id,
                "context": pred.context
            }
            for pred in predictions
        ]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des prédictions: {str(e)}"
        )

@router.get("/performance/")
async def get_model_performance(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère la performance des modèles
    """
    try:
        if current_user.role not in ["teacher", "admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès réservé aux professeurs et administrateurs"
            )

        performances = db.query(ModelPerformance).all()
        
        return [
            {
                "model_id": perf.model_id,
                "model_name": perf.model_name,
                "overall_performance": perf.overall_performance,
                "recent_predictions": perf.recent_predictions,
                "success_rate": perf.success_rate,
                "average_response_time": perf.average_response_time,
                "error_rate": perf.error_rate,
                "last_used": perf.last_used,
                "usage_count": perf.usage_count
            }
            for perf in performances
        ]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération de la performance: {str(e)}"
        )

# ============================================================================
# ENDPOINTS D'ENTRAÎNEMENT
# ============================================================================

@router.post("/{model_id}/train")
async def start_model_training(
    model_id: int,
    training_config: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Démarre l'entraînement d'un modèle IA
    """
    try:
        if current_user.role not in ["teacher", "admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès réservé aux professeurs et administrateurs"
            )

        # Vérifier que le modèle existe
        model = db.query(AIModel).filter(AIModel.id == model_id).first()
        if not model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Modèle IA non trouvé"
            )

        # Créer une nouvelle session d'entraînement
        new_session = TrainingSession(
            model_id=model_id,
            model_name=model.name,
            session_name=f"Session d'entraînement - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            status="running",
            start_time=datetime.now(),
            progress=0,
            current_epoch=0,
            total_epochs=training_config.get("epochs", 100),
            current_loss=None,
            current_accuracy=None,
            logs=["Entraînement démarré"],
            metrics={
                "training_loss": [],
                "validation_loss": [],
                "training_accuracy": [],
                "validation_accuracy": []
            },
            created_by=current_user.id
        )

        db.add(new_session)
        db.commit()
        db.refresh(new_session)

        # Mettre à jour le statut du modèle
        model.status = "training"
        model.updated_at = datetime.now()
        db.commit()

        return {
            "id": new_session.id,
            "model_id": new_session.model_id,
            "model_name": new_session.model_name,
            "session_name": new_session.session_name,
            "status": new_session.status,
            "start_time": new_session.start_time,
            "progress": new_session.progress,
            "current_epoch": new_session.current_epoch,
            "total_epochs": new_session.total_epochs,
            "created_by": new_session.created_by,
            "created_at": new_session.created_at
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors du démarrage de l'entraînement: {str(e)}"
        )

@router.post("/{model_id}/deploy")
async def deploy_model(
    model_id: int,
    deployment_config: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Déploie un modèle IA
    """
    try:
        if current_user.role not in ["teacher", "admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès réservé aux professeurs et administrateurs"
            )

        # Vérifier que le modèle existe
        model = db.query(AIModel).filter(AIModel.id == model_id).first()
        if not model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Modèle IA non trouvé"
            )

        # Vérifier que le modèle est actif
        if not model.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le modèle doit être actif avant d'être déployé"
            )

        # Mettre à jour le statut
        model.is_active = True
        db.commit()

        return {
            "message": "Modèle déployé avec succès",
            "model_id": model.id,
            "status": "active",
            "deployed_at": model.updated_at
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors du déploiement: {str(e)}"
        )
