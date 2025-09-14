#!/usr/bin/env python3
"""
Script pour vérifier manuellement la base de données
"""

import sqlite3
import os
import sys

def check_db_manually():
    # Chemin vers la base de données
    db_path = "data/app.db"
    
    print("=== VÉRIFICATION MANUELLE DE LA BASE DE DONNÉES ===")
    print(f"Chemin de la base: {os.path.abspath(db_path)}")
    
    if not os.path.exists(db_path):
        print(f"❌ ERREUR: Base de données non trouvée: {db_path}")
        return
    
    # Connexion directe à SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("\n=== 1. VÉRIFICATION DE LA TABLE CONTENTS ===")
        
        # Vérifier si la table existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='contents'")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            print("❌ ERREUR: La table 'contents' n'existe pas!")
            return
        else:
            print("✅ La table 'contents' existe")
        
        # Vérifier les colonnes
        cursor.execute("PRAGMA table_info(contents)")
        columns = cursor.fetchall()
        
        print(f"\nColonnes trouvées ({len(columns)}):")
        column_names = []
        for col in columns:
            column_name = col[1]
            column_type = col[2]
            column_names.append(column_name)
            print(f"  - {column_name} ({column_type})")
        
        # Vérifier spécifiquement content_type
        if 'content_type' in column_names:
            print("\n✅ La colonne 'content_type' existe")
            
            # Vérifier les valeurs
            cursor.execute("SELECT id, title, content_type FROM contents LIMIT 5")
            rows = cursor.fetchall()
            print("Exemples de valeurs content_type:")
            for row in rows:
                print(f"  - ID: {row[0]}, Title: {row[1]}, Type: {row[2]}")
        else:
            print("\n❌ ERREUR: La colonne 'content_type' n'existe pas!")
            
            # Ajouter la colonne
            print("Ajout de la colonne 'content_type'...")
            cursor.execute("ALTER TABLE contents ADD COLUMN content_type VARCHAR(50) DEFAULT 'text'")
            cursor.execute("UPDATE contents SET content_type = 'text' WHERE content_type IS NULL")
            print("✅ Colonne 'content_type' ajoutée et mise à jour!")
        
        # Test de requête SQL directe
        print("\n=== 2. TEST DE REQUÊTE SQL DIRECTE ===")
        try:
            cursor.execute("SELECT COUNT(*) FROM contents")
            count = cursor.fetchone()[0]
            print(f"✅ Nombre d'enregistrements: {count}")
            
            cursor.execute("SELECT id, title, content_type FROM contents LIMIT 3")
            rows = cursor.fetchall()
            print("✅ Requête SQL directe réussie:")
            for row in rows:
                print(f"  - ID: {row[0]}, Title: {row[1]}, Type: {row[2]}")
                
        except Exception as e:
            print(f"❌ Erreur lors de la requête SQL directe: {e}")
        
        # Test de la requête qui échoue dans SQLAlchemy
        print("\n=== 3. TEST DE LA REQUÊTE QUI ÉCHOUE ===")
        try:
            cursor.execute("""
                SELECT contents.id, contents.title, contents.description, 
                       contents.content_type, contents.subject, contents.level, 
                       contents.difficulty, contents.estimated_time, contents.content_data, 
                       contents.file_url, contents.thumbnail_url, contents.tags, 
                       contents.learning_objectives, contents.prerequisites, 
                       contents.skills_targeted, contents.created_by, contents.category_id, 
                       contents.created_at, contents.updated_at, contents.is_active
                FROM contents
                WHERE lower(contents.subject) LIKE lower(?)
            """, ('%None%',))
            
            rows = cursor.fetchall()
            print(f"✅ Requête SQLAlchemy simulée réussie: {len(rows)} résultats")
            
        except Exception as e:
            print(f"❌ Erreur lors de la requête SQLAlchemy simulée: {e}")
        
        # Vérifier les autres colonnes manquantes
        print("\n=== 4. VÉRIFICATION DES AUTRES COLONNES ===")
        required_columns = [
            'difficulty', 'estimated_time', 'content_data', 'thumbnail_url',
            'tags', 'learning_objectives', 'prerequisites', 'skills_targeted',
            'created_at', 'updated_at', 'is_active'
        ]
        
        missing_columns = []
        for col in required_columns:
            if col not in column_names:
                missing_columns.append(col)
        
        if missing_columns:
            print(f"❌ Colonnes manquantes: {missing_columns}")
            for col in missing_columns:
                print(f"Ajout de la colonne '{col}'...")
                if col in ['difficulty', 'estimated_time']:
                    cursor.execute(f"ALTER TABLE contents ADD COLUMN {col} FLOAT DEFAULT 1.0")
                elif col in ['created_at', 'updated_at']:
                    cursor.execute(f"ALTER TABLE contents ADD COLUMN {col} DATETIME")
                elif col == 'is_active':
                    cursor.execute(f"ALTER TABLE contents ADD COLUMN {col} BOOLEAN DEFAULT 1")
                else:
                    cursor.execute(f"ALTER TABLE contents ADD COLUMN {col} TEXT")
                print(f"✅ Colonne '{col}' ajoutée!")
        else:
            print("✅ Toutes les colonnes requises existent")
        
        # Mise à jour finale
        print("\n=== 5. MISE À JOUR FINALE ===")
        cursor.execute("UPDATE contents SET content_type = 'text' WHERE content_type IS NULL")
        cursor.execute("UPDATE contents SET difficulty = 1.0 WHERE difficulty IS NULL")
        cursor.execute("UPDATE contents SET estimated_time = 15 WHERE estimated_time IS NULL")
        cursor.execute("UPDATE contents SET is_active = 1 WHERE is_active IS NULL")
        
        from datetime import datetime
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("UPDATE contents SET created_at = ?, updated_at = ? WHERE created_at IS NULL", 
                      (current_time, current_time))
        
        print("✅ Données mises à jour!")
        
        # Vérification finale
        print("\n=== 6. VÉRIFICATION FINALE ===")
        cursor.execute("PRAGMA table_info(contents)")
        final_columns = cursor.fetchall()
        print(f"Nombre total de colonnes: {len(final_columns)}")
        
        # Test final
        cursor.execute("SELECT COUNT(*) FROM contents")
        final_count = cursor.fetchone()[0]
        print(f"Nombre d'enregistrements: {final_count}")
        
        conn.commit()
        print("\n🎉 Vérification manuelle terminée avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    check_db_manually() 