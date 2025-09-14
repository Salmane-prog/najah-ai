from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json

from database import get_db
from models.user import User
from models.quiz import Quiz, QuizResult
from models.learning_history import LearningHistory
from models.class_group import ClassGroup
# Pas de modèle Subject, le sujet est un champ string dans Quiz
from core.security import get_current_user

router = APIRouter(tags=["Student Analytics"])

# ============================================================================
# ENDPOINTS D'ANALYTICS ÉTUDIANT
# ============================================================================

@router.get("/student/{student_id}/analytics")
async def get_student_analytics(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Récupérer les analytics complètes d'un étudiant"""
    try:
        # Vérifier que l'utilisateur peut accéder à ces données
        if current_user.role.value != "student" or current_user.id != student_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès non autorisé aux analytics de cet étudiant"
            )
        
        # Récupérer les données de base
        quiz_results = db.query(QuizResult).filter(QuizResult.user_id == student_id).all()
        learning_history = db.query(LearningHistory).filter(LearningHistory.student_id == student_id).all()
        
        # Calculer les métriques
        total_quizzes = len(quiz_results)
        # Utiliser le score pour déterminer si c'est correct (> 50%)
        correct_answers = sum(1 for result in quiz_results if result.percentage > 50)
        average_score = (correct_answers / total_quizzes * 100) if total_quizzes > 0 else 0
        
        # Calculer la progression
        completed_topics = len(set(history.topic for history in learning_history)) if learning_history else 0
        
        # Gérer le cas où il n'y a pas d'historique
        last_activity = None
        if learning_history:
            try:
                last_activity = max([history.timestamp for history in learning_history]).isoformat()
            except (ValueError, AttributeError):
                last_activity = None
        
        analytics = {
            "student_id": student_id,
            "total_quizzes": total_quizzes,
            "correct_answers": correct_answers,
            "average_score": round(average_score, 2),
            "completed_topics": completed_topics,
            "last_activity": last_activity,
            "performance_trend": "stable",  # À calculer plus précisément
            "strengths": [],  # À analyser à partir des résultats
            "weaknesses": []  # À analyser à partir des résultats
        }
        
        return {"status": "success", "data": analytics}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des analytics: {str(e)}"
        )

@router.get("/student/{student_id}/performance")
async def get_student_performance(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Récupérer les performances d'un étudiant"""
    try:
        if current_user.role.value != "student" or current_user.id != student_id:
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        # Récupérer les résultats des quiz
        quiz_results = db.query(QuizResult).filter(QuizResult.user_id == student_id).all()
        
        if not quiz_results:
            return {"status": "success", "data": {"message": "Aucun résultat trouvé"}}
        
        # Calculer les performances par sujet
        performance_by_subject = {}
        for result in quiz_results:
            if result.quiz and result.quiz.subject:
                subject = result.quiz.subject  # Le sujet est un champ string, pas un objet
                if subject not in performance_by_subject:
                    performance_by_subject[subject] = {"total": 0, "correct": 0, "scores": []}
                
                performance_by_subject[subject]["total"] += 1
                if result.percentage > 50:  # Considérer comme correct si > 50%
                    performance_by_subject[subject]["correct"] += 1
                performance_by_subject[subject]["scores"].append(result.score)
        
        # Calculer les moyennes
        for subject in performance_by_subject:
            scores = performance_by_subject[subject]["scores"]
            performance_by_subject[subject]["average_score"] = round(sum(scores) / len(scores), 2)
            performance_by_subject[subject]["success_rate"] = round(
                performance_by_subject[subject]["correct"] / performance_by_subject[subject]["total"] * 100, 2
            )
        
        return {"status": "success", "data": performance_by_subject}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@router.get("/student/{student_id}/progress")
async def get_student_progress(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Récupérer la progression d'un étudiant"""
    try:
        if current_user.role.value != "student" or current_user.id != student_id:
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        # Récupérer l'historique d'apprentissage
        learning_history = db.query(LearningHistory).filter(
            LearningHistory.student_id == student_id
        ).order_by(LearningHistory.timestamp.desc()).all()
        
        if not learning_history:
            return {"status": "success", "data": {"message": "Aucun historique trouvé"}}
        
        # Calculer la progression
        total_topics = len(set(history.topic for history in learning_history))
        completed_topics = len(set(history.topic for history in learning_history if history.status == "completed"))
        
        progress = {
            "student_id": student_id,
            "total_topics": total_topics,
            "completed_topics": completed_topics,
            "completion_rate": round(completed_topics / total_topics * 100, 2) if total_topics > 0 else 0,
            "recent_activities": [
                {
                    "topic": history.topic,
                    "status": history.status,
                    "timestamp": history.timestamp.isoformat()
                }
                for history in learning_history[:10]  # 10 dernières activités
            ]
        }
        
        return {"status": "success", "data": progress}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@router.get("/student/{student_id}/subjects")
async def get_student_subjects(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Récupérer les sujets d'un étudiant"""
    try:
        if current_user.role.value != "student" or current_user.id != student_id:
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        # Récupérer les sujets depuis l'historique d'apprentissage
        learning_history = db.query(LearningHistory).filter(
            LearningHistory.student_id == student_id
        ).all()
        
        # Extraire les sujets uniques
        subjects = list(set(history.subject for history in learning_history if history.subject))
        
        # Si aucun sujet trouvé, retourner une liste vide
        if not subjects:
            return {"status": "success", "data": []}
        
        return {"status": "success", "data": subjects}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

# ============================================================================
# ENDPOINTS POUR LES QUIZ ET ASSESSMENTS
# ============================================================================

@router.get("/quiz_assignments/student/{student_id}")
async def get_student_quiz_assignments(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Récupérer les quiz assignés à un étudiant"""
    try:
        if current_user.role.value != "student" or current_user.id != student_id:
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        # Récupérer les quiz assignés (simulation)
        # Dans un vrai système, vous auriez une table quiz_assignments
        assigned_quizzes = db.query(Quiz).filter(
            Quiz.is_active == True
        ).limit(10).all()  # Limiter à 10 quiz pour la démo
        
        quiz_data = []
        for quiz in assigned_quizzes:
            quiz_data.append({
                "id": quiz.id,
                "title": quiz.title,
                "subject": quiz.subject if quiz.subject else "Général",
                "difficulty": quiz.difficulty,
                "estimated_time": quiz.estimated_time,
                "due_date": None,  # À implémenter avec une vraie table d'assignation
                "status": "assigned"
            })
        
        return {"status": "success", "data": quiz_data}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@router.get("/assessments/student/{student_id}/pending")
async def get_student_pending_assessments(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Récupérer les évaluations en attente d'un étudiant"""
    try:
        if current_user.role.value != "student" or current_user.id != student_id:
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        # Pour l'instant, retourner une liste vide
        # À implémenter avec une vraie table d'évaluations
        return {"status": "success", "data": []}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

# ============================================================================
# ENDPOINTS POUR LES CHEMINS D'APPRENTISSAGE
# ============================================================================

@router.get("/learning_paths/student/{student_id}/active")
async def get_student_active_learning_paths(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Récupérer les chemins d'apprentissage actifs d'un étudiant"""
    try:
        if current_user.role.value != "student" or current_user.id != student_id:
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        # Pour l'instant, retourner une liste vide
        # À implémenter avec une vraie table de chemins d'apprentissage
        return {"status": "success", "data": []}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

# ============================================================================
# ENDPOINTS POUR LES ANALYTICS AVANCÉES
# ============================================================================

@router.get("/student/{student_id}/cognitive_profile")
async def get_student_cognitive_profile(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Récupérer le profil cognitif d'un étudiant"""
    try:
        if current_user.role.value != "student" or current_user.id != student_id:
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        # Analyser les résultats pour déterminer le profil cognitif
        quiz_results = db.query(QuizResult).filter(QuizResult.user_id == student_id).all()
        
        if not quiz_results:
            return {"status": "success", "data": {"message": "Données insuffisantes pour l'analyse"}}
        
        # Analyse simple basée sur les scores
        scores = [result.score for result in quiz_results]
        average_score = sum(scores) / len(scores)
        
        # Déterminer le style d'apprentissage basé sur les scores
        if average_score >= 80:
            learning_style = "Excellence"
        elif average_score >= 60:
            learning_style = "Bon"
        elif average_score >= 40:
            learning_style = "Moyen"
        else:
            learning_style = "En difficulté"
        
        cognitive_profile = {
            "student_id": student_id,
            "learning_style": learning_style,
            "average_score": round(average_score, 2),
            "total_assessments": len(quiz_results),
            "strengths": ["Logique", "Mémoire"] if average_score >= 70 else [],
            "weaknesses": ["Calcul", "Concentration"] if average_score < 50 else [],
            "recommendations": [
                "Continuer avec les exercices actuels" if average_score >= 70 else "Revoir les bases",
                "Pratiquer régulièrement" if average_score < 70 else "Explorer des sujets plus avancés"
            ]
        }
        
        return {"status": "success", "data": cognitive_profile}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@router.get("/student/{student_id}/performance_trend")
async def get_student_performance_trend(
    student_id: int,
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Récupérer la tendance de performance d'un étudiant sur une période"""
    try:
        if current_user.role.value != "student" or current_user.id != student_id:
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        # Calculer la date de début
        start_date = datetime.now() - timedelta(days=days)
        
        # Récupérer les résultats sur la période
        quiz_results = db.query(QuizResult).filter(
            QuizResult.user_id == student_id,
            QuizResult.created_at >= start_date
        ).order_by(QuizResult.created_at.asc()).all()
        
        if not quiz_results:
            return {"status": "success", "data": {"message": "Aucun résultat sur cette période"}}
        
        # Grouper par semaine
        weekly_data = {}
        for result in quiz_results:
            week_start = result.created_at - timedelta(days=result.created_at.weekday())
            week_key = week_start.strftime("%Y-%m-%d")
            
            if week_key not in weekly_data:
                weekly_data[week_key] = {"scores": [], "count": 0}
            
            weekly_data[week_key]["scores"].append(result.score)
            weekly_data[week_key]["count"] += 1
        
        # Calculer les moyennes hebdomadaires
        trend_data = []
        for week, data in weekly_data.items():
            if data["scores"]:
                trend_data.append({
                    "week": week,
                    "average_score": round(sum(data["scores"]) / len(data["scores"]), 2),
                    "quiz_count": data["count"]
                })
        
        return {"status": "success", "data": trend_data}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}") 