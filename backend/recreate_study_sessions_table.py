#!/usr/bin/env python3
"""
Script pour recréer la table study_sessions avec la bonne structure
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text

def recreate_study_sessions_table():
    """Recréer la table study_sessions avec la bonne structure"""
    
    # Créer une connexion directe à la base de données
    engine = create_engine("sqlite:///../data/app.db")
    
    try:
        with engine.connect() as conn:
            # Sauvegarder les données existantes
            result = conn.execute(text("SELECT * FROM study_sessions"))
            existing_data = result.fetchall()
            print(f"📊 Sauvegarde de {len(existing_data)} sessions existantes")
            
            # Supprimer l'ancienne table
            conn.execute(text("DROP TABLE IF EXISTS study_sessions"))
            print("🗑️  Ancienne table supprimée")
            
            # Créer la nouvelle table avec la bonne structure
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
            print("✅ Nouvelle table créée avec la bonne structure")
            
            # Restaurer les données existantes
            if existing_data:
                for row in existing_data:
                    # Ignorer l'ancien ID et laisser SQLite générer un nouveau
                    conn.execute(text("""
                        INSERT INTO study_sessions (user_id, subject, topic, planned_duration, actual_duration, start_time, end_time, status, notes, productivity_rating, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """), (row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]))
                
                conn.commit()
                print(f"✅ {len(existing_data)} sessions restaurées")
            
            # Vérifier la nouvelle structure
            result = conn.execute(text("PRAGMA table_info(study_sessions)"))
            columns = result.fetchall()
            
            print("\n📋 Nouvelle structure de la table 'study_sessions':")
            for column in columns:
                print(f"   {column[1]} ({column[2]}) - {'NOT NULL' if column[3] else 'NULL'} - PK: {column[5]}")
            
            # Tester l'insertion
            print("\n🧪 Test d'insertion...")
            result = conn.execute(text("""
                INSERT INTO study_sessions (user_id, topic, subject, start_time, end_time, planned_duration, notes, status)
                VALUES (4, 'Test Session', 'Test Subject', '2025-01-20 10:00:00', '2025-01-20 12:00:00', 120, 'Test notes', 'planned')
            """))
            conn.commit()
            
            # Récupérer l'ID généré
            result = conn.execute(text("SELECT last_insert_rowid()"))
            last_id = result.fetchone()[0]
            print(f"✅ Test d'insertion réussi, ID généré: {last_id}")
            
            # Nettoyer la session de test
            conn.execute(text("DELETE FROM study_sessions WHERE id = ?"), (last_id,))
            conn.commit()
            print("✅ Session de test supprimée")
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")

if __name__ == "__main__":
    recreate_study_sessions_table() 