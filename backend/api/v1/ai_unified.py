from fastapi import APIRouter, HTTPException, Depends, Body
from pydantic import BaseModel
from typing import Dict, Optional, List
from services.unified_ai_service import UnifiedAIService
from api.v1.auth import get_current_user, get_db
from models.user import User
from models.quiz import Quiz, QuizResult, Question
from models.learning_path import LearningPath
from sqlalchemy.orm import Session
from sqlalchemy import func
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class ComprehensiveAnalysisRequest(BaseModel):
    student_id: int
    include_deep_learning: bool = True
    include_cognitive_diagnostic: bool = True
    include_performance_prediction: bool = True
    include_content_generation: bool = True

class RealTimeAdaptationRequest(BaseModel):
    student_response: str
    current_difficulty: str
    topic: str
    quiz_id: Optional[int] = None

class VirtualTutorRequest(BaseModel):
    student_question: str
    student_context: Dict
    quiz_id: Optional[int] = None

@router.post("/comprehensive-analysis")
async def comprehensive_ai_analysis(
    request: ComprehensiveAnalysisRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Analyse AI complète d'un étudiant avec toutes les fonctionnalités.
    """
    try:
        # Récupérer les données de l'étudiant depuis la base de données
        student_data = _get_student_data_from_db(db, request.student_id)
        
        # Initialiser le service unifié
        unified_service = UnifiedAIService()
        
        # Effectuer l'analyse complète
        analysis_result = unified_service.comprehensive_ai_analysis(student_data)
        
        # Sauvegarder les résultats dans la base de données
        _save_analysis_results_to_db(db, request.student_id, analysis_result)
        
        return {
            "success": True,
            "analysis": analysis_result,
            "student_id": request.student_id,
            "generated_by": "UnifiedAIService"
        }
        
    except Exception as e:
        logger.error(f"Erreur analyse complète: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'analyse: {str(e)}")

@router.post("/real-time-adaptation")
async def real_time_adaptation(
    request: RealTimeAdaptationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Adaptation en temps réel basée sur la réponse de l'étudiant.
    """
    try:
        unified_service = UnifiedAIService()
        
        # Adaptation en temps réel
        adaptation_result = unified_service.real_time_adaptation(
            student_response=request.student_response,
            current_difficulty=request.current_difficulty,
            topic=request.topic
        )
        
        # Si un quiz_id est fourni, sauvegarder l'adaptation
        if request.quiz_id:
            _save_adaptation_to_db(db, request.quiz_id, adaptation_result)
        
        return {
            "success": True,
            "adaptation": adaptation_result,
            "topic": request.topic,
            "generated_by": "UnifiedAIService"
        }
        
    except Exception as e:
        logger.error(f"Erreur adaptation temps réel: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'adaptation: {str(e)}")

@router.post("/virtual-tutor")
async def virtual_tutor(
    request: VirtualTutorRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Tuteur virtuel avec contexte de l'étudiant.
    """
    try:
        unified_service = UnifiedAIService()
        
        # Obtenir la réponse du tuteur
        tutor_result = unified_service.virtual_tutor(
            student_question=request.student_question,
            student_context=request.student_context
        )
        
        # Sauvegarder l'interaction si un quiz_id est fourni
        if request.quiz_id:
            _save_tutor_interaction_to_db(db, request.quiz_id, request.student_question, tutor_result)
        
        return {
            "success": True,
            "tutor_response": tutor_result,
            "generated_by": "UnifiedAIService"
        }
        
    except Exception as e:
        logger.error(f"Erreur tuteur virtuel: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération de réponse: {str(e)}")

@router.post("/deep-learning-analysis")
async def deep_learning_analysis(
    student_id: int = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Analyse Deep Learning des performances de l'étudiant.
    """
    try:
        # Récupérer les données d'apprentissage
        learning_data = _get_learning_data_from_db(db, student_id)
        
        unified_service = UnifiedAIService()
        
        # Analyse Deep Learning
        dl_result = unified_service.deep_learning_analysis(learning_data)
        
        return {
            "success": True,
            "deep_learning_analysis": dl_result,
            "student_id": student_id,
            "generated_by": "UnifiedAIService"
        }
        
    except Exception as e:
        logger.error(f"Erreur Deep Learning: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'analyse Deep Learning: {str(e)}")

@router.post("/cognitive-diagnostic")
async def cognitive_diagnostic(
    student_id: int = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Diagnostic cognitif avancé de l'étudiant.
    """
    try:
        # Récupérer les réponses de l'étudiant
        student_responses = _get_student_responses_from_db(db, student_id)
        
        unified_service = UnifiedAIService()
        
        # Diagnostic cognitif
        diagnostic_result = unified_service.cognitive_diagnostic(student_id, student_responses)
        
        return {
            "success": True,
            "cognitive_diagnostic": diagnostic_result,
            "student_id": student_id,
            "generated_by": "UnifiedAIService"
        }
        
    except Exception as e:
        logger.error(f"Erreur diagnostic cognitif: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors du diagnostic: {str(e)}")

@router.post("/performance-prediction")
async def performance_prediction(
    student_id: int = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Prédiction de performance basée sur l'historique.
    """
    try:
        # Récupérer l'historique des performances
        performance_history = _get_performance_history_from_db(db, student_id)
        
        unified_service = UnifiedAIService()
        
        # Prédiction de performance
        prediction_result = unified_service.performance_prediction(performance_history)
        
        return {
            "success": True,
            "performance_prediction": prediction_result,
            "student_id": student_id,
            "generated_by": "UnifiedAIService"
        }
        
    except Exception as e:
        logger.error(f"Erreur prédiction performance: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction: {str(e)}")

@router.post("/generate-personalized-content")
async def generate_personalized_content(
    student_id: int = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Génération de contenu personnalisé pour l'étudiant.
    """
    try:
        # Récupérer le profil de l'étudiant
        student_profile = _get_student_profile_from_db(db, student_id)
        
        unified_service = UnifiedAIService()
        
        # Génération de contenu personnalisé
        content_result = unified_service.generate_personalized_content(student_profile)
        
        return {
            "success": True,
            "personalized_content": content_result,
            "student_id": student_id,
            "generated_by": "UnifiedAIService"
        }
        
    except Exception as e:
        logger.error(f"Erreur génération contenu: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération: {str(e)}")

# Fonctions utilitaires pour la base de données
def _get_student_data_from_db(db: Session, student_id: int) -> Dict:
    """Récupère les données de l'étudiant depuis la base de données."""
    # Récupérer les résultats de quiz
    quiz_results = db.query(QuizResult).filter(QuizResult.student_id == student_id).all()
    
    # Récupérer les réponses
    responses = []
    for result in quiz_results:
        for answer in result.answers:
            responses.append({
                "answer": answer.answer_text,
                "score": result.score,
                "quiz_id": result.quiz_id
            })
    
    # Récupérer l'historique des performances
    history = [
        {
            "score": result.score,
            "date": result.completed_at.isoformat() if result.completed_at else None,
            "quiz_id": result.quiz_id
        }
        for result in quiz_results
    ]
    
    # Récupérer le profil de l'étudiant
    user = db.query(User).filter(User.id == student_id).first()
    profile = {
        "level": "intermediate",  # À adapter selon vos besoins
        "weak_subjects": [],  # À calculer selon les résultats
        "strong_subjects": []  # À calculer selon les résultats
    }
    
    return {
        "student_id": student_id,
        "responses": responses,
        "history": history,
        "profile": profile,
        "free_text_answer": "",  # À adapter selon vos besoins
        "expected_answer": ""  # À adapter selon vos besoins
    }

def _get_learning_data_from_db(db: Session, student_id: int) -> Dict:
    """Récupère les données d'apprentissage pour l'analyse Deep Learning."""
    quiz_results = db.query(QuizResult).filter(QuizResult.student_id == student_id).all()
    
    answers = []
    correct_answers = []
    
    for result in quiz_results:
        for answer in result.answers:
            answers.append(answer.answer_text or "")
            correct_answers.append(answer.question.correct_answer or "")
    
    return {
        "answers": answers,
        "correct_answers": correct_answers
    }

def _get_student_responses_from_db(db: Session, student_id: int) -> List[Dict]:
    """Récupère les réponses de l'étudiant pour le diagnostic cognitif."""
    quiz_results = db.query(QuizResult).filter(QuizResult.student_id == student_id).all()
    
    responses = []
    for result in quiz_results:
        for answer in result.answers:
            responses.append({
                "answer": answer.answer_text,
                "score": result.score,
                "is_correct": answer.is_correct,
                "quiz_id": result.quiz_id
            })
    
    return responses

def _get_performance_history_from_db(db: Session, student_id: int) -> List[Dict]:
    """Récupère l'historique des performances pour la prédiction."""
    quiz_results = db.query(QuizResult).filter(QuizResult.student_id == student_id).all()
    
    history = []
    for result in quiz_results:
        history.append({
            "score": result.score,
            "date": result.completed_at.isoformat() if result.completed_at else None,
            "quiz_id": result.quiz_id
        })
    
    return history

def _get_student_profile_from_db(db: Session, student_id: int) -> Dict:
    """Récupère le profil de l'étudiant pour la génération de contenu."""
    # Analyser les résultats pour identifier les forces/faiblesses
    quiz_results = db.query(QuizResult).filter(QuizResult.student_id == student_id).all()
    
    # Calculer les moyennes par sujet
    subject_scores = {}
    for result in quiz_results:
        subject = result.quiz.subject or "Général"
        if subject not in subject_scores:
            subject_scores[subject] = []
        subject_scores[subject].append(result.score)
    
    # Identifier les sujets faibles (< 60% de moyenne)
    weak_subjects = []
    strong_subjects = []
    
    for subject, scores in subject_scores.items():
        avg_score = sum(scores) / len(scores)
        if avg_score < 60:
            weak_subjects.append(subject)
        else:
            strong_subjects.append(subject)
    
    return {
        "level": "intermediate",  # À adapter selon vos besoins
        "weak_subjects": weak_subjects,
        "strong_subjects": strong_subjects
    }

def _save_analysis_results_to_db(db: Session, student_id: int, analysis_result: Dict):
    """Sauvegarde les résultats d'analyse dans la base de données."""
    # Ici vous pouvez sauvegarder les résultats dans une table dédiée
    # Par exemple : AIAnalysisResults
    pass

def _save_adaptation_to_db(db: Session, quiz_id: int, adaptation_result: Dict):
    """Sauvegarde les adaptations dans la base de données."""
    # Ici vous pouvez sauvegarder les adaptations
    pass

def _save_tutor_interaction_to_db(db: Session, quiz_id: int, question: str, tutor_result: Dict):
    """Sauvegarde les interactions avec le tuteur dans la base de données."""
    # Ici vous pouvez sauvegarder les interactions
    pass 