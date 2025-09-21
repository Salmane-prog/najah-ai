#!/usr/bin/env python3
"""
Script pour créer la table question_history
"""

import sqlite3
import os
from datetime import datetime

def create_question_history_table():
    """Créer la table question_history"""
    
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), "..", "data", "app.db")
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return False
    
    print(f"🔍 Connexion à la base de données: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Vérifier si la table existe déjà
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='question_history'")
        if cursor.fetchone():
            print("✅ Table question_history existe déjà")
            return True
        
        # Créer la table question_history
        cursor.execute("""
            CREATE TABLE question_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_id INTEGER NOT NULL,
                question_id INTEGER NOT NULL,
                question_text TEXT NOT NULL,
                difficulty VARCHAR(20) NOT NULL,
                topic VARCHAR(100),
                asked_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                student_response TEXT,
                is_correct INTEGER,
                FOREIGN KEY (test_id) REFERENCES french_adaptive_tests (id)
            )
        """)
        
        # Créer des index pour améliorer les performances
        cursor.execute("CREATE INDEX idx_question_history_test_id ON question_history(test_id)")
        cursor.execute("CREATE INDEX idx_question_history_question_id ON question_history(question_id)")
        cursor.execute("CREATE INDEX idx_question_history_difficulty ON question_history(difficulty)")
        
        conn.commit()
        print("✅ Table question_history créée avec succès")
        print("✅ Index créés pour optimiser les performances")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de la table: {e}")
        conn.rollback()
        return False
        
    finally:
        conn.close()

if __name__ == "__main__":
    create_question_history_table()














