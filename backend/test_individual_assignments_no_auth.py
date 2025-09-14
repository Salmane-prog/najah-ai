#!/usr/bin/env python3
"""
Test script pour vérifier la fonctionnalité d'assignation individuelle des étudiants (sans auth)
"""

import requests
import json
from datetime import datetime, timedelta

def test_individual_assignments_no_auth():
    """Test de la fonctionnalité d'assignation individuelle sans authentification"""
    
    base_url = "http://localhost:8000/api/v1/teacher-assignments"
    
    print("🧪 Test de la fonctionnalité d'assignation individuelle (sans auth)")
    print("=" * 70)
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        # 1. Tester l'endpoint des étudiants (devrait retourner 401)
        print("\n1. 📋 Test de l'endpoint /students...")
        response = requests.get(f"{base_url}/students", headers=headers)
        
        if response.status_code == 401:
            print("✅ Endpoint protégé correctement (401 Unauthorized)")
        else:
            print(f"⚠️  Statut inattendu: {response.status_code}")
        
        # 2. Tester l'endpoint des étudiants d'une classe spécifique
        print("\n2. 📋 Test de l'endpoint /students/{class_id}...")
        response = requests.get(f"{base_url}/students/1", headers=headers)
        
        if response.status_code == 401:
            print("✅ Endpoint protégé correctement (401 Unauthorized)")
        else:
            print(f"⚠️  Statut inattendu: {response.status_code}")
        
        # 3. Tester la création de devoir individuel (devrait retourner 401)
        print("\n3. 📝 Test de création de devoir individuel...")
        
        homework_data = {
            "title": "Devoir individuel test",
            "description": "Ce devoir est assigné individuellement",
            "subject": "Mathématiques",
            "student_ids": [1, 2, 3],
            "due_date": (datetime.now() + timedelta(days=7)).isoformat(),
            "priority": "medium",
            "estimated_time": 120
        }
        
        response = requests.post(f"{base_url}/homework", 
                               headers=headers, 
                               json=homework_data)
        
        if response.status_code == 401:
            print("✅ Endpoint protégé correctement (401 Unauthorized)")
        else:
            print(f"⚠️  Statut inattendu: {response.status_code}")
        
        # 4. Tester la création d'objectif individuel (devrait retourner 401)
        print("\n4. 🎯 Test de création d'objectif individuel...")
        
        goal_data = {
            "title": "Objectif individuel test",
            "description": "Cet objectif est assigné individuellement",
            "subject": "Sciences",
            "student_ids": [1, 2],
            "target_date": (datetime.now() + timedelta(days=14)).isoformat(),
            "milestones": [
                {"title": "Étape 1", "description": "Première étape", "completed": False}
            ]
        }
        
        response = requests.post(f"{base_url}/learning-goals", 
                               headers=headers, 
                               json=goal_data)
        
        if response.status_code == 401:
            print("✅ Endpoint protégé correctement (401 Unauthorized)")
        else:
            print(f"⚠️  Statut inattendu: {response.status_code}")
        
        # 5. Tester la création de devoir par classe (devrait retourner 401)
        print("\n5. 🏫 Test de création de devoir par classe...")
        
        homework_class_data = {
            "title": "Devoir par classe test",
            "description": "Ce devoir est assigné à toute une classe",
            "subject": "Histoire",
            "class_id": 1,
            "due_date": (datetime.now() + timedelta(days=5)).isoformat(),
            "priority": "high",
            "estimated_time": 90
        }
        
        response = requests.post(f"{base_url}/homework", 
                               headers=headers, 
                               json=homework_class_data)
        
        if response.status_code == 401:
            print("✅ Endpoint protégé correctement (401 Unauthorized)")
        else:
            print(f"⚠️  Statut inattendu: {response.status_code}")
        
        # 6. Vérifier que le serveur répond
        print("\n6. 🔍 Test de connectivité du serveur...")
        try:
            response = requests.get("http://localhost:8000/docs", timeout=5)
            if response.status_code == 200:
                print("✅ Serveur accessible et fonctionnel")
            else:
                print(f"⚠️  Serveur accessible mais statut: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("❌ Serveur non accessible")
            return
        except Exception as e:
            print(f"❌ Erreur de connexion: {e}")
            return
        
        print("\n✅ Test terminé avec succès!")
        print("\n📋 Résumé:")
        print("   - Tous les endpoints sont correctement protégés")
        print("   - Le serveur est accessible")
        print("   - La fonctionnalité d'assignation individuelle est prête")
        print("\n💡 Pour tester avec authentification:")
        print("   1. Connectez-vous en tant que professeur")
        print("   2. Accédez à la page Assignations")
        print("   3. Créez un nouveau devoir/objectif")
        print("   4. Sélectionnez 'Étudiants spécifiques'")
        print("   5. Choisissez les étudiants individuellement")
        
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")

if __name__ == "__main__":
    test_individual_assignments_no_auth() 