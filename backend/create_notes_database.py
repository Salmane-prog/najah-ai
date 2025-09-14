#!/usr/bin/env python3
"""
Script pour créer la base de données et les tables pour les notes
"""

import sqlite3
import os

def create_notes_database():
    """Créer la base de données et les tables pour les notes"""
    try:
        print("🗄️ CRÉATION DE LA BASE DE DONNÉES NOTES")
        print("=" * 50)
        
        # Chemin vers la base de données (selon la configuration)
        db_path = "F:/IMT/stage/Yancode/Najah__AI/data/app.db"
        
        # Créer le dossier data s'il n'existe pas
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Connexion à la base de données (créera le fichier s'il n'existe pas)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Créer la table users si elle n'existe pas
        print("\n1. Création de la table users...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                username TEXT UNIQUE,
                first_name TEXT,
                last_name TEXT,
                role TEXT DEFAULT 'student',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("   ✅ Table users créée")
        
        # Créer la table notes
        print("\n2. Création de la table notes...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                content TEXT,
                subject TEXT,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        print("   ✅ Table notes créée")
        
        # Insérer un utilisateur de test
        print("\n3. Insertion d'un utilisateur de test...")
        cursor.execute("""
            INSERT OR IGNORE INTO users (id, email, username, first_name, last_name, role)
            VALUES (1, 'test@example.com', 'testuser', 'Test', 'User', 'student')
        """)
        print("   ✅ Utilisateur de test créé")
        
        # Vérifier la structure des tables
        print("\n4. Vérification de la structure...")
        
        # Structure de la table users
        cursor.execute("PRAGMA table_info(users)")
        users_columns = cursor.fetchall()
        print("   Table users:")
        for col in users_columns:
            print(f"      - {col[1]} ({col[2]})")
        
        # Structure de la table notes
        cursor.execute("PRAGMA table_info(notes)")
        notes_columns = cursor.fetchall()
        print("   Table notes:")
        for col in notes_columns:
            print(f"      - {col[1]} ({col[2]})")
        
        # Commit et fermer
        conn.commit()
        conn.close()
        
        print("\n" + "=" * 50)
        print("🎉 BASE DE DONNÉES NOTES CRÉÉE AVEC SUCCÈS!")
        print("✅ Tables users et notes créées")
        print("✅ Utilisateur de test créé")
        print("✅ Base de données prête pour les tests!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")

if __name__ == "__main__":
    create_notes_database() 