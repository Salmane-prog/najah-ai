#!/usr/bin/env python3
"""
Script pour ajouter la colonne created_by manquante
"""

import sqlite3
import os

def add_created_by_column():
    # Chemin vers la base de données
    db_path = "data/app.db"
    
    print("=== AJOUT DE LA COLONNE CREATED_BY ===")
    
    if not os.path.exists(db_path):
        print(f"❌ ERREUR: Base de données non trouvée: {db_path}")
        return
    
    # Connexion à la base de données
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("1. Vérification de la colonne created_by...")
        
        # Vérifier les colonnes existantes
        cursor.execute("PRAGMA table_info(contents)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        if 'created_by' in column_names:
            print("✅ La colonne 'created_by' existe déjà")
        else:
            print("❌ La colonne 'created_by' n'existe pas")
            print("Ajout de la colonne 'created_by'...")
            cursor.execute("ALTER TABLE contents ADD COLUMN created_by INTEGER")
            print("✅ Colonne 'created_by' ajoutée!")
        
        print("\n2. Mise à jour des données existantes...")
        
        # Mettre à jour les enregistrements existants avec une valeur par défaut
        cursor.execute("UPDATE contents SET created_by = 1 WHERE created_by IS NULL")
        print("✅ Données mises à jour!")
        
        print("\n3. Vérification finale...")
        
        # Vérifier les colonnes finales
        cursor.execute("PRAGMA table_info(contents)")
        final_columns = cursor.fetchall()
        print(f"Nombre total de colonnes: {len(final_columns)}")
        
        # Afficher toutes les colonnes
        print("Colonnes finales:")
        for col in final_columns:
            print(f"  - {col[1]} ({col[2]})")
        
        # Test de requête
        cursor.execute("SELECT COUNT(*) FROM contents")
        count = cursor.fetchone()[0]
        print(f"Nombre d'enregistrements: {count}")
        
        if count > 0:
            cursor.execute("SELECT id, title, created_by FROM contents LIMIT 3")
            rows = cursor.fetchall()
            print("Exemples d'enregistrements:")
            for row in rows:
                print(f"  - ID: {row[0]}, Title: {row[1]}, Created_by: {row[2]}")
        
        conn.commit()
        print("\n🎉 Colonne created_by ajoutée avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    add_created_by_column() 