from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base
from datetime import datetime

class DetailedReport(Base):
    __tablename__ = "detailed_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    report_type = Column(String(50), nullable=False)  # performance, progress, analytics, behavior
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    period_start = Column(DateTime(timezone=True), nullable=False)
    period_end = Column(DateTime(timezone=True), nullable=False)
    data = Column(JSON, nullable=False)  # Données du rapport
    insights = Column(Text, nullable=True)  # Insights générés
    recommendations = Column(JSON, nullable=True)  # Recommandations
    is_exported = Column(Boolean, default=False)
    exported_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    user = relationship("User", foreign_keys=[user_id])

class SubjectProgressReport(Base):
    __tablename__ = "subject_progress_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject = Column(String(100), nullable=False)
    period_start = Column(DateTime(timezone=True), nullable=False)
    period_end = Column(DateTime(timezone=True), nullable=False)
    total_score = Column(Float, nullable=False)
    max_score = Column(Float, nullable=False)
    percentage = Column(Float, nullable=False)
    improvement_rate = Column(Float, nullable=True)
    topics_covered = Column(JSON, nullable=True)  # Liste des sujets couverts
    strengths = Column(JSON, nullable=True)  # Points forts
    weaknesses = Column(JSON, nullable=True)  # Points faibles
    recommendations = Column(JSON, nullable=True)  # Recommandations
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    user = relationship("User", foreign_keys=[user_id])

class AnalyticsReport(Base):
    __tablename__ = "analytics_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    analytics_type = Column(String(50), nullable=False)  # engagement, performance, behavior, learning_patterns
    period_start = Column(DateTime(timezone=True), nullable=False)
    period_end = Column(DateTime(timezone=True), nullable=False)
    metrics = Column(JSON, nullable=False)  # Métriques calculées
    trends = Column(JSON, nullable=True)  # Tendances identifiées
    insights = Column(Text, nullable=True)  # Insights générés
    recommendations = Column(JSON, nullable=True)  # Recommandations
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    user = relationship("User", foreign_keys=[user_id])

class ReportExport(Base):
    __tablename__ = "report_exports"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    report_id = Column(Integer, ForeignKey("detailed_reports.id"), nullable=False)
    export_format = Column(String(20), nullable=False)  # pdf, excel, csv, json
    file_url = Column(String(500), nullable=True)
    file_size = Column(Integer, nullable=True)  # en bytes
    exported_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    user = relationship("User", foreign_keys=[user_id])
    report = relationship("DetailedReport")
