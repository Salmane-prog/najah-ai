from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey, JSON, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

class AIModel(Base):
    __tablename__ = "ai_models"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    model_type = Column(String(100))  # ml_algorithm, neural_network, expert_system
    algorithm = Column(String(100))  # random_forest, svm, lstm, transformer, etc.
    version = Column(String(50))
    description = Column(Text)
    
    # Métriques de performance
    accuracy = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    mse = Column(Float)  # Mean Squared Error pour la régression
    
    # Configuration du modèle
    hyperparameters = Column(JSON)  # Paramètres d'hyperparamétrage
    model_config = Column(JSON)  # Configuration générale du modèle
    feature_importance = Column(JSON)  # Importance des features
    
    # Fichiers du modèle
    model_file_path = Column(String(500))  # Chemin vers le fichier du modèle
    model_weights = Column(LargeBinary)  # Poids du modèle (optionnel)
    
    # Métadonnées
    training_data_size = Column(Integer)
    training_duration = Column(Float)  # Durée d'entraînement en heures
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relations
    training_sessions = relationship("ModelTrainingSession", back_populates="model")
    predictions = relationship("AIModelPrediction", back_populates="model")
    deployments = relationship("ModelDeployment", back_populates="model")

class ModelTrainingSession(Base):
    __tablename__ = "model_training_sessions"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("ai_models.id"))
    session_name = Column(String(255))
    
    # Données d'entraînement
    training_data_source = Column(String(255))
    training_data_size = Column(Integer)
    validation_data_size = Column(Integer)
    
    # Paramètres d'entraînement
    epochs = Column(Integer)
    batch_size = Column(Integer)
    learning_rate = Column(Float)
    optimizer = Column(String(100))
    loss_function = Column(String(100))
    
    # Résultats de l'entraînement
    training_accuracy = Column(Float)
    validation_accuracy = Column(Float)
    training_loss = Column(Float)
    validation_loss = Column(Float)
    
    # Métadonnées
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    status = Column(String(50), default="running")  # running, completed, failed
    
    # Relations
    model = relationship("AIModel", back_populates="training_sessions")

class AIModelPrediction(Base):
    __tablename__ = "ai_model_predictions"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("ai_models.id"))
    student_id = Column(Integer, ForeignKey("users.id"))
    
    # Données de prédiction
    input_features = Column(JSON)  # Features d'entrée
    prediction_type = Column(String(100))  # performance, difficulty, recommendation
    predicted_value = Column(Float)
    confidence_score = Column(Float)
    prediction_interval = Column(JSON)  # Intervalle de confiance
    
    # Métadonnées
    prediction_timestamp = Column(DateTime(timezone=True), server_default=func.now())
    processing_time = Column(Float)  # Temps de traitement en millisecondes
    
    # Relations
    model = relationship("AIModel", back_populates="predictions")
    student = relationship("User")

class ModelDeployment(Base):
    __tablename__ = "model_deployments"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("ai_models.id"))
    environment = Column(String(100))  # development, staging, production
    deployment_url = Column(String(500))
    
    # Configuration de déploiement
    deployment_config = Column(JSON)
    scaling_config = Column(JSON)  # Configuration de mise à l'échelle
    monitoring_config = Column(JSON)  # Configuration de monitoring
    
    # Métadonnées
    deployed_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(50), default="active")  # active, inactive, error
    health_check = Column(JSON)  # État de santé du déploiement
    
    # Relations
    model = relationship("AIModel", back_populates="deployments")

class DataCollection(Base):
    __tablename__ = "data_collection"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    data_type = Column(String(100))  # interaction, performance, behavior
    data_source = Column(String(100))  # quiz, exercise, navigation, etc.
    
    # Données collectées
    raw_data = Column(JSON)  # Données brutes
    processed_data = Column(JSON)  # Données traitées
    data_metadata = Column(JSON)  # Métadonnées (timestamp, session_id, etc.)
    
    # Qualité des données
    data_quality_score = Column(Float)  # Score de qualité des données
    completeness = Column(Float)  # Complétude des données
    accuracy = Column(Float)  # Précision des données
    
    # Métadonnées
    collected_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True))
    
    # Relations (commentées temporairement)
    # student = relationship("User", back_populates="data_collections")

class AILearningPatternAnalysis(Base):
    __tablename__ = "ai_learning_pattern_analysis"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    pattern_type = Column(String(100))  # study_time, difficulty_preference, etc.
    
    # Analyse du pattern
    pattern_data = Column(JSON)  # Données du pattern
    confidence_score = Column(Float)  # Confiance dans l'analyse
    pattern_strength = Column(Float)  # Force du pattern (0-1)
    
    # Insights
    insights = Column(JSON)  # Insights générés
    recommendations = Column(JSON)  # Recommandations basées sur le pattern
    
    # Métadonnées
    analyzed_at = Column(DateTime(timezone=True), server_default=func.now())
    last_updated = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations (commentées temporairement)
    # student = relationship("User", back_populates="pattern_analyses")

class ContinuousImprovement(Base):
    __tablename__ = "continuous_improvement"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("ai_models.id"))
    
    # Métriques d'amélioration
    improvement_type = Column(String(100))  # accuracy, performance, efficiency
    improvement_metric = Column(Float)  # Valeur de la métrique
    improvement_percentage = Column(Float)  # Pourcentage d'amélioration
    
    # Feedback et validation
    user_feedback = Column(JSON)  # Feedback des utilisateurs
    validation_results = Column(JSON)  # Résultats de validation
    
    # Métadonnées
    improvement_date = Column(DateTime(timezone=True), server_default=func.now())
    validated_at = Column(DateTime(timezone=True))
    
    # Relations
    model = relationship("AIModel")
