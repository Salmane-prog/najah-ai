#!/usr/bin/env python3
"""
Script pour ajouter les colonnes subject et tags à la table notes
"""

import sqlite3
import os

def fix_notes_table():
    """Ajouter les colonnes subject et tags à la table notes"""
    try:
        print("🔧 CORRECTION DE LA TABLE NOTES")
        print("=" * 40)
        
        # Chemin vers la base de données
        db_path = "F:/IMT/stage/Yancode/Najah__AI/data/app.db"
        
        if not os.path.exists(db_path):
            print(f"❌ Base de données non trouvée: {db_path}")
            return
        
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier la structure actuelle de la table
        print("\n1. Vérification de la structure actuelle...")
        cursor.execute("PRAGMA table_info(notes)")
        columns = cursor.fetchall()
        
        print(f"   Colonnes actuelles:")
        for col in columns:
            print(f"      - {col[1]} ({col[2]})")
        
        # Vérifier si la colonne subject existe
        subject_exists = any(col[1] == 'subject' for col in columns)
        
        if not subject_exists:
            print("\n2. Ajout de la colonne subject...")
            cursor.execute("ALTER TABLE notes ADD COLUMN subject TEXT")
            print("   ✅ Colonne subject ajoutée")
        else:
            print("\n2. Colonne subject existe déjà")
        
        # Vérifier si la colonne tags existe
        tags_exists = any(col[1] == 'tags' for col in columns)
        
        if not tags_exists:
            print("\n3. Ajout de la colonne tags...")
            cursor.execute("ALTER TABLE notes ADD COLUMN tags TEXT")
            print("   ✅ Colonne tags ajoutée")
        else:
            print("\n3. Colonne tags existe déjà")
        
        # Vérifier la structure finale
        print("\n4. Vérification de la structure finale...")
        cursor.execute("PRAGMA table_info(notes)")
        columns = cursor.fetchall()
        
        print(f"   Colonnes finales:")
        for col in columns:
            print(f"      - {col[1]} ({col[2]})")
        
        # Commit et fermer
        conn.commit()
        conn.close()
        
        print("\n" + "=" * 40)
        print("🎉 CORRECTION DE LA TABLE NOTES TERMINÉE!")
        print("✅ La table notes est maintenant compatible avec le modèle UserNote!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {e}")

if __name__ == "__main__":
    fix_notes_table() 