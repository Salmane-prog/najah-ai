from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

class ClassAnalytics(Base):
    __tablename__ = "class_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("class_groups.id"), nullable=False)
    
    # Métriques de performance
    average_score = Column(Float, default=0.0)
    total_quizzes_taken = Column(Integer, default=0)
    total_contents_completed = Column(Integer, default=0)
    average_completion_time = Column(Float, default=0.0)
    
    # Métriques d'engagement
    active_students_count = Column(Integer, default=0)
    total_study_time = Column(Integer, default=0)  # en minutes
    participation_rate = Column(Float, default=0.0)  # pourcentage
    
    # Métriques de progression
    overall_progress = Column(Float, default=0.0)  # pourcentage moyen
    students_on_track = Column(Integer, default=0)
    students_needing_help = Column(Integer, default=0)
    
    # Métadonnées
    last_updated = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text, nullable=True)
    
    # Relations
    class_group = relationship("ClassGroup", foreign_keys=[class_id], viewonly=True)

