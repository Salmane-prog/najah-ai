import asyncio
import json
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime, timedelta
import logging
from database_service import db_service
from ai_prediction_service import ai_prediction_service

logger = logging.getLogger(__name__)

class AlertRule:
    def __init__(self, rule_id: str, name: str, description: str, metric: str, 
                 operator: str, threshold: float, severity: str, enabled: bool = True):
        self.rule_id = rule_id
        self.name = name
        self.description = description
        self.metric = metric
        self.operator = operator  # <, >, <=, >=, ==, !=
        self.threshold = threshold
        self.severity = severity  # low, medium, high, critical
        self.enabled = enabled
        self.triggered_count = 0
        self.last_triggered = None
        self.created_at = datetime.now()
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "description": self.description,
            "metric": self.metric,
            "operator": self.operator,
            "threshold": self.threshold,
            "severity": self.severity,
            "enabled": self.enabled,
            "triggered_count": self.triggered_count,
            "last_triggered": self.last_triggered.isoformat() if self.last_triggered else None,
            "created_at": self.created_at.isoformat()
        }

class Alert:
    def __init__(self, alert_id: str, rule: AlertRule, current_value: float, 
                 message: str, timestamp: datetime = None):
        self.alert_id = alert_id
        self.rule = rule
        self.current_value = current_value
        self.message = message
        self.timestamp = timestamp or datetime.now()
        self.status = "active"  # active, acknowledged, resolved
        self.acknowledged_by = None
        self.acknowledged_at = None
        self.resolved_by = None
        self.resolved_at = None
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "alert_id": self.alert_id,
            "rule": self.rule.to_dict(),
            "current_value": self.current_value,
            "message": self.message,
            "timestamp": self.timestamp.isoformat(),
            "status": self.status,
            "acknowledged_by": self.acknowledged_by,
            "acknowledged_at": self.acknowledged_at.isoformat() if self.acknowledged_at else None,
            "resolved_by": self.resolved_by,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None
        }

class IntelligentAlertsService:
    def __init__(self):
        self.alert_rules: Dict[str, AlertRule] = {}
        self.active_alerts: Dict[str, Alert] = {}
        self.alert_history: List[Alert] = []
        self.monitoring_task = None
        self.is_monitoring = False
        
        # Initialiser les règles d'alerte par défaut
        self._initialize_default_rules()
        
    def _initialize_default_rules(self):
        """Initialiser les règles d'alerte par défaut"""
        default_rules = [
            AlertRule(
                "score_drop", "Score moyen en baisse", 
                "Alerte si le score moyen global descend sous 60%",
                "overall_average_score", "<", 60, "high"
            ),
            AlertRule(
                "completion_low", "Taux de completion faible",
                "Alerte si moins de 70% des tests sont terminés",
                "completion_rate", "<", 70, "medium"
            ),
            AlertRule(
                "difficult_tests_high", "Tests difficiles en hausse",
                "Alerte si plus de 30% des tests sont considérés difficiles",
                "difficult_tests_percentage", ">", 30, "medium"
            ),
            AlertRule(
                "student_engagement_low", "Engagement des étudiants faible",
                "Alerte si l'engagement des étudiants descend sous 50%",
                "student_engagement", "<", 50, "high"
            ),
            AlertRule(
                "performance_decline", "Déclin de performance détecté",
                "Alerte si la performance moyenne baisse de plus de 10% en une semaine",
                "weekly_performance_change", "<", -10, "critical"
            )
        ]
        
        for rule in default_rules:
            self.add_alert_rule(rule)
    
    def add_alert_rule(self, rule: AlertRule) -> bool:
        """Ajouter une nouvelle règle d'alerte"""
        try:
            self.alert_rules[rule.rule_id] = rule
            logger.info(f"✅ Règle d'alerte ajoutée: {rule.name}")
            return True
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'ajout de la règle: {e}")
            return False
    
    def remove_alert_rule(self, rule_id: str) -> bool:
        """Supprimer une règle d'alerte"""
        try:
            if rule_id in self.alert_rules:
                del self.alert_rules[rule_id]
                logger.info(f"✅ Règle d'alerte supprimée: {rule_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Erreur lors de la suppression de la règle: {e}")
            return False
    
    def update_alert_rule(self, rule_id: str, updates: Dict[str, Any]) -> bool:
        """Mettre à jour une règle d'alerte"""
        try:
            if rule_id in self.alert_rules:
                rule = self.alert_rules[rule_id]
                for key, value in updates.items():
                    if hasattr(rule, key):
                        setattr(rule, key, value)
                logger.info(f"✅ Règle d'alerte mise à jour: {rule_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Erreur lors de la mise à jour de la règle: {e}")
            return False
    
    def get_current_metrics(self) -> Dict[str, float]:
        """Récupérer les métriques actuelles pour l'évaluation des alertes"""
        try:
            # Récupérer les performances des étudiants
            students = db_service.get_real_student_performances()
            tests = db_service.get_real_test_performances()
            
            if not students or not tests:
                return {}
            
            # Calculer le score moyen global
            overall_scores = [s['averageScore'] for s in students if s['averageScore'] is not None]
            overall_average = sum(overall_scores) / len(overall_scores) if overall_scores else 0
            
            # Calculer le taux de completion
            completion_rates = [t['completionRate'] for t in tests if t['completionRate'] is not None]
            avg_completion = sum(completion_rates) / len(completion_rates) if completion_rates else 0
            
            # Calculer le pourcentage de tests difficiles
            difficult_tests = [t for t in tests if t.get('difficultyLevel', 0) >= 7]
            difficult_percentage = (len(difficult_tests) / len(tests)) * 100 if tests else 0
            
            # Calculer l'engagement des étudiants (basé sur l'activité récente)
            recent_students = [s for s in students if s.get('lastTestDate')]
            engagement_percentage = (len(recent_students) / len(students)) * 100 if students else 0
            
            return {
                "overall_average_score": overall_average,
                "completion_rate": avg_completion,
                "difficult_tests_percentage": difficult_percentage,
                "student_engagement": engagement_percentage,
                "total_students": len(students),
                "total_tests": len(tests)
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la récupération des métriques: {e}")
            return {}
    
    def evaluate_alert_rules(self) -> List[Alert]:
        """Évaluer toutes les règles d'alerte et déclencher les alertes nécessaires"""
        triggered_alerts = []
        current_metrics = self.get_current_metrics()
        
        if not current_metrics:
            return triggered_alerts
        
        for rule in self.alert_rules.values():
            if not rule.enabled:
                continue
                
            try:
                # Vérifier si la règle doit être déclenchée
                if self._should_trigger_alert(rule, current_metrics):
                    # Créer une nouvelle alerte
                    alert = self._create_alert(rule, current_metrics)
                    if alert:
                        triggered_alerts.append(alert)
                        self._trigger_alert(alert)
                        
            except Exception as e:
                logger.error(f"❌ Erreur lors de l'évaluation de la règle {rule.rule_id}: {e}")
        
        return triggered_alerts
    
    def _should_trigger_alert(self, rule: AlertRule, metrics: Dict[str, float]) -> bool:
        """Vérifier si une règle d'alerte doit être déclenchée"""
        if rule.metric not in metrics:
            return False
        
        current_value = metrics[rule.metric]
        threshold = rule.threshold
        
        # Évaluer la condition selon l'opérateur
        if rule.operator == "<":
            return current_value < threshold
        elif rule.operator == ">":
            return current_value > threshold
        elif rule.operator == "<=":
            return current_value <= threshold
        elif rule.operator == ">=":
            return current_value >= threshold
        elif rule.operator == "==":
            return current_value == threshold
        elif rule.operator == "!=":
            return current_value != threshold
        
        return False
    
    def _create_alert(self, rule: AlertRule, metrics: Dict[str, float]) -> Optional[Alert]:
        """Créer une nouvelle alerte"""
        try:
            import uuid
            alert_id = str(uuid.uuid4())
            
            current_value = metrics.get(rule.metric, 0)
            
            # Générer le message de l'alerte
            message = self._generate_alert_message(rule, current_value)
            
            # Créer l'alerte
            alert = Alert(alert_id, rule, current_value, message)
            
            # Mettre à jour la règle
            rule.triggered_count += 1
            rule.last_triggered = datetime.now()
            
            return alert
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la création de l'alerte: {e}")
            return None
    
    def _generate_alert_message(self, rule: AlertRule, current_value: float) -> str:
        """Générer un message d'alerte personnalisé"""
        if rule.metric == "overall_average_score":
            return f"Le score moyen global est descendu à {current_value:.1f}% (seuil: {rule.threshold}%)"
        elif rule.metric == "completion_rate":
            return f"Le taux de completion est descendu à {current_value:.1f}% (seuil: {rule.threshold}%)"
        elif rule.metric == "difficult_tests_percentage":
            return f"{current_value:.1f}% des tests sont maintenant considérés difficiles (seuil: {rule.threshold}%)"
        elif rule.metric == "student_engagement":
            return f"L'engagement des étudiants est descendu à {current_value:.1f}% (seuil: {rule.threshold}%)"
        else:
            return f"La métrique {rule.metric} a atteint {current_value:.1f} (seuil: {rule.threshold})"
    
    def _trigger_alert(self, alert: Alert):
        """Déclencher une alerte"""
        try:
            # Ajouter à la liste des alertes actives
            self.active_alerts[alert.alert_id] = alert
            
            # Ajouter à l'historique
            self.alert_history.append(alert)
            
            # Limiter l'historique à 1000 alertes
            if len(self.alert_history) > 1000:
                self.alert_history = self.alert_history[-1000:]
            
            logger.warning(f"🚨 ALERTE DÉCLENCHÉE: {alert.rule.name} - {alert.message}")
            
            # Ici vous pourriez ajouter des notifications (email, SMS, webhook, etc.)
            self._send_notifications(alert)
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du déclenchement de l'alerte: {e}")
    
    def _send_notifications(self, alert: Alert):
        """Envoyer des notifications pour une alerte"""
        try:
            # Log de la notification (à remplacer par de vraies notifications)
            notification_data = {
                "type": "alert",
                "severity": alert.rule.severity,
                "title": alert.rule.name,
                "message": alert.message,
                "timestamp": alert.timestamp.isoformat(),
                "current_value": alert.current_value,
                "threshold": alert.rule.threshold
            }
            
            logger.info(f"📢 Notification envoyée: {json.dumps(notification_data, indent=2)}")
            
            # TODO: Implémenter de vraies notifications
            # - Email aux professeurs
            # - Webhook vers Slack/Discord
            # - SMS pour les alertes critiques
            # - Push notifications
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'envoi des notifications: {e}")
    
    def acknowledge_alert(self, alert_id: str, user_id: int) -> bool:
        """Reconnaître une alerte"""
        try:
            if alert_id in self.active_alerts:
                alert = self.active_alerts[alert_id]
                alert.status = "acknowledged"
                alert.acknowledged_by = user_id
                alert.acknowledged_at = datetime.now()
                logger.info(f"✅ Alerte reconnue: {alert_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Erreur lors de la reconnaissance de l'alerte: {e}")
            return False
    
    def resolve_alert(self, alert_id: str, user_id: int) -> bool:
        """Résoudre une alerte"""
        try:
            if alert_id in self.active_alerts:
                alert = self.active_alerts[alert_id]
                alert.status = "resolved"
                alert.resolved_by = user_id
                alert.resolved_at = datetime.now()
                
                # Retirer de la liste des alertes actives
                del self.active_alerts[alert_id]
                
                logger.info(f"✅ Alerte résolue: {alert_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Erreur lors de la résolution de l'alerte: {e}")
            return False
    
    def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Récupérer toutes les alertes actives"""
        return [alert.to_dict() for alert in self.active_alerts.values()]
    
    def get_alert_rules(self) -> List[Dict[str, Any]]:
        """Récupérer toutes les règles d'alerte"""
        return [rule.to_dict() for rule in self.alert_rules.values()]
    
    def get_alert_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Récupérer l'historique des alertes"""
        recent_alerts = self.alert_history[-limit:] if self.alert_history else []
        return [alert.to_dict() for alert in recent_alerts]
    
    async def start_monitoring(self, interval_seconds: int = 60):
        """Démarrer la surveillance continue des alertes"""
        if self.is_monitoring:
            logger.warning("⚠️ La surveillance est déjà en cours")
            return
        
        self.is_monitoring = True
        logger.info(f"🚀 Démarrage de la surveillance des alertes (intervalle: {interval_seconds}s)")
        
        while self.is_monitoring:
            try:
                # Évaluer les règles d'alerte
                triggered_alerts = self.evaluate_alert_rules()
                
                if triggered_alerts:
                    logger.info(f"🚨 {len(triggered_alerts)} nouvelles alertes déclenchées")
                
                # Attendre l'intervalle suivant
                await asyncio.sleep(interval_seconds)
                
            except Exception as e:
                logger.error(f"❌ Erreur lors de la surveillance: {e}")
                await asyncio.sleep(interval_seconds)
    
    def stop_monitoring(self):
        """Arrêter la surveillance des alertes"""
        self.is_monitoring = False
        logger.info("🛑 Surveillance des alertes arrêtée")

# Instance globale du service
intelligent_alerts_service = IntelligentAlertsService()

















