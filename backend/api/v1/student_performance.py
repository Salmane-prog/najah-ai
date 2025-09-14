from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from core.database import SessionLocal, get_db
from models.adaptive_evaluation import AdaptiveTest, TestAttempt
from models.user import User
from models.learning_path import LearningPath
from models.student_learning_path import StudentLearningPath
from models.badge import Badge, UserBadge
from models.learning_history import LearningHistory
from core.security import get_current_user
from api.v1.auth import require_role
from typing import List, Dict, Any
from datetime import datetime, timedelta
import json
from models.class_group import ClassStudent
from models.class_group import ClassGroup

router = APIRouter()

@router.get("/class/{class_id}/students-performance")
def get_class_students_performance(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Obtenir les performances de tous les étudiants d'une classe."""
    try:
        # Vérifier que la classe existe
        class_group = db.query(ClassGroup).filter(ClassGroup.id == class_id).first()
        if not class_group:
            raise HTTPException(status_code=404, detail="Classe non trouvée")
        
        # Récupérer tous les étudiants de la classe
        class_students = db.query(ClassStudent).filter(ClassStudent.class_id == class_id).all()
        
        students_performance = []
        
        for class_student in class_students:
            student = db.query(User).filter(User.id == class_student.student_id).first()
            if not student:
                continue
            
            # Récupérer les résultats de test de l'étudiant depuis test_attempts
            test_attempts = db.query(TestAttempt).filter(TestAttempt.student_id == student.id).all()
            
            # Calculer les statistiques
            total_quizzes = len(test_attempts)
            if total_quizzes > 0:
                total_score = sum(attempt.total_score or 0 for attempt in test_attempts)
                max_possible_score = sum(attempt.max_score or 1 for attempt in test_attempts)
                
                if max_possible_score > 0:
                    overall_percentage = (total_score / max_possible_score) * 100
                else:
                    overall_percentage = 0
                    
                average_score = overall_percentage  # Le score moyen est le pourcentage
            else:
                average_score = 0
                overall_percentage = 0
            
            # Récupérer l'activité récente
            recent_activity = db.query(LearningHistory).filter(
                LearningHistory.student_id == student.id
            ).order_by(LearningHistory.timestamp.desc()).limit(5).all()
            
            students_performance.append({
                "student_id": student.id,
                "student_name": student.username or student.email,
                "total_quizzes": total_quizzes,
                "average_score": round(average_score, 2),
                "overall_percentage": round(overall_percentage, 2),
                "recent_activity_count": len(recent_activity),
                "last_activity": recent_activity[0].timestamp.isoformat() if recent_activity else None
            })
        
        # Calculer les statistiques de la classe
        if students_performance:
            class_average = sum(s["overall_percentage"] for s in students_performance) / len(students_performance)
            class_max = max(s["overall_percentage"] for s in students_performance)
            class_min = min(s["overall_percentage"] for s in students_performance)
        else:
            class_average = 0
            class_max = 0
            class_min = 0
        
        return {
            "class_id": class_id,
            "class_name": class_group.name,
            "students_count": len(students_performance),
            "class_average": round(class_average, 2),
            "class_max": round(class_max, 2),
            "class_min": round(class_min, 2),
            "students": students_performance
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'analyse de performance de classe: {str(e)}")

@router.get("/my-performance")
def get_my_performance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtenir la performance de l'étudiant connecté (pour étudiants)."""
    try:
        # Vérifier que l'utilisateur est un étudiant
        if current_user.role != "student":
            raise HTTPException(status_code=403, detail="Accès réservé aux étudiants")
        
        student_id = current_user.id
        
        # Récupérer les résultats de test depuis test_attempts (même logique que le dashboard professeur)
        # Récupérer d'abord les classes de l'étudiant
        student_classes = db.query(ClassStudent).join(ClassGroup).filter(
            ClassStudent.student_id == student_id
        ).all()
        
        # Récupérer les tests créés par les professeurs de ces classes
        teacher_ids = [cls.class_group.teacher_id for cls in student_classes if cls.class_group.teacher_id]
        
        if teacher_ids:
            test_attempts = db.query(TestAttempt).join(AdaptiveTest).filter(
                AdaptiveTest.created_by.in_(teacher_ids),
                TestAttempt.student_id == student_id
            ).all()
        else:
            test_attempts = []
        
        # Calculer les statistiques
        total_quizzes = len(test_attempts)
        if total_quizzes > 0:
            total_score = sum(attempt.total_score or 0 for attempt in test_attempts)
            max_possible_score = sum(attempt.max_score or 1 for attempt in test_attempts)
            
            if max_possible_score > 0:
                overall_percentage = (total_score / max_possible_score) * 100
            else:
                overall_percentage = 0
                
            average_score = overall_percentage  # Le score moyen est le pourcentage
        else:
            average_score = 0
            overall_percentage = 0
        
        # Analyser par sujet (simplifié pour l'instant)
        subject_analysis = {}
        for attempt in test_attempts:
            test = db.query(AdaptiveTest).filter(AdaptiveTest.id == attempt.test_id).first()
            if test and test.subject:
                if test.subject not in subject_analysis:
                    subject_analysis[test.subject] = {
                        "total_quizzes": 0,
                        "total_score": 0,
                        "max_score": 0,
                        "average_score": 0
                    }
                
                subject_analysis[test.subject]["total_quizzes"] += 1
                subject_analysis[test.subject]["total_score"] += attempt.total_score or 0
                subject_analysis[test.subject]["max_score"] += attempt.max_score or 1
        
        # Calculer les moyennes par sujet
        for subject, data in subject_analysis.items():
            if data["total_quizzes"] > 0:
                data["average_score"] = data["total_score"] / data["total_quizzes"]
                data["percentage"] = (data["total_score"] / data["max_score"]) * 100 if data["max_score"] > 0 else 0
        
        # Récupérer l'historique d'apprentissage
        learning_history = db.query(LearningHistory).filter(
            LearningHistory.student_id == student_id
        ).order_by(LearningHistory.timestamp.desc()).limit(10).all()
        
        # Analyser les tendances
        recent_scores = [entry.score for entry in learning_history if entry.score is not None]
        trend = "stable"
        if len(recent_scores) >= 2:
            if recent_scores[0] > recent_scores[-1]:
                trend = "improving"
            elif recent_scores[0] < recent_scores[-1]:
                trend = "declining"
        
        return {
            "student_id": student_id,
            "student_name": current_user.username,
            "total_quizzes": total_quizzes,
            "average_score": round(average_score, 2),
            "overall_percentage": round(overall_percentage, 2),
            "trend": trend,
            "subject_analysis": subject_analysis,
            "recent_activity": len(learning_history),
            "last_activity": learning_history[0].created_at.isoformat() if learning_history else None
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'analyse de performance: {str(e)}")

@router.get("/{student_id}")
def get_student_performance(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Obtenir la performance détaillée d'un étudiant (pour professeurs/admins)."""
    try:
        # Vérifier que l'étudiant existe
        student = db.query(User).filter(User.id == student_id, User.role == "student").first()
        if not student:
            raise HTTPException(status_code=404, detail="Étudiant non trouvé")
        
        # Récupérer les résultats de test depuis test_attempts
        test_attempts = db.query(TestAttempt).filter(TestAttempt.student_id == student_id).all()
        
        # Calculer les statistiques
        total_quizzes = len(test_attempts)
        if total_quizzes > 0:
            total_score = sum(attempt.total_score or 0 for attempt in test_attempts)
            max_possible_score = sum(attempt.max_score or 1 for attempt in test_attempts)
            
            if max_possible_score > 0:
                overall_percentage = (total_score / max_possible_score) * 100
            else:
                overall_percentage = 0
                
            average_score = overall_percentage  # Le score moyen est le pourcentage
        else:
            average_score = 0
            overall_percentage = 0
        
        # Analyser par sujet (simplifié pour l'instant)
        subject_analysis = {}
        for attempt in test_attempts:
            test = db.query(AdaptiveTest).filter(AdaptiveTest.id == attempt.test_id).first()
            if test and test.subject:
                if test.subject not in subject_analysis:
                    subject_analysis[test.subject] = {
                        "total_quizzes": 0,
                        "total_score": 0,
                        "max_score": 0,
                        "average_score": 0
                    }
                
                subject_analysis[test.subject]["total_quizzes"] += 1
                subject_analysis[test.subject]["total_score"] += attempt.total_score or 0
                subject_analysis[test.subject]["max_score"] += attempt.max_score or 1
        
        # Calculer les moyennes par sujet
        for subject, data in subject_analysis.items():
            if data["total_quizzes"] > 0:
                data["average_score"] = data["total_score"] / data["total_quizzes"]
                data["percentage"] = (data["total_score"] / data["max_score"]) * 100 if data["max_score"] > 0 else 0
        
        # Récupérer l'historique d'apprentissage
        learning_history = db.query(LearningHistory).filter(
            LearningHistory.student_id == student_id
        ).order_by(LearningHistory.timestamp.desc()).limit(10).all()
        
        # Analyser les tendances
        recent_scores = [entry.score for entry in learning_history if entry.score is not None]
        trend = "stable"
        if len(recent_scores) >= 2:
            if recent_scores[0] > recent_scores[-1]:
                trend = "improving"
            elif recent_scores[0] < recent_scores[-1]:
                trend = "declining"
        
        return {
            "student_id": student_id,
            "student_name": student.username,
            "total_quizzes": total_quizzes,
            "average_score": round(average_score, 2),
            "overall_percentage": round(overall_percentage, 2),
            "trend": trend,
            "subject_analysis": subject_analysis,
            "recent_activity": len(learning_history),
            "last_activity": learning_history[0].created_at.isoformat() if learning_history else None
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'analyse de performance: {str(e)}")

@router.get("/{student_id}/progress")
def get_student_progress(
    student_id: int,
    period: str = "month",
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Obtenir la progression détaillée d'un étudiant."""
    try:
        # Calculer la période
        if period == "week":
            start_date = datetime.utcnow() - timedelta(days=7)
        elif period == "month":
            start_date = datetime.utcnow() - timedelta(days=30)
        elif period == "year":
            start_date = datetime.utcnow() - timedelta(days=365)
        else:
            start_date = datetime.utcnow() - timedelta(days=30)
        
        # Récupérer les résultats récents
        recent_results = db.query(QuizResult).filter(
            QuizResult.student_id == student_id,
            QuizResult.created_at >= start_date
        ).order_by(QuizResult.created_at.asc()).all()
        
        # Analyser la progression
        progress_data = []
        cumulative_score = 0
        cumulative_max = 0
        
        for result in recent_results:
            cumulative_score += result.score
            cumulative_max += result.max_score
            percentage = (cumulative_score / cumulative_max) * 100 if cumulative_max > 0 else 0
            
            progress_data.append({
                "date": result.created_at.isoformat(),
                "quiz_id": result.quiz_id,
                "score": result.score,
                "max_score": result.max_score,
                "percentage": round(percentage, 2),
                "cumulative_percentage": round(percentage, 2)
            })
        
        # Calculer les métriques de progression
        if progress_data:
            initial_percentage = progress_data[0]["cumulative_percentage"]
            final_percentage = progress_data[-1]["cumulative_percentage"]
            improvement = final_percentage - initial_percentage
        else:
            improvement = 0
        
        return {
            "student_id": student_id,
            "period": period,
            "total_quizzes": len(recent_results),
            "improvement": round(improvement, 2),
            "progress_data": progress_data,
            "current_level": "intermediate" if improvement > 5 else "beginner"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'analyse de progression: {str(e)}") 