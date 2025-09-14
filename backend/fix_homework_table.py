#!/usr/bin/env python3
"""
Script pour corriger la table homework et s'assurer qu'elle a une clé primaire auto-incrémentée
"""

import sqlite3
import os
from pathlib import Path

def fix_homework_table():
    """Corriger la table homework"""
    
    # Chemin vers la base de données
    db_path = Path("F:/IMT/stage/Yancode/Najah__AI/data/app.db")
    
    if not db_path.exists():
        print(f"❌ Base de données non trouvée: {db_path}")
        return
    
    print(f"🔧 Correction de la table homework dans: {db_path}")
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier si la table existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='homework'")
        if not cursor.fetchone():
            print("❌ Table 'homework' n'existe pas")
            return
        
        # Vérifier la structure actuelle de la table
        cursor.execute("PRAGMA table_info(homework)")
        columns = cursor.fetchall()
        
        print("📋 Structure actuelle de la table homework:")
        for col in columns:
            try:
                print(f"  - {col[1]} ({col[2]}) - PK: {col[5]} - Auto: {col[6]}")
            except IndexError:
                print(f"  - {col[1]} ({col[2]}) - Structure incomplète")
        
        # Vérifier si la colonne id est configurée comme auto-increment
        id_column = None
        for col in columns:
            if col[1] == 'id':
                id_column = col
                break
        
        if id_column and len(id_column) > 6 and id_column[5] == 1 and id_column[6] == 1:
            print("✅ La colonne 'id' est déjà configurée comme clé primaire auto-incrémentée")
        else:
            print("⚠️  La colonne 'id' n'est pas configurée comme auto-increment")
            
            # Créer une nouvelle table avec la bonne structure
            print("🔧 Recréation de la table homework...")
            
            # Sauvegarder les données existantes
            cursor.execute("SELECT * FROM homework")
            existing_data = cursor.fetchall()
            print(f"📊 {len(existing_data)} enregistrements existants sauvegardés")
            
            # Supprimer l'ancienne table
            cursor.execute("DROP TABLE homework")
            
            # Recréer la table avec la bonne structure
            create_table_sql = """
            CREATE TABLE homework (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                subject VARCHAR(100),
                class_id INTEGER,
                assigned_by INTEGER,
                assigned_to INTEGER,
                due_date DATETIME NOT NULL,
                status VARCHAR(20) DEFAULT 'pending',
                priority VARCHAR(20) DEFAULT 'medium',
                estimated_time INTEGER,
                actual_time INTEGER,
                grade FLOAT,
                feedback TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            cursor.execute(create_table_sql)
            
            # Réinsérer les données si elles existent
            if existing_data:
                print("📥 Réinsertion des données existantes...")
                insert_sql = """
                INSERT INTO homework (
                    title, description, subject, class_id, assigned_by, assigned_to,
                    due_date, status, priority, estimated_time, actual_time, grade, feedback,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                
                for row in existing_data:
                    # Adapter les données selon la nouvelle structure
                    if len(row) >= 15:  # Si on a assez de colonnes
                        cursor.execute(insert_sql, row)
                    else:
                        # Adapter les données manquantes
                        adapted_row = list(row) + [None] * (15 - len(row))
                        cursor.execute(insert_sql, adapted_row)
        
        # Vérifier la nouvelle structure
        cursor.execute("PRAGMA table_info(homework)")
        new_columns = cursor.fetchall()
        
        print("\n📋 Nouvelle structure de la table homework:")
        for col in new_columns:
            try:
                print(f"  - {col[1]} ({col[2]}) - PK: {col[5]} - Auto: {col[6]}")
            except IndexError:
                print(f"  - {col[1]} ({col[2]}) - Structure incomplète")
        
        # Valider les changements
        conn.commit()
        print("✅ Table homework corrigée avec succès!")
        
        # Tester l'insertion d'un enregistrement de test
        print("\n🧪 Test d'insertion...")
        test_sql = """
        INSERT INTO homework (title, description, subject, assigned_by, assigned_to, due_date)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        
        cursor.execute(test_sql, (
            "Test devoir",
            "Description de test",
            "Mathématiques",
            1,  # assigned_by
            2,  # assigned_to
            "2024-12-31 23:59:59"
        ))
        
        test_id = cursor.lastrowid
        print(f"✅ Test réussi! ID généré: {test_id}")
        
        # Supprimer l'enregistrement de test
        cursor.execute("DELETE FROM homework WHERE id = ?", (test_id,))
        conn.commit()
        print("🧹 Enregistrement de test supprimé")
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_homework_table() 