from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from models.user import User
from models.quiz import Quiz, QuizResult, Question
from api.v1.users import get_current_user
from api.v1.auth import require_role
from typing import List, Dict, Any
from datetime import datetime
import json

router = APIRouter()

@router.get("/pending-corrections")
def get_pending_corrections(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher']))
):
    """Récupérer les quiz en attente de correction."""
    try:
        from models.class_group import ClassGroup, ClassStudent
        
        # Récupérer les classes du professeur
        teacher_classes = db.query(ClassGroup).filter(
            ClassGroup.teacher_id == current_user.id
        ).all()
        
        class_ids = [c.id for c in teacher_classes]
        
        # Récupérer les quiz du professeur
        teacher_quizzes = db.query(Quiz).filter(
            Quiz.created_by == current_user.id
        ).all()
        
        quiz_ids = [q.id for q in teacher_quizzes]
        
        # Récupérer les résultats en attente de correction
        pending_results = db.query(QuizResult).filter(
            QuizResult.quiz_id.in_(quiz_ids),
            QuizResult.needs_manual_correction == True,
            QuizResult.corrected == False
        ).all()
        
        # Récupérer les détails des élèves
        student_ids = [r.student_id for r in pending_results]
        students = db.query(User).filter(User.id.in_(student_ids)).all()
        students_dict = {s.id: s for s in students}
        
        # Récupérer les détails des quiz
        quizzes_dict = {q.id: q for q in teacher_quizzes}
        
        return {
            "pending_corrections": [
                {
                    "result_id": result.id,
                    "quiz": {
                        "id": result.quiz_id,
                        "title": quizzes_dict.get(result.quiz_id, {}).title,
                        "subject": quizzes_dict.get(result.quiz_id, {}).subject
                    },
                    "student": {
                        "id": result.student_id,
                        "name": f"{students_dict.get(result.student_id, {}).first_name} {students_dict.get(result.student_id, {}).last_name}",
                        "email": students_dict.get(result.student_id, {}).email
                    },
                    "score": result.score,
                    "submitted_at": result.created_at.isoformat(),
                    "needs_correction": result.needs_manual_correction,
                    "correction_notes": result.correction_notes
                }
                for result in pending_results
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des corrections en attente: {str(e)}")

@router.get("/correction/{result_id}")
def get_correction_details(
    result_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher']))
):
    """Récupérer les détails d'une correction spécifique."""
    try:
        # Récupérer le résultat
        result = db.query(QuizResult).filter(QuizResult.id == result_id).first()
        
        if not result:
            raise HTTPException(status_code=404, detail="Résultat non trouvé")
        
        # Vérifier que le quiz appartient au professeur
        quiz = db.query(Quiz).filter(
            Quiz.id == result.quiz_id,
            Quiz.created_by == current_user.id
        ).first()
        
        if not quiz:
            raise HTTPException(status_code=403, detail="Vous n'êtes pas autorisé à corriger ce quiz")
        
        # Récupérer les questions et réponses
        questions = db.query(Question).filter(
            Question.quiz_id == result.quiz_id
        ).all()
        
        # Récupérer les réponses de l'élève
        student_answers = json.loads(result.answers) if result.answers else {}
        
        # Analyser chaque question
        detailed_correction = []
        for question in questions:
            student_answer = student_answers.get(str(question.id), "")
            is_correct = question.correct_answer == student_answer
            
            detailed_correction.append({
                "question_id": question.id,
                "question_text": question.question_text,
                "question_type": question.question_type,
                "correct_answer": question.correct_answer,
                "student_answer": student_answer,
                "is_correct": is_correct,
                "points": question.points,
                "explanation": question.explanation
            })
        
        # Récupérer les informations de l'élève
        student = db.query(User).filter(User.id == result.student_id).first()
        
        return {
            "result_id": result.id,
            "quiz": {
                "id": quiz.id,
                "title": quiz.title,
                "subject": quiz.subject,
                "total_points": quiz.total_points
            },
            "student": {
                "id": student.id,
                "name": f"{student.first_name} {student.last_name}",
                "email": student.email
            },
            "score": result.score,
            "submitted_at": result.created_at.isoformat(),
            "time_taken": result.time_taken,
            "detailed_correction": detailed_correction,
            "correction_notes": result.correction_notes,
            "needs_manual_correction": result.needs_manual_correction
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des détails de correction: {str(e)}")

@router.post("/correct/{result_id}")
def submit_correction(
    result_id: int,
    correction_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher']))
):
    """Soumettre une correction manuelle."""
    try:
        # Récupérer le résultat
        result = db.query(QuizResult).filter(QuizResult.id == result_id).first()
        
        if not result:
            raise HTTPException(status_code=404, detail="Résultat non trouvé")
        
        # Vérifier que le quiz appartient au professeur
        quiz = db.query(Quiz).filter(
            Quiz.id == result.quiz_id,
            Quiz.created_by == current_user.id
        ).first()
        
        if not quiz:
            raise HTTPException(status_code=403, detail="Vous n'êtes pas autorisé à corriger ce quiz")
        
        # Mettre à jour la correction
        result.corrected = True
        result.corrected_by = current_user.id
        result.corrected_at = datetime.utcnow()
        result.correction_notes = correction_data.get("notes", "")
        result.final_score = correction_data.get("final_score", result.score)
        
        # Mettre à jour les réponses corrigées si fournies
        if "corrected_answers" in correction_data:
            result.corrected_answers = json.dumps(correction_data["corrected_answers"])
        
        db.commit()
        db.refresh(result)
        
        return {
            "message": "Correction soumise avec succès",
            "result_id": result.id,
            "final_score": result.final_score
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la soumission de la correction: {str(e)}")

@router.get("/auto-correct/{result_id}")
def auto_correct_quiz(
    result_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher']))
):
    """Corriger automatiquement un quiz."""
    try:
        # Récupérer le résultat
        result = db.query(QuizResult).filter(QuizResult.id == result_id).first()
        
        if not result:
            raise HTTPException(status_code=404, detail="Résultat non trouvé")
        
        # Vérifier que le quiz appartient au professeur
        quiz = db.query(Quiz).filter(
            Quiz.id == result.quiz_id,
            Quiz.created_by == current_user.id
        ).first()
        
        if not quiz:
            raise HTTPException(status_code=403, detail="Vous n'êtes pas autorisé à corriger ce quiz")
        
        # Récupérer les questions
        questions = db.query(Question).filter(
            Question.quiz_id == result.quiz_id
        ).all()
        
        # Récupérer les réponses de l'élève
        student_answers = json.loads(result.answers) if result.answers else {}
        
        # Corriger automatiquement
        total_points = 0
        earned_points = 0
        corrected_answers = {}
        
        for question in questions:
            total_points += question.points
            student_answer = student_answers.get(str(question.id), "")
            
            # Vérifier si la réponse est correcte
            is_correct = question.correct_answer == student_answer
            
            if is_correct:
                earned_points += question.points
            
            corrected_answers[str(question.id)] = {
                "student_answer": student_answer,
                "correct_answer": question.correct_answer,
                "is_correct": is_correct,
                "points": question.points,
                "earned_points": question.points if is_correct else 0
            }
        
        # Calculer le score final
        final_score = (earned_points / total_points) * 100 if total_points > 0 else 0
        
        # Mettre à jour le résultat
        result.score = final_score
        result.corrected = True
        result.corrected_by = current_user.id
        result.corrected_at = datetime.utcnow()
        result.corrected_answers = json.dumps(corrected_answers)
        result.needs_manual_correction = False
        
        db.commit()
        db.refresh(result)
        
        return {
            "message": "Quiz corrigé automatiquement",
            "result_id": result.id,
            "final_score": final_score,
            "total_points": total_points,
            "earned_points": earned_points,
            "correction_details": corrected_answers
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la correction automatique: {str(e)}")

@router.get("/correction-stats")
def get_correction_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher']))
):
    """Récupérer les statistiques de correction."""
    try:
        # Récupérer les quiz du professeur
        teacher_quizzes = db.query(Quiz).filter(
            Quiz.created_by == current_user.id
        ).all()
        
        quiz_ids = [q.id for q in teacher_quizzes]
        
        # Statistiques globales
        total_results = db.query(QuizResult).filter(
            QuizResult.quiz_id.in_(quiz_ids)
        ).count()
        
        pending_corrections = db.query(QuizResult).filter(
            QuizResult.quiz_id.in_(quiz_ids),
            QuizResult.needs_manual_correction == True,
            QuizResult.corrected == False
        ).count()
        
        corrected_results = db.query(QuizResult).filter(
            QuizResult.quiz_id.in_(quiz_ids),
            QuizResult.corrected == True
        ).count()
        
        # Statistiques par quiz
        quiz_stats = []
        for quiz in teacher_quizzes:
            quiz_results = db.query(QuizResult).filter(
                QuizResult.quiz_id == quiz.id
            ).all()
            
            if quiz_results:
                avg_score = sum(r.score for r in quiz_results) / len(quiz_results)
                pending_count = sum(1 for r in quiz_results if r.needs_manual_correction and not r.corrected)
                
                quiz_stats.append({
                    "quiz_id": quiz.id,
                    "quiz_title": quiz.title,
                    "total_submissions": len(quiz_results),
                    "average_score": round(avg_score, 2),
                    "pending_corrections": pending_count
                })
        
        return {
            "total_results": total_results,
            "pending_corrections": pending_corrections,
            "corrected_results": corrected_results,
            "correction_rate": (corrected_results / total_results * 100) if total_results > 0 else 0,
            "quiz_statistics": quiz_stats
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des statistiques: {str(e)}") 