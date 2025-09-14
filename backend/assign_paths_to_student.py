#!/usr/bin/env python3
"""
Script pour assigner les parcours d'apprentissage à l'étudiant
"""

import sqlite3
import os
from datetime import datetime, timedelta

def assign_paths_to_student():
    """Assigner les parcours à l'étudiant"""
    print("🎯 ASSIGNATION DES PARCOURS À L'ÉTUDIANT")
    print("=" * 60)
    
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db')
    print(f"📁 Base de données: {db_path}")
    
    if not os.path.exists(db_path):
        print("❌ Base de données non trouvée!")
        return
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Étape 1: Vérifier l'étudiant
        print("\n1️⃣ Vérification de l'étudiant...")
        cursor.execute("SELECT id, user_id FROM students WHERE user_id = 30")
        student = cursor.fetchone()
        
        if student:
            student_id, user_id = student
            print(f"   ✅ Étudiant trouvé: ID {student_id}, User ID {user_id}")
        else:
            print("   ❌ Étudiant non trouvé!")
            return
        
        # Étape 2: Vérifier les parcours disponibles
        print("\n2️⃣ Vérification des parcours disponibles...")
        cursor.execute("SELECT id, title, subject FROM learning_paths")
        paths = cursor.fetchall()
        
        if paths:
            print(f"   ✅ {len(paths)} parcours disponibles:")
            for path in paths:
                print(f"      - ID: {path[0]}, Titre: {path[1]}, Matière: {path[2]}")
        else:
            print("   ❌ Aucun parcours disponible!")
            return
        
        # Étape 3: Assigner les parcours à l'étudiant
        print("\n3️⃣ Assignation des parcours à l'étudiant...")
        
        # Supprimer les anciennes assignations
        cursor.execute("DELETE FROM student_learning_paths WHERE student_id = ?", (student_id,))
        print(f"   🗑️ Anciennes assignations supprimées")
        
        # Assigner tous les parcours
        assigned_count = 0
        for path in paths:
            path_id = path[0]
            
            # Insérer l'assignation
            cursor.execute("""
                INSERT INTO student_learning_paths 
                (student_id, learning_path_id, started_at, current_step, progress, is_completed, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                student_id,
                path_id,
                datetime.utcnow().isoformat(),
                1,  # Commencer à la première étape
                0.0,  # Progression initiale
                False,  # Non complété
                datetime.utcnow().isoformat()
            ))
            assigned_count += 1
            print(f"      ✅ Parcours {path[1]} assigné")
        
        # Étape 4: Créer des évaluations pour l'étudiant
        print("\n4️⃣ Création d'évaluations pour l'étudiant...")
        
        # Vérifier les évaluations existantes
        cursor.execute("SELECT id, title FROM assessments")
        assessments = cursor.fetchall()
        
        if assessments:
            print(f"   ✅ {len(assessments)} évaluations disponibles:")
            for assessment in assessments:
                print(f"      - ID: {assessment[0]}, Titre: {assessment[1]}")
            
            # Créer des résultats d'évaluation pour l'étudiant
            for assessment in assessments:
                assessment_id = assessment[0]
                
                # Vérifier si l'étudiant a déjà un résultat
                cursor.execute("""
                    SELECT id FROM assessment_results 
                    WHERE student_id = ? AND assessment_id = ?
                """, (student_id, assessment_id))
                
                if not cursor.fetchone():
                    # Créer un résultat d'évaluation
                    cursor.execute("""
                        INSERT INTO assessment_results 
                        (student_id, assessment_id, score, max_score, percentage, completed, started_at, completed_at, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        student_id,
                        assessment_id,
                        0,  # Score initial
                        100,  # Score maximum
                        0.0,  # Pourcentage initial
                        False,  # Non complété
                        datetime.utcnow().isoformat(),
                        None,  # Pas encore complété
                        datetime.utcnow().isoformat()
                    ))
                    print(f"      ✅ Résultat créé pour {assessment[1]}")
        else:
            print("   ⚠️ Aucune évaluation disponible")
        
        # Valider les changements
        conn.commit()
        print(f"\n✅ {assigned_count} parcours assignés avec succès!")
        
        # Étape 5: Vérification finale
        print("\n5️⃣ Vérification finale...")
        
        # Vérifier les parcours assignés
        cursor.execute("""
            SELECT COUNT(*) FROM student_learning_paths 
            WHERE student_id = ?
        """, (student_id,))
        assigned_paths = cursor.fetchone()[0]
        print(f"   🛤️ Parcours assignés: {assigned_paths}")
        
        # Vérifier les évaluations
        cursor.execute("""
            SELECT COUNT(*) FROM assessment_results 
            WHERE student_id = ?
        """, (student_id,))
        assessment_results = cursor.fetchone()[0]
        print(f"   📝 Résultats d'évaluation: {assessment_results}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de l'assignation: {e}")

if __name__ == "__main__":
    assign_paths_to_student()







