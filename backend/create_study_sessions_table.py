#!/usr/bin/env python3
"""
Script pour créer la table study_sessions
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text

def create_study_sessions_table():
    """Créer la table study_sessions si elle n'existe pas"""
    
    # Créer une connexion directe à la base de données
    engine = create_engine("sqlite:///../data/app.db")
    
    try:
        with engine.connect() as conn:
            # Vérifier si la table existe
            result = conn.execute(text("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='study_sessions'
            """))
            
            if result.fetchone():
                print("✅ Table study_sessions existe déjà")
                return
            
            # Créer la table study_sessions
            conn.execute(text("""
                CREATE TABLE study_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    subject VARCHAR(100),
                    topic VARCHAR(255),
                    planned_duration INTEGER,
                    actual_duration INTEGER,
                    start_time DATETIME,
                    end_time DATETIME,
                    status VARCHAR(20) DEFAULT 'planned',
                    notes TEXT,
                    productivity_rating INTEGER,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """))
            
            # Commit les changements
            conn.commit()
            print("✅ Table study_sessions créée avec succès")
            
    except Exception as e:
        print(f"❌ Erreur lors de la création de la table: {str(e)}")

if __name__ == "__main__":
    create_study_sessions_table() 