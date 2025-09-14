from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Any
from datetime import datetime, timedelta
import logging

from core.database import get_db
from core.security import get_current_user
from models.user import User

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/teacher/{teacher_id}/monitoring/students")
async def get_student_activity(
    teacher_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Récupère l'activité en temps réel des étudiants pour un enseignant"""
    try:
        # Vérifier que l'utilisateur est un enseignant
        if current_user.role != 'teacher':
            raise HTTPException(status_code=403, detail="Accès refusé")
        
        # Vérifier que l'enseignant peut accéder à ces données
        if current_user.id != teacher_id:
            raise HTTPException(status_code=403, detail="Accès refusé aux données d'un autre enseignant")
        
        # Requête pour récupérer l'activité des étudiants
        query = text("""
            SELECT 
                qr.id as attempt_id,
                u.id as student_id,
                CONCAT(u.first_name, ' ', u.last_name) as student_name,
                q.id as test_id,
                q.title as test_title,
                q.total_questions,
                qr.current_question,
                qr.difficulty_level as difficulty,
                qr.confidence_score as confidence,
                CASE 
                    WHEN qr.completed_at IS NOT NULL THEN 'completed'
                    WHEN qr.started_at IS NOT NULL AND qr.completed_at IS NULL THEN 'active'
                    ELSE 'paused'
                END as status,
                COALESCE(
                    (julianday('now') - julianday(qr.started_at)) * 24 * 60, 
                    0
                ) as time_spent_minutes,
                CASE 
                    WHEN qr.completed_at IS NOT NULL THEN 'Terminé'
                    WHEN qr.started_at IS NOT NULL AND qr.completed_at IS NULL THEN 
                        CASE 
                            WHEN (julianday('now') - julianday(qr.started_at)) * 24 * 60 < 1 THEN 'Il y a moins d\'1 min'
                            WHEN (julianday('now') - julianday(qr.started_at)) * 24 * 60 < 60 THEN 
                                CAST((julianday('now') - julianday(qr.started_at)) * 24 * 60 AS INTEGER) || ' min'
                            ELSE 
                                CAST((julianday('now') - julianday(qr.started_at)) * 24 AS INTEGER) || 'h'
                        END
                    ELSE 'En attente'
                END as last_activity
            FROM quiz_results qr
            JOIN quizzes q ON qr.quiz_id = q.id
            JOIN users u ON qr.student_id = u.id
            JOIN class_students cs ON u.id = cs.student_id
            JOIN class_groups cg ON cs.class_id = cg.id
            WHERE cg.teacher_id = :teacher_id
            AND qr.started_at >= datetime('now', '-24 hours')  -- Activité des dernières 24h
            ORDER BY qr.started_at DESC
        """)
        
        result = db.execute(query, {"teacher_id": teacher_id})
        activities = []
        
        for row in result:
            activity = {
                "id": row.attempt_id,
                "name": row.student_name,
                "testId": row.test_id,
                "testTitle": row.test_title,
                "currentQuestion": row.current_question or 0,
                "totalQuestions": row.total_questions or 0,
                "difficulty": float(row.difficulty or 5.0),
                "confidence": float(row.confidence or 0.5),
                "timeSpent": int(row.time_spent_minutes or 0),
                "status": row.status,
                "lastActivity": row.last_activity
            }
            activities.append(activity)
        
        logger.info(f"Récupération de {len(activities)} activités d'étudiants pour l'enseignant {teacher_id}")
        
        return {
            "success": True,
            "activities": activities
        }
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'activité des étudiants: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")

@router.get("/teacher/{teacher_id}/monitoring/tests")
async def get_test_performance(
    teacher_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Récupère les performances des tests pour un enseignant"""
    try:
        # Vérifier que l'utilisateur est un enseignant
        if current_user.role != 'teacher':
            raise HTTPException(status_code=403, detail="Accès refusé")
        
        # Vérifier que l'enseignant peut accéder à ces données
        if current_user.id != teacher_id:
            raise HTTPException(status_code=403, detail="Accès refusé aux données d'un autre enseignant")
        
        # Requête pour récupérer les performances des tests
        query = text("""
            SELECT 
                q.id as test_id,
                q.title as test_title,
                COUNT(DISTINCT CASE 
                    WHEN qr.started_at IS NOT NULL AND qr.completed_at IS NULL 
                    THEN qr.student_id 
                END) as active_students,
                AVG(qr.difficulty_level) as avg_difficulty,
                AVG(qr.confidence_score) as avg_confidence,
                ROUND(
                    (COUNT(CASE WHEN qr.completed_at IS NOT NULL THEN 1 END) * 100.0) / 
                    NULLIF(COUNT(qr.id), 0), 2
                ) as completion_rate,
                AVG(
                    CASE 
                        WHEN qr.completed_at IS NOT NULL 
                        THEN (julianday(qr.completed_at) - julianday(qr.started_at)) * 24 * 60
                    END
                ) as avg_time_minutes
            FROM quizzes q
            LEFT JOIN quiz_results qr ON q.id = qr.quiz_id
            JOIN class_students cs ON qr.student_id = cs.student_id
            JOIN class_groups cg ON cs.class_id = cg.id
            WHERE cg.teacher_id = :teacher_id
            AND qr.started_at >= datetime('now', '-7 days')  -- Tests des 7 derniers jours
            GROUP BY q.id, q.title
            HAVING COUNT(qr.id) > 0
            ORDER BY q.created_at DESC
        """)
        
        result = db.execute(query, {"teacher_id": teacher_id})
        performances = []
        
        for row in result:
            performance = {
                "testId": row.test_id,
                "title": row.test_title,
                "activeStudents": int(row.active_students or 0),
                "averageDifficulty": float(row.avg_difficulty or 5.0),
                "averageConfidence": float(row.avg_confidence or 0.5),
                "completionRate": float(row.completion_rate or 0.0),
                "averageTime": int(row.avg_time_minutes or 0)
            }
            performances.append(performance)
        
        logger.info(f"Récupération de {len(performances)} performances de tests pour l'enseignant {teacher_id}")
        
        return {
            "success": True,
            "performances": performances
        }
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des performances des tests: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")

@router.get("/teacher/{teacher_id}/monitoring/overview")
async def get_monitoring_overview(
    teacher_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Récupère un aperçu complet du monitoring pour un enseignant"""
    try:
        # Vérifier que l'utilisateur est un enseignant
        if current_user.role != 'teacher':
            raise HTTPException(status_code=403, detail="Accès refusé")
        
        # Vérifier que l'enseignant peut accéder à ces données
        if current_user.id != teacher_id:
            raise HTTPException(status_code=403, detail="Accès refusé aux données d'un autre enseignant")
        
        # Récupérer les données d'activité et de performance
        activities_query = text("""
            SELECT 
                COUNT(DISTINCT CASE 
                    WHEN qr.started_at IS NOT NULL AND qr.completed_at IS NULL 
                    THEN qr.student_id 
                END) as active_students,
                COUNT(CASE WHEN qr.completed_at IS NOT NULL THEN 1 END) as completed_tests,
                COUNT(DISTINCT q.id) as total_tests,
                AVG(qr.confidence_score) as avg_confidence
            FROM quiz_results qr
            JOIN quizzes q ON qr.quiz_id = q.id
            JOIN class_students cs ON qr.student_id = cs.student_id
            JOIN class_groups cg ON cs.class_id = cg.id
            WHERE cg.teacher_id = :teacher_id
            AND qr.started_at >= datetime('now', '-24 hours')
        """)
        
        result = db.execute(activities_query, {"teacher_id": teacher_id}).fetchone()
        
        overview = {
            "activeStudents": int(result.active_students or 0),
            "completedTests": int(result.completed_tests or 0),
            "totalTests": int(result.total_tests or 0),
            "averageConfidence": round(float(result.avg_confidence or 0.5) * 100, 1)
        }
        
        logger.info(f"Aperçu du monitoring récupéré pour l'enseignant {teacher_id}: {overview}")
        
        return {
            "success": True,
            "overview": overview
        }
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'aperçu du monitoring: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")





