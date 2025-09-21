#!/usr/bin/env python3
"""
Script pour vérifier la structure de la table model_predictions
"""

import sqlite3
import os

# Chemin vers la base de données
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db')

def check_predictions_table():
    """Vérifie la structure de la table model_predictions"""
    print("🔍 Vérification de la structure de la table model_predictions...")
    
    if not os.path.exists(DB_PATH):
        print(f"❌ Base de données non trouvée: {DB_PATH}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Vérifier si la table model_predictions existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='model_predictions'")
        if not cursor.fetchone():
            print("❌ Table 'model_predictions' n'existe pas")
            return
        
        # Obtenir la structure de la table
        cursor.execute("PRAGMA table_info(model_predictions)")
        columns = cursor.fetchall()
        
        print("📋 Structure de la table 'model_predictions':")
        print("   ID | Nom | Type | NotNull | Default | PrimaryKey")
        print("   ---|-----|------|---------|---------|-----------")
        
        for col in columns:
            cid, name, type_, notnull, default, pk = col
            print(f"   {cid or 0:2} | {(name or ''):15} | {(type_ or ''):10} | {notnull or 0:7} | {(str(default) if default else ''):7} | {pk or 0:10}")
        
        # Vérifier le contenu
        cursor.execute("SELECT COUNT(*) FROM model_predictions")
        count = cursor.fetchone()[0]
        print(f"\n📊 Nombre de prédictions dans la table: {count}")
        
        if count > 0:
            cursor.execute("SELECT * FROM model_predictions LIMIT 3")
            rows = cursor.fetchall()
            print("\n📄 Exemples de prédictions:")
            for i, row in enumerate(rows):
                print(f"   Prédiction {i+1}: {row}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_predictions_table()


























