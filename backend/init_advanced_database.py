#!/usr/bin/env python3
"""
Script d'initialisation de la base de données avancée
Crée toutes les tables nécessaires pour les nouvelles fonctionnalités
"""

import sqlite3
import json
from datetime import datetime
import os

def create_advanced_tables():
    """Créer les tables avancées pour les nouvelles fonctionnalités"""
    
    # Connexion à la base de données
    db_path = "najah_ai.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données {db_path} non trouvée!")
        print("Création d'une nouvelle base de données...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🔧 Création des tables avancées...")
    
    try:
        # 1. Table des questions étendues
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS extended_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_text TEXT NOT NULL,
                question_type TEXT NOT NULL,
                subject TEXT NOT NULL,
                difficulty INTEGER NOT NULL,
                competency TEXT,
                learning_style TEXT,
                options TEXT,
                correct_answer TEXT NOT NULL,
                explanation TEXT,
                estimated_time INTEGER,
                cognitive_load REAL,
                tags TEXT,
                curriculum_standards TEXT,
                prerequisites TEXT,
                learning_objectives TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Table 'extended_questions' créée")
        
        # 2. Table des métadonnées des questions
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS question_metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id INTEGER NOT NULL,
                bloom_taxonomy_level TEXT,
                knowledge_type TEXT,
                cognitive_domain TEXT,
                difficulty_justification TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (question_id) REFERENCES extended_questions (id)
            )
        """)
        print("✅ Table 'question_metadata' créée")
        
        # 3. Table des tags
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS question_tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tag TEXT UNIQUE NOT NULL,
                category TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Table 'question_tags' créée")
        
        # 4. Table des relations questions-tags
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS question_tag_relations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id INTEGER NOT NULL,
                tag_id INTEGER NOT NULL,
                FOREIGN KEY (question_id) REFERENCES extended_questions (id),
                FOREIGN KEY (tag_id) REFERENCES question_tags (id)
            )
        """)
        print("✅ Table 'question_tag_relations' créée")
        
        # 5. Table des profils cognitifs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cognitive_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                learning_style TEXT NOT NULL,
                strengths TEXT,
                weaknesses TEXT,
                recommendations TEXT,
                confidence_level REAL,
                generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Table 'cognitive_profiles' créée")
        
        # 6. Table des analyses de réponses
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS response_analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                question_id INTEGER NOT NULL,
                response_time INTEGER,
                is_correct BOOLEAN NOT NULL,
                time_analysis TEXT,
                pattern TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Table 'response_analyses' créée")
        
        # 7. Table des capacités des étudiants (IRT)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS student_abilities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                ability_level REAL NOT NULL,
                confidence_interval TEXT,
                estimated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Table 'student_abilities' créée")
        
        # 8. Table des sessions adaptatives
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS adaptive_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                session_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                session_end TIMESTAMP,
                initial_difficulty INTEGER NOT NULL,
                final_difficulty INTEGER,
                questions_answered INTEGER DEFAULT 0,
                correct_answers INTEGER DEFAULT 0,
                total_time INTEGER,
                cognitive_load_tracking TEXT,
                adaptation_history TEXT
            )
        """)
        print("✅ Table 'adaptive_sessions' créée")
        
        # Créer des index pour améliorer les performances
        print("🔧 Création des index...")
        
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_extended_questions_subject ON extended_questions(subject)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_extended_questions_difficulty ON extended_questions(difficulty)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_extended_questions_type ON extended_questions(question_type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cognitive_profiles_student ON cognitive_profiles(student_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_response_analyses_student ON response_analyses(student_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_student_abilities_student ON student_abilities(student_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_adaptive_sessions_student ON adaptive_sessions(student_id)")
        
        print("✅ Index créés")
        
        # Insérer quelques tags de base
        print("🔧 Insertion des tags de base...")
        
        base_tags = [
            ("mathématiques", "matière", "Questions de mathématiques"),
            ("français", "matière", "Questions de français"),
            ("sciences", "matière", "Questions de sciences"),
            ("histoire", "matière", "Questions d'histoire"),
            ("géographie", "matière", "Questions de géographie"),
            ("facile", "difficulté", "Questions de niveau facile"),
            ("moyen", "difficulté", "Questions de niveau moyen"),
            ("difficile", "difficulté", "Questions de niveau difficile"),
            ("QCM", "type", "Questions à choix multiples"),
            ("texte_libre", "type", "Questions à réponse libre"),
            ("image", "type", "Questions avec support image"),
            ("logique", "compétence", "Développement de la logique"),
            ("mémoire", "compétence", "Exercice de la mémoire"),
            ("compréhension", "compétence", "Compréhension de texte"),
            ("calcul", "compétence", "Calculs mathématiques"),
            ("analyse", "compétence", "Analyse et réflexion"),
            ("visuel", "style", "Style d'apprentissage visuel"),
            ("auditif", "style", "Style d'apprentissage auditif"),
            ("kinesthésique", "style", "Style d'apprentissage kinesthésique"),
            ("lecture_écriture", "style", "Style d'apprentissage lecture/écriture")
        ]
        
        for tag, category, description in base_tags:
            try:
                cursor.execute("""
                    INSERT OR IGNORE INTO question_tags (tag, category, description)
                    VALUES (?, ?, ?)
                """, (tag, category, description))
            except Exception as e:
                print(f"⚠️ Erreur lors de l'insertion du tag {tag}: {e}")
        
        print("✅ Tags de base insérés")
        
        # Valider les changements
        conn.commit()
        print("✅ Toutes les tables ont été créées avec succès!")
        
        # Vérifier la structure
        print("\n🔍 Vérification de la structure des tables...")
        
        tables = [
            "extended_questions", "question_metadata", "question_tags", 
            "question_tag_relations", "cognitive_profiles", "response_analyses",
            "student_abilities", "adaptive_sessions"
        ]
        
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            print(f"   📋 {table}: {len(columns)} colonnes")
        
        # Compter les tags
        cursor.execute("SELECT COUNT(*) FROM question_tags")
        tag_count = cursor.fetchone()[0]
        print(f"   🏷️ Tags disponibles: {tag_count}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables: {e}")
        conn.rollback()
        raise
    
    finally:
        conn.close()

def test_database_connection():
    """Tester la connexion à la base de données"""
    try:
        conn = sqlite3.connect("najah_ai.db")
        cursor = conn.cursor()
        
        # Test simple
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        if result and result[0] == 1:
            print("✅ Connexion à la base de données réussie!")
            return True
        else:
            print("❌ Erreur de connexion à la base de données!")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False
    
    finally:
        conn.close()

if __name__ == "__main__":
    print("🚀 Initialisation de la base de données avancée...")
    print("=" * 50)
    
    # Créer les tables
    create_advanced_tables()
    
    print("\n" + "=" * 50)
    
    # Tester la connexion
    test_database_connection()
    
    print("\n🎉 Initialisation terminée!")
    print("\n📋 Tables créées:")
    print("   - extended_questions (banque de questions étendue)")
    print("   - question_metadata (métadonnées des questions)")
    print("   - question_tags (tags de catégorisation)")
    print("   - question_tag_relations (relations questions-tags)")
    print("   - cognitive_profiles (profils cognitifs)")
    print("   - response_analyses (analyses des réponses)")
    print("   - student_abilities (capacités IRT)")
    print("   - adaptive_sessions (sessions adaptatives)")
    
    print("\n🔧 Prochaines étapes:")
    print("   1. Exécuter create_extended_question_bank.py pour peupler la banque")
    print("   2. Tester les endpoints avancés")
    print("   3. Intégrer les composants frontend")












