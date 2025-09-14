#!/usr/bin/env python3
"""
Script pour créer des données de test complètes avec une progression réelle
pour l'utilisateur 30
"""

import sqlite3
import os
from datetime import datetime, timedelta

def create_complete_test_data():
    """Créer des données de test complètes avec progression réelle"""
    
    db_path = "najah_ai.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données {db_path} non trouvée")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🚀 CRÉATION DE DONNÉES DE TEST COMPLÈTES")
        print("=" * 60)
        
        # 1. Vérifier que l'utilisateur 30 existe
        print("\n1. 👤 VÉRIFICATION DE L'UTILISATEUR 30")
        print("-" * 40)
        
        cursor.execute("SELECT id FROM users WHERE id = 30")
        user_exists = cursor.fetchone()
        
        if not user_exists:
            print("   ❌ Utilisateur 30 non trouvé")
            print("   🔧 Création de l'utilisateur 30...")
            
            # Créer l'utilisateur 30
            cursor.execute("""
                INSERT INTO users (id, username, email, full_name, role, created_at)
                VALUES (30, 'student30', 'student30@najah.edu', 'Étudiant Test 30', 'student', ?)
            """, (datetime.now().isoformat(),))
            
            print("   ✅ Utilisateur 30 créé")
        else:
            print("   ✅ Utilisateur 30 existe déjà")
        
        # 2. Vérifier que des parcours existent
        print("\n2. 🗺️ VÉRIFICATION DES PARCOURS")
        print("-" * 40)
        
        cursor.execute("SELECT id, title, subject FROM learning_paths LIMIT 10")
        paths = cursor.fetchall()
        
        if not paths:
            print("   ❌ Aucun parcours d'apprentissage trouvé")
            print("   🔧 Création de parcours de test...")
            
            # Créer des parcours de test
            test_paths = [
                ("Parcours Mathématiques", "Mathématiques", "medium", 120),
                ("Parcours Français", "Français", "medium", 90),
                ("Parcours Histoire", "Histoire", "easy", 75),
                ("Parcours Sciences", "Sciences", "hard", 150),
                ("Parcours Géographie", "Géographie", "medium", 60),
                ("Parcours Littérature", "Littérature", "medium", 100),
                ("Parcours Philosophie", "Philosophie", "hard", 80),
                ("Parcours Arts", "Arts", "easy", 45),
                ("Parcours Musique", "Musique", "medium", 70),
                ("Parcours Sport", "Sport", "easy", 30),
                ("Parcours Informatique", "Informatique", "hard", 180),
                ("Parcours Langues", "Langues", "medium", 110),
                ("Parcours Économie", "Économie", "medium", 85),
                ("Parcours Droit", "Droit", "hard", 95),
                ("Parcours Médecine", "Médecine", "hard", 200),
                ("Parcours Ingénierie", "Ingénierie", "hard", 160),
                ("Parcours Architecture", "Architecture", "medium", 130),
                ("Parcours Design", "Design", "medium", 90)
            ]
            
            for title, subject, difficulty, duration in test_paths:
                cursor.execute("""
                    INSERT INTO learning_paths (title, subject, difficulty, estimated_duration, created_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (title, subject, difficulty, duration, datetime.now().isoformat()))
            
            print(f"   ✅ {len(test_paths)} parcours de test créés")
            
            # Récupérer les IDs des parcours créés
            cursor.execute("SELECT id FROM learning_paths")
            paths = cursor.fetchall()
        
        print(f"   ✅ {len(paths)} parcours disponibles")
        
        # 3. Créer des données de progression variées
        print("\n3. 📊 CRÉATION DES DONNÉES DE PROGRESSION")
        print("-" * 40)
        
        # Vider la table existante
        cursor.execute("DELETE FROM student_learning_paths WHERE student_id = 30")
        print("   🗑️ Anciennes données supprimées")
        
        # Créer des données de progression variées
        test_data = []
        
        for i, (path_id,) in enumerate(paths):
            # Progression variée pour tester différents scénarios
            if i == 0:  # Premier parcours - début
                current_step = 1
                progress = 6.67  # 1/15 * 100
                is_completed = False
            elif i == 1:  # Deuxième parcours - milieu
                current_step = 8
                progress = 53.33  # 8/15 * 100
                is_completed = False
            elif i == 2:  # Troisième parcours - presque fini
                current_step = 14
                progress = 93.33  # 14/15 * 100
                is_completed = False
            elif i == 3:  # Quatrième parcours - terminé
                current_step = 15
                progress = 100.0
                is_completed = True
            elif i == 4:  # Cinquième parcours - progression moyenne
                current_step = 7
                progress = 46.67  # 7/15 * 100
                is_completed = False
            else:  # Autres parcours - progression variée
                current_step = (i % 15) + 1
                progress = round((current_step / 15) * 100, 2)
                is_completed = False
            
            # Date de début variée
            start_date = datetime.now() - timedelta(days=i*2)
            
            test_data.append((
                30,  # student_id
                path_id,  # learning_path_id
                current_step,  # current_step
                15,  # total_steps
                progress,  # progress_percentage
                70.0 + (i * 3),  # performance_score
                is_completed,  # is_completed
                start_date.isoformat(),  # started_at
                datetime.now().isoformat() if is_completed else None,  # completed_at
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
        print(f"   ✅ {inserted_rows} lignes de données de progression créées")
        
        # 4. Vérifier le résultat
        print("\n4. 📊 VÉRIFICATION DES DONNÉES CRÉÉES")
        print("-" * 40)
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN progress_percentage IS NULL THEN 1 END) as null_progress,
                COUNT(CASE WHEN current_step IS NULL THEN 1 END) as null_step,
                COUNT(CASE WHEN total_steps IS NULL THEN 1 END) as null_total,
                COUNT(CASE WHEN is_completed = 1 THEN 1 END) as completed_paths
            FROM student_learning_paths
            WHERE student_id = 30
        """)
        
        stats = cursor.fetchone()
        print(f"   Total parcours: {stats[0]}")
        print(f"   Progress NULL: {stats[1]}")
        print(f"   Current Step NULL: {stats[2]}")
        print(f"   Total Steps NULL: {stats[3]}")
        print(f"   Parcours terminés: {stats[4]}")
        
        # 5. Afficher des exemples de données
        print("\n5. 📋 EXEMPLES DE DONNÉES CRÉÉES")
        print("-" * 40)
        
        cursor.execute("""
            SELECT 
                id, learning_path_id, current_step, total_steps,
                progress_percentage, is_completed
            FROM student_learning_paths 
            WHERE student_id = 30
            LIMIT 5
        """)
        
        rows = cursor.fetchall()
        
        if rows:
            print("   Données créées:")
            for row in rows:
                print(f"   ID: {row[0]}, Path: {row[1]}, Step: {row[2]}/{row[3]}, Progress: {row[4]}%, Completed: {row[5]}")
                print("   ---")
        
        # 6. Calculer la progression moyenne
        print("\n6. 🎯 CALCUL DE LA PROGRESSION MOYENNE")
        print("-" * 40)
        
        cursor.execute("""
            SELECT 
                AVG(progress_percentage) as avg_progress,
                MIN(progress_percentage) as min_progress,
                MAX(progress_percentage) as max_progress
            FROM student_learning_paths 
            WHERE student_id = 30
        """)
        
        progress_stats = cursor.fetchone()
        
        if progress_stats[0] is not None:
            print(f"   Progression moyenne: {progress_stats[0]:.2f}%")
            print(f"   Progression min: {progress_stats[1]:.2f}%")
            print(f"   Progression max: {progress_stats[2]:.2f}%")
        else:
            print("   ❌ Impossible de calculer la progression")
        
        conn.commit()
        conn.close()
        
        print("\n   🎯 Données de test complètes créées avec succès!")
        print("   🔄 Maintenant, rafraîchissez votre dashboard pour voir les vrais pourcentages!")
        
    except Exception as e:
        print(f"💥 Erreur lors de la création: {e}")

if __name__ == "__main__":
    create_complete_test_data()
