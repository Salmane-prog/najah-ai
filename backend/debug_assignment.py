#!/usr/bin/env python3
"""
Script pour déboguer l'assignation et voir l'ID exact reçu
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

def debug_assignment(token):
    """Déboguer l'assignation avec l'ID problématique"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        # ID problématique reçu du frontend
        problematic_test_id = 1755444025108
        
        print(f"🔍 Débogage de l'assignation avec l'ID: {problematic_test_id}")
        print(f"📊 Type de l'ID: {type(problematic_test_id)}")
        print(f"📊 Taille de l'ID: {len(str(problematic_test_id))} caractères")
        
        # Vérifier si cet ID existe dans la base
        print(f"\n🔄 Vérification de l'existence du test {problematic_test_id}...")
        
        response = requests.get(
            f"{API_BASE}/teacher-adaptive-evaluation/tests/{problematic_test_id}",
            headers=headers
        )
        
        print(f"📊 Status de la vérification: {response.status_code}")
        if response.status_code == 404:
            print("❌ Test non trouvé - L'ID n'existe pas dans la base")
        elif response.status_code == 200:
            print("✅ Test trouvé - L'ID existe")
        else:
            print(f"⚠️ Réponse inattendue: {response.text}")
        
        # Essayer d'assigner avec un ID valide
        print(f"\n🔄 Test d'assignation avec un ID valide (1)...")
        
        assignment_data = {
            "class_ids": [1],
            "student_ids": [],
            "due_date": "2025-01-25T23:59:00"
        }
        
        response = requests.post(
            f"{API_BASE}/teacher-adaptive-evaluation/tests/1/assign",
            json=assignment_data,
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Assignation réussie avec l'ID 1!")
            print(f"📊 Résultat: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ Erreur avec l'ID 1: {response.status_code} - {response.text}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du débogage: {e}")
        return False

def main():
    """Fonction principale"""
    print("🔍 Débogage de l'assignation avec ID problématique")
    print("=" * 60)
    
    # Obtenir le token
    token = get_auth_token()
    if not token:
        print("❌ Impossible d'obtenir le token d'authentification")
        return
    
    print("✅ Token obtenu avec succès")
    print()
    
    # Déboguer l'assignation
    debug_assignment(token)
    
    print("\n🎯 Conclusion:")
    print("L'ID 1755444025108 semble être un timestamp JavaScript")
    print("Il faut vérifier pourquoi le frontend envoie cet ID au lieu de l'ID réel du test")

if __name__ == "__main__":
    main()


















