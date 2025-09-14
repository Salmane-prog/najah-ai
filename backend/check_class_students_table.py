#!/usr/bin/env python3
"""
Script pour vérifier la structure de la table class_students
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text

def check_class_students_table():
    """Vérifier la structure de la table class_students"""
    
    # Créer une connexion directe à la base de données
    engine = create_engine("sqlite:///../data/app.db")
    
    try:
        with engine.connect() as conn:
            # Vérifier si la table existe
            result = conn.execute(text("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='class_students'
            """))
            table_exists = result.fetchone()
            
            if not table_exists:
                print("❌ La table 'class_students' n'existe pas")
                return
            
            print("✅ La table 'class_students' existe")
            
            # Vérifier la structure de la table
            result = conn.execute(text("PRAGMA table_info(class_students)"))
            columns = result.fetchall()
            
            print("📋 Structure de la table class_students:")
            for col in columns:
                print(f"   - {col[1]} ({col[2]}) - {'NOT NULL' if col[3] else 'NULL'}")
            
            # Vérifier les données existantes
            result = conn.execute(text("SELECT COUNT(*) FROM class_students"))
            count = result.fetchone()[0]
            print(f"📊 Nombre d'enregistrements: {count}")
            
            if count > 0:
                result = conn.execute(text("SELECT * FROM class_students LIMIT 3"))
                rows = result.fetchall()
                print("📝 Exemples d'enregistrements:")
                for row in rows:
                    print(f"   - {row}")
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")

if __name__ == "__main__":
    check_class_students_table() 