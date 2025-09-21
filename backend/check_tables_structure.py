#!/usr/bin/env python3
"""
Script pour vérifier la structure des tables importantes
"""

from core.database import engine
from sqlalchemy import text

def check_table_structure():
    """Vérifier la structure des tables importantes"""
    
    tables_to_check = [
        'french_adaptive_tests',
        'french_learning_profiles', 
        'questions',
        'question_history',
        'adaptive_tests',
        'adaptive_questions'
    ]
    
    for table_name in tables_to_check:
        try:
            with engine.connect() as conn:
                result = conn.execute(text(f'PRAGMA table_info({table_name})'))
                columns = [row for row in result]
                
                print(f"\n=== Structure de la table: {table_name} ===")
                if columns:
                    for col in columns:
                        nullable = "NULL" if col[3] else "NOT NULL"
                        print(f"  {col[1]} ({col[2]}) {nullable}")
                else:
                    print("  Table vide ou inexistante")
                    
        except Exception as e:
            print(f"\n❌ Erreur lors de la vérification de {table_name}: {e}")

if __name__ == "__main__":
    check_table_structure()














