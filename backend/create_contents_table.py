#!/usr/bin/env python3
"""
Script pour créer la table contents manquante
"""

import sqlite3
import os

def create_contents_table():
    # Chemin vers la base de données
    db_path = "data/app.db"
    
    # Vérifier si la base de données existe
    if not os.path.exists(db_path):
        print(f"Base de données non trouvée: {db_path}")
        return
    
    # Connexion à la base de données
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Vérifier si la table contents existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='contents'")
        table_exists = cursor.fetchone()
        
        if table_exists:
            print("La table 'contents' existe déjà")
            # Vérifier les colonnes existantes
            cursor.execute("PRAGMA table_info(contents)")
            columns = cursor.fetchall()
            print("Colonnes existantes:")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
        else:
            print("Création de la table 'contents'...")
            
            # Créer la table contents
            cursor.execute("""
                CREATE TABLE contents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    content_type VARCHAR(50) NOT NULL,
                    subject VARCHAR(100) NOT NULL,
                    level VARCHAR(50) NOT NULL,
                    difficulty FLOAT DEFAULT 1.0,
                    estimated_time INTEGER DEFAULT 15,
                    content_data TEXT,
                    file_url VARCHAR(500),
                    thumbnail_url VARCHAR(500),
                    tags TEXT,
                    learning_objectives TEXT,
                    prerequisites TEXT,
                    skills_targeted TEXT,
                    created_by INTEGER NOT NULL,
                    category_id INTEGER,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (created_by) REFERENCES users (id),
                    FOREIGN KEY (category_id) REFERENCES categories (id)
                )
            """)
            
            print("Table 'contents' créée avec succès!")
            
            # Ajouter quelques données de test
            cursor.execute("""
                INSERT INTO contents (title, description, content_type, subject, level, created_by) 
                VALUES 
                ('Introduction à la littérature', 'Cours d''introduction à la littérature française', 'text', 'Littérature', 'beginner', 1),
                ('Analyse de texte', 'Méthodes d''analyse de texte', 'text', 'Littérature', 'intermediate', 1),
                ('Histoire de la littérature', 'Panorama de la littérature française', 'text', 'Littérature', 'advanced', 1)
            """)
            
            print("Données de test ajoutées!")
        
        conn.commit()
        print("Opération terminée avec succès!")
        
    except Exception as e:
        print(f"Erreur: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    create_contents_table() 