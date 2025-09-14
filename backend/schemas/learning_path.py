#!/usr/bin/env python3
"""
Schémas Pydantic pour les learning paths
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class LearningPathStart(BaseModel):
    """Démarrage d'un learning path"""
    pass

class LearningPathStepComplete(BaseModel):
    """Complétion d'une étape"""
    step_number: int = Field(..., description="Numéro de l'étape complétée")
    time_spent: Optional[int] = Field(None, description="Temps passé en secondes")

class LearningPathProgress(BaseModel):
    """Progression d'un learning path"""
    learning_path_id: int
    student_id: int
    progress: float
    progress_percentage: float
    current_step: int
    total_steps: int
    is_completed: bool
    started_at: Optional[datetime]
    completed_at: Optional[datetime]

class LearningPathStep(BaseModel):
    """Étape d'un learning path"""
    id: int
    step_number: int
    title: str
    description: Optional[str]
    content_type: str
    estimated_duration: Optional[int]
    is_required: bool
    is_active: bool

class LearningPathWithSteps(BaseModel):
    """Learning path avec ses étapes"""
    learning_path: dict
    steps: List[LearningPathStep] 