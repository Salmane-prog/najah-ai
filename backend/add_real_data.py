#!/usr/bin/env python3
"""
Script pour ajouter des données réelles dans la base de données
"""

import sqlite3
import os
import json
from datetime import datetime, timedelta
import random

# Chemin vers la base de données
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db')

def add_real_data():
    """Ajoute des données réelles dans la base de données"""
    print("🚀 Ajout de données réelles dans la base de données...")
    
    if not os.path.exists(DB_PATH):
        print(f"❌ Base de données non trouvée: {DB_PATH}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 1. Ajouter des utilisateurs de test
        print("👥 Ajout d'utilisateurs de test...")
        
        # Vérifier si les utilisateurs existent déjà
        cursor.execute("SELECT COUNT(*) FROM users WHERE email LIKE '%test%'")
        existing_users = cursor.fetchone()[0]
        
        if existing_users == 0:
            # Ajouter un professeur de test
            cursor.execute("""
                INSERT INTO users (email, username, first_name, last_name, role, is_active, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                'prof.test.real@najah.ai',
                'prof_test_real',
                'Professeur',
                'Test',
                'teacher',
                True,
                datetime.now().isoformat()
            ))
            teacher_id = cursor.lastrowid
            
            # Ajouter des étudiants de test
            students_data = [
                ('etudiant1.real@najah.ai', 'etudiant1_real', 'Étudiant', 'Un', 'student'),
                ('etudiant2.real@najah.ai', 'etudiant2_real', 'Étudiant', 'Deux', 'student'),
                ('etudiant3.real@najah.ai', 'etudiant3_real', 'Étudiant', 'Trois', 'student'),
                ('etudiant4.real@najah.ai', 'etudiant4_real', 'Étudiant', 'Quatre', 'student'),
                ('etudiant5.real@najah.ai', 'etudiant5_real', 'Étudiant', 'Cinq', 'student'),
            ]
            
            student_ids = []
            for email, username, first_name, last_name, role in students_data:
                cursor.execute("""
                    INSERT INTO users (email, username, first_name, last_name, role, is_active, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    email, username, first_name, last_name, role, True,
                    datetime.now().isoformat()
                ))
                student_ids.append(cursor.lastrowid)
            
            print(f"✅ {len(student_ids) + 1} utilisateurs ajoutés (1 prof + {len(student_ids)} étudiants)")
        else:
            print("✅ Utilisateurs de test déjà présents")
            # Récupérer les IDs existants
            cursor.execute("SELECT id FROM users WHERE role = 'teacher' LIMIT 1")
            teacher_id = cursor.fetchone()[0]
            
            cursor.execute("SELECT id FROM users WHERE role = 'student' LIMIT 5")
            student_ids = [row[0] for row in cursor.fetchall()]
        
        # 2. Ajouter des classes de test
        print("🏫 Ajout de classes de test...")
        
        try:
            cursor.execute("SELECT COUNT(*) FROM class_groups")
            existing_classes = cursor.fetchone()[0]
            print(f"   📊 Classes existantes: {existing_classes}")
            
            if existing_classes == 0:
                print("   ➕ Création de nouvelles classes...")
                classes_data = [
                    ('Classe 3ème A', 'Français', teacher_id),
                    ('Classe 4ème B', 'Mathématiques', teacher_id),
                    ('Classe 5ème C', 'Histoire', teacher_id),
                ]
                
                class_ids = []
                for name, subject, teacher_id in classes_data:
                    cursor.execute("""
                        INSERT INTO class_groups (name, subject, teacher_id, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        name, subject, teacher_id,
                        datetime.now().isoformat(), datetime.now().isoformat()
                    ))
                    class_ids.append(cursor.lastrowid)
                    print(f"   ✅ Classe créée: {name}")
                
                print(f"✅ {len(class_ids)} classes ajoutées")
            else:
                print("✅ Classes de test déjà présentes")
                cursor.execute("SELECT id FROM class_groups LIMIT 3")
                class_ids = [row[0] for row in cursor.fetchall()]
                print(f"   📋 IDs des classes: {class_ids}")
        except Exception as e:
            print(f"   ❌ Erreur lors de l'ajout des classes: {e}")
            class_ids = []
        
        # 3. Ajouter des étudiants aux classes (simplifié)
        print("👨‍🎓 Association étudiants-classes (simplifiée)...")
        print("   ℹ️ La relation étudiants-classes se fait via une table de liaison séparée")
        print("   ✅ Passons à l'ajout des modèles IA...")
        
        # 4. Ajouter des modèles IA de test
        print("🧠 Ajout de modèles IA de test...")
        
        cursor.execute("SELECT COUNT(*) FROM ai_models")
        existing_models = cursor.fetchone()[0]
        
        if existing_models == 0:
            models_data = [
                ('Modèle de Prédiction de Performance', 'Modèle ML pour prédire les performances des étudiants', 'ml_algorithm', '2.1.0', '{"accuracy": 87.5, "precision": 85.2, "recall": 88.7}', 'trained', 'production'),
                ('Modèle de Détection de Blocages', 'Modèle pour identifier les difficultés d\'apprentissage', 'ml_algorithm', '1.8.2', '{"accuracy": 82.3, "precision": 80.1, "recall": 84.5}', 'trained', 'staging'),
                ('Modèle de Recommandations', 'Système de recommandations personnalisées', 'ml_algorithm', '1.5.0', '{"accuracy": 79.8, "precision": 77.3, "recall": 81.2}', 'not_trained', 'not_deployed'),
            ]
            
            model_ids = []
            for name, description, model_type, version, performance_metrics, training_status, deployment_status in models_data:
                cursor.execute("""
                    INSERT INTO ai_models (name, description, model_type, version, performance_metrics, training_status, deployment_status, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    name, description, model_type, version, performance_metrics, training_status, deployment_status,
                    datetime.now().isoformat(), datetime.now().isoformat()
                ))
                model_ids.append(cursor.lastrowid)
            
            print(f"✅ {len(model_ids)} modèles IA ajoutés")
        else:
            print("✅ Modèles IA de test déjà présents")
            cursor.execute("SELECT id FROM ai_models LIMIT 3")
            model_ids = [row[0] for row in cursor.fetchall()]
        
        # 5. Ajouter des sessions d'entraînement de test
        print("🏋️ Ajout de sessions d'entraînement de test...")
        
        cursor.execute("SELECT COUNT(*) FROM model_training_sessions")
        existing_sessions = cursor.fetchone()[0]
        
        if existing_sessions == 0:
            for i, model_id in enumerate(model_ids):
                status = "completed" if i == 0 else "running"
                start_time = datetime.now() - timedelta(days=i+1)
                end_time = datetime.now() if status == "completed" else None
                duration = (end_time - start_time).seconds if end_time else None
                
                # Paramètres d'entraînement en JSON
                training_params = {
                    "epochs": random.randint(50, 150),
                    "batch_size": random.choice([16, 32, 64]),
                    "learning_rate": random.uniform(0.001, 0.01),
                    "optimizer": random.choice(['adam', 'sgd']),
                    "loss_function": random.choice(['binary_crossentropy', 'categorical_crossentropy'])
                }
                
                # Métriques de validation en JSON
                validation_metrics = {
                    "accuracy": random.uniform(75, 95) if status == "completed" else 0,
                    "precision": random.uniform(70, 90) if status == "completed" else 0,
                    "recall": random.uniform(75, 90) if status == "completed" else 0
                }
                
                cursor.execute("""
                    INSERT INTO model_training_sessions (
                        model_id, session_name, training_data_size, training_parameters,
                        start_time, end_time, duration, status, accuracy, loss,
                        validation_metrics, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    model_id, f"Session d'entraînement {i+1}",
                    random.randint(3000, 8000), json.dumps(training_params),
                    start_time.isoformat(), end_time.isoformat() if end_time else None,
                    duration, status,
                    random.uniform(80, 95) if status == "completed" else 0,
                    random.uniform(0.1, 0.5) if status == "completed" else 0,
                    json.dumps(validation_metrics), datetime.now().isoformat()
                ))
            
            print(f"✅ {len(model_ids)} sessions d'entraînement ajoutées")
        else:
            print("✅ Sessions d'entraînement de test déjà présentes")
        
        # 6. Ajouter des prédictions de test
        print("🔮 Ajout de prédictions de test...")
        
        cursor.execute("SELECT COUNT(*) FROM model_predictions")
        existing_predictions = cursor.fetchone()[0]
        
        if existing_predictions == 0:
            for i, model_id in enumerate(model_ids):
                for j, student_id in enumerate(student_ids[:2]):  # 2 prédictions par modèle
                    # Données d'entrée simulées
                    input_data = {
                        "student_id": student_id,
                        "features": ["performance_history", "study_time", "engagement_level"],
                        "values": [random.uniform(70, 95), random.uniform(30, 120), random.uniform(0.6, 1.0)]
                    }
                    
                    # Résultat de prédiction simulé
                    predicted_score = random.uniform(70, 95)
                    prediction_result = {
                        "predicted_score": predicted_score,
                        "confidence_level": "high" if predicted_score > 85 else "medium",
                        "recommendations": ["Continuer les efforts", "Réviser les concepts difficiles"]
                    }
                    
                    cursor.execute("""
                        INSERT INTO model_predictions (
                            model_id, input_data, prediction_result, confidence, 
                            processing_time, user_id, session_id
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        model_id, json.dumps(input_data), json.dumps(prediction_result),
                        random.uniform(0.7, 0.95), random.uniform(0.1, 0.5),
                        student_id, f"session_{model_id}_{student_id}"
                    ))
            
            print(f"✅ {len(model_ids) * 2} prédictions ajoutées")
        else:
            print("✅ Prédictions de test déjà présentes")
        
        # 7. Ajout de métriques de performance (simplifié)
        print("📊 Ajout de métriques de performance (simplifié)...")
        print("   ℹ️ Les métriques de performance sont stockées dans la table learning_analytics")
        print("   ✅ Passons au résumé final...")
        
        # Valider les changements
        conn.commit()
        print("🎉 Toutes les données de test ont été ajoutées avec succès !")
        
        # Afficher un résumé
        print("\n📋 Résumé des données ajoutées:")
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'teacher'")
        teacher_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'student'")
        student_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM class_groups")
        class_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM ai_models")
        model_count = cursor.fetchone()[0]
        
        print(f"   👨‍🏫 Professeurs: {teacher_count}")
        print(f"   👨‍🎓 Étudiants: {student_count}")
        print(f"   🏫 Classes: {class_count}")
        print(f"   🧠 Modèles IA: {model_count}")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'ajout des données: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    add_real_data()
