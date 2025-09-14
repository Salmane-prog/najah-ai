from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from core.database import get_db
from models.user import User
from models.quiz import QuizResult, Quiz
from models.learning_history import LearningHistory
from models.student_analytics import StudentProgress
from api.v1.auth import require_role, get_current_user
from typing import List, Dict, Any
from datetime import datetime, timedelta
import json

router = APIRouter()

@router.get("/real-time/class/{class_id}")
def get_real_time_class_performance(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Monitoring en temps réel des performances d'une classe."""
    try:
        # Récupérer les étudiants de la classe
        from models.class_group import ClassStudent
        class_students = db.query(ClassStudent).filter(ClassStudent.class_id == class_id).all()
        student_ids = [cs.student_id for cs in class_students]
        
        if not student_ids:
            return {"message": "Aucun étudiant dans cette classe", "data": {}}
        
        # Activité des dernières 24h
        yesterday = datetime.utcnow() - timedelta(days=1)
        
        # Quiz complétés aujourd'hui
        today_quizzes = db.query(QuizResult).filter(
            QuizResult.student_id.in_(student_ids),
            QuizResult.created_at >= yesterday
        ).all()
        
        # Sessions d'apprentissage aujourd'hui
        today_sessions = db.query(LearningHistory).filter(
            LearningHistory.student_id.in_(student_ids),
            LearningHistory.timestamp >= yesterday
        ).all()
        
        # Calculer les métriques
        total_quizzes = len(today_quizzes)
        avg_score = sum(q.score for q in today_quizzes) / len(today_quizzes) if today_quizzes else 0
        active_students = len(set(q.student_id for q in today_quizzes))
        total_time = sum(s.time_spent for s in today_sessions) if today_sessions else 0
        
        # Tendances (comparaison avec hier)
        two_days_ago = datetime.utcnow() - timedelta(days=2)
        yesterday_quizzes = db.query(QuizResult).filter(
            QuizResult.student_id.in_(student_ids),
            QuizResult.created_at >= two_days_ago,
            QuizResult.created_at < yesterday
        ).all()
        
        yesterday_avg = sum(q.score for q in yesterday_quizzes) / len(yesterday_quizzes) if yesterday_quizzes else 0
        score_trend = "up" if avg_score > yesterday_avg else "down" if avg_score < yesterday_avg else "stable"
        
        return {
            "class_id": class_id,
            "timestamp": datetime.utcnow().isoformat(),
            "metrics": {
                "total_quizzes_today": total_quizzes,
                "average_score": round(avg_score, 2),
                "active_students": active_students,
                "total_learning_time": total_time,
                "score_trend": score_trend,
                "participation_rate": round((active_students / len(student_ids)) * 100, 2)
            },
            "alerts": generate_performance_alerts(avg_score, active_students, len(student_ids))
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur monitoring: {str(e)}")

@router.get("/real-time/class/{class_id}/test")
def get_real_time_class_performance_test(
    class_id: int,
    db: Session = Depends(get_db)
):
    """Monitoring en temps réel des performances d'une classe (version test sans auth)."""
    try:
        # Récupérer les étudiants de la classe
        from models.class_group import ClassStudent
        class_students = db.query(ClassStudent).filter(ClassStudent.class_id == class_id).all()
        student_ids = [cs.student_id for cs in class_students]
        
        if not student_ids:
            return {"message": "Aucun étudiant dans cette classe", "data": {}}
        
        # Activité des dernières 24h
        yesterday = datetime.utcnow() - timedelta(days=1)
        
        # Quiz complétés aujourd'hui
        today_quizzes = db.query(QuizResult).filter(
            QuizResult.student_id.in_(student_ids),
            QuizResult.created_at >= yesterday
        ).all()
        
        # Sessions d'apprentissage aujourd'hui
        today_sessions = db.query(LearningHistory).filter(
            LearningHistory.student_id.in_(student_ids),
            LearningHistory.timestamp >= yesterday
        ).all()
        
        # Calculer les métriques
        total_quizzes = len(today_quizzes)
        avg_score = sum(q.score for q in today_quizzes) / len(today_quizzes) if today_quizzes else 0
        active_students = len(set(q.student_id for q in today_quizzes))
        total_time = sum(s.time_spent for s in today_sessions) if today_sessions else 0
        
        # Tendances (comparaison avec hier)
        two_days_ago = datetime.utcnow() - timedelta(days=2)
        yesterday_quizzes = db.query(QuizResult).filter(
            QuizResult.student_id.in_(student_ids),
            QuizResult.created_at >= two_days_ago,
            QuizResult.created_at < yesterday
        ).all()
        
        yesterday_avg = sum(q.score for q in yesterday_quizzes) / len(yesterday_quizzes) if yesterday_quizzes else 0
        score_trend = "up" if avg_score > yesterday_avg else "down" if avg_score < yesterday_avg else "stable"
        
        return {
            "class_id": class_id,
            "timestamp": datetime.utcnow().isoformat(),
            "metrics": {
                "total_quizzes_today": total_quizzes,
                "average_score": round(avg_score, 2),
                "active_students": active_students,
                "total_learning_time": total_time,
                "score_trend": score_trend,
                "participation_rate": round((active_students / len(student_ids)) * 100, 2)
            },
            "alerts": generate_performance_alerts(avg_score, active_students, len(student_ids))
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur monitoring: {str(e)}")

@router.get("/student/{student_id}/detailed")
def get_student_detailed_performance(
    student_id: int,
    period: str = Query("week", description="Période: day, week, month"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Monitoring détaillé des performances d'un étudiant."""
    try:
        # Définir la période
        now = datetime.utcnow()
        if period == "day":
            start_date = now - timedelta(days=1)
        elif period == "week":
            start_date = now - timedelta(days=7)
        elif period == "month":
            start_date = now - timedelta(days=30)
        else:
            start_date = now - timedelta(days=7)
        
        # Récupérer les données
        quiz_results = db.query(QuizResult).filter(
            QuizResult.student_id == student_id,
            QuizResult.created_at >= start_date
        ).order_by(QuizResult.created_at.desc()).all()
        
        learning_sessions = db.query(LearningHistory).filter(
            LearningHistory.student_id == student_id,
            LearningHistory.timestamp >= start_date
        ).order_by(LearningHistory.timestamp.desc()).all()
        
        # Analyser par sujet
        subject_performance = {}
        for result in quiz_results:
            subject = result.sujet or "Général"
            if subject not in subject_performance:
                subject_performance[subject] = {
                    "quizzes": 0,
                    "total_score": 0,
                    "best_score": 0,
                    "worst_score": 100
                }
            
            subject_performance[subject]["quizzes"] += 1
            subject_performance[subject]["total_score"] += result.score
            subject_performance[subject]["best_score"] = max(subject_performance[subject]["best_score"], result.score)
            subject_performance[subject]["worst_score"] = min(subject_performance[subject]["worst_score"], result.score)
        
        # Calculer les moyennes
        for subject, data in subject_performance.items():
            data["average_score"] = round(data["total_score"] / data["quizzes"], 2)
        
        # Tendances temporelles
        daily_performance = {}
        for result in quiz_results:
            day = result.created_at.strftime('%Y-%m-%d')
            if day not in daily_performance:
                daily_performance[day] = []
            daily_performance[day].append(result.score)
        
        # Calculer les moyennes quotidiennes
        daily_averages = {}
        for day, scores in daily_performance.items():
            daily_averages[day] = round(sum(scores) / len(scores), 2)
        
        # Identifier les patterns
        patterns = analyze_learning_patterns(learning_sessions)
        
        return {
            "student_id": student_id,
            "period": period,
            "summary": {
                "total_quizzes": len(quiz_results),
                "total_sessions": len(learning_sessions),
                "overall_average": round(sum(r.score for r in quiz_results) / len(quiz_results), 2) if quiz_results else 0,
                "total_time": sum(s.time_spent for s in learning_sessions),
                "consistency_score": calculate_consistency_score(quiz_results)
            },
            "subject_performance": subject_performance,
            "daily_trends": daily_averages,
            "learning_patterns": patterns,
            "recommendations": generate_student_recommendations(subject_performance, patterns)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur monitoring étudiant: {str(e)}")

@router.get("/alerts/performance")
def get_performance_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Générer des alertes de performance."""
    try:
        alerts = []
        
        # Alertes pour les scores bas
        low_performers = db.query(QuizResult).filter(
            QuizResult.score < 50,
            QuizResult.created_at >= datetime.utcnow() - timedelta(days=7)
        ).all()
        
        if low_performers:
            student_ids = list(set(r.student_id for r in low_performers))
            students = db.query(User).filter(User.id.in_(student_ids)).all()
            
            for student in students:
                student_results = [r for r in low_performers if r.student_id == student.id]
                avg_score = sum(r.score for r in student_results) / len(student_results)
                
                alerts.append({
                    "type": "low_performance",
                    "severity": "high" if avg_score < 30 else "medium",
                    "student_id": student.id,
                    "student_name": student.username,
                    "message": f"Performance faible: {avg_score:.1f}% de moyenne",
                    "recommendation": "Considérer un soutien personnalisé"
                })
        
        # Alertes pour l'inactivité
        inactive_threshold = datetime.utcnow() - timedelta(days=3)
        inactive_students = db.query(User).filter(
            User.role == "student",
            ~User.id.in_(
                db.query(QuizResult.student_id).filter(QuizResult.created_at >= inactive_threshold)
            )
        ).all()
        
        for student in inactive_students:
            alerts.append({
                "type": "inactivity",
                "severity": "medium",
                "student_id": student.id,
                "student_name": student.username,
                "message": "Aucune activité depuis 3 jours",
                "recommendation": "Envoyer un rappel d'engagement"
            })
        
        return {"alerts": alerts, "count": len(alerts)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur alertes: {str(e)}")

def generate_performance_alerts(avg_score: float, active_students: int, total_students: int) -> List[Dict]:
    """Générer des alertes basées sur les métriques."""
    alerts = []
    
    if avg_score < 60:
        alerts.append({
            "type": "low_class_performance",
            "severity": "high",
            "message": f"Performance de classe faible: {avg_score:.1f}%",
            "recommendation": "Réviser les méthodes d'enseignement"
        })
    
    participation_rate = (active_students / total_students) * 100 if total_students > 0 else 0
    if participation_rate < 50:
        alerts.append({
            "type": "low_participation",
            "severity": "medium",
            "message": f"Taux de participation faible: {participation_rate:.1f}%",
            "recommendation": "Encourager l'engagement des étudiants"
        })
    
    return alerts

def analyze_learning_patterns(sessions: List[LearningHistory]) -> Dict[str, Any]:
    """Analyser les patterns d'apprentissage."""
    if not sessions:
        return {"patterns": [], "insights": []}
    
    # Analyser les heures d'activité
    hour_activity = {}
    for session in sessions:
        hour = session.timestamp.hour
        hour_activity[hour] = hour_activity.get(hour, 0) + 1
    
    # Trouver les heures de pointe
    peak_hours = sorted(hour_activity.items(), key=lambda x: x[1], reverse=True)[:3]
    
    # Analyser la durée des sessions
    session_durations = [s.time_spent for s in sessions if s.time_spent]
    avg_duration = sum(session_durations) / len(session_durations) if session_durations else 0
    
    return {
        "peak_hours": [{"hour": h, "count": c} for h, c in peak_hours],
        "average_session_duration": round(avg_duration, 2),
        "total_sessions": len(sessions),
        "preferred_activity_times": "matin" if any(h < 12 for h, _ in peak_hours) else "après-midi"
    }

def calculate_consistency_score(results: List[QuizResult]) -> float:
    """Calculer un score de cohérence basé sur la variance des scores."""
    if len(results) < 2:
        return 100.0
    
    scores = [r.score for r in results]
    mean_score = sum(scores) / len(scores)
    variance = sum((score - mean_score) ** 2 for score in scores) / len(scores)
    
    # Plus la variance est faible, plus le score de cohérence est élevé
    consistency = max(0, 100 - (variance / 10))
    return round(consistency, 2)

def generate_student_recommendations(subject_performance: Dict, patterns: Dict) -> List[str]:
    """Générer des recommandations personnalisées."""
    recommendations = []
    
    # Recommandations basées sur les performances par sujet
    weak_subjects = [subject for subject, data in subject_performance.items() 
                    if data["average_score"] < 70]
    
    if weak_subjects:
        recommendations.append(f"Focus sur les matières faibles: {', '.join(weak_subjects)}")
    
    # Recommandations basées sur les patterns
    if patterns.get("average_session_duration", 0) < 20:
        recommendations.append("Augmenter la durée des sessions d'apprentissage")
    
    if not patterns.get("peak_hours"):
        recommendations.append("Établir un planning d'étude régulier")
    
    return recommendations 