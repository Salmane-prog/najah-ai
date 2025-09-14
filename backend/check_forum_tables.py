#!/usr/bin/env python3
"""
Script pour vérifier l'existence des tables du forum
"""

import sqlite3
import os

def check_forum_tables():
    """Vérifier si les tables du forum existent"""
    
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), "..", "data", "app.db")
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier les tables existantes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in cursor.fetchall()]
        
        print("📋 Tables existantes dans la base de données:")
        for table in sorted(tables):
            print(f"  - {table}")
        
        # Vérifier spécifiquement les tables du forum
        forum_tables = ['forum_categories', 'forum_threads', 'forum_replies']
        missing_tables = []
        
        print("\n🔍 Vérification des tables du forum:")
        for table in forum_tables:
            if table in tables:
                print(f"  ✅ {table} - EXISTE")
                
                # Compter les enregistrements
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"     📊 Nombre d'enregistrements: {count}")
            else:
                print(f"  ❌ {table} - MANQUANTE")
                missing_tables.append(table)
        
        # Vérifier la structure des tables existantes
        if 'forum_categories' in tables:
            print("\n🏗️ Structure de la table forum_categories:")
            cursor.execute("PRAGMA table_info(forum_categories)")
            columns = cursor.fetchall()
            for col in columns:
                print(f"  - {col[1]} ({col[2]}) - {'NOT NULL' if col[3] else 'NULL'}")
        
        if 'forum_threads' in tables:
            print("\n🏗️ Structure de la table forum_threads:")
            cursor.execute("PRAGMA table_info(forum_threads)")
            columns = cursor.fetchall()
            for col in columns:
                print(f"  - {col[1]} ({col[2]}) - {'NOT NULL' if col[3] else 'NULL'}")
        
        conn.close()
        
        if missing_tables:
            print(f"\n⚠️ Tables manquantes: {', '.join(missing_tables)}")
            return False
        else:
            print("\n✅ Toutes les tables du forum sont présentes!")
            return True
            
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False

if __name__ == "__main__":
    check_forum_tables()

