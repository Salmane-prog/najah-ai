#!/usr/bin/env python3
"""
Schémas Pydantic pour les assessments
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class AssessmentAnswer(BaseModel):
    """Réponse à une question d'évaluation"""
    question_id: int = Field(..., description="ID de la question")
    answer: str = Field(..., description="Réponse de l'étudiant")

class AssessmentSubmit(BaseModel):
    """Soumission d'une évaluation"""
    answers: List[AssessmentAnswer] = Field(..., description="Liste des réponses")
    time_spent: Optional[int] = Field(None, description="Temps passé en secondes")

class AssessmentStart(BaseModel):
    """Démarrage d'une évaluation"""
    pass

class AssessmentResponse(BaseModel):
    """Réponse d'une évaluation"""
    id: int
    title: str
    description: Optional[str]
    subject: Optional[str]
    status: str
    started_at: Optional[datetime]
    completed_at: Optional[datetime]

class AssessmentQuestionResponse(BaseModel):
    """Question d'évaluation"""
    id: int
    question_text: str
    question_type: str
    subject: str
    difficulty: str
    options: Optional[str]
    points: Optional[float]
    order: int

class AssessmentResultResponse(BaseModel):
    """Résultat d'une évaluation"""
    total_score: float
    max_score: float
    percentage: float
    completed_at: Optional[datetime]

class AssessmentWithQuestions(BaseModel):
    """Évaluation avec ses questions"""
    assessment: AssessmentResponse
    questions: List[AssessmentQuestionResponse]

class AssessmentWithResult(BaseModel):
    """Évaluation avec son résultat"""
    assessment: AssessmentResponse
    result: AssessmentResultResponse 