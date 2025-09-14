#!/usr/bin/env python3
"""
Script pour appliquer la migration des tables d'évaluation
"""
import sqlite3
import os

def apply_assessment_migration():
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return False
    
    print(f"🔍 Application de la migration des tables d'évaluation...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Créer la table assessments
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                assessment_type VARCHAR NOT NULL,
                title VARCHAR NOT NULL,
                description TEXT,
                status VARCHAR DEFAULT 'in_progress',
                started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                completed_at DATETIME,
                FOREIGN KEY (student_id) REFERENCES users (id)
            )
        """)
        
        # Créer la table assessment_questions
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assessment_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                assessment_id INTEGER NOT NULL,
                question_text TEXT NOT NULL,
                question_type VARCHAR NOT NULL,
                subject VARCHAR NOT NULL,
                difficulty VARCHAR NOT NULL,
                options TEXT,
                correct_answer VARCHAR NOT NULL,
                points REAL DEFAULT 1.0,
                "order" INTEGER DEFAULT 0,
                FOREIGN KEY (assessment_id) REFERENCES assessments (id)
            )
        """)
        
        # Créer la table assessment_results
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assessment_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                assessment_id INTEGER NOT NULL,
                student_id INTEGER NOT NULL,
                total_score REAL NOT NULL,
                max_score REAL NOT NULL,
                percentage REAL NOT NULL,
                subject_scores TEXT,
                difficulty_scores TEXT,
                completed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (assessment_id) REFERENCES assessments (id),
                FOREIGN KEY (student_id) REFERENCES users (id)
            )
        """)
        
        # Créer les index
        cursor.execute("CREATE INDEX IF NOT EXISTS ix_assessments_id ON assessments (id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS ix_assessment_questions_id ON assessment_questions (id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS ix_assessment_results_id ON assessment_results (id)")
        
        conn.commit()
        print("✅ Tables d'évaluation créées avec succès !")
        
        # Vérifier les tables créées
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'assessment%'")
        tables = cursor.fetchall()
        print(f"📋 Tables d'évaluation créées: {[table[0] for table in tables]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    print("🚀 Application de la migration des tables d'évaluation...")
    success = apply_assessment_migration()
    
    if success:
        print(f"\n✅ Migration réussie! Les tables d'évaluation sont prêtes.")
        print(f"   Vous pouvez maintenant tester l'évaluation initiale.")
    else:
        print(f"\n❌ Migration échouée. Vérifiez les erreurs ci-dessus.") 