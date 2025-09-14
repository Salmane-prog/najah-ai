#!/usr/bin/env python3
"""
API pour les analytics IA avancées avec données réelles
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, desc, asc, case, extract
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import json

from core.database import get_db
from models.user import User, UserRole
from models.class_group import ClassGroup, ClassStudent
from models.learning_history import LearningHistory
from models.quiz import QuizResult, Quiz
from models.analytics import LearningAnalytics, StudentPrediction, BlockageDetection, LearningPattern
from models.assessment import Assessment, AssessmentResult
from models.homework import AdvancedHomework as Homework, AdvancedHomeworkSubmission as HomeworkSubmission
from core.security import get_current_user
from api.v1.auth import require_role

router = APIRouter(prefix="/ai-analytics", tags=["Analytics IA Avancées"])

# ============================================================================
# ENDPOINT PRINCIPAL - ANALYTICS IA COMPLÈTES
# ============================================================================

@router.get("/")
def get_ai_analytics_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Récupérer toutes les données d'analytics IA pour le professeur"""
    try:
        now = datetime.utcnow()
        week_start = now - timedelta(days=now.weekday())
        month_start = now.replace(day=1)
        
        # 1. ANALYTICS D'APPRENTISSAGE
        learning_analytics = get_learning_analytics(db, current_user.id, week_start, now)
        
        # 2. PRÉDICTIONS IA
        predictions = get_ai_predictions(db, current_user.id)
        
        # 3. DÉTECTION DE BLOCAGES
        blockages = get_learning_blockages(db, current_user.id)
        
        # 4. PATTERNS D'APPRENTISSAGE
        patterns = get_learning_patterns(db, current_user.id)
        
        # 5. RECOMMANDATIONS IA
        recommendations = get_ai_recommendations(db, current_user.id, learning_analytics, predictions, blockages)
        
        return {
            "learning_analytics": learning_analytics,
            "predictions": predictions,
            "blockages": blockages,
            "patterns": patterns,
            "recommendations": recommendations,
            "generated_at": now.isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des analytics IA: {str(e)}")

# ============================================================================
# FONCTIONS HELPER POUR RÉCUPÉRER LES DONNÉES
# ============================================================================

def get_learning_analytics(db: Session, teacher_id: int, week_start: datetime, now: datetime) -> Dict[str, Any]:
    """Récupérer les analytics d'apprentissage"""
    
    class_ids = get_teacher_class_ids(db, teacher_id)
    
    # Statistiques générales
    total_quizzes = db.query(func.count(QuizResult.id)).join(
        ClassStudent, QuizResult.student_id == ClassStudent.student_id
    ).filter(
        ClassStudent.class_id.in_(class_ids),
        QuizResult.created_at >= week_start,
        QuizResult.created_at <= now
    ).scalar() or 0
    
    completed_quizzes = db.query(func.count(QuizResult.id)).join(
        ClassStudent, QuizResult.student_id == ClassStudent.student_id
    ).filter(
        ClassStudent.class_id.in_(class_ids),
        QuizResult.created_at >= week_start,
        QuizResult.created_at <= now,
        QuizResult.status == "completed"
    ).scalar() or 0
    
    completion_rate = round((completed_quizzes / total_quizzes * 100) if total_quizzes > 0 else 0, 1)
    
    # Score moyen récent
    recent_average = db.query(func.avg(QuizResult.score)).join(
        ClassStudent, QuizResult.student_id == ClassStudent.student_id
    ).filter(
        ClassStudent.class_id.in_(class_ids),
        QuizResult.created_at >= week_start,
        QuizResult.created_at <= now
    ).scalar() or 0
    
    # Performance récente vs semaine précédente
    last_week_start = week_start - timedelta(days=7)
    last_week_average = db.query(func.avg(QuizResult.score)).join(
        ClassStudent, QuizResult.student_id == ClassStudent.student_id
    ).filter(
        ClassStudent.class_id.in_(class_ids),
        QuizResult.created_at >= last_week_start,
        QuizResult.created_at < week_start
    ).scalar() or 0
    
    performance_change = 0
    if last_week_average > 0:
        performance_change = round(((recent_average - last_week_average) / last_week_average) * 100, 1)
    
    # Analyse des forces et faiblesses par matière
    subject_analysis = db.query(
        Quiz.subject,
        func.avg(QuizResult.score).label('avg_score'),
        func.count(QuizResult.id).label('quiz_count')
    ).join(
        QuizResult, Quiz.id == QuizResult.quiz_id
    ).join(
        ClassStudent, QuizResult.student_id == ClassStudent.student_id
    ).filter(
        ClassStudent.class_id.in_(class_ids),
        QuizResult.created_at >= week_start,
        QuizResult.created_at <= now
    ).group_by(Quiz.subject).all()
    
    strengths = []
    weaknesses = []
    
    for subject_data in subject_analysis:
        if subject_data.avg_score >= 75:
            strengths.append(subject_data.subject)
        elif subject_data.avg_score < 60:
            weaknesses.append(subject_data.subject)
    
    return {
        "total_quizzes": total_quizzes,
        "completed_quizzes": completed_quizzes,
        "completion_rate": completion_rate,
        "average_score": round(recent_average, 1),
        "recent_performance": round(recent_average, 1),
        "performance_trend": "up" if performance_change > 0 else "down" if performance_change < 0 else "stable",
        "strengths": strengths,
        "weaknesses": weaknesses,
        "subject_analysis": [
            {
                "subject": data.subject,
                "average_score": round(data.avg_score, 1),
                "quiz_count": data.quiz_count
            }
            for data in subject_analysis
        ]
    }

def get_ai_predictions(db: Session, teacher_id: int) -> Dict[str, Any]:
    """Récupérer les prédictions IA"""
    
    class_ids = get_teacher_class_ids(db, teacher_id)
    
    # Prédictions existantes dans la base
    predictions = db.query(StudentPrediction).join(
        ClassStudent, StudentPrediction.student_id == ClassStudent.student_id
    ).filter(
        ClassStudent.class_id.in_(class_ids)
    ).order_by(desc(StudentPrediction.prediction_date)).limit(10).all()
    
    # Si pas de prédictions, générer des prédictions basées sur les données actuelles
    if not predictions:
        predictions = generate_predictions_from_data(db, class_ids)
    
    prediction_data = []
    for pred in predictions:
        student = db.query(User).filter(User.id == pred.student_id).first()
        prediction_data.append({
            "student_name": student.username if student else f"Élève {pred.student_id}",
            "prediction_type": pred.prediction_type,
            "predicted_value": pred.predicted_value,
            "confidence_score": pred.confidence_score,
            "prediction_date": pred.prediction_date.isoformat(),
            "trend": "up" if pred.predicted_value > 70 else "down" if pred.predicted_value < 50 else "stable"
        })
    
    # Statistiques des prédictions
    high_confidence = len([p for p in prediction_data if p["confidence_score"] >= 0.8])
    medium_confidence = len([p for p in prediction_data if 0.6 <= p["confidence_score"] < 0.8])
    low_confidence = len([p for p in prediction_data if p["confidence_score"] < 0.6])
    
    return {
        "predictions": prediction_data,
        "confidence_distribution": {
            "high": high_confidence,
            "medium": medium_confidence,
            "low": low_confidence
        },
        "total_predictions": len(prediction_data)
    }

def generate_predictions_from_data(db: Session, class_ids: List[int]) -> List[StudentPrediction]:
    """Générer des prédictions basées sur les données actuelles"""
    
    # Analyser les performances récentes des étudiants
    recent_performance = db.query(
        QuizResult.student_id,
        func.avg(QuizResult.score).label('avg_score'),
        func.count(QuizResult.id).label('quiz_count')
    ).join(
        ClassStudent, QuizResult.student_id == ClassStudent.student_id
    ).filter(
        ClassStudent.class_id.in_(class_ids),
        QuizResult.created_at >= datetime.utcnow() - timedelta(days=30)
    ).group_by(QuizResult.student_id).all()
    
    predictions = []
    for perf in recent_performance:
        if perf.quiz_count >= 3:  # Au moins 3 quiz pour faire une prédiction
            # Prédiction basée sur la tendance
            predicted_score = min(100, max(0, perf.avg_score + (perf.avg_score * 0.1)))
            confidence = min(0.95, max(0.3, 0.7 + (perf.quiz_count * 0.05)))
            
            # Créer une prédiction simulée
            prediction = StudentPrediction(
                student_id=perf.student_id,
                model_id=1,  # Modèle par défaut
                prediction_type="performance",
                predicted_value=predicted_score,
                confidence_score=confidence,
                prediction_date=datetime.utcnow()
            )
            predictions.append(prediction)
    
    return predictions

def get_learning_blockages(db: Session, teacher_id: int) -> Dict[str, Any]:
    """Récupérer la détection des blocages d'apprentissage"""
    
    class_ids = get_teacher_class_ids(db, teacher_id)
    
    # Blocages existants dans la base
    blockages = db.query(BlockageDetection).join(
        ClassStudent, BlockageDetection.student_id == ClassStudent.student_id
    ).filter(
        ClassStudent.class_id.in_(class_ids)
    ).order_by(desc(BlockageDetection.detected_at)).all()
    
    # Si pas de blocages, analyser les données pour détecter des blocages potentiels
    if not blockages:
        blockages = detect_blockages_from_data(db, class_ids)
    
    blockage_data = []
    for blockage in blockages:
        student = db.query(User).filter(User.id == blockage.student_id).first()
        blockage_data.append({
            "student_name": student.username if student else f"Élève {blockage.student_id}",
            "subject": blockage.subject,
            "concept": blockage.concept,
            "blockage_type": blockage.blockage_type,
            "severity": blockage.severity,
            "symptoms": blockage.symptoms,
            "detected_at": blockage.detected_at.isoformat(),
            "resolved": blockage.resolved_at is not None
        })
    
    # Statistiques des blocages
    high_severity = len([b for b in blockage_data if b["severity"] >= 4])
    medium_severity = len([b for b in blockage_data if b["severity"] == 3])
    low_severity = len([b for b in blockage_data if b["severity"] <= 2])
    
    return {
        "blockages": blockage_data,
        "severity_distribution": {
            "high": high_severity,
            "medium": medium_severity,
            "low": low_severity
        },
        "total_blockages": len(blockage_data),
        "resolved_count": len([b for b in blockage_data if b["resolved"]])
    }

def detect_blockages_from_data(db: Session, class_ids: List[int]) -> List[BlockageDetection]:
    """Détecter les blocages basés sur les données de performance"""
    
    # Analyser les étudiants avec des scores faibles répétés
    struggling_students = db.query(
        QuizResult.student_id,
        Quiz.subject,
        func.avg(QuizResult.score).label('avg_score'),
        func.count(QuizResult.id).label('quiz_count')
    ).join(
        Quiz, QuizResult.quiz_id == Quiz.id
    ).join(
        ClassStudent, QuizResult.student_id == ClassStudent.student_id
    ).filter(
        ClassStudent.class_id.in_(class_ids),
        QuizResult.created_at >= datetime.utcnow() - timedelta(days=30)
    ).group_by(QuizResult.student_id, Quiz.subject).having(
        func.avg(QuizResult.score) < 60,
        func.count(QuizResult.id) >= 2
    ).all()
    
    blockages = []
    for student in struggling_students:
        # Déterminer le type de blocage
        if student.avg_score < 40:
            blockage_type = "cognitive"
            severity = 4
        elif student.avg_score < 50:
            blockage_type = "cognitive"
            severity = 3
        else:
            blockage_type = "motivational"
            severity = 2
        
        # Créer un blocage simulé
        blockage = BlockageDetection(
            student_id=student.student_id,
            subject=student.subject,
            concept="Concepts généraux",
            blockage_type=blockage_type,
            severity=severity,
            symptoms={"low_scores": True, "repeated_failures": True},
            detected_at=datetime.utcnow()
        )
        blockages.append(blockage)
    
    return blockages

def get_learning_patterns(db: Session, teacher_id: int) -> Dict[str, Any]:
    """Récupérer les patterns d'apprentissage"""
    
    class_ids = get_teacher_class_ids(db, teacher_id)
    
    # Patterns existants dans la base
    patterns = db.query(LearningPattern).join(
        ClassStudent, LearningPattern.student_id == ClassStudent.student_id
    ).filter(
        ClassStudent.class_id.in_(class_ids)
    ).order_by(desc(LearningPattern.detected_at)).all()
    
    # Si pas de patterns, analyser les données pour détecter des patterns
    if not patterns:
        patterns = detect_patterns_from_data(db, class_ids)
    
    pattern_data = []
    for pattern in patterns:
        student = db.query(User).filter(User.id == pattern.student_id).first()
        pattern_data.append({
            "student_name": student.username if student else f"Élève {pattern.student_id}",
            "pattern_type": pattern.pattern_type,
            "pattern_data": pattern.pattern_data,
            "confidence": pattern.confidence,
            "detected_at": pattern.detected_at.isoformat()
        })
    
    return {
        "patterns": pattern_data,
        "total_patterns": len(pattern_data),
        "pattern_types": list(set([p["pattern_type"] for p in pattern_data]))
    }

def detect_patterns_from_data(db: Session, class_ids: List[int]) -> List[LearningPattern]:
    """Détecter les patterns basés sur les données d'apprentissage"""
    
    # Analyser les habitudes d'étude
    study_patterns = db.query(
        LearningHistory.student_id,
        extract('hour', LearningHistory.timestamp).label('hour'),
        func.count(LearningHistory.id).label('session_count')
    ).join(
        ClassStudent, LearningHistory.student_id == ClassStudent.student_id
    ).filter(
        ClassStudent.class_id.in_(class_ids),
        LearningHistory.timestamp >= datetime.utcnow() - timedelta(days=30)
    ).group_by(LearningHistory.student_id, extract('hour', LearningHistory.timestamp)).all()
    
    patterns = []
    for pattern in study_patterns:
        if pattern.session_count >= 5:  # Au moins 5 sessions à la même heure
            # Déterminer le type de pattern
            if 8 <= pattern.hour <= 12:
                pattern_type = "morning_study"
                pattern_data = {"preferred_time": "Matin", "session_count": pattern.session_count}
            elif 13 <= pattern.hour <= 17:
                pattern_type = "afternoon_study"
                pattern_data = {"preferred_time": "Après-midi", "session_count": pattern.session_count}
            elif 18 <= pattern.hour <= 22:
                pattern_type = "evening_study"
                pattern_data = {"preferred_time": "Soirée", "session_count": pattern.session_count}
            else:
                pattern_type = "night_study"
                pattern_data = {"preferred_time": "Nuit", "session_count": pattern.session_count}
            
            # Créer un pattern simulé
            learning_pattern = LearningPattern(
                student_id=pattern.student_id,
                pattern_type=pattern_type,
                pattern_data=pattern_data,
                confidence=min(0.95, 0.6 + (pattern.session_count * 0.05)),
                detected_at=datetime.utcnow()
            )
            patterns.append(learning_pattern)
    
    return patterns

def get_ai_recommendations(db: Session, teacher_id: int, learning_analytics: Dict, predictions: Dict, blockages: Dict) -> Dict[str, Any]:
    """Générer des recommandations IA basées sur l'analyse"""
    
    recommendations = []
    
    # Recommandations basées sur les analytics d'apprentissage
    if learning_analytics["weaknesses"]:
        recommendations.append({
            "type": "subject_improvement",
            "priority": "high",
            "title": "Renforcer les matières en difficulté",
            "description": f"Les matières {', '.join(learning_analytics['weaknesses'])} nécessitent une attention particulière",
            "action": "Planifier des sessions de remédiation ciblées",
            "estimated_impact": "Élevé"
        })
    
    if learning_analytics["performance_trend"] == "down":
        recommendations.append({
            "type": "performance_decline",
            "priority": "high",
            "title": "Inverser la tendance de performance",
            "description": "La performance générale est en baisse",
            "action": "Analyser les causes et ajuster la pédagogie",
            "estimated_impact": "Élevé"
        })
    
    # Recommandations basées sur les prédictions
    if predictions["confidence_distribution"]["low"] > predictions["confidence_distribution"]["high"]:
        recommendations.append({
            "type": "prediction_quality",
            "priority": "medium",
            "title": "Améliorer la qualité des prédictions",
            "description": "Trop de prédictions avec une faible confiance",
            "action": "Collecter plus de données d'apprentissage",
            "estimated_impact": "Moyen"
        })
    
    # Recommandations basées sur les blocages
    if blockages["severity_distribution"]["high"] > 0:
        recommendations.append({
            "type": "critical_blockages",
            "priority": "critical",
            "title": "Intervention urgente requise",
            "description": f"{blockages['severity_distribution']['high']} élève(s) avec des blocages critiques",
            "action": "Intervention immédiate et suivi personnalisé",
            "estimated_impact": "Critique"
        })
    
    # Recommandations générales
    if learning_analytics["completion_rate"] < 80:
        recommendations.append({
            "type": "engagement",
            "priority": "medium",
            "title": "Améliorer l'engagement des élèves",
            "description": f"Taux de completion des quiz: {learning_analytics['completion_rate']}%",
            "action": "Rendre les quiz plus attractifs et variés",
            "estimated_impact": "Moyen"
        })
    
    # Si pas de recommandations spécifiques, proposer des améliorations générales
    if not recommendations:
        recommendations = [
            {
                "type": "general_improvement",
                "priority": "low",
                "title": "Maintenir l'excellence",
                "description": "Les performances sont bonnes, continuer sur cette lancée",
                "action": "Surveiller les tendances et maintenir la qualité",
                "estimated_impact": "Faible"
            }
        ]
    
    return {
        "recommendations": recommendations,
        "total_recommendations": len(recommendations),
        "priority_distribution": {
            "critical": len([r for r in recommendations if r["priority"] == "critical"]),
            "high": len([r for r in recommendations if r["priority"] == "high"]),
            "medium": len([r for r in recommendations if r["priority"] == "medium"]),
            "low": len([r for r in recommendations if r["priority"] == "low"])
        }
    }

# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

def get_teacher_class_ids(db: Session, teacher_id: int) -> List[int]:
    """Récupérer les IDs des classes d'un professeur"""
    classes = db.query(ClassGroup.id).filter(ClassGroup.teacher_id == teacher_id).all()
    return [c.id for c in classes]

# ============================================================================
# ENDPOINTS SPÉCIFIQUES POUR LES WIDGETS
# ============================================================================

@router.get("/learning-analytics")
def get_ai_learning_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Récupérer uniquement les analytics d'apprentissage IA"""
    try:
        now = datetime.utcnow()
        week_start = now - timedelta(days=now.weekday())
        learning_analytics = get_learning_analytics(db, current_user.id, week_start, now)
        return learning_analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@router.get("/predictions")
def get_ai_predictions_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Récupérer uniquement les prédictions IA"""
    try:
        predictions = get_ai_predictions(db, current_user.id)
        return predictions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@router.get("/blockages")
def get_ai_blockages_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Récupérer uniquement la détection des blocages"""
    try:
        blockages = get_learning_blockages(db, current_user.id)
        return blockages
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@router.get("/patterns")
def get_ai_patterns_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Récupérer uniquement les patterns d'apprentissage"""
    try:
        patterns = get_learning_patterns(db, current_user.id)
        return patterns
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@router.get("/recommendations")
def get_ai_recommendations_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Récupérer uniquement les recommandations IA"""
    try:
        now = datetime.utcnow()
        week_start = now - timedelta(days=now.weekday())
        learning_analytics = get_learning_analytics(db, current_user.id, week_start, now)
        predictions = get_ai_predictions(db, current_user.id)
        blockages = get_learning_blockages(db, current_user.id)
        recommendations = get_ai_recommendations(db, current_user.id, learning_analytics, predictions, blockages)
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")
