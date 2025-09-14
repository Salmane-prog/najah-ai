#!/usr/bin/env python3
"""
Script pour vérifier la structure exacte des tables users et assessments
"""

import sqlite3
import os

def check_table_structure():
    """Vérifier la structure des tables existantes"""
    
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'app.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return
    
    print(f"🔍 VÉRIFICATION DE LA STRUCTURE DES TABLES")
    print("=" * 60)
    print(f"📍 Base de données: {db_path}")
    print()
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 1. Vérifier la structure de la table users
        print("1. 👤 STRUCTURE DE LA TABLE 'users'")
        print("-" * 40)
        
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        
        print("📊 Colonnes disponibles:")
        for col in columns:
            print(f"   - {col[1]} ({col[2]}) - Nullable: {col[3]} - Default: {col[4]}")
        
        print()
        
        # 2. Vérifier la structure de la table assessments
        print("2. 📝 STRUCTURE DE LA TABLE 'assessments'")
        print("-" * 40)
        
        cursor.execute("PRAGMA table_info(assessments)")
        columns = cursor.fetchall()
        
        print("📊 Colonnes disponibles:")
        for col in columns:
            print(f"   - {col[1]} ({col[2]}) - Nullable: {col[3]} - Default: {col[4]}")
        
        print()
        
        # 3. Vérifier la structure de la table student_assessment_results
        print("3. 📊 STRUCTURE DE LA TABLE 'student_assessment_results'")
        print("-" * 40)
        
        cursor.execute("PRAGMA table_info(student_assessment_results)")
        columns = cursor.fetchall()
        
        print("📊 Colonnes disponibles:")
        for col in columns:
            print(f"   - {col[1]} ({col[2]}) - Nullable: {col[3]} - Default: {col[4]}")
        
        print()
        
        # 4. Vérifier quelques données d'exemple
        print("4. 📋 EXEMPLES DE DONNÉES")
        print("-" * 40)
        
        # Exemple d'utilisateur
        cursor.execute("SELECT * FROM users LIMIT 1")
        user_example = cursor.fetchone()
        if user_example:
            print("👤 Exemple d'utilisateur:")
            cursor.execute("PRAGMA table_info(users)")
            user_columns = [col[1] for col in cursor.fetchall()]
            for i, value in enumerate(user_example):
                print(f"   {user_columns[i]}: {value}")
        
        print()
        
        # Exemple d'évaluation
        cursor.execute("SELECT * FROM assessments LIMIT 1")
        assessment_example = cursor.fetchone()
        if assessment_example:
            print("📝 Exemple d'évaluation:")
            cursor.execute("PRAGMA table_info(assessments)")
            assessment_columns = [col[1] for col in cursor.fetchall()]
            for i, value in enumerate(assessment_example):
                print(f"   {assessment_columns[i]}: {value}")
        
        print()
        print("🎯 MAINTENANT NOUS SAVONS EXACTEMENT COMMENT CRÉER LES DONNÉES!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    check_table_structure() 