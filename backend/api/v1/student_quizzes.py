from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from core.database import get_db
from models.user import User
from models.quiz import Quiz, QuizResult, Question
from typing import List, Dict, Any
from datetime import datetime, timedelta
import json

router = APIRouter()

@router.get("/student/{student_id}")
def get_student_quizzes(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Récupérer tous les quiz d'un étudiant (version test sans auth)"""
    try:
        # Vérifier que l'étudiant existe
        student = db.query(User).filter(User.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Étudiant non trouvé")
        
        # Récupérer les quiz assignés
        assigned_quizzes = db.query(Quiz).filter(
            Quiz.is_active == True
        ).all()
        
        # Récupérer les résultats de quiz de l'étudiant
        student_results = db.query(QuizResult).filter(
            QuizResult.student_id == student_id
        ).all()
        
        # Formater les quiz
        quizzes = []
        
        for quiz in assigned_quizzes:
            # Vérifier si l'étudiant a déjà passé ce quiz
            existing_result = next(
                (r for r in student_results if r.quiz_id == quiz.id), 
                None
            )
            
            # Compter le nombre de questions pour ce quiz
            question_count = len(quiz.questions) if quiz.questions else 0
            
            quiz_data = {
                "id": quiz.id,
                "title": quiz.title,
                "description": quiz.description or "Quiz d'apprentissage",
                "subject": quiz.subject or "Général",
                "difficulty": quiz.difficulty,
                "time_limit": quiz.time_limit or 30,
                "total_questions": question_count,
                "is_active": quiz.is_active,
                "created_at": quiz.created_at.isoformat() if quiz.created_at else None,
                "status": "completed" if existing_result else "assigned",
                "score": existing_result.score if existing_result else None,
                "completed_at": existing_result.created_at.isoformat() if existing_result else None,
                "time_spent": existing_result.time_spent if existing_result else None
            }
            
            quizzes.append(quiz_data)
        
        # Si aucun quiz, créer des quiz de test
        if not quizzes:
            quizzes = [
                {
                    "id": 1,
                    "title": "Quiz de Grammaire Française",
                    "description": "Testez vos connaissances en grammaire française",
                    "subject": "Français",
                    "difficulty": "medium",
                    "time_limit": 30,
                    "total_questions": 15,
                    "is_active": True,
                    "created_at": datetime.utcnow().isoformat(),
                    "status": "assigned",
                    "score": None,
                    "completed_at": None,
                    "time_spent": None
                },
                {
                    "id": 2,
                    "title": "Quiz de Vocabulaire A1",
                    "description": "Évaluez votre vocabulaire de base",
                    "subject": "Français",
                    "difficulty": "easy",
                    "time_limit": 25,
                    "total_questions": 10,
                    "is_active": True,
                    "created_at": datetime.utcnow().isoformat(),
                    "status": "assigned",
                    "score": None,
                    "completed_at": None,
                    "time_spent": None
                }
            ]
        
        return {
            "student_id": student_id,
            "total_quizzes": len(quizzes),
            "assigned_quizzes": len([q for q in quizzes if q["status"] == "assigned"]),
            "completed_quizzes": len([q for q in quizzes if q["status"] == "completed"]),
            "quizzes": quizzes
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur get_student_quizzes: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération: {str(e)}")

@router.get("/student/{student_id}/assigned")
def get_assigned_quizzes(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Récupérer les quiz assignés à un étudiant"""
    try:
        all_quizzes = get_student_quizzes(student_id, db)
        assigned = [q for q in all_quizzes["quizzes"] if q["status"] == "assigned"]
        
        return {
            "student_id": student_id,
            "total_assigned": len(assigned),
            "quizzes": assigned
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@router.get("/student/{student_id}/completed")
def get_completed_quizzes(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Récupérer les quiz complétés par un étudiant"""
    try:
        all_quizzes = get_student_quizzes(student_id, db)
        completed = [q for q in all_quizzes["quizzes"] if q["status"] == "completed"]
        
        return {
            "student_id": student_id,
            "total_completed": len(completed),
            "average_score": sum(q["score"] for q in completed) / len(completed) if completed else 0,
            "quizzes": completed
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@router.get("/student/{student_id}/performance")
def get_student_performance(
    student_id: int,
    subject: str = Query(None, description="Filtrer par sujet"),
    db: Session = Depends(get_db)
):
    """Récupérer les performances d'un étudiant"""
    try:
        # Vérifier que l'étudiant existe
        student = db.query(User).filter(User.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Étudiant non trouvé")
        
        # Récupérer les résultats
        query = db.query(QuizResult).filter(QuizResult.student_id == student_id)
        
        if subject:
            query = query.filter(QuizResult.sujet == subject)
        
        results = query.all()
        
        if not results:
            return {
                "student_id": student_id,
                "subject": subject,
                "message": "Aucun résultat trouvé",
                "performance": {}
            }
        
        # Calculer les performances
        total_quizzes = len(results)
        total_score = sum(r.score for r in results)
        average_score = total_score / total_quizzes
        
        # Performance par sujet
        subject_performance = {}
        for result in results:
            subj = result.sujet or "Général"
            if subj not in subject_performance:
                subject_performance[subj] = {"total": 0, "count": 0, "scores": []}
            
            subject_performance[subj]["total"] += result.score
            subject_performance[subj]["count"] += 1
            subject_performance[subj]["scores"].append(result.score)
        
        # Calculer les moyennes par sujet
        for subj in subject_performance:
            scores = subject_performance[subj]["scores"]
            subject_performance[subj]["average"] = sum(scores) / len(scores)
            subject_performance[subj]["min"] = min(scores)
            subject_performance[subj]["max"] = max(scores)
        
        performance = {
            "student_id": student_id,
            "total_quizzes": total_quizzes,
            "overall_average": round(average_score, 2),
            "subject_performance": subject_performance,
            "recent_trend": "stable",  # À calculer plus précisément
            "strengths": [subj for subj, perf in subject_performance.items() if perf["average"] >= 70],
            "weaknesses": [subj for subj, perf in subject_performance.items() if perf["average"] < 50]
        }
        
        return performance
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@router.get("/student/{student_id}/recommendations")
def get_quiz_recommendations(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Obtenir des recommandations de quiz pour un étudiant"""
    try:
        # Vérifier que l'étudiant existe
        student = db.query(User).filter(User.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Étudiant non trouvé")
        
        # Récupérer les performances directement sans appeler get_student_performance
        query = db.query(QuizResult).filter(QuizResult.student_id == student_id)
        results = query.all()
        
        if not results:
            # Aucun résultat, recommandations générales
            recommendations = [
                {
                    "type": "exploration",
                    "subject": "Français",
                    "difficulty": "medium",
                    "reason": "Découvrir de nouveaux concepts",
                    "priority": "medium"
                }
            ]
        else:
            # Calculer les performances par sujet
            subject_performance = {}
            for result in results:
                subj = result.sujet or "Général"
                if subj not in subject_performance:
                    subject_performance[subj] = {"total": 0, "count": 0, "scores": []}
                
                subject_performance[subj]["total"] += result.score
                subject_performance[subj]["count"] += 1
                subject_performance[subj]["scores"].append(result.score)
            
            # Calculer les moyennes par sujet
            for subj in subject_performance:
                scores = subject_performance[subj]["scores"]
                subject_performance[subj]["average"] = sum(scores) / len(scores)
            
            recommendations = []
            
            # Recommandations basées sur les performances
            weaknesses = [subj for subj, perf in subject_performance.items() if perf["average"] < 50]
            strengths = [subj for subj, perf in subject_performance.items() if perf["average"] >= 70]
            
            if weaknesses:
                for weakness in weaknesses:
                    recommendations.append({
                        "type": "remediation",
                        "subject": weakness,
                        "difficulty": "easy",
                        "reason": f"Renforcer les bases en {weakness}",
                        "priority": "high"
                    })
            
            if strengths:
                for strength in strengths:
                    recommendations.append({
                        "type": "advancement",
                        "subject": strength,
                        "difficulty": "hard",
                        "reason": f"Explorer des concepts avancés en {strength}",
                        "priority": "medium"
                    })
            
            # Recommandations générales si aucune spécifique
            if not recommendations:
                recommendations = [
                    {
                        "type": "exploration",
                        "subject": "Français",
                        "difficulty": "medium",
                        "reason": "Découvrir de nouveaux concepts",
                        "priority": "medium"
                    }
                ]
        
        return {
            "student_id": student_id,
            "total_recommendations": len(recommendations),
            "recommendations": recommendations
        }
        
    except Exception as e:
        print(f"❌ Erreur get_quiz_recommendations: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération: {str(e)}")
