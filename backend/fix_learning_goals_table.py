import sqlite3

def fix_learning_goals_table():
    """Corriger la table learning_goals pour avoir un ID auto-increment."""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    try:
        # Supprimer la table existante
        cursor.execute("DROP TABLE IF EXISTS learning_goals")
        
        # Recréer la table avec AUTOINCREMENT
        cursor.execute('''
            CREATE TABLE learning_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                subject TEXT NOT NULL,
                target_date DATETIME,
                progress REAL DEFAULT 0.0,
                status TEXT DEFAULT 'active',
                user_id INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        print("✅ Table learning_goals recréée avec AUTOINCREMENT!")
        
        # Vérifier la structure
        cursor.execute("PRAGMA table_info(learning_goals)")
        columns = cursor.fetchall()
        print("\n📋 Nouvelle structure:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]}) - Auto: {col[5]}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_learning_goals_table() 