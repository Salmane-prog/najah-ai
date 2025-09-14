from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from core.database import get_db
from core.security import get_current_user
from models.ai_advanced import (
    AIRecommendation, AITutoringSession, AITutoringInteraction,
    DifficultyDetection, AdaptiveContent
)
from models.analytics import LearningAnalytics
from models.user import User, UserRole
from pydantic import BaseModel

router = APIRouter(tags=["ai_advanced"])

# Pydantic models
class AIRecommendationCreate(BaseModel):
    recommendation_type: str
    title: str
    description: Optional[str] = None
    content_id: Optional[int] = None
    quiz_id: Optional[int] = None
    learning_path_id: Optional[int] = None
    confidence_score: float = 0.0
    reason: Optional[str] = None

class AITutoringSessionCreate(BaseModel):
    subject: Optional[str] = None
    topic: Optional[str] = None
    session_type: str = "general"

class AITutoringInteractionCreate(BaseModel):
    user_message: str
    interaction_type: str = "question"

class DifficultyDetectionCreate(BaseModel):
    subject: str
    topic: str
    difficulty_level: str
    confidence_score: float = 0.0
    evidence: Optional[dict] = None

class AIRecommendationResponse(BaseModel):
    id: int
    user_id: int
    recommendation_type: str
    title: str
    description: Optional[str]
    content_id: Optional[int]
    quiz_id: Optional[int]
    learning_path_id: Optional[int]
    confidence_score: float
    reason: Optional[str]
    is_accepted: bool
    is_dismissed: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class AITutoringSessionResponse(BaseModel):
    id: int
    user_id: int
    subject: Optional[str]
    topic: Optional[str]
    session_type: str
    start_time: datetime
    end_time: Optional[datetime]
    duration: Optional[int]
    status: str
    notes: Optional[str]
    
    class Config:
        from_attributes = True

class AITutoringInteractionResponse(BaseModel):
    id: int
    session_id: int
    user_message: str
    ai_response: str
    interaction_type: str
    timestamp: datetime
    user_satisfaction: Optional[int]
    
    class Config:
        from_attributes = True

class DifficultyDetectionResponse(BaseModel):
    id: int
    user_id: int
    subject: str
    topic: str
    difficulty_level: str
    confidence_score: float
    evidence: Optional[dict]
    detected_at: datetime
    is_resolved: bool
    resolution_notes: Optional[str]
    
    class Config:
        from_attributes = True

# AI Recommendations
@router.get("/recommendations", response_model=List[AIRecommendationResponse])
async def get_ai_recommendations(
    recommendation_type: Optional[str] = None,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les recommandations IA pour l'utilisateur"""
    query = db.query(AIRecommendation).filter(
        AIRecommendation.user_id == current_user.id,
        AIRecommendation.is_dismissed == False
    )
    
    if recommendation_type:
        query = query.filter(AIRecommendation.recommendation_type == recommendation_type)
    
    recommendations = query.order_by(AIRecommendation.confidence_score.desc()).limit(limit).all()
    return [AIRecommendationResponse(**rec.__dict__) for rec in recommendations]

@router.post("/recommendations/{recommendation_id}/accept")
async def accept_ai_recommendation(
    recommendation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Accepter une recommandation IA"""
    recommendation = db.query(AIRecommendation).filter(
        AIRecommendation.id == recommendation_id,
        AIRecommendation.user_id == current_user.id
    ).first()
    
    if not recommendation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recommandation non trouvée"
        )
    
    recommendation.is_accepted = True
    db.commit()
    
    return {"message": "Recommandation acceptée avec succès"}

@router.post("/recommendations/{recommendation_id}/dismiss")
async def dismiss_ai_recommendation(
    recommendation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Rejeter une recommandation IA"""
    recommendation = db.query(AIRecommendation).filter(
        AIRecommendation.id == recommendation_id,
        AIRecommendation.user_id == current_user.id
    ).first()
    
    if not recommendation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recommandation non trouvée"
        )
    
    recommendation.is_dismissed = True
    db.commit()
    
    return {"message": "Recommandation rejetée avec succès"}

# AI Tutoring
@router.post("/tutoring/sessions", response_model=AITutoringSessionResponse)
async def create_ai_tutoring_session(
    session: AITutoringSessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer une session de tutorat IA"""
    db_session = AITutoringSession(
        user_id=current_user.id,
        subject=session.subject,
        topic=session.topic,
        session_type=session.session_type
    )
    
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    
    return AITutoringSessionResponse(**db_session.__dict__)

@router.get("/tutoring/sessions", response_model=List[AITutoringSessionResponse])
async def get_ai_tutoring_sessions(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les sessions de tutorat IA"""
    query = db.query(AITutoringSession).filter(AITutoringSession.user_id == current_user.id)
    
    if status:
        query = query.filter(AITutoringSession.status == status)
    
    sessions = query.order_by(AITutoringSession.start_time.desc()).all()
    return [AITutoringSessionResponse(**session.__dict__) for session in sessions]

@router.post("/tutoring/sessions/{session_id}/interactions", response_model=AITutoringInteractionResponse)
async def create_ai_tutoring_interaction(
    session_id: int,
    interaction: AITutoringInteractionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer une interaction de tutorat IA"""
    # Vérifier si la session existe et appartient à l'utilisateur
    session = db.query(AITutoringSession).filter(
        AITutoringSession.id == session_id,
        AITutoringSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session de tutorat non trouvée"
        )
    
    # Simuler une réponse IA (dans un vrai système, cela appellerait un service IA)
    ai_response = f"Voici une réponse IA à votre question : {interaction.user_message}"
    
    db_interaction = AITutoringInteraction(
        session_id=session_id,
        user_message=interaction.user_message,
        ai_response=ai_response,
        interaction_type=interaction.interaction_type
    )
    
    db.add(db_interaction)
    db.commit()
    db.refresh(db_interaction)
    
    return AITutoringInteractionResponse(**db_interaction.__dict__)

@router.get("/tutoring/sessions/{session_id}/interactions", response_model=List[AITutoringInteractionResponse])
async def get_ai_tutoring_interactions(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les interactions d'une session de tutorat"""
    # Vérifier si la session existe et appartient à l'utilisateur
    session = db.query(AITutoringSession).filter(
        AITutoringSession.id == session_id,
        AITutoringSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session de tutorat non trouvée"
        )
    
    interactions = db.query(AITutoringInteraction).filter(
        AITutoringInteraction.session_id == session_id
    ).order_by(AITutoringInteraction.timestamp).all()
    
    return [AITutoringInteractionResponse(**interaction.__dict__) for interaction in interactions]

# Difficulty Detection
@router.post("/difficulty-detection", response_model=DifficultyDetectionResponse)
async def create_difficulty_detection(
    detection: DifficultyDetectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer une détection de difficulté"""
    db_detection = DifficultyDetection(
        user_id=current_user.id,
        subject=detection.subject,
        topic=detection.topic,
        difficulty_level=detection.difficulty_level,
        confidence_score=detection.confidence_score,
        evidence=detection.evidence
    )
    
    db.add(db_detection)
    db.commit()
    db.refresh(db_detection)
    
    return DifficultyDetectionResponse(**db_detection.__dict__)

@router.get("/difficulty-detection", response_model=List[DifficultyDetectionResponse])
async def get_difficulty_detections(
    subject: Optional[str] = None,
    is_resolved: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les détections de difficulté"""
    query = db.query(DifficultyDetection).filter(DifficultyDetection.user_id == current_user.id)
    
    if subject:
        query = query.filter(DifficultyDetection.subject == subject)
    if is_resolved is not None:
        query = query.filter(DifficultyDetection.is_resolved == is_resolved)
    
    detections = query.order_by(DifficultyDetection.detected_at.desc()).all()
    return [DifficultyDetectionResponse(**detection.__dict__) for detection in detections]

@router.put("/difficulty-detection/{detection_id}/resolve")
async def resolve_difficulty_detection(
    detection_id: int,
    resolution_notes: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Marquer une détection de difficulté comme résolue"""
    detection = db.query(DifficultyDetection).filter(
        DifficultyDetection.id == detection_id,
        DifficultyDetection.user_id == current_user.id
    ).first()
    
    if not detection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Détection de difficulté non trouvée"
        )
    
    detection.is_resolved = True
    detection.resolution_notes = resolution_notes
    db.commit()
    
    return {"message": "Détection de difficulté marquée comme résolue"}

# Learning Analytics
@router.get("/analytics/performance")
async def get_performance_analytics(
    subject: Optional[str] = None,
    period: str = "week",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les analytics de performance"""
    # Ici, vous implémenteriez la logique pour analyser les performances
    # Pour l'instant, retournons des données simulées
    analytics_data = {
        "user_id": current_user.id,
        "period": period,
        "subject": subject,
        "overall_score": 85.5,
        "improvement_rate": 12.3,
        "strengths": ["Mathématiques", "Logique"],
        "weaknesses": ["Histoire", "Géographie"],
        "recommendations": [
            "Continuez à pratiquer les mathématiques",
            "Consacrez plus de temps à l'histoire"
        ]
    }
    
    return analytics_data

@router.get("/analytics/engagement")
async def get_engagement_analytics(
    period: str = "week",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les analytics d'engagement"""
    # Données simulées d'engagement
    engagement_data = {
        "user_id": current_user.id,
        "period": period,
        "total_time_spent": 1250,  # minutes
        "sessions_count": 15,
        "completion_rate": 78.5,
        "engagement_score": 8.2,
        "trends": {
            "daily_activity": [65, 70, 85, 90, 75, 80, 95],
            "weekly_progress": [12, 15, 18, 22, 25, 28, 30]
        }
    }
    
    return engagement_data 