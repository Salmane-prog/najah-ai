from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

# Import des modèles pour éviter les erreurs de mapper
from .content import Content
from .learning_path import LearningPath

class LearningHistory(Base):
    __tablename__ = "learning_history"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=True)
    path_id = Column(Integer, ForeignKey("learning_paths.id"), nullable=True)
    action = Column(String, nullable=False)  # ex: "start", "complete", "answer_qcm", etc.
    score = Column(Float, nullable=True)
    progression = Column(Float, nullable=True)  # % de progression sur le contenu ou parcours
    details = Column(Text, nullable=True)  # infos additionnelles (JSON, texte...)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    student = relationship("User", foreign_keys=[student_id], viewonly=True)
    content = relationship("Content")
    path = relationship("LearningPath") 