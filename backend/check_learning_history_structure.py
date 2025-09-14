#!/usr/bin/env python3
"""
Script pour vérifier la structure de learning_history
"""
import sqlite3
import os

def check_learning_history_structure():
    """Vérifier la structure exacte de learning_history"""
    db_path = "F:/IMT/stage/Yancode/Najah__AI/data/app.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🔍 Vérification de la structure learning_history...")
    print("=" * 50)
    
    try:
        # Vérifier si la table existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='learning_history'")
        if not cursor.fetchone():
            print("❌ Table learning_history n'existe pas")
            return
        
        # Obtenir la structure complète
        cursor.execute("PRAGMA table_info(learning_history)")
        columns = cursor.fetchall()
        
        print("📋 Structure de la table learning_history:")
        print("-" * 30)
        for col in columns:
            print(f"   • {col[1]} ({col[2]}) - {'NOT NULL' if col[3] else 'NULL'}")
        
        # Vérifier les données existantes
        cursor.execute("SELECT COUNT(*) FROM learning_history")
        count = cursor.fetchone()[0]
        print(f"\n📊 Nombre d'entrées: {count}")
        
        if count > 0:
            print("\n📝 Exemple d'entrée:")
            cursor.execute("SELECT * FROM learning_history LIMIT 1")
            example = cursor.fetchone()
            if example:
                print(f"   {example}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_learning_history_structure() 