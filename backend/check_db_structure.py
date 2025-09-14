#!/usr/bin/env python3
"""
Script pour vérifier la structure de la base de données
"""

import sqlite3
import os

def check_database_structure():
    """Vérifie la structure de la base de données"""
    
    # Chemin correct vers ta base de données
    db_path = r"F:\IMT\stage\Yancode\Najah__AI\data\app.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return False
    
    print(f"🗄️ Base de données trouvée: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Lister toutes les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"\n📋 Tables existantes ({len(tables)}):")
        for table in tables:
            print(f"  - {table[0]}")
        
        # Vérifier si la table users existe
        users_table_exists = any(table[0] == 'users' for table in tables)
        
        if users_table_exists:
            print(f"\n✅ Table 'users' trouvée !")
            
            # Vérifier la structure de la table users
            cursor.execute("PRAGMA table_info(users)")
            columns = cursor.fetchall()
            
            print(f"\n🔍 Structure de la table 'users':")
            for col in columns:
                cid, name, type_name, not_null, default_val, pk = col
                print(f"  - {name} ({type_name}) {'NOT NULL' if not_null else 'NULL'} {'PK' if pk else ''}")
            
            # Compter les utilisateurs
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            print(f"\n👥 Nombre d'utilisateurs: {user_count}")
            
            if user_count > 0:
                # Afficher quelques utilisateurs
                cursor.execute("SELECT id, email, role, first_name, last_name FROM users LIMIT 5")
                users = cursor.fetchall()
                print(f"\n👤 Exemples d'utilisateurs:")
                for user in users:
                    print(f"  - ID: {user[0]}, Email: {user[1]}, Rôle: {user[2]}, Nom: {user[3]} {user[4]}")
        else:
            print(f"\n❌ Table 'users' non trouvée")
            
            # Vérifier s'il y a d'autres tables d'utilisateurs
            user_related_tables = [table[0] for table in tables if 'user' in table[0].lower()]
            if user_related_tables:
                print(f"\n🔍 Tables liées aux utilisateurs trouvées:")
                for table in user_related_tables:
                    print(f"  - {table}")
        
        conn.close()
        return users_table_exists
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Vérification de la structure de la base de données")
    print("=" * 60)
    
    has_users_table = check_database_structure()
    
    if has_users_table:
        print(f"\n✅ La table 'users' existe et peut être utilisée")
    else:
        print(f"\n❌ La table 'users' n'existe pas et doit être créée")
