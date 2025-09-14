#!/usr/bin/env python3
"""
Script corrigé pour configurer un nouvel étudiant avec évaluation initiale et parcours
"""

import sqlite3
import os
from datetime import datetime

def setup_new_student_fixed():
    """Configurer un nouvel étudiant avec la vraie structure"""
    print("🎓 CONFIGURATION D'UN NOUVEL ÉTUDIANT (STRUCTURE CORRIGÉE)")
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
        
        # Étape 1: Vérifier l'utilisateur
        print("\n1️⃣ Vérification de l'utilisateur...")
        cursor.execute("SELECT id, username, email, role FROM users WHERE id = 30")
        user = cursor.fetchone()
        
        if user:
            user_id, username, email, role = user
            print(f"   ✅ Utilisateur trouvé: ID {user_id}, {username} ({email}), Rôle: {role}")
        else:
            print("   ❌ Utilisateur non trouvé!")
            return
        
        # Étape 2: Créer une évaluation initiale
        print("\n2️⃣ Création de l'évaluation initiale...")
        
        # Insérer l'évaluation dans la table assessments
        cursor.execute("""
            INSERT INTO assessments 
            (student_id, assessment_type, title, description, subject, priority, estimated_time, status, started_at, created_by, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,  # student_id
            "initial_evaluation",  # assessment_type
            "Test de Positionnement Initial",  # title
            "Évaluation pour déterminer votre niveau et vos besoins d'apprentissage",  # description
            "Général",  # subject
            "high",  # priority
            45,  # estimated_time (minutes)
            "pending",  # status
            datetime.utcnow().isoformat(),  # started_at
            user_id,  # created_by
            datetime.utcnow().isoformat()  # created_at
        ))
        
        assessment_id = cursor.lastrowid
        print(f"   ✅ Évaluation créée: ID {assessment_id}")
        
        # Étape 3: Créer des questions pour l'évaluation
        print("\n3️⃣ Création des questions d'évaluation...")
        
        questions_data = [
            ("Quel est votre niveau en mathématiques ?", "Mathématiques", "easy", "Débutant", 1.0, 1),
            ("Connaissez-vous les bases de la grammaire française ?", "Français", "easy", "Oui", 1.0, 2),
            ("Avez-vous des connaissances en sciences ?", "Sciences", "easy", "Basiques", 1.0, 3),
            ("Quel est votre objectif principal d'apprentissage ?", "Général", "easy", "Progression", 1.0, 4),
            ("Combien de temps pouvez-vous consacrer à l'apprentissage par jour ?", "Général", "easy", "30 minutes", 1.0, 5)
        ]
        
        for question, subject, difficulty, correct_answer, points, order in questions_data:
            cursor.execute("""
                INSERT INTO assessment_questions 
                (assessment_id, question_text, question_type, subject, difficulty, correct_answer, points, "order")
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                assessment_id,
                question,
                "multiple_choice",
                subject,
                difficulty,
                correct_answer,
                points,
                order
            ))
        
        print(f"   ✅ {len(questions_data)} questions créées")
        
        # Étape 4: Créer un résultat d'évaluation pour l'étudiant
        print("\n4️⃣ Création du résultat d'évaluation...")
        
        cursor.execute("""
            INSERT INTO assessment_results 
            (assessment_id, student_id, total_score, max_score, percentage, completed_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            assessment_id,
            user_id,
            0.0,  # Score initial
            5.0,  # Score maximum (5 questions)
            0.0,  # Pourcentage initial
            None  # Pas encore complété
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
            """, (user_id, path_id))
            
            if not cursor.fetchone():
                # Assigner le parcours
                cursor.execute("""
                    INSERT INTO student_learning_paths 
                    (student_id, learning_path_id, progress, is_completed, started_at, current_step, total_steps)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_id,
                    path_id,
                    0.0,  # Progression initiale
                    False,  # Non complété
                    datetime.utcnow().isoformat(),
                    1,  # Commencer à la première étape
                    5  # Total d'étapes estimé
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
            SELECT COUNT(*) FROM assessments 
            WHERE student_id = ?
        """, (user_id,))
        assessment_count = cursor.fetchone()[0]
        print(f"   📝 Évaluations: {assessment_count}")
        
        # Vérifier les parcours assignés
        cursor.execute("""
            SELECT COUNT(*) FROM student_learning_paths 
            WHERE student_id = ?
        """, (user_id,))
        paths_count = cursor.fetchone()[0]
        print(f"   🛤️ Parcours assignés: {paths_count}")
        
        conn.close()
        
        print(f"\n🎉 L'étudiant est maintenant prêt pour l'évaluation initiale!")
        print(f"   Rechargez le dashboard pour voir les changements")
        
    except Exception as e:
        print(f"❌ Erreur lors de la configuration: {e}")

if __name__ == "__main__":
    setup_new_student_fixed()







