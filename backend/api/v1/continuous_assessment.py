from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import json

from core.database import get_db
from api.v1.users import get_current_user
from api.v1.auth import require_role
from models.user import User
from models.continuous_assessment import (
    Competency, StudentCompetency, ContinuousAssessment, 
    StudentContinuousAssessment, ProgressReport
)
from models.class_group import ClassGroup

router = APIRouter()

# === GESTION DES COMPÉTENCES ===

@router.get("/competencies")
def get_competencies(
    subject: Optional[str] = Query(None, description="Filtrer par matière"),
    level: Optional[str] = Query(None, description="Filtrer par niveau"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Récupérer les compétences disponibles."""
    try:
        query = db.query(Competency).filter(Competency.is_active == True)
        
        if subject:
            query = query.filter(Competency.subject == subject)
        
        if level:
            query = query.filter(Competency.level == level)
        
        competencies = query.all()
        
        return [
            {
                "id": comp.id,
                "name": comp.name,
                "description": comp.description,
                "subject": comp.subject,
                "level": comp.level,
                "category": comp.category
            }
            for comp in competencies
        ]
        
    except Exception as e:
        print(f"Erreur dans get_competencies: {str(e)}")
        return []

@router.post("/competencies")
def create_competency(
    competency_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Créer une nouvelle compétence."""
    try:
        competency = Competency(
            name=competency_data["name"],
            description=competency_data.get("description", ""),
            subject=competency_data["subject"],
            level=competency_data["level"],
            category=competency_data.get("category", "knowledge"),
            created_by=current_user.id
        )
        
        db.add(competency)
        db.commit()
        db.refresh(competency)
        
        return {"message": "Compétence créée avec succès", "competency_id": competency.id}
        
    except Exception as e:
        db.rollback()
        print(f"Erreur dans create_competency: {str(e)}")
        raise HTTPException(status_code=400, detail="Erreur lors de la création de la compétence")

# === ÉVALUATION CONTINUE ===

@router.get("/assessments")
def get_continuous_assessments(
    class_id: Optional[int] = Query(None, description="Filtrer par classe"),
    subject: Optional[str] = Query(None, description="Filtrer par matière"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Récupérer les évaluations continues."""
    try:
        query = db.query(ContinuousAssessment).filter(
            ContinuousAssessment.teacher_id == current_user.id,
            ContinuousAssessment.is_active == True
        )
        
        if class_id:
            query = query.filter(ContinuousAssessment.class_id == class_id)
        
        if subject:
            query = query.filter(ContinuousAssessment.subject == subject)
        
        assessments = query.order_by(ContinuousAssessment.created_at.desc()).all()
        
        return [
            {
                "id": assessment.id,
                "title": assessment.title,
                "description": assessment.description,
                "assessment_type": assessment.assessment_type,
                "subject": assessment.subject,
                "class_name": assessment.class_group.name if assessment.class_group else None,
                "competencies_targeted": assessment.competencies_targeted,
                "weight": assessment.weight,
                "due_date": assessment.due_date.isoformat() if assessment.due_date else None,
                "created_at": assessment.created_at.isoformat()
            }
            for assessment in assessments
        ]
        
    except Exception as e:
        print(f"Erreur dans get_continuous_assessments: {str(e)}")
        return []

@router.post("/assessments")
def create_continuous_assessment(
    assessment_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Créer une nouvelle évaluation continue."""
    try:
        assessment = ContinuousAssessment(
            title=assessment_data["title"],
            description=assessment_data.get("description", ""),
            assessment_type=assessment_data["assessment_type"],
            subject=assessment_data["subject"],
            class_id=assessment_data.get("class_id"),
            teacher_id=current_user.id,
            competencies_targeted=assessment_data.get("competencies_targeted", []),
            weight=assessment_data.get("weight", 1.0),
            due_date=datetime.fromisoformat(assessment_data["due_date"]) if assessment_data.get("due_date") else None
        )
        
        db.add(assessment)
        db.commit()
        db.refresh(assessment)
        
        return {"message": "Évaluation continue créée avec succès", "assessment_id": assessment.id}
        
    except Exception as e:
        db.rollback()
        print(f"Erreur dans create_continuous_assessment: {str(e)}")
        raise HTTPException(status_code=400, detail="Erreur lors de la création de l'évaluation")

# === SUIVI DES COMPÉTENCES ÉTUDIANT ===

@router.get("/student/{student_id}/competencies")
def get_student_competencies(
    student_id: int,
    subject: Optional[str] = Query(None, description="Filtrer par matière"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Récupérer les compétences d'un étudiant."""
    try:
        query = db.query(StudentCompetency).filter(StudentCompetency.student_id == student_id)
        
        if subject:
            query = query.join(Competency).filter(Competency.subject == subject)
        
        student_competencies = query.all()
        
        return [
            {
                "id": sc.id,
                "competency_id": sc.competency_id,
                "competency_name": sc.competency.name,
                "competency_subject": sc.competency.subject,
                "level_achieved": sc.level_achieved,
                "progress_percentage": sc.progress_percentage,
                "last_assessed": sc.last_assessed.isoformat() if sc.last_assessed else None,
                "assessment_count": sc.assessment_count
            }
            for sc in student_competencies
        ]
        
    except Exception as e:
        print(f"Erreur dans get_student_competencies: {str(e)}")
        return []

@router.put("/student/{student_id}/competency/{competency_id}")
def update_student_competency(
    student_id: int,
    competency_id: int,
    competency_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Mettre à jour le niveau d'une compétence pour un étudiant."""
    try:
        student_competency = db.query(StudentCompetency).filter(
            StudentCompetency.student_id == student_id,
            StudentCompetency.competency_id == competency_id
        ).first()
        
        if not student_competency:
            # Créer une nouvelle entrée
            student_competency = StudentCompetency(
                student_id=student_id,
                competency_id=competency_id,
                level_achieved=competency_data.get("level_achieved", "not_started"),
                progress_percentage=competency_data.get("progress_percentage", 0.0),
                assessment_count=competency_data.get("assessment_count", 0)
            )
            db.add(student_competency)
        else:
            # Mettre à jour l'entrée existante
            student_competency.level_achieved = competency_data.get("level_achieved", student_competency.level_achieved)
            student_competency.progress_percentage = competency_data.get("progress_percentage", student_competency.progress_percentage)
            student_competency.assessment_count = competency_data.get("assessment_count", student_competency.assessment_count)
            student_competency.last_assessed = datetime.utcnow()
        
        db.commit()
        
        return {"message": "Compétence étudiante mise à jour avec succès"}
        
    except Exception as e:
        db.rollback()
        print(f"Erreur dans update_student_competency: {str(e)}")
        raise HTTPException(status_code=400, detail="Erreur lors de la mise à jour")

# === RAPPORTS DE PROGRESSION ===

@router.get("/student/{student_id}/progress-report")
def get_student_progress_report(
    student_id: int,
    period: str = Query("monthly", description="Période: weekly, monthly, semester"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Générer un rapport de progression pour un étudiant."""
    try:
        # Calculer les dates de début et fin
        end_date = datetime.utcnow()
        if period == "weekly":
            start_date = end_date - timedelta(days=7)
        elif period == "monthly":
            start_date = end_date - timedelta(days=30)
        elif period == "semester":
            start_date = end_date - timedelta(days=180)
        else:
            start_date = end_date - timedelta(days=30)
        
        # Récupérer les compétences de l'étudiant
        student_competencies = db.query(StudentCompetency).filter(
            StudentCompetency.student_id == student_id
        ).all()
        
        # Calculer la progression globale
        total_competencies = len(student_competencies)
        if total_competencies > 0:
            overall_progress = sum(sc.progress_percentage for sc in student_competencies) / total_competencies
        else:
            overall_progress = 0.0
        
        # Analyser les forces et faiblesses
        strengths = []
        weaknesses = []
        
        for sc in student_competencies:
            if sc.progress_percentage >= 80:
                strengths.append({
                    "competency_name": sc.competency.name,
                    "progress": sc.progress_percentage,
                    "level": sc.level_achieved
                })
            elif sc.progress_percentage < 50:
                weaknesses.append({
                    "competency_name": sc.competency.name,
                    "progress": sc.progress_percentage,
                    "level": sc.level_achieved
                })
        
        # Générer des recommandations
        recommendations = []
        if weaknesses:
            recommendations.append("Se concentrer sur les compétences en difficulté")
        if overall_progress < 70:
            recommendations.append("Augmenter le temps d'étude et de pratique")
        if len(strengths) > len(weaknesses):
            recommendations.append("Continuer à développer les points forts")
        
        # Créer le rapport
        report = ProgressReport(
            student_id=student_id,
            teacher_id=current_user.id,
            period=period,
            start_date=start_date,
            end_date=end_date,
            overall_progress=overall_progress,
            competencies_summary=[
                {
                    "competency_name": sc.competency.name,
                    "subject": sc.competency.subject,
                    "progress": sc.progress_percentage,
                    "level": sc.level_achieved
                }
                for sc in student_competencies
            ],
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations
        )
        
        db.add(report)
        db.commit()
        
        return {
            "period": period,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "overall_progress": round(overall_progress, 2),
            "competencies_summary": report.competencies_summary,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations
        }
        
    except Exception as e:
        db.rollback()
        print(f"Erreur dans get_student_progress_report: {str(e)}")
        raise HTTPException(status_code=400, detail="Erreur lors de la génération du rapport")

@router.get("/class/{class_id}/progress-summary")
def get_class_progress_summary(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Récupérer un résumé de progression pour une classe."""
    try:
        # Récupérer tous les étudiants de la classe
        class_students = db.query(User).join(ClassGroup).filter(
            User.role == "student",
            ClassGroup.id == class_id
        ).all()
        
        class_summary = []
        
        for student in class_students:
            # Calculer la progression moyenne de l'étudiant
            student_competencies = db.query(StudentCompetency).filter(
                StudentCompetency.student_id == student.id
            ).all()
            
            if student_competencies:
                avg_progress = sum(sc.progress_percentage for sc in student_competencies) / len(student_competencies)
            else:
                avg_progress = 0.0
            
            class_summary.append({
                "student_id": student.id,
                "student_name": student.username,
                "average_progress": round(avg_progress, 2),
                "competencies_count": len(student_competencies)
            })
        
        # Calculer les statistiques de la classe
        if class_summary:
            class_avg_progress = sum(s["average_progress"] for s in class_summary) / len(class_summary)
            top_students = sorted(class_summary, key=lambda x: x["average_progress"], reverse=True)[:3]
            struggling_students = [s for s in class_summary if s["average_progress"] < 50]
        else:
            class_avg_progress = 0.0
            top_students = []
            struggling_students = []
        
        return {
            "class_id": class_id,
            "total_students": len(class_summary),
            "class_average_progress": round(class_avg_progress, 2),
            "top_students": top_students,
            "struggling_students": struggling_students,
            "students_summary": class_summary
        }
        
    except Exception as e:
        print(f"Erreur dans get_class_progress_summary: {str(e)}")
        return {
            "class_id": class_id,
            "total_students": 0,
            "class_average_progress": 0.0,
            "top_students": [],
            "struggling_students": [],
            "students_summary": []
        } 