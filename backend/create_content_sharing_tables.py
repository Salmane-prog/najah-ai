#!/usr/bin/env python3
"""Script pour créer les tables de partage de contenu"""

import sqlite3
import os
from pathlib import Path

def create_content_sharing_tables():
    """Créer les tables de partage de contenu"""
    
    # Chemin vers la base de données
    db_path = Path("../data/app.db")
    
    if not db_path.exists():
        print(f"❌ Base de données non trouvée: {db_path}")
        return
    
    # Créer la connexion
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🚀 Création des tables de partage de contenu...")
    
    try:
        # Table content_sharings
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS content_sharings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content_id INTEGER NOT NULL,
            shared_by INTEGER NOT NULL,
            shared_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            target_type VARCHAR(20) NOT NULL,
            target_ids TEXT, -- JSON string
            allow_download BOOLEAN DEFAULT 1,
            allow_view BOOLEAN DEFAULT 1,
            expiration_date TIMESTAMP NULL,
            notify_students BOOLEAN DEFAULT 1,
            custom_message TEXT,
            view_count INTEGER DEFAULT 0,
            download_count INTEGER DEFAULT 0,
            student_count INTEGER DEFAULT 0,
            FOREIGN KEY (content_id) REFERENCES contents (id),
            FOREIGN KEY (shared_by) REFERENCES users (id)
        )
        ''')
        
        # Table content_accesses
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS content_accesses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            sharing_id INTEGER NOT NULL,
            first_accessed TIMESTAMP NULL,
            last_accessed TIMESTAMP NULL,
            access_count INTEGER DEFAULT 0,
            can_view BOOLEAN DEFAULT 1,
            can_download BOOLEAN DEFAULT 1,
            FOREIGN KEY (content_id) REFERENCES contents (id),
            FOREIGN KEY (sharing_id) REFERENCES content_sharings (id),
            FOREIGN KEY (student_id) REFERENCES users (id)
        )
        ''')
        
        # Créer les index
        cursor.execute('CREATE INDEX IF NOT EXISTS ix_content_sharings_id ON content_sharings (id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS ix_content_accesses_id ON content_accesses (id)')
        
        conn.commit()
        print("✅ Tables de partage de contenu créées avec succès")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    create_content_sharing_tables()



