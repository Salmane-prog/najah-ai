#!/usr/bin/env python3
"""
API pour les parcours d'apprentissage français personnalisés
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
    FrenchLearningPath, FrenchLearningModule
)

router = APIRouter(tags=["french_learning_paths"])

@router.get("/initial-assessment/student/{student_id}/profile")
async def get_student_learning_profile(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer le profil d'apprentissage français de l'étudiant (avec auth)"""
    # Cette fonction nécessite une authentification complète
    # Pour les tests, utilisez la version -test
    raise HTTPException(status_code=501, detail="Utilisez l'endpoint -test pour les tests")

@router.get("/initial-assessment/student/{student_id}/profile-test")
async def get_student_learning_profile_test(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Récupérer le profil d'apprentissage français de l'étudiant (version test sans auth)"""
    try:
        print(f"🔍 [FRENCH_PROFILE] Début analyse profil français pour étudiant {student_id}")
        
        # Vérifier que l'étudiant existe
        student = db.query(User).filter(
            User.id == student_id,
            User.role == UserRole.student
        ).first()
        
        if not student:
            print(f"❌ [FRENCH_PROFILE] Étudiant {student_id} non trouvé")
            raise HTTPException(status_code=404, detail="Étudiant non trouvé")
        
        print(f"✅ [FRENCH_PROFILE] Étudiant trouvé: {student.first_name} {student.last_name}")
        
        # Récupérer le profil d'apprentissage français
        profile = db.query(FrenchLearningProfile).filter(
            FrenchLearningProfile.student_id == student_id
        ).first()
        
        if not profile:
            print(f"⚠️ [FRENCH_PROFILE] Aucun profil français trouvé, création d'un profil par défaut")
            # Créer un profil par défaut basé sur les quiz existants
            from models.quiz import QuizResult
            quiz_results = db.query(QuizResult).filter(
                QuizResult.student_id == student_id,
                QuizResult.is_completed == True
            ).order_by(QuizResult.created_at.desc()).limit(20).all()
            
            if quiz_results:
                # Analyser les performances pour déterminer le niveau
                avg_score = sum(r.score for r in quiz_results) / len(quiz_results)
                if avg_score >= 80:
                    level = "B1"
                    learning_style = "Analytique"
                elif avg_score >= 60:
                    level = "A2"
                    learning_style = "Mixte"
                else:
                    level = "A1"
                    learning_style = "Pratique"
                
                # Déterminer le nom d'affichage
                display_name = "Élève sans nom"
                if student.first_name and student.last_name:
                    display_name = f"{student.first_name} {student.last_name}"
                elif student.username:
                    display_name = student.username
                elif student.email:
                    email_name = student.email.split('@')[0]
                    display_name = email_name.replace('.', ' ').title()
                
                return {
                    "student_id": student_id,
                    "student_name": display_name,
                    "french_level": level,
                    "learning_style": learning_style,
                    "cognitive_profile": {
                        "memory_type": "Mixte",
                        "attention_span": "Moyenne",
                        "problem_solving": "Analytique"
                    },
                    "strengths": [f"Performance générale (Score moyen: {round(avg_score, 1)}%)"],
                    "areas_for_improvement": [],
                    "learning_preferences": {
                        "preferred_content_types": ["interactif", "visuel"],
                        "preferred_difficulty": "moyen" if avg_score >= 60 else "facile",
                        "preferred_pace": "modéré"
                    },
                    "total_quizzes": len(quiz_results),
                    "analysis_date": datetime.utcnow().isoformat()
                }
            else:
                # Aucun quiz trouvé
                return {
                    "student_id": student_id,
                    "student_name": f"{student.first_name} {student.last_name}" if student.first_name and student.last_name else student.email,
                    "french_level": "A1",
                    "learning_style": "Mixte",
                    "cognitive_profile": {
                        "memory_type": "Mixte",
                        "attention_span": "Moyenne",
                        "problem_solving": "Analytique"
                    },
                    "strengths": [],
                    "areas_for_improvement": ["Commencer par des quiz simples"],
                    "learning_preferences": {
                        "preferred_content_types": ["interactif"],
                        "preferred_difficulty": "facile",
                        "preferred_pace": "lent"
                    },
                    "message": "Aucun quiz complété, profil par défaut créé"
                }
        
        # Si un profil existe, l'utiliser
        print(f"✅ [FRENCH_PROFILE] Profil existant trouvé, utilisation des données réelles")
        
        # Récupérer les compétences et leur progression
        competencies = db.query(FrenchCompetency).all()
        competency_progress = db.query(FrenchCompetencyProgress).filter(
            FrenchCompetencyProgress.student_id == student_id
        ).all()
        
        # Construire les données du profil
        strengths = []
        areas_for_improvement = []
        
        for progress in competency_progress:
            competency = next((c for c in competencies if c.id == progress.competency_id), None)
            if competency:
                mastery_level = progress.progress_percentage / 100.0  # Convertir en décimal
                if mastery_level >= 0.7:  # 70% ou plus = force
                    strengths.append(f"{competency.name} (Niveau: {progress.progress_percentage:.0f}%)")
                elif mastery_level < 0.5:  # Moins de 50% = à améliorer
                    areas_for_improvement.append(f"{competency.name} (Niveau: {progress.progress_percentage:.0f}%)")
        
        # Déterminer le nom d'affichage
        display_name = "Élève sans nom"
        if student.first_name and student.last_name:
            display_name = f"{student.first_name} {student.last_name}"
        elif student.username:
            display_name = student.username
        elif student.email:
            email_name = student.email.split('@')[0]
            display_name = email_name.replace('.', ' ').title()
        
        return {
            "student_id": student_id,
            "student_name": display_name,
            "french_level": profile.french_level or "A1",
            "learning_style": profile.learning_style or "Mixte",
            "cognitive_profile": {
                "memory_type": "Mixte",
                "attention_span": "Moyenne", 
                "problem_solving": "Analytique"
            },
            "strengths": strengths if strengths else ["Performance générale"],
            "areas_for_improvement": areas_for_improvement if areas_for_improvement else ["Aucun axe d'amélioration identifié"],
            "learning_preferences": {
                "preferred_content_types": ["interactif", "visuel"],
                "preferred_difficulty": "moyen",
                "preferred_pace": profile.preferred_pace or "modéré"
            },
            "analysis_date": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ [FRENCH_PROFILE] Erreur: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'analyse du profil français: {str(e)}"
        )

@router.get("/recommendations/student/{student_id}")
async def get_student_recommendations(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les recommandations personnalisées pour l'étudiant (avec auth)"""
    # Cette fonction nécessite une authentification complète
    # Pour les tests, utilisez la version /test
    raise HTTPException(status_code=501, detail="Utilisez l'endpoint /test pour les tests")

@router.get("/recommendations/student/{student_id}/test")
async def get_student_recommendations_test(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Récupérer les recommandations personnalisées pour l'étudiant (version test sans auth)"""
    try:
        print(f"🔍 [FRENCH_RECOMMENDATIONS] Début analyse recommandations pour étudiant {student_id}")
        
        # Vérifier que l'étudiant existe
        student = db.query(User).filter(
            User.id == student_id,
            User.role == UserRole.student
        ).first()
        
        if not student:
            print(f"❌ [FRENCH_RECOMMENDATIONS] Étudiant {student_id} non trouvé")
            raise HTTPException(status_code=404, detail="Étudiant non trouvé")
        
        print(f"✅ [FRENCH_RECOMMENDATIONS] Étudiant trouvé: {student.first_name} {student.last_name}")
        
        # Récupérer le profil et les compétences faibles
        profile = db.query(FrenchLearningProfile).filter(
            FrenchLearningProfile.student_id == student_id
        ).first()
        
        if not profile:
            print(f"⚠️ [FRENCH_RECOMMENDATIONS] Aucun profil français trouvé, génération de recommandations basées sur les quiz")
            # Générer des recommandations basées sur les quiz existants
            from models.quiz import QuizResult
            quiz_results = db.query(QuizResult).filter(
                QuizResult.student_id == student_id,
                QuizResult.is_completed == True
            ).order_by(QuizResult.created_at.desc()).limit(20).all()
            
            if quiz_results:
                avg_score = sum(r.score for r in quiz_results) / len(quiz_results)
                
                recommendations = []
                if avg_score < 60:
                    recommendations.append({
                        "title": "Renforcer les bases",
                        "description": "Votre score moyen est de {:.1f}%. Commencez par des exercices de niveau débutant",
                        "type": "exercice",
                        "subject": "Français",
                        "priority": "high"
                    })
                elif avg_score < 80:
                    recommendations.append({
                        "title": "Améliorer la compréhension",
                        "description": "Votre score moyen est de {:.1f}%. Pratiquez avec des exercices de niveau intermédiaire",
                        "type": "quiz",
                        "subject": "Français",
                        "priority": "medium"
                    })
                
                recommendations.append({
                    "title": "Continuer la pratique",
                    "description": "Vous avez complété {} quiz. Continuez à pratiquer régulièrement",
                    "type": "contenu",
                    "subject": "Français",
                    "priority": "medium"
                })
                
                return {
                    "student_id": student_id,
                    "student_name": f"{student.first_name} {student.last_name}" if student.first_name and student.last_name else student.email,
                    "recommendations": recommendations,
                    "total_quizzes": len(quiz_results),
                    "average_score": round(avg_score, 1),
                    "analysis_date": datetime.utcnow().isoformat()
                }
            else:
                return {
                    "student_id": student_id,
                    "student_name": f"{student.first_name} {student.last_name}" if student.first_name and student.last_name else student.email,
                    "recommendations": [
                        {
                            "title": "Commencer l'apprentissage",
                            "description": "Aucun quiz complété. Commencez par des exercices simples",
                            "type": "exercice",
                            "subject": "Français",
                            "priority": "high"
                        }
                    ],
                    "message": "Aucun quiz complété, recommandations de base"
                }
        
        # Si un profil existe, l'utiliser
        print(f"✅ [FRENCH_RECOMMENDATIONS] Profil existant trouvé, génération de recommandations personnalisées")
        
        # Récupérer les compétences avec progression faible
        competency_progress = db.query(FrenchCompetencyProgress).filter(
            FrenchCompetencyProgress.student_id == student_id,
            FrenchCompetencyProgress.progress_percentage < 60.0  # Moins de 60%
        ).all()
        
        recommendations = []
        
        for progress in competency_progress:
            competency = db.query(FrenchCompetency).filter(
                FrenchCompetency.id == progress.competency_id
            ).first()
            
            if competency:
                mastery_level = progress.progress_percentage / 100.0
                recommendations.append({
                    "title": f"Améliorer {competency.name}",
                    "description": f"Renforcer vos compétences en {competency.name.lower()} (Niveau actuel: {progress.progress_percentage:.0f}%)",
                    "type": competency.category.lower() if competency.category else "général",
                    "subject": "Français",
                    "priority": "high" if mastery_level < 0.3 else "medium"
                })
        
        # Si aucune compétence faible, suggérer des améliorations générales
        if not recommendations:
            recommendations.append({
                "title": "Maintenir l'excellence",
                "description": "Vos compétences sont excellentes. Continuez à pratiquer pour maintenir votre niveau",
                "type": "contenu",
                "subject": "Français",
                "priority": "low"
            })
        
        # Limiter à 6 recommandations maximum
        return {
            "student_id": student_id,
            "student_name": f"{student.first_name} {student.last_name}" if student.first_name and student.last_name else student.email,
            "recommendations": recommendations[:6],
            "analysis_date": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ [FRENCH_RECOMMENDATIONS] Erreur: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la génération des recommandations: {str(e)}"
        )

# Contenu des modules français
FRENCH_MODULE_CONTENT = {
    "A1": {
        "grammar": [
            {
                "name": "Les Articles Définis",
                "content_type": "video",
                "content_data": {
                    "video_url": "/content/french/a1/grammar/articles-definis.mp4",
                    "duration": 15,
                    "description": "Apprenez à utiliser les articles le, la, les, l'"
                },
                "estimated_duration": 20,
                "prerequisites": [],
                "learning_outcomes": ["Identifier les articles", "Utiliser correctement les articles"]
            },
            {
                "name": "Le Verbe Être",
                "content_type": "text",
                "content_data": {
                    "text_content": "Le verbe être est le verbe le plus important en français...",
                    "examples": ["Je suis", "Tu es", "Il/Elle est"],
                    "exercises": ["Conjuguer être au présent", "Compléter des phrases"]
                },
                "estimated_duration": 25,
                "prerequisites": ["Les Articles Définis"],
                "learning_outcomes": ["Conjuguer être", "Former des phrases simples"]
            }
        ],
        "vocabulary": [
            {
                "name": "Les Salutations",
                "content_type": "interactive",
                "content_data": {
                    "words": ["Bonjour", "Au revoir", "Merci", "S'il vous plaît"],
                    "pronunciation": "/audio/french/a1/vocabulary/salutations.mp3",
                    "exercises": ["Associer mots et images", "Pratiquer la prononciation"]
                },
                "estimated_duration": 30,
                "prerequisites": [],
                "learning_outcomes": ["Connaître les salutations", "Prononcer correctement"]
            }
        ]
    },
    "A2": {
        "grammar": [
            {
                "name": "Le Passé Composé",
                "content_type": "video",
                "content_data": {
                    "video_url": "/content/french/a2/grammar/passe-compose.mp4",
                    "duration": 20,
                    "description": "Maîtrisez le passé composé avec avoir et être"
                },
                "estimated_duration": 35,
                "prerequisites": ["Le Verbe Être", "Les Articles Définis"],
                "learning_outcomes": ["Former le passé composé", "Utiliser avoir et être"]
            }
        ],
        "vocabulary": [
            {
                "name": "La Famille",
                "content_type": "interactive",
                "content_data": {
                    "words": ["Père", "Mère", "Frère", "Sœur", "Grand-père", "Grand-mère"],
                    "pronunciation": "/audio/french/a2/vocabulary/famille.mp3",
                    "exercises": ["Arbre généalogique", "Décrire sa famille"]
                },
                "estimated_duration": 40,
                "prerequisites": ["Les Salutations"],
                "learning_outcomes": ["Nommer les membres de la famille", "Décrire des relations"]
            }
        ]
    }
}

@router.post("/learning-paths/generate")
async def generate_french_learning_path(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Génère un parcours d'apprentissage français personnalisé pour un étudiant"""
    try:
        # Vérifier que l'étudiant existe
        student = db.query(User).filter(
            User.id == student_id,
            User.role == UserRole.student
        ).first()
        
        if not student:
            raise HTTPException(status_code=404, detail="Étudiant non trouvé")
        
        # Récupérer le profil d'apprentissage français
        profile = db.query(FrenchLearningProfile).filter(
            FrenchLearningProfile.student_id == student_id
        ).first()
        
        if not profile:
            raise HTTPException(
                status_code=400, 
                detail="L'étudiant doit d'abord passer l'évaluation initiale française"
            )
        
        # Vérifier s'il y a déjà un parcours actif
        existing_path = db.query(FrenchLearningPath).filter(
            FrenchLearningPath.student_id == student_id,
            FrenchLearningPath.status == "active"
        ).first()
        
        if existing_path:
            raise HTTPException(
                status_code=400, 
                detail="Un parcours d'apprentissage français est déjà actif pour cet étudiant"
            )
        
        # Déterminer le niveau et la difficulté
        french_level = profile.french_level
        preferred_pace = profile.preferred_pace
        
        # Calculer la durée estimée selon le rythme préféré
        pace_multiplier = {
            "lent": 1.5,
            "moyen": 1.0,
            "rapide": 0.7
        }.get(preferred_pace, 1.0)
        
        # Créer le parcours d'apprentissage
        learning_path = FrenchLearningPath(
            student_id=student_id,
            path_name=f"Parcours Français {french_level} - {preferred_pace.capitalize()}",
            total_modules=len(FRENCH_MODULE_CONTENT[french_level]["grammar"]) + len(FRENCH_MODULE_CONTENT[french_level]["vocabulary"]),
            difficulty_level=french_level,
            learning_objectives=json.dumps([
                "Maîtriser les bases grammaticales",
                "Acquérir un vocabulaire essentiel",
                "Développer la compréhension orale et écrite"
            ])
        )
        
        db.add(learning_path)
        db.commit()
        db.refresh(learning_path)
        
        # Créer les modules d'apprentissage
        modules_created = []
        module_order = 1
        
        # Ajouter les modules de grammaire
        for grammar_module in FRENCH_MODULE_CONTENT[french_level]["grammar"]:
            module = FrenchLearningModule(
                path_id=learning_path.id,
                module_name=grammar_module["name"],
                module_order=module_order,
                difficulty_level=french_level,
                estimated_duration=int(grammar_module["estimated_duration"] * pace_multiplier),
                content_type=grammar_module["content_type"],
                content_data=json.dumps(grammar_module["content_data"]),
                prerequisites=json.dumps(grammar_module["prerequisites"]),
                learning_outcomes=json.dumps(grammar_module["learning_outcomes"])
            )
            db.add(module)
            modules_created.append(module)
            module_order += 1
        
        # Ajouter les modules de vocabulaire
        for vocab_module in FRENCH_MODULE_CONTENT[french_level]["vocabulary"]:
            module = FrenchLearningModule(
                path_id=learning_path.id,
                module_name=vocab_module["name"],
                module_order=module_order,
                difficulty_level=french_level,
                estimated_duration=int(vocab_module["estimated_duration"] * pace_multiplier),
                content_type=vocab_module["content_type"],
                content_data=json.dumps(vocab_module["content_data"]),
                prerequisites=json.dumps(vocab_module["prerequisites"]),
                learning_outcomes=json.dumps(vocab_module["learning_outcomes"])
            )
            db.add(module)
            modules_created.append(module)
            module_order += 1
        
        db.commit()
        
        return {
            "path_id": learning_path.id,
            "path_name": learning_path.path_name,
            "total_modules": learning_path.total_modules,
            "estimated_duration": sum(m.estimated_duration for m in modules_created),
            "modules": [
                {
                    "id": m.id,
                    "name": m.module_name,
                    "order": m.module_order,
                    "duration": m.estimated_duration,
                    "content_type": m.content_type
                }
                for m in modules_created
            ],
            "message": "Parcours d'apprentissage français généré avec succès"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la génération du parcours : {str(e)}"
        )

@router.get("/learning-paths/student/{student_id}")
async def get_student_french_learning_path(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupère le parcours d'apprentissage français d'un étudiant"""
    try:
        # Vérifier l'autorisation
        if current_user.role not in [UserRole.teacher, UserRole.admin] and current_user.id != student_id:
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        # Récupérer le parcours actif
        learning_path = db.query(FrenchLearningPath).filter(
            FrenchLearningPath.student_id == student_id,
            FrenchLearningPath.status == "active"
        ).first()
        
        if not learning_path:
            return {
                "message": "Aucun parcours d'apprentissage français actif",
                "has_path": False
            }
        
        # Récupérer les modules avec leur contenu
        modules = db.query(FrenchLearningModule).filter(
            FrenchLearningModule.path_id == learning_path.id
        ).order_by(FrenchLearningModule.module_order).all()
        
        return {
            "has_path": True,
            "path": {
                "id": learning_path.id,
                "name": learning_path.path_name,
                "current_module": learning_path.current_module,
                "total_modules": learning_path.total_modules,
                "completion_percentage": learning_path.completion_percentage,
                "difficulty_level": learning_path.difficulty_level,
                "status": learning_path.status,
                "created_at": learning_path.created_at
            },
            "modules": [
                {
                    "id": m.id,
                    "name": m.module_name,
                    "order": m.module_order,
                    "duration": m.estimated_duration,
                    "content_type": m.content_type,
                    "content_data": json.loads(m.content_data) if m.content_data else {},
                    "prerequisites": json.loads(m.prerequisites) if m.prerequisites else [],
                    "learning_outcomes": json.loads(m.learning_outcomes) if m.learning_outcomes else [],
                    "is_completed": m.module_order < learning_path.current_module,
                    "is_current": m.module_order == learning_path.current_module
                }
                for m in modules
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération du parcours : {str(e)}"
        )

@router.post("/learning-paths/{path_id}/complete-module")
async def complete_french_module(
    path_id: int,
    module_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Marque un module comme terminé et passe au suivant"""
    try:
        # Récupérer le parcours
        learning_path = db.query(FrenchLearningPath).filter(
            FrenchLearningPath.id == path_id
        ).first()
        
        if not learning_path:
            raise HTTPException(status_code=404, detail="Parcours non trouvé")
        
        # Vérifier l'autorisation
        if current_user.role not in [UserRole.teacher, UserRole.admin] and current_user.id != learning_path.student_id:
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        # Vérifier que le module est le module actuel
        if learning_path.current_module != module_id:
            raise HTTPException(
                status_code=400, 
                detail="Ce module n'est pas le module actuel du parcours"
            )
        
        # Marquer le module comme terminé
        learning_path.current_module += 1
        
        # Calculer le pourcentage de progression
        learning_path.completion_percentage = (learning_path.current_module - 1) / learning_path.total_modules * 100
        
        # Vérifier si le parcours est terminé
        if learning_path.current_module > learning_path.total_modules:
            learning_path.status = "completed"
            learning_path.completion_percentage = 100.0
        
        db.commit()
        
        return {
            "path_id": path_id,
            "module_completed": module_id,
            "new_current_module": learning_path.current_module,
            "completion_percentage": learning_path.completion_percentage,
            "status": learning_path.status,
            "message": "Module terminé avec succès"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la finalisation du module : {str(e)}"
        )

@router.get("/learning-paths/teacher/{teacher_id}/overview")
async def get_teacher_french_learning_overview(
    teacher_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Vue d'ensemble des parcours français pour un professeur"""
    try:
        # Vérifier l'autorisation
        if current_user.id != teacher_id and current_user.role != UserRole.admin:
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        # Récupérer tous les parcours français actifs
        active_paths = db.query(FrenchLearningPath).filter(
            FrenchLearningPath.status == "active"
        ).all()
        
        overview_data = []
        total_students = 0
        total_completion = 0
        
        for path in active_paths:
            # Récupérer les informations de l'étudiant
            student = db.query(User).filter(User.id == path.student_id).first()
            
            overview_data.append({
                "student_id": path.student_id,
                "student_name": f"{student.first_name or ''} {student.last_name or ''}".strip() or student.email,
                "path_name": path.path_name,
                "current_module": path.current_module,
                "total_modules": path.total_modules,
                "completion_percentage": path.completion_percentage,
                "difficulty_level": path.difficulty_level,
                "created_at": path.created_at
            })
            
            total_students += 1
            total_completion += path.completion_percentage
        
        average_completion = total_completion / total_students if total_students > 0 else 0
        
        return {
            "total_active_paths": total_students,
            "average_completion": round(average_completion, 2),
            "paths": overview_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération de la vue d'ensemble : {str(e)}"
        )
