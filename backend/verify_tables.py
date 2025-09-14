#!/usr/bin/env python3
"""
Script pour vérifier que toutes les tables d'évaluation adaptative existent
"""

import sqlite3
import os

def verify_tables():
    """Vérifie que toutes les tables d'évaluation adaptative existent"""
    
    db_path = 'data/app.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 Vérification des tables d'évaluation adaptative...")
        print("=" * 60)
        
        # Vérifier toutes les tables nécessaires
        required_tables = [
            'adaptive_tests',
            'adaptive_test_assignments', 
            'adaptive_test_questions',
            'adaptive_test_responses',
            'formative_evaluations',
            'formative_evaluation_assignments',
            'formative_evaluation_questions',
            'formative_evaluation_submissions'
        ]
        
        missing_tables = []
        existing_tables = []
        
        for table in required_tables:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if cursor.fetchone():
                existing_tables.append(table)
                print(f"✅ {table}")
            else:
                missing_tables.append(table)
                print(f"❌ {table} - MANQUANTE")
        
        print(f"\n📊 Résumé:")
        print(f"   Tables existantes: {len(existing_tables)}/{len(required_tables)}")
        print(f"   Tables manquantes: {len(missing_tables)}")
        
        if missing_tables:
            print(f"\n🚨 Tables manquantes:")
            for table in missing_tables:
                print(f"   - {table}")
            
            print(f"\n💡 Exécutez: python create_missing_tables.py")
            return False
        else:
            print(f"\n🎉 Toutes les tables existent !")
            
            # Vérifier le contenu des tables principales
            print(f"\n📋 Contenu des tables:")
            
            cursor.execute("SELECT COUNT(*) FROM adaptive_tests")
            count = cursor.fetchone()[0]
            print(f"   adaptive_tests: {count} tests")
            
            cursor.execute("SELECT COUNT(*) FROM adaptive_test_assignments")
            count = cursor.fetchone()[0]
            print(f"   adaptive_test_assignments: {count} attributions")
            
            cursor.execute("SELECT COUNT(*) FROM formative_evaluations")
            count = cursor.fetchone()[0]
            print(f"   formative_evaluations: {count} évaluations")
            
            return True
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    verify_tables()





















