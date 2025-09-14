#!/usr/bin/env python3
"""
Script pour corriger les données de progression existantes
dans la table student_learning_paths
"""

import sqlite3
import os
from datetime import datetime

def fix_existing_progress_data():
    """Corriger les données de progression existantes"""
    
    db_path = "najah_ai.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données {db_path} non trouvée")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔧 CORRECTION DES DONNÉES DE PROGRESSION EXISTANTES")
        print("=" * 60)
        
        # 1. Vérifier l'état actuel
        print("\n1. 📊 ÉTAT ACTUEL DES DONNÉES")
        print("-" * 40)
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN progress_percentage IS NULL THEN 1 END) as null_progress,
                COUNT(CASE WHEN current_step IS NULL THEN 1 END) as null_step,
                COUNT(CASE WHEN total_steps IS NULL THEN 1 END) as null_total,
                COUNT(CASE WHEN progress_percentage = 0 THEN 1 END) as zero_progress
            FROM student_learning_paths
        """)
        
        stats = cursor.fetchone()
        print(f"   Total: {stats[0]}")
        print(f"   Progress NULL: {stats[1]}")
        print(f"   Current Step NULL: {stats[2]}")
        print(f"   Total Steps NULL: {stats[3]}")
        print(f"   Progress = 0: {stats[4]}")
        
        # 2. Afficher quelques exemples de données problématiques
        print("\n2. 🔍 EXEMPLES DE DONNÉES PROBLÉMATIQUES")
        print("-" * 40)
        
        cursor.execute("""
            SELECT 
                id, student_id, learning_path_id, current_step, total_steps,
                progress_percentage, is_completed
            FROM student_learning_paths 
            WHERE progress_percentage IS NULL OR current_step IS NULL OR total_steps IS NULL
            LIMIT 5
        """)
        
        problematic_rows = cursor.fetchall()
        
        if problematic_rows:
            print("   Données problématiques trouvées:")
            for row in problematic_rows:
                print(f"   ID: {row[0]}, Student: {row[1]}, Path: {row[2]}")
                print(f"   Step: {row[3]}, Total: {row[4]}, Progress: {row[5]}%, Completed: {row[6]}")
                print("   ---")
        else:
            print("   ✅ Aucune donnée problématique trouvée")
        
        # 3. Corriger les données
        print("\n3. 🔧 CORRECTION DES DONNÉES")
        print("-" * 40)
        
        # Corriger les total_steps NULL
        cursor.execute("""
            UPDATE student_learning_paths 
            SET total_steps = 15
            WHERE total_steps IS NULL
        """)
        
        updated_total_steps = cursor.rowcount
        print(f"   ✅ {updated_total_steps} lignes de total_steps corrigées")
        
        # Corriger les current_step NULL
        cursor.execute("""
            UPDATE student_learning_paths 
            SET current_step = 1
            WHERE current_step IS NULL
        """)
        
        updated_current_steps = cursor.rowcount
        print(f"   ✅ {updated_current_steps} lignes de current_step corrigées")
        
        # Corriger les progress_percentage NULL ou 0
        cursor.execute("""
            UPDATE student_learning_paths 
            SET progress_percentage = CASE 
                WHEN current_step IS NOT NULL AND total_steps IS NOT NULL AND total_steps > 0
                THEN ROUND((CAST(current_step AS FLOAT) / CAST(total_steps AS FLOAT)) * 100, 2)
                ELSE 0
            END
            WHERE progress_percentage IS NULL OR progress_percentage = 0
        """)
        
        updated_progress = cursor.rowcount
        print(f"   ✅ {updated_progress} lignes de progress_percentage corrigées")
        
        # 4. Vérifier le résultat
        print("\n4. 📊 RÉSULTAT APRÈS CORRECTION")
        print("-" * 40)
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN progress_percentage IS NULL THEN 1 END) as null_progress,
                COUNT(CASE WHEN current_step IS NULL THEN 1 END) as null_step,
                COUNT(CASE WHEN total_steps IS NULL THEN 1 END) as null_total,
                COUNT(CASE WHEN progress_percentage = 0 THEN 1 END) as zero_progress
            FROM student_learning_paths
        """)
        
        stats_after = cursor.fetchone()
        print(f"   Total: {stats_after[0]}")
        print(f"   Progress NULL: {stats_after[1]}")
        print(f"   Current Step NULL: {stats_after[2]}")
        print(f"   Total Steps NULL: {stats_after[3]}")
        print(f"   Progress = 0: {stats_after[4]}")
        
        # 5. Afficher des exemples de données corrigées
        print("\n5. 📋 EXEMPLES DE DONNÉES CORRIGÉES")
        print("-" * 40)
        
        cursor.execute("""
            SELECT 
                id, student_id, learning_path_id, current_step, total_steps,
                progress_percentage, is_completed
            FROM student_learning_paths 
            LIMIT 5
        """)
        
        corrected_rows = cursor.fetchall()
        
        if corrected_rows:
            print("   Données corrigées:")
            for row in corrected_rows:
                print(f"   ID: {row[0]}, Student: {row[1]}, Path: {row[2]}")
                print(f"   Step: {row[3]}/{row[4]}, Progress: {row[5]}%, Completed: {row[6]}")
                print("   ---")
        
        # 6. Vérifier spécifiquement pour l'utilisateur 30
        print("\n6. 👤 VÉRIFICATION POUR L'UTILISATEUR 30")
        print("-" * 40)
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                AVG(progress_percentage) as avg_progress,
                MIN(progress_percentage) as min_progress,
                MAX(progress_percentage) as max_progress
            FROM student_learning_paths 
            WHERE student_id = 30
        """)
        
        user_stats = cursor.fetchone()
        
        if user_stats[0] > 0:
            print(f"   Total parcours: {user_stats[0]}")
            print(f"   Progression moyenne: {user_stats[1]:.2f}%")
            print(f"   Progression min: {user_stats[2]:.2f}%")
            print(f"   Progression max: {user_stats[3]:.2f}%")
        else:
            print("   ❌ Aucun parcours trouvé pour l'utilisateur 30")
        
        conn.commit()
        conn.close()
        
        print("\n   🎯 Correction terminée avec succès!")
        
    except Exception as e:
        print(f"💥 Erreur lors de la correction: {e}")

if __name__ == "__main__":
    fix_existing_progress_data()
