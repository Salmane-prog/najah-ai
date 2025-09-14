from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from pydantic import BaseModel
import json

from core.database import SessionLocal
from api.v1.users import get_current_user
from models.user import User, UserRole
from models.organization import Homework, StudySession, Reminder, LearningGoal
from models.class_group import ClassGroup, ClassStudent

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(tags=["Progress Reports"])

# =====================================================
# SCHÉMAS PYDANTIC
# =====================================================

class ProgressReport(BaseModel):
    student_id: int
    student_name: str
    period: str  # weekly, monthly, semester
    start_date: datetime
    end_date: datetime
    summary: Dict[str, Any]
    details: Dict[str, Any]
    recommendations: List[str]
    created_at: datetime

class SubjectProgress(BaseModel):
    subject: str
    goals_count: int
    completed_goals: int
    avg_progress: float
    study_time_hours: float
    homework_completion_rate: float

class WeeklyProgress(BaseModel):
    week_start: datetime
    week_end: datetime
    study_sessions: int
    total_study_time: float
    completed_homework: int
    completed_goals: int
    achievements_unlocked: int

# =====================================================
# FONCTIONS DE CALCUL DE PROGRESSION
# =====================================================

def calculate_student_progress(
    db: Session,
    student_id: int,
    start_date: datetime,
    end_date: datetime
) -> Dict[str, Any]:
    """Calculer la progression complète d'un étudiant"""
    
    # Récupérer les données de l'étudiant
    student = db.query(User).filter(User.id == student_id).first()
    if not student:
        return {}
    
    # Devoirs
    total_homework = db.query(Homework).filter(
        Homework.assigned_to == student_id,
        Homework.created_at >= start_date,
        Homework.created_at <= end_date
    ).count()
    
    completed_homework = db.query(Homework).filter(
        Homework.assigned_to == student_id,
        Homework.status == "completed",
        Homework.created_at >= start_date,
        Homework.created_at <= end_date
    ).count()
    
    overdue_homework = db.query(Homework).filter(
        Homework.assigned_to == student_id,
        Homework.status == "overdue",
        Homework.created_at >= start_date,
        Homework.created_at <= end_date
    ).count()
    
    # Sessions d'étude
    study_sessions = db.query(StudySession).filter(
        StudySession.user_id == student_id,
        StudySession.start_time >= start_date,
        StudySession.start_time <= end_date,
        StudySession.status == "completed"
    ).all()
    
    total_study_time = sum(session.duration or 0 for session in study_sessions)
    study_time_hours = total_study_time / 60
    
    # Objectifs d'apprentissage
    goals = db.query(LearningGoal).filter(
        LearningGoal.user_id == student_id,
        LearningGoal.created_at >= start_date,
        LearningGoal.created_at <= end_date
    ).all()
    
    total_goals = len(goals)
    completed_goals = len([g for g in goals if g.status == "completed"])
    active_goals = len([g for g in goals if g.status == "active"])
    avg_progress = sum(g.progress for g in goals) / len(goals) if goals else 0
    
    # Progression par matière
    subjects_progress = {}
    for goal in goals:
        if goal.subject not in subjects_progress:
            subjects_progress[goal.subject] = {
                "goals_count": 0,
                "completed_goals": 0,
                "total_progress": 0,
                "study_time": 0
            }
        
        subjects_progress[goal.subject]["goals_count"] += 1
        subjects_progress[goal.subject]["total_progress"] += goal.progress
        
        if goal.status == "completed":
            subjects_progress[goal.subject]["completed_goals"] += 1
    
    # Calculer les moyennes par matière
    for subject in subjects_progress:
        goals_count = subjects_progress[subject]["goals_count"]
        subjects_progress[subject]["avg_progress"] = (
            subjects_progress[subject]["total_progress"] / goals_count * 100
        ) if goals_count > 0 else 0
    
    # Calculer les métriques de performance
    homework_completion_rate = (completed_homework / total_homework * 100) if total_homework > 0 else 0
    study_consistency = len(study_sessions) / ((end_date - start_date).days + 1)  # sessions par jour
    goal_achievement_rate = (completed_goals / total_goals * 100) if total_goals > 0 else 0
    
    # Générer des recommandations
    recommendations = []
    
    if homework_completion_rate < 70:
        recommendations.append("Améliorez votre taux de completion des devoirs")
    
    if study_consistency < 0.5:
        recommendations.append("Étudiez plus régulièrement, même pour de courtes sessions")
    
    if goal_achievement_rate < 50:
        recommendations.append("Concentrez-vous sur la réalisation de vos objectifs")
    
    if overdue_homework > 0:
        recommendations.append(f"Vous avez {overdue_homework} devoir(s) en retard")
    
    if study_time_hours < 10:  # Moins de 10h par période
        recommendations.append("Augmentez votre temps d'étude")
    
    return {
        "student_id": student_id,
        "student_name": f"{student.first_name} {student.last_name}",
        "period": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "duration_days": (end_date - start_date).days
        },
        "summary": {
            "total_homework": total_homework,
            "completed_homework": completed_homework,
            "overdue_homework": overdue_homework,
            "homework_completion_rate": round(homework_completion_rate, 2),
            "study_sessions_count": len(study_sessions),
            "total_study_time_hours": round(study_time_hours, 1),
            "study_consistency": round(study_consistency, 2),
            "total_goals": total_goals,
            "completed_goals": completed_goals,
            "active_goals": active_goals,
            "goal_achievement_rate": round(goal_achievement_rate, 2),
            "average_progress": round(avg_progress * 100, 2)
        },
        "details": {
            "subjects_progress": subjects_progress,
            "study_sessions": [
                {
                    "id": session.id,
                    "title": session.title,
                    "subject": session.subject,
                    "duration_minutes": session.duration,
                    "start_time": session.start_time.isoformat(),
                    "end_time": session.end_time.isoformat() if session.end_time else None
                }
                for session in study_sessions
            ],
            "goals": [
                {
                    "id": goal.id,
                    "title": goal.title,
                    "subject": goal.subject,
                    "progress": goal.progress,
                    "status": goal.status,
                    "target_date": goal.target_date.isoformat()
                }
                for goal in goals
            ]
        },
        "recommendations": recommendations,
        "performance_score": round(
            (homework_completion_rate * 0.3 + 
             study_consistency * 20 + 
             goal_achievement_rate * 0.3 + 
             avg_progress * 100 * 0.2), 2
        )
    }

# =====================================================
# ENDPOINTS POUR LES RAPPORTS DE PROGRESSION
# =====================================================

@router.get("/student/{student_id}/progress")
def get_student_progress_report(
    student_id: int,
    period: str = "monthly",  # weekly, monthly, semester
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Générer un rapport de progression pour un étudiant"""
    
    # Vérifier les permissions
    if current_user.role == UserRole.student and current_user.id != student_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous ne pouvez voir que vos propres rapports"
        )
    
    # Calculer la période
    end_date = datetime.utcnow()
    if period == "weekly":
        start_date = end_date - timedelta(days=7)
    elif period == "monthly":
        start_date = end_date - timedelta(days=30)
    elif period == "semester":
        start_date = end_date - timedelta(days=90)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Période invalide. Utilisez: weekly, monthly, semester"
        )
    
    progress_data = calculate_student_progress(db, student_id, start_date, end_date)
    
    if not progress_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Étudiant non trouvé"
        )
    
    return progress_data

@router.get("/class/{class_id}/progress")
def get_class_progress_report(
    class_id: int,
    period: str = "monthly",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Générer un rapport de progression pour une classe"""
    
    if current_user.role != UserRole.teacher:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seuls les professeurs peuvent voir les rapports de classe"
        )
    
    # Vérifier que le professeur a accès à cette classe
    class_group = db.query(ClassGroup).filter(
        ClassGroup.id == class_id,
        ClassGroup.teacher_id == current_user.id
    ).first()
    
    if not class_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Classe non trouvée ou accès non autorisé"
        )
    
    # Récupérer les étudiants de la classe
    students = db.query(ClassStudent).filter(
        ClassStudent.class_id == class_id
    ).all()
    
    # Calculer la période
    end_date = datetime.utcnow()
    if period == "weekly":
        start_date = end_date - timedelta(days=7)
    elif period == "monthly":
        start_date = end_date - timedelta(days=30)
    elif period == "semester":
        start_date = end_date - timedelta(days=90)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Période invalide"
        )
    
    # Générer les rapports pour chaque étudiant
    class_progress = []
    class_summary = {
        "total_students": len(students),
        "avg_homework_completion": 0,
        "avg_study_time": 0,
        "avg_goal_achievement": 0,
        "avg_performance_score": 0
    }
    
    total_homework_completion = 0
    total_study_time = 0
    total_goal_achievement = 0
    total_performance_score = 0
    
    for student in students:
        progress_data = calculate_student_progress(db, student.student_id, start_date, end_date)
        if progress_data:
            class_progress.append(progress_data)
            
            summary = progress_data["summary"]
            total_homework_completion += summary["homework_completion_rate"]
            total_study_time += summary["total_study_time_hours"]
            total_goal_achievement += summary["goal_achievement_rate"]
            total_performance_score += progress_data["performance_score"]
    
    # Calculer les moyennes
    if class_progress:
        class_summary["avg_homework_completion"] = round(total_homework_completion / len(class_progress), 2)
        class_summary["avg_study_time"] = round(total_study_time / len(class_progress), 2)
        class_summary["avg_goal_achievement"] = round(total_goal_achievement / len(class_progress), 2)
        class_summary["avg_performance_score"] = round(total_performance_score / len(class_progress), 2)
    
    return {
        "class_id": class_id,
        "class_name": class_group.name,
        "period": period,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "class_summary": class_summary,
        "students_progress": class_progress
    }

@router.get("/weekly-progress")
def get_weekly_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer la progression hebdomadaire de l'étudiant"""
    
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cet endpoint est réservé aux étudiants"
        )
    
    # Calculer les 4 dernières semaines
    end_date = datetime.utcnow()
    weekly_progress = []
    
    for i in range(4):
        week_end = end_date - timedelta(weeks=i)
        week_start = week_end - timedelta(days=7)
        
        progress_data = calculate_student_progress(db, current_user.id, week_start, week_end)
        
        if progress_data:
            weekly_progress.append({
                "week_start": week_start.isoformat(),
                "week_end": week_end.isoformat(),
                "summary": progress_data["summary"],
                "performance_score": progress_data["performance_score"]
            })
    
    return {
        "student_id": current_user.id,
        "student_name": f"{current_user.first_name} {current_user.last_name}",
        "weekly_progress": weekly_progress
    }

@router.get("/subject-progress")
def get_subject_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer la progression par matière"""
    
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cet endpoint est réservé aux étudiants"
        )
    
    # Récupérer les objectifs par matière
    goals = db.query(LearningGoal).filter(
        LearningGoal.user_id == current_user.id
    ).all()
    
    subjects_progress = {}
    
    for goal in goals:
        if goal.subject not in subjects_progress:
            subjects_progress[goal.subject] = {
                "goals_count": 0,
                "completed_goals": 0,
                "total_progress": 0,
                "study_time_hours": 0
            }
        
        subjects_progress[goal.subject]["goals_count"] += 1
        subjects_progress[goal.subject]["total_progress"] += goal.progress
        
        if goal.status == "completed":
            subjects_progress[goal.subject]["completed_goals"] += 1
    
    # Calculer les moyennes et ajouter le temps d'étude
    for subject in subjects_progress:
        goals_count = subjects_progress[subject]["goals_count"]
        subjects_progress[subject]["avg_progress"] = (
            subjects_progress[subject]["total_progress"] / goals_count * 100
        ) if goals_count > 0 else 0
        
        # Calculer le temps d'étude pour cette matière
        study_sessions = db.query(StudySession).filter(
            StudySession.user_id == current_user.id,
            StudySession.subject == subject,
            StudySession.status == "completed"
        ).all()
        
        total_study_time = sum(session.duration or 0 for session in study_sessions)
        subjects_progress[subject]["study_time_hours"] = round(total_study_time / 60, 1)
        
        # Calculer le taux de completion des devoirs pour cette matière
        total_homework = db.query(Homework).filter(
            Homework.assigned_to == current_user.id,
            Homework.subject == subject
        ).count()
        
        completed_homework = db.query(Homework).filter(
            Homework.assigned_to == current_user.id,
            Homework.subject == subject,
            Homework.status == "completed"
        ).count()
        
        subjects_progress[subject]["homework_completion_rate"] = (
            completed_homework / total_homework * 100
        ) if total_homework > 0 else 0
    
    return {
        "student_id": current_user.id,
        "subjects_progress": subjects_progress
    }

# =====================================================
# ENDPOINTS POUR LES RECOMMANDATIONS PERSONNALISÉES
# =====================================================

@router.get("/recommendations")
def get_personalized_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Générer des recommandations personnalisées"""
    
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cet endpoint est réservé aux étudiants"
        )
    
    # Analyser les données récentes (30 derniers jours)
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=30)
    
    progress_data = calculate_student_progress(db, current_user.id, start_date, end_date)
    
    if not progress_data:
        return {"recommendations": ["Commencez par créer vos premiers objectifs d'apprentissage"]}
    
    summary = progress_data["summary"]
    recommendations = []
    
    # Recommandations basées sur les performances
    if summary["homework_completion_rate"] < 70:
        recommendations.append({
            "type": "homework",
            "priority": "high",
            "title": "Améliorez votre taux de completion",
            "description": f"Votre taux de completion est de {summary['homework_completion_rate']}%. Essayez de terminer tous vos devoirs à temps.",
            "action": "Planifiez vos devoirs avec des rappels"
        })
    
    if summary["study_consistency"] < 0.5:
        recommendations.append({
            "type": "study",
            "priority": "high",
            "title": "Étudiez plus régulièrement",
            "description": "Vous étudiez en moyenne {:.1f} fois par jour. Essayez d'étudier au moins 30 minutes par jour.",
            "action": "Créez des sessions d'étude quotidiennes"
        })
    
    if summary["goal_achievement_rate"] < 50:
        recommendations.append({
            "type": "goals",
            "priority": "medium",
            "title": "Concentrez-vous sur vos objectifs",
            "description": f"Vous avez terminé {summary['completed_goals']} sur {summary['total_goals']} objectifs.",
            "action": "Divisez vos objectifs en étapes plus petites"
        })
    
    if summary["total_study_time_hours"] < 10:
        recommendations.append({
            "type": "study",
            "priority": "medium",
            "title": "Augmentez votre temps d'étude",
            "description": f"Vous avez étudié {summary['total_study_time_hours']} heures ce mois-ci.",
            "action": "Planifiez des sessions d'étude plus longues"
        })
    
    # Recommandations positives
    if summary["homework_completion_rate"] >= 90:
        recommendations.append({
            "type": "achievement",
            "priority": "low",
            "title": "Excellent travail !",
            "description": "Votre taux de completion des devoirs est excellent. Continuez comme ça !",
            "action": "Aidez d'autres étudiants"
        })
    
    if summary["study_consistency"] >= 1.0:
        recommendations.append({
            "type": "achievement",
            "priority": "low",
            "title": "Étudiant assidu",
            "description": "Vous étudiez régulièrement. C'est parfait pour maintenir vos connaissances !",
            "action": "Diversifiez vos méthodes d'étude"
        })
    
    return {
        "student_id": current_user.id,
        "recommendations": recommendations,
        "performance_summary": summary
    } 