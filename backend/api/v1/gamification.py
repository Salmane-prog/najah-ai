from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from core.database import get_db
from models.gamification import UserLevel, Challenge, UserChallenge, Leaderboard, LeaderboardEntry, Achievement, UserAchievement
from models.user import User
from models.quiz import Quiz, QuizResult
from models.class_group import ClassStudent
from api.v1.users import get_current_user
from api.v1.auth import require_role
from typing import List, Dict, Any
from datetime import datetime, timedelta
import json
from models.learning_history import LearningHistory
from models.user import UserRole
from models.badge import UserBadge, Badge
import random

router = APIRouter()

# Endpoints de test sans authentification pour diagnostiquer
@router.get("/test/user/{user_id}/points")
def get_user_points_test(user_id: int, db: Session = Depends(get_db)):
    """Récupérer les points d'un utilisateur (test sans auth)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    # Calculer les points basés sur les quiz complétés
    quiz_results = db.query(QuizResult).filter(
        QuizResult.student_id == user_id,
        QuizResult.is_completed == True
    ).all()
    
    total_points = sum(result.score for result in quiz_results)
    
    return {
        "user_id": user_id,
        "total_points": total_points,
        "quiz_count": len(quiz_results)
    }

@router.get("/test/user/{user_id}/level")
def get_user_level_test(user_id: int, db: Session = Depends(get_db)):
    """Récupérer le niveau d'un utilisateur (test sans auth)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    # Calculer le niveau basé sur les points
    quiz_results = db.query(QuizResult).filter(
        QuizResult.student_id == user_id,
        QuizResult.is_completed == True
    ).all()
    
    total_points = sum(result.score for result in quiz_results)
    level = (total_points // 100) + 1  # 100 points par niveau
    
    return {
        "user_id": user_id,
        "level": level,
        "total_points": total_points,
        "points_to_next_level": 100 - (total_points % 100)
    }

@router.get("/test/user/{user_id}/achievements")
def get_user_achievements_test(user_id: int, db: Session = Depends(get_db)):
    """Récupérer les achievements d'un utilisateur (test sans auth)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    # Calculer les achievements basés sur les performances
    quiz_results = db.query(QuizResult).filter(
        QuizResult.student_id == user_id,
        QuizResult.is_completed == True
    ).all()
    
    achievements = []
    
    if len(quiz_results) >= 5:
        achievements.append({
            "id": 1,
            "name": "Quiz Master",
            "description": "A complété 5 quiz",
            "unlocked": True
        })
    
    if len(quiz_results) >= 10:
        achievements.append({
            "id": 2,
            "name": "Quiz Expert",
            "description": "A complété 10 quiz",
            "unlocked": True
        })
    
    avg_score = sum(result.score for result in quiz_results) / len(quiz_results) if quiz_results else 0
    if avg_score >= 80:
        achievements.append({
            "id": 3,
            "name": "High Scorer",
            "description": "Score moyen de 80% ou plus",
            "unlocked": True
        })
    
    return {
        "user_id": user_id,
        "achievements": achievements,
        "total_achievements": len(achievements)
    }

@router.get("/test/user/{user_id}/challenges")
def get_user_challenges_test(user_id: int, db: Session = Depends(get_db)):
    """Récupérer les challenges d'un utilisateur (test sans auth)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    # Générer des challenges basés sur les performances
    quiz_results = db.query(QuizResult).filter(
        QuizResult.student_id == user_id,
        QuizResult.is_completed == True
    ).all()
    
    challenges = [
        {
            "id": 1,
            "name": "Premier Quiz",
            "description": "Compléter votre premier quiz",
            "completed": len(quiz_results) >= 1,
            "progress": min(len(quiz_results), 1)
        },
        {
            "id": 2,
            "name": "Quiz Régulier",
            "description": "Compléter 5 quiz",
            "completed": len(quiz_results) >= 5,
            "progress": min(len(quiz_results), 5)
        },
        {
            "id": 3,
            "name": "Score Parfait",
            "description": "Obtenir 100% sur un quiz",
            "completed": any(result.score == 100 for result in quiz_results),
            "progress": 1 if any(result.score == 100 for result in quiz_results) else 0
        }
    ]
    
    return {
        "user_id": user_id,
        "challenges": challenges,
        "completed_challenges": sum(1 for c in challenges if c["completed"])
    }

@router.get("/test/leaderboard")
def get_leaderboard_test(db: Session = Depends(get_db)):
    """Récupérer le leaderboard des étudiants (test sans auth)"""
    # Calculer les points pour chaque étudiant
    students = db.query(User).filter(User.role == "student").all()
    
    leaderboard = []
    for student in students:
        quiz_results = db.query(QuizResult).filter(
            QuizResult.student_id == student.id,
            QuizResult.is_completed == True
        ).all()
        
        total_points = sum(result.score for result in quiz_results)
        
        leaderboard.append({
            "user_id": student.id,
            "username": student.username,
            "email": student.email,
            "total_points": total_points,
            "quiz_count": len(quiz_results)
        })
    
    # Trier par points décroissants
    leaderboard.sort(key=lambda x: x["total_points"], reverse=True)
    
    return {
        "leaderboard": leaderboard[:10],  # Top 10
        "total_students": len(students)
    }

@router.get("/test/user/stats")
def get_user_stats_test(db: Session = Depends(get_db)):
    """Récupérer les statistiques gamification d'un utilisateur (test sans auth)"""
    # Utiliser un utilisateur par défaut pour le test
    user = db.query(User).filter(User.role == "student").first()
    if not user:
        return {
            "user_id": 0,
            "total_points": 0,
            "level": 1,
            "quiz_count": 0,
            "average_score": 0,
            "points_to_next_level": 100
        }
    
    quiz_results = db.query(QuizResult).filter(
        QuizResult.student_id == user.id,
        QuizResult.is_completed == True
    ).all()
    
    total_points = sum(result.score for result in quiz_results)
    level = (total_points // 100) + 1
    avg_score = sum(result.score for result in quiz_results) / len(quiz_results) if quiz_results else 0
    
    return {
        "user_id": user.id,
        "total_points": total_points,
        "level": level,
        "quiz_count": len(quiz_results),
        "average_score": round(avg_score, 2),
        "points_to_next_level": 100 - (total_points % 100)
    }

@router.get("/user/{user_id}/level")
def get_user_level(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Récupérer le niveau et XP d'un utilisateur."""
    
    # Vérifier que l'utilisateur accède à ses propres données
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    user_level = db.query(UserLevel).filter(UserLevel.user_id == user_id).first()
    
    if not user_level:
        # Créer un niveau par défaut
        user_level = UserLevel(
            user_id=user_id,
            level=1,
            current_xp=0,
            total_xp=0,
            xp_to_next_level=1000
        )
        db.add(user_level)
        db.commit()
        db.refresh(user_level)
    
    return user_level

@router.post("/user/{user_id}/add-xp")
def add_user_xp(
    user_id: int,
    xp_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Ajouter de l'XP à un utilisateur."""
    
    # Vérifier que l'utilisateur accède à ses propres données
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    xp_amount = xp_data.get("xp", 0)
    reason = xp_data.get("reason", "Activité")
    
    user_level = db.query(UserLevel).filter(UserLevel.user_id == user_id).first()
    
    if not user_level:
        user_level = UserLevel(
            user_id=user_id,
            level=1,
            current_xp=0,
            total_xp=0,
            xp_to_next_level=1000
        )
        db.add(user_level)
        db.commit()
    
    # Ajouter l'XP
    user_level.current_xp += xp_amount
    user_level.total_xp += xp_amount
    
    # Vérifier si l'utilisateur monte de niveau
    level_ups = []
    while user_level.current_xp >= user_level.xp_to_next_level:
        user_level.level += 1
        user_level.current_xp -= user_level.xp_to_next_level
        user_level.xp_to_next_level = calculate_xp_for_level(user_level.level)
        level_ups.append(user_level.level)
    
    db.commit()
    db.refresh(user_level)
    
    return {
        "user_level": user_level,
        "xp_gained": xp_amount,
        "reason": reason,
        "level_ups": level_ups
    }

def calculate_xp_for_level(level: int) -> int:
    """Calculer l'XP nécessaire pour le niveau suivant."""
    return int(1000 * (1.2 ** (level - 1)))

@router.get("/user/{user_id}/points")
def get_user_points(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Récupérer les points totaux d'un utilisateur."""
    
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    # Calculer les points totaux depuis les achievements et challenges
    achievements_points = db.query(func.sum(Achievement.points)).join(
        UserAchievement, UserAchievement.achievement_id == Achievement.id
    ).filter(UserAchievement.user_id == user_id).scalar() or 0
    
    challenges_points = db.query(func.sum(Challenge.points)).join(
        UserChallenge, UserChallenge.challenge_id == Challenge.id
    ).filter(UserChallenge.user_id == user_id, UserChallenge.completed == True).scalar() or 0
    
    total_points = achievements_points + challenges_points
    
    return {
        "user_id": user_id,
        "total_points": total_points,
        "achievements_points": achievements_points,
        "challenges_points": challenges_points
    }

@router.get("/user/{user_id}/achievements")
def get_user_achievements(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Récupérer les achievements d'un utilisateur avec progression."""
    
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    # Récupérer tous les achievements
    all_achievements = db.query(Achievement).all()
    user_achievements = db.query(UserAchievement).filter(UserAchievement.user_id == user_id).all()
    
    # Créer un dictionnaire des achievements débloqués
    unlocked_achievements = {ua.achievement_id: ua for ua in user_achievements}
    
    achievements_with_progress = []
    
    for achievement in all_achievements:
        user_achievement = unlocked_achievements.get(achievement.id)
        
        # Calculer la progression basée sur le type d'achievement
        progress = calculate_achievement_progress(achievement, user_id, db)
        
        achievements_with_progress.append({
            "id": achievement.id,
            "name": achievement.name,
            "description": achievement.description,
            "points": achievement.points,
            "icon": achievement.icon,
            "category": achievement.category,
            "unlocked": user_achievement is not None,
            "unlocked_at": user_achievement.unlocked_at if user_achievement else None,
            "progress": progress,
            "completed": progress["current"] >= progress["target"]
        })
    
    return {
        "user_id": user_id,
        "achievements": achievements_with_progress,
        "total_achievements": len(all_achievements),
        "unlocked_count": len(unlocked_achievements)
    }

@router.get("/user/{user_id}/challenges")
def get_user_challenges(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Récupérer les challenges d'un utilisateur avec progression."""
    
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    # Récupérer tous les challenges
    all_challenges = db.query(Challenge).all()
    user_challenges = db.query(UserChallenge).filter(UserChallenge.user_id == user_id).all()
    
    # Créer un dictionnaire des challenges de l'utilisateur
    user_challenge_dict = {uc.challenge_id: uc for uc in user_challenges}
    
    challenges_with_progress = []
    
    for challenge in all_challenges:
        user_challenge = user_challenge_dict.get(challenge.id)
        
        # Calculer la progression basée sur le type de challenge
        progress = calculate_challenge_progress(challenge, user_id, db)
        
        challenges_with_progress.append({
            "id": challenge.id,
            "name": challenge.name,
            "description": challenge.description,
            "points": challenge.points,
            "icon": challenge.icon,
            "category": challenge.category,
            "completed": user_challenge.completed if user_challenge else False,
            "completed_at": user_challenge.completed_at if user_challenge else None,
            "progress": progress,
            "active": user_challenge.active if user_challenge else False
        })
    
    return {
        "user_id": user_id,
        "challenges": challenges_with_progress,
        "total_challenges": len(all_challenges),
        "completed_count": len([c for c in challenges_with_progress if c["completed"]])
    }

@router.post("/user/{user_id}/achievements/{achievement_id}/unlock")
def unlock_achievement(
    user_id: int,
    achievement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Débloquer un achievement pour un utilisateur."""
    
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    # Vérifier que l'achievement existe
    achievement = db.query(Achievement).filter(Achievement.id == achievement_id).first()
    if not achievement:
        raise HTTPException(status_code=404, detail="Achievement non trouvé")
    
    # Vérifier que l'achievement n'est pas déjà débloqué
    existing = db.query(UserAchievement).filter(
        UserAchievement.user_id == user_id,
        UserAchievement.achievement_id == achievement_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Achievement déjà débloqué")
    
    # Vérifier que l'utilisateur a rempli les critères
    progress = calculate_achievement_progress(achievement, user_id, db)
    if progress["current"] < progress["target"]:
        raise HTTPException(status_code=400, detail="Critères non remplis pour débloquer cet achievement")
    
    # Débloquer l'achievement
    user_achievement = UserAchievement(
        user_id=user_id,
        achievement_id=achievement_id,
        unlocked_at=datetime.utcnow()
    )
    db.add(user_achievement)
    db.commit()
    db.refresh(user_achievement)
    
    return {
        "message": f"Achievement '{achievement.name}' débloqué !",
        "points_earned": achievement.points,
        "achievement": achievement
    }

@router.post("/user/{user_id}/challenges/{challenge_id}/complete")
def complete_challenge(
    user_id: int,
    challenge_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Compléter un challenge pour un utilisateur."""
    
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    # Vérifier que le challenge existe
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge non trouvé")
    
    # Vérifier que le challenge n'est pas déjà complété
    existing = db.query(UserChallenge).filter(
        UserChallenge.user_id == user_id,
        UserChallenge.challenge_id == challenge_id
    ).first()
    
    if existing and existing.completed:
        raise HTTPException(status_code=400, detail="Challenge déjà complété")
    
    # Vérifier que l'utilisateur a rempli les critères
    progress = calculate_challenge_progress(challenge, user_id, db)
    if progress["current"] < progress["target"]:
        raise HTTPException(status_code=400, detail="Critères non remplis pour compléter ce challenge")
    
    # Compléter le challenge
    if existing:
        existing.completed = True
        existing.completed_at = datetime.utcnow()
    else:
        user_challenge = UserChallenge(
            user_id=user_id,
            challenge_id=challenge_id,
            completed=True,
            completed_at=datetime.utcnow(),
            active=True
        )
        db.add(user_challenge)
    
    db.commit()
    
    return {
        "message": f"Challenge '{challenge.name}' complété !",
        "points_earned": challenge.points,
        "challenge": challenge
    }

def calculate_achievement_progress(achievement: Achievement, user_id: int, db: Session) -> Dict[str, Any]:
    """Calculer la progression d'un achievement."""
    
    if achievement.name == "Quiz Master":
        # Compléter 10 quiz
        quiz_count = db.query(QuizResult).filter(QuizResult.student_id == user_id).count()
        return {"current": quiz_count, "target": 10}
    
    elif achievement.name == "Perfect Score":
        # Obtenir un score parfait sur un quiz
        perfect_quizzes = db.query(QuizResult).filter(
            QuizResult.student_id == user_id,
            QuizResult.score == QuizResult.max_score
        ).count()
        return {"current": perfect_quizzes, "target": 1}
    
    elif achievement.name == "Streak Master":
        # Compléter des quiz 5 jours de suite
        # Calculer la plus longue série de jours consécutifs
        results = db.query(QuizResult).filter(QuizResult.student_id == user_id).order_by(QuizResult.completed_at).all()
        
        if not results:
            return {"current": 0, "target": 5}
        
        # Grouper par jour
        from datetime import datetime, timedelta
        daily_activity = {}
        for result in results:
            day = result.completed_at.date()
            if day not in daily_activity:
                daily_activity[day] = 0
            daily_activity[day] += 1
        
        # Calculer la plus longue série
        dates = sorted(daily_activity.keys())
        max_streak = 0
        current_streak = 0
        
        for i, date in enumerate(dates):
            if i == 0:
                current_streak = 1
            else:
                prev_date = dates[i-1]
                if (date - prev_date).days == 1:
                    current_streak += 1
                else:
                    current_streak = 1
            
            max_streak = max(max_streak, current_streak)
        
        return {"current": max_streak, "target": 5}
    
    elif achievement.name == "Rapide comme l'éclair":
        # Complétez 5 quiz en moins de 30 minutes
        fast_quizzes = db.query(QuizResult).filter(
            QuizResult.student_id == user_id,
            QuizResult.time_taken <= 1800  # 30 minutes en secondes
        ).count()
        return {"current": fast_quizzes, "target": 5}
    
    elif achievement.name == "Maître du Sujet":
        # Obtenez une moyenne de 90%+ sur 10 quiz d'un même sujet
        # Calculer la moyenne par sujet
        results = db.query(QuizResult).filter(QuizResult.student_id == user_id).all()
        
        if not results:
            return {"current": 0, "target": 10}
        
        # Grouper par sujet
        subject_scores = {}
        for result in results:
            subject = result.quiz.subject if result.quiz else "Général"
            if subject not in subject_scores:
                subject_scores[subject] = []
            subject_scores[subject].append(result.score)
        
        # Trouver le sujet avec la meilleure moyenne
        best_subject_avg = 0
        for subject, scores in subject_scores.items():
            if len(scores) >= 10:
                avg = sum(scores) / len(scores)
                if avg >= 90:
                    best_subject_avg = avg
                    break
        
        return {"current": 1 if best_subject_avg >= 90 else 0, "target": 1}
    
    elif achievement.name == "Lève-tôt":
        # Complétez un quiz avant 8h du matin
        from datetime import datetime
        early_quizzes = db.query(QuizResult).filter(
            QuizResult.student_id == user_id,
            func.extract('hour', QuizResult.completed_at) < 8
        ).count()
        return {"current": early_quizzes, "target": 1}
    
    return {"current": 0, "target": 1}

def calculate_challenge_progress(challenge: Challenge, user_id: int, db: Session) -> Dict[str, Any]:
    """Calculer la progression d'un challenge."""
    
    if challenge.name == "Quiz Master":
        # Compléter 10 quiz
        quiz_count = db.query(QuizResult).filter(QuizResult.student_id == user_id).count()
        return {"current": quiz_count, "target": 10}
    
    elif challenge.name == "Streak Master":
        # Compléter des quiz 5 jours de suite
        # Utiliser la même logique que pour l'achievement
        results = db.query(QuizResult).filter(QuizResult.student_id == user_id).order_by(QuizResult.completed_at).all()
        
        if not results:
            return {"current": 0, "target": 5}
        
        from datetime import datetime, timedelta
        daily_activity = {}
        for result in results:
            day = result.completed_at.date()
            if day not in daily_activity:
                daily_activity[day] = 0
            daily_activity[day] += 1
        
        dates = sorted(daily_activity.keys())
        max_streak = 0
        current_streak = 0
        
        for i, date in enumerate(dates):
            if i == 0:
                current_streak = 1
            else:
                prev_date = dates[i-1]
                if (date - prev_date).days == 1:
                    current_streak += 1
                else:
                    current_streak = 1
            
            max_streak = max(max_streak, current_streak)
        
        return {"current": max_streak, "target": 5}
    
    return {"current": 0, "target": 1}

@router.get("/leaderboards/")
def get_leaderboards(
    leaderboard_type: str = None,
    subject: str = None,
    class_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student']))
):
    """Récupérer les classements."""
    
    query = db.query(Leaderboard).filter(Leaderboard.is_active == True)
    
    if leaderboard_type:
        query = query.filter(Leaderboard.leaderboard_type == leaderboard_type)
    if subject:
        query = query.filter(Leaderboard.subject == subject)
    if class_id:
        query = query.filter(Leaderboard.class_id == class_id)
    
    leaderboards = query.all()
    
    # Enrichir avec les entrées
    enriched_leaderboards = []
    for leaderboard in leaderboards:
        entries = db.query(LeaderboardEntry).filter(
            LeaderboardEntry.leaderboard_id == leaderboard.id
        ).order_by(LeaderboardEntry.score.desc()).limit(10).all()
        
        enriched_leaderboard = {
            **leaderboard.__dict__,
            "entries": entries
        }
        enriched_leaderboards.append(enriched_leaderboard)
    
    return enriched_leaderboards

@router.get("/leaderboard")
def get_leaderboard(
    leaderboard_type: str = "global",
    class_id: int = None,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Accepter tous les utilisateurs connectés
):
    """Obtenir le classement."""
    try:
        # Construire la requête de base
        query = db.query(User).filter(User.role == UserRole.student)
        
        # Filtrer par classe si spécifié
        if class_id:
            # Utiliser la relation ClassStudent pour filtrer par classe
            query = query.join(ClassStudent).filter(ClassStudent.class_id == class_id)
        
        # Récupérer tous les étudiants avec leurs statistiques
        students = query.all()
        
        leaderboard_entries = []
        for student in students:
            # Calculer le score total basé sur les résultats de quiz
            quiz_results = db.query(QuizResult).filter(QuizResult.student_id == student.id).all()
            
            if quiz_results:
                total_score = sum(result.score for result in quiz_results)
                avg_score = total_score / len(quiz_results)
                quiz_count = len(quiz_results)
            else:
                total_score = 0
                avg_score = 0
                quiz_count = 0
            
            # Compter les badges
            badges_count = db.query(UserBadge).filter(UserBadge.user_id == student.id).count()
            
            # Calculer le niveau basé sur l'expérience
            user_level = db.query(UserLevel).filter(UserLevel.user_id == student.id).first()
            level = user_level.level if user_level else 1
            
            # Score final basé sur plusieurs facteurs
            final_score = (avg_score * 0.6) + (badges_count * 10) + (level * 5) + (quiz_count * 2)
            
            leaderboard_entries.append({
                "rank": 0,  # Sera calculé après tri
                "user_id": student.id,
                "username": student.username,
                "score": round(final_score, 1),
                "level": level,
                "badges_count": badges_count,
                "quiz_count": quiz_count,
                "avg_score": round(avg_score, 1)
            })
        
        # Trier par score décroissant et assigner les rangs
        leaderboard_entries.sort(key=lambda x: x["score"], reverse=True)
        for i, entry in enumerate(leaderboard_entries):
            entry["rank"] = i + 1
        
        return {
            "leaderboard_type": leaderboard_type,
            "class_id": class_id,
            "entries": leaderboard_entries[:limit]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de classement: {str(e)}")

@router.get("/learning-streak")
def get_learning_streak(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Récupérer les données de série d'apprentissage."""
    try:
        # Récupérer l'activité des 30 derniers jours
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        activities = db.query(LearningHistory).filter(
            LearningHistory.timestamp >= thirty_days_ago
        ).order_by(LearningHistory.timestamp).all()
        
        # Créer un historique des 30 derniers jours
        history = []
        current_streak = 0
        best_streak = 0
        temp_streak = 0
        
        # Grouper par jour
        daily_activity = {}
        for activity in activities:
            day = activity.created_at.date()
            if day not in daily_activity:
                daily_activity[day] = 0
            daily_activity[day] += 1
        
        # Créer l'historique des 30 derniers jours
        for i in range(30):
            check_date = datetime.utcnow().date() - timedelta(days=29-i)
            if check_date in daily_activity and daily_activity[check_date] > 0:
                history.append(1)
                temp_streak += 1
                if temp_streak > best_streak:
                    best_streak = temp_streak
            else:
                history.append(0)
                if temp_streak > 0:
                    temp_streak = 0
        
        # Calculer la série actuelle
        current_streak = 0
        for i in range(len(history)-1, -1, -1):
            if history[i] == 1:
                current_streak += 1
            else:
                break
        
        return {
            "current": current_streak,
            "best": best_streak,
            "history": history
        }
        
    except Exception as e:
        print(f"Erreur dans get_learning_streak: {str(e)}")
        return {
            "current": 0,
            "best": 0,
            "history": [0] * 30
        } 

@router.get("/user-progress")
def get_user_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['student', 'admin']))
):
    """Récupérer la progression de l'utilisateur (points, niveau, etc.)."""
    try:
        # Calculer les points totaux basés sur les activités
        activities = db.query(LearningHistory).filter(
            LearningHistory.student_id == current_user.id
        ).all()
        
        total_points = 0
        for activity in activities:
            # Points basés sur le type d'action
            if "quiz" in activity.action.lower():
                total_points += 50
            elif "content" in activity.action.lower():
                total_points += 30
            elif "learning_path" in activity.action.lower():
                total_points += 100
            else:
                total_points += 25
        
        # Calculer le niveau (1 point = 1 XP, niveau tous les 1000 XP)
        current_xp = total_points
        level = (current_xp // 1000) + 1
        xp_to_next_level = 1000 - (current_xp % 1000)
        
        # Déterminer le rang
        if level <= 2:
            rank = "Débutant"
        elif level <= 5:
            rank = "Intermédiaire"
        elif level <= 10:
            rank = "Avancé"
        else:
            rank = "Expert"
        
        return {
            "totalPoints": total_points,
            "level": level,
            "xpToNextLevel": xp_to_next_level,
            "currentXp": current_xp % 1000,
            "rank": rank
        }
        
    except Exception as e:
        print(f"Erreur dans get_user_progress: {str(e)}")
        return {
            "totalPoints": 0,
            "level": 1,
            "xpToNextLevel": 1000,
            "currentXp": 0,
            "rank": "Débutant"
        } 

@router.get("/user/stats")
def get_user_gamification_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Accepter tous les utilisateurs connectés
):
    """Récupérer les statistiques de gamification de l'utilisateur connecté."""
    
    try:
        print(f"[DEBUG] get_user_gamification_stats appelé pour user_id: {current_user.id}")
        
        # Récupérer le niveau de l'utilisateur
        user_level = db.query(UserLevel).filter(UserLevel.user_id == current_user.id).first()
        
        # Récupérer les badges
        user_badges = db.query(UserBadge).filter(UserBadge.user_id == current_user.id).count()
        
        # Récupérer les achievements
        user_achievements = db.query(UserAchievement).filter(UserAchievement.user_id == current_user.id).count()
        
        # Récupérer les challenges
        user_challenges = db.query(UserChallenge).filter(UserChallenge.user_id == current_user.id).count()
        completed_challenges = db.query(UserChallenge).filter(
            UserChallenge.user_id == current_user.id,
            UserChallenge.is_completed == True
        ).count()
        
        # Récupérer les résultats de quiz
        quiz_results = db.query(QuizResult).filter(QuizResult.student_id == current_user.id).all()
        total_quizzes = len(quiz_results)
        completed_quizzes = len([r for r in quiz_results if r.is_completed])
        avg_score = sum(r.score for r in quiz_results if r.score) / len(quiz_results) if quiz_results else 0
        
        # Créer un niveau par défaut si l'utilisateur n'en a pas
        if not user_level:
            user_level = UserLevel(
                user_id=current_user.id,
                level=1,
                current_xp=0,
                total_xp=0,
                xp_to_next_level=1000
            )
            db.add(user_level)
            db.commit()
            db.refresh(user_level)
        
        # Calculer le pourcentage de progression
        progress_percentage = (user_level.current_xp / 1000) * 100 if user_level else 0
        
        result = {
            "user_id": current_user.id,
            "level": user_level.level if user_level else 1,
            "current_xp": user_level.current_xp if user_level else 0,
            "total_xp": user_level.total_xp if user_level else 0,
            "progress_percentage": progress_percentage,
            "badges_count": user_badges,
            "achievements_count": user_achievements,
            "challenges_count": user_challenges,
            "completed_challenges": completed_challenges,
            "total_quizzes": total_quizzes,
            "completed_quizzes": completed_quizzes,
            "average_score": round(avg_score, 2),
            "completion_rate": round((completed_quizzes / total_quizzes * 100) if total_quizzes > 0 else 0, 2)
        }
        
        print(f"[DEBUG] Résultat: {result}")
        return result
        
    except Exception as e:
        print(f"[ERROR] Erreur dans get_user_gamification_stats: {e}")
        import traceback
        traceback.print_exc()
        # Retourner des données par défaut en cas d'erreur
        return {
            "user_id": current_user.id if current_user else 0,
            "level": 1,
            "current_xp": 0,
            "total_xp": 0,
            "progress_percentage": 0,
            "badges_count": 0,
            "achievements_count": 0,
            "challenges_count": 0,
            "completed_challenges": 0,
            "total_quizzes": 0,
            "completed_quizzes": 0,
            "average_score": 0,
            "completion_rate": 0
        } 

@router.get("/student/{student_id}/stats")
def get_student_gamification_stats(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Récupérer les statistiques de gamification d'un étudiant spécifique (pour les profs)."""
    
    try:
        print(f"[DEBUG] get_student_gamification_stats appelé pour student_id: {student_id}")
        
        # Vérifier que l'étudiant existe
        student = db.query(User).filter(User.id == student_id, User.role == UserRole.student).first()
        if not student:
            raise HTTPException(status_code=404, detail="Étudiant non trouvé")
        
        # Récupérer le niveau de l'étudiant
        user_level = db.query(UserLevel).filter(UserLevel.user_id == student_id).first()
        
        # Récupérer les badges
        user_badges = db.query(UserBadge).filter(UserBadge.user_id == student_id).all()
        badges_info = []
        for user_badge in user_badges:
            badge = db.query(Badge).filter(Badge.id == user_badge.badge_id).first()
            if badge:
                badges_info.append({
                    "id": badge.id,
                    "name": badge.name,
                    "description": badge.description,
                    "icon": "🏆",
                    "awarded_at": user_badge.awarded_at.isoformat() if user_badge.awarded_at else None
                })
        
        # Récupérer les achievements
        user_achievements = db.query(UserAchievement).filter(UserAchievement.user_id == student_id).count()
        
        # Récupérer les challenges
        user_challenges = db.query(UserChallenge).filter(UserChallenge.user_id == student_id).count()
        completed_challenges = db.query(UserChallenge).filter(
            UserChallenge.user_id == student_id,
            UserChallenge.is_completed == True
        ).count()
        
        # Récupérer les résultats de quiz
        quiz_results = db.query(QuizResult).filter(QuizResult.student_id == student_id).all()
        total_quizzes = len(quiz_results)
        completed_quizzes = len([r for r in quiz_results if r.is_completed])
        avg_score = sum(r.score for r in quiz_results if r.score) / len(quiz_results) if quiz_results else 0
        
        # Créer un niveau par défaut si l'étudiant n'en a pas
        if not user_level:
            user_level = UserLevel(
                user_id=student_id,
                level=1,
                current_xp=0,
                total_xp=0,
                xp_to_next_level=1000
            )
            db.add(user_level)
            db.commit()
            db.refresh(user_level)
        
        # Calculer le pourcentage de progression
        progress_percentage = (user_level.current_xp / 1000) * 100 if user_level else 0
        
        # Générer des activités récentes simulées
        recent_activity = []
        if quiz_results:
            for i, result in enumerate(quiz_results[:5]):
                recent_activity.append({
                    "id": i + 1,
                    "type": "quiz_completed",
                    "description": f"Quiz complété avec un score de {result.score}%",
                    "points_earned": 10 + (result.score // 10),
                    "timestamp": result.created_at.isoformat() if result.created_at else datetime.utcnow().isoformat()
                })
        
        result = {
            "user_id": student_id,
            "level": user_level.level if user_level else 1,
            "current_xp": user_level.current_xp if user_level else 0,
            "total_xp": user_level.total_xp if user_level else 0,
            "progress_percentage": progress_percentage,
            "badges_count": len(badges_info),
            "achievements_count": user_achievements,
            "challenges_count": user_challenges,
            "completed_challenges": completed_challenges,
            "total_quizzes": total_quizzes,
            "completed_quizzes": completed_quizzes,
            "average_score": round(avg_score, 2),
            "completion_rate": round((completed_quizzes / total_quizzes * 100) if total_quizzes > 0 else 0, 2),
            "badges": badges_info,
            "recent_activity": recent_activity
        }
        
        print(f"[DEBUG] Résultat: {result}")
        return result
        
    except Exception as e:
        print(f"[ERROR] Erreur dans get_student_gamification_stats: {e}")
        import traceback
        traceback.print_exc()
        # Retourner des données par défaut en cas d'erreur
        return {
            "user_id": student_id,
            "level": 1,
            "current_xp": 0,
            "total_xp": 0,
            "progress_percentage": 0,
            "badges_count": 0,
            "achievements_count": 0,
            "challenges_count": 0,
            "completed_challenges": 0,
            "total_quizzes": 0,
            "completed_quizzes": 0,
            "average_score": 0,
            "completion_rate": 0,
            "badges": [],
            "recent_activity": []
        }

@router.get("/student/{student_id}/badges")
def get_student_badges(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Récupérer les badges d'un étudiant (version test sans auth)"""
    try:
        print(f"🔥 [DEBUG] Récupération des badges pour l'étudiant {student_id}")
        
        # Récupérer les badges de l'étudiant
        user_badges = db.query(UserBadge).filter(UserBadge.user_id == student_id).all()
        badges_info = []
        
        for user_badge in user_badges:
            badge = db.query(Badge).filter(Badge.id == user_badge.badge_id).first()
            if badge:
                badges_info.append({
                    "id": badge.id,
                    "name": badge.name,
                    "description": badge.description,
                    "icon": "🏆",
                    "awarded_at": user_badge.awarded_at.isoformat() if user_badge.awarded_at else None
                })
        
        print(f"🔥 [DEBUG] {len(badges_info)} badges trouvés pour l'étudiant {student_id}")
        return badges_info
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des badges: {e}")
        return [] 