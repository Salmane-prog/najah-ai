#!/usr/bin/env python3
"""
Script pour lister toutes les tables liées à l'IA
"""

import sqlite3
import os

# Chemin vers la base de données
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db')

def list_ai_tables():
    """Liste toutes les tables liées à l'IA"""
    print("🔍 Liste des tables liées à l'IA...")
    
    if not os.path.exists(DB_PATH):
        print(f"❌ Base de données non trouvée: {DB_PATH}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Obtenir toutes les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print("📋 Toutes les tables de la base de données:")
        ai_related_tables = []
        
        for table in tables:
            table_name = table[0]
            if any(keyword in table_name.lower() for keyword in ['ai', 'model', 'training', 'prediction', 'analytics', 'learning']):
                ai_related_tables.append(table_name)
                print(f"   🧠 {table_name}")
            else:
                print(f"   📄 {table_name}")
        
        print(f"\n🎯 Tables liées à l'IA trouvées: {len(ai_related_tables)}")
        for table in ai_related_tables:
            print(f"   • {table}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    list_ai_tables()























