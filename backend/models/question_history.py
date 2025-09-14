#!/usr/bin/env python3
"""
Modèle pour l'historique des questions posées
"""

from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class QuestionHistory(Base):
    """Historique des questions posées dans les tests adaptatifs"""
    __tablename__ = "question_history"
    
    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("french_adaptive_tests.id"), nullable=False)
    question_id = Column(Integer, nullable=False)  # ID de la question dans la banque
    question_text = Column(Text, nullable=False)  # Texte de la question posée
    difficulty = Column(String(20), nullable=False)  # Niveau de difficulté
    topic = Column(String(100), nullable=True)  # Sujet de la question
    asked_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    student_response = Column(Text, nullable=True)  # Réponse de l'étudiant
    is_correct = Column(Integer, nullable=True)  # 1 si correct, 0 si incorrect
    
    # Relations
    test = relationship("FrenchAdaptiveTest")
    
    class Config:
        orm_mode = True

