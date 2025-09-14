from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models.user import User
from api.v1.auth import require_role
from typing import List, Dict, Any
from datetime import datetime, timedelta
from models.quiz import QuizResult
from models.class_group import ClassGroup, ClassStudent
from models.assessment import Assessment

router = APIRouter()

@router.get("/teacher-tasks")
def get_teacher_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Récupérer les tâches du professeur basées sur les données réelles"""
    try:
        tasks = []
        task_id = 1

        # 1. Tâches basées sur les quiz à corriger
        pending_quizzes = db.query(QuizResult).filter(
            QuizResult.is_completed == True,
            QuizResult.score == None  # Quiz complétés mais non notés
        ).count()

        if pending_quizzes > 0:
            tasks.append({
                "id": task_id,
                "title": f"Corriger {pending_quizzes} quiz",
                "description": f"{pending_quizzes} quiz en attente de correction",
                "priority": "high",
                "due_date": (datetime.now() + timedelta(days=2)).isoformat(),
                "status": "pending",
                "type": "grading",
                "count": pending_quizzes
            })
            task_id += 1

        # 2. Tâches basées sur les classes à surveiller
        teacher_classes = db.query(ClassGroup).filter(
            ClassGroup.teacher_id == current_user.id
        ).count()

        if teacher_classes > 0:
            tasks.append({
                "id": task_id,
                "title": f"Surveiller {teacher_classes} classe(s)",
                "description": f"Suivi des performances de {teacher_classes} classe(s)",
                "priority": "medium",
                "due_date": (datetime.now() + timedelta(days=1)).isoformat(),
                "status": "pending",
                "type": "monitoring",
                "count": teacher_classes
            })
            task_id += 1

        # 3. Tâches basées sur les évaluations en attente
        pending_assessments = db.query(Assessment).filter(
            Assessment.status == "pending"
        ).count()

        if pending_assessments > 0:
            tasks.append({
                "id": task_id,
                "title": f"Préparer {pending_assessments} évaluation(s)",
                "description": f"{pending_assessments} évaluation(s) à préparer",
                "priority": "high",
                "due_date": (datetime.now() + timedelta(days=3)).isoformat(),
                "status": "pending",
                "type": "assessment",
                "count": pending_assessments
            })
            task_id += 1

        # 4. Tâches basées sur les étudiants en difficulté
        struggling_students = db.query(QuizResult.student_id).filter(
            QuizResult.is_completed == True,
            QuizResult.score < 60
        ).distinct().count()

        if struggling_students > 0:
            tasks.append({
                "id": task_id,
                "title": f"Aider {struggling_students} étudiant(s) en difficulté",
                "description": f"{struggling_students} étudiant(s) avec un score < 60%",
                "priority": "high",
                "due_date": (datetime.now() + timedelta(days=1)).isoformat(),
                "status": "pending",
                "type": "support",
                "count": struggling_students
            })
            task_id += 1

        # 5. Activité récente (quiz complétés cette semaine)
        week_ago = datetime.now() - timedelta(days=7)
        recent_activity = db.query(QuizResult).filter(
            QuizResult.is_completed == True,
            QuizResult.created_at >= week_ago
        ).count()

        if recent_activity > 0:
            tasks.append({
                "id": task_id,
                "title": f"Analyser {recent_activity} activité(s) récente(s)",
                "description": f"{recent_activity} quiz complétés cette semaine",
                "priority": "low",
                "due_date": (datetime.now() + timedelta(days=5)).isoformat(),
                "status": "pending",
                "type": "analysis",
                "count": recent_activity
            })
            task_id += 1

        if not tasks:
            tasks.append({
                "id": task_id,
                "title": "Aucune tâche urgente",
                "description": "Toutes les tâches sont à jour",
                "priority": "low",
                "due_date": (datetime.now() + timedelta(days=7)).isoformat(),
                "status": "completed",
                "type": "info",
                "count": 0
            })

        return {
            "teacher_id": current_user.id,
            "tasks": tasks,
            "total_tasks": len(tasks),
            "pending_tasks": len([t for t in tasks if t["status"] == "pending"]),
            "completed_tasks": len([t for t in tasks if t["status"] == "completed"]),
            "data_source": "real_database"
        }

    except Exception as e:
        print(f"[ERROR] Erreur dans get_teacher_tasks: {e}")
        import traceback
        traceback.print_exc()
        return {
            "teacher_id": current_user.id,
            "tasks": [],
            "total_tasks": 0,
            "pending_tasks": 0,
            "completed_tasks": 0,
            "data_source": "error_fallback"
        } 