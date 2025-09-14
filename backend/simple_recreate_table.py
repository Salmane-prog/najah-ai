#!/usr/bin/env python3
"""
Script simple pour recréer la table study_sessions
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text

def simple_recreate_table():
    """Recréer la table study_sessions simplement"""
    
    engine = create_engine("sqlite:///../data/app.db")
    
    try:
        with engine.connect() as conn:
            # Supprimer l'ancienne table
            conn.execute(text("DROP TABLE IF EXISTS study_sessions"))
            print("🗑️  Ancienne table supprimée")
            
            # Créer la nouvelle table
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
            conn.commit()
            print("✅ Nouvelle table créée")
            
            # Vérifier la structure
            result = conn.execute(text("PRAGMA table_info(study_sessions)"))
            columns = result.fetchall()
            
            print("\n📋 Structure de la nouvelle table:")
            for column in columns:
                print(f"   {column[1]} ({column[2]}) - PK: {column[5]}")
            
            # Test d'insertion
            print("\n🧪 Test d'insertion...")
            result = conn.execute(text("""
                INSERT INTO study_sessions (user_id, topic, subject, start_time, end_time, planned_duration, notes, status)
                VALUES (4, 'Test Session', 'Test Subject', '2025-01-20 10:00:00', '2025-01-20 12:00:00', 120, 'Test notes', 'planned')
            """))
            conn.commit()
            
            # Récupérer l'ID
            result = conn.execute(text("SELECT last_insert_rowid()"))
            last_id = result.fetchone()[0]
            print(f"✅ Test réussi, ID généré: {last_id}")
            
            # Nettoyer
            conn.execute(text("DELETE FROM study_sessions WHERE id = ?"), (last_id,))
            conn.commit()
            print("✅ Nettoyage terminé")
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")

if __name__ == "__main__":
    simple_recreate_table() 