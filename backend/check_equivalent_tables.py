#!/usr/bin/env python3
"""
Script pour vérifier si des tables existantes font le même travail
que les tables manquantes pour nos widgets
"""

import sqlite3
import os

def check_equivalent_tables():
    """Vérifier les tables équivalentes"""
    
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'app.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return
    
    print(f"🔍 Vérification des tables équivalentes dans: {db_path}")
    print("=" * 70)
    
    # Connexion à la base de données
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Récupérer toutes les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        all_tables = [table[0] for table in tables]
        
        print(f"📋 Nombre total de tables: {len(all_tables)}")
        print()
        
        # 1. VÉRIFICATION POUR assessment_results
        print("1. 🔍 RECHERCHE D'ÉQUIVALENT POUR 'assessment_results'")
        print("-" * 50)
        print("Fonction : Stocke les résultats des évaluations")
        
        potential_assessment_results = [
            'student_assessment_results',  # D'après votre diagnostic
            'assessment_results',
            'test_results',
            'evaluation_results',
            'quiz_results',
            'student_results'
        ]
        
        for table in potential_assessment_results:
            if table in all_tables:
                print(f"✅ Table trouvée: {table}")
                # Vérifier la structure
                try:
                    cursor.execute(f"PRAGMA table_info({table})")
                    columns = cursor.fetchall()
                    print(f"   📊 Colonnes: {[col[1] for col in columns]}")
                    
                    # Vérifier le nombre d'enregistrements
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"   📈 Enregistrements: {count}")
                    
                    # Vérifier s'il y a des données pour l'utilisateur 30
                    if 'student_id' in [col[1] for col in columns]:
                        cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE student_id = 30")
                        user_count = cursor.fetchone()[0]
                        print(f"   👤 Données pour utilisateur 30: {user_count}")
                    
                except Exception as e:
                    print(f"   ❌ Erreur lors de l'analyse: {e}")
            else:
                print(f"❌ {table} - Non trouvée")
        
        print()
        
        # 2. VÉRIFICATION POUR learning_paths
        print("2. 🔍 RECHERCHE D'ÉQUIVALENT POUR 'learning_paths'")
        print("-" * 50)
        print("Fonction : Définit des parcours d'apprentissage")
        
        potential_learning_paths = [
            'learning_paths',
            'learning_path',
            'courses',
            'curriculum',
            'modules',
            'subjects',
            'topics'
        ]
        
        for table in potential_learning_paths:
            if table in all_tables:
                print(f"✅ Table trouvée: {table}")
                try:
                    cursor.execute(f"PRAGMA table_info({table})")
                    columns = cursor.fetchall()
                    print(f"   📊 Colonnes: {[col[1] for col in columns]}")
                    
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"   📈 Enregistrements: {count}")
                    
                except Exception as e:
                    print(f"   ❌ Erreur lors de l'analyse: {e}")
            else:
                print(f"❌ {table} - Non trouvée")
        
        print()
        
        # 3. VÉRIFICATION POUR learning_path_steps
        print("3. 🔍 RECHERCHE D'ÉQUIVALENT POUR 'learning_path_steps'")
        print("-" * 50)
        print("Fonction : Détaille chaque étape du parcours")
        
        potential_steps = [
            'learning_path_steps',
            'learning_path_step',
            'course_steps',
            'module_steps',
            'lessons',
            'units',
            'chapters'
        ]
        
        for table in potential_steps:
            if table in all_tables:
                print(f"✅ Table trouvée: {table}")
                try:
                    cursor.execute(f"PRAGMA table_info({table})")
                    columns = cursor.fetchall()
                    print(f"   📊 Colonnes: {[col[1] for col in columns]}")
                    
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"   📈 Enregistrements: {count}")
                    
                except Exception as e:
                    print(f"   ❌ Erreur lors de l'analyse: {e}")
            else:
                print(f"❌ {table} - Non trouvée")
        
        print()
        
        # 4. VÉRIFICATION POUR student_learning_paths
        print("4. 🔍 RECHERCHE D'ÉQUIVALENT POUR 'student_learning_paths'")
        print("-" * 50)
        print("Fonction : Suit la progression de chaque étudiant")
        
        potential_progress = [
            'student_learning_paths',
            'student_learning_path',
            'student_progress',
            'enrollments',
            'student_courses',
            'progress_tracking',
            'student_modules'
        ]
        
        for table in potential_progress:
            if table in all_tables:
                print(f"✅ Table trouvée: {table}")
                try:
                    cursor.execute(f"PRAGMA table_info({table})")
                    columns = cursor.fetchall()
                    print(f"   📊 Colonnes: {[col[1] for col in columns]}")
                    
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"   📈 Enregistrements: {count}")
                    
                    # Vérifier s'il y a des données pour l'utilisateur 30
                    if 'student_id' in [col[1] for col in columns]:
                        cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE student_id = 30")
                        user_count = cursor.fetchone()[0]
                        print(f"   👤 Données pour utilisateur 30: {user_count}")
                    
                except Exception as e:
                    print(f"   ❌ Erreur lors de l'analyse: {e}")
            else:
                print(f"❌ {table} - Non trouvée")
        
        print()
        
        # ANALYSE DES TABLES SIMILAIRES
        print("🔍 ANALYSE DES TABLES SIMILAIRES TROUVÉES")
        print("=" * 50)
        
        # Vérifier student_assessment_results plus en détail
        if 'student_assessment_results' in all_tables:
            print("📊 ANALYSE DÉTAILLÉE DE 'student_assessment_results':")
            try:
                cursor.execute("PRAGMA table_info(student_assessment_results)")
                columns = cursor.fetchall()
                print(f"   Colonnes: {[col[1] for col in columns]}")
                
                # Vérifier le contenu
                cursor.execute("SELECT * FROM student_assessment_results LIMIT 3")
                sample_data = cursor.fetchall()
                print(f"   Exemple de données: {sample_data}")
                
                # Vérifier pour l'utilisateur 30
                cursor.execute("SELECT COUNT(*) FROM student_assessment_results WHERE student_id = 30")
                user_count = cursor.fetchone()[0]
                print(f"   Données pour utilisateur 30: {user_count}")
                
            except Exception as e:
                print(f"   ❌ Erreur: {e}")
        
        print()
        print("🎯 CONCLUSION:")
        print("Si des tables équivalentes existent, nous pouvons les utiliser")
        print("au lieu de créer de nouvelles tables !")
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    check_equivalent_tables()
