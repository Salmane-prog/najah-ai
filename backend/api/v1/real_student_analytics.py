#!/usr/bin/env python3
"""
Endpoints pour les analytics réelles des étudiants
Connecte les fonctionnalités AI aux vraies données des étudiants
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from core.database import get_db
from models.user import User, UserRole
from models.class_group import ClassGroup, ClassStudent
from models.quiz import Quiz, QuizResult
from models.homework import AdvancedHomework, AdvancedHomeworkSubmission
from core.security import get_current_user
from typing import List, Dict, Any
from datetime import datetime, timedelta
import json

router = APIRouter()

# ============================================================================
# ANALYTICS RÉELLES DES TESTS ADAPTATIFS
# ============================================================================

@router.get("/adaptive-tests/overview")
async def get_adaptive_tests_overview(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Vue d'ensemble des tests adaptatifs avec données réelles"""
    
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Accès réservé aux professeurs")
    
    try:
        # Récupérer les tests adaptatifs créés par le professeur
        adaptive_tests = db.execute("""
            SELECT 
                at.id,
                at.title,
                at.subject,
                at.total_questions,
                at.estimated_duration,
                at.created_at,
                COUNT(ata.student_id) as assigned_students,
                COUNT(CASE WHEN ata.status = 'completed' THEN 1 END) as completed_tests,
                AVG(ata.current_score) as average_score
            FROM adaptive_tests at
            LEFT JOIN adaptive_test_assignments ata ON at.id = ata.test_id
            WHERE at.created_by = :teacher_id
            GROUP BY at.id
            ORDER BY at.created_at DESC
        """, {"teacher_id": current_user.id}).fetchall()
        
        # Statistiques globales
        total_tests = len(adaptive_tests)
        total_assigned = sum(test.assigned_students for test in adaptive_tests)
        total_completed = sum(test.completed_tests for test in adaptive_tests)
        overall_average = sum(test.average_score or 0 for test in adaptive_tests) / total_tests if total_tests > 0 else 0
        
        return {
            "overview": {
                "total_tests": total_tests,
                "total_assigned": total_assigned,
                "total_completed": total_completed,
                "completion_rate": (total_completed / total_assigned * 100) if total_assigned > 0 else 0,
                "overall_average": round(overall_average, 2)
            },
            "tests": [
                {
                    "id": test.id,
                    "title": test.title,
                    "subject": test.subject,
                    "total_questions": test.total_questions,
                    "estimated_duration": test.estimated_duration,
                    "assigned_students": test.assigned_students,
                    "completed_tests": test.completed_tests,
                    "average_score": round(test.average_score or 0, 2),
                    "created_at": test.created_at
                }
                for test in adaptive_tests
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des analytics: {str(e)}")

@router.get("/adaptive-tests/{test_id}/student-performance")
async def get_adaptive_test_student_performance(
    test_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Performance détaillée des étudiants pour un test adaptatif spécifique"""
    
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Accès réservé aux professeurs")
    
    try:
        # Vérifier que le test appartient au professeur
        test = db.execute("""
            SELECT id, title, subject FROM adaptive_tests 
            WHERE id = :test_id AND created_by = :teacher_id
        """, {"test_id": test_id, "teacher_id": current_user.id}).fetchone()
        
        if not test:
            raise HTTPException(status_code=404, detail="Test non trouvé")
        
        # Récupérer les performances des étudiants
        student_performances = db.execute("""
            SELECT 
                u.id,
                u.first_name,
                u.last_name,
                u.email,
                ata.status,
                ata.current_score,
                ata.max_score,
                ata.questions_answered,
                ata.total_questions,
                ata.time_spent,
                ata.adaptation_level,
                ata.started_at,
                ata.completed_at
            FROM adaptive_test_assignments ata
            JOIN users u ON ata.student_id = u.id
            WHERE ata.test_id = :test_id
            ORDER BY ata.current_score DESC
        """, {"test_id": test_id}).fetchall()
        
        # Calculer les statistiques
        total_students = len(student_performances)
        completed_students = len([s for s in student_performances if s.status == 'completed'])
        average_score = sum(s.current_score or 0 for s in student_performances) / total_students if total_students > 0 else 0
        
        return {
            "test_info": {
                "id": test.id,
                "title": test.title,
                "subject": test.subject
            },
            "statistics": {
                "total_students": total_students,
                "completed_students": completed_students,
                "in_progress_students": total_students - completed_students,
                "completion_rate": (completed_students / total_students * 100) if total_students > 0 else 0,
                "average_score": round(average_score, 2)
            },
            "student_performances": [
                {
                    "student_id": s.id,
                    "name": f"{s.first_name} {s.last_name}",
                    "email": s.email,
                    "status": s.status,
                    "current_score": s.current_score or 0,
                    "max_score": s.max_score or 100,
                    "questions_answered": s.questions_answered or 0,
                    "total_questions": s.total_questions,
                    "time_spent": s.time_spent or 0,
                    "adaptation_level": s.adaptation_level,
                    "started_at": s.started_at,
                    "completed_at": s.completed_at
                }
                for s in student_performances
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des performances: {str(e)}")

# ============================================================================
# ANALYTICS RÉELLES DES ÉVALUATIONS FORMATIVES
# ============================================================================

@router.get("/formative-evaluations/overview")
async def get_formative_evaluations_overview(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Vue d'ensemble des évaluations formatives avec données réelles"""
    
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Accès réservé aux professeurs")
    
    try:
        # Récupérer les évaluations formatives créées par le professeur
        evaluations = db.execute("""
            SELECT 
                fe.id,
                fe.title,
                fe.subject,
                fe.evaluation_type,
                fe.total_points,
                fe.due_date,
                fe.status,
                fe.created_at,
                COUNT(fea.student_id) as assigned_students,
                COUNT(CASE WHEN fea.status = 'submitted' THEN 1 END) as submitted_assignments,
                COUNT(CASE WHEN fea.status = 'graded' THEN 1 END) as graded_assignments,
                AVG(fea.score) as average_score
            FROM formative_evaluations fe
            LEFT JOIN formative_evaluation_assignments fea ON fe.id = fea.evaluation_id
            WHERE fe.created_by = :teacher_id
            GROUP BY fe.id
            ORDER BY fe.created_at DESC
        """, {"teacher_id": current_user.id}).fetchall()
        
        # Statistiques globales
        total_evaluations = len(evaluations)
        total_assigned = sum(eval.assigned_students for eval in evaluations)
        total_submitted = sum(eval.submitted_assignments for eval in evaluations)
        total_graded = sum(eval.graded_assignments for eval in evaluations)
        
        return {
            "overview": {
                "total_evaluations": total_evaluations,
                "total_assigned": total_assigned,
                "total_submitted": total_submitted,
                "total_graded": total_graded,
                "submission_rate": (total_submitted / total_assigned * 100) if total_assigned > 0 else 0,
                "grading_rate": (total_graded / total_submitted * 100) if total_submitted > 0 else 0
            },
            "evaluations": [
                {
                    "id": eval.id,
                    "title": eval.title,
                    "subject": eval.subject,
                    "evaluation_type": eval.evaluation_type,
                    "total_points": eval.total_points,
                    "due_date": eval.due_date,
                    "status": eval.status,
                    "assigned_students": eval.assigned_students,
                    "submitted_assignments": eval.submitted_assignments,
                    "graded_assignments": eval.graded_assignments,
                    "average_score": round(eval.average_score or 0, 2),
                    "created_at": eval.created_at
                }
                for eval in evaluations
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des analytics: {str(e)}")

@router.get("/formative-evaluations/{evaluation_id}/student-submissions")
async def get_formative_evaluation_student_submissions(
    evaluation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Soumissions des étudiants pour une évaluation formative spécifique"""
    
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Accès réservé aux professeurs")
    
    try:
        # Vérifier que l'évaluation appartient au professeur
        evaluation = db.execute("""
            SELECT id, title, subject, evaluation_type FROM formative_evaluations 
            WHERE id = :evaluation_id AND created_by = :teacher_id
        """, {"evaluation_id": evaluation_id, "teacher_id": current_user.id}).fetchone()
        
        if not evaluation:
            raise HTTPException(status_code=404, detail="Évaluation non trouvée")
        
        # Récupérer les soumissions des étudiants
        student_submissions = db.execute("""
            SELECT 
                u.id,
                u.first_name,
                u.last_name,
                u.email,
                fea.status,
                fea.score,
                fea.feedback,
                fea.submitted_at,
                fea.graded_at,
                COUNT(fes.id) as submission_count
            FROM formative_evaluation_assignments fea
            JOIN users u ON fea.student_id = u.id
            LEFT JOIN formative_evaluation_submissions fes ON fea.id = fes.assignment_id
            WHERE fea.evaluation_id = :evaluation_id
            GROUP BY u.id, fea.id
            ORDER BY fea.submitted_at DESC
        """, {"evaluation_id": evaluation_id}).fetchall()
        
        # Calculer les statistiques
        total_students = len(student_submissions)
        submitted_students = len([s for s in student_submissions if s.status == 'submitted'])
        graded_students = len([s for s in student_submissions if s.status == 'graded'])
        average_score = sum(s.score or 0 for s in student_submissions if s.score) / graded_students if graded_students > 0 else 0
        
        return {
            "evaluation_info": {
                "id": evaluation.id,
                "title": evaluation.title,
                "subject": evaluation.subject,
                "evaluation_type": evaluation.evaluation_type
            },
            "statistics": {
                "total_students": total_students,
                "submitted_students": submitted_students,
                "graded_students": graded_students,
                "submission_rate": (submitted_students / total_students * 100) if total_students > 0 else 0,
                "grading_rate": (graded_students / submitted_students * 100) if submitted_students > 0 else 0,
                "average_score": round(average_score, 2)
            },
            "student_submissions": [
                {
                    "student_id": s.id,
                    "name": f"{s.first_name} {s.last_name}",
                    "email": s.email,
                    "status": s.status,
                    "score": s.score,
                    "feedback": s.feedback,
                    "submitted_at": s.submitted_at,
                    "graded_at": s.graded_at,
                    "submission_count": s.submission_count
                }
                for s in student_submissions
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des soumissions: {str(e)}")

# ============================================================================
# MONITORING EN TEMPS RÉEL
# ============================================================================

@router.get("/real-time/monitoring")
async def get_real_time_monitoring(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Monitoring en temps réel des activités des étudiants"""
    
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Accès réservé aux professeurs")
    
    try:
        # Activités récentes des tests adaptatifs
        recent_adaptive_activities = db.execute("""
            SELECT 
                u.first_name,
                u.last_name,
                at.title as test_title,
                ata.status,
                ata.current_score,
                ata.questions_answered,
                ata.updated_at
            FROM adaptive_test_assignments ata
            JOIN users u ON ata.student_id = u.id
            JOIN adaptive_tests at ON ata.test_id = at.id
            WHERE at.created_by = :teacher_id
            AND ata.updated_at >= datetime('now', '-1 hour')
            ORDER BY ata.updated_at DESC
            LIMIT 10
        """, {"teacher_id": current_user.id}).fetchall()
        
        # Activités récentes des évaluations formatives
        recent_formative_activities = db.execute("""
            SELECT 
                u.first_name,
                u.last_name,
                fe.title as evaluation_title,
                fea.status,
                fea.score,
                fea.updated_at
            FROM formative_evaluation_assignments fea
            JOIN users u ON fea.student_id = u.id
            JOIN formative_evaluations fe ON fea.evaluation_id = fe.id
            WHERE fe.created_by = :teacher_id
            AND fea.updated_at >= datetime('now', '-1 hour')
            ORDER BY fea.updated_at DESC
            LIMIT 10
        """, {"teacher_id": current_user.id}).fetchall()
        
        # Statistiques en temps réel
        current_stats = db.execute("""
            SELECT 
                (SELECT COUNT(*) FROM adaptive_test_assignments ata 
                 JOIN adaptive_tests at ON ata.test_id = at.id 
                 WHERE at.created_by = :teacher_id AND ata.status = 'in_progress') as active_adaptive_tests,
                (SELECT COUNT(*) FROM formative_evaluation_assignments fea 
                 JOIN formative_evaluations fe ON fea.evaluation_id = fe.id 
                 WHERE fe.created_by = :teacher_id AND fea.status = 'submitted') as pending_grades
        """, {"teacher_id": current_user.id}).fetchone()
        
        return {
            "real_time_stats": {
                "active_adaptive_tests": current_stats.active_adaptive_tests,
                "pending_grades": current_stats.pending_grades,
                "last_updated": datetime.now().isoformat()
            },
            "recent_adaptive_activities": [
                {
                    "student_name": f"{a.first_name} {a.last_name}",
                    "test_title": a.test_title,
                    "status": a.status,
                    "current_score": a.current_score or 0,
                    "questions_answered": a.questions_answered or 0,
                    "updated_at": a.updated_at
                }
                for a in recent_adaptive_activities
            ],
            "recent_formative_activities": [
                {
                    "student_name": f"{a.first_name} {a.last_name}",
                    "evaluation_title": a.evaluation_title,
                    "status": a.status,
                    "score": a.score,
                    "updated_at": a.updated_at
                }
                for a in recent_formative_activities
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du monitoring: {str(e)}")

# ============================================================================
# ANALYTICS GLOBALES DES ÉTUDIANTS
# ============================================================================

@router.get("/students/global-analytics")
async def get_students_global_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analytics globales de tous les étudiants du professeur"""
    
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Accès réservé aux professeurs")
    
    try:
        # Récupérer tous les étudiants du professeur
        students = db.execute("""
            SELECT DISTINCT u.id, u.first_name, u.last_name, u.email
            FROM users u
            JOIN class_students cs ON u.id = cs.student_id
            JOIN class_groups cg ON cs.class_id = cg.id
            WHERE cg.teacher_id = :teacher_id AND u.role = 'student'
        """, {"teacher_id": current_user.id}).fetchall()
        
        student_analytics = []
        
        for student in students:
            # Analytics des tests adaptatifs
            adaptive_stats = db.execute("""
                SELECT 
                    COUNT(*) as total_tests,
                    COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_tests,
                    AVG(current_score) as average_score,
                    SUM(time_spent) as total_time
                FROM adaptive_test_assignments ata
                JOIN adaptive_tests at ON ata.test_id = at.id
                WHERE ata.student_id = :student_id AND at.created_by = :teacher_id
            """, {"student_id": student.id, "teacher_id": current_user.id}).fetchone()
            
            # Analytics des évaluations formatives
            formative_stats = db.execute("""
                SELECT 
                    COUNT(*) as total_evaluations,
                    COUNT(CASE WHEN status = 'submitted' THEN 1 END) as submitted_evaluations,
                    COUNT(CASE WHEN status = 'graded' THEN 1 END) as graded_evaluations,
                    AVG(score) as average_score
                FROM formative_evaluation_assignments fea
                JOIN formative_evaluations fe ON fea.evaluation_id = fe.id
                WHERE fea.student_id = :student_id AND fe.created_by = :teacher_id
            """, {"student_id": student.id, "teacher_id": current_user.id}).fetchone()
            
            student_analytics.append({
                "student_id": student.id,
                "name": f"{student.first_name} {student.last_name}",
                "email": student.email,
                "adaptive_tests": {
                    "total_tests": adaptive_stats.total_tests or 0,
                    "completed_tests": adaptive_stats.completed_tests or 0,
                    "completion_rate": (adaptive_stats.completed_tests / adaptive_stats.total_tests * 100) if adaptive_stats.total_tests and adaptive_stats.total_tests > 0 else 0,
                    "average_score": round(adaptive_stats.average_score or 0, 2),
                    "total_time": adaptive_stats.total_time or 0
                },
                "formative_evaluations": {
                    "total_evaluations": formative_stats.total_evaluations or 0,
                    "submitted_evaluations": formative_stats.submitted_evaluations or 0,
                    "graded_evaluations": formative_stats.graded_evaluations or 0,
                    "submission_rate": (formative_stats.submitted_evaluations / formative_stats.total_evaluations * 100) if formative_stats.total_evaluations and formative_stats.total_evaluations > 0 else 0,
                    "average_score": round(formative_stats.average_score or 0, 2)
                }
            })
        
        return {
            "total_students": len(students),
            "student_analytics": student_analytics
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des analytics: {str(e)}")























