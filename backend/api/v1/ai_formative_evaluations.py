from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import openai
import json
import re
from pydantic import BaseModel

from core.database import get_db
from core.security import get_current_user
from models.user import User
from api.v1.auth import require_role

router = APIRouter(prefix="/ai-formative-evaluations", tags=["ai-formative-evaluations"])

# ============================================================================
# MODÈLES DE DONNÉES
# ============================================================================

class FormativeEvaluationRequest(BaseModel):
    title: str
    subject: str
    assessment_type: str  # 'project', 'presentation', 'discussion', 'portfolio', 'observation', 'self_evaluation'
    description: str
    target_level: str  # 'beginner', 'intermediate', 'advanced'
    duration_minutes: int
    max_students: int
    learning_objectives: List[str]
    custom_requirements: Optional[str] = None

class AIGeneratedEvaluation(BaseModel):
    title: str
    description: str
    assessment_type: str
    criteria: List[Dict[str, Any]]
    rubric: Dict[str, Dict[str, str]]
    questions: List[Dict[str, Any]]
    instructions: str
    estimated_duration: int
    difficulty_level: str
    success_indicators: List[str]

# ============================================================================
# PROMPTS IA PRÉ-DÉFINIS
# ============================================================================

FORMATIVE_EVALUATION_PROMPTS = {
    "project": """
    Crée une évaluation formative pour un projet de recherche avec les éléments suivants:
    - Titre accrocheur et descriptif
    - Description détaillée des objectifs
    - 5-7 critères d'évaluation clairs et mesurables
    - Grille de notation avec 4 niveaux (Excellent, Bon, Satisfaisant, À améliorer)
    - 3-5 questions d'évaluation pertinentes
    - Instructions détaillées pour les étudiants
    - Indicateurs de réussite concrets
    """,
    
    "presentation": """
    Crée une évaluation formative pour une présentation orale avec:
    - Titre engageant
    - Description des compétences à évaluer
    - Critères d'évaluation orale (clarté, structure, support visuel, etc.)
    - Grille de notation adaptée aux présentations
    - Questions d'auto-évaluation
    - Instructions pour la préparation
    - Indicateurs de performance orale
    """,
    
    "discussion": """
    Crée une évaluation formative pour une discussion critique avec:
    - Titre stimulant la réflexion
    - Description des objectifs de discussion
    - Critères d'évaluation de la participation et de la réflexion
    - Grille de notation pour les discussions
    - Questions de réflexion post-discussion
    - Instructions pour la participation active
    - Indicateurs de qualité de la discussion
    """,
    
    "portfolio": """
    Crée une évaluation formative pour un portfolio avec:
    - Titre valorisant le travail personnel
    - Description des objectifs du portfolio
    - Critères d'évaluation de la diversité et de la progression
    - Grille de notation pour les portfolios
    - Questions de réflexion personnelle
    - Instructions pour la constitution du portfolio
    - Indicateurs de développement des compétences
    """,
    
    "observation": """
    Crée une évaluation formative pour une observation participante avec:
    - Titre encourageant l'observation
    - Description des compétences d'observation
    - Critères d'évaluation de l'observation et de l'analyse
    - Grille de notation pour les observations
    - Questions d'analyse post-observation
    - Instructions pour l'observation structurée
    - Indicateurs de qualité de l'observation
    """,
    
    "self_evaluation": """
    Crée une évaluation formative pour une auto-évaluation avec:
    - Titre encourageant la réflexivité
    - Description des objectifs d'auto-évaluation
    - Critères d'évaluation de la réflexivité et de l'honnêteté
    - Grille de notation pour l'auto-évaluation
    - Questions de réflexion personnelle
    - Instructions pour l'auto-évaluation
    - Indicateurs de qualité de la réflexion
    """
}

# ============================================================================
# ENDPOINTS PRINCIPAUX
# ============================================================================

@router.post("/generate-evaluation/")
async def generate_formative_evaluation_with_ai(
    request: FormativeEvaluationRequest,
    current_user: User = Depends(require_role(['teacher', 'admin'])),
    db: Session = Depends(get_db)
):
    """
    Génère une évaluation formative complète avec l'IA
    """
    try:
        print(f"[AI] Génération d'évaluation formative pour {current_user.email}")
        print(f"[AI] Type: {request.assessment_type}, Matière: {request.subject}")
        
        # Construire le prompt personnalisé
        base_prompt = FORMATIVE_EVALUATION_PROMPTS.get(request.assessment_type, "")
        if not base_prompt:
            raise HTTPException(
                status_code=400,
                detail=f"Type d'évaluation non supporté: {request.assessment_type}"
            )
        
        # Prompt personnalisé avec les détails de l'utilisateur
        personalized_prompt = f"""
        {base_prompt}
        
        CONTEXTE SPÉCIFIQUE:
        - Matière: {request.subject}
        - Niveau cible: {request.target_level}
        - Durée estimée: {request.duration_minutes} minutes
        - Nombre d'étudiants max: {request.max_students}
        - Objectifs d'apprentissage: {', '.join(request.learning_objectives)}
        - Exigences personnalisées: {request.custom_requirements or 'Aucune'}
        
        FORMAT DE RÉPONSE ATTENDU (JSON):
        {{
            "title": "Titre de l'évaluation",
            "description": "Description détaillée",
            "assessment_type": "{request.assessment_type}",
            "criteria": [
                {{
                    "name": "Nom du critère",
                    "description": "Description du critère",
                    "weight": 20,
                    "max_points": 4
                }}
            ],
            "rubric": {{
                "excellent": {{
                    "points": 4,
                    "description": "Description du niveau excellent"
                }},
                "good": {{
                    "points": 3,
                    "description": "Description du niveau bon"
                }},
                "satisfactory": {{
                    "points": 2,
                    "description": "Description du niveau satisfaisant"
                }},
                "needs_improvement": {{
                    "points": 1,
                    "description": "Description du niveau à améliorer"
                }}
            }},
            "questions": [
                {{
                    "question": "Question d'évaluation",
                    "type": "reflection",
                    "max_points": 5
                }}
            ],
            "instructions": "Instructions détaillées pour les étudiants",
            "estimated_duration": {request.duration_minutes},
            "difficulty_level": "{request.target_level}",
            "success_indicators": [
                "Indicateur de réussite 1",
                "Indicateur de réussite 2"
            ]
        }}
        
        IMPORTANT: Retourne UNIQUEMENT le JSON valide, sans texte supplémentaire.
        """
        
        # Appel à l'IA (simulation pour l'instant)
        ai_response = await simulate_ai_generation(personalized_prompt, request)
        
        # Valider et formater la réponse
        formatted_evaluation = format_ai_response(ai_response, request)
        
        print(f"[AI] Évaluation générée avec succès: {formatted_evaluation['title']}")
        
        return {
            "success": True,
            "evaluation": formatted_evaluation,
            "generated_at": datetime.now().isoformat(),
            "ai_model_used": "GPT-4 (simulation)",
            "teacher_id": current_user.id
        }
        
    except Exception as e:
        print(f"[AI] Erreur lors de la génération: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la génération de l'évaluation: {str(e)}"
        )

@router.post("/enhance-existing-evaluation/")
async def enhance_existing_evaluation_with_ai(
    evaluation_data: Dict[str, Any],
    enhancement_type: str = Body(...),  # 'criteria', 'rubric', 'questions', 'instructions'
    current_user: User = Depends(require_role(['teacher', 'admin'])),
    db: Session = Depends(get_db)
):
    """
    Améliore une évaluation formative existante avec l'IA
    """
    try:
        print(f"[AI] Amélioration d'évaluation existante pour {current_user.email}")
        print(f"[AI] Type d'amélioration: {enhancement_type}")
        
        # Construire le prompt d'amélioration
        enhancement_prompt = build_enhancement_prompt(evaluation_data, enhancement_type)
        
        # Appel à l'IA pour l'amélioration
        enhanced_content = await simulate_ai_enhancement(enhancement_prompt, enhancement_type)
        
        return {
            "success": True,
            "enhanced_content": enhanced_content,
            "enhancement_type": enhancement_type,
            "enhanced_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"[AI] Erreur lors de l'amélioration: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'amélioration: {str(e)}"
        )

# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

async def simulate_ai_generation(prompt: str, request: FormativeEvaluationRequest) -> Dict[str, Any]:
    """
    Simule la génération IA (à remplacer par un vrai appel OpenAI)
    """
    print(f"[AI] Simulation de génération avec prompt: {prompt[:200]}...")
    
    # Simulation d'une réponse IA
    if request.assessment_type == "project":
        return {
            "title": f"Projet de Recherche - {request.subject}",
            "description": f"Évaluation formative pour un projet de recherche en {request.subject} permettant aux étudiants de développer leurs compétences de recherche et d'analyse.",
            "assessment_type": request.assessment_type,
            "criteria": [
                {
                    "name": "Qualité de la recherche",
                    "description": "Pertinence et diversité des sources consultées",
                    "weight": 25,
                    "max_points": 4
                },
                {
                    "name": "Méthodologie",
                    "description": "Clarté et cohérence de l'approche méthodologique",
                    "weight": 25,
                    "max_points": 4
                },
                {
                    "name": "Analyse critique",
                    "description": "Profondeur de l'analyse et qualité des arguments",
                    "weight": 30,
                    "max_points": 4
                },
                {
                    "name": "Présentation",
                    "description": "Clarté de la présentation et qualité du support visuel",
                    "weight": 20,
                    "max_points": 4
                }
            ],
            "rubric": {
                "excellent": {
                    "points": 4,
                    "description": "Travail exceptionnel démontrant une maîtrise approfondie du sujet"
                },
                "good": {
                    "points": 3,
                    "description": "Travail de qualité avec une bonne compréhension du sujet"
                },
                "satisfactory": {
                    "points": 2,
                    "description": "Travail acceptable avec une compréhension de base"
                },
                "needs_improvement": {
                    "points": 1,
                    "description": "Travail nécessitant des améliorations significatives"
                }
            },
            "questions": [
                {
                    "question": "Quelle est la question de recherche principale de votre projet ?",
                    "type": "reflection",
                    "max_points": 5
                },
                {
                    "question": "Comment avez-vous sélectionné vos sources de recherche ?",
                    "type": "methodology",
                    "max_points": 5
                },
                {
                    "question": "Quels sont les principaux défis que vous avez rencontrés ?",
                    "type": "reflection",
                    "max_points": 5
                }
            ],
            "instructions": f"""
            Instructions pour le projet de recherche en {request.subject}:
            
            1. Choisissez un sujet spécifique et pertinent
            2. Effectuez une recherche documentaire approfondie
            3. Développez une méthodologie claire
            4. Présentez vos résultats de manière structurée
            5. Incluez une analyse critique de vos sources
            6. Préparez une présentation orale de 10-15 minutes
            
            Durée estimée: {request.duration_minutes} minutes
            Date de remise: À définir avec votre enseignant
            """,
            "estimated_duration": request.duration_minutes,
            "difficulty_level": request.target_level,
            "success_indicators": [
                "Sujet de recherche clairement défini",
                "Sources variées et pertinentes consultées",
                "Méthodologie bien structurée",
                "Analyse critique développée",
                "Présentation claire et engageante"
            ]
        }
    
    # Ajouter d'autres types d'évaluations ici...
    return {}

def format_ai_response(ai_response: Dict[str, Any], request: FormativeEvaluationRequest) -> Dict[str, Any]:
    """
    Formate et valide la réponse de l'IA
    """
    # Validation basique
    required_fields = ["title", "description", "criteria", "rubric", "questions"]
    for field in required_fields:
        if field not in ai_response:
            raise ValueError(f"Champ manquant dans la réponse IA: {field}")
    
    # Ajouter des métadonnées
    ai_response["created_at"] = datetime.now().isoformat()
    ai_response["ai_generated"] = True
    
    return ai_response

def build_enhancement_prompt(evaluation_data: Dict[str, Any], enhancement_type: str) -> str:
    """
    Construit un prompt pour améliorer une évaluation existante
    """
    base_evaluation = evaluation_data.get("description", "")
    
    enhancement_prompts = {
        "criteria": f"Améliore les critères d'évaluation de cette évaluation: {base_evaluation}",
        "rubric": f"Crée une grille de notation plus détaillée pour: {base_evaluation}",
        "questions": f"Génère des questions d'évaluation supplémentaires pour: {base_evaluation}",
        "instructions": f"Améliore les instructions pour cette évaluation: {base_evaluation}"
    }
    
    return enhancement_prompts.get(enhancement_type, "Améliore cette évaluation")

async def simulate_ai_enhancement(prompt: str, enhancement_type: str) -> Dict[str, Any]:
    """
    Simule l'amélioration IA (à remplacer par un vrai appel OpenAI)
    """
    print(f"[AI] Simulation d'amélioration: {enhancement_type}")
    
    # Retourner du contenu amélioré simulé
    return {
        "enhanced_content": f"Contenu amélioré pour {enhancement_type}",
        "improvements": ["Amélioration 1", "Amélioration 2"],
        "suggestions": ["Suggestion 1", "Suggestion 2"]
    }

# ============================================================================
# ENDPOINTS DE TEST ET DIAGNOSTIC
# ============================================================================

@router.get("/test/")
async def test_ai_endpoint():
    """
    Test simple pour vérifier que l'endpoint fonctionne
    """
    return {
        "message": "Module IA pour évaluations formatives accessible",
        "status": "ok",
        "available_types": list(FORMATIVE_EVALUATION_PROMPTS.keys()),
        "timestamp": datetime.now().isoformat()
    }

@router.get("/available-types/")
async def get_available_assessment_types():
    """
    Retourne les types d'évaluations supportés par l'IA
    """
    return {
        "assessment_types": [
            {
                "type": "project",
                "name": "Projet de Recherche",
                "description": "Travail de recherche individuel ou en groupe",
                "best_for": ["Recherche", "Analyse", "Méthodologie"]
            },
            {
                "type": "presentation",
                "name": "Présentation Orale",
                "description": "Exposé oral devant la classe",
                "best_for": ["Expression orale", "Confiance en soi", "Communication"]
            },
            {
                "type": "discussion",
                "name": "Discussion Critique",
                "description": "Débat et analyse critique en groupe",
                "best_for": ["Esprit critique", "Collaboration", "Réflexion"]
            },
            {
                "type": "portfolio",
                "name": "Portfolio",
                "description": "Collection de travaux et réflexions",
                "best_for": ["Progression", "Réflexion personnelle", "Diversité"]
            },
            {
                "type": "observation",
                "name": "Observation Participante",
                "description": "Observation et analyse de situations",
                "best_for": ["Observation", "Analyse", "Réflexion"]
            },
            {
                "type": "self_evaluation",
                "name": "Auto-évaluation",
                "description": "Évaluation de ses propres compétences",
                "best_for": ["Réflexivité", "Conscience de soi", "Développement"]
            }
        ]
    }
