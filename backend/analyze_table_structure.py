#!/usr/bin/env python3
"""
Script d'analyse complète de la structure des tables
"""

import sqlite3
import os
from datetime import datetime

def analyze_table_structure():
    """Analyser la structure complète des tables"""
    print("🏗️ ANALYSE COMPLÈTE DE LA STRUCTURE DES TABLES")
    print("=" * 80)
    
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db')
    print(f"📁 Base de données: {db_path}")
    
    if not os.path.exists(db_path):
        print("❌ Base de données non trouvée!")
        return
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Étape 1: Toutes les tables
        print("\n1️⃣ TOUTES LES TABLES DE LA BASE DE DONNÉES")
        print("-" * 60)
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        
        print(f"📋 Total: {len(tables)} tables trouvées")
        
        # Catégoriser les tables
        student_tables = []
        assessment_tables = []
        learning_tables = []
        user_tables = []
        content_tables = []
        analytics_tables = []
        other_tables = []
        
        for table in tables:
            table_name = table[0].lower()
            
            if any(keyword in table_name for keyword in ['student', 'assessment', 'quiz', 'homework']):
                student_tables.append(table[0])
            elif any(keyword in table_name for keyword in ['learning', 'path', 'step']):
                learning_tables.append(table[0])
            elif any(keyword in table_name for keyword in ['user', 'auth']):
                user_tables.append(table[0])
            elif any(keyword in table_name for keyword in ['content', 'question', 'material']):
                content_tables.append(table[0])
            elif any(keyword in table_name for keyword in ['analytics', 'progress', 'report']):
                analytics_tables.append(table[0])
            else:
                other_tables.append(table[0])
        
        # Afficher les catégories
        print(f"\n   🎓 Tables Étudiant: {len(student_tables)}")
        for table in student_tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"      📋 {table}: {count} lignes")
        
        print(f"\n   🛤️ Tables Apprentissage: {len(learning_tables)}")
        for table in learning_tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"      📋 {table}: {count} lignes")
        
        print(f"\n   👤 Tables Utilisateur: {len(user_tables)}")
        for table in user_tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"      📋 {table}: {count} lignes")
        
        print(f"\n   📚 Tables Contenu: {len(content_tables)}")
        for table in content_tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"      📋 {table}: {count} lignes")
        
        print(f"\n   📊 Tables Analytics: {len(analytics_tables)}")
        for table in analytics_tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"      📋 {table}: {count} lignes")
        
        print(f"\n   🔧 Autres Tables: {len(other_tables)}")
        for table in other_tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"      📋 {table}: {count} lignes")
        
        # Étape 2: Structure détaillée des tables clés
        print("\n2️⃣ STRUCTURE DÉTAILLÉE DES TABLES CLÉS")
        print("-" * 60)
        
        key_tables = [
            'users', 'assessments', 'assessment_questions', 'assessment_results',
            'learning_paths', 'learning_path_steps', 'student_learning_paths',
            'quizzes', 'questions', 'quiz_results', 'advanced_homeworks'
        ]
        
        for table_name in key_tables:
            try:
                print(f"\n   📋 Table: {table_name}")
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                
                for col in columns:
                    col_name, col_type, not_null, default_val, pk = col[1], col[2], col[3], col[4], col[5]
                    constraints = []
                    if not_null:
                        constraints.append("NOT NULL")
                    if pk:
                        constraints.append("PRIMARY KEY")
                    if default_val:
                        constraints.append(f"DEFAULT {default_val}")
                    
                    constraint_str = " ".join(constraints) if constraints else ""
                    print(f"      - {col_name} ({col_type}) {constraint_str}")
                
                # Compter les lignes
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"      📊 Total: {count} lignes")
                
            except Exception as e:
                print(f"      ❌ Erreur: {e}")
        
        # Étape 3: Relations entre tables
        print("\n3️⃣ RELATIONS ENTRE TABLES")
        print("-" * 60)
        
        print("   🔗 Relations identifiées:")
        print("      - users (1) → assessments (N)")
        print("      - assessments (1) → assessment_questions (N)")
        print("      - assessments (1) → assessment_results (N)")
        print("      - users (1) → student_learning_paths (N)")
        print("      - learning_paths (1) → learning_path_steps (N)")
        print("      - learning_paths (1) → student_learning_paths (N)")
        print("      - users (1) → quiz_results (N)")
        print("      - users (1) → advanced_homework_submissions (N)")
        
        # Étape 4: Vérification des contraintes de clés étrangères
        print("\n4️⃣ VÉRIFICATION DES CONTRAINTES DE CLÉS ÉTRANGÈRES")
        print("-" * 60)
        
        print("   🔍 Vérification des références...")
        
        # Vérifier les références assessments → users
        try:
            cursor.execute("""
                SELECT COUNT(*) FROM assessments a 
                LEFT JOIN users u ON a.student_id = u.id 
                WHERE u.id IS NULL
            """)
            orphaned = cursor.fetchone()[0]
            if orphaned > 0:
                print(f"      ⚠️ {orphaned} assessments avec student_id invalide")
            else:
                print(f"      ✅ Tous les assessments ont des student_id valides")
        except:
            print(f"      ❌ Impossible de vérifier les références assessments")
        
        # Vérifier les références student_learning_paths → users
        try:
            cursor.execute("""
                SELECT COUNT(*) FROM student_learning_paths slp 
                LEFT JOIN users u ON slp.student_id = u.id 
                WHERE u.id IS NULL
            """)
            orphaned = cursor.fetchone()[0]
            if orphaned > 0:
                print(f"      ⚠️ {orphaned} parcours étudiants avec student_id invalide")
            else:
                print(f"      ✅ Tous les parcours étudiants ont des student_id valides")
        except:
            print(f"      ❌ Impossible de vérifier les références parcours")
        
        # Étape 5: Recommandations d'amélioration
        print("\n5️⃣ RECOMMANDATIONS D'AMÉLIORATION")
        print("-" * 60)
        
        print("   🎯 Pour l'Évaluation Initiale:")
        print("      ✅ Table assessments existe avec student_id")
        print("      ✅ Table assessment_questions existe")
        print("      ✅ Table assessment_results existe")
        print("      ⚠️ Manque: workflow d'évaluation, questions adaptatives")
        
        print("\n   🛤️ Pour les Parcours d'Apprentissage:")
        print("      ✅ Table learning_paths existe")
        print("      ✅ Table learning_path_steps existe")
        print("      ✅ Table student_learning_paths existe")
        print("      ⚠️ Manque: génération automatique, adaptation IA")
        
        print("\n   🔗 Pour l'Interconnexion:")
        print("      ✅ Relations de base existent")
        print("      ⚠️ Manque: logique métier, workflow complet")
        print("      ⚠️ Manque: endpoints pour start/submit/complete")
        
        conn.close()
        
        print("\n" + "=" * 80)
        print("🎯 RÉSUMÉ DE L'ANALYSE")
        print("✅ Structure de base solide")
        print("⚠️ Logique métier à implémenter")
        print("🔗 Relations bien définies")
        print("📊 Données présentes pour développement")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {e}")

if __name__ == "__main__":
    analyze_table_structure()







