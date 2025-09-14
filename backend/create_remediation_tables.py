#!/usr/bin/env python3
"""
Script pour créer les tables de remédiation dans la base de données
"""

import sqlite3
import os
from datetime import datetime

def create_remediation_tables():
    """Créer les tables de remédiation"""
    
    # Chemin vers la base de données
    db_path = "data/najah_ai.db"
    
    # Créer le dossier data s'il n'existe pas
    os.makedirs("data", exist_ok=True)
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔧 Création des tables de remédiation...")
        
        # Table des résultats de remédiation
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS remediation_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                topic TEXT NOT NULL,
                exercise_type TEXT NOT NULL,
                score INTEGER NOT NULL,
                max_score INTEGER NOT NULL,
                percentage REAL NOT NULL,
                time_spent INTEGER NOT NULL,
                weak_areas_improved TEXT,
                difficulty_level TEXT DEFAULT 'medium',
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES users (id)
            )
        """)
        print("✅ Table remediation_results créée")
        
        # Table des badges de remédiation
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS remediation_badges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                badge_type TEXT NOT NULL,
                badge_name TEXT NOT NULL,
                badge_description TEXT,
                badge_icon TEXT,
                earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT,
                FOREIGN KEY (student_id) REFERENCES users (id)
            )
        """)
        print("✅ Table remediation_badges créée")
        
        # Table du progrès de remédiation
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS remediation_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                topic TEXT NOT NULL,
                current_level INTEGER DEFAULT 0,
                previous_level INTEGER DEFAULT 0,
                improvement INTEGER DEFAULT 0,
                exercises_completed INTEGER DEFAULT 0,
                total_exercises INTEGER DEFAULT 0,
                success_rate REAL DEFAULT 0.0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES users (id)
            )
        """)
        print("✅ Table remediation_progress créée")
        
        # Créer des index pour améliorer les performances
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_remediation_results_student 
            ON remediation_results (student_id)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_remediation_results_topic 
            ON remediation_results (topic)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_remediation_badges_student 
            ON remediation_badges (student_id)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_remediation_progress_student 
            ON remediation_progress (student_id)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_remediation_progress_topic 
            ON remediation_progress (topic)
        """)
        
        print("✅ Index créés")
        
        # Insérer quelques données d'exemple
        print("📝 Insertion de données d'exemple...")
        
        # Vérifier si des utilisateurs existent
        cursor.execute("SELECT id FROM users LIMIT 1")
        user_exists = cursor.fetchone()
        
        if user_exists:
            student_id = user_exists[0]
            
            # Insérer un résultat d'exemple
            cursor.execute("""
                INSERT OR IGNORE INTO remediation_results 
                (student_id, topic, exercise_type, score, max_score, percentage, time_spent, weak_areas_improved)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                student_id,
                'fondamentaux',
                'quiz',
                2,
                3,
                67.0,
                180,
                '["fondamentaux"]'
            ))
            
            # Insérer un badge d'exemple
            cursor.execute("""
                INSERT OR IGNORE INTO remediation_badges 
                (student_id, badge_type, badge_name, badge_description, badge_icon, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                student_id,
                'first_quiz',
                'Premier Quiz',
                'Complétez votre premier quiz de remédiation',
                '🎯',
                '{"exercise_type": "quiz", "topic": "fondamentaux"}'
            ))
            
            # Insérer un progrès d'exemple
            cursor.execute("""
                INSERT OR IGNORE INTO remediation_progress 
                (student_id, topic, current_level, previous_level, improvement, exercises_completed, total_exercises, success_rate)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                student_id,
                'fondamentaux',
                6,
                5,
                1,
                1,
                1,
                67.0
            ))
            
            print("✅ Données d'exemple insérées")
        else:
            print("⚠️  Aucun utilisateur trouvé, données d'exemple non insérées")
        
        # Valider les changements
        conn.commit()
        print("✅ Changements validés")
        
        # Afficher la structure des tables
        print("\n📋 Structure des tables créées:")
        
        cursor.execute("PRAGMA table_info(remediation_results)")
        print("\nremediation_results:")
        for column in cursor.fetchall():
            print(f"  - {column[1]} ({column[2]})")
        
        cursor.execute("PRAGMA table_info(remediation_badges)")
        print("\nremediation_badges:")
        for column in cursor.fetchall():
            print(f"  - {column[1]} ({column[2]})")
        
        cursor.execute("PRAGMA table_info(remediation_progress)")
        print("\nremediation_progress:")
        for column in cursor.fetchall():
            print(f"  - {column[1]} ({column[2]})")
        
        print(f"\n🎉 Tables de remédiation créées avec succès dans {db_path}")
        
    except sqlite3.Error as e:
        print(f"❌ Erreur SQLite: {e}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    finally:
        if conn:
            conn.close()
            print("🔒 Connexion fermée")

def verify_tables():
    """Vérifier que les tables ont été créées correctement"""
    
    db_path = "data/najah_ai.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("\n🔍 Vérification des tables...")
        
        # Vérifier l'existence des tables
        tables = ['remediation_results', 'remediation_badges', 'remediation_progress']
        
        for table in tables:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if cursor.fetchone():
                print(f"✅ Table {table} existe")
                
                # Compter les enregistrements
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"   📊 {count} enregistrement(s)")
            else:
                print(f"❌ Table {table} n'existe pas")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")

if __name__ == "__main__":
    print("🚀 Création des tables de remédiation...")
    print("=" * 50)
    
    create_remediation_tables()
    verify_tables()
    
    print("\n" + "=" * 50)
    print("✨ Script terminé !")








