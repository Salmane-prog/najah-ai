from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# Schémas de base
class RemediationResultBase(BaseModel):
    topic: str = Field(..., description="Domaine de remédiation (fondamentaux, conjugaison, vocabulaire)")
    exercise_type: str = Field(..., description="Type d'exercice (quiz, reading, practice)")
    score: int = Field(..., ge=0, description="Score obtenu")
    max_score: int = Field(..., gt=0, description="Score maximum possible")
    percentage: float = Field(..., ge=0, le=100, description="Pourcentage de réussite")
    time_spent: int = Field(..., ge=0, description="Temps passé en secondes")
    weak_areas_improved: Optional[List[str]] = Field(default=[], description="Domaines améliorés")
    difficulty_level: Optional[str] = Field(default="medium", description="Niveau de difficulté")

class RemediationResultCreate(RemediationResultBase):
    student_id: int = Field(..., description="ID de l'étudiant")

class RemediationResultResponse(RemediationResultBase):
    id: int
    student_id: int
    completed_at: datetime
    
    class Config:
        from_attributes = True

# Schémas pour les badges
class BadgeBase(BaseModel):
    badge_type: str = Field(..., description="Type de badge")
    badge_name: str = Field(..., description="Nom du badge")
    badge_description: Optional[str] = Field(default=None, description="Description du badge")
    badge_icon: Optional[str] = Field(default=None, description="Icône du badge")
    metadata: Optional[Dict[str, Any]] = Field(default={}, description="Métadonnées du badge")

class BadgeCreate(BadgeBase):
    student_id: int = Field(..., description="ID de l'étudiant")

class BadgeResponse(BadgeBase):
    id: int
    student_id: int
    earned_at: datetime
    
    class Config:
        from_attributes = True

# Schémas pour le progrès
class ProgressBase(BaseModel):
    topic: str = Field(..., description="Domaine de remédiation")
    current_level: int = Field(..., ge=0, le=10, description="Niveau actuel")
    previous_level: int = Field(..., ge=0, le=10, description="Niveau précédent")
    improvement: int = Field(..., description="Amélioration du niveau")
    exercises_completed: int = Field(..., ge=0, description="Nombre d'exercices complétés")
    total_exercises: int = Field(..., ge=0, description="Total d'exercices disponibles")
    success_rate: float = Field(..., ge=0, le=100, description="Taux de réussite")

class ProgressCreate(ProgressBase):
    student_id: int = Field(..., description="ID de l'étudiant")

class ProgressResponse(ProgressBase):
    id: int
    student_id: int
    last_updated: datetime
    
    class Config:
        from_attributes = True

# Schémas pour les statistiques
class RemediationStats(BaseModel):
    total_exercises: int = Field(..., description="Total d'exercices complétés")
    average_score: float = Field(..., description="Score moyen")
    total_time: int = Field(..., description="Temps total passé en secondes")
    topics_covered: List[str] = Field(..., description="Domaines couverts")
    badges_earned: int = Field(..., description="Nombre de badges obtenus")
    current_level: float = Field(..., description="Niveau global actuel")

# Schémas pour la comparaison avant/après
class ProgressComparison(BaseModel):
    topic: str = Field(..., description="Domaine de remédiation")
    before: ProgressResponse = Field(..., description="Progrès avant")
    after: ProgressResponse = Field(..., description="Progrès après")
    improvement_percentage: float = Field(..., description="Pourcentage d'amélioration")
    time_to_improve: Optional[int] = Field(default=None, description="Temps pour améliorer en secondes")

# Schémas pour les recommandations
class RemediationRecommendation(BaseModel):
    topic: str = Field(..., description="Domaine recommandé")
    priority: str = Field(..., description="Priorité (high, medium, low)")
    reason: str = Field(..., description="Raison de la recommandation")
    suggested_exercises: List[str] = Field(..., description="Types d'exercices suggérés")
    estimated_time: int = Field(..., description="Temps estimé en minutes")








