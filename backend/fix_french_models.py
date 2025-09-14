#!/usr/bin/env python3
"""
Script pour corriger le problème de relation entre FrenchLearningProfile et FrenchCompetencyProgress
"""
import sqlite3
import os

def fix_french_models():
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return False
    
    print(f"🔍 Correction des modèles français...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Vérifier si la colonne profile_id existe déjà
        cursor.execute("PRAGMA table_info(french_competency_progress)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'profile_id' not in columns:
            print("➕ Ajout de la colonne profile_id à french_competency_progress...")
            cursor.execute("""
                ALTER TABLE french_competency_progress 
                ADD COLUMN profile_id INTEGER REFERENCES french_learning_profiles(id)
            """)
            print("✅ Colonne profile_id ajoutée avec succès")
        else:
            print("ℹ️ La colonne profile_id existe déjà")
        
        # Vérifier si la table french_learning_profiles existe
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='french_learning_profiles'
        """)
        
        if not cursor.fetchone():
            print("➕ Création de la table french_learning_profiles...")
            cursor.execute("""
                CREATE TABLE french_learning_profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    learning_style VARCHAR NOT NULL,
                    french_level VARCHAR NOT NULL,
                    preferred_pace VARCHAR NOT NULL,
                    strengths TEXT,
                    weaknesses TEXT,
                    cognitive_profile TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES users (id)
                )
            """)
            print("✅ Table french_learning_profiles créée avec succès")
        
        # Vérifier si la table french_competency_progress existe
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='french_competency_progress'
        """)
        
        if not cursor.fetchone():
            print("➕ Création de la table french_competency_progress...")
            cursor.execute("""
                CREATE TABLE french_competency_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    competency_id INTEGER NOT NULL,
                    profile_id INTEGER,
                    current_level VARCHAR NOT NULL,
                    progress_percentage REAL DEFAULT 0.0,
                    last_assessed DATETIME,
                    next_assessment_date DATETIME,
                    attempts_count INTEGER DEFAULT 0,
                    best_score REAL DEFAULT 0.0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES users (id),
                    FOREIGN KEY (competency_id) REFERENCES french_competencies (id),
                    FOREIGN KEY (profile_id) REFERENCES french_learning_profiles (id)
                )
            """)
            print("✅ Table french_competency_progress créée avec succès")
        
        # Vérifier si la table french_competencies existe
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='french_competencies'
        """)
        
        if not cursor.fetchone():
            print("➕ Création de la table french_competencies...")
            cursor.execute("""
                CREATE TABLE french_competencies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR NOT NULL,
                    category VARCHAR NOT NULL,
                    difficulty_level VARCHAR NOT NULL,
                    description TEXT,
                    prerequisites TEXT,
                    estimated_hours INTEGER DEFAULT 2,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("✅ Table french_competencies créée avec succès")
        
        conn.commit()
        print("🎉 Correction terminée avec succès!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    fix_french_models()

