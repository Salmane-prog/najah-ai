from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from datetime import datetime, timedelta
from core.database import get_db
from core.security import get_current_user, require_role
from models.reports import (
    DetailedReport, SubjectProgressReport, AnalyticsReport, ReportExport
)
from models.user import User, UserRole
from pydantic import BaseModel
from models.quiz import QuizResult  # Correction de l'import

# ============================================================================
# MODÈLES PYDANTIC POUR LES REQUÊTES
# ============================================================================

class CreateDetailedReportData(BaseModel):
    report_type: str
    title: str
    description: Optional[str] = None
    period_start: str
    period_end: str

class CreateSubjectProgressReportData(BaseModel):
    subject: str
    period_start: str
    period_end: str

class CreateAnalyticsReportData(BaseModel):
    analytics_type: str
    period_start: str
    period_end: str

router = APIRouter(tags=["reports"])

# Pydantic models
class DetailedReportCreate(BaseModel):
    report_type: str
    title: str
    description: Optional[str] = None
    period_start: datetime
    period_end: datetime

class SubjectProgressReportCreate(BaseModel):
    subject: str
    period_start: datetime
    period_end: datetime

class AnalyticsReportCreate(BaseModel):
    analytics_type: str
    period_start: datetime
    period_end: datetime

class DetailedReportResponse(BaseModel):
    id: int
    user_id: int
    report_type: str
    title: str
    description: Optional[str]
    period_start: datetime
    period_end: datetime
    data: dict
    insights: Optional[str]
    recommendations: Optional[dict]
    is_exported: bool
    exported_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True

class SubjectProgressReportResponse(BaseModel):
    id: int
    user_id: int
    subject: str
    period_start: datetime
    period_end: datetime
    total_score: float
    max_score: float
    percentage: float
    improvement_rate: Optional[float]
    topics_covered: Optional[dict]
    strengths: Optional[dict]
    weaknesses: Optional[dict]
    recommendations: Optional[dict]
    created_at: datetime
    
    class Config:
        from_attributes = True

class AnalyticsReportResponse(BaseModel):
    id: int
    user_id: int
    analytics_type: str
    period_start: datetime
    period_end: datetime
    metrics: dict
    trends: Optional[dict]
    insights: Optional[str]
    recommendations: Optional[dict]
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============================================================================
# ENDPOINT DE TEST PUBLIC
# ============================================================================

@router.get("/test")
def test_reports_endpoint():
    """Endpoint de test public pour vérifier que l'API fonctionne"""
    return {
        "message": "API Reports fonctionne correctement",
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "endpoints_available": [
            "/api/v1/reports/detailed",
            "/api/v1/reports/subject-progress", 
            "/api/v1/reports/analytics",
            "/api/v1/reports/test"
        ]
    }

@router.get("/debug")
def debug_reports_endpoint(db: Session = Depends(get_db)):
    """Endpoint de débogage pour voir les données brutes"""
    try:
        # Récupérer un rapport simple
        result = db.execute(text("SELECT id, title FROM detailed_reports LIMIT 1")).fetchone()
        if result:
            return {
                "success": True,
                "data": {"id": result[0], "title": result[1]},
                "message": "Données récupérées avec succès"
            }
        else:
            return {
                "success": True,
                "data": None,
                "message": "Aucun rapport trouvé"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Erreur lors de la récupération"
        }

# ============================================================================
# ENDPOINTS MANQUANTS - RAPPORTS
# ============================================================================

@router.get("/detailed")
def get_detailed_reports(
    report_type: str = None,
    limit: int = 10,
    db: Session = Depends(get_db)
    # Temporairement sans authentification pour le développement
):
    """Récupérer les rapports détaillés (développement sans authentification)"""
    try:
        # Utiliser du SQL direct pour éviter les problèmes de modèles
        sql = "SELECT * FROM detailed_reports"
        
        if report_type:
            sql += " WHERE report_type = :report_type"
            sql += " ORDER BY created_at DESC LIMIT :limit"
            reports = db.execute(text(sql), {"report_type": report_type, "limit": limit}).fetchall()
        else:
            sql += " ORDER BY created_at DESC LIMIT :limit"
            reports = db.execute(text(sql), {"limit": limit}).fetchall()
        
        # Convertir en dictionnaires
        serialized_reports = []
        for report in reports:
            serialized_reports.append({
                "id": report[0],
                "user_id": report[1],
                "report_type": report[2],
                "title": report[3],
                "description": report[4],
                "period_start": report[5],
                "period_end": report[6],
                "data": report[7] if report[7] else "",
                "insights": report[8] if report[8] else "",
                "recommendations": report[9] if report[9] else "",
                "is_exported": bool(report[10]),
                "exported_at": report[11],
                "created_at": report[12]
            })
        
        return {
            "reports": serialized_reports,
            "total": len(serialized_reports)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des rapports: {str(e)}")

@router.get("/detailed/{report_id}")
def get_detailed_report(
    report_id: int,
    db: Session = Depends(get_db)
    # Temporairement sans authentification pour le développement
):
    """Récupérer un rapport détaillé spécifique (développement sans authentification)"""
    try:
        report = db.query(DetailedReport).filter(DetailedReport.id == report_id).first()
        
        if not report:
            raise HTTPException(status_code=404, detail="Rapport non trouvé")
        
        return report
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération du rapport: {str(e)}")

@router.post("/detailed")
def create_detailed_report(
    data: CreateDetailedReportData,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'student']))
):
    """Créer un nouveau rapport détaillé"""
    try:
        report = DetailedReport(
            user_id=current_user.id,
            report_type=data.report_type,
            title=data.title,
            description=data.description,
            period_start=datetime.fromisoformat(data.period_start),
            period_end=datetime.fromisoformat(data.period_end),
            data={},  # Données vides par défaut
            insights="",
            recommendations={}
        )
        
        db.add(report)
        db.commit()
        db.refresh(report)
        
        return report
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création du rapport: {str(e)}")

@router.get("/subject-progress")
def get_subject_progress_reports(
    subject: str = None,
    limit: int = 10,
    db: Session = Depends(get_db)
    # Temporairement sans authentification pour le développement
):
    """Récupérer les rapports de progression par matière (développement sans authentification)"""
    try:
        # Utiliser du SQL direct pour éviter les problèmes de modèles
        sql = "SELECT * FROM subject_progress_reports"
        
        if subject:
            sql += " WHERE subject = :subject"
            sql += " ORDER BY created_at DESC LIMIT :limit"
            reports = db.execute(text(sql), {"subject": subject, "limit": limit}).fetchall()
        else:
            sql += " ORDER BY created_at DESC LIMIT :limit"
            reports = db.execute(text(sql), {"limit": limit}).fetchall()
        
        # Convertir en dictionnaires
        serialized_reports = []
        for report in reports:
            serialized_reports.append({
                "id": report[0],
                "user_id": report[1],
                "subject": report[2],
                "period_start": report[3],
                "period_end": report[4],
                "total_score": report[5],
                "max_score": report[6],
                "percentage": report[7],
                "improvement_rate": report[8],
                "topics_covered": report[9] if report[9] else "",
                "strengths": report[10] if report[10] else "",
                "weaknesses": report[11] if report[11] else "",
                "recommendations": report[12] if report[12] else "",
                "created_at": report[13]
            })
        
        return {
            "reports": serialized_reports,
            "total": len(serialized_reports)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des rapports: {str(e)}")

@router.post("/subject-progress")
def create_subject_progress_report(
    data: CreateSubjectProgressReportData,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'student']))
):
    """Créer un nouveau rapport de progression par matière"""
    try:
        # Calculer le pourcentage basé sur les scores existants
        quiz_results = db.query(QuizResult).filter(
            QuizResult.student_id == current_user.id
        ).all()
        
        total_score = sum(result.score for result in quiz_results) if quiz_results else 0
        max_score = sum(result.max_score for result in quiz_results) if quiz_results else 100
        
        percentage = (total_score / max_score * 100) if max_score > 0 else 0
        
        report = SubjectProgressReport(
            user_id=current_user.id,
            subject=data.subject,
            period_start=datetime.fromisoformat(data.period_start),
            period_end=datetime.fromisoformat(data.period_end),
            total_score=total_score,
            max_score=max_score,
            percentage=percentage,
            improvement_rate=0.0,
            topics_covered=[],
            strengths=[],
            weaknesses=[],
            recommendations=[]
        )
        
        db.add(report)
        db.commit()
        db.refresh(report)
        
        return report
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création du rapport: {str(e)}")

@router.get("/analytics")
def get_analytics_reports(
    analytics_type: str = None,
    limit: int = 10,
    db: Session = Depends(get_db)
    # Temporairement sans authentification pour le développement
):
    """Récupérer les rapports d'analytics (développement sans authentification)"""
    try:
        # Utiliser du SQL direct pour éviter les problèmes de modèles
        sql = "SELECT * FROM analytics_reports"
        
        if analytics_type:
            sql += " WHERE analytics_type = :analytics_type"
            sql += " ORDER BY created_at DESC LIMIT :limit"
            reports = db.execute(text(sql), {"analytics_type": analytics_type, "limit": limit}).fetchall()
        else:
            sql += " ORDER BY created_at DESC LIMIT :limit"
            reports = db.execute(text(sql), {"limit": limit}).fetchall()
        
        # Convertir en dictionnaires
        serialized_reports = []
        for report in reports:
            serialized_reports.append({
                "id": report[0],
                "user_id": report[1],
                "analytics_type": report[2],
                "period_start": report[3],
                "period_end": report[4],
                "metrics": report[5] if report[5] else "",
                "trends": report[6] if report[6] else "",
                "insights": report[7] if report[7] else "",
                "recommendations": report[8] if report[8] else "",
                "created_at": report[9]
            })
        
        return {
            "reports": serialized_reports,
            "total": len(serialized_reports)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des rapports: {str(e)}")

@router.post("/analytics")
def create_analytics_report(
    data: CreateAnalyticsReportData,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'student']))
):
    """Créer un nouveau rapport d'analytics"""
    try:
        # Générer des métriques basées sur les données existantes
        quiz_results = db.query(QuizResult).filter(
            QuizResult.student_id == current_user.id
        ).all()
        
        metrics = {
            "total_quizzes": len(quiz_results),
            "average_score": sum(result.score for result in quiz_results) / len(quiz_results) if quiz_results else 0,
            "total_time": sum(result.time_taken for result in quiz_results if result.time_taken) or 0
        }
        
        report = AnalyticsReport(
            user_id=current_user.id,
            analytics_type=data.analytics_type,
            period_start=datetime.fromisoformat(data.period_start),
            period_end=datetime.fromisoformat(data.period_end),
            metrics=metrics,
            trends={},
            insights="Analyse basée sur les résultats de quiz",
            recommendations=[]
        )
        
        db.add(report)
        db.commit()
        db.refresh(report)
        
        return report
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création du rapport: {str(e)}")

@router.post("/{report_id}/export")
def export_report(
    report_id: int,
    export_format: str = "pdf",
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'student']))
):
    """Exporter un rapport"""
    try:
        # Vérifier que le rapport existe et appartient à l'utilisateur
        report = db.query(DetailedReport).filter(
            DetailedReport.id == report_id,
            DetailedReport.user_id == current_user.id
        ).first()
        
        if not report:
            raise HTTPException(status_code=404, detail="Rapport non trouvé")
        
        # Simuler l'export
        export_data = {
            "report_id": report_id,
            "export_format": export_format,
            "file_url": f"/exports/report_{report_id}.{export_format}",
            "file_size": 1024,  # Taille simulée
            "exported_at": datetime.now().isoformat(),
            "status": "completed"
        }
        
        # Marquer le rapport comme exporté
        report.is_exported = True
        report.exported_at = datetime.now()
        db.commit()
        
        return export_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'export: {str(e)}")

# Helper functions
async def generate_report_data(user_id: int, report_type: str, period_start: datetime, period_end: datetime, db: Session):
    """Générer les données d'un rapport"""
    # Simulation de données basées sur le type de rapport
    if report_type == "performance":
        return {
            "overall_score": 85.5,
            "subject_scores": {
                "Mathématiques": 90.0,
                "Français": 82.0,
                "Histoire": 78.0
            },
            "improvement_rate": 12.3,
            "insights": "Performance stable avec une amélioration notable en mathématiques",
            "recommendations": [
                "Continuez à pratiquer les mathématiques",
                "Consacrez plus de temps à l'histoire"
            ]
        }
    elif report_type == "progress":
        return {
            "completed_topics": 15,
            "total_topics": 20,
            "completion_rate": 75.0,
            "time_spent": 1250,  # minutes
            "insights": "Progression régulière avec un bon rythme d'apprentissage",
            "recommendations": [
                "Maintenez ce rythme d'apprentissage",
                "Considérez des sessions plus longues pour les sujets difficiles"
            ]
        }
    else:
        return {
            "data": "Données génériques",
            "insights": "Aucun insight spécifique",
            "recommendations": []
        }

async def calculate_subject_progress(user_id: int, subject: str, period_start: datetime, period_end: datetime, db: Session):
    """Calculer la progression pour une matière"""
    # Simulation de calcul de progression
    return {
        "total_score": 85.0,
        "max_score": 100.0,
        "percentage": 85.0,
        "improvement_rate": 8.5,
        "topics_covered": ["Algèbre", "Géométrie", "Statistiques"],
        "strengths": ["Algèbre", "Calcul mental"],
        "weaknesses": ["Géométrie", "Résolution de problèmes"],
        "recommendations": [
            "Pratiquez plus la géométrie",
            "Faites des exercices de résolution de problèmes"
        ]
    }

@router.get("/teacher", response_model=List[DetailedReportResponse])
async def get_teacher_reports(
    current_user: User = Depends(require_role(['teacher'])),
    db: Session = Depends(get_db)
):
    """Récupérer tous les rapports pour un professeur"""
    try:
        # Récupérer tous les rapports créés par le professeur
        reports = db.query(DetailedReport).filter(
            DetailedReport.user_id == current_user.id
        ).all()
        
        return reports
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération des rapports: {str(e)}"
        )

async def generate_analytics_data(user_id: int, analytics_type: str, period_start: datetime, period_end: datetime, db: Session):
    """Générer les données d'analytics"""
    # Simulation de données d'analytics
    if analytics_type == "engagement":
        return {
            "metrics": {
                "total_time_spent": 1250,
                "sessions_count": 15,
                "completion_rate": 78.5,
                "engagement_score": 8.2
            },
            "trends": {
                "daily_activity": [65, 70, 85, 90, 75, 80, 95],
                "weekly_progress": [12, 15, 18, 22, 25, 28, 30]
            },
            "insights": "Engagement élevé avec une tendance positive",
            "recommendations": [
                "Maintenez ce niveau d'engagement",
                "Considérez des sessions plus fréquentes"
            ]
        }
    elif analytics_type == "behavior":
        return {
            "metrics": {
                "preferred_time": "14:00-16:00",
                "preferred_duration": 45,
                "preferred_subjects": ["Mathématiques", "Sciences"],
                "learning_style": "visuel"
            },
            "trends": {
                "time_preferences": {"morning": 20, "afternoon": 60, "evening": 20},
                "subject_preferences": {"math": 40, "science": 30, "history": 20, "language": 10}
            },
            "insights": "Préférence pour les sessions d'après-midi et les matières scientifiques",
            "recommendations": [
                "Planifiez les sessions importantes l'après-midi",
                "Intégrez plus de contenu scientifique"
            ]
        }
    else:
        return {
            "metrics": {},
            "trends": {},
            "insights": "Aucun insight spécifique",
            "recommendations": []
        } 