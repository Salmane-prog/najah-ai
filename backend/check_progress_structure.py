#!/usr/bin/env python3
"""
Script pour vérifier la structure des données de progression
et identifier pourquoi nous avons des NaN%
"""

import sqlite3
import os
from datetime import datetime

def check_progress_structure():
    """Vérifier la structure des données de progression"""
    
    db_path = "najah_ai.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données {db_path} non trouvée")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 VÉRIFICATION DE LA STRUCTURE DES DONNÉES DE PROGRESSION")
        print("=" * 60)
        
        # 1. Vérifier la table student_learning_paths
        print("\n1. 📊 TABLE student_learning_paths")
        print("-" * 40)
        
        cursor.execute("PRAGMA table_info(student_learning_paths)")
        columns = cursor.fetchall()
        
        for col in columns:
            print(f"   {col[1]} ({col[2]}) - Not Null: {col[3]}, Default: {col[4]}")
        
        # 2. Vérifier les données existantes
        print("\n2. 📈 DONNÉES EXISTANTES")
        print("-" * 40)
        
        cursor.execute("""
            SELECT 
                id, 
                student_id, 
                learning_path_id,
                current_step,
                total_steps,
                progress_percentage,
                is_completed,
                started_at
            FROM student_learning_paths 
            WHERE student_id = 30
            LIMIT 5
        """)
        
        rows = cursor.fetchall()
        
        if rows:
            print("   Données trouvées pour l'utilisateur 30:")
            for row in rows:
                print(f"   ID: {row[0]}, Student: {row[1]}, Path: {row[2]}")
                print(f"   Step: {row[3]}/{row[4]}, Progress: {row[5]}%, Completed: {row[6]}")
                print(f"   Started: {row[7]}")
                print("   ---")
        else:
            print("   ❌ Aucune donnée trouvée pour l'utilisateur 30")
        
        # 3. Vérifier la table learning_paths
        print("\n3. 🗺️ TABLE learning_paths")
        print("-" * 40)
        
        cursor.execute("PRAGMA table_info(learning_paths)")
        columns = cursor.fetchall()
        
        for col in columns:
            print(f"   {col[1]} ({col[2]}) - Not Null: {col[3]}, Default: {col[4]}")
        
        # 4. Vérifier les données des parcours
        cursor.execute("SELECT id, title, subject, difficulty, estimated_duration FROM learning_paths LIMIT 5")
        rows = cursor.fetchall()
        
        if rows:
            print("\n   Parcours disponibles:")
            for row in rows:
                print(f"   ID: {row[0]}, Titre: {row[1]}, Matière: {row[2]}")
                print(f"   Difficulté: {row[3]}, Durée: {row[4]} min")
                print("   ---")
        
        # 5. Vérifier les valeurs NULL ou vides
        print("\n4. 🔍 VÉRIFICATION DES VALEURS NULL/VIDES")
        print("-" * 40)
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN progress_percentage IS NULL THEN 1 END) as null_progress,
                COUNT(CASE WHEN current_step IS NULL THEN 1 END) as null_step,
                COUNT(CASE WHEN total_steps IS NULL THEN 1 END) as null_total
            FROM student_learning_paths
        """)
        
        stats = cursor.fetchone()
        print(f"   Total: {stats[0]}")
        print(f"   Progress NULL: {stats[1]}")
        print(f"   Current Step NULL: {stats[2]}")
        print(f"   Total Steps NULL: {stats[3]}")
        
        conn.close()
        
    except Exception as e:
        print(f"💥 Erreur: {e}")

def fix_progress_data():
    """Corriger les données de progression manquantes"""
    
    db_path = "najah_ai.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données {db_path} non trouvée")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("\n🔧 CORRECTION DES DONNÉES DE PROGRESSION")
        print("=" * 50)
        
        # 1. Mettre à jour les progress_percentage NULL
        cursor.execute("""
            UPDATE student_learning_paths 
            SET progress_percentage = CASE 
                WHEN current_step IS NOT NULL AND total_steps IS NOT NULL AND total_steps > 0
                THEN ROUND((CAST(current_step AS FLOAT) / CAST(total_steps AS FLOAT)) * 100, 2)
                ELSE 0
            END
            WHERE progress_percentage IS NULL
        """)
        
        updated_rows = cursor.rowcount
        print(f"   ✅ {updated_rows} lignes de progression mises à jour")
        
        # 2. Mettre à jour les current_step NULL
        cursor.execute("""
            UPDATE student_learning_paths 
            SET current_step = 1
            WHERE current_step IS NULL
        """)
        
        updated_rows = cursor.rowcount
        print(f"   ✅ {updated_rows} lignes de current_step mises à jour")
        
        # 3. Mettre à jour les total_steps NULL
        cursor.execute("""
            UPDATE student_learning_paths 
            SET total_steps = 15
            WHERE total_steps IS NULL
        """)
        
        updated_rows = cursor.rowcount
        print(f"   ✅ {updated_rows} lignes de total_steps mises à jour")
        
        # 4. Vérifier le résultat
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN progress_percentage IS NULL THEN 1 END) as null_progress,
                COUNT(CASE WHEN current_step IS NULL THEN 1 END) as null_step,
                COUNT(CASE WHEN total_steps IS NULL THEN 1 END) as null_total
            FROM student_learning_paths
        """)
        
        stats = cursor.fetchone()
        print(f"\n   📊 APRÈS CORRECTION:")
        print(f"   Total: {stats[0]}")
        print(f"   Progress NULL: {stats[1]}")
        print(f"   Current Step NULL: {stats[2]}")
        print(f"   Total Steps NULL: {stats[3]}")
        
        conn.commit()
        conn.close()
        
        print("\n   🎯 Correction terminée avec succès!")
        
    except Exception as e:
        print(f"💥 Erreur lors de la correction: {e}")

if __name__ == "__main__":
    check_progress_structure()
    fix_progress_data()
