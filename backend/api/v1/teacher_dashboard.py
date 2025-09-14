#!/usr/bin/env python3
"""
API pour le dashboard du professeur avec données réelles
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, timedelta

from core.database import get_db
from core.security import get_current_user
from models.user import User
from models.adaptive_evaluation import AdaptiveTest, TestAttempt
from models.class_group import ClassGroup, ClassStudent
from models.student_analytics import StudentAnalytics
from models.homework import AdvancedHomework as Homework
from models.homework import AdvancedHomeworkSubmission as HomeworkSubmission

router = APIRouter(tags=["teacher-dashboard"])

# ============================================================================
# ENDPOINTS PRINCIPAUX
# ============================================================================

@router.get("/")
async def get_teacher_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère les données du dashboard professeur
    """
    try:
        # Vérifier que l'utilisateur est un professeur
        if current_user.role != "teacher":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès réservé aux professeurs"
            )

        # Récupérer les statistiques de base
        total_students = db.query(ClassStudent).join(ClassGroup).filter(
            ClassGroup.teacher_id == current_user.id
        ).count()

        total_quizzes = db.query(Quiz).filter(
            Quiz.created_by == current_user.id
        ).count()

        total_classes = db.query(ClassGroup).filter(
            ClassGroup.teacher_id == current_user.id
        ).count()

        # Récupérer les quiz récents
        recent_quizzes = db.query(Quiz).filter(
            Quiz.created_by == current_user.id
        ).order_by(Quiz.created_at.desc()).limit(5).all()

        # Récupérer les classes
        classes = db.query(ClassGroup).filter(
            ClassGroup.teacher_id == current_user.id
        ).all()

        # Récupérer les performances récentes
        recent_performances = db.query(QuizResult).join(Quiz).filter(
            Quiz.created_by == current_user.id
        ).order_by(QuizResult.completed_at.desc()).limit(10).all()

        # Calculer les métriques
        total_assignments = db.query(Homework).filter(
            Homework.assigned_by == current_user.id
        ).count()

        pending_submissions = db.query(HomeworkSubmission).join(Homework).filter(
            Homework.assigned_by == current_user.id,
            HomeworkSubmission.status == "submitted"
        ).count()

        return {
            "overview": {
                "total_students": total_students,
                "total_quizzes": total_quizzes,
                "total_classes": total_classes,
                "total_assignments": total_assignments,
                "pending_submissions": pending_submissions
            },
            "recent_quizzes": [
                {
                    "id": quiz.id,
                    "title": quiz.title,
                    "subject": quiz.subject,
                    "created_at": quiz.created_at,
                    "status": quiz.status
                }
                for quiz in recent_quizzes
            ],
            "classes": [
                {
                    "id": cls.id,
                    "name": cls.name,
                    "subject": cls.subject,
                    "student_count": db.query(ClassStudent).filter(
                        ClassStudent.class_id == cls.id
                    ).count()
                }
                for cls in classes
            ],
            "recent_performances": [
                {
                    "student_name": result.student_name,
                    "quiz_title": result.quiz_title,
                    "score": result.score,
                    "completed_at": result.completed_at
                }
                for result in recent_performances
            ]
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération du dashboard: {str(e)}"
        )

@router.get("/analytics")
async def get_teacher_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère les analytics détaillées du professeur
    """
    try:
        if current_user.role != "teacher":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès réservé aux professeurs"
            )

        # Récupérer les performances moyennes par classe
        class_performances = []
        classes = db.query(ClassGroup).filter(
            ClassGroup.teacher_id == current_user.id
        ).all()

        for cls in classes:
            quiz_results = db.query(QuizResult).join(Quiz).filter(
                Quiz.created_by == current_user.id,
                QuizResult.class_id == cls.id
            ).all()

            if quiz_results:
                avg_score = sum(result.score for result in quiz_results) / len(quiz_results)
                class_performances.append({
                    "class_name": cls.name,
                    "average_score": round(avg_score, 2),
                    "total_attempts": len(quiz_results)
                })

        # Récupérer les tendances de performance
        recent_results = db.query(QuizResult).join(Quiz).filter(
            Quiz.created_by == current_user.id,
            QuizResult.completed_at >= datetime.now() - timedelta(days=30)
        ).order_by(QuizResult.completed_at).all()

        # Grouper par jour
        daily_performance = {}
        for result in recent_results:
            date = result.completed_at.date().isoformat()
            if date not in daily_performance:
                daily_performance[date] = []
            daily_performance[date].append(result.score)

        # Calculer la moyenne quotidienne
        daily_averages = [
            {
                "date": date,
                "average_score": round(sum(scores) / len(scores), 2),
                "attempts": len(scores)
            }
            for date, scores in daily_performance.items()
        ]

        return {
            "class_performances": class_performances,
            "daily_performance": daily_averages,
            "total_students": db.query(ClassStudent).join(ClassGroup).filter(
                ClassGroup.teacher_id == current_user.id
            ).count(),
            "total_quizzes": db.query(Quiz).filter(
                Quiz.created_by == current_user.id
            ).count()
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des analytics: {str(e)}"
        )

@router.get("/students")
async def get_teacher_students(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère la liste des étudiants du professeur
    """
    try:
        if current_user.role != "teacher":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès réservé aux professeurs"
            )

        # Récupérer tous les étudiants du professeur
        all_students = db.query(ClassStudent).join(ClassGroup).join(User, ClassStudent.student_id == User.id).filter(
            ClassGroup.teacher_id == current_user.id
        ).all()
        
        # Éliminer les doublons en Python (plus fiable)
        seen_student_ids = set()
        students = []
        for student in all_students:
            if student.student_id not in seen_student_ids:
                students.append(student)
                seen_student_ids.add(student.student_id)
        
        student_data = []
        for student in students:
            # Récupérer les performances de l'étudiant depuis test_attempts
            test_attempts = db.query(TestAttempt).join(AdaptiveTest).filter(
                AdaptiveTest.created_by == current_user.id,
                TestAttempt.student_id == student.student_id
            ).all()

            if test_attempts:
                # Calculer le score moyen en pourcentage
                total_score = sum(attempt.total_score or 0 for attempt in test_attempts)
                max_possible_score = sum(attempt.max_score or 1 for attempt in test_attempts)
                
                if max_possible_score > 0:
                    avg_score = (total_score / max_possible_score) * 100
                else:
                    avg_score = 0
                    
                total_attempts = len(test_attempts)
                # Récupérer la dernière activité
                last_activity = max(test_attempts, key=lambda x: x.completed_at or x.started_at).completed_at or max(test_attempts, key=lambda x: x.started_at).started_at if test_attempts else None
            else:
                avg_score = 0
                total_attempts = 0
                last_activity = None

            # Récupérer l'email de l'étudiant
            student_user = db.query(User).filter(User.id == student.student_id).first()
            email = student_user.email if student_user else "Email non défini"
            
            # Récupérer les données de gamification (XP, badges, etc.)
            # Note: Ces tables n'existent peut-être pas encore, on met des valeurs par défaut
            total_xp = 0  # À implémenter quand la table XP sera créée
            badges_count = 16  # Valeur hardcodée pour l'instant
            level = 1  # Niveau par défaut
            
            # Calculer la progression (basée sur le score moyen)
            progression = avg_score if avg_score > 0 else 0

            student_data.append({
                "id": student.student_id,
                "name": student.student.username or f"Élève {student.student_id}",
                "email": email,
                "class_name": student.class_group.name,
                "average_score": round(avg_score, 2),
                "total_attempts": total_attempts,
                "last_activity": last_activity.isoformat() if last_activity else None,
                "progression": round(progression, 2),
                "total_xp": total_xp,
                "badges_count": badges_count,
                "level": level
            })

        return {
            "students": student_data,
            "total_count": len(student_data)
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des étudiants: {str(e)}"
        )

@router.get("/quizzes")
async def get_teacher_quizzes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère la liste des quiz du professeur
    """
    try:
        if current_user.role != "teacher":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès réservé aux professeurs"
            )

        quizzes = db.query(AdaptiveTest).filter(
            AdaptiveTest.created_by == current_user.id
        ).order_by(AdaptiveTest.created_at.desc()).all()

        quiz_data = []
        for quiz in quizzes:
            # Récupérer les statistiques du test
            results = db.query(TestAttempt).filter(
                TestAttempt.test_id == quiz.id
            ).all()

            if results:
                # Calculer le score moyen en pourcentage
                total_score = sum(result.total_score or 0 for result in results)
                max_possible_score = sum(result.max_score or 1 for result in results)
                
                if max_possible_score > 0:
                    avg_score = (total_score / max_possible_score) * 100
                else:
                    avg_score = 0
                    
                total_attempts = len(results)
                completion_rate = len([r for r in results if r.status == "completed"]) / len(results) * 100 if results else 0
            else:
                avg_score = 0
                total_attempts = 0
                completion_rate = 0

            quiz_data.append({
                "id": quiz.id,
                "title": quiz.title,
                "subject": quiz.subject,
                "status": "active" if quiz.is_active else "inactive",
                "created_at": quiz.created_at,
                "average_score": round(avg_score, 2),
                "total_attempts": total_attempts,
                "completion_rate": round(completion_rate, 1)
            })

        return {
            "quizzes": quiz_data,
            "total_count": len(quiz_data)
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des quiz: {str(e)}"
        )
