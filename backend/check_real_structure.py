#!/usr/bin/env python3
"""
Script pour vérifier la vraie structure de la base de données
"""

import sqlite3
import os

def check_real_structure():
    """Vérifier la vraie structure de la base de données"""
    print("🔍 VÉRIFICATION DE LA VRAIE STRUCTURE DE LA BASE DE DONNÉES")
    print("=" * 70)
    
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
        
        # Vérifier toutes les tables
        print("\n1️⃣ Toutes les tables:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            print(f"   📋 {table_name}")
            
            # Compter les lignes
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"      - Lignes: {count}")
            except:
                print(f"      - Lignes: Erreur")
        
        # Vérifier les tables liées aux utilisateurs
        print("\n2️⃣ Tables liées aux utilisateurs:")
        user_tables = ['users', 'user_profiles', 'student_profiles', 'user_details']
        
        for table_name in user_tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"   📋 {table_name}: {count} lignes")
                
                if count > 0:
                    # Voir la structure
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    columns = cursor.fetchall()
                    print(f"      Colonnes: {[col[1] for col in columns]}")
                    
                    # Voir quelques exemples
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT 2")
                    examples = cursor.fetchall()
                    for example in examples:
                        print(f"      Exemple: {example}")
                        
            except Exception as e:
                print(f"   ❌ {table_name}: {e}")
        
        # Vérifier les tables d'évaluation
        print("\n3️⃣ Tables d'évaluation:")
        assessment_tables = ['assessments', 'assessment_questions', 'assessment_results']
        
        for table_name in assessment_tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"   📋 {table_name}: {count} lignes")
                
                if count > 0:
                    # Voir la structure
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    columns = cursor.fetchall()
                    print(f"      Colonnes: {[col[1] for col in columns]}")
                    
            except Exception as e:
                print(f"   ❌ {table_name}: {e}")
        
        # Vérifier les tables de parcours
        print("\n4️⃣ Tables de parcours:")
        path_tables = ['learning_paths', 'learning_path_steps', 'student_learning_paths']
        
        for table_name in path_tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"   📋 {table_name}: {count} lignes")
                
                if count > 0:
                    # Voir la structure
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    columns = cursor.fetchall()
                    print(f"      Colonnes: {[col[1] for col in columns]}")
                    
            except Exception as e:
                print(f"   ❌ {table_name}: {e}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")

if __name__ == "__main__":
    check_real_structure()







