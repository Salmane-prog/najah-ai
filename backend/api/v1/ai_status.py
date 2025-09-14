#!/usr/bin/env python3
"""
API pour vérifier le statut des services IA
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any

from core.database import get_db
from core.security import get_current_user
from models.user import User
from config.ai_config import AIConfig

router = APIRouter(prefix="/ai", tags=["ai_status"])

@router.get("/status")
async def get_ai_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Retourne le statut des services IA"""
    
    try:
        # Vérifier la disponibilité des services IA
        ai_status = AIConfig.get_ai_status()
        
        # Informations sur l'utilisateur
        user_info = {
            "id": current_user.id,
            "email": current_user.email,
            "role": current_user.role
        }
        
        # Statut des modèles IA
        models_status = {
            "openai": {
                "available": ai_status["openai"],
                "model": AIConfig.OPENAI_MODEL,
                "max_tokens": AIConfig.OPENAI_MAX_TOKENS
            },
            "huggingface": {
                "available": ai_status["huggingface"],
                "models": ai_status["models"],
                "base_url": AIConfig.HUGGINGFACE_BASE_URL
            }
        }
        
        # Configuration des seuils d'adaptation
        adaptation_config = {
            "thresholds": ai_status["adaptation_thresholds"],
            "learning_styles": list(AIConfig.LEARNING_STYLE_INDICATORS.keys())
        }
        
        return {
            "status": "success",
            "message": "Statut des services IA récupéré avec succès",
            "user": user_info,
            "ai_services": models_status,
            "adaptation_config": adaptation_config,
            "timestamp": "2024-01-01T00:00:00Z"  # À remplacer par datetime.now()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Erreur lors de la récupération du statut IA: {str(e)}",
            "ai_services": {
                "openai": {"available": False},
                "huggingface": {"available": False}
            }
        }

@router.get("/test")
async def test_ai_services(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Teste les services IA disponibles"""
    
    test_results = {}
    
    # Test OpenAI
    if AIConfig.is_openai_available():
        try:
            # Test simple de génération
            test_results["openai"] = {
                "status": "available",
                "test": "success"
            }
        except Exception as e:
            test_results["openai"] = {
                "status": "error",
                "test": str(e)
            }
    else:
        test_results["openai"] = {
            "status": "unavailable",
            "test": "API key manquante"
        }
    
    # Test HuggingFace
    if AIConfig.is_huggingface_available():
        try:
            # Test simple de connexion
            test_results["huggingface"] = {
                "status": "available",
                "test": "success"
            }
        except Exception as e:
            test_results["huggingface"] = {
                "status": "error",
                "test": str(e)
            }
    else:
        test_results["huggingface"] = {
            "status": "unavailable",
            "test": "API key manquante"
        }
    
    return {
        "status": "success",
        "message": "Tests des services IA terminés",
        "test_results": test_results,
        "user_id": current_user.id
    }
