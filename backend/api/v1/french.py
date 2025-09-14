from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json
import random

from database import get_db
from models.user import User
from models.quiz import Quiz, QuizResult
from models.learning_history import LearningHistory
from core.security import get_current_user

router = APIRouter(prefix="/api/v1/french", tags=["French Assessment"])

# ============================================================================
# DONNÉES MOCKÉES POUR L'ÉVALUATION INITIALE FRANÇAISE
# ============================================================================

FRENCH_QUESTIONS = [
    {
        "id": "french_1",
        "question": "Quel est l'article correct ? '____ chat'",
        "options": ["Le", "La", "Les", "L'"],
        "correct": "Le",
        "difficulty": "easy",
        "explanation": "Le mot 'chat' est masculin, donc on utilise l'article 'Le'.",
        "category": "grammar",
        "cognitive_domain": "comprehension"
    },
    {
        "id": "french_2",
        "question": "Conjuguez le verbe 'être' à la première personne du singulier au présent : 'Je ____ étudiant'",
        "options": ["suis", "es", "est", "sont"],
        "correct": "suis",
        "difficulty": "easy",
        "explanation": "À la première personne du singulier, 'être' se conjugue 'suis'.",
        "category": "conjugation",
        "cognitive_domain": "memory"
    },
    {
        "id": "french_3",
        "question": "Quel est le pluriel de 'journal' ?",
        "options": ["journaux", "journals", "journales", "journauxs"],
        "correct": "journaux",
        "difficulty": "medium",
        "explanation": "Les mots en 'al' font leur pluriel en 'aux'.",
        "category": "grammar",
        "cognitive_domain": "comprehension"
    },
    {
        "id": "french_4",
        "question": "Complétez : 'Il ____ (aller) au cinéma hier soir'",
        "options": ["va", "vais", "est allé", "allait"],
        "correct": "est allé",
        "difficulty": "medium",
        "explanation": "Pour une action passée terminée, on utilise le passé composé.",
        "category": "grammar",
        "cognitive_domain": "analysis"
    },
    {
        "id": "french_5",
        "question": "Quel est le synonyme de 'rapidement' ?",
        "options": ["lentement", "vite", "doucement", "facilement"],
        "correct": "vite",
        "difficulty": "easy",
        "explanation": "'Rapidement' et 'vite' expriment la même idée de vitesse.",
        "category": "vocabulary",
        "cognitive_domain": "comprehension"
    },
    {
        "id": "french_6",
        "question": "Identifiez l'adjectif dans : 'La belle maison rouge'",
        "options": ["La", "belle", "maison", "rouge"],
        "correct": "belle",
        "difficulty": "easy",
        "explanation": "'Belle' est un adjectif qualificatif qui qualifie 'maison'.",
        "category": "grammar",
        "cognitive_domain": "analysis"
    },
    {
        "id": "french_7",
        "question": "Quel temps utiliser pour exprimer une habitude ?",
        "options": ["passé composé", "imparfait", "futur simple", "conditionnel"],
        "correct": "imparfait",
        "difficulty": "medium",
        "explanation": "L'imparfait exprime les habitudes et actions répétées dans le passé.",
        "category": "grammar",
        "cognitive_domain": "comprehension"
    },
    {
        "id": "french_8",
        "question": "Complétez : 'Si j'____ (avoir) le temps, je ____ (aller) au musée'",
        "options": ["avais, irais", "ai, vais", "aurais, irai", "avais, vais"],
        "correct": "avais, irais",
        "difficulty": "hard",
        "explanation": "C'est une phrase conditionnelle avec l'imparfait + conditionnel.",
        "category": "grammar",
        "cognitive_domain": "analysis"
    },
    {
        "id": "french_9",
        "question": "Quel est le genre du mot 'voiture' ?",
        "options": ["masculin", "féminin", "neutre", "variable"],
        "correct": "féminin",
        "difficulty": "easy",
        "explanation": "Le mot 'voiture' est féminin, on dit 'une voiture'.",
        "category": "grammar",
        "cognitive_domain": "memory"
    },
    {
        "id": "french_10",
        "question": "Identifiez la fonction de 'très' dans : 'Il est très intelligent'",
        "options": ["adverbe", "adjectif", "nom", "préposition"],
        "correct": "adverbe",
        "difficulty": "medium",
        "explanation": "'Très' est un adverbe d'intensité qui modifie l'adjectif 'intelligent'.",
        "category": "grammar",
        "cognitive_domain": "analysis"
    }
]

# ============================================================================
# ENDPOINTS POUR L'ÉVALUATION INITIALE
# ============================================================================

@router.post("/initial-assessment/start")
async def start_french_assessment(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Démarrer l'évaluation initiale française"""
    try:
        if current_user.role.value != "student":
            raise HTTPException(status_code=403, detail="Seuls les étudiants peuvent passer l'évaluation")
        
        # Créer une session d'évaluation
        test_id = f"french_test_{current_user.id}_{int(datetime.now().timestamp())}"
        
        # Sélectionner la première question
        first_question = random.choice(FRENCH_QUESTIONS)
        
        # Créer le progrès initial
        progress = {
            "current": 1,
            "total": len(FRENCH_QUESTIONS),
            "difficulty": "easy",
            "score": 0,
            "questions_answered": 0
        }
        
        return {
            "status": "started",
            "test_id": test_id,
            "current_question": first_question,
            "progress": progress,
            "message": "Évaluation française démarrée avec succès"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors du démarrage de l'évaluation: {str(e)}"
        )

@router.post("/initial-assessment/{test_id}/submit")
async def submit_french_answer(
    test_id: str,
    answer_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Soumettre une réponse à l'évaluation française"""
    try:
        if current_user.role.value != "student":
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        answer = answer_data.get("answer")
        is_correct = answer_data.get("is_correct", False)
        question_difficulty = answer_data.get("question_difficulty", "easy")
        
        if not answer:
            raise HTTPException(status_code=400, detail="Réponse manquante")
        
        # Simuler le traitement de la réponse
        # En réalité, on stockerait cela en base de données
        
        # Déterminer la prochaine question basée sur la performance
        current_question_index = 1  # À adapter selon la logique réelle
        
        if current_question_index < len(FRENCH_QUESTIONS):
            # Il reste des questions
            next_question = FRENCH_QUESTIONS[current_question_index]
            
            # Mettre à jour le progrès
            progress = {
                "current": current_question_index + 1,
                "total": len(FRENCH_QUESTIONS),
                "difficulty": "medium" if is_correct else "easy",
                "score": 100 if is_correct else 0,
                "questions_answered": current_question_index
            }
            
            return {
                "status": "in_progress",
                "next_question": next_question,
                "progress": progress,
                "feedback": "Réponse traitée avec succès"
            }
        else:
            # Test terminé
            final_score = 85  # Score simulé
            
            # Générer le profil d'apprentissage
            learning_profile = {
                "level": "A1" if final_score < 60 else "A2" if final_score < 80 else "B1",
                "strengths": ["motivation", "persévérance"] if final_score > 70 else ["motivation"],
                "weaknesses": ["grammaire", "vocabulaire"] if final_score < 80 else ["grammaire"],
                "learning_style": "auditif",
                "cognitive_profile": {
                    "memory_type": "visual",
                    "attention_span": "medium",
                    "problem_solving": "analytical"
                }
            }
            
            return {
                "status": "completed",
                "final_score": final_score,
                "learning_profile": learning_profile,
                "message": "Évaluation française terminée avec succès"
            }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la soumission: {str(e)}"
        )

@router.get("/initial-assessment/{test_id}/questions")
async def get_french_question(
    test_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Récupérer la question actuelle de l'évaluation française"""
    try:
        if current_user.role.value != "student":
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        # Retourner une question aléatoire pour la démo
        question = random.choice(FRENCH_QUESTIONS)
        
        progress = {
            "current": 1,
            "total": len(FRENCH_QUESTIONS),
            "difficulty": "easy",
            "score": 0,
            "questions_answered": 0
        }
        
        return {
            "question": question,
            "progress": progress
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération de la question: {str(e)}"
        )

@router.get("/initial-assessment/{test_id}/results")
async def get_french_assessment_results(
    test_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Récupérer les résultats de l'évaluation française"""
    try:
        if current_user.role.value != "student":
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        # Résultats simulés
        results = {
            "test_id": test_id,
            "student_id": current_user.id,
            "final_score": 85,
            "level": "A2",
            "strengths": ["motivation", "persévérance"],
            "weaknesses": ["grammaire", "vocabulaire"],
            "learning_style": "auditif",
            "cognitive_profile": {
                "memory_type": "visual",
                "attention_span": "medium",
                "problem_solving": "analytical"
            },
            "completed_at": datetime.now().isoformat()
        }
        
        return {
            "status": "success",
            "data": results
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des résultats: {str(e)}"
        )

# ============================================================================
# ENDPOINTS POUR LA BANQUE DE QUESTIONS
# ============================================================================

@router.get("/questions")
async def get_french_questions(
    difficulty: Optional[str] = None,
    category: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Récupérer les questions françaises disponibles"""
    try:
        questions = FRENCH_QUESTIONS.copy()
        
        # Filtrer par difficulté si spécifiée
        if difficulty:
            questions = [q for q in questions if q["difficulty"] == difficulty]
        
        # Filtrer par catégorie si spécifiée
        if category:
            questions = [q for q in questions if q["category"] == category]
        
        return {
            "status": "success",
            "data": {
                "questions": questions,
                "total": len(questions),
                "filters": {
                    "difficulty": difficulty,
                    "category": category
                }
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des questions: {str(e)}"
        )

@router.get("/questions/{question_id}")
async def get_french_question_by_id(
    question_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Récupérer une question française spécifique"""
    try:
        question = next((q for q in FRENCH_QUESTIONS if q["id"] == question_id), None)
        
        if not question:
            raise HTTPException(status_code=404, detail="Question non trouvée")
        
        return {
            "status": "success",
            "data": question
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération de la question: {str(e)}"
        )
