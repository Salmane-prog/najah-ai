#!/usr/bin/env python3
"""
Script de migration pour les tables avancées - Version simplifiée
"""
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from core.database import engine

def create_new_tables():
    """Créer uniquement les nouvelles tables"""
    print("🔧 Création des nouvelles tables avancées...")
    
    try:
        with engine.connect() as conn:
            # Table learning_path_steps
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS learning_path_steps (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    learning_path_id INTEGER NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    step_type VARCHAR(50) NOT NULL,
                    content_id INTEGER,
                    quiz_id INTEGER,
                    "order" INTEGER NOT NULL,
                    estimated_duration INTEGER DEFAULT 15,
                    is_required BOOLEAN DEFAULT 1,
                    prerequisites JSON,
                    created_at DATETIME,
                    updated_at DATETIME,
                    FOREIGN KEY (learning_path_id) REFERENCES learning_paths (id),
                    FOREIGN KEY (content_id) REFERENCES contents (id),
                    FOREIGN KEY (quiz_id) REFERENCES quizzes (id)
                )
            """))
            
            # Table student_progress
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS student_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    learning_path_id INTEGER NOT NULL,
                    current_step_id INTEGER,
                    completed_steps JSON,
                    progress_percentage FLOAT DEFAULT 0.0,
                    started_at DATETIME,
                    last_activity DATETIME,
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (student_id) REFERENCES users (id),
                    FOREIGN KEY (learning_path_id) REFERENCES learning_paths (id),
                    FOREIGN KEY (current_step_id) REFERENCES learning_path_steps (id)
                )
            """))
            
            # Table class_analytics
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS class_analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    class_id INTEGER NOT NULL,
                    date DATETIME,
                    total_students INTEGER DEFAULT 0,
                    active_students INTEGER DEFAULT 0,
                    average_progress FLOAT DEFAULT 0.0,
                    completed_quizzes INTEGER DEFAULT 0,
                    average_score FLOAT DEFAULT 0.0,
                    weak_subjects JSON,
                    strong_subjects JSON,
                    FOREIGN KEY (class_id) REFERENCES class_groups (id)
                )
            """))
            
            # Table student_analytics
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS student_analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    class_id INTEGER,
                    date DATETIME,
                    total_quizzes INTEGER DEFAULT 0,
                    average_score FLOAT DEFAULT 0.0,
                    progress_percentage FLOAT DEFAULT 0.0,
                    time_spent INTEGER DEFAULT 0,
                    completed_contents INTEGER DEFAULT 0,
                    weak_subjects JSON,
                    strong_subjects JSON,
                    learning_style VARCHAR(50),
                    FOREIGN KEY (student_id) REFERENCES users (id),
                    FOREIGN KEY (class_id) REFERENCES class_groups (id)
                )
            """))
            
            # Table real_time_activities
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS real_time_activities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    activity_type VARCHAR(50) NOT NULL,
                    activity_data JSON,
                    timestamp DATETIME,
                    session_id VARCHAR(255),
                    FOREIGN KEY (student_id) REFERENCES users (id)
                )
            """))
            
            conn.commit()
            print("✅ Nouvelles tables créées avec succès!")
            return True
            
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables: {e}")
        return False

def update_existing_tables():
    """Mettre à jour les tables existantes"""
    print("🔄 Mise à jour des tables existantes...")
    
    try:
        with engine.connect() as conn:
            # Vérifier et ajouter les colonnes à learning_paths
            result = conn.execute(text("PRAGMA table_info(learning_paths);"))
            columns = [row[1] for row in result]
            
            new_columns = [
                ("level", "TEXT"),
                ("estimated_duration", "INTEGER DEFAULT 30"),
                ("is_adaptive", "BOOLEAN DEFAULT 0"),
                ("created_by", "INTEGER"),
                ("created_at", "DATETIME"),
                ("updated_at", "DATETIME")
            ]
            
            for col_name, col_type in new_columns:
                if col_name not in columns:
                    conn.execute(text(f"ALTER TABLE learning_paths ADD COLUMN {col_name} {col_type};"))
                    print(f"✅ Colonne {col_name} ajoutée à learning_paths")
            
            # Vérifier et ajouter les colonnes à class_groups
            result = conn.execute(text("PRAGMA table_info(class_groups);"))
            columns = [row[1] for row in result]
            
            new_class_columns = [
                ("level", "TEXT"),
                ("subject", "TEXT"),
                ("max_students", "INTEGER DEFAULT 30"),
                ("is_active", "BOOLEAN DEFAULT 1"),
                ("created_at", "DATETIME")
            ]
            
            for col_name, col_type in new_class_columns:
                if col_name not in columns:
                    conn.execute(text(f"ALTER TABLE class_groups ADD COLUMN {col_name} {col_type};"))
                    print(f"✅ Colonne {col_name} ajoutée à class_groups")
            
            # Vérifier et ajouter les colonnes à users
            result = conn.execute(text("PRAGMA table_info(users);"))
            columns = [row[1] for row in result]
            
            if "is_active" not in columns:
                conn.execute(text("ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT 1;"))
                print("✅ Colonne is_active ajoutée à users")
            
            conn.commit()
            print("✅ Tables existantes mises à jour")
            return True
            
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour des tables: {e}")
        return False

def create_sample_data():
    """Créer des données d'exemple"""
    print("📝 Création de données d'exemple...")
    
    try:
        with engine.connect() as conn:
            # Créer un enseignant de test
            conn.execute(text("""
                INSERT OR IGNORE INTO users (username, email, hashed_password, role)
                VALUES ('teacher_test', 'teacher@test.com', 
                '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj3bp.gS.Oe', 'teacher')
            """))
            
            # Récupérer l'ID de l'enseignant
            result = conn.execute(text("SELECT id FROM users WHERE email = 'teacher@test.com'"))
            teacher_id = result.fetchone()[0]
            
            # Créer une classe de test
            conn.execute(text("""
                INSERT OR IGNORE INTO class_groups (name, description, teacher_id, level, subject, max_students)
                VALUES ('Classe Test', 'Classe de test pour l''interface avancée', ?, 'middle', 'Mathématiques', 25)
            """), (teacher_id,))
            
            # Récupérer l'ID de la classe
            result = conn.execute(text("SELECT id FROM class_groups WHERE name = 'Classe Test'"))
            class_id = result.fetchone()[0]
            
            # Créer un parcours de test
            conn.execute(text("""
                INSERT OR IGNORE INTO learning_paths (name, description, objectives, level, estimated_duration, is_adaptive, created_by)
                VALUES ('Parcours Test', 'Parcours de test pour l''interface avancée', 'Tester les fonctionnalités avancées', 'intermediate', 15, 1, ?)
            """), (teacher_id,))
            
            # Récupérer l'ID du parcours
            result = conn.execute(text("SELECT id FROM learning_paths WHERE name = 'Parcours Test'"))
            path_id = result.fetchone()[0]
            
            # Créer des étapes de test
            steps = [
                ("Introduction aux concepts", "Première étape du parcours", "content", 1, 20),
                ("Quiz de vérification", "Quiz pour vérifier les acquis", "quiz", 2, 15),
                ("Exercices pratiques", "Application des concepts", "activity", 3, 30)
            ]
            
            for title, description, step_type, order_num, duration in steps:
                conn.execute(text("""
                    INSERT OR IGNORE INTO learning_path_steps 
                    (learning_path_id, title, description, step_type, "order", estimated_duration)
                    VALUES (?, ?, ?, ?, ?, ?)
                """), (path_id, title, description, step_type, order_num, duration))
            
            conn.commit()
            print("✅ Données d'exemple créées avec succès")
            
    except Exception as e:
        print(f"❌ Erreur lors de la création des données d'exemple: {e}")

def main():
    """Fonction principale"""
    print("🚀 Migration vers l'interface enseignant avancée")
    print("=" * 60)
    
    # Créer les nouvelles tables
    if not create_new_tables():
        print("❌ Échec de la création des nouvelles tables")
        return
    
    # Mettre à jour les tables existantes
    if not update_existing_tables():
        print("❌ Échec de la mise à jour des tables existantes")
        return
    
    # Créer des données d'exemple
    create_sample_data()
    
    print("\n" + "=" * 60)
    print("✅ Migration terminée avec succès!")
    print("\n📋 Nouvelles fonctionnalités disponibles:")
    print("   • Gestion avancée des classes")
    print("   • Création de parcours avec étapes")
    print("   • Suivi temps réel des étudiants")
    print("   • Analytics détaillés")
    print("   • Rapports avancés")
    print("\n🔗 Endpoints disponibles:")
    print("   • GET /api/v1/teacher/classes/")
    print("   • POST /api/v1/teacher/classes/")
    print("   • GET /api/v1/teacher/classes/{class_id}/analytics")
    print("   • POST /api/v1/teacher/learning-paths/")
    print("   • GET /api/v1/teacher/realtime/dashboard")
    print("   • GET /api/v1/teacher/reports/student/{student_id}")
    print("   • GET /api/v1/teacher/reports/class/{class_id}")

if __name__ == "__main__":
    main() 