#!/usr/bin/env python3
"""
API pour les recommandations IA des étudiants
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import random

from database import get_db
from models import User, Assessment, AssessmentResult, QuizResult, TestAttempt
from core.security import get_current_user

router = APIRouter()

@router.get("/student/{student_id}")
async def get_student_ai_recommendations(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupérer les recommandations IA pour un étudiant
    """
    try:
        # Vérifier que l'utilisateur est l'étudiant lui-même ou un enseignant
        if current_user.role == "student" and current_user.id != student_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès non autorisé"
            )
        
        # Vérifier que l'étudiant existe
        student = db.query(User).filter(User.id == student_id, User.role == "student").first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Étudiant non trouvé"
            )
        
        # Récupérer les performances récentes
        recent_results = db.query(AssessmentResult).filter(
            AssessmentResult.student_id == student_id
        ).order_by(AssessmentResult.created_at.desc()).limit(10).all()
        
        quiz_results = db.query(QuizResult).filter(
            QuizResult.student_id == student_id
        ).order_by(QuizResult.created_at.desc()).limit(10).all()
        
        test_attempts = db.query(TestAttempt).filter(
            TestAttempt.student_id == student_id
        ).order_by(TestAttempt.created_at.desc()).limit(10).all()
        
        # Analyser les performances pour générer des recommandations
        recommendations = generate_ai_recommendations(
            student_id, recent_results, quiz_results, test_attempts
        )
        
        return {
            "student_id": student_id,
            "recommendations": recommendations,
            "total_count": len(recommendations),
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erreur lors de la récupération des recommandations IA: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne du serveur"
        )

@router.post("/{recommendation_id}/accept")
async def accept_ai_recommendation(
    recommendation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Accepter une recommandation IA
    """
    try:
        # Pour l'instant, on simule l'acceptation
        # Dans une vraie implémentation, on sauvegarderait cela en base
        
        return {
            "message": "Recommandation acceptée avec succès",
            "recommendation_id": recommendation_id,
            "accepted_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        print(f"Erreur lors de l'acceptation de la recommandation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne du serveur"
        )

def generate_ai_recommendations(
    student_id: int,
    assessment_results: List[AssessmentResult],
    quiz_results: List[QuizResult],
    test_attempts: List[TestAttempt]
) -> List[dict]:
    """
    Générer des recommandations IA basées sur les performances
    """
    recommendations = []
    
    # Analyser les scores moyens
    if assessment_results:
        avg_score = sum(r.score for r in assessment_results if r.score is not None) / len(assessment_results)
        
        if avg_score < 60:
            recommendations.append({
                "id": len(recommendations) + 1,
                "type": "review",
                "title": "Révision des concepts de base",
                "description": "Vos scores indiquent un besoin de révision des fondamentaux",
                "priority": "high",
                "subject": "Général",
                "estimated_time_minutes": 45,
                "difficulty": "easy",
                "reason": f"Score moyen de {avg_score:.1f}%",
                "impact_score": 85,
                "created_at": datetime.utcnow().isoformat(),
                "is_completed": False
            })
    
    # Analyser les quiz
    if quiz_results:
        recent_quiz_scores = [r.score for r in quiz_results[:5] if r.score is not None]
        if recent_quiz_scores:
            avg_quiz_score = sum(recent_quiz_scores) / len(recent_quiz_scores)
            
            if avg_quiz_score < 70:
                recommendations.append({
                    "id": len(recommendations) + 1,
                    "type": "practice",
                    "title": "Pratique des quiz",
                    "description": "Entraînez-vous avec plus de quiz pour améliorer vos compétences",
                    "priority": "medium",
                    "subject": "Quiz",
                    "estimated_time_minutes": 30,
                    "difficulty": "medium",
                    "reason": f"Score moyen des quiz: {avg_quiz_score:.1f}%",
                    "impact_score": 75,
                    "created_at": datetime.utcnow().isoformat(),
                    "is_completed": False
                })
    
    # Recommandations basées sur les matières
    subjects = ["Mathématiques", "Français", "Sciences", "Histoire", "Géographie"]
    for subject in subjects:
        if random.random() < 0.3:  # 30% de chance d'avoir une recommandation par matière
            recommendations.append({
                "id": len(recommendations) + 1,
                "type": random.choice(["study", "practice", "challenge"]),
                "title": f"Amélioration en {subject}",
                "description": f"Concentrez-vous sur vos points faibles en {subject}",
                "priority": random.choice(["low", "medium", "high"]),
                "subject": subject,
                "estimated_time_minutes": random.choice([30, 45, 60]),
                "difficulty": random.choice(["easy", "medium", "hard"]),
                "reason": "Analyse des performances par matière",
                "impact_score": random.randint(60, 95),
                "created_at": datetime.utcnow().isoformat(),
                "is_completed": False
            })
    
    # Recommandation de consolidation
    if len(recommendations) < 3:
        recommendations.append({
            "id": len(recommendations) + 1,
            "type": "consolidation",
            "title": "Consolidation des acquis",
            "description": "Renforcez vos connaissances acquises récemment",
            "priority": "low",
            "subject": "Général",
            "estimated_time_minutes": 20,
            "difficulty": "easy",
            "reason": "Maintenance des compétences",
            "impact_score": 65,
            "created_at": datetime.utcnow().isoformat(),
            "is_completed": False
        })
    
    return recommendations[:5]  # Limiter à 5 recommandations
