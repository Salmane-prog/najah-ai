from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from core.database import get_db
from models.user import User
from models.quiz import QuizResult
from models.content import Content
from models.assessment import Assessment, AssessmentResult
from api.v1.users import get_current_user
from api.v1.auth import require_role
from typing import List, Dict, Any
from datetime import datetime, timedelta
import json

router = APIRouter()

@router.get("/student/{student_id}/personalized")
def get_personalized_recommendations(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Obtenir des recommandations personnalisées pour un étudiant."""
    
    # Vérifier que l'étudiant accède à ses propres données
    if current_user.id != student_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    # Analyser les performances récentes
    recent_results = db.query(QuizResult).filter(
        QuizResult.student_id == student_id,
        QuizResult.is_completed == True
    ).order_by(QuizResult.created_at.desc()).limit(20).all()
    
    # Analyser l'évaluation initiale
    assessment = db.query(Assessment).filter(
        Assessment.student_id == student_id,
        Assessment.assessment_type == "initial"
    ).order_by(Assessment.completed_at.desc()).first()
    
    recommendations = []
    
    if assessment:
        result = db.query(AssessmentResult).filter(
            AssessmentResult.assessment_id == assessment.id
        ).first()
        
        if result:
            subject_scores = json.loads(result.subject_scores)
            
            # Recommandations basées sur les faiblesses identifiées
            for subject, scores in subject_scores.items():
                if scores["correct"] / scores["total"] < 0.7:
                    # Trouver du contenu de remédiation
                    remediation_content = db.query(Content).filter(
                        Content.subject == subject,
                        Content.level == "beginner",
                        Content.is_active == True
                    ).limit(3).all()
                    
                    for content in remediation_content:
                        recommendations.append({
                            "type": "remediation",
                            "title": f"Remédiation en {subject}",
                            "description": content.description,
                            "content_id": content.id,
                            "priority": "high",
                            "reason": f"Difficulté identifiée en {subject}",
                            "estimated_time": content.estimated_time
                        })
    
    # Recommandations basées sur les performances récentes
    if recent_results:
        # Analyser les tendances
        subject_performance = {}
        for result in recent_results:
            if result.sujet not in subject_performance:
                subject_performance[result.sujet] = []
            subject_performance[result.sujet].append(result.score)
        
        # Identifier les sujets en difficulté
        weak_subjects = []
        for subject, scores in subject_performance.items():
            avg_score = sum(scores) / len(scores)
            if avg_score < 70:
                weak_subjects.append(subject)
        
        # Recommandations de consolidation
        for subject in weak_subjects:
            consolidation_content = db.query(Content).filter(
                Content.subject == subject,
                Content.level == "intermediate",
                Content.is_active == True
            ).limit(2).all()
            
            for content in consolidation_content:
                recommendations.append({
                    "type": "consolidation",
                    "title": f"Consolidation en {subject}",
                    "description": content.description,
                    "content_id": content.id,
                    "priority": "medium",
                    "reason": f"Performance récente faible en {subject}",
                    "estimated_time": content.estimated_time
                })
        
        # Recommandations de défi si l'étudiant performe bien
        recent_avg = sum(r.score for r in recent_results[:5]) / min(5, len(recent_results))
        if recent_avg >= 80:
            challenge_content = db.query(Content).filter(
                Content.level == "advanced",
                Content.is_active == True
            ).limit(2).all()
            
            for content in challenge_content:
                recommendations.append({
                    "type": "challenge",
                    "title": f"Défi - {content.title}",
                    "description": content.description,
                    "content_id": content.id,
                    "priority": "low",
                    "reason": "Excellentes performances récentes",
                    "estimated_time": content.estimated_time
                })
    
    # Recommandations de découverte (si pas assez de recommandations)
    if len(recommendations) < 5:
        discovery_content = db.query(Content).filter(
            Content.is_active == True
        ).order_by(func.random()).limit(5 - len(recommendations)).all()
        
        for content in discovery_content:
            recommendations.append({
                "type": "discovery",
                "title": f"Découverte - {content.title}",
                "description": content.description,
                "content_id": content.id,
                "priority": "low",
                "reason": "Contenu recommandé pour vous",
                "estimated_time": content.estimated_time
            })
    
    return {
        "student_id": student_id,
        "recommendations": recommendations,
        "analysis": {
            "total_recent_quizzes": len(recent_results),
            "average_recent_score": sum(r.score for r in recent_results) / len(recent_results) if recent_results else 0,
            "weak_subjects": weak_subjects if 'weak_subjects' in locals() else [],
            "has_assessment": assessment is not None
        }
    }

@router.get("/student/{student_id}/adaptive")
def get_adaptive_recommendations(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Obtenir des recommandations adaptatives en temps réel."""
    
    # Vérifier que l'étudiant accède à ses propres données
    if current_user.id != student_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    # Analyser le comportement d'apprentissage
    learning_patterns = analyze_learning_patterns(student_id, db)
    
    # Générer des recommandations adaptatives
    adaptive_recommendations = []
    
    # Recommandations basées sur le rythme d'apprentissage
    if learning_patterns["avg_session_duration"] < 15:
        # Sessions courtes, proposer du contenu court
        short_content = db.query(Content).filter(
            Content.estimated_time <= 15,
            Content.is_active == True
        ).limit(3).all()
        
        for content in short_content:
            adaptive_recommendations.append({
                "type": "short_session",
                "title": f"Session courte - {content.title}",
                "description": content.description,
                "content_id": content.id,
                "priority": "medium",
                "reason": "Adapté à votre rythme d'apprentissage",
                "estimated_time": content.estimated_time
            })
    
    # Recommandations basées sur les préférences de contenu
    if learning_patterns["preferred_content_types"]:
        for content_type in learning_patterns["preferred_content_types"][:2]:
            preferred_content = db.query(Content).filter(
                Content.content_type == content_type,
                Content.is_active == True
            ).limit(2).all()
            
            for content in preferred_content:
                adaptive_recommendations.append({
                    "type": "preference",
                    "title": f"Selon vos préférences - {content.title}",
                    "description": content.description,
                    "content_id": content.id,
                    "priority": "medium",
                    "reason": f"Basé sur votre préférence pour le contenu {content_type}",
                    "estimated_time": content.estimated_time
                })
    
    return {
        "student_id": student_id,
        "adaptive_recommendations": adaptive_recommendations,
        "learning_patterns": learning_patterns
    }

def analyze_learning_patterns(student_id: int, db: Session) -> Dict[str, Any]:
    """Analyser les patterns d'apprentissage d'un étudiant."""
    
    # Analyser les sessions d'apprentissage récentes
    recent_activity = db.query(QuizResult).filter(
        QuizResult.student_id == student_id,
        QuizResult.created_at >= datetime.utcnow() - timedelta(days=30)
    ).all()
    
    if not recent_activity:
        return {
            "avg_session_duration": 0,
            "preferred_content_types": [],
            "learning_consistency": 0,
            "peak_learning_hours": []
        }
    
    # Calculer la durée moyenne des sessions
    session_durations = []
    for result in recent_activity:
        if result.started_at and result.completed_at:
            duration = (result.completed_at - result.started_at).total_seconds() / 60
            session_durations.append(duration)
    
    avg_session_duration = sum(session_durations) / len(session_durations) if session_durations else 0
    
    # Analyser les types de contenu préférés (basé sur les sujets)
    subject_preferences = {}
    for result in recent_activity:
        if result.sujet not in subject_preferences:
            subject_preferences[result.sujet] = 0
        subject_preferences[result.sujet] += 1
    
    preferred_subjects = sorted(subject_preferences.items(), key=lambda x: x[1], reverse=True)[:3]
    
    # Analyser la cohérence d'apprentissage
    learning_days = set()
    for result in recent_activity:
        learning_days.add(result.created_at.date())
    
    learning_consistency = len(learning_days) / 30  # Pourcentage de jours avec activité
    
    return {
        "avg_session_duration": avg_session_duration,
        "preferred_content_types": [subject for subject, _ in preferred_subjects],
        "learning_consistency": learning_consistency,
        "peak_learning_hours": [],  # À implémenter avec plus de données
        "total_sessions": len(recent_activity)
    } 