#!/usr/bin/env python3
"""
Script pour créer la table student_learning_paths manquante
avec la bonne structure pour la progression
"""

import sqlite3
import os
from datetime import datetime

def create_student_learning_paths_table():
    """Créer la table student_learning_paths manquante"""
    
    db_path = "najah_ai.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données {db_path} non trouvée")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔧 CRÉATION DE LA TABLE student_learning_paths")
        print("=" * 50)
        
        # Créer la table avec la bonne structure
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS student_learning_paths (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                learning_path_id INTEGER NOT NULL,
                current_step INTEGER NOT NULL DEFAULT 1,
                total_steps INTEGER NOT NULL DEFAULT 15,
                progress_percentage REAL NOT NULL DEFAULT 0.0,
                performance_score REAL DEFAULT 0.0,
                is_completed BOOLEAN DEFAULT FALSE,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP NULL,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES users (id),
                FOREIGN KEY (learning_path_id) REFERENCES learning_paths (id)
            )
        """)
        
        print("   ✅ Table student_learning_paths créée avec succès")
        
        # Créer des index pour améliorer les performances
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_student_learning_paths_student ON student_learning_paths(student_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_student_learning_paths_path ON student_learning_paths(learning_path_id)")
        
        print("   ✅ Index créés avec succès")
        
        conn.commit()
        conn.close()
        
        print("\n   🎯 Table créée avec succès!")
        
    except Exception as e:
        print(f"💥 Erreur lors de la création: {e}")

def populate_test_data():
    """Peupler la table avec des données de test pour l'utilisateur 30"""
    
    db_path = "najah_ai.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données {db_path} non trouvée")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("\n📊 PEUPLEMENT AVEC DES DONNÉES DE TEST")
        print("=" * 50)
        
        # Vérifier que l'utilisateur 30 existe
        cursor.execute("SELECT id FROM users WHERE id = 30")
        user_exists = cursor.fetchone()
        
        if not user_exists:
            print("   ❌ Utilisateur 30 non trouvé")
            return
        
        # Vérifier que des parcours existent
        cursor.execute("SELECT id FROM learning_paths LIMIT 5")
        paths = cursor.fetchall()
        
        if not paths:
            print("   ❌ Aucun parcours d'apprentissage trouvé")
            return
        
        print(f"   ✅ {len(paths)} parcours trouvés")
        
        # Créer des données de test pour l'utilisateur 30
        test_data = []
        
        for i, (path_id,) in enumerate(paths):
            # Progression variée pour tester
            if i == 0:  # Premier parcours - début
                current_step = 1
                progress = 6.67  # 1/15 * 100
            elif i == 1:  # Deuxième parcours - milieu
                current_step = 8
                progress = 53.33  # 8/15 * 100
            elif i == 2:  # Troisième parcours - presque fini
                current_step = 14
                progress = 93.33  # 14/15 * 100
            else:  # Autres parcours - progression aléatoire
                current_step = (i % 15) + 1
                progress = round((current_step / 15) * 100, 2)
            
            test_data.append((
                30,  # student_id
                path_id,  # learning_path_id
                current_step,  # current_step
                15,  # total_steps
                progress,  # progress_percentage
                75.0 + (i * 5),  # performance_score
                False,  # is_completed
                datetime.now().isoformat(),  # started_at
                None,  # completed_at
                datetime.now().isoformat()  # last_activity
            ))
        
        # Insérer les données de test
        cursor.executemany("""
            INSERT INTO student_learning_paths (
                student_id, learning_path_id, current_step, total_steps,
                progress_percentage, performance_score, is_completed,
                started_at, completed_at, last_activity
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, test_data)
        
        inserted_rows = cursor.rowcount
        print(f"   ✅ {inserted_rows} lignes de données de test insérées")
        
        # Vérifier le résultat
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN progress_percentage IS NULL THEN 1 END) as null_progress,
                COUNT(CASE WHEN current_step IS NULL THEN 1 END) as null_step,
                COUNT(CASE WHEN total_steps IS NULL THEN 1 END) as null_total
            FROM student_learning_paths
            WHERE student_id = 30
        """)
        
        stats = cursor.fetchone()
        print(f"\n   📊 DONNÉES CRÉÉES:")
        print(f"   Total: {stats[0]}")
        print(f"   Progress NULL: {stats[1]}")
        print(f"   Current Step NULL: {stats[2]}")
        print(f"   Total Steps NULL: {stats[3]}")
        
        # Afficher un exemple de données
        cursor.execute("""
            SELECT 
                id, learning_path_id, current_step, total_steps,
                progress_percentage, is_completed
            FROM student_learning_paths 
            WHERE student_id = 30
            LIMIT 3
        """)
        
        rows = cursor.fetchall()
        print(f"\n   📋 EXEMPLE DE DONNÉES:")
        for row in rows:
            print(f"   ID: {row[0]}, Path: {row[1]}, Step: {row[2]}/{row[3]}, Progress: {row[4]}%, Completed: {row[5]}")
        
        conn.commit()
        conn.close()
        
        print("\n   🎯 Données de test créées avec succès!")
        
    except Exception as e:
        print(f"💥 Erreur lors du peuplement: {e}")

if __name__ == "__main__":
    create_student_learning_paths_table()
    populate_test_data()
