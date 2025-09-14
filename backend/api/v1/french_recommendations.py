#!/usr/bin/env python3
"""
API pour les recommandations françaises personnalisées basées sur l'IA
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import json
import random

from core.database import get_db
from core.security import get_current_user, require_role
from models.user import User, UserRole
from models.french_learning import (
    FrenchLearningProfile, FrenchCompetency, FrenchCompetencyProgress,
    FrenchLearningPath, FrenchRecommendation
)

router = APIRouter(tags=["french_recommendations"])

# Contenu recommandé français
FRENCH_RECOMMENDED_CONTENT = {
    "grammar": {
        "A1": [
            {
                "id": "gram_a1_001",
                "title": "Les Articles Partitifs",
                "type": "video",
                "url": "/content/french/a1/grammar/articles-partitifs.mp4",
                "duration": 12,
                "difficulty": "easy",
                "tags": ["grammaire", "articles", "débutant"]
            },
            {
                "id": "gram_a1_002",
                "title": "La Négation Simple",
                "type": "interactive",
                "url": "/content/french/a1/grammar/negation-simple",
                "duration": 18,
                "difficulty": "easy",
                "tags": ["grammaire", "négation", "débutant"]
            }
        ],
        "A2": [
            {
                "id": "gram_a2_001",
                "title": "Les Pronoms Compléments",
                "type": "video",
                "url": "/content/french/a2/grammar/pronoms-complements.mp4",
                "duration": 20,
                "difficulty": "medium",
                "tags": ["grammaire", "pronoms", "intermédiaire"]
            }
        ]
    },
    "vocabulary": {
        "A1": [
            {
                "id": "voc_a1_001",
                "title": "Les Couleurs",
                "type": "interactive",
                "url": "/content/french/a1/vocabulary/couleurs",
                "duration": 15,
                "difficulty": "easy",
                "tags": ["vocabulaire", "couleurs", "débutant"]
            },
            {
                "id": "voc_a1_002",
                "title": "Les Nombres 1-100",
                "type": "audio",
                "url": "/content/french/a1/vocabulary/nombres.mp3",
                "duration": 25,
                "difficulty": "easy",
                "tags": ["vocabulaire", "nombres", "débutant"]
            }
        ],
        "A2": [
            {
                "id": "voc_a2_001",
                "title": "Les Professions",
                "type": "interactive",
                "url": "/content/french/a2/vocabulary/professions",
                "duration": 30,
                "difficulty": "medium",
                "tags": ["vocabulaire", "professions", "intermédiaire"]
            }
        ]
    },
    "exercises": {
        "A1": [
            {
                "id": "ex_a1_001",
                "title": "Quiz Articles Définis",
                "type": "quiz",
                "url": "/exercises/french/a1/quiz-articles-definis",
                "duration": 10,
                "difficulty": "easy",
                "tags": ["exercice", "quiz", "articles", "débutant"]
            }
        ],
        "A2": [
            {
                "id": "ex_a2_001",
                "title": "Exercice Passé Composé",
                "type": "exercise",
                "url": "/exercises/french/a2/exercice-passe-compose",
                "duration": 15,
                "difficulty": "medium",
                "tags": ["exercice", "conjugaison", "passé", "intermédiaire"]
            }
        ]
    }
}

@router.get("/recommendations/student/{student_id}")
async def get_french_recommendations(
    student_id: int,
    recommendation_type: Optional[str] = None,
    limit: int = 5,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupère les recommandations françaises personnalisées pour un étudiant"""
    try:
        # Vérifier l'autorisation
        if current_user.role not in [UserRole.teacher, UserRole.admin] and current_user.id != student_id:
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        # Récupérer le profil d'apprentissage français
        profile = db.query(FrenchLearningProfile).filter(
            FrenchLearningProfile.student_id == student_id
        ).first()
        
        if not profile:
            raise HTTPException(
                status_code=400,
                detail="L'étudiant doit d'abord passer l'évaluation initiale française"
            )
        
        # Récupérer la progression des compétences
        competency_progress = db.query(FrenchCompetencyProgress).filter(
            FrenchCompetencyProgress.student_id == student_id
        ).all()
        
        # Analyser les forces et faiblesses
        strengths = json.loads(profile.strengths) if profile.strengths else []
        weaknesses = json.loads(profile.weaknesses) if profile.weaknesses else []
        french_level = profile.french_level
        learning_style = profile.learning_style
        
        # Générer des recommandations basées sur l'IA
        recommendations = generate_ai_recommendations(
            student_id, profile, competency_progress, 
            recommendation_type, limit
        )
        
        # Créer ou mettre à jour les recommandations en base
        await save_recommendations_to_db(student_id, recommendations, db)
        
        return {
            "student_id": student_id,
            "french_level": french_level,
            "learning_style": learning_style,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations,
            "total_recommendations": len(recommendations)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la génération des recommandations : {str(e)}"
        )

@router.post("/recommendations/{recommendation_id}/accept")
async def accept_french_recommendation(
    recommendation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Accepte une recommandation française"""
    try:
        # Récupérer la recommandation
        recommendation = db.query(FrenchRecommendation).filter(
            FrenchRecommendation.id == recommendation_id
        ).first()
        
        if not recommendation:
            raise HTTPException(status_code=404, detail="Recommandation non trouvée")
        
        # Vérifier l'autorisation
        if current_user.id != recommendation.student_id:
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        # Marquer comme acceptée
        recommendation.status = "accepted"
        recommendation.accepted_at = datetime.utcnow()
        
        db.commit()
        
        return {
            "recommendation_id": recommendation_id,
            "status": "accepted",
            "message": "Recommandation acceptée avec succès"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'acceptation de la recommandation : {str(e)}"
        )

@router.post("/recommendations/{recommendation_id}/dismiss")
async def dismiss_french_recommendation(
    recommendation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Rejette une recommandation française"""
    try:
        # Récupérer la recommandation
        recommendation = db.query(FrenchRecommendation).filter(
            FrenchRecommendation.id == recommendation_id
        ).first()
        
        if not recommendation:
            raise HTTPException(status_code=404, detail="Recommandation non trouvée")
        
        # Vérifier l'autorisation
        if current_user.id != recommendation.student_id:
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        # Marquer comme rejetée
        recommendation.status = "dismissed"
        recommendation.dismissed_at = datetime.utcnow()
        
        db.commit()
        
        return {
            "recommendation_id": recommendation_id,
            "status": "dismissed",
            "message": "Recommandation rejetée"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du rejet de la recommandation : {str(e)}"
        )

@router.get("/recommendations/class/{class_id}/common")
async def get_common_french_recommendations(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Récupère les recommandations françaises communes pour une classe"""
    try:
        # Récupérer les étudiants de la classe
        from models.class_group import ClassStudent
        class_students = db.query(ClassStudent).filter(
            ClassStudent.class_id == class_id
        ).all()
        
        if not class_students:
            return {
                "message": "Aucun étudiant dans cette classe",
                "common_recommendations": []
            }
        
        student_ids = [cs.student_id for cs in class_students]
        
        # Analyser les profils de la classe
        class_profiles = db.query(FrenchLearningProfile).filter(
            FrenchLearningProfile.student_id.in_(student_ids)
        ).all()
        
        if not class_profiles:
            return {
                "message": "Aucun profil français trouvé pour cette classe",
                "common_recommendations": []
            }
        
        # Identifier les difficultés communes
        common_weaknesses = analyze_common_weaknesses(class_profiles)
        
        # Générer des recommandations communes
        common_recommendations = generate_common_recommendations(common_weaknesses)
        
        return {
            "class_id": class_id,
            "total_students": len(class_profiles),
            "common_weaknesses": common_weaknesses,
            "common_recommendations": common_recommendations
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération des recommandations communes : {str(e)}"
        )

# Fonctions utilitaires IA
def generate_ai_recommendations(
    student_id: int,
    profile: FrenchLearningProfile,
    competency_progress: List[FrenchCompetencyProgress],
    recommendation_type: Optional[str],
    limit: int
) -> List[Dict[str, Any]]:
    """Génère des recommandations personnalisées basées sur l'IA"""
    
    recommendations = []
    french_level = profile.french_level
    learning_style = profile.learning_style
    
    # Analyser les compétences en difficulté
    weak_competencies = []
    strong_competencies = []
    
    for progress in competency_progress:
        if progress.progress_percentage < 50:
            weak_competencies.append(progress.competency_id)
        elif progress.progress_percentage > 80:
            strong_competencies.append(progress.competency_id)
    
    # Recommandations de remédiation (pour les compétences faibles)
    if weak_competencies and (not recommendation_type or recommendation_type == "remediation"):
        remediation_recs = generate_remediation_recommendations(
            weak_competencies, french_level, learning_style
        )
        recommendations.extend(remediation_recs)
    
    # Recommandations de renforcement (pour les compétences fortes)
    if strong_competencies and (not recommendation_type or recommendation_type == "reinforcement"):
        reinforcement_recs = generate_reinforcement_recommendations(
            strong_competencies, french_level, learning_style
        )
        recommendations.extend(reinforcement_recs)
    
    # Recommandations de progression
    if not recommendation_type or recommendation_type == "progression":
        progression_recs = generate_progression_recommendations(
            french_level, learning_style
        )
        recommendations.extend(progression_recs)
    
    # Mélanger et limiter les recommandations
    random.shuffle(recommendations)
    return recommendations[:limit]

def generate_remediation_recommendations(
    weak_competencies: List[int],
    french_level: str,
    learning_style: str
) -> List[Dict[str, Any]]:
    """Génère des recommandations de remédiation"""
    recommendations = []
    
    # Contenu de remédiation pour les compétences faibles
    for competency_id in weak_competencies:
        if french_level in FRENCH_RECOMMENDED_CONTENT["exercises"]:
            exercises = FRENCH_RECOMMENDED_CONTENT["exercises"][french_level]
            for exercise in exercises:
                recommendations.append({
                    "id": f"remediation_{competency_id}_{exercise['id']}",
                    "type": "remediation",
                    "title": f"Remédiation : {exercise['title']}",
                    "content": exercise,
                    "reason": "Compétence identifiée comme faible",
                    "priority": "high",
                    "estimated_duration": exercise["duration"]
                })
    
    return recommendations

def generate_reinforcement_recommendations(
    strong_competencies: List[int],
    french_level: str,
    learning_style: str
) -> List[Dict[str, Any]]:
    """Génère des recommandations de renforcement"""
    recommendations = []
    
    # Contenu de renforcement pour les compétences fortes
    if french_level in FRENCH_RECOMMENDED_CONTENT["grammar"]:
        grammar_content = FRENCH_RECOMMENDED_CONTENT["grammar"][french_level]
        for content in grammar_content:
            recommendations.append({
                "id": f"reinforcement_grammar_{content['id']}",
                "type": "reinforcement",
                "title": f"Renforcement : {content['title']}",
                "content": content,
                "reason": "Compétence identifiée comme forte - possibilité d'approfondir",
                "priority": "medium",
                "estimated_duration": content["duration"]
            })
    
    return recommendations

def generate_progression_recommendations(
    french_level: str,
    learning_style: str
) -> List[Dict[str, Any]]:
    """Génère des recommandations de progression"""
    recommendations = []
    
    # Déterminer le niveau suivant
    level_progression = {"A1": "A2", "A2": "B1", "B1": "B2", "B2": "C1", "C1": "C2"}
    next_level = level_progression.get(french_level, french_level)
    
    # Contenu du niveau suivant
    if next_level in FRENCH_RECOMMENDED_CONTENT["vocabulary"]:
        vocab_content = FRENCH_RECOMMENDED_CONTENT["vocabulary"][next_level]
        for content in vocab_content:
            recommendations.append({
                "id": f"progression_vocab_{content['id']}",
                "type": "progression",
                "title": f"Progression vers {next_level} : {content['title']}",
                "content": content,
                "reason": "Préparation au niveau supérieur",
                "priority": "medium",
                "estimated_duration": content["duration"]
            })
    
    return recommendations

def analyze_common_weaknesses(class_profiles: List[FrenchLearningProfile]) -> List[str]:
    """Analyse les faiblesses communes dans une classe"""
    all_weaknesses = []
    
    for profile in class_profiles:
        if profile.weaknesses:
            weaknesses = json.loads(profile.weaknesses)
            all_weaknesses.extend(weaknesses)
    
    # Compter les occurrences
    weakness_counts = {}
    for weakness in all_weaknesses:
        weakness_counts[weakness] = weakness_counts.get(weakness, 0) + 1
    
    # Retourner les faiblesses les plus communes (plus de 50% de la classe)
    threshold = len(class_profiles) * 0.5
    common_weaknesses = [
        weakness for weakness, count in weakness_counts.items()
        if count >= threshold
    ]
    
    return common_weaknesses

def generate_common_recommendations(common_weaknesses: List[str]) -> List[Dict[str, Any]]:
    """Génère des recommandations communes pour une classe"""
    recommendations = []
    
    for weakness in common_weaknesses:
        if weakness == "grammaire":
            recommendations.append({
                "id": f"common_grammar_{weakness}",
                "type": "common",
                "title": "Atelier Grammaire Collective",
                "description": "Session de remédiation collective sur les points grammaticaux difficiles",
                "duration": 45,
                "format": "groupe",
                "priority": "high"
            })
        elif weakness == "vocabulaire":
            recommendations.append({
                "id": f"common_vocab_{weakness}",
                "type": "common",
                "title": "Jeu de Vocabulaire Interactif",
                "description": "Activité collective pour enrichir le vocabulaire",
                "duration": 30,
                "format": "groupe",
                "priority": "medium"
            })
    
    return recommendations

async def save_recommendations_to_db(
    student_id: int,
    recommendations: List[Dict[str, Any]],
    db: Session
):
    """Sauvegarde les recommandations en base de données"""
    try:
        for rec in recommendations:
            # Vérifier si la recommandation existe déjà
            existing_rec = db.query(FrenchRecommendation).filter(
                FrenchRecommendation.student_id == student_id,
                FrenchRecommendation.content_id == rec.get("id"),
                FrenchRecommendation.status == "pending"
            ).first()
            
            if not existing_rec:
                # Créer une nouvelle recommandation
                new_rec = FrenchRecommendation(
                    student_id=student_id,
                    recommendation_type=rec["type"],
                    content_id=rec.get("id"),
                    content_type=rec.get("content_type", "unknown"),
                    reason=rec["reason"],
                    priority=rec.get("priority", "medium")
                )
                db.add(new_rec)
        
        db.commit()
        
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des recommandations : {e}")
        db.rollback()
