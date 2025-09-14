from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from core.database import get_db
from models.user import User
from models.quiz import Quiz, QuizAssignment, QuizResult
from typing import List, Dict, Any
from datetime import datetime, timedelta
import json
from pydantic import BaseModel

# Modèles Pydantic
class Notification(BaseModel):
    id: str
    type: str
    title: str
    message: str
    quiz_title: str
    student_name: str
    due_date: str = None
    score: float = None
    created_at: str
    is_read: bool
    priority: str

class NotificationResponse(BaseModel):
    notifications: List[Notification]
    total_count: int
    unread_count: int

router = APIRouter()

@router.get("/quiz", response_model=NotificationResponse)
def get_quiz_notifications(
    db: Session = Depends(get_db)
):
    """Récupérer toutes les notifications de quiz (version test sans auth)"""
    try:
        # Simuler des notifications basées sur les données existantes
        notifications = []
        
        # Récupérer les quiz assignés avec échéances
        assignments = db.query(QuizAssignment).filter(
            QuizAssignment.is_active == True,
            QuizAssignment.due_date.isnot(None)
        ).all()
        
        for assignment in assignments:
            quiz = db.query(Quiz).filter(Quiz.id == assignment.quiz_id).first()
            student = db.query(User).filter(User.id == assignment.student_id).first()
            
            if quiz and student:
                # Vérifier si l'étudiant a répondu
                quiz_result = db.query(QuizResult).filter(
                    QuizResult.quiz_id == assignment.quiz_id,
                    QuizResult.student_id == assignment.student_id
                ).first()
                
                # Notification pour quiz en retard
                if not quiz_result and assignment.due_date < datetime.utcnow():
                    days_overdue = (datetime.utcnow() - assignment.due_date).days
                    notifications.append(Notification(
                        id=f"overdue_{assignment.id}",
                        type="overdue",
                        title=f"Quiz en retard",
                        message=f"L'étudiant {student.username} n'a pas encore répondu au quiz '{quiz.title}' ({days_overdue} jour(s) de retard)",
                        quiz_title=quiz.title,
                        student_name=student.username,
                        due_date=assignment.due_date.isoformat(),
                        created_at=datetime.utcnow().isoformat(),
                        is_read=False,
                        priority="high"
                    ))
                
                # Notification pour échéance proche (dans les 2 jours)
                elif not quiz_result and assignment.due_date > datetime.utcnow():
                    days_until_due = (assignment.due_date - datetime.utcnow()).days
                    if days_until_due <= 2:
                        notifications.append(Notification(
                            id=f"due_soon_{assignment.id}",
                            type="due_soon",
                            title=f"Échéance proche",
                            message=f"L'étudiant {student.username} doit répondre au quiz '{quiz.title}' dans {days_until_due} jour(s)",
                            quiz_title=quiz.title,
                            student_name=student.username,
                            due_date=assignment.due_date.isoformat(),
                            created_at=datetime.utcnow().isoformat(),
                            is_read=False,
                            priority="medium"
                        ))
                
                # Notification pour quiz terminé avec score faible
                elif quiz_result and quiz_result.score < 60:
                    notifications.append(Notification(
                        id=f"low_score_{assignment.id}",
                        type="low_score",
                        title=f"Score faible",
                        message=f"L'étudiant {student.username} a obtenu un score faible ({quiz_result.score}/100) au quiz '{quiz.title}'",
                        quiz_title=quiz.title,
                        student_name=student.username,
                        score=quiz_result.score,
                        created_at=datetime.utcnow().isoformat(),
                        is_read=False,
                        priority="medium"
                    ))
                
                # Notification pour quiz terminé avec succès
                elif quiz_result and quiz_result.score >= 80:
                    notifications.append(Notification(
                        id=f"completed_{assignment.id}",
                        type="completed",
                        title=f"Quiz terminé avec succès",
                        message=f"L'étudiant {student.username} a brillamment réussi le quiz '{quiz.title}' avec un score de {quiz_result.score}/100",
                        quiz_title=quiz.title,
                        student_name=student.username,
                        score=quiz_result.score,
                        created_at=datetime.utcnow().isoformat(),
                        is_read=False,
                        priority="low"
                    ))
        
        # Si aucune notification réelle, créer des exemples
        if not notifications:
            notifications = [
                Notification(
                    id="example_1",
                    type="overdue",
                    title="Quiz en retard",
                    message="L'étudiant etudiant1 n'a pas encore répondu au quiz 'Quiz Mathématiques - Niveau 1' (2 jour(s) de retard)",
                    quiz_title="Quiz Mathématiques - Niveau 1",
                    student_name="etudiant1",
                    due_date=(datetime.utcnow() - timedelta(days=2)).isoformat(),
                    created_at=datetime.utcnow().isoformat(),
                    is_read=False,
                    priority="high"
                ),
                Notification(
                    id="example_2",
                    type="due_soon",
                    title="Échéance proche",
                    message="L'étudiant etudiant2 doit répondre au quiz 'Quiz de Français' dans 1 jour(s)",
                    quiz_title="Quiz de Français",
                    student_name="etudiant2",
                    due_date=(datetime.utcnow() + timedelta(days=1)).isoformat(),
                    created_at=datetime.utcnow().isoformat(),
                    is_read=False,
                    priority="medium"
                ),
                Notification(
                    id="example_3",
                    type="low_score",
                    title="Score faible",
                    message="L'étudiant etudiant3 a obtenu un score faible (45/100) au quiz 'Quiz d'Histoire'",
                    quiz_title="Quiz d'Histoire",
                    student_name="etudiant3",
                    score=45,
                    created_at=datetime.utcnow().isoformat(),
                    is_read=False,
                    priority="medium"
                )
            ]
        
        unread_count = len([n for n in notifications if not n.is_read])
        
        return NotificationResponse(
            notifications=notifications,
            total_count=len(notifications),
            unread_count=unread_count
        )
        
    except Exception as e:
        print(f"❌ Erreur get_quiz_notifications: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@router.put("/{notification_id}/read")
def mark_notification_as_read(
    notification_id: str,
    db: Session = Depends(get_db)
):
    """Marquer une notification comme lue"""
    try:
        # Dans une vraie implémentation, on mettrait à jour la base de données
        # Pour cette version test, on retourne juste un succès
        return {
            "message": "Notification marquée comme lue",
            "notification_id": notification_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@router.put("/mark-all-read")
def mark_all_notifications_as_read(
    db: Session = Depends(get_db)
):
    """Marquer toutes les notifications comme lues"""
    try:
        # Dans une vraie implémentation, on mettrait à jour la base de données
        return {
            "message": "Toutes les notifications ont été marquées comme lues"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@router.get("/overdue")
def get_overdue_notifications(
    db: Session = Depends(get_db)
):
    """Récupérer les notifications pour quiz en retard"""
    try:
        overdue_quizzes = []
        
        # Récupérer les quiz assignés en retard
        assignments = db.query(QuizAssignment).filter(
            QuizAssignment.is_active == True,
            QuizAssignment.due_date.isnot(None),
            QuizAssignment.due_date < datetime.utcnow()
        ).all()
        
        for assignment in assignments:
            quiz = db.query(Quiz).filter(Quiz.id == assignment.quiz_id).first()
            student = db.query(User).filter(User.id == assignment.student_id).first()
            
            if quiz and student:
                # Vérifier si l'étudiant a répondu
                quiz_result = db.query(QuizResult).filter(
                    QuizResult.quiz_id == assignment.quiz_id,
                    QuizResult.student_id == assignment.student_id
                ).first()
                
                # Seulement si pas encore répondu
                if not quiz_result:
                    days_overdue = (datetime.utcnow() - assignment.due_date).days
                    overdue_quizzes.append({
                        "id": assignment.id,
                        "quiz_title": quiz.title,
                        "student_name": student.username,
                        "due_date": assignment.due_date.isoformat(),
                        "days_overdue": days_overdue,
                        "assignment_id": assignment.id
                    })
        
        # Si aucun quiz en retard réel, créer des exemples
        if not overdue_quizzes:
            overdue_quizzes = [
                {
                    "id": 1,
                    "quiz_title": "Quiz Mathématiques - Niveau 1",
                    "student_name": "etudiant1",
                    "due_date": (datetime.utcnow() - timedelta(days=2)).isoformat(),
                    "days_overdue": 2,
                    "assignment_id": 1
                },
                {
                    "id": 2,
                    "quiz_title": "Quiz de Français",
                    "student_name": "etudiant2",
                    "due_date": (datetime.utcnow() - timedelta(days=1)).isoformat(),
                    "days_overdue": 1,
                    "assignment_id": 2
                }
            ]
        
        return {
            "overdue_quizzes": overdue_quizzes,
            "total_overdue": len(overdue_quizzes)
        }
        
    except Exception as e:
        print(f"❌ Erreur get_overdue_notifications: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@router.get("/summary")
def get_notifications_summary(
    db: Session = Depends(get_db)
):
    """Récupérer un résumé des notifications"""
    try:
        # Compter les différents types de notifications
        summary = {
            "total_notifications": 0,
            "unread_count": 0,
            "high_priority": 0,
            "overdue_quizzes": 0,
            "due_soon_quizzes": 0,
            "recent_completions": 0
        }
        
        # Récupérer les quiz assignés
        assignments = db.query(QuizAssignment).filter(
            QuizAssignment.is_active == True
        ).all()
        
        for assignment in assignments:
            if assignment.due_date:
                # Quiz en retard
                if assignment.due_date < datetime.utcnow():
                    summary["overdue_quizzes"] += 1
                    summary["high_priority"] += 1
                
                # Échéance proche
                elif (assignment.due_date - datetime.utcnow()).days <= 2:
                    summary["due_soon_quizzes"] += 1
                    summary["high_priority"] += 1
        
        # Quiz récemment complétés
        recent_results = db.query(QuizResult).filter(
            QuizResult.created_at >= datetime.utcnow() - timedelta(days=7)
        ).count()
        summary["recent_completions"] = recent_results
        
        summary["total_notifications"] = (
            summary["overdue_quizzes"] + 
            summary["due_soon_quizzes"] + 
            summary["recent_completions"]
        )
        
        return summary
        
    except Exception as e:
        print(f"❌ Erreur get_notifications_summary: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@router.get("/user/{user_id}")
async def get_user_notifications(user_id: int, db: Session = Depends(get_db)):
    """Récupérer les notifications d'un utilisateur (version test sans auth)"""
    try:
        # Simuler des notifications pour l'utilisateur
        notifications = [
            {
                "id": 1,
                "title": "Nouveau quiz assigné",
                "message": "Vous avez un nouveau quiz à compléter",
                "type": "quiz_assignment",
                "is_read": False,
                "created_at": "2025-08-24T19:00:00"
            }
        ]
        return notifications
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}") 