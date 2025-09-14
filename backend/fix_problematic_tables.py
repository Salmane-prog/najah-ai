#!/usr/bin/env python3
"""
Script pour corriger uniquement les tables problématiques
"""

import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import engine, SessionLocal
from sqlalchemy import text

def fix_problematic_tables():
    """Corrige uniquement les tables problématiques"""
    print("=== CORRECTION DES TABLES PROBLÉMATIQUES ===")
    
    db = SessionLocal()
    try:
        # 1. Corriger detailed_reports (ajouter les colonnes manquantes)
        print("\n1. Correction de detailed_reports...")
        try:
            # Supprimer l'ancienne table
            db.execute(text("DROP TABLE IF EXISTS detailed_reports"))
            print("  - Ancienne table detailed_reports supprimee")
            
            # Recréer avec le bon schéma
            db.execute(text("""
                CREATE TABLE detailed_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    report_type VARCHAR(50) NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    period_start TIMESTAMP NOT NULL,
                    period_end TIMESTAMP NOT NULL,
                    data TEXT NOT NULL,
                    insights TEXT,
                    recommendations TEXT,
                    is_exported BOOLEAN DEFAULT FALSE,
                    exported_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            print("  - Nouvelle table detailed_reports creee avec le bon schéma")
            
        except Exception as e:
            print(f"  ERREUR: {e}")
        
        # 2. Créer advanced_homeworks (table manquante)
        print("\n2. Creation de advanced_homeworks...")
        try:
            db.execute(text("""
                CREATE TABLE advanced_homeworks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    subject VARCHAR(100) NOT NULL,
                    class_id INTEGER,
                    created_by INTEGER NOT NULL,
                    due_date TIMESTAMP NOT NULL,
                    priority VARCHAR(20) DEFAULT 'medium',
                    estimated_time INTEGER,
                    max_score REAL DEFAULT 100.0,
                    instructions TEXT,
                    attachments TEXT,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP
                )
            """))
            print("  - Table advanced_homeworks creee")
            
        except Exception as e:
            print(f"  ERREUR: {e}")
        
        # 3. Créer analytics_reports (table manquante)
        print("\n3. Creation de analytics_reports...")
        try:
            db.execute(text("""
                CREATE TABLE analytics_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    analytics_type VARCHAR(50) NOT NULL,
                    period_start TIMESTAMP NOT NULL,
                    period_end TIMESTAMP NOT NULL,
                    metrics TEXT NOT NULL,
                    trends TEXT,
                    insights TEXT,
                    recommendations TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            print("  - Table analytics_reports creee")
            
        except Exception as e:
            print(f"  ERREUR: {e}")
        
        # 4. Créer ai_recommendations (table manquante)
        print("\n4. Creation de ai_recommendations...")
        try:
            db.execute(text("""
                CREATE TABLE ai_recommendations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    recommendation_type VARCHAR(50) NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    content_id INTEGER,
                    quiz_id INTEGER,
                    learning_path_id INTEGER,
                    confidence_score REAL DEFAULT 0.0,
                    reason TEXT,
                    is_accepted BOOLEAN DEFAULT FALSE,
                    is_dismissed BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            print("  - Table ai_recommendations creee")
            
        except Exception as e:
            print(f"  ERREUR: {e}")
        
        # 5. Créer ai_tutoring_sessions (table manquante)
        print("\n5. Creation de ai_tutoring_sessions...")
        try:
            db.execute(text("""
                CREATE TABLE ai_tutoring_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    subject VARCHAR(100),
                    topic VARCHAR(255),
                    session_type VARCHAR(50) DEFAULT 'general',
                    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    end_time TIMESTAMP,
                    duration INTEGER,
                    status VARCHAR(20) DEFAULT 'active',
                    notes TEXT
                )
            """))
            print("  - Table ai_tutoring_sessions creee")
            
        except Exception as e:
            print(f"  ERREUR: {e}")
        
        # 6. Créer difficulty_detections (table manquante)
        print("\n6. Creation de difficulty_detections...")
        try:
            db.execute(text("""
                CREATE TABLE difficulty_detections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    subject VARCHAR(100) NOT NULL,
                    topic VARCHAR(255) NOT NULL,
                    difficulty_level VARCHAR(20) NOT NULL,
                    confidence_score REAL DEFAULT 0.0,
                    evidence TEXT,
                    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_resolved BOOLEAN DEFAULT FALSE,
                    resolution_notes TEXT
                )
            """))
            print("  - Table difficulty_detections creee")
            
        except Exception as e:
            print(f"  ERREUR: {e}")
        
        # Valider les changements
        db.commit()
        print("\n=== CORRECTION TERMINÉE ===")
        print("Toutes les tables problématiques ont été corrigees!")
        
    except Exception as e:
        print(f"ERREUR GENERALE: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Demarrage de la correction des tables problématiques...")
    fix_problematic_tables()
    print("Script termine!")
