from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from core.database import get_db
from models.user import User
from api.v1.auth import require_role
from models.quiz import QuizResult
from models.badge import UserBadge, Badge
from models.learning_history import LearningHistory
from models.class_group import ClassGroup, ClassStudent
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any

router = APIRouter()

class AdvancedNotificationSystem:
    def __init__(self, db: Session):
        self.db = db
    
    def check_achievements(self, user_id: int) -> List[Dict[str, Any]]:
        """Vérifier et créer les notifications d'accomplissements."""
        notifications = []
        
        # Vérifier les accomplissements de quiz
        quiz_achievements = self._check_quiz_achievements(user_id)
        notifications.extend(quiz_achievements)
        
        # Vérifier les accomplissements de badges
        badge_achievements = self._check_badge_achievements(user_id)
        notifications.extend(badge_achievements)
        
        # Vérifier les accomplissements de défis
        challenge_achievements = self._check_challenge_achievements(user_id)
        notifications.extend(challenge_achievements)
        
        # Vérifier les accomplissements de progression
        progress_achievements = self._check_progress_achievements(user_id)
        notifications.extend(progress_achievements)
        
        return notifications
    
    def _check_quiz_achievements(self, user_id: int) -> List[Dict[str, Any]]:
        """Vérifier les accomplissements liés aux quiz."""
        notifications = []
        
        # Compter les quiz complétés
        quiz_count = self.db.query(QuizResult).filter(
            QuizResult.student_id == user_id,
            QuizResult.is_completed == True
        ).count()
        
        # Accomplissements basés sur le nombre de quiz
        achievements = [
            {"name": "Premier Quiz", "description": "Complétez votre premier quiz", "count": 1},
            {"name": "Quiz Régulier", "description": "Complétez 10 quiz", "count": 10},
            {"name": "Quiz Master", "description": "Complétez 50 quiz", "count": 50},
            {"name": "Quiz Expert", "description": "Complétez 100 quiz", "count": 100}
        ]
        
        for achievement in achievements:
            if quiz_count >= achievement["count"]:
                # Vérifier si l'accomplissement n'a pas déjà été notifié
                existing_notification = self.db.execute(text("""
                    SELECT id FROM notifications 
                    WHERE user_id = :user_id AND type = 'achievement' AND title = :title
                """), {"user_id": user_id, "title": achievement["name"]}).fetchone()
                
                if not existing_notification:
                    notifications.append({
                        "type": "achievement",
                        "title": achievement["name"],
                        "message": achievement["description"],
                        "icon": "🎯",
                        "points_reward": achievement["count"] * 10
                    })
        
        # Accomplissements basés sur les scores parfaits
        perfect_scores = self.db.query(QuizResult).filter(
            QuizResult.student_id == user_id,
            QuizResult.score == 100
        ).count()
        
        if perfect_scores >= 5:
            existing_notification = self.db.execute(text("""
                SELECT id FROM notifications 
                WHERE user_id = :user_id AND type = 'achievement' AND title = 'Perfectionniste'
            """), {"user_id": user_id}).fetchone()
            
            if not existing_notification:
                notifications.append({
                    "type": "achievement",
                    "title": "Perfectionniste",
                    "message": f"Obtenez {perfect_scores} scores parfaits",
                    "icon": "⭐",
                    "points_reward": perfect_scores * 20
                })
        
        return notifications
    
    def _check_badge_achievements(self, user_id: int) -> List[Dict[str, Any]]:
        """Vérifier les accomplissements liés aux badges."""
        notifications = []
        
        # Compter les badges
        badge_count = self.db.query(UserBadge).filter(UserBadge.user_id == user_id).count()
        
        # Accomplissements basés sur le nombre de badges
        achievements = [
            {"name": "Premier Badge", "description": "Obtenez votre premier badge", "count": 1},
            {"name": "Collectionneur", "description": "Obtenez 5 badges", "count": 5},
            {"name": "Expert Badges", "description": "Obtenez 10 badges", "count": 10},
            {"name": "Maître Badges", "description": "Obtenez 20 badges", "count": 20}
        ]
        
        for achievement in achievements:
            if badge_count >= achievement["count"]:
                existing_notification = self.db.execute(text("""
                    SELECT id FROM notifications 
                    WHERE user_id = :user_id AND type = 'achievement' AND title = :title
                """), {"user_id": user_id, "title": achievement["name"]}).fetchone()
                
                if not existing_notification:
                    notifications.append({
                        "type": "achievement",
                        "title": achievement["name"],
                        "message": achievement["description"],
                        "icon": "🏅",
                        "points_reward": achievement["count"] * 15
                    })
        
        return notifications
    
    def _check_challenge_achievements(self, user_id: int) -> List[Dict[str, Any]]:
        """Vérifier les accomplissements liés aux défis."""
        notifications = []
        
        # Compter les défis complétés
        completed_challenges = self.db.execute(text("""
            SELECT COUNT(*) FROM user_challenges 
            WHERE user_id = :user_id AND is_completed = 1
        """), {"user_id": user_id}).fetchone()[0]
        
        # Accomplissements basés sur les défis
        achievements = [
            {"name": "Premier Défi", "description": "Complétez votre premier défi", "count": 1},
            {"name": "Défieur Régulier", "description": "Complétez 5 défis", "count": 5},
            {"name": "Maître des Défis", "description": "Complétez 10 défis", "count": 10}
        ]
        
        for achievement in achievements:
            if completed_challenges >= achievement["count"]:
                existing_notification = self.db.execute(text("""
                    SELECT id FROM notifications 
                    WHERE user_id = :user_id AND type = 'achievement' AND title = :title
                """), {"user_id": user_id, "title": achievement["name"]}).fetchone()
                
                if not existing_notification:
                    notifications.append({
                        "type": "achievement",
                        "title": achievement["name"],
                        "message": achievement["description"],
                        "icon": "🏆",
                        "points_reward": achievement["count"] * 25
                    })
        
        return notifications
    
    def _check_progress_achievements(self, user_id: int) -> List[Dict[str, Any]]:
        """Vérifier les accomplissements liés à la progression."""
        notifications = []
        
        # Calculer la progression récente
        recent_results = self.db.query(QuizResult).filter(
            QuizResult.student_id == user_id,
            QuizResult.completed_at >= datetime.utcnow() - timedelta(days=30)
        ).all()
        
        if recent_results:
            recent_avg = sum(r.score for r in recent_results if r.score) / len(recent_results)
            
            # Accomplissements basés sur l'amélioration
            if recent_avg >= 90:
                existing_notification = self.db.execute(text("""
                    SELECT id FROM notifications 
                    WHERE user_id = :user_id AND type = 'achievement' AND title = 'Excellence'
                """), {"user_id": user_id}).fetchone()
                
                if not existing_notification:
                    notifications.append({
                        "type": "achievement",
                        "title": "Excellence",
                        "message": f"Maintenez une moyenne de {recent_avg:.1f}%",
                        "icon": "🌟",
                        "points_reward": 100
                    })
        
        return notifications
    
    def create_notification(self, user_id: int, notification_data: Dict[str, Any]) -> Dict[str, Any]:
        """Créer une notification dans la base de données."""
        try:
            cursor = self.db.execute(text("""
                INSERT INTO notifications (user_id, type, title, message, icon, 
                                       points_reward, is_read, created_at)
                VALUES (:user_id, :type, :title, :message, :icon, :points_reward, :is_read, :created_at)
            """), {
                "user_id": user_id,
                "type": notification_data["type"],
                "title": notification_data["title"],
                "message": notification_data["message"],
                "icon": notification_data.get("icon", "🎉"),
                "points_reward": notification_data.get("points_reward", 0),
                "is_read": 0,  # is_read = False
                "created_at": datetime.utcnow()
            })
            
            notification_id = cursor.lastrowid
            
            return {
                "id": notification_id,
                **notification_data,
                "created_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            print(f"Erreur lors de la création de notification: {str(e)}")
            return None

@router.post("/check-achievements")
def check_user_achievements(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student', 'teacher', 'admin']))
):
    """Vérifier et créer les notifications d'accomplissements pour un utilisateur."""
    try:
        notification_system = AdvancedNotificationSystem(db)
        achievements = notification_system.check_achievements(current_user.id)
        
        created_notifications = []
        for achievement in achievements:
            notification = notification_system.create_notification(current_user.id, achievement)
            if notification:
                created_notifications.append(notification)
        
        return {
            "user_id": current_user.id,
            "achievements_found": len(achievements),
            "notifications_created": len(created_notifications),
            "notifications": created_notifications
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de vérification: {str(e)}")

@router.get("/achievements/{user_id}")
def get_user_achievements(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Obtenir les accomplissements d'un utilisateur."""
    try:
        notification_system = AdvancedNotificationSystem(db)
        achievements = notification_system.check_achievements(user_id)
        
        return {
            "user_id": user_id,
            "achievements": achievements
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de récupération: {str(e)}")

@router.post("/trigger-achievement-check")
def trigger_achievement_check(
    action_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Déclencher une vérification d'accomplissement après une action."""
    try:
        notification_system = AdvancedNotificationSystem(db)
        
        # Vérifier les accomplissements
        achievements = notification_system.check_achievements(current_user.id)
        
        # Créer les notifications
        created_notifications = []
        for achievement in achievements:
            notification = notification_system.create_notification(current_user.id, achievement)
            if notification:
                created_notifications.append(notification)
        
        # Attribuer des points si nécessaire
        total_points = sum(notif.get("points_reward", 0) for notif in created_notifications)
        
        if total_points > 0:
            # Mettre à jour les points de l'utilisateur
            user = db.query(User).filter(User.id == current_user.id).first()
            if user:
                current_exp = getattr(user, 'experience', 0) or 0
                user.experience = current_exp + total_points
                db.commit()
        
        return {
            "user_id": current_user.id,
            "action": action_data.get("action_type", "unknown"),
            "achievements_found": len(achievements),
            "notifications_created": len(created_notifications),
            "points_awarded": total_points,
            "notifications": created_notifications
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de déclenchement: {str(e)}") 

@router.get("/user-notifications/{user_id}")
def get_user_notifications(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["student", "teacher", "admin"]))
):
    """Obtenir les notifications d'un utilisateur."""
    try:
        # Simuler des notifications pour l'utilisateur
        notifications = [
            {
                "id": 1,
                "type": "achievement",
                "title": "🎉 Nouveau badge débloqué !",
                "message": "Félicitations ! Vous avez obtenu le badge 'Mathématicien'",
                "icon": "🏆",
                "points_reward": 50,
                "is_read": False,
                "created_at": "2024-01-15T10:00:00"
            },
            {
                "id": 2,
                "type": "challenge",
                "title": "💪 Nouveau défi disponible",
                "message": "Un nouveau défi 'Quiz de la semaine' est disponible",
                "icon": "🎯",
                "points_reward": 100,
                "is_read": True,
                "created_at": "2024-01-14T15:30:00"
            },
            {
                "id": 3,
                "type": "badge",
                "title": "⭐ Badge 'Persévérant'",
                "message": "Vous avez complété 10 quiz consécutifs !",
                "icon": "⭐",
                "points_reward": 75,
                "is_read": False,
                "created_at": "2024-01-13T09:15:00"
            }
        ]
        
        return {"notifications": notifications}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des notifications: {str(e)}")

@router.put("/mark-read/{notification_id}")
def mark_notification_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["student", "teacher", "admin"]))
):
    """Marquer une notification comme lue."""
    try:
        # Simuler la mise à jour
        return {"message": f"Notification {notification_id} marquée comme lue"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du marquage: {str(e)}") 