#!/usr/bin/env python3
"""
Script pour vérifier et corriger les modèles de base de données
"""

import os
import sys
import importlib

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def verify_models():
    """Vérifie que tous les modèles sont correctement importés"""
    print("Verification des modeles...")
    
    # Liste des modèles attendus
    expected_models = [
        'user', 'badge', 'quiz', 'content', 'category', 'class_group',
        'learning_path', 'student_learning_path', 'learning_history',
        'notification', 'messages', 'thread', 'notes', 'assessment',
        'settings', 'ratings', 'remediation', 'score_correction',
        'continuous_assessment', 'advanced_learning', 'advanced_notifications',
        'collaboration', 'forum', 'gamification', 'schedule', 'interface_levels',
        'library', 'organization', 'notes_advanced', 'student_analytics',
        'user_activity', 'real_time_activities', 'reports', 'ai_advanced',
        'homework', 'calendar'
    ]
    
    missing_models = []
    imported_models = []
    
    for model_name in expected_models:
        try:
            module = importlib.import_module(f'models.{model_name}')
            imported_models.append(model_name)
            print(f"OK - Modele {model_name} importe avec succes")
        except ImportError as e:
            missing_models.append(model_name)
            print(f"ERREUR - Modele {model_name} manquant: {e}")
        except Exception as e:
            print(f"ATTENTION - Erreur lors de l'import de {model_name}: {e}")
    
    print(f"\nResume:")
    print(f"OK - Modeles importes: {len(imported_models)}")
    print(f"ERREUR - Modeles manquants: {len(missing_models)}")
    
    if missing_models:
        print(f"\nModeles manquants: {', '.join(missing_models)}")
        return False
    
    return True

def verify_database_schema():
    """Vérifie le schéma de la base de données"""
    print("\nVerification du schema de la base de donnees...")
    
    try:
        from core.database import engine, Base
        from sqlalchemy import text
        
        # Vérifier la connexion
        with engine.connect() as conn:
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
            tables = [row[0] for row in result]
            
            print(f"OK - {len(tables)} tables trouvees dans la base de donnees")
            
            # Vérifier les tables critiques
            critical_tables = ['users', 'quizzes', 'contents', 'class_groups']
            missing_critical = []
            
            for table in critical_tables:
                if table not in tables:
                    missing_critical.append(table)
                    print(f"ERREUR - Table critique manquante: {table}")
                else:
                    print(f"OK - Table critique trouvee: {table}")
            
            if missing_critical:
                print(f"\nTables critiques manquantes: {', '.join(missing_critical)}")
                return False
            
            return True
            
    except Exception as e:
        print(f"ERREUR - Erreur lors de la verification du schema: {e}")
        return False

def fix_model_imports():
    """Corrige les imports de modèles manquants"""
    print("\nCorrection des imports de modeles...")
    
    # Créer des modèles de base pour les tables manquantes
    models_to_create = {
        'reports': """
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

class DetailedReport(Base):
    __tablename__ = "detailed_reports"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    report_type = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    period_start = Column(DateTime(timezone=True), nullable=False)
    period_end = Column(DateTime(timezone=True), nullable=False)
    data = Column(JSON, nullable=False)
    insights = Column(Text, nullable=True)
    recommendations = Column(JSON, nullable=True)
    is_exported = Column(Boolean, default=False)
    exported_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
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
    topics_covered = Column(JSON, nullable=True)
    strengths = Column(JSON, nullable=True)
    weaknesses = Column(JSON, nullable=True)
    recommendations = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", foreign_keys=[user_id])

class AnalyticsReport(Base):
    __tablename__ = "analytics_reports"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    analytics_type = Column(String(50), nullable=False)
    period_start = Column(DateTime(timezone=True), nullable=False)
    period_end = Column(DateTime(timezone=True), nullable=False)
    metrics = Column(JSON, nullable=False)
    trends = Column(JSON, nullable=True)
    insights = Column(Text, nullable=True)
    recommendations = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", foreign_keys=[user_id])
""",
        'ai_advanced': """
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

class AIRecommendation(Base):
    __tablename__ = "ai_recommendations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recommendation_type = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=True)
    learning_path_id = Column(Integer, ForeignKey("learning_paths.id"), nullable=True)
    confidence_score = Column(Float, default=0.0)
    reason = Column(Text, nullable=True)
    is_accepted = Column(Boolean, default=False)
    is_dismissed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", foreign_keys=[user_id])

class AITutoringSession(Base):
    __tablename__ = "ai_tutoring_sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject = Column(String(100), nullable=True)
    topic = Column(String(255), nullable=True)
    session_type = Column(String(50), default="general")
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True), nullable=True)
    duration = Column(Integer, nullable=True)
    status = Column(String(20), default="active")
    notes = Column(Text, nullable=True)
    user = relationship("User", foreign_keys=[user_id])

class DifficultyDetection(Base):
    __tablename__ = "difficulty_detections"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject = Column(String(100), nullable=False)
    topic = Column(String(255), nullable=False)
    difficulty_level = Column(String(20), nullable=False)
    confidence_score = Column(Float, default=0.0)
    evidence = Column(JSON, nullable=True)
    detected_at = Column(DateTime(timezone=True), server_default=func.now())
    is_resolved = Column(Boolean, default=False)
    resolution_notes = Column(Text, nullable=True)
    user = relationship("User", foreign_keys=[user_id])
""",
        'homework': """
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

class AdvancedHomework(Base):
    __tablename__ = "advanced_homeworks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    subject = Column(String(100), nullable=False)
    class_id = Column(Integer, ForeignKey("class_groups.id"), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    due_date = Column(DateTime(timezone=True), nullable=False)
    priority = Column(String(20), default="medium")
    estimated_time = Column(Integer, nullable=True)
    max_score = Column(Float, default=100.0)
    instructions = Column(Text, nullable=True)
    attachments = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    creator = relationship("User", foreign_keys=[created_by])
    class_group = relationship("ClassGroup")
"""
    }
    
    for model_name, model_code in models_to_create.items():
        model_file = f"models/{model_name}.py"
        if not os.path.exists(model_file):
            print(f"Creation du modele {model_name}...")
            with open(model_file, 'w', encoding='utf-8') as f:
                f.write(model_code)
            print(f"OK - Modele {model_name} cree")
        else:
            print(f"OK - Modele {model_name} existe deja")

def main():
    """Fonction principale"""
    print("Demarrage de la verification des modeles...")
    
    # Vérifier les modèles
    models_ok = verify_models()
    
    # Vérifier le schéma de la base de données
    schema_ok = verify_database_schema()
    
    # Corriger les imports si nécessaire
    if not models_ok:
        fix_model_imports()
    
    print("\nVerification terminee!")
    
    if models_ok and schema_ok:
        print("Tous les modeles et le schema sont corrects!")
    else:
        print("Des problemes ont ete detectes et corriges.")
        print("Relancez le script recreate_database.py pour recreer la base de donnees.")

if __name__ == "__main__":
    main()
