#!/usr/bin/env python3
"""
Script pour corriger les tables manquantes et les erreurs de base de données
"""

import sqlite3
import os
from pathlib import Path

def create_missing_tables():
    """Crée toutes les tables manquantes"""
    
    # Chemin vers la base de données
    db_path = Path("data/app.db")
    
    if not db_path.exists():
        print("❌ Base de données non trouvée")
        return
    
    print("🔧 Création des tables manquantes...")
    
    # Connexion à la base de données
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 1. Table detailed_reports si elle n'existe pas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS detailed_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                report_type TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                period_start TEXT NOT NULL,
                period_end TEXT NOT NULL,
                data TEXT,
                insights TEXT,
                recommendations TEXT,
                is_exported BOOLEAN DEFAULT 0,
                exported_at TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Table detailed_reports créée")
        
        # 2. Table subject_progress_reports
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subject_progress_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                subject TEXT NOT NULL,
                period_start TEXT NOT NULL,
                period_end TEXT NOT NULL,
                total_score REAL NOT NULL,
                max_score REAL NOT NULL,
                percentage REAL NOT NULL,
                improvement_rate REAL,
                topics_covered TEXT,
                strengths TEXT,
                weaknesses TEXT,
                recommendations TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Table subject_progress_reports créée")
        
        # 3. Table analytics_reports
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analytics_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                analytics_type TEXT NOT NULL,
                period_start TEXT NOT NULL,
                period_end TEXT NOT NULL,
                metrics TEXT,
                trends TEXT,
                insights TEXT,
                recommendations TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Table analytics_reports créée")
        
        # 4. Table advanced_homeworks
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS advanced_homeworks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                subject TEXT,
                class_id INTEGER,
                created_by INTEGER NOT NULL,
                due_date TEXT,
                priority TEXT DEFAULT 'medium',
                estimated_time INTEGER,
                max_score REAL,
                instructions TEXT,
                attachments TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Table advanced_homeworks créée")
        
        # 5. Table class_students si elle n'existe pas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS class_students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_id INTEGER NOT NULL,
                student_id INTEGER NOT NULL,
                joined_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Table class_students créée")
        
        # 6. Table ai_recommendations
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ai_recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                recommendation_type TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                content_id INTEGER,
                quiz_id INTEGER,
                learning_path_id INTEGER,
                confidence_score REAL DEFAULT 0.0,
                reason TEXT,
                is_accepted BOOLEAN DEFAULT 0,
                is_dismissed BOOLEAN DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Table ai_recommendations créée")
        
        # 7. Table ai_tutoring_sessions
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ai_tutoring_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                subject TEXT,
                topic TEXT,
                session_type TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT,
                duration INTEGER,
                status TEXT DEFAULT 'active',
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Table ai_tutoring_sessions créée")
        
        # 8. Table difficulty_detection
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS difficulty_detection (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                subject TEXT NOT NULL,
                topic TEXT NOT NULL,
                difficulty_level TEXT NOT NULL,
                confidence_score REAL DEFAULT 0.0,
                evidence TEXT,
                detected_at TEXT DEFAULT CURRENT_TIMESTAMP,
                is_resolved BOOLEAN DEFAULT 0,
                resolution_notes TEXT
            )
        """)
        print("✅ Table difficulty_detection créée")
        
        # Valider les changements
        conn.commit()
        print("\n🎉 Toutes les tables manquantes ont été créées avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables: {e}")
        conn.rollback()
    finally:
        conn.close()

def insert_sample_data():
    """Insère des données d'exemple pour tester"""
    
    db_path = Path("data/app.db")
    if not db_path.exists():
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Données d'exemple pour ai_recommendations
        cursor.execute("""
            INSERT OR IGNORE INTO ai_recommendations 
            (user_id, recommendation_type, title, description, confidence_score)
            VALUES 
            (4, 'content', 'Revoir les bases de l algebre', 'Base sur vos resultats recents', 0.85),
            (4, 'quiz', 'Quiz sur les equations', 'Pour renforcer vos competences', 0.78)
        """)
        
        # Données d'exemple pour subject_progress_reports
        cursor.execute("""
            INSERT OR IGNORE INTO subject_progress_reports 
            (user_id, subject, period_start, period_end, total_score, max_score, percentage)
            VALUES 
            (4, 'Mathematiques', '2025-08-01', '2025-08-11', 75.0, 100.0, 75.0),
            (4, 'Physique', '2025-08-01', '2025-08-11', 82.0, 100.0, 82.0)
        """)
        
        # Données d'exemple pour analytics_reports
        cursor.execute("""
            INSERT OR IGNORE INTO analytics_reports 
            (user_id, analytics_type, period_start, period_end, metrics)
            VALUES 
            (4, 'performance', '2025-08-01', '2025-08-11', '{"avg_score": 78.5, "improvement": 12.3}'),
            (4, 'engagement', '2025-08-01', '2025-08-11', '{"study_time": 45, "sessions": 8}')
        """)
        
        # Données d'exemple pour detailed_reports
        cursor.execute("""
            INSERT OR IGNORE INTO detailed_reports 
            (user_id, report_type, title, description, period_start, period_end)
            VALUES 
            (4, 'monthly', 'Rapport mensuel aout 2025', 'Resume des activites du mois', '2025-08-01', '2025-08-31')
        """)
        
        conn.commit()
        print("✅ Données d'exemple insérées")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'insertion des données: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("🔧 CORRECTION DES TABLES MANQUANTES")
    print("=" * 50)
    
    create_missing_tables()
    print()
    insert_sample_data()
    
    print("\n✅ Correction terminée!")
    print("💡 Redémarrez le serveur pour appliquer les changements")
