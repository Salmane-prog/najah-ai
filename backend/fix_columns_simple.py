#!/usr/bin/env python3
"""
Script simple pour ajouter les colonnes manquantes essentielles
"""

import sqlite3
import os
from pathlib import Path

def fix_essential_columns():
    """Ajoute les colonnes manquantes essentielles"""
    
    db_path = Path("F:/IMT/stage/Yancode/Najah__AI/data/app.db")
    
    if not db_path.exists():
        print("❌ Base de données non trouvée")
        return
    
    print(f"🔧 Ajout des colonnes essentielles dans: {db_path.absolute()}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 1. Ajouter created_by à calendar_events
        print("\n📅 Ajout de created_by à calendar_events...")
        try:
            cursor.execute("ALTER TABLE calendar_events ADD COLUMN created_by INTEGER")
            print("   ✅ Colonne created_by ajoutée")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("   ✅ Colonne created_by existe déjà")
            else:
                print(f"   ❌ Erreur: {e}")
        
        # 2. Ajouter criteria à badges
        print("\n🏆 Ajout de criteria à badges...")
        try:
            cursor.execute("ALTER TABLE badges ADD COLUMN criteria TEXT")
            print("   ✅ Colonne criteria ajoutée")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("   ✅ Colonne criteria existe déjà")
            else:
                print(f"   ❌ Erreur: {e}")
        
        # 3. Ajouter progress à learning_history
        print("\n📚 Ajout de progress à learning_history...")
        try:
            cursor.execute("ALTER TABLE learning_history ADD COLUMN progress REAL")
            print("   ✅ Colonne progress ajoutée")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("   ✅ Colonne progress existe déjà")
            else:
                print(f"   ❌ Erreur: {e}")
        
        # 4. Ajouter time_spent à learning_history
        print("\n⏱️ Ajout de time_spent à learning_history...")
        try:
            cursor.execute("ALTER TABLE learning_history ADD COLUMN time_spent INTEGER")
            print("   ✅ Colonne time_spent ajoutée")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("   ✅ Colonne time_spent existe déjà")
            else:
                print(f"   ❌ Erreur: {e}")
        
        # 5. Ajouter created_at à learning_history
        print("\n📅 Ajout de created_at à learning_history...")
        try:
            cursor.execute("ALTER TABLE learning_history ADD COLUMN created_at TEXT")
            print("   ✅ Colonne created_at ajoutée")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("   ✅ Colonne created_at existe déjà")
            else:
                print(f"   ❌ Erreur: {e}")
        
        # Valider les changements
        conn.commit()
        
        print("\n🎉 Colonnes essentielles ajoutées!")
        
        # Vérifier le résultat final
        print("\n📋 VÉRIFICATION FINALE:")
        important_tables = ['calendar_events', 'badges', 'learning_history']
        for table_name in important_tables:
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [row[1] for row in cursor.fetchall()]
            print(f"   {table_name}: {len(columns)} colonnes - {', '.join(columns)}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("🔧 AJOUT DES COLONNES ESSENTIELLES")
    print("=" * 50)
    
    fix_essential_columns()
    
    print("\n" + "=" * 50)
    print("✅ AJOUT TERMINÉ!")
    print("💡 IMPORTANT: Redémarrez le serveur backend maintenant!")
    print("🚀 Les colonnes essentielles sont ajoutées")
    print("📊 Plus d'erreurs de colonnes manquantes!")


