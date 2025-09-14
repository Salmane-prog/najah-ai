from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from core.database import get_db
from models.user import User
from models.remediation import RemediationResult, RemediationBadge, RemediationProgress
from api.v1.auth import require_role
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json
import logging
from pydantic import BaseModel
from core.security import get_current_user
from models.user import User

# Import de la nouvelle banque d'exercices diversifiée
from data.remediation_exercises import exercise_bank, get_exercises_for_remediation_plan

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(tags=["remediation"])

# Modèles de données
class RemediationStep(BaseModel):
    step_number: int
    topic: str
    learning_objective: str
    content_type: str
    estimated_duration: int
    prerequisites: List[str]
    resources: List[str]

class RemediationPlan(BaseModel):
    student_id: int
    subject: str
    created_date: str
    steps: List[RemediationStep]
    total_duration: int
    progress: int
    current_step: int

class PlanRequest(BaseModel):
    subject: str
    include_exercises: bool = True
    include_assessments: bool = True

# ============================================================================
# ENDPOINTS PRINCIPAUX
# ============================================================================

@router.post("/results", response_model=Dict[str, Any])
async def save_remediation_result(
    result: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Sauvegarder un résultat de remédiation"""
    try:
        logger.info(f"💾 Sauvegarde résultat remédiation pour utilisateur {current_user.id}")
        
        # Créer l'objet RemediationResult
        remediation_result = RemediationResult(
            student_id=result["student_id"],
            topic=result["topic"],
            exercise_type=result["exercise_type"],
            score=result["score"],
            max_score=result["max_score"],
            percentage=result["percentage"],
            time_spent=result.get("time_spent", 0),
            weak_areas_improved=json.dumps(result.get("weak_areas_improved", [])),
            completed_at=datetime.utcnow()
        )
        
        db.add(remediation_result)
        db.commit()
        db.refresh(remediation_result)
        
        # Mettre à jour le progrès
        await update_remediation_progress(db, result["student_id"], result["topic"])
        
        # Vérifier et attribuer des badges
        await check_and_award_badges(db, result["student_id"], result["topic"])
        
        logger.info(f"✅ Résultat sauvegardé avec succès: ID {remediation_result.id}")
        
        return {
            "success": True,
            "message": "Résultat de remédiation sauvegardé",
            "result_id": remediation_result.id,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur sauvegarde résultat: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la sauvegarde: {str(e)}"
        )

@router.get("/results/student/{student_id}", response_model=List[Dict[str, Any]])
async def get_remediation_results(
    student_id: int,
    topic: Optional[str] = Query(None, description="Filtrer par sujet"),
    exercise_type: Optional[str] = Query(None, description="Filtrer par type d'exercice"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer tous les résultats de remédiation pour un étudiant"""
    try:
        logger.info(f"🔍 Récupération résultats remédiation pour étudiant {student_id}")
        
        query = db.query(RemediationResult).filter(RemediationResult.student_id == student_id)
        
        if topic:
            query = query.filter(RemediationResult.topic == topic)
        if exercise_type:
            query = query.filter(RemediationResult.exercise_type == exercise_type)
            
        results = query.order_by(RemediationResult.completed_at.desc()).all()
        
        # Convertir en format JSON
        formatted_results = []
        for result in results:
            formatted_results.append({
                "id": result.id,
                "student_id": result.student_id,
                "topic": result.topic,
                "exercise_type": result.exercise_type,
                "score": result.score,
                "max_score": result.max_score,
                "percentage": result.percentage,
                "time_spent": result.time_spent,
                "completed_at": result.completed_at.isoformat() if result.completed_at else None,
                "weak_areas_improved": json.loads(result.weak_areas_improved) if result.weak_areas_improved else []
            })
        
        logger.info(f"✅ {len(formatted_results)} résultats récupérés")
        return formatted_results
        
    except Exception as e:
        logger.error(f"❌ Erreur récupération résultats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération: {str(e)}"
        )

@router.get("/progress/student/{student_id}", response_model=List[Dict[str, Any]])
async def get_remediation_progress(
    student_id: int,
    topic: Optional[str] = Query(None, description="Filtrer par sujet"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer le progrès de remédiation pour un étudiant"""
    try:
        logger.info(f"📊 Récupération progrès remédiation pour étudiant {student_id}")
        
        query = db.query(RemediationProgress).filter(RemediationProgress.student_id == student_id)
        
        if topic:
            query = query.filter(RemediationProgress.topic == topic)
            
        progress = query.all()
        
        # Convertir en format JSON
        formatted_progress = []
        for prog in progress:
            formatted_progress.append({
                "id": prog.id,
                "student_id": prog.student_id,
                "topic": prog.topic,
                "current_level": prog.current_level,
                "previous_level": prog.previous_level,
                "improvement": prog.improvement,
                "exercises_completed": prog.exercises_completed,
                "total_exercises": prog.total_exercises,
                "success_rate": prog.success_rate,
                "last_updated": prog.last_updated.isoformat() if prog.last_updated else None
            })
        
        logger.info(f"✅ Progrès récupéré pour {len(formatted_progress)} sujets")
        return formatted_progress
        
    except Exception as e:
        logger.error(f"❌ Erreur récupération progrès: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération du progrès: {str(e)}"
        )

# ============================================================================
# ENDPOINTS DE BADGES ET RÉCOMPENSES
# ============================================================================

@router.get("/badges/student/{student_id}", response_model=List[Dict[str, Any]])
async def get_student_badges(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer tous les badges d'un étudiant"""
    try:
        badges = db.query(RemediationBadge).filter(
            RemediationBadge.student_id == student_id
        ).order_by(RemediationBadge.earned_at.desc()).all()
        
        formatted_badges = []
        for badge in badges:
            formatted_badges.append({
                "id": badge.id,
                "student_id": badge.student_id,
                "badge_type": badge.badge_type,
                "badge_name": badge.badge_name,
                "description": badge.description,
                "earned_at": badge.earned_at.isoformat() if badge.earned_at else None,
                "points": badge.points
            })
        
        return formatted_badges
        
    except Exception as e:
        logger.error(f"❌ Erreur récupération badges: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des badges: {str(e)}"
        )

@router.post("/badges/award", response_model=Dict[str, Any])
async def award_badge(
    badge_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Attribuer un badge à un étudiant"""
    try:
        # Vérifier si le badge existe déjà
        existing_badge = db.query(RemediationBadge).filter(
            RemediationBadge.student_id == badge_data["student_id"],
            RemediationBadge.badge_type == badge_data["badge_type"],
            RemediationBadge.badge_name == badge_data["badge_name"]
        ).first()
        
        if existing_badge:
            return {
                "success": False,
                "message": "Badge déjà attribué",
                "badge_id": existing_badge.id
            }
        
        # Créer le nouveau badge
        badge = RemediationBadge(
            student_id=badge_data["student_id"],
            badge_type=badge_data["badge_type"],
            badge_name=badge_data["badge_name"],
            description=badge_data.get("description", ""),
            points=badge_data.get("points", 0),
            earned_at=datetime.utcnow()
        )
        
        db.add(badge)
        db.commit()
        db.refresh(badge)
        
        return {
            "success": True,
            "message": "Badge attribué avec succès",
            "badge_id": badge.id
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur attribution badge: {str(e)}")
        db.rollback()

# ============================================================================
# ENDPOINTS DE STATISTIQUES ET ANALYTICS
# ============================================================================

@router.get("/stats/student/{student_id}", response_model=Dict[str, Any])
async def get_remediation_stats(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les statistiques de remédiation pour un étudiant"""
    try:
        # Statistiques générales
        total_exercises = db.query(func.count(RemediationResult.id)).filter(
            RemediationResult.student_id == student_id
        ).scalar()
        
        total_score = db.query(func.sum(RemediationResult.score)).filter(
            RemediationResult.student_id == student_id
        ).scalar() or 0
        
        total_max_score = db.query(func.sum(RemediationResult.max_score)).filter(
            RemediationResult.student_id == student_id
        ).scalar() or 0
        
        avg_percentage = (total_score / total_max_score * 100) if total_max_score > 0 else 0
        
        # Statistiques par type d'exercice
        exercise_stats = db.query(
            RemediationResult.exercise_type,
            func.count(RemediationResult.id).label('count'),
            func.avg(RemediationResult.percentage).label('avg_percentage')
        ).filter(
            RemediationResult.student_id == student_id
        ).group_by(RemediationResult.exercise_type).all()
        
        exercise_breakdown = {}
        for stat in exercise_stats:
            exercise_breakdown[stat.exercise_type] = {
                "count": stat.count,
                "average_percentage": round(stat.avg_percentage, 2) if stat.avg_percentage else 0
            }
        
        # Statistiques par sujet
        topic_stats = db.query(
            RemediationResult.topic,
            func.count(RemediationResult.id).label('count'),
            func.avg(RemediationResult.percentage).label('avg_percentage')
        ).filter(
            RemediationResult.student_id == student_id
        ).group_by(RemediationResult.topic).all()
        
        topic_breakdown = {}
        for stat in topic_stats:
            topic_breakdown[stat.topic] = {
                "count": stat.count,
                "average_percentage": round(stat.avg_percentage, 2) if stat.avg_percentage else 0
            }
        
        return {
            "student_id": student_id,
            "total_exercises": total_exercises,
            "overall_average": round(avg_percentage, 2),
            "total_score": total_score,
            "total_max_score": total_max_score,
            "exercise_breakdown": exercise_breakdown,
            "topic_breakdown": topic_breakdown,
            "last_updated": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur récupération statistiques: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des statistiques: {str(e)}"
        )

# ============================================================================
# ENDPOINTS DE COMPARAISON ET RECOMMANDATIONS
# ============================================================================

@router.get("/comparison/student/{student_id}", response_model=Dict[str, Any])
async def get_progress_comparison(
    student_id: int,
    topic: Optional[str] = Query(None, description="Sujet spécifique"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Comparer le progrès avant/après remédiation"""
    try:
        # Récupérer les résultats récents (derniers 30 jours)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        recent_results = db.query(RemediationResult).filter(
            RemediationResult.student_id == student_id,
            RemediationResult.completed_at >= thirty_days_ago
        )
        
        if topic:
            recent_results = recent_results.filter(RemediationResult.topic == topic)
            
        recent_results = recent_results.order_by(RemediationResult.completed_at.asc()).all()
        
        if len(recent_results) < 2:
            return {
                "student_id": student_id,
                "message": "Pas assez de données pour la comparaison",
                "data_points": len(recent_results)
            }
        
        # Calculer l'amélioration
        first_result = recent_results[0]
        last_result = recent_results[-1]
        
        improvement = last_result.percentage - first_result.percentage
        
        # Analyser la tendance
        scores = [r.percentage for r in recent_results]
        trend = "stable"
        if len(scores) >= 3:
            if scores[-1] > scores[0] + 5:
                trend = "amélioration"
            elif scores[-1] < scores[0] - 5:
                trend = "dégradation"
        
        return {
            "student_id": student_id,
            "topic": topic or "tous",
            "comparison": {
                "first_result": {
                    "date": first_result.completed_at.isoformat(),
                    "percentage": first_result.percentage
                },
                "last_result": {
                    "date": last_result.completed_at.isoformat(),
                    "percentage": last_result.percentage
                },
                "improvement": round(improvement, 2),
                "trend": trend
            },
            "total_exercises": len(recent_results),
            "period_days": 30
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur comparaison progrès: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la comparaison: {str(e)}"
        )

@router.get("/recommendations/student/{student_id}", response_model=List[Dict[str, Any]])
async def get_remediation_recommendations(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Générer des recommandations de remédiation personnalisées"""
    try:
        # Analyser les performances récentes
        recent_results = db.query(RemediationResult).filter(
            RemediationResult.student_id == student_id,
            RemediationResult.completed_at >= datetime.utcnow() - timedelta(days=14)
        ).all()
        
        if not recent_results:
            return [
                {
                    "type": "commencer",
                    "message": "Commencez votre parcours de remédiation",
                    "priority": "high",
                    "action": "Commencer par un quiz d'évaluation"
                }
            ]
        
        recommendations = []
        
        # Analyser les domaines faibles
        topic_performance = {}
        for result in recent_results:
            if result.topic not in topic_performance:
                topic_performance[result.topic] = []
            topic_performance[result.topic].append(result.percentage)
        
        for topic, scores in topic_performance.items():
            avg_score = sum(scores) / len(scores)
            
            if avg_score < 60:
                recommendations.append({
                    "type": "amélioration",
                    "topic": topic,
                    "message": f"Continuez à travailler sur {topic}",
                    "priority": "high",
                    "action": f"Réviser {topic} avec des exercices ciblés",
                    "current_level": round(avg_score, 1),
                    "target_level": 75
                })
            elif avg_score < 80:
                recommendations.append({
                    "type": "consolidation",
                    "topic": topic,
                    "message": f"Consolidez vos connaissances en {topic}",
                    "priority": "medium",
                    "action": f"Pratiquer {topic} avec des exercices avancés",
                    "current_level": round(avg_score, 1),
                    "target_level": 90
                })
        
        # Recommandations basées sur la fréquence
        if len(recent_results) < 5:
            recommendations.append({
                "type": "fréquence",
                "message": "Augmentez la fréquence de vos exercices",
                "priority": "medium",
                "action": "Faire au moins 3 exercices par semaine"
            })
        
        return recommendations[:5]  # Limiter à 5 recommandations
        
    except Exception as e:
        logger.error(f"❌ Erreur génération recommandations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la génération des recommandations: {str(e)}"
        )

# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

async def update_remediation_progress(
    db: Session, 
    student_id: int, 
    topic: str
):
    """Mettre à jour le progrès de remédiation pour un étudiant et un sujet"""
    try:
        # Récupérer ou créer l'entrée de progrès
        progress = db.query(RemediationProgress).filter(
            RemediationProgress.student_id == student_id,
            RemediationProgress.topic == topic
        ).first()
        
        if not progress:
            progress = RemediationProgress(
                student_id=student_id,
                topic=topic,
                current_level=1,
                previous_level=1,
                improvement=0.0,
                exercises_completed=0,
                total_exercises=0,
                success_rate=0.0
            )
            db.add(progress)
        
        # Récupérer les résultats récents pour ce sujet
        recent_results = db.query(RemediationResult).filter(
            RemediationResult.student_id == student_id,
            RemediationResult.topic == topic
        ).order_by(RemediationResult.completed_at.desc()).limit(10).all()
        
        if recent_results:
            # Calculer les nouvelles métriques
            total_exercises = len(recent_results)
            total_score = sum(r.score for r in recent_results)
            total_max_score = sum(r.max_score for r in recent_results)
            success_rate = (total_score / total_max_score * 100) if total_max_score > 0 else 0
            
            # Mettre à jour le niveau
            previous_level = progress.current_level
            if success_rate >= 90:
                new_level = 5
            elif success_rate >= 80:
                new_level = 4
            elif success_rate >= 70:
                new_level = 3
            elif success_rate >= 60:
                new_level = 2
            else:
                new_level = 1
            
            # Calculer l'amélioration
            improvement = new_level - previous_level
            
            # Mettre à jour l'objet
            progress.previous_level = previous_level
            progress.current_level = new_level
            progress.improvement = improvement
            progress.exercises_completed = total_exercises
            progress.total_exercises = total_exercises
            progress.success_rate = success_rate
            progress.last_updated = datetime.utcnow()
        
        db.commit()
        logger.info(f"✅ Progrès mis à jour pour étudiant {student_id}, sujet {topic}")
        
    except Exception as e:
        logger.error(f"❌ Erreur mise à jour progrès: {str(e)}")
        db.rollback()

async def check_and_award_badges(
    db: Session, 
    student_id: int, 
    topic: str
):
    """Vérifier et attribuer des badges basés sur les performances"""
    try:
        # Récupérer les statistiques du sujet
        topic_results = db.query(RemediationResult).filter(
            RemediationResult.student_id == student_id,
            RemediationResult.topic == topic
        ).all()
        
        if not topic_results:
            return
        
        total_exercises = len(topic_results)
        avg_percentage = sum(r.percentage for r in topic_results) / len(topic_results)
        
        # Badge "Débutant" - Premier exercice
        if total_exercises == 1:
            await award_badge_internal(db, student_id, "achievement", "Débutant", 
                                    "Premier exercice de remédiation complété", 10)
        
        # Badge "Persévérant" - 5 exercices
        if total_exercises == 5:
            await award_badge_internal(db, student_id, "achievement", "Persévérant", 
                                    "5 exercices de remédiation complétés", 25)
        
        # Badge "Expert" - 10 exercices avec >80% de réussite
        if total_exercises >= 10 and avg_percentage >= 80:
            await award_badge_internal(db, student_id, "expertise", "Expert", 
                                    f"Expert en {topic} avec {round(avg_percentage, 1)}% de réussite", 50)
        
        # Badge "Amélioration" - Progrès significatif
        if len(topic_results) >= 3:
            recent_avg = sum(r.percentage for r in topic_results[-3:]) / 3
            first_avg = sum(r.percentage for r in topic_results[:3]) / 3
            if recent_avg > first_avg + 20:
                await award_badge_internal(db, student_id, "improvement", "Amélioration", 
                                        f"Amélioration significative en {topic}", 30)
        
    except Exception as e:
        logger.error(f"❌ Erreur vérification badges: {str(e)}")

async def award_badge_internal(
    db: Session, 
    student_id: int, 
    badge_type: str, 
    badge_name: str, 
    description: str, 
    points: int
):
    """Attribuer un badge en interne (sans endpoint public)"""
    try:
        # Vérifier si le badge existe déjà
        existing = db.query(RemediationBadge).filter(
            RemediationBadge.student_id == student_id,
            RemediationBadge.badge_type == badge_type,
            RemediationBadge.badge_name == badge_name
        ).first()
        
        if not existing:
            badge = RemediationBadge(
                student_id=student_id,
                badge_type=badge_type,
                badge_name=badge_name,
                description=description,
                points=points,
                earned_at=datetime.utcnow()
            )
            db.add(badge)
            db.commit()
            logger.info(f"🏆 Badge '{badge_name}' attribué à l'étudiant {student_id}")
            
    except Exception as e:
        logger.error(f"❌ Erreur attribution badge interne: {str(e)}")
        db.rollback()

# ============================================================================
# ENDPOINTS DE TEST ET DÉVELOPPEMENT
# ============================================================================

@router.get("/health")
async def health_check():
    """Vérification de santé de l'API de remédiation"""
    return {
        "status": "healthy",
        "service": "remediation-api",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

@router.get("/test")
async def test_endpoint():
    """Endpoint de test pour vérifier que l'API fonctionne"""
    return {
        "message": "API de remédiation fonctionnelle",
        "endpoints": [
            "/results",
            "/results/student/{student_id}",
            "/progress/student/{student_id}",
            "/badges/student/{student_id}",
            "/stats/student/{student_id}",
            "/comparison/student/{student_id}",
            "/recommendations/student/{student_id}"
        ],
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/student/{student_id}/plan-test")
async def generate_remediation_plan_test(
    student_id: int,
    subject_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Générer un plan de remédiation de test pour un étudiant"""
    try:
        logger.info(f"📋 Génération plan de remédiation de test pour étudiant {student_id}")
        
        # Récupérer les résultats de remédiation existants
        results = db.query(RemediationResult).filter(
            RemediationResult.student_id == student_id
        ).all()
        
        # Calculer la progression basée sur les résultats existants
        total_exercises = len(results)
        if total_exercises > 0:
            avg_percentage = sum(r.percentage for r in results) / total_exercises
            progress = min(100, avg_percentage)
        else:
            progress = 0
        
        # Créer un plan de remédiation de test
        plan = {
            "student_id": student_id,
            "subject": subject_data.get("subject", "Français"),
            "progress": progress,
            "current_step": min(total_exercises + 1, 5),  # Étape actuelle
            "plan_steps": [
                {
                    "step_number": 1,
                    "topic": "Fondamentaux",
                    "learning_objective": "Maîtriser les bases de la grammaire",
                    "estimated_duration": 30,
                    "content_type": "quiz"
                },
                {
                    "step_number": 2,
                    "topic": "Conjugaison",
                    "learning_objective": "Apprendre les temps principaux",
                    "estimated_duration": 45,
                    "content_type": "reading"
                },
                {
                    "step_number": 3,
                    "topic": "Vocabulaire",
                    "learning_objective": "Enrichir le vocabulaire de base",
                    "estimated_duration": 25,
                    "content_type": "practice"
                },
                {
                    "step_number": 4,
                    "topic": "Compréhension",
                    "learning_objective": "Améliorer la compréhension écrite",
                    "estimated_duration": 40,
                    "content_type": "quiz"
                },
                {
                    "step_number": 5,
                    "topic": "Expression",
                    "learning_objective": "Développer l'expression orale",
                    "estimated_duration": 35,
                    "content_type": "practice"
                }
            ],
            "estimated_completion_time": 175,  # 2h55 en minutes
            "weak_areas": [
                {
                    "topic": "Fondamentaux",
                    "current_level": 2,
                    "target_level": 7,
                    "priority": "high"
                },
                {
                    "topic": "Conjugaison",
                    "current_level": 4,
                    "target_level": 7,
                    "priority": "medium"
                }
            ]
        }
        
        logger.info(f"✅ Plan de remédiation généré pour étudiant {student_id}")
        return plan
        
    except Exception as e:
        logger.error(f"❌ Erreur génération plan de remédiation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la génération du plan: {str(e)}"
        ) 

@router.post("/student/{student_id}/plan", response_model=RemediationPlan)
async def generate_remediation_plan(
    student_id: int,
    request: PlanRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Génère un plan de remédiation personnalisé pour un étudiant
    """
    try:
        # Vérifier que l'utilisateur connecté est bien l'étudiant demandé
        if current_user.id != student_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Vous ne pouvez accéder qu'à votre propre plan de remédiation"
            )
        
        # Générer un plan de remédiation simulé basé sur la matière
        plan = generate_simulated_plan(student_id, request.subject)
        
        return plan
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erreur lors de la génération du plan de remédiation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la génération du plan de remédiation"
        )

def generate_simulated_plan(student_id: int, subject: str) -> RemediationPlan:
    """
    Génère un plan de remédiation diversifié et personnalisé
    """
    if subject.lower() == "français":
        # Utiliser la banque d'exercices diversifiée
        topics = ["grammar", "conjugation", "vocabulary", "comprehension"]
        
        # Récupérer des exercices diversifiés pour chaque topic
        diverse_exercises = get_exercises_for_remediation_plan(
            student_id=student_id,
            subject=subject,
            topics=topics,
            difficulty="intermédiaire"
        )
        
        steps = []
        for i, topic in enumerate(topics, 1):
            # Trouver des exercices pour ce topic
            topic_exercises = [ex for ex in diverse_exercises if topic in ex.get("topic", "").lower()]
            
            if topic_exercises:
                # Créer une étape basée sur les exercices disponibles
                exercise = topic_exercises[0]
                steps.append(RemediationStep(
                    step_number=i,
                    topic=exercise["topic"],
                    learning_objective=exercise["question"][:100] + "...",
                    content_type=exercise["type"],
                    estimated_duration=exercise["estimated_time"],
                    prerequisites=[],
                    resources=[f"Exercices {exercise['type']}", "Feedback personnalisé"]
                ))
            else:
                # Fallback si aucun exercice trouvé
                fallback_objectives = {
                    "grammar": "Maîtriser les règles de base de la grammaire française",
                    "conjugation": "Conjuguer correctement les verbes aux temps principaux",
                    "vocabulary": "Enrichir le vocabulaire de base",
                    "comprehension": "Améliorer la compréhension de textes"
                }
                
                steps.append(RemediationStep(
                    step_number=i,
                    topic=topic.capitalize(),
                    learning_objective=fallback_objectives.get(topic, f"Améliorer les compétences en {topic}"),
                    content_type="quiz",
                    estimated_duration=35,
                    prerequisites=[],
                    resources=["Exercices diversifiés", "Feedback adaptatif"]
                ))
    elif subject.lower() == "mathématiques":
        steps = [
            RemediationStep(
                step_number=1,
                topic="Nombres",
                learning_objective="Maîtriser les opérations de base",
                content_type="quiz",
                estimated_duration=40,
                prerequisites=[],
                resources=["Exercices de calcul", "Vidéos explicatives"]
            ),
            RemediationStep(
                step_number=2,
                topic="Géométrie",
                learning_objective="Comprendre les formes et mesures",
                content_type="practice",
                estimated_duration=50,
                prerequisites=["Nombres"],
                resources=["Figures géométriques", "Exercices pratiques"]
            )
        ]
    else:
        # Plan générique pour les autres matières
        steps = [
            RemediationStep(
                step_number=1,
                topic="Bases",
                learning_objective="Acquérir les connaissances fondamentales",
                content_type="reading",
                estimated_duration=30,
                prerequisites=[],
                resources=["Manuel de base", "Résumés"]
            ),
            RemediationStep(
                step_number=2,
                topic="Application",
                learning_objective="Mettre en pratique les connaissances",
                content_type="quiz",
                estimated_duration=45,
                prerequisites=["Bases"],
                resources=["Exercices", "Cas pratiques"]
            )
        ]
    
    total_duration = sum(step.estimated_duration for step in steps)
    
    return RemediationPlan(
        student_id=student_id,
        subject=subject,
        created_date="2024-01-01T00:00:00Z",
        steps=steps,
        total_duration=total_duration,
        progress=0,
        current_step=1
    )

@router.get("/student/{student_id}/results")
async def get_remediation_results(
    student_id: int,
    current_user: User = Depends(get_current_user)
):
    """
    Récupère les résultats de remédiation d'un étudiant
    """
    try:
        if current_user.id != student_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès non autorisé"
            )
        
        # Retourner des résultats simulés
        return {
            "student_id": student_id,
            "results": [
                {
                    "topic": "Fondamentaux",
                    "score": 75,
                    "completed_at": "2024-01-01T10:00:00Z"
                },
                {
                    "topic": "Conjugaison",
                    "score": 80,
                    "completed_at": "2024-01-01T11:00:00Z"
                }
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des résultats"
        )

@router.get("/exercises/diverse")
async def get_diverse_exercises(
    topic: str = Query(..., description="Topic des exercices"),
    difficulty: str = Query(..., description="Niveau de difficulté"),
    count: int = Query(3, description="Nombre d'exercices à récupérer"),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère des exercices diversifiés pour éviter la redondance
    """
    try:
        logger.info(f"🔍 [DIVERSE_EXERCISES] Demande d'exercices: topic={topic}, difficulty={difficulty}, count={count}")
        logger.info(f"👤 [DIVERSE_EXERCISES] Utilisateur authentifié: {current_user.id}")
        
        # Utiliser directement l'ID de l'utilisateur authentifié
        logger.info(f"🔍 [DIVERSE_EXERCISES] Appel à exercise_bank.get_diverse_exercises...")
        
        diverse_exercises = exercise_bank.get_diverse_exercises(
            topic=topic,
            difficulty=difficulty,
            count=count,
            student_id=current_user.id,
            avoid_repetition=False  # Désactivé temporairement pour debug
        )
        
        logger.info(f"🔍 [DIVERSE_EXERCISES] Résultat de exercise_bank: {diverse_exercises}")
        logger.info(f"✅ [DIVERSE_EXERCISES] {len(diverse_exercises)} exercices trouvés")
        
        return {
            "success": True,
            "exercises": diverse_exercises,
            "total_found": len(diverse_exercises),
            "topic": topic,
            "difficulty": difficulty,
            "avoided_repetition": True
        }
        
    except Exception as e:
        logger.error(f"❌ [DIVERSE_EXERCISES] Erreur lors de la récupération d'exercices diversifiés: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération d'exercices: {str(e)}"
        )

@router.get("/exercises/test")
async def test_diverse_exercises_endpoint(
    current_user: User = Depends(get_current_user)
):
    """
    Endpoint de test pour vérifier l'authentification
    """
    logger.info(f"🧪 [TEST_ENDPOINT] Test d'authentification pour utilisateur: {current_user.id}")
    
    return {
        "success": True,
        "message": "Endpoint de test accessible",
        "user_id": current_user.id,
        "user_email": current_user.email,
        "timestamp": datetime.now().isoformat()
    }

@router.get("/exercises/test-public")
async def test_public_endpoint():
    """
    Endpoint de test public sans authentification
    """
    logger.info("🧪 [TEST_PUBLIC] Endpoint public accessible")
    
    return {
        "success": True,
        "message": "Endpoint public accessible",
        "timestamp": datetime.now().isoformat(),
        "note": "Cet endpoint ne nécessite pas d'authentification"
    }

@router.get("/exercises/test-auth")
async def test_auth_endpoint(
    current_user: Optional[User] = Depends(get_current_user)
):
    """
    Endpoint de test avec authentification optionnelle
    """
    if current_user:
        logger.info(f"🧪 [TEST_AUTH] Utilisateur authentifié: {current_user.id}")
        return {
            "success": True,
            "message": "Utilisateur authentifié",
            "user_id": current_user.id,
            "user_email": current_user.email,
            "timestamp": datetime.now().isoformat()
        }
    else:
        logger.info("🧪 [TEST_AUTH] Aucun utilisateur authentifié")
        return {
            "success": False,
            "message": "Aucun utilisateur authentifié",
            "timestamp": datetime.now().isoformat(),
            "note": "Ajoutez le header: Authorization: Bearer VOTRE_TOKEN_JWT"
        }

@router.get("/exercises/debug-auth")
async def debug_auth_endpoint(
    request: Request
):
    """
    Endpoint de debug pour diagnostiquer l'authentification
    """
    logger.info("🔍 [DEBUG_AUTH] Début diagnostic authentification")
    
    # Récupérer tous les headers
    headers = dict(request.headers)
    logger.info(f"📋 [DEBUG_AUTH] Headers reçus: {headers}")
    
    # Vérifier le header Authorization
    auth_header = headers.get("authorization", "NON TROUVÉ")
    logger.info(f"🔑 [DEBUG_AUTH] Header Authorization: {auth_header}")
    
    # Vérifier le header User-Agent
    user_agent = headers.get("user-agent", "NON TROUVÉ")
    logger.info(f"🌐 [DEBUG_AUTH] User-Agent: {user_agent}")
    
    return {
        "success": True,
        "message": "Diagnostic d'authentification",
        "headers_received": list(headers.keys()),
        "authorization_header": auth_header,
        "user_agent": user_agent,
        "timestamp": datetime.now().isoformat(),
        "note": "Vérifiez les logs backend pour plus de détails"
    }

@router.get("/exercises/statistics")
async def get_exercise_statistics(
    current_user: User = Depends(get_current_user)
):
    """
    Retourne des statistiques sur la banque d'exercices
    """
    try:
        from data.remediation_exercises import get_exercise_statistics
        
        stats = get_exercise_statistics()
        
        return {
            "success": True,
            "statistics": stats,
            "message": "Statistiques de la banque d'exercices récupérées avec succès"
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la récupération des statistiques: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des statistiques: {str(e)}"
        )

@router.get("/exercises/by-type/{exercise_type}")
async def get_exercises_by_type(
    exercise_type: str,
    topic: str = Query(None, description="Topic spécifique (optionnel)"),
    difficulty: str = Query(None, description="Niveau de difficulté (optionnel)"),
    count: int = Query(5, description="Nombre d'exercices à récupérer"),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère des exercices par type (quiz, practice, matching, etc.)
    """
    try:
        # Récupérer tous les exercices du type demandé
        all_exercises = []
        
        for category in exercise_bank.all_exercises.values():
            for subcategory in category.values():
                for exercise in subcategory:
                    if exercise["type"] == exercise_type:
                        all_exercises.append(exercise)
        
        # Filtrer par topic si spécifié
        if topic:
            all_exercises = [ex for ex in all_exercises 
                           if topic.lower() in ex.get("topic", "").lower()]
        
        # Filtrer par difficulté si spécifiée
        if difficulty:
            all_exercises = [ex for ex in all_exercises 
                           if ex["difficulty"] == difficulty]
        
        # Mélanger et limiter
        random.shuffle(all_exercises)
        selected_exercises = all_exercises[:count]
        
        return {
            "success": True,
            "exercise_type": exercise_type,
            "exercises": selected_exercises,
            "total_found": len(selected_exercises),
            "filters_applied": {
                "topic": topic,
                "difficulty": difficulty
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la récupération d'exercices par type: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération d'exercices: {str(e)}"
        ) 