#!/usr/bin/env python3
"""
Script complet pour recréer toutes les tables manquantes
"""

import sqlite3
import os
from pathlib import Path

def recreate_database():
    """Recrée complètement la base de données avec toutes les tables nécessaires"""
    
    # Chemin vers la base de données
    db_path = Path("data/app.db")
    
    print(f"🔧 Recréation de la base de données: {db_path.absolute()}")
    
    # Supprimer la base existante si elle existe
    if db_path.exists():
        print("🗑️ Suppression de l'ancienne base de données...")
        os.remove(db_path)
    
    # Créer le dossier data s'il n'existe pas
    db_path.parent.mkdir(exist_ok=True)
    
    # Connexion à la nouvelle base de données
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("📋 Création des tables...")
        
        # 1. Table detailed_reports
        cursor.execute("""
            CREATE TABLE detailed_reports (
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
            CREATE TABLE subject_progress_reports (
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
            CREATE TABLE analytics_reports (
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
            CREATE TABLE advanced_homeworks (
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
        
        # 5. Table class_students
        cursor.execute("""
            CREATE TABLE class_students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_id INTEGER NOT NULL,
                student_id INTEGER NOT NULL,
                joined_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Table class_students créée")
        
        # 6. Table ai_recommendations
        cursor.execute("""
            CREATE TABLE ai_recommendations (
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
            CREATE TABLE ai_tutoring_sessions (
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
            CREATE TABLE difficulty_detection (
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
        
        # 9. Table ai_advanced_analytics
        cursor.execute("""
            CREATE TABLE ai_advanced_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                analytics_type TEXT NOT NULL,
                data TEXT,
                insights TEXT,
                predictions TEXT,
                trends TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Table ai_advanced_analytics créée")
        
        # Valider les changements
        conn.commit()
        print("\n🎉 Base de données recréée avec succès!")
        
        # Vérifier que les tables existent
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        print(f"\n📊 Tables créées ({len(tables)}):")
        for table in sorted(tables):
            print(f"   - {table}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        conn.rollback()
    finally:
        conn.close()

def insert_sample_data():
    """Insère des données d'exemple pour tester"""
    
    db_path = Path("data/app.db")
    if not db_path.exists():
        print("❌ Base de données non trouvée")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("\n📝 Insertion des données d'exemple...")
        
        # Données pour detailed_reports
        cursor.execute("""
            INSERT INTO detailed_reports 
            (user_id, report_type, title, description, period_start, period_end)
            VALUES 
            (4, 'monthly', 'Rapport mensuel aout 2025', 'Resume des activites du mois', '2025-08-01', '2025-08-31'),
            (4, 'weekly', 'Rapport hebdomadaire semaine 32', 'Progression de la semaine', '2025-08-04', '2025-08-10')
        """)
        
        # Données pour subject_progress_reports
        cursor.execute("""
            INSERT INTO subject_progress_reports 
            (user_id, subject, period_start, period_end, total_score, max_score, percentage)
            VALUES 
            (4, 'Mathematiques', '2025-08-01', '2025-08-11', 75.0, 100.0, 75.0),
            (4, 'Physique', '2025-08-01', '2025-08-11', 82.0, 100.0, 82.0),
            (4, 'Chimie', '2025-08-01', '2025-08-11', 68.0, 100.0, 68.0)
        """)
        
        # Données pour analytics_reports
        cursor.execute("""
            INSERT INTO analytics_reports 
            (user_id, analytics_type, period_start, period_end, metrics)
            VALUES 
            (4, 'performance', '2025-08-01', '2025-08-11', '{"avg_score": 78.5, "improvement": 12.3}'),
            (4, 'engagement', '2025-08-01', '2025-08-11', '{"study_time": 45, "sessions": 8}'),
            (4, 'learning_patterns', '2025-08-01', '2025-08-11', '{"preferred_time": "morning", "focus_duration": 25}')
        """)
        
        # Données pour ai_recommendations
        cursor.execute("""
            INSERT INTO ai_recommendations 
            (user_id, recommendation_type, title, description, confidence_score)
            VALUES 
            (4, 'content', 'Revoir les bases de l algebre', 'Base sur vos resultats recents', 0.85),
            (4, 'quiz', 'Quiz sur les equations', 'Pour renforcer vos competences', 0.78),
            (4, 'study_session', 'Session de revision mathematiques', 'Planifier 2h de revision', 0.92)
        """)
        
        # Données pour ai_tutoring_sessions
        cursor.execute("""
            INSERT INTO ai_tutoring_sessions 
            (user_id, subject, topic, session_type, start_time, duration)
            VALUES 
            (4, 'Mathematiques', 'Equations du second degre', 'revision', '2025-08-12 14:00:00', 60),
            (4, 'Physique', 'Mecanique classique', 'explication', '2025-08-13 10:00:00', 45)
        """)
        
        # Données pour difficulty_detection
        cursor.execute("""
            INSERT INTO difficulty_detection 
            (user_id, subject, topic, difficulty_level, confidence_score, evidence)
            VALUES 
            (4, 'Mathematiques', 'Calcul integral', 'high', 0.87, 'Echecs repetes aux exercices'),
            (4, 'Chimie', 'Stoechiometrie', 'medium', 0.65, 'Resultats variables')
        """)
        
        # Données pour class_students
        cursor.execute("""
            INSERT INTO class_students 
            (class_id, student_id)
            VALUES 
            (1, 4),
            (2, 4)
        """)
        
        conn.commit()
        print("✅ Données d'exemple insérées avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'insertion des données: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("🔧 RECRÉATION COMPLÈTE DE LA BASE DE DONNÉES")
    print("=" * 60)
    
    recreate_database()
    insert_sample_data()
    
    print("\n" + "=" * 60)
    print("✅ RECRÉATION TERMINÉE!")
    print("💡 IMPORTANT: Redémarrez le serveur backend maintenant!")
    print("🚀 Les erreurs 500 et 404 devraient disparaître")




