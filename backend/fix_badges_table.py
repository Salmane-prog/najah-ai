#!/usr/bin/env python3
"""
Script pour corriger la structure de la table badges
"""

import sqlite3
import os
from pathlib import Path

def fix_badges_table():
    """Corrige la structure de la table badges"""
    
    db_path = Path("F:/IMT/stage/Yancode/Najah__AI/data/app.db")
    
    if not db_path.exists():
        print("❌ Base de données non trouvée")
        return
    
    print(f"🔧 Correction de la table badges dans: {db_path.absolute()}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Vérifier la structure actuelle de la table badges
        cursor.execute("PRAGMA table_info(badges)")
        columns = [row[1] for row in cursor.fetchall()]
        
        print(f"📊 Colonnes actuelles de badges: {columns}")
        
        # Si la table n'a pas la bonne structure, la recréer
        if 'user_id' not in columns:
            print("🔄 Recréation de la table badges...")
            
            # Supprimer l'ancienne table
            cursor.execute("DROP TABLE IF EXISTS badges")
            
            # Créer la nouvelle table avec la bonne structure
            cursor.execute("""
                CREATE TABLE badges (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT,
                    rarity TEXT DEFAULT 'bronze',
                    earned_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    icon TEXT DEFAULT '🏆',
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            
            print("✅ Table badges recréée avec la bonne structure")
        else:
            print("✅ Table badges a déjà la bonne structure")
        
        # Valider les changements
        conn.commit()
        
        # Vérifier la structure finale
        cursor.execute("PRAGMA table_info(badges)")
        final_columns = [row[1] for row in cursor.fetchall()]
        print(f"\n📋 Structure finale de badges: {final_columns}")
        
        print("\n🎉 Correction de la table badges terminée!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("🔧 CORRECTION DE LA TABLE BADGES")
    print("=" * 50)
    
    fix_badges_table()
    
    print("\n" + "=" * 50)
    print("✅ CORRECTION TERMINÉE!")
    print("💡 Maintenant vous pouvez exécuter sync_calculations.py")
    print("🚀 La table badges est corrigée")


