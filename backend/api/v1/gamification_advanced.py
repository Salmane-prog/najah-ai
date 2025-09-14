from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.user import User, UserRole
from models.quiz import QuizResult
from models.badge import UserBadge, Badge
from api.v1.users import get_current_user, require_role
from typing import List, Dict, Any
import json
from datetime import datetime, timedelta

router = APIRouter()

class AdvancedGamification:
    def __init__(self, db: Session):
        self.db = db
    
    def calculate_points(self, user_id: int, action_type: str, action_data: Dict[str, Any] = None) -> int:
        """Calculer les points basés sur l'action."""
        base_points = {
            "quiz_completed": 10,
            "quiz_perfect": 50,
            "quiz_improvement": 25,
            "streak_day": 5,
            "badge_earned": 100,
            "help_others": 15,
            "content_created": 75,
            "challenge_completed": 200,
            "class_participation": 20
        }
        
        points = base_points.get(action_type, 0)
        
        # Bonus basés sur les données
        if action_type == "quiz_completed" and action_data:
            score = action_data.get("score", 0)
            if score >= 90:
                points += 30  # Bonus pour excellente performance
            elif score >= 80:
                points += 20
            elif score >= 70:
                points += 10
        
        elif action_type == "quiz_improvement" and action_data:
            improvement = action_data.get("improvement", 0)
            points += min(improvement * 2, 50)  # Bonus pour amélioration
        
        elif action_type == "streak_day" and action_data:
            streak_length = action_data.get("streak_length", 1)
            if streak_length >= 7:
                points += 20  # Bonus pour longue série
            elif streak_length >= 3:
                points += 10
        
        return points
    
    def update_user_level(self, user_id: int) -> Dict[str, Any]:
        """Mettre à jour le niveau de l'utilisateur."""
        # Récupérer les points actuels
        user_points = self.db.query(User).filter(User.id == user_id).first()
        if not user_points:
            return {"level": 1, "experience": 0, "next_level_exp": 100}
        
        # Calculer le niveau basé sur l'expérience
        experience = getattr(user_points, 'experience', 0) or 0
        level = 1
        exp_needed = 100
        
        while experience >= exp_needed:
            experience -= exp_needed
            level += 1
            exp_needed = int(exp_needed * 1.5)  # Augmentation exponentielle
        
        # Ne pas essayer de modifier l'objet user directement
        # Les attributs level et experience n'existent peut-être pas
        
        return {
            "level": level,
            "experience": experience,
            "next_level_exp": exp_needed,
            "progress_percentage": (experience / exp_needed * 100) if exp_needed > 0 else 100
        }
    
    def create_challenge(self, challenge_data: Dict[str, Any], teacher_id: int) -> Dict[str, Any]:
        """Créer un nouveau défi."""
        challenge = {
            "title": challenge_data.get("title", "Défi"),
            "description": challenge_data.get("description", ""),
            "challenge_type": challenge_data.get("type", "quiz"),
            "difficulty": challenge_data.get("difficulty", "medium"),
            "points_reward": challenge_data.get("points_reward", 100),
            "requirements": challenge_data.get("requirements", {}),
            "start_date": challenge_data.get("start_date"),
            "end_date": challenge_data.get("end_date"),
            "created_by": teacher_id,
            "is_active": True
        }
        
        # Insérer dans la base de données
        cursor = self.db.execute("""
            INSERT INTO challenges (title, description, challenge_type, difficulty, 
                                 points_reward, requirements, start_date, end_date, 
                                 created_by, is_active, created_at)
            VALUES (:title, :description, :challenge_type, :difficulty, 
                   :points_reward, :requirements, :start_date, :end_date, 
                   :created_by, :is_active, :created_at)
        """, {
            **challenge,
            "requirements": json.dumps(challenge["requirements"]),
            "created_at": datetime.utcnow()
        })
        
        challenge_id = cursor.lastrowid
        
        return {
            "id": challenge_id,
            **challenge,
            "created_at": datetime.utcnow().isoformat()
        }
    
    def get_user_challenges(self, user_id: int) -> List[Dict[str, Any]]:
        """Récupérer les défis d'un utilisateur."""
        # Pour l'instant, retourner une liste vide car les tables challenges n'existent peut-être pas
        # TODO: Implémenter quand les tables seront créées
        return []
    
    def update_challenge_progress(self, user_id: int, challenge_id: int, progress: float) -> Dict[str, Any]:
        """Mettre à jour le progrès d'un défi."""
        # Vérifier si le défi existe
        challenge = self.db.execute("""
            SELECT * FROM challenges WHERE id = :challenge_id AND is_active = 1
        """, {"challenge_id": challenge_id}).fetchone()
        
        if not challenge:
            raise HTTPException(status_code=404, detail="Défi non trouvé")
        
        # Mettre à jour le progrès
        self.db.execute("""
            UPDATE user_challenges 
            SET progress = :progress, updated_at = :updated_at
            WHERE user_id = :user_id AND challenge_id = :challenge_id
        """, {
            "progress": progress,
            "updated_at": datetime.utcnow(),
            "user_id": user_id,
            "challenge_id": challenge_id
        })
        
        # Vérifier si le défi est complété
        if progress >= 100:
            self.db.execute("""
                UPDATE user_challenges 
                SET status = 'completed', completed_at = :completed_at, points_earned = :points_earned
                WHERE user_id = :user_id AND challenge_id = :challenge_id
            """, {
                "completed_at": datetime.utcnow(),
                "points_earned": challenge.points_reward,
                "user_id": user_id,
                "challenge_id": challenge_id
            })
            
            # Ajouter les points à l'utilisateur
            user = self.db.query(User).filter(User.id == user_id).first()
            if user:
                current_exp = getattr(user, 'experience', 0) or 0
                user.experience = current_exp + challenge.points_reward
                self.db.commit()
        
        self.db.commit()
        
        return {
            "challenge_id": challenge_id,
            "progress": progress,
            "completed": progress >= 100,
            "points_earned": challenge.points_reward if progress >= 100 else 0
        }
    
    def get_leaderboard(self, leaderboard_type: str = "global", class_id: int = None) -> List[Dict[str, Any]]:
        """Obtenir le classement."""
        if leaderboard_type == "class" and class_id:
            # Classement de classe
            students = self.db.query(ClassStudent).filter(ClassStudent.class_id == class_id).all()
            user_ids = [s.student_id for s in students]
            
            if not user_ids:
                return []
            
            # Récupérer les données des étudiants
            leaderboard_data = []
            for user_id in user_ids:
                user = self.db.query(User).filter(User.id == user_id).first()
                if not user:
                    continue
                
                # Calculer le score total
                results = self.db.query(QuizResult).filter(QuizResult.student_id == user_id).all()
                total_score = sum(r.score for r in results if r.score) if results else 0
                avg_score = total_score / len(results) if results else 0
                
                # Compter les badges
                badges = self.db.query(UserBadge).filter(UserBadge.user_id == user_id).count()
                
                # Score total (points + badges + performance)
                total_points = (getattr(user, 'experience', 0) or 0) + (badges * 50) + (avg_score * 10)
                
                leaderboard_data.append({
                    "user_id": user.id,
                    "username": user.username,
                    "total_points": total_points,
                    "level": getattr(user, 'level', 1) or 1,
                    "badges_count": badges,
                    "average_score": round(avg_score, 1),
                    "quiz_count": len(results)
                })
        else:
            # Classement global
            users = self.db.query(User).filter(User.role == "student").all()
            leaderboard_data = []
            
            for user in users:
                # Calculer le score total
                results = self.db.query(QuizResult).filter(QuizResult.student_id == user.id).all()
                total_score = sum(r.score for r in results if r.score) if results else 0
                avg_score = total_score / len(results) if results else 0
                
                # Compter les badges
                badges = self.db.query(UserBadge).filter(UserBadge.user_id == user.id).count()
                
                # Score total
                total_points = (getattr(user, 'experience', 0) or 0) + (badges * 50) + (avg_score * 10)
                
                leaderboard_data.append({
                    "user_id": user.id,
                    "username": user.username,
                    "total_points": total_points,
                    "level": getattr(user, 'level', 1) or 1,
                    "badges_count": badges,
                    "average_score": round(avg_score, 1),
                    "quiz_count": len(results)
                })
        
        # Trier par score total
        leaderboard_data.sort(key=lambda x: x["total_points"], reverse=True)
        
        # Ajouter le rang
        for i, entry in enumerate(leaderboard_data):
            entry["rank"] = i + 1
        
        return leaderboard_data[:20]  # Top 20

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/challenges/create")
def create_challenge(
    challenge_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher']))
):
    """Créer un nouveau défi."""
    try:
        gamification = AdvancedGamification(db)
        challenge = gamification.create_challenge(challenge_data, current_user.id)
        return challenge
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de création de défi: {str(e)}")

@router.get("/challenges/user")
def get_user_challenges(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Récupérer les défis d'un utilisateur."""
    try:
        gamification = AdvancedGamification(db)
        challenges = gamification.get_user_challenges(current_user.id)
        return {"challenges": challenges}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de récupération des défis: {str(e)}")

@router.post("/challenges/{challenge_id}/progress")
def update_challenge_progress(
    challenge_id: int,
    progress_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Mettre à jour le progrès d'un défi."""
    try:
        gamification = AdvancedGamification(db)
        progress = progress_data.get("progress", 0)
        result = gamification.update_challenge_progress(current_user.id, challenge_id, progress)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de mise à jour du progrès: {str(e)}")

@router.get("/leaderboard")
def get_leaderboard(
    leaderboard_type: str = "global",
    class_id: int = None,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Obtenir le classement."""
    try:
        gamification = AdvancedGamification(db)
        leaderboard = gamification.get_leaderboard(leaderboard_type, class_id)
        return {
            "leaderboard_type": leaderboard_type,
            "class_id": class_id,
            "entries": leaderboard
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de classement: {str(e)}")

@router.get("/user/stats")
def get_user_gamification_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student', 'teacher', 'admin']))
):
    """Obtenir les statistiques de gamification d'un utilisateur."""
    try:
        gamification = AdvancedGamification(db)
        
        # Mettre à jour le niveau
        level_info = gamification.update_user_level(current_user.id)
        
        # Récupérer les défis
        challenges = gamification.get_user_challenges(current_user.id)
        
        # Récupérer les badges
        badges = db.query(UserBadge).filter(UserBadge.user_id == current_user.id).all()
        
        # Récupérer les informations des badges
        badge_info = []
        for user_badge in badges:
            badge = db.query(Badge).filter(Badge.id == user_badge.badge_id).first()
            if badge:
                badge_info.append({"id": badge.id, "name": badge.name})
            else:
                badge_info.append({"id": user_badge.badge_id, "name": "Badge inconnu"})
        
        # Calculer les statistiques
        total_quizzes = db.query(QuizResult).filter(QuizResult.student_id == current_user.id).count()
        completed_quizzes = db.query(QuizResult).filter(
            QuizResult.student_id == current_user.id,
            QuizResult.is_completed == True
        ).count()
        
        # Calculer le streak
        # Pour l'instant, retourner 0 car LearningHistory n'a peut-être pas les bons attributs
        streak_days = 0
        
        return {
            "user_id": current_user.id,
            "username": current_user.username,
            "level": level_info["level"],
            "experience": level_info["experience"],
            "next_level_exp": level_info["next_level_exp"],
            "progress_percentage": level_info["progress_percentage"],
            "total_points": getattr(current_user, 'experience', 0) or 0,
            "badges_count": len(badges),
            "challenges_active": len([c for c in challenges if c["status"] == "active"]),
            "challenges_completed": len([c for c in challenges if c["status"] == "completed"]),
            "total_quizzes": total_quizzes,
            "completed_quizzes": completed_quizzes,
            "completion_rate": (completed_quizzes / total_quizzes * 100) if total_quizzes > 0 else 0,
            "streak_days": streak_days,
            "badges": badge_info,
            "challenges": challenges
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de statistiques: {str(e)}")

@router.post("/points/award")
def award_points(
    points_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Attribuer des points à un utilisateur."""
    try:
        gamification = AdvancedGamification(db)
        
        action_type = points_data.get("action_type")
        action_data = points_data.get("action_data", {})
        
        points = gamification.calculate_points(current_user.id, action_type, action_data)
        
        # Ajouter les points à l'utilisateur
        user = db.query(User).filter(User.id == current_user.id).first()
        if user:
            current_exp = getattr(user, 'experience', 0) or 0
            user.experience = current_exp + points
            db.commit()
        
        return {"points_awarded": points, "total_points": getattr(user, 'experience', 0) or 0}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'attribution de points: {str(e)}") 