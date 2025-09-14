#!/usr/bin/env python3
"""
Script pour corriger la structure de la base de données
"""

import sqlite3
import os

def fix_database_structure():
    """Corriger la structure de la base de données"""
    
    print("🔧 Correction de la structure de la base de données...")
    
    # Chemin vers la base de données
    db_path = "../data/app.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée : {db_path}")
        return
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier les tables existantes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [row[0] for row in cursor.fetchall()]
        print(f"📋 Tables existantes : {existing_tables}")
        
        # Corriger la table learning_history
        print("\n🔧 Correction de la table learning_history...")
        try:
            # Vérifier si la colonne path_id existe
            cursor.execute("PRAGMA table_info(learning_history)")
            columns = [row[1] for row in cursor.fetchall()]
            
            if 'path_id' not in columns:
                print("   ➕ Ajout de la colonne path_id...")
                cursor.execute("ALTER TABLE learning_history ADD COLUMN path_id INTEGER")
                print("   ✅ Colonne path_id ajoutée")
            else:
                print("   ✅ Colonne path_id existe déjà")
                
        except Exception as e:
            print(f"   ❌ Erreur lors de la correction de learning_history : {e}")
        
        # Corriger la table user_badge (renommer user_badges en user_badge)
        print("\n🔧 Correction de la table user_badge...")
        try:
            # Vérifier si la table user_badge existe
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_badge'")
            user_badge_exists = cursor.fetchone() is not None
            
            if not user_badge_exists:
                print("   ➕ Création de la table user_badge...")
                cursor.execute("""
                    CREATE TABLE user_badge (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        badge_id INTEGER NOT NULL,
                        progression REAL DEFAULT 0.0,
                        awarded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id),
                        FOREIGN KEY (badge_id) REFERENCES badges (id)
                    )
                """)
                print("   ✅ Table user_badge créée")
                
                # Copier les données de user_badges vers user_badge si elle existe
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_badges'")
                if cursor.fetchone():
                    print("   📋 Copie des données de user_badges vers user_badge...")
                    cursor.execute("""
                        INSERT INTO user_badge (user_id, badge_id, progression, awarded_at)
                        SELECT user_id, badge_id, progression, awarded_at FROM user_badges
                    """)
                    print("   ✅ Données copiées")
            else:
                print("   ✅ Table user_badge existe déjà")
                
        except Exception as e:
            print(f"   ❌ Erreur lors de la correction de user_badge : {e}")
        
        # Vérifier et corriger les autres tables si nécessaire
        print("\n🔍 Vérification des autres tables...")
        
        # Vérifier la table contents
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='contents'")
        if not cursor.fetchone():
            print("   ➕ Création de la table contents...")
            cursor.execute("""
                CREATE TABLE contents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    content_type TEXT DEFAULT 'text',
                    subject TEXT,
                    difficulty_level TEXT DEFAULT 'beginner',
                    duration_minutes INTEGER DEFAULT 30,
                    created_by INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (created_by) REFERENCES users (id)
                )
            """)
            print("   ✅ Table contents créée")
        
        # Valider les changements
        conn.commit()
        
        print("\n🎉 Structure de la base de données corrigée !")
        
        # Afficher un résumé des tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"📋 Tables disponibles : {len(tables)}")
        for table in sorted(tables):
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"   • {table}: {count} enregistrements")
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction : {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_database_structure() 