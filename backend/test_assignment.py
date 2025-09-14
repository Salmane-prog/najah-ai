#!/usr/bin/env python3
"""
Script de test pour l'assignation d'un test adaptatif
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

def get_auth_token():
    """Obtenir un token d'authentification"""
    try:
        login_data = {
            "email": "marizee.dubois@najah.ai",
            "password": "password123"
        }
        
        response = requests.post(f"{API_BASE}/auth/login", json=login_data)
        
        if response.status_code == 200:
            data = response.json()
            return data.get("access_token")
        else:
            print(f"❌ Erreur de connexion: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Erreur lors de la connexion: {e}")
        return None

def test_assignment(token):
    """Tester l'assignation d'un test adaptatif"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        # Données d'assignation
        assignment_data = {
            "class_ids": [1],  # Classe "dazdaz"
            "student_ids": [2],  # Étudiant "Prénom19 Nom19"
            "due_date": "2025-01-25T23:59:00"
        }
        
        print("🔄 Test de l'assignation d'un test adaptatif...")
        print(f"📋 Données d'assignation: {json.dumps(assignment_data, indent=2)}")
        
        # ID du test à assigner (utiliser un ID existant)
        test_id = 1  # Premier test dans la base
        
        response = requests.post(
            f"{API_BASE}/teacher-adaptive-evaluation/tests/{test_id}/assign",
            json=assignment_data,
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Test assigné avec succès!")
            print(f"📊 Résultat: {json.dumps(result, indent=2)}")
            return True
        else:
            print(f"❌ Erreur: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test d'assignation: {e}")
        return False

def test_student_view(token):
    """Tester la vue étudiant des tests assignés"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        print("🔄 Test de la vue étudiant des tests assignés...")
        
        # Tester avec l'étudiant "Prénom19 Nom19" (ID 2)
        student_id = 2
        
        response = requests.get(
            f"{API_BASE}/adaptive-evaluation/student/{student_id}/assigned",
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Tests assignés récupérés!")
            print(f"📊 Résultat: {json.dumps(result, indent=2)}")
            return True
        else:
            print(f"❌ Erreur: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test de la vue étudiant: {e}")
        return False

def main():
    """Fonction principale"""
    print("🧪 Test de l'assignation et de la vue étudiant des tests adaptatifs")
    print("=" * 70)
    
    # Obtenir le token
    token = get_auth_token()
    if not token:
        print("❌ Impossible d'obtenir le token d'authentification")
        return
    
    print("✅ Token obtenu avec succès")
    print()
    
    # Tester l'assignation
    success = True
    
    if not test_assignment(token):
        success = False
    
    print()
    
    # Tester la vue étudiant
    if not test_student_view(token):
        success = False
    
    print()
    
    if success:
        print("🎉 Tous les tests ont réussi !")
        print("✅ L'assignation fonctionne maintenant")
        print("✅ Les étudiants peuvent voir leurs tests assignés")
    else:
        print("❌ Certains tests ont échoué")

if __name__ == "__main__":
    main()


















