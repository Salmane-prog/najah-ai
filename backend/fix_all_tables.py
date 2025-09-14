#!/usr/bin/env python3
"""
Script pour corriger toutes les tables et colonnes manquantes
"""

import sqlite3
import os

def fix_all_tables():
    """Corriger toutes les tables et colonnes manquantes"""
    
    print("🔧 Correction complète de la base de données...")
    
    # Chemin vers la base de données
    db_path = "../data/app.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée : {db_path}")
        return
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Corriger la table learning_history
        print("\n🔧 Correction de learning_history...")
        try:
            cursor.execute("PRAGMA table_info(learning_history)")
            columns = [row[1] for row in cursor.fetchall()]
            
            missing_columns = []
            if 'action' not in columns:
                missing_columns.append('action TEXT')
            if 'path_id' not in columns:
                missing_columns.append('path_id INTEGER')
            if 'content_id' not in columns:
                missing_columns.append('content_id INTEGER')
            if 'score' not in columns:
                missing_columns.append('score REAL')
            if 'progression' not in columns:
                missing_columns.append('progression REAL')
            if 'details' not in columns:
                missing_columns.append('details TEXT')
            if 'timestamp' not in columns:
                missing_columns.append('timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
            
            for col_def in missing_columns:
                col_name = col_def.split()[0]
                print(f"   ➕ Ajout de la colonne {col_name}...")
                cursor.execute(f"ALTER TABLE learning_history ADD COLUMN {col_def}")
            
            if missing_columns:
                print(f"   ✅ {len(missing_columns)} colonnes ajoutées")
            else:
                print("   ✅ Toutes les colonnes existent déjà")
                
        except Exception as e:
            print(f"   ❌ Erreur lors de la correction de learning_history : {e}")
        
        # 2. Corriger la table badges
        print("\n🔧 Correction de badges...")
        try:
            cursor.execute("PRAGMA table_info(badges)")
            columns = [row[1] for row in cursor.fetchall()]
            
            missing_columns = []
            if 'criteria' not in columns:
                missing_columns.append('criteria TEXT')
            if 'image_url' not in columns:
                missing_columns.append('image_url TEXT')
            if 'secret' not in columns:
                missing_columns.append('secret BOOLEAN DEFAULT 0')
            
            for col_def in missing_columns:
                col_name = col_def.split()[0]
                print(f"   ➕ Ajout de la colonne {col_name}...")
                cursor.execute(f"ALTER TABLE badges ADD COLUMN {col_def}")
            
            if missing_columns:
                print(f"   ✅ {len(missing_columns)} colonnes ajoutées")
            else:
                print("   ✅ Toutes les colonnes existent déjà")
                
        except Exception as e:
            print(f"   ❌ Erreur lors de la correction de badges : {e}")
        
        # 3. Corriger la table user_badge
        print("\n🔧 Correction de user_badge...")
        try:
            # Supprimer et recréer la table user_badge
            cursor.execute("DROP TABLE IF EXISTS user_badge")
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
            print("   ✅ Table user_badge recréée")
            
            # Copier les données de user_badges si elle existe
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_badges'")
            if cursor.fetchone():
                print("   📋 Copie des données...")
                cursor.execute("""
                    INSERT INTO user_badge (user_id, badge_id, progression)
                    SELECT user_id, badge_id, progression FROM user_badges
                """)
                cursor.execute("SELECT COUNT(*) FROM user_badge")
                count = cursor.fetchone()[0]
                print(f"   ✅ {count} enregistrements copiés")
            else:
                print("   ℹ️ Aucune donnée à copier")
                
        except Exception as e:
            print(f"   ❌ Erreur lors de la correction de user_badge : {e}")
        
        # 4. Corriger la table contents
        print("\n🔧 Correction de contents...")
        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='contents'")
            if not cursor.fetchone():
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
            else:
                print("   ✅ Table contents existe déjà")
                
        except Exception as e:
            print(f"   ❌ Erreur lors de la correction de contents : {e}")
        
        # 5. Corriger la table quizzes
        print("\n🔧 Correction de quizzes...")
        try:
            cursor.execute("PRAGMA table_info(quizzes)")
            columns = [row[1] for row in cursor.fetchall()]
            
            missing_columns = []
            if 'time_limit' not in columns:
                missing_columns.append('time_limit INTEGER DEFAULT 15')
            if 'max_attempts' not in columns:
                missing_columns.append('max_attempts INTEGER DEFAULT 1')
            if 'is_active' not in columns:
                missing_columns.append('is_active BOOLEAN DEFAULT 1')
            
            for col_def in missing_columns:
                col_name = col_def.split()[0]
                print(f"   ➕ Ajout de la colonne {col_name}...")
                cursor.execute(f"ALTER TABLE quizzes ADD COLUMN {col_def}")
            
            if missing_columns:
                print(f"   ✅ {len(missing_columns)} colonnes ajoutées")
            else:
                print("   ✅ Toutes les colonnes existent déjà")
                
        except Exception as e:
            print(f"   ❌ Erreur lors de la correction de quizzes : {e}")
        
        # Valider les changements
        conn.commit()
        
        print("\n🎉 Base de données corrigée avec succès !")
        
        # Afficher un résumé des tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"\n📋 Tables disponibles : {len(tables)}")
        for table in sorted(tables):
            if table != 'sqlite_sequence':
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"   • {table}: {count} enregistrements")
        
        print("\n✅ Toutes les corrections ont été appliquées !")
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction : {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_all_tables() 