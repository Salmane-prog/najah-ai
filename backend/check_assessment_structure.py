#!/usr/bin/env python3
"""
Script pour vérifier la structure exacte des tables d'évaluation
"""

import sqlite3
import os

def check_assessment_structure():
    """Vérifier la structure exacte des tables d'évaluation"""
    print("🔍 VÉRIFICATION DE LA STRUCTURE DES TABLES D'ÉVALUATION")
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
        
        # Vérifier la structure de assessments
        print("\n1️⃣ Table 'assessments':")
        cursor.execute("PRAGMA table_info(assessments)")
        columns = cursor.fetchall()
        for col in columns:
            print(f"   📋 {col[1]} ({col[2]}) - {'NOT NULL' if col[3] else 'NULL'}")
        
        # Vérifier la structure de assessment_questions
        print("\n2️⃣ Table 'assessment_questions':")
        try:
            cursor.execute("PRAGMA table_info(assessment_questions)")
            columns = cursor.fetchall()
            for col in columns:
                print(f"   📋 {col[1]} ({col[2]}) - {'NOT NULL' if col[3] else 'NULL'}")
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
        
        # Vérifier la structure de assessment_results
        print("\n3️⃣ Table 'assessment_results':")
        try:
            cursor.execute("PRAGMA table_info(assessment_results)")
            columns = cursor.fetchall()
            for col in columns:
                print(f"   📋 {col[1]} ({col[2]}) - {'NOT NULL' if col[3] else 'NULL'}")
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
        
        # Vérifier les données existantes
        print("\n4️⃣ Données existantes:")
        
        # Assessments
        cursor.execute("SELECT COUNT(*) FROM assessments")
        assessment_count = cursor.fetchone()[0]
        print(f"   📝 Assessments: {assessment_count}")
        
        if assessment_count > 0:
            cursor.execute("SELECT id, title, student_id, status FROM assessments LIMIT 3")
            assessments = cursor.fetchall()
            for assessment in assessments:
                print(f"      - ID: {assessment[0]}, Titre: {assessment[1]}, Student: {assessment[2]}, Status: {assessment[3]}")
        
        # Questions
        try:
            cursor.execute("SELECT COUNT(*) FROM assessment_questions")
            questions_count = cursor.fetchone()[0]
            print(f"   ❓ Questions: {questions_count}")
        except:
            print(f"   ❓ Questions: Table n'existe pas")
        
        # Résultats
        try:
            cursor.execute("SELECT COUNT(*) FROM assessment_results")
            results_count = cursor.fetchone()[0]
            print(f"   📊 Résultats: {results_count}")
        except:
            print(f"   📊 Résultats: Table n'existe pas")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")

if __name__ == "__main__":
    check_assessment_structure()







