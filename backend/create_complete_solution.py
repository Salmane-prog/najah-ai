#!/usr/bin/env python3
"""
Script complet pour créer la solution complète :
1. Table assessment_assignments (liaison étudiants-évaluations)
2. Tables learning_paths manquantes
3. Utilisateur 30 et données de test
"""

import sqlite3
import os
from datetime import datetime

def create_assessment_assignments_table():
    """Créer la table de liaison étudiants-évaluations"""
    
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'app.db')
    
    print(f"🔗 CRÉATION DE LA TABLE ASSESSMENT_ASSIGNMENTS")
    print("=" * 60)
    print(f"📍 Base de données: {db_path}")
    print()
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Créer la table assessment_assignments
        print("📝 Création de la table assessment_assignments...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS assessment_assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                assessment_id INTEGER NOT NULL,
                status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'completed', 'overdue')),
                assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                due_date TIMESTAMP,
                started_at TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES users (id),
                FOREIGN KEY (assessment_id) REFERENCES assessments (id),
                UNIQUE(student_id, assessment_id)
            )
        ''')
        
        print("✅ Table assessment_assignments créée/vérifiée")
        
        # Créer un index pour améliorer les performances
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_assessment_assignments_student 
            ON assessment_assignments(student_id)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_assessment_assignments_assessment 
            ON assessment_assignments(assessment_id)
        ''')
        
        print("✅ Index de performance créés")
        
        # Valider les changements
        conn.commit()
        print("🎉 Table assessment_assignments prête!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        conn.rollback()
    
    finally:
        conn.close()

def create_learning_paths_tables():
    """Créer les 3 tables manquantes pour les parcours d'apprentissage"""
    
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'app.db')
    
    print(f"\n📚 CRÉATION DES TABLES LEARNING PATHS")
    print("-" * 50)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 1. Table learning_paths
        print("1. 📚 Création de la table learning_paths...")
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
        print("   ✅ Table learning_paths créée/vérifiée")
        
        # 2. Table learning_path_steps
        print("2. 🎯 Création de la table learning_path_steps...")
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
        print("   ✅ Table learning_path_steps créée/vérifiée")
        
        # 3. Table student_learning_paths
        print("3. 👤 Création de la table student_learning_paths...")
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
        print("   ✅ Table student_learning_paths créée/vérifiée")
        
        # Valider les changements
        conn.commit()
        print("\n🎉 3 tables learning_paths créées avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables: {e}")
        conn.rollback()
    
    finally:
        conn.close()

def create_test_user_30():
    """Créer l'utilisateur de test avec ID 30"""
    
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'app.db')
    
    print(f"\n👤 CRÉATION DE L'UTILISATEUR DE TEST")
    print("-" * 40)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Vérifier si l'utilisateur 30 existe déjà
        cursor.execute("SELECT id, username, role FROM users WHERE id = 30")
        existing_user = cursor.fetchone()
        
        if existing_user:
            print(f"✅ Utilisateur 30 existe déjà: {existing_user}")
            return existing_user[0]
        
        # Créer l'utilisateur 30 avec la bonne structure
        cursor.execute('''
            INSERT INTO users (id, username, email, full_name, role, created_at)
            VALUES (30, 'student30', 'student30@test.com', 'Étudiant Test 30', 'student', ?)
        ''', (datetime.now(),))
        
        print("✅ Utilisateur 30 créé avec succès")
        
        # Valider les changements
        conn.commit()
        return 30
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de l'utilisateur: {e}")
        conn.rollback()
        return None
    
    finally:
        conn.close()

def create_test_data_for_user_30():
    """Créer des données de test complètes pour l'utilisateur 30"""
    
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'app.db')
    
    print(f"\n🧪 CRÉATION DES DONNÉES DE TEST COMPLÈTES")
    print("-" * 50)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 1. Créer des évaluations de test
        print("1. 📝 Création d'évaluations de test...")
        
        # Vérifier si des évaluations existent déjà
        cursor.execute("SELECT COUNT(*) FROM assessments")
        existing_assessments = cursor.fetchone()[0]
        
        if existing_assessments == 0:
            # Créer des évaluations
            cursor.execute('''
                INSERT INTO assessments (title, description, category_id, total_points, time_limit, is_active, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', ('Évaluation Mathématiques', 'Test de connaissances en algèbre', 1, 20, 30, 1, datetime.now()))
            
            cursor.execute('''
                INSERT INTO assessments (title, description, category_id, total_points, time_limit, is_active, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', ('Évaluation Physique', 'Test de mécanique', 2, 25, 25, 1, datetime.now()))
            
            print("   ✅ 2 évaluations créées")
        else:
            print(f"   ✅ {existing_assessments} évaluations existent déjà")
        
        # 2. Créer des assignations d'évaluations pour l'utilisateur 30
        print("2. 🔗 Création des assignations d'évaluations...")
        
        # Récupérer les IDs des évaluations
        cursor.execute("SELECT id FROM assessments LIMIT 2")
        assessments = cursor.fetchall()
        
        if len(assessments) >= 2:
            assessment1_id = assessments[0][0]
            assessment2_id = assessments[1][0]
            
            # Vérifier si des assignations existent déjà
            cursor.execute("SELECT COUNT(*) FROM assessment_assignments WHERE student_id = 30")
            existing_assignments = cursor.fetchone()[0]
            
            if existing_assignments == 0:
                # Assignation 1 : En attente
                cursor.execute('''
                    INSERT INTO assessment_assignments (student_id, assessment_id, status, assigned_at, due_date)
                    VALUES (?, ?, ?, ?, ?)
                ''', (30, assessment1_id, 'pending', datetime.now(), '2024-02-15 23:59:59'))
                
                # Assignation 2 : Terminée
                cursor.execute('''
                    INSERT INTO assessment_assignments (student_id, assessment_id, status, assigned_at, started_at, completed_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (30, assessment2_id, 'completed', '2024-01-10 10:00:00', '2024-01-10 10:30:00', '2024-01-10 10:55:00'))
                
                print("   ✅ 2 assignations d'évaluations créées")
            else:
                print(f"   ✅ {existing_assignments} assignations existent déjà")
        
        # 3. Créer des résultats d'évaluations
        print("3. 📊 Création des résultats d'évaluations...")
        
        # Vérifier si des résultats existent déjà
        cursor.execute("SELECT COUNT(*) FROM student_assessment_results WHERE student_id = 30")
        existing_results = cursor.fetchone()[0]
        
        if existing_results == 0 and len(assessments) >= 2:
            # Résultat pour l'évaluation 2 (terminée)
            cursor.execute('''
                INSERT INTO student_assessment_results (student_id, assessment_id, score, total_possible, percentage, time_taken, completed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (30, assessment2_id, 18, 25, 72.0, 1500, '2024-01-10 10:55:00'))
            
            print("   ✅ 1 résultat d'évaluation créé")
        else:
            print(f"   ✅ {existing_results} résultats existent déjà")
        
        # 4. Créer des parcours d'apprentissage
        print("4. 🗺️ Création de parcours d'apprentissage...")
        
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
            
            print("   ✅ 2 parcours créés")
        else:
            print(f"   ✅ {existing_paths} parcours existent déjà")
        
        # 5. Créer des relations étudiant-parcours
        print("5. 🔗 Création des relations étudiant-parcours...")
        
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
                
                print("   ✅ 2 relations étudiant-parcours créées")
            else:
                print(f"   ✅ {existing_relations} relations existent déjà")
        
        # Valider les changements
        conn.commit()
        print("\n🎉 Données de test complètes créées avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des données: {e}")
        conn.rollback()
    
    finally:
        conn.close()

def verify_complete_solution():
    """Vérifier que la solution complète fonctionne"""
    
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'app.db')
    
    print(f"\n🔍 VÉRIFICATION DE LA SOLUTION COMPLÈTE")
    print("=" * 60)
    
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
        
        # Vérifier les assignations d'évaluations
        cursor.execute("SELECT COUNT(*) FROM assessment_assignments WHERE student_id = 30")
        assignment_count = cursor.fetchone()[0]
        print(f"📝 Assignations d'évaluations pour l'utilisateur 30: {assignment_count}")
        
        # Vérifier les résultats d'évaluations
        cursor.execute("SELECT COUNT(*) FROM student_assessment_results WHERE student_id = 30")
        result_count = cursor.fetchone()[0]
        print(f"📊 Résultats d'évaluations pour l'utilisateur 30: {result_count}")
        
        # Vérifier les parcours
        cursor.execute("SELECT COUNT(*) FROM student_learning_paths WHERE student_id = 30")
        path_count = cursor.fetchone()[0]
        print(f"🗺️ Parcours pour l'utilisateur 30: {path_count}")
        
        # Vérifier toutes les tables créées
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('assessment_assignments', 'learning_paths', 'learning_path_steps', 'student_learning_paths')")
        created_tables = cursor.fetchall()
        print(f"📋 Tables créées: {[table[0] for table in created_tables]}")
        
        print(f"\n🎯 RÉSUMÉ FINAL:")
        print(f"   - Utilisateur 30: {'✅ Créé' if user else '❌ Manquant'}")
        print(f"   - Assignations d'évaluations: {assignment_count}")
        print(f"   - Résultats d'évaluations: {result_count}")
        print(f"   - Parcours: {path_count}")
        print(f"   - Tables créées: {'✅ Complètes' if len(created_tables) == 4 else '❌ Manquantes'}")
        
        if user and assignment_count > 0 and result_count > 0 and path_count > 0 and len(created_tables) == 4:
            print(f"\n🎉 SUCCÈS COMPLET ! VOS WIDGETS DEVRAIENT MAINTENANT AFFICHER DES DONNÉES!")
            print(f"🔄 Rafraîchissez votre dashboard et testez les widgets!")
            print(f"📊 Les endpoints devraient maintenant retourner des données réelles!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    print("🚀 CRÉATION DE LA SOLUTION COMPLÈTE")
    print("=" * 70)
    print("📋 Ce script crée :")
    print("   1. 🔗 Table assessment_assignments (liaison étudiants-évaluations)")
    print("   2. 📚 Tables learning_paths manquantes")
    print("   3. 👤 Utilisateur 30 avec données de test")
    print("   4. 📝 Assignations et résultats d'évaluations")
    print("   5. 🗺️ Parcours d'apprentissage")
    print()
    
    create_assessment_assignments_table()
    create_learning_paths_tables()
    create_test_user_30()
    create_test_data_for_user_30()
    verify_complete_solution()
    
    print("\n🎉 SOLUTION COMPLÈTE CRÉÉE AVEC SUCCÈS!")
    print("🔄 Maintenant, rafraîchissez votre dashboard et testez les widgets!")
    print("📊 Les 404 devraient être remplacés par des données réelles!")
