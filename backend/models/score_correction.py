from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float
from sqlalchemy.sql import func
from core.database import Base

class ScoreCorrection(Base):
    __tablename__ = "score_corrections"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    quiz_result_id = Column(Integer, nullable=False, index=True)
    
    # Scores
    original_score = Column(Float, nullable=False)  # Score original
    corrected_score = Column(Float, nullable=False)  # Score corrigé
    score_adjustment = Column(Float, nullable=False)  # Différence (corrected - original)
    
    # Informations sur la correction
    reason = Column(Text)  # Raison de la correction
    subject = Column(String(50))  # Sujet du quiz
    
    # Qui a fait la correction
    corrected_by = Column(Integer, nullable=False)  # ID de l'utilisateur qui a fait la correction
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 