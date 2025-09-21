import numpy as np
from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta
import logging
from database_service import db_service

logger = logging.getLogger(__name__)

class AIPredictionService:
    def __init__(self):
        self.prediction_models = {}
        
    def calculate_trend(self, scores: List[float]) -> Dict[str, Any]:
        """Calculer la tendance d'une série de scores"""
        if len(scores) < 2:
            return {"trend": "stable", "slope": 0, "confidence": 0}
        
        try:
            # Régression linéaire simple
            x = np.arange(len(scores))
            y = np.array(scores)
            
            # Calculer la pente et l'intercept
            slope, intercept = np.polyfit(x, y, 1)
            
            # Calculer le coefficient de corrélation (R²)
            y_pred = slope * x + intercept
            correlation = np.corrcoef(y, y_pred)[0, 1]
            r_squared = correlation ** 2 if not np.isnan(correlation) else 0
            
            # Déterminer la tendance
            if abs(slope) < 0.5:
                trend = "stable"
            elif slope > 0.5:
                trend = "up"
            else:
                trend = "down"
            
            # Calculer la confiance basée sur R²
            confidence = min(95, max(5, r_squared * 100))
            
            return {
                "trend": trend,
                "slope": round(slope, 2),
                "confidence": round(confidence, 1),
                "r_squared": round(r_squared, 3)
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du calcul de tendance: {e}")
            return {"trend": "stable", "slope": 0, "confidence": 0}
    
    def predict_student_performance(self, student_id: int, days_ahead: int = 30) -> Dict[str, Any]:
        """Prédire la performance future d'un étudiant"""
        try:
            # Récupérer l'historique de l'étudiant
            history = db_service.get_student_learning_history(student_id, days=90)
            
            if not history:
                return {"error": "Pas assez de données pour la prédiction"}
            
            # Extraire les scores et dates
            scores = [float(record['score']) for record in history]
            dates = [datetime.fromisoformat(record['created_at']) for record in history]
            
            # Calculer la tendance actuelle
            trend_analysis = self.calculate_trend(scores)
            
            # Prédiction basée sur la tendance
            if trend_analysis['trend'] == "up":
                predicted_score = min(100, scores[-1] + (trend_analysis['slope'] * days_ahead / 30))
                improvement_potential = "Élevé"
            elif trend_analysis['trend'] == "down":
                predicted_score = max(0, scores[-1] + (trend_analysis['slope'] * days_ahead / 30))
                improvement_potential = "Faible"
            else:
                predicted_score = scores[-1]
                improvement_potential = "Moyen"
            
            # Calculer la variabilité des scores
            score_variability = np.std(scores) if len(scores) > 1 else 0
            
            # Recommandations basées sur l'analyse
            recommendations = self._generate_student_recommendations(
                trend_analysis, score_variability, scores[-1]
            )
            
            return {
                "student_id": student_id,
                "current_average": round(np.mean(scores), 1),
                "predicted_score": round(predicted_score, 1),
                "trend_analysis": trend_analysis,
                "score_variability": round(score_variability, 1),
                "improvement_potential": improvement_potential,
                "confidence_level": trend_analysis['confidence'],
                "recommendations": recommendations,
                "prediction_horizon_days": days_ahead,
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la prédiction pour l'étudiant {student_id}: {e}")
            return {"error": str(e)}
    
    def predict_subject_performance(self, subject: str, days_ahead: int = 30) -> Dict[str, Any]:
        """Prédire la performance future d'une matière"""
        try:
            # Récupérer les tendances de la matière
            trends = db_service.get_subject_performance_trends(subject, days=90)
            
            if not trends:
                return {"error": "Pas assez de données pour la prédiction"}
            
            # Extraire les scores moyens par date
            scores = [float(record['averageScore']) for record in trends if record['averageScore'] is not None]
            dates = [datetime.fromisoformat(record['date']) for record in trends]
            
            if len(scores) < 2:
                return {"error": "Pas assez de données pour la prédiction"}
            
            # Calculer la tendance
            trend_analysis = self.calculate_trend(scores)
            
            # Prédiction
            if trend_analysis['trend'] == "up":
                predicted_score = min(100, scores[-1] + (trend_analysis['slope'] * days_ahead / 30))
            elif trend_analysis['trend'] == "down":
                predicted_score = max(0, scores[-1] + (trend_analysis['slope'] * days_ahead / 30))
            else:
                predicted_score = scores[-1]
            
            # Analyser la saisonnalité (si assez de données)
            seasonality = self._analyze_seasonality(scores, dates) if len(scores) >= 30 else None
            
            return {
                "subject": subject,
                "current_average": round(np.mean(scores), 1),
                "predicted_score": round(predicted_score, 1),
                "trend_analysis": trend_analysis,
                "seasonality": seasonality,
                "confidence_level": trend_analysis['confidence'],
                "prediction_horizon_days": days_ahead,
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la prédiction pour la matière {subject}: {e}")
            return {"error": str(e)}
    
    def predict_class_performance(self, class_id: int, days_ahead: int = 30) -> Dict[str, Any]:
        """Prédire la performance future d'une classe entière"""
        try:
            # Récupérer tous les étudiants de la classe
            # Note: Cette requête dépend de votre structure de base de données
            class_students_query = """
            SELECT DISTINCT u.id, u.first_name, u.last_name
            FROM users u
            JOIN class_groups cg ON u.id = cg.student_id
            WHERE cg.class_id = ? AND u.role = 'student'
            """
            
            students = db_service.execute_query(class_students_query, (class_id,))
            
            if not students:
                return {"error": "Aucun étudiant trouvé dans cette classe"}
            
            # Prédire pour chaque étudiant
            student_predictions = []
            total_predicted_score = 0
            valid_predictions = 0
            
            for student in students:
                prediction = self.predict_student_performance(student['id'], days_ahead)
                if 'error' not in prediction:
                    student_predictions.append({
                        "student_id": student['id'],
                        "student_name": f"{student['first_name']} {student['last_name']}",
                        "prediction": prediction
                    })
                    total_predicted_score += prediction['predicted_score']
                    valid_predictions += 1
            
            if valid_predictions == 0:
                return {"error": "Aucune prédiction valide pour les étudiants de cette classe"}
            
            # Calculer la prédiction de classe
            class_predicted_score = total_predicted_score / valid_predictions
            
            # Analyser la distribution des prédictions
            predicted_scores = [p['prediction']['predicted_score'] for p in student_predictions]
            score_std = np.std(predicted_scores) if len(predicted_scores) > 1 else 0
            
            return {
                "class_id": class_id,
                "total_students": len(students),
                "valid_predictions": valid_predictions,
                "class_predicted_score": round(class_predicted_score, 1),
                "score_distribution": {
                    "min": round(min(predicted_scores), 1),
                    "max": round(max(predicted_scores), 1),
                    "std": round(score_std, 1)
                },
                "student_predictions": student_predictions,
                "prediction_horizon_days": days_ahead,
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la prédiction pour la classe {class_id}: {e}")
            return {"error": str(e)}
    
    def _generate_student_recommendations(self, trend: Dict, variability: float, current_score: float) -> List[str]:
        """Générer des recommandations personnalisées pour un étudiant"""
        recommendations = []
        
        if trend['trend'] == "down":
            recommendations.append("🔴 Votre performance est en baisse. Considérez revoir les concepts de base.")
            recommendations.append("📚 Planifiez des sessions de révision régulières.")
        
        elif trend['trend'] == "up":
            recommendations.append("🟢 Excellente progression ! Continuez sur cette lancée.")
            if current_score < 80:
                recommendations.append("🎯 Objectif : Atteindre 80% dans les prochaines semaines.")
        
        if variability > 15:
            recommendations.append("⚠️ Votre performance varie beaucoup. Travaillez sur la constance.")
            recommendations.append("📝 Gardez un journal de vos révisions pour identifier les difficultés.")
        
        if current_score < 60:
            recommendations.append("🚨 Score faible détecté. Demandez de l'aide à votre professeur.")
            recommendations.append("🔄 Refaites les tests précédents pour renforcer vos connaissances.")
        
        if not recommendations:
            recommendations.append("✅ Votre performance est stable. Continuez vos efforts !")
        
        return recommendations
    
    def _analyze_seasonality(self, scores: List[float], dates: List[datetime]) -> Dict[str, Any]:
        """Analyser la saisonnalité des scores"""
        try:
            if len(scores) < 30:
                return None
            
            # Convertir en array numpy
            scores_array = np.array(scores)
            
            # Calculer la moyenne mobile sur 7 jours
            window_size = min(7, len(scores) // 4)
            moving_avg = np.convolve(scores_array, np.ones(window_size)/window_size, mode='valid')
            
            # Calculer la variance expliquée par la saisonnalité
            if len(moving_avg) > 1:
                seasonal_variance = np.var(moving_avg) / np.var(scores_array)
            else:
                seasonal_variance = 0
            
            return {
                "has_seasonality": seasonal_variance > 0.1,
                "seasonal_strength": round(seasonal_variance, 3),
                "moving_average": [round(x, 1) for x in moving_avg.tolist()]
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'analyse de saisonnalité: {e}")
            return None

# Instance globale du service
ai_prediction_service = AIPredictionService()

















