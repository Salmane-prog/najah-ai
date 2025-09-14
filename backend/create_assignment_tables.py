import sqlite3
from pathlib import Path

def create_assignment_tables():
    """Créer les tables pour les soumissions et le suivi des devoirs"""
    
    # Chemin vers la base de données
    db_path = Path(__file__).parent.parent / "data" / "app.db"
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔧 Création des tables pour les devoirs...")
        
        # Table assignment_submissions
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assignment_submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                assignment_id INTEGER NOT NULL,
                student_id INTEGER NOT NULL,
                submitted_file TEXT NOT NULL,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'submitted',
                grade INTEGER,
                feedback TEXT,
                graded_at TIMESTAMP,
                graded_by INTEGER,
                FOREIGN KEY (assignment_id) REFERENCES assignments (id),
                FOREIGN KEY (student_id) REFERENCES users (id),
                FOREIGN KEY (graded_by) REFERENCES users (id)
            )
        """)
        print("✅ Table assignment_submissions créée")
        
        # Table student_assignments
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS student_assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                assignment_id INTEGER NOT NULL,
                student_id INTEGER NOT NULL,
                status TEXT DEFAULT 'assigned',
                started_at TIMESTAMP,
                submitted_at TIMESTAMP,
                completed_at TIMESTAMP,
                time_spent INTEGER,
                notes TEXT,
                FOREIGN KEY (assignment_id) REFERENCES assignments (id),
                FOREIGN KEY (student_id) REFERENCES users (id)
            )
        """)
        print("✅ Table student_assignments créée")
        
        # Créer les index pour améliorer les performances
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_submission_assignment ON assignment_submissions(assignment_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_submission_student ON assignment_submissions(student_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_student_assignment ON student_assignments(assignment_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_student_assignment_student ON student_assignments(student_id)")
        print("✅ Index créés")
        
        # Valider les changements
        conn.commit()
        print("\n🎉 Tables créées avec succès !")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        conn.rollback()
        return False
        
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("🚀 Création des tables pour les devoirs...")
    success = create_assignment_tables()
    
    if success:
        print("\n✅ Script terminé avec succès !")
    else:
        print("\n💥 Échec du script !")

