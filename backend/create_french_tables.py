#!/usr/bin/env python3
"""
Script pour créer les tables françaises manquantes
"""

import sqlite3
import os

def create_french_tables():
    """Créer les tables françaises manquantes"""
    
    # Chemin vers la base de données
    db_path = "data/app.db"
    
    # Créer le dossier data s'il n'existe pas
    os.makedirs("data", exist_ok=True)
    
    print(f"🔧 Création des tables françaises dans {db_path}")
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Table des profils d'apprentissage français
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS french_learning_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                learning_style TEXT,
                french_level TEXT,
                preferred_pace TEXT,
                strengths TEXT,  -- JSON string
                weaknesses TEXT, -- JSON string
                cognitive_profile TEXT, -- JSON string
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES users (id)
            )
        """)
        
        # Table des tests adaptatifs français
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS french_adaptive_tests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                status TEXT DEFAULT 'in_progress',
                current_question_index INTEGER DEFAULT 0,
                total_questions INTEGER DEFAULT 20,
                current_difficulty INTEGER DEFAULT 1,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                final_score REAL,
                FOREIGN KEY (student_id) REFERENCES users (id)
            )
        """)
        
        # Table de l'historique des questions
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS question_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                question_id INTEGER NOT NULL,
                test_id INTEGER NOT NULL,
                answered_correctly BOOLEAN,
                difficulty_level INTEGER,
                response_time INTEGER,
                answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES users (id)
            )
        """)
        
        # Créer un profil d'exemple pour l'étudiant ID 30 (ClaN)
        cursor.execute("""
            INSERT OR IGNORE INTO french_learning_profiles 
            (student_id, learning_style, french_level, preferred_pace, strengths, weaknesses, cognitive_profile, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """, (
            30,  # student_id
            "Visuel-Kinesthésique",  # learning_style
            "Intermédiaire",  # french_level
            "Modéré",  # preferred_pace
            '["Grammaire", "Vocabulaire", "Compréhension écrite"]',  # strengths (JSON)
            '["Conjugaison", "Expression orale"]',  # weaknesses (JSON)
            '{"final_score": 75, "difficulty_breakdown": {"facile": 8, "moyen": 6, "difficile": 6}, "test_id": 67}',  # cognitive_profile (JSON)
        ))
        
        # Valider les changements
        conn.commit()
        
        print("✅ Tables françaises créées avec succès !")
        print("📊 Profil d'exemple créé pour l'étudiant ID 30")
        
        # Vérifier les tables créées
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%french%'")
        french_tables = cursor.fetchall()
        print(f"📋 Tables françaises disponibles: {[table[0] for table in french_tables]}")
        
        # Vérifier le profil créé
        cursor.execute("SELECT * FROM french_learning_profiles WHERE student_id = 30")
        profile = cursor.fetchone()
        if profile:
            print(f"👤 Profil trouvé: ID={profile[0]}, Style={profile[2]}, Niveau={profile[3]}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    create_french_tables()
