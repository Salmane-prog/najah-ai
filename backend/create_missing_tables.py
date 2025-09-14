#!/usr/bin/env python3
"""
Script pour créer SEULEMENT les tables manquantes et un utilisateur de test
"""

import sqlite3
import os
from datetime import datetime

def create_missing_tables():
    """Créer seulement les tables manquantes"""
    
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'app.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return
    
    print(f"🔍 Création des tables manquantes dans: {db_path}")
    print("=" * 60)
    
    # Connexion à la base de données
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 1. Créer la table assessment_results (si elle n'existe pas)
        print("1. Création de la table assessment_results...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS assessment_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                assessment_id INTEGER NOT NULL,
                student_id INTEGER NOT NULL,
                score REAL NOT NULL,
                max_score REAL NOT NULL,
                percentage REAL NOT NULL,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                strengths TEXT,
                weaknesses TEXT,
                recommendations TEXT,
                FOREIGN KEY (assessment_id) REFERENCES assessments (id),
                FOREIGN KEY (student_id) REFERENCES users (id)
            )
        ''')
        print("✅ Table assessment_results créée/vérifiée")
        
        # 2. Créer la table learning_paths (si elle n'existe pas)
        print("2. Création de la table learning_paths...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_paths (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                subject TEXT NOT NULL,
                difficulty TEXT DEFAULT 'medium',
                estimated_duration INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✅ Table learning_paths créée/vérifiée")
        
        # 3. Créer la table learning_path_steps (si elle n'existe pas)
        print("3. Création de la table learning_path_steps...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_path_steps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                learning_path_id INTEGER NOT NULL,
                step_number INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                content_type TEXT,
                estimated_duration INTEGER,
                is_required BOOLEAN DEFAULT 1,
                is_active BOOLEAN DEFAULT 1,
                is_completed BOOLEAN DEFAULT 0,
                FOREIGN KEY (learning_path_id) REFERENCES learning_paths (id)
            )
        ''')
        print("✅ Table learning_path_steps créée/vérifiée")
        
        # 4. Créer la table student_learning_paths (si elle n'existe pas)
        print("4. Création de la table student_learning_paths...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS student_learning_paths (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                learning_path_id INTEGER NOT NULL,
                progress REAL DEFAULT 0.0,
                current_step INTEGER DEFAULT 1,
                total_steps INTEGER DEFAULT 1,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_completed BOOLEAN DEFAULT 0,
                FOREIGN KEY (student_id) REFERENCES users (id),
                FOREIGN KEY (learning_path_id) REFERENCES learning_paths (id)
            )
        ''')
        print("✅ Table student_learning_paths créée/vérifiée")
        
        # Valider les changements
        conn.commit()
        print("\n🎉 Tables manquantes créées avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables: {e}")
        conn.rollback()
    
    finally:
        conn.close()

def create_test_user():
    """Créer un utilisateur de test avec ID 30"""
    
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'app.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return
    
    print(f"\n👤 Création de l'utilisateur de test...")
    print("=" * 40)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Vérifier si l'utilisateur 30 existe déjà
        cursor.execute("SELECT id FROM users WHERE id = 30")
        existing_user = cursor.fetchone()
        
        if existing_user:
            print("✅ Utilisateur 30 existe déjà")
            return
        
        # Créer l'utilisateur 30
        cursor.execute('''
            INSERT INTO users (id, username, email, hashed_password, role, is_active, first_name, last_name, created_at)
            VALUES (30, 'student30', 'student30@test.com', 'test123', 'student', 1, 'Étudiant', 'Test', ?)
        ''', (datetime.now(),))
        
        print("✅ Utilisateur 30 créé avec succès")
        
        # Valider les changements
        conn.commit()
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de l'utilisateur: {e}")
        conn.rollback()
    
    finally:
        conn.close()

def create_test_data():
    """Créer des données de test pour l'utilisateur 30"""
    
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'app.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return
    
    print(f"\n🧪 Création des données de test...")
    print("=" * 40)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 1. Créer des évaluations de test pour l'utilisateur 30
        print("1. Création d'évaluations de test...")
        
        # Vérifier si des évaluations existent déjà pour l'utilisateur 30
        cursor.execute("SELECT COUNT(*) FROM assessments WHERE student_id = 30")
        existing_assessments = cursor.fetchone()[0]
        
        if existing_assessments == 0:
            cursor.execute('''
                INSERT INTO assessments (title, description, subject, difficulty, estimated_time, status, student_id, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', ('Évaluation Mathématiques', 'Test de connaissances en algèbre', 'Mathématiques', 'medium', 30, 'pending', 30, datetime.now()))
            
            cursor.execute('''
                INSERT INTO assessments (title, description, subject, difficulty, estimated_time, status, student_id, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', ('Évaluation Physique', 'Test de mécanique', 'Physique', 'easy', 25, 'completed', 30, datetime.now()))
            
            print("✅ 2 évaluations créées")
        else:
            print(f"✅ {existing_assessments} évaluations existent déjà")
        
        # 2. Créer des parcours d'apprentissage
        print("2. Création de parcours d'apprentissage...")
        
        # Vérifier si des parcours existent déjà
        cursor.execute("SELECT COUNT(*) FROM learning_paths")
        existing_paths = cursor.fetchone()[0]
        
        if existing_paths == 0:
            cursor.execute('''
                INSERT INTO learning_paths (title, subject, difficulty, estimated_duration, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', ('Parcours Mathématiques', 'Mathématiques', 'medium', 120, datetime.now()))
            
            cursor.execute('''
                INSERT INTO learning_paths (title, subject, difficulty, estimated_duration, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', ('Parcours Physique', 'Physique', 'easy', 90, datetime.now()))
            
            print("✅ 2 parcours créés")
        else:
            print(f"✅ {existing_paths} parcours existent déjà")
        
        # 3. Créer des relations étudiant-parcours
        print("3. Création des relations étudiant-parcours...")
        
        # Récupérer les IDs des parcours
        cursor.execute("SELECT id FROM learning_paths LIMIT 2")
        paths = cursor.fetchall()
        
        if len(paths) >= 2:
            path1_id = paths[0][0]
            path2_id = paths[1][0]
            
            # Vérifier si des relations existent déjà
            cursor.execute("SELECT COUNT(*) FROM student_learning_paths WHERE student_id = 30")
            existing_relations = cursor.fetchone()[0]
            
            if existing_relations == 0:
                cursor.execute('''
                    INSERT INTO student_learning_paths (student_id, learning_path_id, progress, current_step, total_steps, started_at, is_completed)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (30, path1_id, 25.0, 2, 8, '2024-01-15', 0))
                
                cursor.execute('''
                    INSERT INTO student_learning_paths (student_id, learning_path_id, progress, current_step, total_steps, started_at, is_completed)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (30, path2_id, 100.0, 5, 5, '2024-01-10', 1))
                
                print("✅ 2 relations étudiant-parcours créées")
            else:
                print(f"✅ {existing_relations} relations existent déjà")
        
        # Valider les changements
        conn.commit()
        print("\n🎉 Données de test créées avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des données: {e}")
        conn.rollback()
    
    finally:
        conn.close()

def verify_test_data():
    """Vérifier que les données de test ont été créées"""
    
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'app.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return
    
    print(f"\n🔍 Vérification des données de test...")
    print("=" * 50)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Vérifier l'utilisateur 30
        cursor.execute("SELECT id, username, role FROM users WHERE id = 30")
        user = cursor.fetchone()
        if user:
            print(f"✅ Utilisateur 30: {user}")
        else:
            print("❌ Utilisateur 30 non trouvé")
            return
        
        # Vérifier les évaluations
        cursor.execute("SELECT COUNT(*) FROM assessments WHERE student_id = 30")
        assessment_count = cursor.fetchone()[0]
        print(f"📊 Évaluations pour l'utilisateur 30: {assessment_count}")
        
        # Vérifier les parcours
        cursor.execute("SELECT COUNT(*) FROM student_learning_paths WHERE student_id = 30")
        path_count = cursor.fetchone()[0]
        print(f"📊 Parcours pour l'utilisateur 30: {path_count}")
        
        print(f"\n🎯 RÉSUMÉ:")
        print(f"   - Utilisateur 30: {'✅ Créé' if user else '❌ Manquant'}")
        print(f"   - Évaluations: {assessment_count}")
        print(f"   - Parcours: {path_count}")
        
        if user and assessment_count > 0 and path_count > 0:
            print(f"\n🎉 VOS WIDGETS DEVRAIENT MAINTENANT AFFICHER DES DONNÉES!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    print("🚀 CRÉATION DES TABLES MANQUANTES ET DONNÉES DE TEST")
    print("=" * 70)
    
    create_missing_tables()
    create_test_user()
    create_test_data()
    verify_test_data()
    
    print("\n🎉 SCRIPT TERMINÉ AVEC SUCCÈS!")
    print("🔄 Maintenant, rafraîchissez votre dashboard et testez les widgets!") 