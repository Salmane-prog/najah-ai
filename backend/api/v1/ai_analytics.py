#!/usr/bin/env python3
"""
API pour les analytics et la progression des étudiants
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import json

from core.database import get_db
from models.user import User
from models.analytics import (
    LearningAnalytics, PredictiveModel, StudentPrediction, LearningPattern,
    BlockageDetection, TeacherDashboard, ParentDashboard, AutomatedReport, ReportRecipient
)
from core.security import get_current_user

router = APIRouter(prefix="/analytics", tags=["Analytics et Reporting"])

# ============================================================================
# ANALYTICS D'APPRENTISSAGE
# ============================================================================

@router.get("/learning-analytics/{student_id}")
def get_student_learning_analytics(
    student_id: int,
    subject: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les analytics d'apprentissage d'un étudiant"""
    # Vérifier les permissions (étudiant ou enseignant)
    if current_user.role != "teacher" and current_user.id != student_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    query = db.query(LearningAnalytics).filter(LearningAnalytics.student_id == student_id)
    
    if subject:
        query = query.filter(LearningAnalytics.subject == subject)
    
    if date_from:
        query = query.filter(LearningAnalytics.date >= date_from)
    
    if date_to:
        query = query.filter(LearningAnalytics.date <= date_to)
    
    analytics = query.order_by(desc(LearningAnalytics.date)).all()
    
    # Calculer les métriques agrégées
    total_time = sum(a.time_spent or 0 for a in analytics)
    total_questions = sum(a.questions_attempted or 0 for a in analytics)
    total_correct = sum(a.questions_correct or 0 for a in analytics)
    avg_accuracy = (total_correct / total_questions * 100) if total_questions > 0 else 0
    
    return {
        "student_id": student_id,
        "analytics": [
            {
                "date": analytics_item.date,
                "subject": analytics_item.subject,
                "time_spent": analytics_item.time_spent,
                "questions_attempted": analytics_item.questions_attempted,
                "questions_correct": analytics_item.questions_correct,
                "accuracy_rate": analytics_item.accuracy_rate,
                "difficulty_level": analytics_item.difficulty_level,
                "session_count": analytics_item.session_count,
                "resource_access_count": analytics_item.resource_access_count,
                "interaction_count": analytics_item.interaction_count,
                "concept_mastery": analytics_item.concept_mastery,
                "learning_speed": analytics_item.learning_speed,
                "retention_rate": analytics_item.retention_rate
            }
            for analytics_item in analytics
        ],
        "summary": {
            "total_time_spent": total_time,
            "total_questions_attempted": total_questions,
            "total_questions_correct": total_correct,
            "average_accuracy": avg_accuracy,
            "total_sessions": sum(a.session_count or 0 for a in analytics),
            "total_resources_accessed": sum(a.resource_access_count or 0 for a in analytics)
        }
    }

@router.get("/class-analytics/{class_id}")
def get_class_learning_analytics(
    class_id: int,
    subject: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les analytics d'apprentissage d'une classe"""
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Accès réservé aux enseignants")
    
    # Récupérer tous les étudiants de la classe
    # Note: Cette logique dépend de votre modèle de classe
    # students = db.query(User).filter(User.class_id == class_id).all()
    
    # Pour l'instant, retourner des données de démonstration
    return {
        "class_id": class_id,
        "subject": subject,
        "total_students": 25,
        "average_performance": 78.5,
        "performance_distribution": {
            "excellent": 5,
            "good": 12,
            "average": 6,
            "below_average": 2
        },
        "top_performers": [
            {"student_id": 1, "name": "Alice Martin", "score": 95},
            {"student_id": 2, "name": "Bob Dupont", "score": 92},
            {"student_id": 3, "name": "Claire Moreau", "score": 89}
        ],
        "subjects_performance": {
            "Français": 82.3,
            "Mathématiques": 75.8,
            "Histoire": 79.1,
            "Sciences": 76.9
        }
    }

# ============================================================================
# ANALYSE PRÉDICTIVE
# ============================================================================

@router.get("/predictive-models")
def get_predictive_models(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer tous les modèles prédictifs disponibles"""
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    models = db.query(PredictiveModel).filter(PredictiveModel.is_active == True).all()
    
    return {
        "models": [
            {
                "id": model.id,
                "name": model.name,
                "model_type": model.model_type,
                "algorithm": model.algorithm,
                "version": model.version,
                "accuracy": model.accuracy,
                "precision": model.precision,
                "recall": model.recall,
                "f1_score": model.f1_score,
                "created_at": model.created_at
            }
            for model in models
        ]
    }

@router.get("/predictions/{student_id}")
def get_student_predictions(
    student_id: int,
    prediction_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les prédictions pour un étudiant"""
    # Vérifier les permissions
    if current_user.role != "teacher" and current_user.id != student_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    query = db.query(StudentPrediction).filter(StudentPrediction.student_id == student_id)
    
    if prediction_type:
        query = query.filter(StudentPrediction.prediction_type == prediction_type)
    
    predictions = query.order_by(desc(StudentPrediction.prediction_date)).all()
    
    return {
        "student_id": student_id,
        "predictions": [
            {
                "id": pred.id,
                "prediction_type": pred.prediction_type,
                "predicted_value": pred.predicted_value,
                "confidence_score": pred.confidence_score,
                "prediction_date": pred.prediction_date,
                "actual_value": pred.actual_value,
                "accuracy": pred.accuracy,
                "model": {
                    "id": pred.model.id,
                    "name": pred.model.name,
                    "algorithm": pred.model.algorithm
                } if pred.model else None
            }
            for pred in predictions
        ]
    }

@router.post("/predictions/generate")
def generate_prediction(
    prediction_request: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Générer une nouvelle prédiction pour un étudiant"""
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    # Logique de génération de prédiction
    # Pour l'instant, retourner une prédiction simulée
    prediction = StudentPrediction(
        student_id=prediction_request["student_id"],
        model_id=prediction_request.get("model_id"),
        prediction_type=prediction_request["prediction_type"],
        predicted_value=prediction_request.get("predicted_value", 75.0),
        confidence_score=prediction_request.get("confidence_score", 0.85),
        prediction_interval={"lower": 70.0, "upper": 80.0}
    )
    
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    
    return {
        "prediction_id": prediction.id,
        "predicted_value": prediction.predicted_value,
        "confidence_score": prediction.confidence_score,
        "prediction_date": prediction.prediction_date
    }

# ============================================================================
# DÉTECTION DES BLOCAGES
# ============================================================================

@router.get("/blockage-detection/{student_id}")
def get_student_blockages(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les blocages détectés pour un étudiant"""
    # Vérifier les permissions
    if current_user.role != "teacher" and current_user.id != student_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    blockages = db.query(BlockageDetection).filter(
        BlockageDetection.student_id == student_id
    ).order_by(desc(BlockageDetection.detected_at)).all()
    
    return {
        "student_id": student_id,
        "blockages": [
            {
                "id": blockage.id,
                "subject": blockage.subject,
                "concept": blockage.concept,
                "blockage_type": blockage.blockage_type,
                "severity": blockage.severity,
                "symptoms": blockage.symptoms,
                "detected_at": blockage.detected_at,
                "resolved_at": blockage.resolved_at,
                "resolution_strategy": blockage.resolution_strategy
            }
            for blockage in blockages
        ]
    }

@router.post("/blockage-detection/analyze")
def analyze_student_blockages(
    analysis_request: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Analyser et détecter les blocages d'un étudiant"""
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    # Logique d'analyse des blocages
    # Pour l'instant, retourner une détection simulée
    blockage = BlockageDetection(
        student_id=analysis_request["student_id"],
        subject=analysis_request["subject"],
        concept=analysis_request.get("concept", "Concept général"),
        blockage_type="cognitive",
        severity=3,
        symptoms=["Réponses incorrectes répétées", "Temps de réponse élevé"],
        detected_at=datetime.utcnow()
    )
    
    db.add(blockage)
    db.commit()
    db.refresh(blockage)
    
    return {
        "blockage_id": blockage.id,
        "detected_at": blockage.detected_at,
        "severity": blockage.severity,
        "recommendations": [
            "Révision des concepts de base",
            "Exercices de renforcement",
            "Support pédagogique supplémentaire"
        ]
    }

# ============================================================================
# TABLEAUX DE BORD
# ============================================================================

@router.get("/teacher-dashboard/{teacher_id}")
def get_teacher_dashboard(
    teacher_id: int,
    dashboard_type: str = "class_overview",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer le tableau de bord d'un enseignant"""
    if current_user.role != "teacher" or current_user.id != teacher_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    # Récupérer la configuration du tableau de bord
    dashboard = db.query(TeacherDashboard).filter(
        TeacherDashboard.teacher_id == teacher_id,
        TeacherDashboard.dashboard_type == dashboard_type
    ).first()
    
    # Données du tableau de bord (simulées pour l'instant)
    dashboard_data = {
        "teacher_id": teacher_id,
        "dashboard_type": dashboard_type,
        "last_updated": datetime.utcnow(),
        "overview": {
            "total_students": 125,
            "active_courses": 8,
            "average_performance": 78.5,
            "attendance_rate": 94.2
        },
        "recent_activities": [
            {"type": "quiz_completed", "student": "Alice Martin", "score": 95, "time": "2h ago"},
            {"type": "assignment_submitted", "student": "Bob Dupont", "status": "pending", "time": "4h ago"},
            {"type": "performance_alert", "student": "Claire Moreau", "issue": "Declining scores", "time": "1d ago"}
        ],
        "performance_metrics": {
            "subject_performance": {
                "Français": {"average": 82.3, "trend": "up"},
                "Mathématiques": {"average": 75.8, "trend": "stable"},
                "Histoire": {"average": 79.1, "trend": "up"},
                "Sciences": {"average": 76.9, "trend": "down"}
            },
            "class_comparison": {
                "class_6A": 81.2,
                "class_6B": 78.9,
                "class_6C": 75.4
            }
        }
    }
    
    return dashboard_data

@router.get("/parent-dashboard/{parent_id}")
def get_parent_dashboard(
    parent_id: int,
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer le tableau de bord d'un parent"""
    if current_user.role != "parent" or current_user.id != parent_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    # Données du tableau de bord parent (simulées)
    dashboard_data = {
        "parent_id": parent_id,
        "student_id": student_id,
        "last_updated": datetime.utcnow(),
        "student_info": {
            "name": "Alice Martin",
            "grade": "6ème",
            "overall_performance": 85.2
        },
        "academic_progress": {
            "current_subjects": ["Français", "Mathématiques", "Histoire", "Sciences"],
            "subject_performance": {
                "Français": {"score": 88, "trend": "up", "rank": "2/25"},
                "Mathématiques": {"score": 82, "trend": "stable", "rank": "5/25"},
                "Histoire": {"score": 91, "trend": "up", "rank": "1/25"},
                "Sciences": {"score": 79, "trend": "down", "rank": "8/25"}
            }
        },
        "recent_activities": [
            {"date": "2024-01-15", "activity": "Quiz Français", "score": 95, "status": "completed"},
            {"date": "2024-01-14", "activity": "Devoir Mathématiques", "score": 78, "status": "completed"},
            {"date": "2024-01-13", "activity": "Exercice Histoire", "score": 92, "status": "completed"}
        ],
        "recommendations": [
            "Continuer l'excellent travail en Histoire",
            "Réviser les concepts de base en Sciences",
            "Maintenir le bon niveau en Français"
        ]
    }
    
    return dashboard_data

# ============================================================================
# RAPPORTS AUTOMATISÉS
# ============================================================================

@router.get("/automated-reports")
def get_automated_reports(
    report_type: Optional[str] = None,
    target_audience: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les rapports automatisés"""
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    query = db.query(AutomatedReport)
    
    if report_type:
        query = query.filter(AutomatedReport.report_type == report_type)
    
    if target_audience:
        query = query.filter(AutomatedReport.target_audience == target_audience)
    
    reports = query.order_by(desc(AutomatedReport.generated_at)).all()
    
    return {
        "reports": [
            {
                "id": report.id,
                "report_type": report.report_type,
                "target_audience": report.target_audience,
                "generated_at": report.generated_at,
                "sent_at": report.sent_at,
                "status": report.status
            }
            for report in reports
        ]
    }

@router.post("/automated-reports/generate")
def generate_automated_report(
    report_request: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Générer un nouveau rapport automatisé"""
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    # Logique de génération de rapport
    report = AutomatedReport(
        report_type=report_request["report_type"],
        target_audience=report_request["target_audience"],
        report_data=report_request.get("report_data", {}),
        status="generated"
    )
    
    db.add(report)
    db.commit()
    db.refresh(report)
    
    return {
        "report_id": report.id,
        "status": report.status,
        "generated_at": report.generated_at
    } 