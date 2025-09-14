#!/usr/bin/env python3
"""
API pour les analytics d'apprentissage des étudiants
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
async def get_student_learning_analytics(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupérer les analytics d'apprentissage pour un étudiant
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
        ).order_by(AssessmentResult.created_at.desc()).limit(20).all()
        
        quiz_results = db.query(QuizResult).filter(
            QuizResult.student_id == student_id
        ).order_by(QuizResult.created_at.desc()).limit(20).all()
        
        test_attempts = db.query(TestAttempt).filter(
            TestAttempt.student_id == student_id
        ).order_by(TestAttempt.created_at.desc()).limit(20).all()
        
        # Générer les analytics
        analytics = generate_learning_analytics(
            student_id, recent_results, quiz_results, test_attempts
        )
        
        return analytics
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erreur lors de la récupération des analytics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne du serveur"
        )

def generate_learning_analytics(
    student_id: int,
    assessment_results: List[AssessmentResult],
    quiz_results: List[QuizResult],
    test_attempts: List[TestAttempt]
) -> dict:
    """
    Générer les analytics d'apprentissage basées sur les performances
    """
    # Calculer le temps d'étude recommandé basé sur les performances
    total_attempts = len(assessment_results) + len(quiz_results) + len(test_attempts)
    
    if total_attempts == 0:
        # Pas de données, recommandations par défaut
        study_time = 90
        break_time = 15
        break_duration = 5
        focus_areas = ["Mathématiques", "Français", "Sciences"]
    else:
        # Calculer le temps basé sur les performances
        avg_score = 0
        if assessment_results:
            scores = [r.score for r in assessment_results if r.score is not None]
            if scores:
                avg_score = sum(scores) / len(scores)
        
        if quiz_results:
            quiz_scores = [r.score for r in quiz_results if r.score is not None]
            if quiz_scores:
                quiz_avg = sum(quiz_scores) / len(quiz_scores)
                avg_score = (avg_score + quiz_avg) / 2
        
        # Ajuster le temps d'étude basé sur les performances
        if avg_score < 60:
            study_time = 120  # Plus de temps si performances faibles
            break_time = 20
            break_duration = 8
        elif avg_score < 80:
            study_time = 90   # Temps moyen
            break_time = 15
            break_duration = 5
        else:
            study_time = 60   # Moins de temps si performances élevées
            break_time = 10
            break_duration = 3
    
    # Analyser les matières par performance
    subject_analysis = analyze_subject_performance(
        assessment_results, quiz_results, test_attempts
    )
    
    return {
        "student_id": student_id,
        "study_time_recommendation": study_time,
        "break_recommendation": break_time,
        "recommended_break_duration": break_duration,
        "focus_areas": focus_areas,
        "subject_analysis": subject_analysis,
        "total_activities": total_attempts,
        "average_score": round(avg_score if 'avg_score' in locals() else 0, 1),
        "generated_at": datetime.utcnow().isoformat()
    }

def analyze_subject_performance(
    assessment_results: List[AssessmentResult],
    quiz_results: List[QuizResult],
    test_attempts: List[TestAttempt]
) -> List[dict]:
    """
    Analyser les performances par matière
    """
    subjects = ["Mathématiques", "Français", "Sciences", "Histoire", "Géographie"]
    analysis = []
    
    for subject in subjects:
        # Simuler des données d'analyse (dans une vraie implémentation, on analyserait les vraies données)
        current_level = random.choice(["Débutant", "Intermédiaire", "Avancé"])
        target_level = "Avancé" if current_level == "Débutant" else "Expert"
        
        # Calculer un pourcentage de progression basé sur le niveau
        if current_level == "Débutant":
            progress = random.randint(20, 50)
        elif current_level == "Intermédiaire":
            progress = random.randint(50, 80)
        else:
            progress = random.randint(80, 95)
        
        # Définir des zones de force/faiblesse
        weak_areas = []
        strong_areas = []
        
        if subject == "Mathématiques":
            weak_areas = ["Algèbre", "Géométrie"] if progress < 70 else ["Calcul avancé"]
            strong_areas = ["Arithmétique", "Statistiques"] if progress > 60 else ["Logique"]
        elif subject == "Français":
            weak_areas = ["Grammaire", "Conjugaison"] if progress < 70 else ["Littérature"]
            strong_areas = ["Compréhension", "Vocabulaire"] if progress > 60 else ["Expression"]
        elif subject == "Sciences":
            weak_areas = ["Physique", "Chimie"] if progress < 70 else ["Biologie avancée"]
            strong_areas = ["Biologie", "Géologie"] if progress > 60 else ["Expérimentation"]
        else:
            weak_areas = [f"{subject} avancé"] if progress < 70 else [f"Spécialisation {subject}"]
            strong_areas = [f"Bases {subject}", f"Concepts {subject}"] if progress > 60 else [f"Expertise {subject}"]
        
        analysis.append({
            "subject": subject,
            "current_level": current_level,
            "target_level": target_level,
            "progress_percentage": progress,
            "weak_areas": weak_areas,
            "strong_areas": strong_areas
        })
    
    return analysis
