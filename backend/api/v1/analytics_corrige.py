#!/usr/bin/env python3
"""
API Analytics avec de vraies données - VERSION CORRIGÉE
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, text
from datetime import datetime, timedelta
from typing import List, Dict, Any

from core.database import get_db
from core.security import get_current_user, require_role
from models.adaptive_evaluation import AdaptiveTest, TestAttempt

router = APIRouter()

@router.get("/class-overview")
async def get_class_overview(
    current_user = Depends(require_role(['teacher'])),
    db: Session = Depends(get_db)
):
    """Vue d'ensemble des classes du professeur avec vraies données"""
    try:
        # Récupérer les classes du professeur depuis la table 'classes'
        classes_result = db.execute(
            text("SELECT id, name, teacher_id FROM classes WHERE teacher_id = :teacher_id"),
            {"teacher_id": current_user.id}
        ).fetchall()
        
        if not classes_result:
            return {
                "totalClasses": 0,
                "totalStudents": 0,
                "activeStudents": 0,
                "averageScore": 0,
                "totalTests": 0,
                "completedTests": 0
            }
        
        class_ids = [cls.id for cls in classes_result]
        
        # Récupérer les étudiants de ces classes
        students_result = db.execute(
            text("SELECT class_id, student_id FROM class_students WHERE class_id IN :class_ids"),
            {"class_ids": tuple(class_ids) if len(class_ids) > 1 else (class_ids[0], class_ids[0])}
        ).fetchall()
        
        student_ids = [s.student_id for s in students_result]
        
        # Récupérer les tests créés par le professeur
        tests_result = db.execute(
            text("SELECT id, title FROM adaptive_tests WHERE created_by = :teacher_id"),
            {"teacher_id": current_user.id}
        ).fetchall()
        
        # Récupérer les tentatives de tests
        if student_ids:
            test_attempts_result = db.execute(
                text("""
                    SELECT ta.student_id, ta.total_score, ta.max_score, ta.completed_at
                    FROM test_attempts ta
                    JOIN adaptive_tests at ON ta.test_id = at.id
                    WHERE at.created_by = :teacher_id AND ta.student_id IN :student_ids
                """),
                {
                    "teacher_id": current_user.id,
                    "student_ids": tuple(student_ids) if len(student_ids) > 1 else (student_ids[0], student_ids[0])
                }
            ).fetchall()
        else:
            test_attempts_result = []
        
        # Calculer les statistiques
        total_classes = len(classes_result)
        total_students = len(set(student_ids)) if student_ids else 0
        total_tests = len(tests_result)
        
        # Étudiants actifs (ayant passé au moins un test cette semaine)
        week_ago = datetime.utcnow() - timedelta(days=7)
        if student_ids:
            active_students_result = db.execute(
                text("""
                    SELECT COUNT(DISTINCT ta.student_id) as active_count
                    FROM test_attempts ta
                    JOIN adaptive_tests at ON ta.test_id = at.id
                    WHERE at.created_by = :teacher_id 
                    AND ta.student_id IN :student_ids
                    AND ta.completed_at >= :week_ago
                """),
                {
                    "teacher_id": current_user.id,
                    "student_ids": tuple(student_ids) if len(student_ids) > 1 else (student_ids[0], student_ids[0]),
                    "week_ago": week_ago
                }
            ).fetchone()
            active_students = active_students_result.active_count if active_students_result else 0
        else:
            active_students = 0
        
        # Score moyen
        if test_attempts_result:
            total_score = sum(attempt.total_score or 0 for attempt in test_attempts_result)
            max_possible_score = sum(attempt.max_score or 1 for attempt in test_attempts_result)
            average_score = (total_score / max_possible_score) * 100 if max_possible_score > 0 else 0
        else:
            average_score = 0
        
        # Tests complétés
        completed_tests = len([ta for ta in test_attempts_result if ta.completed_at])
        
        return {
            "totalClasses": total_classes,
            "totalStudents": total_students,
            "activeStudents": active_students,
            "averageScore": round(average_score, 2),
            "totalTests": total_tests,
            "completedTests": completed_tests
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des analytics: {str(e)}"
        )

@router.get("/student-performances")
async def get_student_performances(
    current_user = Depends(require_role(['teacher'])),
    db: Session = Depends(get_db)
):
    """Performances des étudiants avec vraies données"""
    try:
        # Récupérer les classes du professeur
        classes_result = db.execute(
            text("SELECT id, name, teacher_id FROM classes WHERE teacher_id = :teacher_id"),
            {"teacher_id": current_user.id}
        ).fetchall()
        
        if not classes_result:
            return []
        
        class_ids = [cls.id for cls in classes_result]
        
        # Récupérer les étudiants de ces classes
        students_result = db.execute(
            text("SELECT class_id, student_id FROM class_students WHERE class_id IN :class_ids"),
            {"class_ids": tuple(class_ids) if len(class_ids) > 1 else (class_ids[0], class_ids[0])}
        ).fetchall()
        
        student_performances = []
        
        for student in students_result:
            # Récupérer les tentatives de tests de cet étudiant
            test_attempts_result = db.execute(
                text("""
                    SELECT ta.total_score, ta.max_score, ta.completed_at, ta.started_at
                    FROM test_attempts ta
                    JOIN adaptive_tests at ON ta.test_id = at.id
                    WHERE at.created_by = :teacher_id AND ta.student_id = :student_id
                """),
                {
                    "teacher_id": current_user.id,
                    "student_id": student.student_id
                }
            ).fetchall()
            
            if test_attempts_result:
                # Calculer le score moyen
                total_score = sum(attempt.total_score or 0 for attempt in test_attempts_result)
                max_possible_score = sum(attempt.max_score or 1 for attempt in test_attempts_result)
                average_score = (total_score / max_possible_score) * 100 if max_possible_score > 0 else 0
                
                # Dernière activité
                last_activity = max(
                    test_attempts_result, 
                    key=lambda x: x.completed_at or x.started_at or datetime.min
                )
                last_activity_date = last_activity.completed_at or last_activity.started_at
                
                student_performances.append({
                    "id": student.student_id,
                    "name": f"Étudiant {student.student_id}",
                    "email": f"student{student.student_id}@najah.ai",
                    "testsCompleted": len(test_attempts_result),
                    "averageScore": round(average_score, 2),
                    "progressPercentage": min(100, average_score),
                    "improvementTrend": "stable",
                    "lastTestDate": last_activity_date.isoformat() if last_activity_date else None
                })
        
        return student_performances
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des performances: {str(e)}"
        )

@router.get("/weekly-progress")
async def get_weekly_progress(
    current_user = Depends(require_role(['teacher'])),
    db: Session = Depends(get_db)
):
    """Progrès hebdomadaire avec vraies données"""
    try:
        # Calculer les 7 dernières semaines
        weeks = []
        for i in range(7):
            week_start = datetime.utcnow() - timedelta(weeks=i+1)
            week_end = week_start + timedelta(days=7)
            weeks.append((week_start, week_end))
        
        weekly_data = []
        
        for i, (week_start, week_end) in enumerate(reversed(weeks)):
            # Récupérer les tentatives de tests pour cette semaine
            test_attempts_result = db.execute(
                text("""
                    SELECT ta.total_score, ta.max_score
                    FROM test_attempts ta
                    JOIN adaptive_tests at ON ta.test_id = at.id
                    WHERE at.created_by = :teacher_id 
                    AND ta.completed_at >= :week_start 
                    AND ta.completed_at < :week_end
                """),
                {
                    "teacher_id": current_user.id,
                    "week_start": week_start,
                    "week_end": week_end
                }
            ).fetchall()
            
            if test_attempts_result:
                # Calculer le score moyen pour cette semaine
                total_score = sum(attempt.total_score or 0 for attempt in test_attempts_result)
                max_possible_score = sum(attempt.max_score or 1 for attempt in test_attempts_result)
                average_score = (total_score / max_possible_score) * 100 if max_possible_score > 0 else 0
                
                weekly_data.append({
                    "week": f"Sem {i+1}",
                    "averageScore": round(average_score, 2),
                    "testsCompleted": len(test_attempts_result)
                })
            else:
                weekly_data.append({
                    "week": f"Sem {i+1}",
                    "averageScore": 0,
                    "testsCompleted": 0
                })
        
        return weekly_data
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération du progrès hebdomadaire: {str(e)}"
        )

@router.get("/monthly-stats")
async def get_monthly_stats(
    current_user = Depends(require_role(['teacher'])),
    db: Session = Depends(get_db)
):
    """Statistiques mensuelles avec vraies données"""
    try:
        # Calculer les 6 derniers mois
        months = []
        month_names = ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin", "Juil", "Août", "Sep", "Oct", "Nov", "Déc"]
        
        for i in range(6):
            current_date = datetime.utcnow()
            month_start = current_date.replace(day=1) - timedelta(days=i*30)
            month_end = month_start.replace(day=28) + timedelta(days=4)
            month_end = month_end.replace(day=1) - timedelta(days=1)
            
            months.append((month_start, month_end, month_names[month_start.month - 1]))
        
        monthly_data = []
        
        for month_start, month_end, month_name in reversed(months):
            # Tests créés ce mois
            tests_created_result = db.execute(
                text("""
                    SELECT COUNT(*) as count
                    FROM adaptive_tests 
                    WHERE created_by = :teacher_id 
                    AND created_at >= :month_start 
                    AND created_at <= :month_end
                """),
                {
                    "teacher_id": current_user.id,
                    "month_start": month_start,
                    "month_end": month_end
                }
            ).fetchone()
            tests_created = tests_created_result.count if tests_created_result else 0
            
            # Tests complétés ce mois
            tests_completed_result = db.execute(
                text("""
                    SELECT COUNT(*) as count
                    FROM test_attempts ta
                    JOIN adaptive_tests at ON ta.test_id = at.id
                    WHERE at.created_by = :teacher_id 
                    AND ta.completed_at >= :month_start 
                    AND ta.completed_at <= :month_end
                """),
                {
                    "teacher_id": current_user.id,
                    "month_start": month_start,
                    "month_end": month_end
                }
            ).fetchone()
            tests_completed = tests_completed_result.count if tests_completed_result else 0
            
            monthly_data.append({
                "month": month_name,
                "testsCreated": tests_created,
                "testsCompleted": tests_completed
            })
        
        return monthly_data
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des statistiques mensuelles: {str(e)}"
        )

@router.get("/test-performances")
async def get_test_performances(
    current_user = Depends(require_role(['teacher'])),
    db: Session = Depends(get_db)
):
    """Performances des tests avec vraies données"""
    try:
        # Récupérer tous les tests créés par le professeur
        tests_result = db.execute(
            text("SELECT id, title, subject FROM adaptive_tests WHERE created_by = :teacher_id"),
            {"teacher_id": current_user.id}
        ).fetchall()
        
        test_performances = []
        
        for test in tests_result:
            # Récupérer les tentatives pour ce test
            test_attempts_result = db.execute(
                text("""
                    SELECT ta.total_score, ta.max_score, ta.completed_at
                    FROM test_attempts ta
                    WHERE ta.test_id = :test_id
                """),
                {"test_id": test.id}
            ).fetchall()
            
            if test_attempts_result:
                # Calculer le score moyen
                total_score = sum(attempt.total_score or 0 for attempt in test_attempts_result)
                max_possible_score = sum(attempt.max_score or 1 for attempt in test_attempts_result)
                average_score = (total_score / max_possible_score) * 100 if max_possible_score > 0 else 0
                
                # Taux de completion
                completed_attempts = len([ta for ta in test_attempts_result if ta.completed_at])
                completion_rate = (completed_attempts / len(test_attempts_result)) * 100 if test_attempts_result else 0
                
                test_performances.append({
                    "id": test.id,
                    "title": test.title or f"Test {test.id}",
                    "subject": test.subject or "Sujet non défini",
                    "difficultyLevel": 5,
                    "averageScore": round(average_score, 2),
                    "participants": len(test_attempts_result),
                    "completionRate": round(completion_rate, 2)
                })
        
        return test_performances
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des performances des tests: {str(e)}"
        )






