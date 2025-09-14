#!/usr/bin/env python3
"""
Test script pour vérifier la fonctionnalité d'assignation individuelle des étudiants
"""

import requests
import json
from datetime import datetime, timedelta

def test_individual_assignments():
    """Test de la fonctionnalité d'assignation individuelle"""
    
    base_url = "http://localhost:8000/api/v1/teacher-assignments"
    
    print("🧪 Test de la fonctionnalité d'assignation individuelle")
    print("=" * 60)
    
    # Simuler un token d'authentification (remplacer par un vrai token)
    headers = {
        'Authorization': 'Bearer test_token',
        'Content-Type': 'application/json'
    }
    
    try:
        # 1. Récupérer tous les étudiants du professeur
        print("\n1. 📋 Récupération des étudiants du professeur...")
        response = requests.get(f"{base_url}/students", headers=headers)
        
        if response.status_code == 200:
            students = response.json()
            print(f"✅ {len(students)} étudiants trouvés")
            for student in students[:3]:  # Afficher les 3 premiers
                print(f"   - {student['first_name']} {student['last_name']} ({student['username']})")
        else:
            print(f"❌ Erreur: {response.status_code} - {response.text}")
            return
        
        if not students:
            print("⚠️  Aucun étudiant trouvé, impossible de tester l'assignation individuelle")
            return
        
        # 2. Récupérer les classes du professeur
        print("\n2. 🏫 Récupération des classes...")
        class_response = requests.get("http://localhost:8000/api/v1/class_groups/", headers=headers)
        
        if class_response.status_code == 200:
            classes = class_response.json()
            print(f"✅ {len(classes)} classes trouvées")
        else:
            print(f"❌ Erreur: {class_response.status_code} - {class_response.text}")
            return
        
        # 3. Test d'assignation individuelle de devoir
        print("\n3. 📝 Test d'assignation individuelle de devoir...")
        
        # Sélectionner les 2 premiers étudiants
        selected_students = [students[0]['id'], students[1]['id']] if len(students) >= 2 else [students[0]['id']]
        
        homework_data = {
            "title": "Devoir individuel test",
            "description": "Ce devoir est assigné individuellement à des étudiants spécifiques",
            "subject": "Mathématiques",
            "student_ids": selected_students,
            "due_date": (datetime.now() + timedelta(days=7)).isoformat(),
            "priority": "medium",
            "estimated_time": 120
        }
        
        response = requests.post(f"{base_url}/homework", 
                               headers=headers, 
                               json=homework_data)
        
        if response.status_code == 200:
            created_homeworks = response.json()
            print(f"✅ {len(created_homeworks)} devoirs créés individuellement")
            for homework in created_homeworks:
                print(f"   - Devoir ID: {homework['id']}, Assigné à: {homework['assigned_to']}")
        else:
            print(f"❌ Erreur: {response.status_code} - {response.text}")
        
        # 4. Test d'assignation individuelle d'objectif
        print("\n4. 🎯 Test d'assignation individuelle d'objectif...")
        
        goal_data = {
            "title": "Objectif individuel test",
            "description": "Cet objectif est assigné individuellement à des étudiants spécifiques",
            "subject": "Sciences",
            "student_ids": selected_students,
            "target_date": (datetime.now() + timedelta(days=14)).isoformat(),
            "milestones": [
                {"title": "Étape 1", "description": "Première étape", "completed": False},
                {"title": "Étape 2", "description": "Deuxième étape", "completed": False}
            ]
        }
        
        response = requests.post(f"{base_url}/learning-goals", 
                               headers=headers, 
                               json=goal_data)
        
        if response.status_code == 200:
            created_goals = response.json()
            print(f"✅ {len(created_goals)} objectifs créés individuellement")
            for goal in created_goals:
                print(f"   - Objectif ID: {goal['id']}, Titre: {goal['title']}")
        else:
            print(f"❌ Erreur: {response.status_code} - {response.text}")
        
        # 5. Test d'assignation par classe (pour comparaison)
        if classes:
            print("\n5. 🏫 Test d'assignation par classe (pour comparaison)...")
            
            homework_class_data = {
                "title": "Devoir par classe test",
                "description": "Ce devoir est assigné à toute une classe",
                "subject": "Histoire",
                "class_id": classes[0]['id'],
                "due_date": (datetime.now() + timedelta(days=5)).isoformat(),
                "priority": "high",
                "estimated_time": 90
            }
            
            response = requests.post(f"{base_url}/homework", 
                                   headers=headers, 
                                   json=homework_class_data)
            
            if response.status_code == 200:
                created_homeworks = response.json()
                print(f"✅ {len(created_homeworks)} devoirs créés pour la classe")
            else:
                print(f"❌ Erreur: {response.status_code} - {response.text}")
        
        # 6. Vérifier les devoirs créés
        print("\n6. 📊 Vérification des devoirs créés...")
        response = requests.get(f"{base_url}/homework", headers=headers)
        
        if response.status_code == 200:
            all_homeworks = response.json()
            print(f"✅ Total de {len(all_homeworks)} devoirs trouvés")
            
            # Compter les devoirs individuels vs par classe
            individual_count = 0
            class_count = 0
            
            for homework in all_homeworks:
                if "Devoir individuel" in homework['title']:
                    individual_count += 1
                elif "Devoir par classe" in homework['title']:
                    class_count += 1
            
            print(f"   - Devoirs individuels: {individual_count}")
            print(f"   - Devoirs par classe: {class_count}")
        
        print("\n✅ Test terminé avec succès!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Erreur de connexion: Assurez-vous que le serveur backend est démarré")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")

if __name__ == "__main__":
    test_individual_assignments() 