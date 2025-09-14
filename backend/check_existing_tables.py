#!/usr/bin/env python3
"""
Script pour vérifier quelles tables existent réellement dans la base de données
"""

import sqlite3
import os

def check_existing_tables():
    """Vérifier quelles tables existent réellement"""
    
    db_path = "najah_ai.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données {db_path} non trouvée")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 VÉRIFICATION DES TABLES EXISTANTES")
        print("=" * 50)
        
        # Récupérer toutes les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        if tables:
            print(f"✅ {len(tables)} tables trouvées:")
            for i, (table_name,) in enumerate(tables, 1):
                print(f"   {i}. {table_name}")
                
                # Vérifier la structure de chaque table
                try:
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    columns = cursor.fetchall()
                    print(f"      Colonnes: {len(columns)}")
                    
                    # Afficher les premières colonnes importantes
                    for col in columns[:5]:  # Limiter à 5 colonnes
                        print(f"        - {col[1]} ({col[2]})")
                    
                    if len(columns) > 5:
                        print(f"        ... et {len(columns) - 5} autres colonnes")
                    
                except Exception as e:
                    print(f"      ❌ Erreur lors de l'inspection: {e}")
                
                print()
        else:
            print("❌ Aucune table trouvée")
        
        # Vérifier les vues
        cursor.execute("SELECT name FROM sqlite_master WHERE type='view'")
        views = cursor.fetchall()
        
        if views:
            print(f"👁️ {len(views)} vues trouvées:")
            for view_name, in views:
                print(f"   - {view_name}")
        
        conn.close()
        
    except Exception as e:
        print(f"💥 Erreur: {e}")

if __name__ == "__main__":
    check_existing_tables()
