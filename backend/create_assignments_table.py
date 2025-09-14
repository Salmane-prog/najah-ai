import sqlite3
import os
from pathlib import Path

def create_assignments_table():
    db_path = Path("../data/app.db")
    if not db_path.exists():
        print(f"❌ Base de données non trouvée: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🚀 Création de la table des assignations...")
    
    try:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(255) NOT NULL,
            description TEXT NOT NULL,
            subject VARCHAR(100) NOT NULL,
            assignment_type VARCHAR(20) NOT NULL,
            target_ids TEXT, -- JSON string
            due_date TIMESTAMP NULL,
            priority VARCHAR(20) DEFAULT 'medium',
            estimated_time INTEGER NULL,
            status VARCHAR(20) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_by INTEGER NOT NULL,
            FOREIGN KEY (created_by) REFERENCES users (id)
        )
        ''')
        
        cursor.execute('CREATE INDEX IF NOT EXISTS ix_assignments_id ON assignments (id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS ix_assignments_created_by ON assignments (created_by)')
        
        conn.commit()
        print("✅ Table des assignations créée avec succès")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de la table: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    create_assignments_table()



