from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from app.database import get_db
from app.models.remediation import RemediationResult, RemediationBadge, RemediationProgress
from app.schemas.remediation import (
    RemediationResultCreate, RemediationResultResponse,
    BadgeCreate, BadgeResponse, ProgressCreate, ProgressResponse,
    RemediationStats, ProgressComparison, RemediationRecommendation
)
from app.auth import get_current_user, require_role
from app.models.user import User, UserRole

router = APIRouter(prefix="/api/v1/remediation", tags=["remediation"])

# ============================================================================
# ENDPOINTS POUR LES RÉSULTATS DE REMÉDIATION
# ============================================================================

@router.post("/results", response_model=RemediationResultResponse)
async def create_remediation_result(
    result: RemediationResultCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer un nouveau résultat de remédiation"""
    try:
        # Créer le résultat
        db_result = RemediationResult(**result.dict())
        db.add(db_result)
        db.commit()
        db.refresh(db_result)
        
        # Mettre à jour le progrès
        await update_remediation_progress(db, result.student_id, result.topic)
        
        # Vérifier les badges
        await check_and_award_badges(db, result.student_id, result)
        
        return db_result
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création du résultat: {str(e)}"
        )

@router.get("/results/student/{student_id}", response_model=List[RemediationResultResponse])
async def get_student_remediation_results(
    student_id: int,
    topic: Optional[str] = Query(None, description="Filtrer par domaine"),
    exercise_type: Optional[str] = Query(None, description="Filtrer par type d'exercice"),
    limit: int = Query(100, le=1000, description="Nombre maximum de résultats"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer tous les résultats de remédiation d'un étudiant"""
    query = db.query(RemediationResult).filter(RemediationResult.student_id == student_id)
    
    if topic:
        query = query.filter(RemediationResult.topic == topic)
    if exercise_type:
        query = query.filter(RemediationResult.exercise_type == exercise_type)
    
    results = query.order_by(RemediationResult.completed_at.desc()).limit(limit).all()
    return results

@router.get("/results/{result_id}", response_model=RemediationResultResponse)
async def get_remediation_result(
    result_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer un résultat de remédiation spécifique"""
    result = db.query(RemediationResult).filter(RemediationResult.id == result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Résultat non trouvé")
    return result

# ============================================================================
# ENDPOINTS POUR LES BADGES ET GAMIFICATION
# ============================================================================

@router.post("/badges", response_model=BadgeResponse)
async def create_badge(
    badge: BadgeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer un nouveau badge pour un étudiant"""
    try:
        db_badge = RemediationBadge(**badge.dict())
        db.add(db_badge)
        db.commit()
        db.refresh(db_badge)
        return db_badge
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création du badge: {str(e)}"
        )

@router.get("/badges/student/{student_id}", response_model=List[BadgeResponse])
async def get_student_badges(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer tous les badges d'un étudiant"""
    badges = db.query(RemediationBadge).filter(
        RemediationBadge.student_id == student_id
    ).order_by(RemediationBadge.earned_at.desc()).all()
    return badges

@router.get("/badges/available/{student_id}")
async def get_available_badges(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les badges disponibles et non encore obtenus par un étudiant"""
    # Récupérer les badges déjà obtenus
    earned_badges = db.query(RemediationBadge).filter(
        RemediationBadge.student_id == student_id
    ).all()
    earned_types = {badge.badge_type for badge in earned_badges}
    
    # Définir tous les badges disponibles
    all_badges = [
        {
            "type": "first_quiz",
            "name": "Premier Quiz",
            "description": "Complétez votre premier quiz de remédiation",
            "icon": "🎯",
            "condition": "Compléter 1 quiz"
        },
        {
            "type": "perfect_score",
            "name": "Score Parfait",
            "description": "Obtenez 100% sur un exercice",
            "icon": "⭐",
            "condition": "Score de 100%"
        },
        {
            "type": "speed_learner",
            "name": "Apprenant Rapide",
            "description": "Complétez un exercice en moins de 2 minutes",
            "icon": "⚡",
            "condition": "Temps < 2 minutes"
        },
        {
            "type": "topic_master",
            "name": "Maître du Domaine",
            "description": "Maîtrisez complètement un domaine (niveau 10)",
            "icon": "👑",
            "condition": "Niveau 10 dans un domaine"
        },
        {
            "type": "consistency",
            "name": "Régularité",
            "description": "Complétez 5 exercices consécutifs",
            "icon": "📈",
            "condition": "5 exercices consécutifs"
        },
        {
            "type": "improvement",
            "name": "Progrès Constant",
            "description": "Améliorez votre niveau de 3 points",
            "icon": "🚀",
            "condition": "Amélioration de 3 niveaux"
        }
    ]
    
    # Filtrer les badges non obtenus
    available_badges = [badge for badge in all_badges if badge["type"] not in earned_types]
    
    return {
        "earned_badges": len(earned_badges),
        "total_badges": len(all_badges),
        "available_badges": available_badges
    }

# ============================================================================
# ENDPOINTS POUR LE PROGRÈS ET LES STATISTIQUES
# ============================================================================

@router.get("/progress/student/{student_id}", response_model=List[ProgressResponse])
async def get_student_progress(
    student_id: int,
    topic: Optional[str] = Query(None, description="Filtrer par domaine"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer le progrès de remédiation d'un étudiant"""
    query = db.query(RemediationProgress).filter(RemediationProgress.student_id == student_id)
    
    if topic:
        query = query.filter(RemediationProgress.topic == topic)
    
    progress = query.all()
    return progress

@router.get("/stats/student/{student_id}", response_model=RemediationStats)
async def get_student_stats(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les statistiques complètes de remédiation d'un étudiant"""
    # Récupérer les résultats
    results = db.query(RemediationResult).filter(
        RemediationResult.student_id == student_id
    ).all()
    
    if not results:
        return RemediationStats(
            total_exercises=0,
            average_score=0.0,
            total_time=0,
            topics_covered=[],
            badges_earned=0,
            current_level=0.0
        )
    
    # Calculer les statistiques
    total_exercises = len(results)
    average_score = sum(r.percentage for r in results) / total_exercises
    total_time = sum(r.time_spent for r in results)
    topics_covered = list(set(r.topic for r in results))
    
    # Compter les badges
    badges_count = db.query(RemediationBadge).filter(
        RemediationBadge.student_id == student_id
    ).count()
    
    # Calculer le niveau global
    progress = db.query(RemediationProgress).filter(
        RemediationProgress.student_id == student_id
    ).all()
    
    current_level = sum(p.current_level for p in progress) / len(progress) if progress else 0.0
    
    return RemediationStats(
        total_exercises=total_exercises,
        average_score=average_score,
        total_time=total_time,
        topics_covered=topics_covered,
        badges_earned=badges_count,
        current_level=current_level
    )

# ============================================================================
# ENDPOINTS POUR LA COMPARAISON AVANT/APRÈS
# ============================================================================

@router.get("/comparison/student/{student_id}", response_model=List[ProgressComparison])
async def get_progress_comparison(
    student_id: int,
    days_back: int = Query(30, description="Nombre de jours pour la comparaison"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Comparer le progrès avant/après sur une période donnée"""
    cutoff_date = datetime.now() - timedelta(days=days_back)
    
    # Récupérer le progrès actuel
    current_progress = db.query(RemediationProgress).filter(
        RemediationProgress.student_id == student_id
    ).all()
    
    comparisons = []
    
    for progress in current_progress:
        # Récupérer le progrès historique (avant)
        historical_progress = db.query(RemediationProgress).filter(
            RemediationProgress.student_id == student_id,
            RemediationProgress.topic == progress.topic,
            RemediationProgress.last_updated < cutoff_date
        ).order_by(RemediationProgress.last_updated.desc()).first()
        
        if historical_progress:
            improvement_percentage = ((progress.current_level - historical_progress.current_level) / 
                                   max(historical_progress.current_level, 1)) * 100
            
            # Calculer le temps pour améliorer
            time_to_improve = None
            if progress.improvement > 0:
                recent_results = db.query(RemediationResult).filter(
                    RemediationResult.student_id == student_id,
                    RemediationResult.topic == progress.topic,
                    RemediationResult.completed_at >= cutoff_date
                ).all()
                
                if recent_results:
                    total_time = sum(r.time_spent for r in recent_results)
                    time_to_improve = total_time
            
            comparisons.append(ProgressComparison(
                topic=progress.topic,
                before=historical_progress,
                after=progress,
                improvement_percentage=improvement_percentage,
                time_to_improve=time_to_improve
            ))
    
    return comparisons

# ============================================================================
# ENDPOINTS POUR LES RECOMMANDATIONS
# ============================================================================

@router.get("/recommendations/student/{student_id}", response_model=List[RemediationRecommendation])
async def get_remediation_recommendations(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Générer des recommandations personnalisées de remédiation"""
    # Récupérer le progrès actuel
    progress = db.query(RemediationProgress).filter(
        RemediationProgress.student_id == student_id
    ).all()
    
    recommendations = []
    
    for prog in progress:
        if prog.current_level < 7:  # Niveau cible
            priority = "high" if prog.current_level < 4 else "medium"
            
            if prog.current_level < 4:
                reason = "Niveau très faible, nécessite une attention immédiate"
                suggested_exercises = ["quiz", "reading", "practice"]
                estimated_time = 45
            elif prog.current_level < 6:
                reason = "Niveau faible, pratique régulière recommandée"
                suggested_exercises = ["quiz", "practice"]
                estimated_time = 30
            else:
                reason = "Niveau intermédiaire, quelques exercices pour atteindre la maîtrise"
                suggested_exercises = ["quiz"]
                estimated_time = 20
            
            recommendations.append(RemediationRecommendation(
                topic=prog.topic,
                priority=priority,
                reason=reason,
                suggested_exercises=suggested_exercises,
                estimated_time=estimated_time
            ))
    
    # Trier par priorité
    priority_order = {"high": 0, "medium": 1, "low": 2}
    recommendations.sort(key=lambda x: priority_order[x.priority])
    
    return recommendations

# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

async def update_remediation_progress(db: Session, student_id: int, topic: str):
    """Mettre à jour le progrès de remédiation pour un domaine"""
    # Récupérer tous les résultats pour ce domaine
    results = db.query(RemediationResult).filter(
        RemediationResult.student_id == student_id,
        RemediationResult.topic == topic
    ).all()
    
    if not results:
        return
    
    # Calculer le progrès
    total_exercises = len(results)
    success_rate = sum(r.percentage for r in results) / total_exercises
    current_level = min(10, int(success_rate / 10))
    
    # Vérifier si le progrès existe déjà
    existing_progress = db.query(RemediationProgress).filter(
        RemediationProgress.student_id == student_id,
        RemediationProgress.topic == topic
    ).first()
    
    if existing_progress:
        existing_progress.previous_level = existing_progress.current_level
        existing_progress.current_level = current_level
        existing_progress.improvement = current_level - existing_progress.previous_level
        existing_progress.exercises_completed = total_exercises
        existing_progress.success_rate = success_rate
        existing_progress.last_updated = datetime.now()
    else:
        new_progress = RemediationProgress(
            student_id=student_id,
            topic=topic,
            current_level=current_level,
            previous_level=0,
            improvement=current_level,
            exercises_completed=total_exercises,
            total_exercises=total_exercises,
            success_rate=success_rate
        )
        db.add(new_progress)
    
    db.commit()

async def check_and_award_badges(db: Session, student_id: int, result: RemediationResult):
    """Vérifier et attribuer des badges basés sur les résultats"""
    # Badge: Premier Quiz
    if not db.query(RemediationBadge).filter(
        RemediationBadge.student_id == student_id,
        RemediationBadge.badge_type == "first_quiz"
    ).first():
        first_badge = RemediationBadge(
            student_id=student_id,
            badge_type="first_quiz",
            badge_name="Premier Quiz",
            badge_description="Complétez votre premier quiz de remédiation",
            badge_icon="🎯",
            metadata={"exercise_type": result.exercise_type, "topic": result.topic}
        )
        db.add(first_badge)
    
    # Badge: Score Parfait
    if result.percentage == 100 and not db.query(RemediationBadge).filter(
        RemediationBadge.student_id == student_id,
        RemediationBadge.badge_type == "perfect_score",
        RemediationBadge.metadata.contains({"topic": result.topic})
    ).first():
        perfect_badge = RemediationBadge(
            student_id=student_id,
            badge_type="perfect_score",
            badge_name="Score Parfait",
            badge_description=f"Obtenez 100% en {result.topic}",
            badge_icon="⭐",
            metadata={"topic": result.topic, "score": result.percentage}
        )
        db.add(perfect_badge)
    
    # Badge: Apprenant Rapide
    if result.time_spent < 120 and not db.query(RemediationBadge).filter(
        RemediationBadge.student_id == student_id,
        RemediationBadge.badge_type == "speed_learner",
        RemediationBadge.metadata.contains({"topic": result.topic})
    ).first():
        speed_badge = RemediationBadge(
            student_id=student_id,
            badge_type="speed_learner",
            badge_name="Apprenant Rapide",
            badge_description=f"Complétez {result.topic} en moins de 2 minutes",
            badge_icon="⚡",
            metadata={"topic": result.topic, "time_spent": result.time_spent}
        )
        db.add(speed_badge)
    
    db.commit()











