#!/usr/bin/env python3
"""
Script pour vérifier la structure de la table users
"""

import sqlite3
import os

# Chemin vers la base de données
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db')

def check_users_table():
    """Vérifie la structure de la table users"""
    print("🔍 Vérification de la structure de la table users...")
    
    if not os.path.exists(DB_PATH):
        print(f"❌ Base de données non trouvée: {DB_PATH}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Vérifier si la table users existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            print("❌ Table 'users' n'existe pas")
            return
        
        # Obtenir la structure de la table
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        
        print("📋 Structure de la table 'users':")
        print("   ID | Nom | Type | NotNull | Default | PrimaryKey")
        print("   ---|-----|------|---------|---------|-----------")
        
        for col in columns:
            cid, name, type_, notnull, default, pk = col
            print(f"   {cid or 0:2} | {(name or ''):15} | {(type_ or ''):10} | {notnull or 0:7} | {(str(default) if default else ''):7} | {pk or 0:10}")
        
        # Vérifier le contenu
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        print(f"\n📊 Nombre d'utilisateurs dans la table: {count}")
        
        if count > 0:
            cursor.execute("SELECT * FROM users LIMIT 3")
            rows = cursor.fetchall()
            print("\n📄 Exemples d'utilisateurs:")
            for i, row in enumerate(rows):
                print(f"   Utilisateur {i+1}: {row}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_users_table()
