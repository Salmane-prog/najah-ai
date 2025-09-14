#!/usr/bin/env python3
"""
Script pour corriger la table adaptive_tests et résoudre le problème de clé étrangère
"""

import sqlite3
import os

def fix_adaptive_tests_table():
    """Corrige la table adaptive_tests"""
    
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), "..", "data", "app.db")
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données {db_path} non trouvée!")
        return
    
    print(f"🔧 Correction de la table adaptive_tests dans: {db_path}")
    print("=" * 60)
    
    try:
        # Connexion à la base
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier la structure actuelle
        print("📋 Structure actuelle de adaptive_tests:")
        cursor.execute("PRAGMA table_info(adaptive_tests);")
        columns = cursor.fetchall()
        
        for col in columns:
            col_id, name, type_name, not_null, default_val, pk = col
            print(f"  - {name}: {type_name} {'NOT NULL' if not_null else 'NULL'} {'PK' if pk else ''}")
        
        print("\n🔍 Contraintes de clé étrangère actuelles:")
        cursor.execute("PRAGMA foreign_key_list(adaptive_tests);")
        foreign_keys = cursor.fetchall()
        
        if foreign_keys:
            for fk in foreign_keys:
                print(f"  - {fk[3]} -> {fk[2]}.{fk[4]}")
        else:
            print("  - Aucune contrainte de clé étrangère")
        
        # Vérifier si la table users existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
        users_exists = cursor.fetchone()
        
        if not users_exists:
            print("\n❌ Table 'users' n'existe pas! Création...")
            
            # Créer la table users
            cursor.execute("""
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY,
                    username VARCHAR,
                    email VARCHAR,
                    hashed_password VARCHAR,
                    role VARCHAR(7),
                    is_active BOOLEAN,
                    first_name VARCHAR(100),
                    last_name VARCHAR(100),
                    avatar VARCHAR(255),
                    phone VARCHAR(20),
                    date_of_birth DATETIME,
                    bio TEXT,
                    created_at DATETIME
                )
            """)
            
            # Insérer un utilisateur par défaut
            cursor.execute("""
                INSERT INTO users (id, username, email, role, is_active, first_name, last_name, created_at)
                VALUES (33, 'marizee.dubois', 'marizee.dubois@najah.ai', 'teacher', 1, 'Marizee', 'Dubois', datetime('now'))
            """)
            
            print("✅ Table 'users' créée avec utilisateur par défaut")
        else:
            print("\n✅ Table 'users' existe déjà")
        
        # Vérifier les données existantes
        cursor.execute("SELECT COUNT(*) FROM adaptive_tests;")
        test_count = cursor.fetchone()[0]
        print(f"\n📊 Tests existants: {test_count}")
        
        if test_count > 0:
            print("⚠️ ATTENTION: Il y a des tests existants. Vérification des created_by...")
            
            # Vérifier les tests sans created_by
            cursor.execute("SELECT id, title, created_by FROM adaptive_tests WHERE created_by IS NULL;")
            null_created_by = cursor.fetchall()
            
            if null_created_by:
                print(f"🔧 {len(null_created_by)} tests sans created_by trouvés. Correction...")
                
                for test_id, title, created_by in null_created_by:
                    cursor.execute("UPDATE adaptive_tests SET created_by = 33 WHERE id = ?", (test_id,))
                    print(f"  - Test {test_id} ({title}): created_by = 33")
            else:
                print("✅ Tous les tests ont un created_by valide")
        
        # Vérifier la contrainte de clé étrangère
        print("\n🔧 Vérification de la contrainte de clé étrangère...")
        
        # Désactiver temporairement les contraintes de clé étrangère
        cursor.execute("PRAGMA foreign_keys = OFF;")
        
        # Recréer la table avec la bonne structure
        print("🔄 Recréation de la table adaptive_tests...")
        
        # Sauvegarder les données existantes
        cursor.execute("SELECT * FROM adaptive_tests;")
        existing_tests = cursor.fetchall()
        
        # Supprimer l'ancienne table
        cursor.execute("DROP TABLE IF EXISTS adaptive_tests;")
        
        # Créer la nouvelle table avec created_by nullable
        cursor.execute("""
            CREATE TABLE adaptive_tests (
                id INTEGER PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                subject VARCHAR(100) NOT NULL,
                description TEXT,
                difficulty_min INTEGER DEFAULT 1,
                difficulty_max INTEGER DEFAULT 10,
                estimated_duration INTEGER DEFAULT 30,
                total_questions INTEGER DEFAULT 20,
                adaptation_type VARCHAR(50) DEFAULT 'hybrid',
                learning_objectives TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users(id)
            )
        """)
        
        # Réactiver les contraintes de clé étrangère
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        # Restaurer les données
        if existing_tests:
            print(f"🔄 Restauration de {len(existing_tests)} tests...")
            
            for test in existing_tests:
                cursor.execute("""
                    INSERT INTO adaptive_tests (
                        id, title, subject, description, difficulty_min, difficulty_max,
                        estimated_duration, total_questions, adaptation_type, learning_objectives,
                        is_active, created_by, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, test)
        
        # Vérifier la nouvelle structure
        print("\n✅ Nouvelle structure de adaptive_tests:")
        cursor.execute("PRAGMA table_info(adaptive_tests);")
        new_columns = cursor.fetchall()
        
        for col in new_columns:
            col_id, name, type_name, not_null, default_val, pk = col
            print(f"  - {name}: {type_name} {'NOT NULL' if not_null else 'NULL'} {'PK' if pk else ''}")
        
        # Valider la contrainte de clé étrangère
        cursor.execute("PRAGMA foreign_key_check;")
        fk_errors = cursor.fetchall()
        
        if fk_errors:
            print(f"\n⚠️ Erreurs de clé étrangère: {len(fk_errors)}")
            for error in fk_errors:
                print(f"  - {error}")
        else:
            print("\n✅ Aucune erreur de clé étrangère détectée")
        
        # Commit des changements
        conn.commit()
        print("\n✅ Base de données corrigée avec succès!")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()

if __name__ == "__main__":
    fix_adaptive_tests_table()
