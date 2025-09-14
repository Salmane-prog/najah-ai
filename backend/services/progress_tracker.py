#!/usr/bin/env python3
"""
Système de suivi de progression des étudiants
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import json

from models.student_learning_path import StudentLearningPath
from models.learning_path import LearningPath
from models.learning_path_step import LearningPathStep
from models.assessment_result import AssessmentResult
from models.quiz_result import QuizResult
from models.user import User

class ProgressTracker:
    """Système de suivi de progression intelligent"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_student_overall_progress(self, student_id: int) -> Dict[str, Any]:
        """Obtenir la progression globale d'un étudiant"""
        
        # Récupérer tous les parcours de l'étudiant
        student_paths = self.db.query(StudentLearningPath).filter(
            StudentLearningPath.student_id == student_id
        ).all()
        
        # Récupérer les résultats d'évaluation
        assessment_results = self.db.query(AssessmentResult).filter(
            AssessmentResult.student_id == student_id
        ).all()
        
        # Récupérer les résultats de quiz
        quiz_results = self.db.query(QuizResult).filter(
            QuizResult.student_id == student_id
        ).all()
        
        # Calculer les statistiques globales
        total_paths = len(student_paths)
        completed_paths = len([p for p in student_paths if p.is_completed])
        active_paths = len([p for p in student_paths if not p.is_completed])
        
        # Progression moyenne des parcours
        avg_progress = 0
        if student_paths:
            avg_progress = sum(p.progress or 0 for p in student_paths) / len(student_paths)
        
        # Score moyen des évaluations
        avg_assessment_score = 0
        if assessment_results:
            avg_assessment_score = sum(r.percentage for r in assessment_results) / len(assessment_results)
        
        # Score moyen des quiz
        avg_quiz_score = 0
        if quiz_results:
            avg_quiz_score = sum(r.percentage for r in quiz_results) / len(quiz_results)
        
        # Calculer le niveau global
        overall_level = self._calculate_overall_level(avg_assessment_score, avg_quiz_score, avg_progress)
        
        # Calculer le temps d'apprentissage total
        total_study_time = self._calculate_total_study_time(student_id)
        
        return {
            "student_id": student_id,
            "overall_level": overall_level,
            "learning_paths": {
                "total": total_paths,
                "completed": completed_paths,
                "active": active_paths,
                "average_progress": round(avg_progress, 1)
            },
            "assessments": {
                "total": len(assessment_results),
                "average_score": round(avg_assessment_score, 1)
            },
            "quizzes": {
                "total": len(quiz_results),
                "average_score": round(avg_quiz_score, 1)
            },
            "study_time": {
                "total_minutes": total_study_time,
                "total_hours": round(total_study_time / 60, 1),
                "average_per_day": self._calculate_daily_average(student_id)
            },
            "last_updated": datetime.utcnow().isoformat()
        }
    
    def get_subject_progress(self, student_id: int, subject: str) -> Dict[str, Any]:
        """Obtenir la progression par matière"""
        
        # Récupérer les parcours de cette matière
        subject_paths = self.db.query(StudentLearningPath).join(LearningPath).filter(
            StudentLearningPath.student_id == student_id,
            LearningPath.subject == subject
        ).all()
        
        # Récupérer les évaluations de cette matière
        subject_assessments = self.db.query(AssessmentResult).join(Assessment).filter(
            AssessmentResult.student_id == student_id,
            Assessment.subject == subject
        ).all()
        
        # Calculer les statistiques de la matière
        total_paths = len(subject_paths)
        completed_paths = len([p for p in subject_paths if p.is_completed])
        avg_progress = 0
        if subject_paths:
            avg_progress = sum(p.progress or 0 for p in subject_paths) / len(subject_paths)
        
        avg_score = 0
        if subject_assessments:
            avg_score = sum(a.percentage for a in subject_assessments) / len(subject_assessments)
        
        # Déterminer le niveau dans cette matière
        subject_level = self._calculate_subject_level(avg_score, avg_progress)
        
        # Identifier les forces et faiblesses
        strengths, weaknesses = self._analyze_subject_performance(subject_assessments, subject_paths)
        
        return {
            "subject": subject,
            "student_id": student_id,
            "level": subject_level,
            "learning_paths": {
                "total": total_paths,
                "completed": completed_paths,
                "active": total_paths - completed_paths,
                "average_progress": round(avg_progress, 1)
            },
            "assessments": {
                "total": len(subject_assessments),
                "average_score": round(avg_score, 1)
            },
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": self._generate_subject_recommendations(subject_level, strengths, weaknesses)
        }
    
    def track_step_completion(self, student_id: int, learning_path_id: int, step_number: int) -> Dict[str, Any]:
        """Suivre la complétion d'une étape"""
        
        # Récupérer le parcours de l'étudiant
        student_path = self.db.query(StudentLearningPath).filter(
            StudentLearningPath.student_id == student_id,
            StudentLearningPath.learning_path_id == learning_path_id
        ).first()
        
        if not student_path:
            return {"error": "Parcours non trouvé"}
        
        # Récupérer le nombre total d'étapes
        total_steps = self.db.query(LearningPathStep).filter(
            LearningPathStep.learning_path_id == learning_path_id
        ).count()
        
        # Mettre à jour la progression
        if step_number <= total_steps:
            progress_percentage = (step_number / total_steps) * 100
            student_path.progress = progress_percentage
            student_path.current_step = step_number + 1
            
            # Vérifier si le parcours est terminé
            if step_number >= total_steps:
                student_path.is_completed = True
                student_path.completed_at = datetime.utcnow()
                student_path.progress = 100.0
            
            self.db.commit()
            
            # Calculer les nouvelles statistiques
            updated_progress = self.get_student_overall_progress(student_id)
            
            return {
                "success": True,
                "step_completed": step_number,
                "new_progress": progress_percentage,
                "is_path_completed": student_path.is_completed,
                "updated_overall_progress": updated_progress
            }
        
        return {"error": "Numéro d'étape invalide"}
    
    def get_learning_analytics(self, student_id: int, period: str = "month") -> Dict[str, Any]:
        """Obtenir des analytics d'apprentissage détaillés"""
        
        # Déterminer la période
        if period == "week":
            start_date = datetime.utcnow() - timedelta(days=7)
        elif period == "month":
            start_date = datetime.utcnow() - timedelta(days=30)
        else:  # year
            start_date = datetime.utcnow() - timedelta(days=365)
        
        # Récupérer les activités de la période
        recent_assessments = self.db.query(AssessmentResult).filter(
            AssessmentResult.student_id == student_id,
            AssessmentResult.completed_at >= start_date
        ).all()
        
        recent_quizzes = self.db.query(QuizResult).filter(
            QuizResult.student_id == student_id,
            QuizResult.completed_at >= start_date
        ).all()
        
        # Analyser la progression temporelle
        daily_progress = self._calculate_daily_progress(student_id, start_date)
        
        # Calculer les tendances
        trends = self._calculate_learning_trends(student_id, start_date)
        
        # Identifier les patterns d'apprentissage
        learning_patterns = self._identify_learning_patterns(student_id, start_date)
        
        return {
            "student_id": student_id,
            "period": period,
            "start_date": start_date.isoformat(),
            "activities": {
                "assessments_completed": len(recent_assessments),
                "quizzes_completed": len(recent_quizzes),
                "total_activities": len(recent_assessments) + len(recent_quizzes)
            },
            "daily_progress": daily_progress,
            "trends": trends,
            "learning_patterns": learning_patterns,
            "recommendations": self._generate_analytics_recommendations(trends, learning_patterns)
        }
    
    def _calculate_overall_level(self, avg_assessment: float, avg_quiz: float, avg_progress: float) -> str:
        """Calculer le niveau global de l'étudiant"""
        
        # Pondération : 40% évaluations, 30% quiz, 30% progression
        weighted_score = (avg_assessment * 0.4) + (avg_quiz * 0.3) + (avg_progress * 0.3)
        
        if weighted_score >= 80:
            return "Avancé"
        elif weighted_score >= 60:
            return "Intermédiaire"
        else:
            return "Débutant"
    
    def _calculate_subject_level(self, avg_score: float, avg_progress: float) -> str:
        """Calculer le niveau dans une matière spécifique"""
        
        # Pondération : 60% score, 40% progression
        weighted_score = (avg_score * 0.6) + (avg_progress * 0.4)
        
        if weighted_score >= 80:
            return "Avancé"
        elif weighted_score >= 60:
            return "Intermédiaire"
        else:
            return "Débutant"
    
    def _calculate_total_study_time(self, student_id: int) -> int:
        """Calculer le temps total d'étude (en minutes)"""
        
        # Estimation basée sur les activités complétées
        # Évaluations : 45 minutes en moyenne
        # Quiz : 20 minutes en moyenne
        # Étapes de parcours : 15 minutes en moyenne
        
        assessment_time = self.db.query(AssessmentResult).filter(
            AssessmentResult.student_id == student_id,
            AssessmentResult.completed_at.isnot(None)
        ).count() * 45
        
        quiz_time = self.db.query(QuizResult).filter(
            QuizResult.student_id == student_id,
            QuizResult.is_completed == True
        ).count() * 20
        
        # Temps des étapes de parcours
        path_steps = self.db.query(StudentLearningPath).filter(
            StudentLearningPath.student_id == student_id
        ).all()
        
        path_time = 0
        for path in path_steps:
            if path.current_step and path.current_step > 1:
                path_time += (path.current_step - 1) * 15
        
        return assessment_time + quiz_time + path_time
    
    def _calculate_daily_average(self, student_id: int) -> float:
        """Calculer la moyenne quotidienne d'étude"""
        
        # Récupérer la date de création du compte
        user = self.db.query(User).filter(User.id == student_id).first()
        if not user or not user.created_at:
            return 0.0
        
        days_since_creation = (datetime.utcnow() - user.created_at).days
        if days_since_creation == 0:
            days_since_creation = 1
        
        total_time = self._calculate_total_study_time(student_id)
        return round(total_time / days_since_creation, 1)
    
    def _analyze_subject_performance(self, assessments: List[AssessmentResult], paths: List[StudentLearningPath]) -> tuple:
        """Analyser les performances dans une matière"""
        
        strengths = []
        weaknesses = []
        
        # Analyser les évaluations
        if assessments:
            recent_scores = [a.percentage for a in assessments[-3:]]  # 3 dernières évaluations
            if recent_scores:
                avg_recent = sum(recent_scores) / len(recent_scores)
                if avg_recent >= 80:
                    strengths.append("Excellente progression récente")
                elif avg_recent < 60:
                    weaknesses.append("Difficultés dans les évaluations récentes")
        
        # Analyser les parcours
        if paths:
            completed_paths = [p for p in paths if p.is_completed]
            if completed_paths:
                strengths.append(f"{len(completed_paths)} parcours complétés avec succès")
            
            active_paths = [p for p in paths if not p.is_completed]
            if active_paths:
                slow_progress = [p for p in active_paths if p.progress and p.progress < 30]
                if slow_progress:
                    weaknesses.append("Progression lente dans certains parcours")
        
        return strengths, weaknesses
    
    def _generate_subject_recommendations(self, level: str, strengths: List[str], weaknesses: List[str]) -> List[str]:
        """Générer des recommandations pour une matière"""
        
        recommendations = []
        
        if level == "Débutant":
            recommendations.append("Concentrez-vous sur les concepts de base")
            recommendations.append("Pratiquez régulièrement avec des exercices simples")
        elif level == "Intermédiaire":
            recommendations.append("Renforcez vos points forts identifiés")
            if weaknesses:
                recommendations.append("Travaillez sur les points faibles identifiés")
        else:  # Avancé
            recommendations.append("Explorez des sujets plus complexes")
            recommendations.append("Aidez les autres étudiants")
        
        # Recommandations basées sur les forces et faiblesses
        if strengths:
            recommendations.append("Continuez à développer vos forces")
        
        if weaknesses:
            recommendations.append("Développez des stratégies pour surmonter les difficultés")
        
        return recommendations[:5]  # Limiter à 5 recommandations
    
    def _calculate_daily_progress(self, student_id: int, start_date: datetime) -> List[Dict[str, Any]]:
        """Calculer la progression quotidienne"""
        
        daily_progress = []
        current_date = start_date
        
        while current_date <= datetime.utcnow():
            # Compter les activités du jour
            day_assessments = self.db.query(AssessmentResult).filter(
                AssessmentResult.student_id == student_id,
                AssessmentResult.completed_at >= current_date,
                AssessmentResult.completed_at < current_date + timedelta(days=1)
            ).count()
            
            day_quizzes = self.db.query(QuizResult).filter(
                QuizResult.student_id == student_id,
                QuizResult.completed_at >= current_date,
                QuizResult.completed_at < current_date + timedelta(days=1)
            ).count()
            
            daily_progress.append({
                "date": current_date.date().isoformat(),
                "assessments": day_assessments,
                "quizzes": day_quizzes,
                "total_activities": day_assessments + day_quizzes
            })
            
            current_date += timedelta(days=1)
        
        return daily_progress
    
    def _calculate_learning_trends(self, student_id: int, start_date: datetime) -> Dict[str, Any]:
        """Calculer les tendances d'apprentissage"""
        
        # Diviser la période en deux pour comparer
        mid_date = start_date + (datetime.utcnow() - start_date) / 2
        
        # Première moitié
        first_half_assessments = self.db.query(AssessmentResult).filter(
            AssessmentResult.student_id == student_id,
            AssessmentResult.completed_at >= start_date,
            AssessmentResult.completed_at < mid_date
        ).all()
        
        # Deuxième moitié
        second_half_assessments = self.db.query(AssessmentResult).filter(
            AssessmentResult.student_id == student_id,
            AssessmentResult.completed_at >= mid_date,
            AssessmentResult.completed_at <= datetime.utcnow()
        ).all()
        
        # Calculer les moyennes
        first_avg = 0
        if first_half_assessments:
            first_avg = sum(a.percentage for a in first_half_assessments) / len(first_half_assessments)
        
        second_avg = 0
        if second_half_assessments:
            second_avg = sum(a.percentage for a in second_half_assessments) / len(second_half_assessments)
        
        # Déterminer la tendance
        if second_avg > first_avg + 5:
            trend = "Amélioration"
        elif second_avg < first_avg - 5:
            trend = "Déclin"
        else:
            trend = "Stable"
        
        return {
            "trend": trend,
            "first_half_average": round(first_avg, 1),
            "second_half_average": round(second_avg, 1),
            "improvement": round(second_avg - first_avg, 1)
        }
    
    def _identify_learning_patterns(self, student_id: int, start_date: datetime) -> Dict[str, Any]:
        """Identifier les patterns d'apprentissage"""
        
        # Analyser les jours de la semaine
        weekday_activity = {i: 0 for i in range(7)}  # 0 = Lundi, 6 = Dimanche
        
        # Récupérer toutes les activités de la période
        activities = self.db.query(AssessmentResult).filter(
            AssessmentResult.student_id == student_id,
            AssessmentResult.completed_at >= start_date
        ).all()
        
        activities.extend(self.db.query(QuizResult).filter(
            QuizResult.student_id == student_id,
            QuizResult.completed_at >= start_date
        ).all())
        
        # Compter par jour de la semaine
        for activity in activities:
            completed_at = activity.completed_at
            if completed_at:
                weekday = completed_at.weekday()
                weekday_activity[weekday] += 1
        
        # Identifier le jour le plus actif
        most_active_day = max(weekday_activity, key=weekday_activity.get)
        day_names = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        
        # Analyser la fréquence
        total_activities = sum(weekday_activity.values())
        if total_activities > 0:
            frequency = "Régulier" if total_activities >= 10 else "Occasionnel"
        else:
            frequency = "Aucune activité"
        
        return {
            "most_active_day": day_names[most_active_day],
            "frequency": frequency,
            "total_activities": total_activities,
            "weekday_distribution": weekday_activity
        }
    
    def _generate_analytics_recommendations(self, trends: Dict[str, Any], patterns: Dict[str, Any]) -> List[str]:
        """Générer des recommandations basées sur les analytics"""
        
        recommendations = []
        
        # Recommandations basées sur les tendances
        if trends["trend"] == "Déclin":
            recommendations.append("Votre performance a diminué récemment. Revenez aux bases.")
            recommendations.append("Considérez demander de l'aide à un enseignant.")
        elif trends["trend"] == "Amélioration":
            recommendations.append("Excellente progression ! Continuez sur cette lancée.")
            recommendations.append("Vous pouvez essayer des défis plus difficiles.")
        
        # Recommandations basées sur les patterns
        if patterns["frequency"] == "Occasionnel":
            recommendations.append("Essayez d'étudier plus régulièrement pour de meilleurs résultats.")
        elif patterns["frequency"] == "Régulier":
            recommendations.append("Maintenez votre rythme d'apprentissage régulier.")
        
        if patterns["most_active_day"] in ["Samedi", "Dimanche"]:
            recommendations.append("Vous étudiez principalement le week-end. Essayez d'étudier en semaine aussi.")
        
        return recommendations[:5]  # Limiter à 5 recommandations
