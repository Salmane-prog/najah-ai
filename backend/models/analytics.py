from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

class LearningAnalytics(Base):
    __tablename__ = "learning_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    subject = Column(String(100), nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
    
    # Métriques de performance
    time_spent = Column(Float)  # Temps passé en minutes
    questions_attempted = Column(Integer)
    questions_correct = Column(Integer)
    accuracy_rate = Column(Float)  # Taux de réussite
    difficulty_level = Column(Float)  # Niveau de difficulté moyen
    
    # Métriques d'engagement
    session_count = Column(Integer)
    resource_access_count = Column(Integer)
    interaction_count = Column(Integer)
    
    # Métriques d'apprentissage
    concept_mastery = Column(JSON)  # {"concept": "score"}
    learning_speed = Column(Float)  # Vitesse d'apprentissage
    retention_rate = Column(Float)  # Taux de rétention
    
    # Relations (commentées temporairement)
    # student = relationship("User", back_populates="learning_analytics")

class PredictiveModel(Base):
    __tablename__ = "predictive_models"
    
    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(255), nullable=False)
    model_type = Column(String(100))  # regression, classification, clustering
    algorithm = Column(String(100))  # random_forest, neural_network, etc.
    version = Column(String(50))
    accuracy = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relations
    predictions = relationship("StudentPrediction", back_populates="model")

class StudentPrediction(Base):
    __tablename__ = "student_predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    model_id = Column(Integer, ForeignKey("predictive_models.id"))
    prediction_type = Column(String(100))  # performance, dropout_risk, learning_path
    predicted_value = Column(Float)
    confidence_score = Column(Float)
    prediction_date = Column(DateTime(timezone=True), server_default=func.now())
    actual_value = Column(Float)  # Valeur réelle si disponible
    accuracy = Column(Float)  # Précision de la prédiction
    
    # Relations (commentées temporairement)
    # student = relationship("User", back_populates="predictions")
    model = relationship("PredictiveModel", back_populates="predictions")

class LearningPattern(Base):
    __tablename__ = "learning_patterns"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    pattern_type = Column(String(100))  # study_time, difficulty_preference, etc.
    pattern_data = Column(JSON)  # Données du pattern
    confidence = Column(Float)  # Confiance dans la détection
    detected_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations (commentées temporairement)
    # student = relationship("User", back_populates="learning_patterns")

class BlockageDetection(Base):
    __tablename__ = "blockage_detections"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    subject = Column(String(100), nullable=False)
    concept = Column(String(100))
    blockage_type = Column(String(100))  # cognitive, motivational, technical
    severity = Column(Integer)  # 1-5 scale
    symptoms = Column(JSON)  # Symptômes détectés
    detected_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True))
    resolution_strategy = Column(Text)
    
    # Relations (commentées temporairement)
    # student = relationship("User", back_populates="blockage_detections")

class TeacherDashboard(Base):
    __tablename__ = "teacher_dashboards"
    
    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id"))
    dashboard_type = Column(String(100))  # class_overview, individual_student, subject_analysis
    configuration = Column(JSON)  # Configuration du tableau de bord
    last_updated = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    teacher = relationship("User", foreign_keys=[teacher_id])

class ParentDashboard(Base):
    __tablename__ = "parent_dashboards"
    
    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey("users.id"))
    student_id = Column(Integer, ForeignKey("users.id"))
    dashboard_type = Column(String(100))  # progress_overview, performance_summary
    configuration = Column(JSON)  # Configuration du tableau de bord
    last_updated = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    parent = relationship("User", foreign_keys=[parent_id])
    student = relationship("User", foreign_keys=[student_id])

class AutomatedReport(Base):
    __tablename__ = "automated_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    report_type = Column(String(100))  # weekly, monthly, quarterly
    target_audience = Column(String(100))  # teacher, parent, student, admin
    report_data = Column(JSON)  # Données du rapport
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    sent_at = Column(DateTime(timezone=True))
    status = Column(String(50), default="generated")  # generated, sent, failed
    
    # Relations
    recipients = relationship("ReportRecipient", back_populates="report")

class ReportRecipient(Base):
    __tablename__ = "report_recipients"
    
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("automated_reports.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    delivery_method = Column(String(50))  # email, sms, in_app
    delivery_status = Column(String(50), default="pending")  # pending, delivered, failed
    
    # Relations
    report = relationship("AutomatedReport", back_populates="recipients")
    user = relationship("User")
