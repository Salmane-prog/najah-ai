#!/usr/bin/env python3
"""
Script pour corriger les problèmes de base de données identifiés dans les logs.
"""

import sqlite3
import os

def fix_database_issues():
    """Corriger les problèmes de base de données."""
    
    # Chemin vers la base de données
    db_path = "../data/app.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données introuvable: {db_path}")
        return
    
    print(f"🔧 Correction des problèmes de base de données dans {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 1. Ajouter la colonne max_score à la table quizzes
        cursor.execute("PRAGMA table_info(quizzes)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'max_score' not in columns:
            print("✓ Ajout de la colonne 'max_score' à la table 'quizzes'...")
            cursor.execute("ALTER TABLE quizzes ADD COLUMN max_score INTEGER DEFAULT 100")
            print("✓ Colonne 'max_score' ajoutée")
        else:
            print("✓ Colonne 'max_score' déjà présente")
        
        # 2. Ajouter la colonne created_at à la table quiz_results
        cursor.execute("PRAGMA table_info(quiz_results)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'created_at' not in columns:
            print("✓ Ajout de la colonne 'created_at' à la table 'quiz_results'...")
            cursor.execute("ALTER TABLE quiz_results ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            print("✓ Colonne 'created_at' ajoutée")
        else:
            print("✓ Colonne 'created_at' déjà présente")
        
        # 3. Ajouter la colonne objectives à la table learning_paths
        cursor.execute("PRAGMA table_info(learning_paths)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'objectives' not in columns:
            print("✓ Ajout de la colonne 'objectives' à la table 'learning_paths'...")
            cursor.execute("ALTER TABLE learning_paths ADD COLUMN objectives TEXT")
            print("✓ Colonne 'objectives' ajoutée")
        else:
            print("✓ Colonne 'objectives' déjà présente")
        
        # 4. Ajouter la colonne created_by à la table learning_paths
        if 'created_by' not in columns:
            print("✓ Ajout de la colonne 'created_by' à la table 'learning_paths'...")
            cursor.execute("ALTER TABLE learning_paths ADD COLUMN created_by INTEGER")
            print("✓ Colonne 'created_by' ajoutée")
        else:
            print("✓ Colonne 'created_by' déjà présente")
        
        # 5. Ajouter la colonne updated_at à la table learning_paths
        if 'updated_at' not in columns:
            print("✓ Ajout de la colonne 'updated_at' à la table 'learning_paths'...")
            cursor.execute("ALTER TABLE learning_paths ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            print("✓ Colonne 'updated_at' ajoutée")
        else:
            print("✓ Colonne 'updated_at' déjà présente")
        
        # 6. Ajouter la colonne created_at à la table learning_paths si elle n'existe pas
        if 'created_at' not in columns:
            print("✓ Ajout de la colonne 'created_at' à la table 'learning_paths'...")
            cursor.execute("ALTER TABLE learning_paths ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            print("✓ Colonne 'created_at' ajoutée")
        else:
            print("✓ Colonne 'created_at' déjà présente")
        
        # 7. Ajouter la colonne created_at à la table users si elle n'existe pas
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'created_at' not in columns:
            print("✓ Ajout de la colonne 'created_at' à la table 'users'...")
            cursor.execute("ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            print("✓ Colonne 'created_at' ajoutée")
        else:
            print("✓ Colonne 'created_at' déjà présente")
        
        # 8. Ajouter la colonne updated_at à la table users si elle n'existe pas
        if 'updated_at' not in columns:
            print("✓ Ajout de la colonne 'updated_at' à la table 'users'...")
            cursor.execute("ALTER TABLE users ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            print("✓ Colonne 'updated_at' ajoutée")
        else:
            print("✓ Colonne 'updated_at' déjà présente")
        
        # 9. Ajouter la colonne created_at à la table badges si elle n'existe pas
        cursor.execute("PRAGMA table_info(badges)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'created_at' not in columns:
            print("✓ Ajout de la colonne 'created_at' à la table 'badges'...")
            cursor.execute("ALTER TABLE badges ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            print("✓ Colonne 'created_at' ajoutée")
        else:
            print("✓ Colonne 'created_at' déjà présente")
        
        # 10. Ajouter la colonne updated_at à la table badges si elle n'existe pas
        if 'updated_at' not in columns:
            print("✓ Ajout de la colonne 'updated_at' à la table 'badges'...")
            cursor.execute("ALTER TABLE badges ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            print("✓ Colonne 'updated_at' ajoutée")
        else:
            print("✓ Colonne 'updated_at' déjà présente")
        
        conn.commit()
        print("✅ Problèmes de base de données corrigés avec succès !")
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction de la base de données: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_database_issues() 