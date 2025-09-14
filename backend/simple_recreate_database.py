#!/usr/bin/env python3
"""
Script simple pour recréer la base de données
"""

import os
import sys

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import engine, SessionLocal
from sqlalchemy import text

def recreate_database_simple():
    """Recrée la base de données de manière simple"""
    print("Suppression de la base de donnees existante...")
    
    # Supprimer le fichier de base de données
    db_path = "data/app.db"
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Base de donnees supprimee")
    else:
        print("Base de donnees n'existait pas")
    
    # Créer les tables de base
    print("Creation des tables de base...")
    
    db = SessionLocal()
    try:
        # Créer les tables essentielles une par une
        tables_sql = [
            """CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email VARCHAR(255) UNIQUE NOT NULL,
                username VARCHAR(100) UNIQUE NOT NULL,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                role VARCHAR(20) NOT NULL DEFAULT 'student',
                is_active BOOLEAN DEFAULT TRUE,
                hashed_password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
            
            """CREATE TABLE class_groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                teacher_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
            
            """CREATE TABLE class_students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_id INTEGER NOT NULL,
                student_id INTEGER NOT NULL,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
            
            """CREATE TABLE quizzes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                subject VARCHAR(100),
                level VARCHAR(20) DEFAULT 'medium',
                created_by INTEGER,
                time_limit INTEGER DEFAULT 30,
                max_score INTEGER DEFAULT 100,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
            
            """CREATE TABLE questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quiz_id INTEGER NOT NULL,
                question_text TEXT NOT NULL,
                question_type VARCHAR(20) DEFAULT 'mcq',
                points INTEGER DEFAULT 1,
                order_num INTEGER DEFAULT 1,
                options TEXT,
                correct_answer TEXT
            )""",
            
            """CREATE TABLE quiz_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quiz_id INTEGER NOT NULL,
                student_id INTEGER NOT NULL,
                score INTEGER NOT NULL,
                max_score INTEGER NOT NULL,
                time_taken INTEGER,
                is_completed BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
            
            """CREATE TABLE contents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                content_type VARCHAR(50) NOT NULL,
                subject VARCHAR(100),
                level VARCHAR(20) DEFAULT 'beginner',
                file_url VARCHAR(500),
                created_by INTEGER,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
            
            """CREATE TABLE detailed_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                report_type VARCHAR(50) NOT NULL,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                period_start TIMESTAMP NOT NULL,
                period_end TIMESTAMP NOT NULL,
                data TEXT NOT NULL,
                insights TEXT,
                recommendations TEXT,
                is_exported BOOLEAN DEFAULT FALSE,
                exported_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
            
            """CREATE TABLE subject_progress_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                subject VARCHAR(100) NOT NULL,
                period_start TIMESTAMP NOT NULL,
                period_end TIMESTAMP NOT NULL,
                total_score REAL NOT NULL,
                max_score REAL NOT NULL,
                percentage REAL NOT NULL,
                improvement_rate REAL,
                topics_covered TEXT,
                strengths TEXT,
                weaknesses TEXT,
                recommendations TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
            
            """CREATE TABLE analytics_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                analytics_type VARCHAR(50) NOT NULL,
                period_start TIMESTAMP NOT NULL,
                period_end TIMESTAMP NOT NULL,
                metrics TEXT NOT NULL,
                trends TEXT,
                insights TEXT,
                recommendations TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
            
            """CREATE TABLE ai_recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                recommendation_type VARCHAR(50) NOT NULL,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                content_id INTEGER,
                quiz_id INTEGER,
                learning_path_id INTEGER,
                confidence_score REAL DEFAULT 0.0,
                reason TEXT,
                is_accepted BOOLEAN DEFAULT FALSE,
                is_dismissed BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
            
            """CREATE TABLE ai_tutoring_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                subject VARCHAR(100),
                topic VARCHAR(255),
                session_type VARCHAR(50) DEFAULT 'general',
                start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_time TIMESTAMP,
                duration INTEGER,
                status VARCHAR(20) DEFAULT 'active',
                notes TEXT
            )""",
            
            """CREATE TABLE difficulty_detections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                subject VARCHAR(100) NOT NULL,
                topic VARCHAR(255) NOT NULL,
                difficulty_level VARCHAR(20) NOT NULL,
                confidence_score REAL DEFAULT 0.0,
                evidence TEXT,
                detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_resolved BOOLEAN DEFAULT FALSE,
                resolution_notes TEXT
            )""",
            
            """CREATE TABLE advanced_homeworks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                subject VARCHAR(100) NOT NULL,
                class_id INTEGER,
                created_by INTEGER NOT NULL,
                due_date TIMESTAMP NOT NULL,
                priority VARCHAR(20) DEFAULT 'medium',
                estimated_time INTEGER,
                max_score REAL DEFAULT 100.0,
                instructions TEXT,
                attachments TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP
            )"""
        ]
        
        for i, sql in enumerate(tables_sql):
            try:
                db.execute(text(sql))
                print(f"OK - Table {i+1} creee")
            except Exception as e:
                print(f"ERREUR - Table {i+1}: {e}")
        
        db.commit()
        print("Tables creees avec succes")
        
    except Exception as e:
        print(f"ERREUR - Erreur lors de la creation des tables: {e}")
        db.rollback()
    finally:
        db.close()
    
    # Créer des données d'exemple
    create_sample_data()
    
    print("Base de donnees recreee avec succes!")

def create_sample_data():
    """Crée des données d'exemple"""
    print("Creation de donnees d'exemple...")
    
    db = SessionLocal()
    try:
        # Créer un utilisateur admin
        db.execute(text("""
            INSERT INTO users (email, username, first_name, last_name, role, is_active, hashed_password)
            VALUES ('admin@najah.ai', 'admin', 'Admin', 'Najah', 'admin', 1, 
                   '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.i8i')
        """))
        
        # Créer un utilisateur étudiant
        db.execute(text("""
            INSERT INTO users (email, username, first_name, last_name, role, is_active, hashed_password)
            VALUES ('student@najah.ai', 'student', 'Student', 'Test', 'student', 1, 
                   '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.i8i')
        """))
        
        # Créer une classe
        db.execute(text("""
            INSERT INTO class_groups (name, description, teacher_id)
            VALUES ('Classe Test', 'Classe de test pour demonstration', 1)
        """))
        
        # Créer un quiz
        db.execute(text("""
            INSERT INTO quizzes (title, description, subject, level, created_by, max_score)
            VALUES ('Quiz Test', 'Quiz de test', 'Mathematiques', 'medium', 1, 100)
        """))
        
        db.commit()
        print("Donnees d'exemple creees")
        
    except Exception as e:
        print(f"ERREUR - Erreur lors de la creation des donnees: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Demarrage de la recreation simple de la base de donnees...")
    recreate_database_simple()
    print("Script termine avec succes!")
