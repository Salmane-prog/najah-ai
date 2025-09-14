import sqlite3
import os

def create_tables_in_data_db():
    """Créer les tables manquantes dans data/app.db"""
    
    db_path = '../data/app.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données '{db_path}' non trouvée!")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🚀 Création des tables manquantes dans data/app.db...")
        print("=" * 60)
        
        # 1. Table quizzes
        print("📝 Création de la table quizzes...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quizzes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                subject TEXT NOT NULL,
                difficulty_level INTEGER DEFAULT 1,
                time_limit INTEGER DEFAULT 30,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        ''')
        print("✅ Table quizzes créée")
        
        # 2. Table questions
        print("📝 Création de la table questions...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quiz_id INTEGER NOT NULL,
                question_text TEXT NOT NULL,
                question_type TEXT DEFAULT 'multiple_choice',
                options TEXT, -- JSON string
                correct_answer TEXT NOT NULL,
                points INTEGER DEFAULT 1,
                difficulty_level INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (quiz_id) REFERENCES quizzes (id)
            )
        ''')
        print("✅ Table questions créée")
        
        # 3. Table quiz_results
        print("📝 Création de la table quiz_results...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quiz_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                quiz_id INTEGER NOT NULL,
                score INTEGER NOT NULL,
                max_score INTEGER NOT NULL,
                percentage REAL NOT NULL,
                time_spent INTEGER,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES users (id),
                FOREIGN KEY (quiz_id) REFERENCES quizzes (id)
            )
        ''')
        print("✅ Table quiz_results créée")
        
        # 4. Table quiz_assignments
        print("📝 Création de la table quiz_assignments...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quiz_assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                quiz_id INTEGER NOT NULL,
                assigned_by INTEGER NOT NULL,
                assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                due_date TIMESTAMP,
                is_completed BOOLEAN DEFAULT FALSE,
                completed_at TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES users (id),
                FOREIGN KEY (quiz_id) REFERENCES quizzes (id),
                FOREIGN KEY (assigned_by) REFERENCES users (id)
            )
        ''')
        print("✅ Table quiz_assignments créée")
        
        # 5. Tables de remédiation
        print("\n🔧 Création des tables de remédiation...")
        
        # Table remediation_results
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS remediation_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                topic TEXT NOT NULL,
                exercise_type TEXT NOT NULL CHECK (exercise_type IN ('quiz', 'reading', 'practice')),
                score INTEGER NOT NULL,
                max_score INTEGER NOT NULL,
                percentage REAL NOT NULL,
                time_spent INTEGER,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                weak_areas_improved TEXT, -- JSON string
                FOREIGN KEY (student_id) REFERENCES users (id)
            )
        ''')
        print("✅ Table remediation_results créée")
        
        # Table remediation_badges
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS remediation_badges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                badge_type TEXT NOT NULL,
                badge_name TEXT NOT NULL,
                description TEXT,
                earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                points INTEGER DEFAULT 0,
                FOREIGN KEY (student_id) REFERENCES users (id)
            )
        ''')
        print("✅ Table remediation_badges créée")
        
        # Table remediation_progress
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS remediation_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                topic TEXT NOT NULL,
                current_level INTEGER DEFAULT 1,
                previous_level INTEGER DEFAULT 1,
                improvement REAL DEFAULT 0.0,
                exercises_completed INTEGER DEFAULT 0,
                total_exercises INTEGER DEFAULT 0,
                success_rate REAL DEFAULT 0.0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES users (id)
            )
        ''')
        print("✅ Table remediation_progress créée")
        
        # Créer les index
        print("\n🔍 Création des index...")
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_quiz_results_student ON quiz_results(student_id)",
            "CREATE INDEX IF NOT EXISTS idx_quiz_results_quiz ON quiz_results(quiz_id)",
            "CREATE INDEX IF NOT EXISTS idx_remediation_results_student ON remediation_results(student_id)",
            "CREATE INDEX IF NOT EXISTS idx_remediation_results_topic ON remediation_results(topic)",
            "CREATE INDEX IF NOT EXISTS idx_remediation_progress_student ON remediation_progress(student_id)",
            "CREATE INDEX IF NOT EXISTS idx_remediation_progress_topic ON remediation_progress(topic)"
        ]
        
        for index in indexes:
            cursor.execute(index)
        print("✅ Index créés")
        
        # Valider les changements
        conn.commit()
        
        print("\n🔍 Vérification finale...")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print("📋 Tables finales dans data/app.db:")
        for table in tables:
            print(f"  ✅ {table[0]}")
        
        conn.close()
        print("\n✨ Toutes les tables ont été créées avec succès dans data/app.db!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables: {e}")
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    create_tables_in_data_db()








