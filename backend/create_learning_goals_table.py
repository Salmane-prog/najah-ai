import sqlite3
import os

# Chemin vers la base de données
DB_PATH = 'database.db'

def create_learning_goals_table():
    """Créer la table learning_goals si elle n'existe pas."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Créer la table learning_goals
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_goals (
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
        print("✅ Table learning_goals créée avec succès!")
        
        # Vérifier la structure de la table
        cursor.execute("PRAGMA table_info(learning_goals)")
        columns = cursor.fetchall()
        print("\n📋 Structure de la table learning_goals:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
            
    except Exception as e:
        print(f"❌ Erreur lors de la création de la table: {e}")
        conn.rollback()
    finally:
        conn.close()

def insert_test_learning_goals():
    """Insérer des objectifs d'apprentissage de test."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Trouver un étudiant pour les tests
        cursor.execute("SELECT id FROM users WHERE role = 'student' LIMIT 1")
        student = cursor.fetchone()
        
        if not student:
            print("❌ Aucun étudiant trouvé dans la base de données")
            return
            
        student_id = student[0]
        
        # Supprimer les anciens objectifs de test
        cursor.execute("DELETE FROM learning_goals WHERE user_id = ?", (student_id,))
        
        # Insérer des objectifs de test
        test_goals = [
            {
                'title': 'Maîtriser les équations du second degré',
                'description': 'Être capable de résoudre toutes les équations du second degré',
                'subject': 'Mathématiques',
                'target_date': '2024-02-01 00:00:00',
                'progress': 75.0,
                'status': 'active'
            },
            {
                'title': 'Améliorer l\'expression écrite',
                'description': 'Écrire des textes plus fluides et structurés',
                'subject': 'Français',
                'target_date': '2024-03-01 00:00:00',
                'progress': 40.0,
                'status': 'active'
            },
            {
                'title': 'Comprendre la photosynthèse',
                'description': 'Maîtriser les mécanismes de la photosynthèse',
                'subject': 'Sciences',
                'target_date': '2024-01-25 00:00:00',
                'progress': 60.0,
                'status': 'active'
            }
        ]
        
        for goal in test_goals:
            cursor.execute('''
                INSERT INTO learning_goals (title, description, subject, target_date, progress, status, user_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                goal['title'],
                goal['description'],
                goal['subject'],
                goal['target_date'],
                goal['progress'],
                goal['status'],
                student_id
            ))
        
        conn.commit()
        print(f"✅ {len(test_goals)} objectifs d'apprentissage de test insérés!")
        
        # Vérifier les données insérées
        cursor.execute("SELECT * FROM learning_goals WHERE user_id = ?", (student_id,))
        goals = cursor.fetchall()
        print(f"\n📊 Objectifs créés pour l'étudiant {student_id}:")
        for goal in goals:
            print(f"  - {goal[1]} ({goal[3]}) - {goal[5]}%")
            
    except Exception as e:
        print(f"❌ Erreur lors de l'insertion des objectifs de test: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("🚀 Création de la table learning_goals...")
    create_learning_goals_table()
    
    print("\n📝 Insertion d'objectifs de test...")
    insert_test_learning_goals()
    
    print("\n✅ Script terminé!") 