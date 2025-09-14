#!/usr/bin/env python3
"""
Script pour vérifier les profils français
"""

import sqlite3

def check_french_profiles():
    """Vérifier les profils français"""
    print("🔍 VÉRIFICATION DES PROFILS FRANÇAIS")
    print("=" * 50)
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect('../data/app.db')
        cursor = conn.cursor()
        
        # Vérifier la structure de french_learning_profiles
        cursor.execute("PRAGMA table_info(french_learning_profiles)")
        columns = cursor.fetchall()
        
        print("📋 Colonnes de french_learning_profiles:")
        for column in columns:
            print(f"  - {column[1]} ({column[2]})")
        
        print("\n📊 Données des profils français:")
        cursor.execute("SELECT * FROM french_learning_profiles LIMIT 3")
        rows = cursor.fetchall()
        
        for i, row in enumerate(rows):
            print(f"  Profil {i+1}: {row}")
        
        # Vérifier french_cognitive_profiles
        print("\n🧠 Profils cognitifs français:")
        cursor.execute("SELECT COUNT(*) FROM french_cognitive_profiles")
        count = cursor.fetchone()[0]
        print(f"  Nombre de profils: {count}")
        
        if count > 0:
            cursor.execute("SELECT * FROM french_cognitive_profiles LIMIT 2")
            rows = cursor.fetchall()
            for i, row in enumerate(rows):
                print(f"    Exemple {i+1}: {row}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_french_profiles()










