from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Optional
from services.openai_service import OpenAIService
from api.v1.auth import get_current_user
from models.user import User

router = APIRouter()

class QuizGenerationRequest(BaseModel):
    topic: str
    difficulty: str = "medium"
    student_level: str = "intermediate"

class TutorRequest(BaseModel):
    question: str
    student_context: Dict

class AnalysisRequest(BaseModel):
    student_answer: str
    correct_answer: str

@router.post("/generate-quiz")
async def generate_quiz_question(
    request: QuizGenerationRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Génère une question de quiz personnalisée avec OpenAI.
    """
    try:
        openai_service = OpenAIService()
        question = openai_service.generate_quiz_question(
            topic=request.topic,
            difficulty=request.difficulty,
            student_level=request.student_level
        )
        
        return {
            "success": True,
            "question": question,
            "generated_by": "OpenAI GPT-4"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération: {str(e)}")

@router.post("/tutor-response")
async def get_tutor_response(
    request: TutorRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Obtient une réponse de tuteur virtuel personnalisée.
    """
    try:
        openai_service = OpenAIService()
        response = openai_service.create_tutor_response(
            student_context=request.student_context,
            question=request.question
        )
        
        return {
            "success": True,
            "response": response,
            "generated_by": "OpenAI GPT-4"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération de réponse: {str(e)}")

@router.post("/analyze-response")
async def analyze_student_response(
    request: AnalysisRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Analyse une réponse d'étudiant par rapport à la réponse correcte.
    """
    try:
        openai_service = OpenAIService()
        analysis = openai_service.analyze_student_response(
            student_answer=request.student_answer,
            correct_answer=request.correct_answer
        )
        
        return {
            "success": True,
            "analysis": analysis,
            "generated_by": "OpenAI GPT-4"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'analyse: {str(e)}")

@router.get("/status")
async def get_openai_status():
    """
    Vérifie le statut de l'API OpenAI.
    """
    try:
        openai_service = OpenAIService()
        stats = openai_service.get_usage_stats()
        
        return {
            "success": True,
            "status": "OpenAI API fonctionnelle",
            "stats": stats
        }
        
    except Exception as e:
        return {
            "success": False,
            "status": "Erreur de connexion OpenAI",
            "error": str(e)
        } 