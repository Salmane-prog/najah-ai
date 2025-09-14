#!/usr/bin/env python3
"""
Script pour créer des évaluations et parcours pour l'étudiant
"""

import sqlite3
import os
from datetime import datetime

def create_student_assessments():
    """Créer des évaluations et parcours pour l'étudiant"""
    print("🎓 CRÉATION DES ÉVALUATIONS ET PARCOURS POUR L'ÉTUDIANT")
    print("=" * 70)
    
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
        cursor.execute("SELECT id FROM students WHERE user_id = 30")
        student = cursor.fetchone()
        
        if student:
            student_id = student[0]
            print(f"   ✅ Étudiant trouvé: ID {student_id}")
        else:
            print("   ❌ Étudiant non trouvé!")
            return
        
        # Étape 2: Créer une évaluation initiale
        print("\n2️⃣ Création de l'évaluation initiale...")
        
        # Insérer l'évaluation
        cursor.execute("""
            INSERT INTO assessments 
            (title, description, subject, level, difficulty, total_questions, time_limit, is_adaptive, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "Évaluation Initiale - Test de Positionnement",
            "Évaluation pour déterminer votre niveau et vos besoins d'apprentissage",
            "Général",
            "beginner",
            "easy",
            20,
            45,
            True,
            datetime.utcnow().isoformat()
        ))
        
        assessment_id = cursor.lastrowid
        print(f"   ✅ Évaluation créée: ID {assessment_id}")
        
        # Étape 3: Créer des questions pour l'évaluation
        print("\n3️⃣ Création des questions d'évaluation...")
        
        questions_data = [
            ("Quel est votre niveau en mathématiques ?", "Mathématiques", "beginner"),
            ("Connaissez-vous les bases de la grammaire française ?", "Français", "beginner"),
            ("Avez-vous des connaissances en sciences ?", "Sciences", "beginner"),
            ("Quel est votre objectif principal d'apprentissage ?", "Général", "beginner"),
            ("Combien de temps pouvez-vous consacrer à l'apprentissage par jour ?", "Général", "beginner")
        ]
        
        for i, (question, subject, level) in enumerate(questions_data, 1):
            cursor.execute("""
                INSERT INTO assessment_questions 
                (assessment_id, question_text, question_type, subject, level, order_index, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                assessment_id,
                question,
                "multiple_choice",
                subject,
                level,
                i,
                datetime.utcnow().isoformat()
            ))
        
        print(f"   ✅ {len(questions_data)} questions créées")
        
        # Étape 4: Créer un résultat d'évaluation pour l'étudiant
        print("\n4️⃣ Création du résultat d'évaluation...")
        
        cursor.execute("""
            INSERT INTO assessment_results 
            (student_id, assessment_id, score, max_score, percentage, completed, started_at, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            student_id,
            assessment_id,
            0,  # Score initial
            100,  # Score maximum
            0.0,  # Pourcentage initial
            False,  # Non complété
            datetime.utcnow().isoformat(),
            datetime.utcnow().isoformat()
        ))
        
        print(f"   ✅ Résultat d'évaluation créé")
        
        # Étape 5: Assigner des parcours recommandés
        print("\n5️⃣ Assignation des parcours recommandés...")
        
        # Sélectionner 3 parcours de base
        cursor.execute("""
            SELECT id, title FROM learning_paths 
            WHERE level = 'beginner' AND difficulty = 'easy'
            LIMIT 3
        """)
        recommended_paths = cursor.fetchall()
        
        assigned_count = 0
        for path in recommended_paths:
            path_id, title = path
            
            # Vérifier si déjà assigné
            cursor.execute("""
                SELECT id FROM student_learning_paths 
                WHERE student_id = ? AND learning_path_id = ?
            """, (student_id, path_id))
            
            if not cursor.fetchone():
                # Assigner le parcours
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
                print(f"      ✅ Parcours '{title}' assigné")
        
        # Valider les changements
        conn.commit()
        print(f"\n✅ Configuration terminée avec succès!")
        print(f"   📝 Évaluation initiale créée")
        print(f"   🛤️ {assigned_count} parcours recommandés assignés")
        
        # Étape 6: Vérification finale
        print("\n6️⃣ Vérification finale...")
        
        # Vérifier les évaluations
        cursor.execute("""
            SELECT COUNT(*) FROM assessment_results 
            WHERE student_id = ?
        """, (student_id,))
        assessment_count = cursor.fetchone()[0]
        print(f"   📝 Évaluations: {assessment_count}")
        
        # Vérifier les parcours assignés
        cursor.execute("""
            SELECT COUNT(*) FROM student_learning_paths 
            WHERE student_id = ?
        """, (student_id,))
        paths_count = cursor.fetchone()[0]
        print(f"   🛤️ Parcours assignés: {paths_count}")
        
        conn.close()
        
        print(f"\n🎉 L'étudiant est maintenant prêt pour l'évaluation initiale!")
        print(f"   Rechargez le dashboard pour voir les changements")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")

if __name__ == "__main__":
    create_student_assessments()







