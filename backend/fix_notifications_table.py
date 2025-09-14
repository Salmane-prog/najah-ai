#!/usr/bin/env python3
"""
Script pour corriger la table notifications en ajoutant les colonnes manquantes
"""

import sqlite3
import os

def fix_notifications_table():
    """Ajouter les colonnes manquantes à la table notifications"""
    
    # Chemin vers la base de données
    db_path = "F:/IMT/stage/Yancode/Najah__AI/data/app.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔧 Correction de la table notifications...")
        
        # Vérifier si les colonnes existent déjà
        cursor.execute("PRAGMA table_info(notifications)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Ajouter la colonne icon si elle n'existe pas
        if 'icon' not in columns:
            print("➕ Ajout de la colonne 'icon'...")
            cursor.execute("ALTER TABLE notifications ADD COLUMN icon VARCHAR(50)")
            print("✅ Colonne 'icon' ajoutée")
        else:
            print("✅ Colonne 'icon' existe déjà")
        
        # Ajouter la colonne points_reward si elle n'existe pas
        if 'points_reward' not in columns:
            print("➕ Ajout de la colonne 'points_reward'...")
            cursor.execute("ALTER TABLE notifications ADD COLUMN points_reward INTEGER DEFAULT 0")
            print("✅ Colonne 'points_reward' ajoutée")
        else:
            print("✅ Colonne 'points_reward' existe déjà")
        
        # Vérifier la structure finale
        cursor.execute("PRAGMA table_info(notifications)")
        final_columns = [column[1] for column in cursor.fetchall()]
        print(f"📋 Colonnes finales: {final_columns}")
        
        # Valider les changements
        conn.commit()
        print("✅ Table notifications corrigée avec succès !")
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_notifications_table() 