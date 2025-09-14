#!/usr/bin/env python3
"""
API pour l'onboarding automatique des étudiants
Vérifie et lance automatiquement l'évaluation initiale à la première connexion
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any
from datetime import datetime

from core.database import get_db
from core.security import get_current_user
from models.user import User
from services.student_onboarding_service import StudentOnboardingService

router = APIRouter(tags=["student_onboarding"])

@router.get("/student/{student_id}/onboarding-status")
async def get_student_onboarding_status(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Vérifier le statut d'onboarding d'un étudiant
    Lance automatiquement l'évaluation initiale si nécessaire
    """
    try:
        # Vérifier l'autorisation
        if current_user.id != student_id and current_user.role.value != "teacher":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès non autorisé"
            )
        
        print(f"🎓 Vérification du statut d'onboarding pour l'étudiant {student_id}")
        
        # Utiliser le service d'onboarding
        onboarding_service = StudentOnboardingService(db)
        onboarding_status = onboarding_service.get_student_onboarding_status(student_id)
        
        return {
            "success": True,
            "message": "Statut d'onboarding récupéré avec succès",
            "data": onboarding_status
        }
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification du statut d'onboarding: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la vérification: {str(e)}"
        )

@router.post("/student/{student_id}/start-onboarding")
async def start_student_onboarding(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Démarrer manuellement l'onboarding d'un étudiant
    """
    try:
        # Vérifier l'autorisation
        if current_user.id != student_id and current_user.role.value != "teacher":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès non autorisé"
            )
        
        print(f"🚀 Démarrage manuel de l'onboarding pour l'étudiant {student_id}")
        
        # Utiliser le service d'onboarding
        onboarding_service = StudentOnboardingService(db)
        
        # Vérifier le statut actuel
        current_status = onboarding_service.check_and_initialize_student(student_id)
        
        if current_status["status"] == "fully_onboarded":
            return {
                "success": True,
                "message": "L'étudiant est déjà entièrement configuré",
                "data": current_status
            }
        
        # Démarrer l'évaluation initiale
        assessment_result = onboarding_service.auto_start_initial_assessment(student_id)
        
        # Mettre à jour le statut
        updated_status = onboarding_service.check_and_initialize_student(student_id)
        
        return {
            "success": True,
            "message": "Onboarding démarré avec succès",
            "data": {
                "previous_status": current_status,
                "assessment_result": assessment_result,
                "current_status": updated_status
            }
        }
        
    except Exception as e:
        print(f"❌ Erreur lors du démarrage de l'onboarding: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors du démarrage: {str(e)}"
        )

@router.get("/student/{student_id}/assessment-ready")
async def check_assessment_readiness(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Vérifier si l'évaluation initiale est prête pour un étudiant
    """
    try:
        # Vérifier l'autorisation
        if current_user.id != student_id and current_user.role.value != "teacher":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès non autorisé"
            )
        
        print(f"🔍 Vérification de la disponibilité de l'évaluation pour l'étudiant {student_id}")
        
        # Utiliser le service d'onboarding
        onboarding_service = StudentOnboardingService(db)
        onboarding_status = onboarding_service.check_and_initialize_student(student_id)
        
        # Vérifier si l'évaluation est prête
        assessment_ready = False
        assessment_id = None
        
        if onboarding_status["status"] == "needs_initial_evaluation":
            # Démarrer automatiquement l'évaluation
            assessment_result = onboarding_service.auto_start_initial_assessment(student_id)
            if assessment_result["success"]:
                assessment_ready = True
                assessment_id = assessment_result["assessment_id"]
        
        elif onboarding_status["status"] == "profile_exists_no_assessment":
            # Vérifier s'il y a une évaluation en cours
            existing_assessment = onboarding_service._get_existing_assessment(student_id)
            if existing_assessment and existing_assessment["status"] == "in_progress":
                assessment_ready = True
                assessment_id = existing_assessment["id"]
        
        return {
            "success": True,
            "message": "Statut de l'évaluation vérifié",
            "data": {
                "assessment_ready": assessment_ready,
                "assessment_id": assessment_id,
                "onboarding_status": onboarding_status
            }
        }
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification de la disponibilité: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la vérification: {str(e)}"
        )

@router.get("/student/{student_id}/onboarding-summary")
async def get_onboarding_summary(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtenir un résumé complet de l'onboarding d'un étudiant
    """
    try:
        # Vérifier l'autorisation
        if current_user.id != student_id and current_user.role.value != "teacher":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès non autorisé"
            )
        
        print(f"📊 Génération du résumé d'onboarding pour l'étudiant {student_id}")
        
        # Utiliser le service d'onboarding
        onboarding_service = StudentOnboardingService(db)
        
        # Vérifier le statut actuel
        onboarding_status = onboarding_service.check_and_initialize_student(student_id)
        
        # Récupérer les informations détaillées
        summary = {
            "student_id": student_id,
            "onboarding_status": onboarding_status,
            "timestamp": datetime.utcnow().isoformat(),
            "next_actions": [],
            "completed_steps": [],
            "pending_steps": []
        }
        
        # Analyser les étapes
        if onboarding_status["has_learning_profile"]:
            summary["completed_steps"].append("Profil d'apprentissage créé")
        else:
            summary["pending_steps"].append("Créer le profil d'apprentissage")
        
        if onboarding_status["has_completed_assessment"]:
            summary["completed_steps"].append("Évaluation initiale terminée")
        else:
            summary["pending_steps"].append("Terminer l'évaluation initiale")
        
        # Déterminer les prochaines actions
        if onboarding_status["status"] == "needs_initial_evaluation":
            summary["next_actions"].append("Commencer l'évaluation initiale")
        elif onboarding_status["status"] == "profile_exists_no_assessment":
            summary["next_actions"].append("Reprendre l'évaluation initiale")
        elif onboarding_status["status"] == "fully_onboarded":
            summary["next_actions"].append("Commencer l'apprentissage")
        
        return {
            "success": True,
            "message": "Résumé d'onboarding généré avec succès",
            "data": summary
        }
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération du résumé: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la génération: {str(e)}"
        )

@router.post("/student/{student_id}/reset-onboarding")
async def reset_student_onboarding(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Réinitialiser l'onboarding d'un étudiant (pour les tests ou corrections)
    """
    try:
        # Vérifier l'autorisation (seulement les professeurs)
        if current_user.role.value != "teacher":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Seuls les professeurs peuvent réinitialiser l'onboarding"
            )
        
        print(f"🔄 Réinitialisation de l'onboarding pour l'étudiant {student_id}")
        
        # Utiliser le service d'onboarding
        onboarding_service = StudentOnboardingService(db)
        
        # Supprimer les données existantes
        self._reset_student_data(db, student_id)
        
        # Vérifier le nouveau statut
        new_status = onboarding_service.check_and_initialize_student(student_id)
        
        return {
            "success": True,
            "message": "Onboarding réinitialisé avec succès",
            "data": {
                "previous_status": "reset",
                "new_status": new_status
            }
        }
        
    except Exception as e:
        print(f"❌ Erreur lors de la réinitialisation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la réinitialisation: {str(e)}"
        )

def _reset_student_data(db: Session, student_id: int):
    """Réinitialiser les données d'un étudiant"""
    try:
        # Supprimer les profils d'apprentissage
        db.execute("""
            DELETE FROM french_learning_profiles 
            WHERE student_id = :student_id
        """, {"student_id": student_id})
        
        # Supprimer les tests
        db.execute("""
            DELETE FROM french_adaptive_tests 
            WHERE student_id = :student_id
        """, {"student_id": student_id})
        
        # Supprimer les réponses
        db.execute("""
            DELETE FROM french_test_answers 
            WHERE student_id = :student_id
        """, {"student_id": student_id})
        
        # Supprimer les questions d'évaluation
        db.execute("""
            DELETE FROM assessment_questions 
            WHERE assessment_id IN (
                SELECT id FROM french_adaptive_tests WHERE student_id = :student_id
            )
        """, {"student_id": student_id})
        
        db.commit()
        print(f"✅ Données réinitialisées pour l'étudiant {student_id}")
        
    except Exception as e:
        print(f"⚠️ Erreur lors de la réinitialisation des données: {e}")
        db.rollback()
        raise





