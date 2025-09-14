#!/usr/bin/env python3
"""
Script de test pour l'endpoint de création de test adaptatif
"""

import requests
import json
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:8000"
API_ENDPOINT = f"{BASE_URL}/api/v1/adaptive-evaluation/tests/"

def test_create_adaptive_test():
    """Test de création d'un test adaptatif"""
    
    print("🧪 Test de création de test adaptatif")
    print("=" * 50)
    
    # 1. D'abord, récupérer un token d'authentification
    print("1️⃣ Récupération du token d'authentification...")
    
    login_data = {
        "email": "marizee.dubois@najah.ai",
        "password": "password123"  # Remplacez par le bon mot de passe
    }
    
    try:
        login_response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
        print(f"   Status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            access_token = token_data.get("access_token")
            print(f"   ✅ Token récupéré: {access_token[:50]}...")
        else:
            print(f"   ❌ Échec de la connexion: {login_response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur lors de la connexion: {e}")
        return False
    
    # 2. Tester la création du test avec le token
    print("\n2️⃣ Test de création du test adaptatif...")
    
    test_data = {
        "title": "Test de Français - Grammaire",
        "subject": "Français",
        "description": "Test adaptatif de grammaire française",
        "difficulty_min": 3,
        "difficulty_max": 7,
        "estimated_duration": 30,
        "total_questions": 10,
        "adaptation_type": "hybrid",
        "learning_objectives": "Maîtriser les règles de grammaire de base",
        "created_by": 33,
        "questions": [
            {
                "question_text": "Quel est l'article correct ? '___ chat'",
                "question_type": "multiple_choice",
                "difficulty_level": 3,
                "learning_objective": "Reconnaître les articles définis",
                "options": ["Le", "La", "Les", "L'"],
                "correct_answer": "Le",
                "explanation": "Le mot 'chat' est masculin singulier"
            },
            {
                "question_text": "Comment se conjugue 'être' à la 1ère personne ?",
                "question_type": "multiple_choice",
                "difficulty_level": 4,
                "learning_objective": "Conjuguer le verbe être",
                "options": ["suis", "es", "est", "sont"],
                "correct_answer": "suis",
                "explanation": "Le verbe 'être' à la 1ère personne se conjugue 'suis'"
            }
        ]
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        print(f"   📤 Envoi de la requête à: {API_ENDPOINT}")
        print(f"   📋 Données: {json.dumps(test_data, indent=2)}")
        print(f"   🔑 Headers: {json.dumps(headers, indent=2)}")
        
        response = requests.post(API_ENDPOINT, json=test_data, headers=headers)
        
        print(f"\n   📥 Réponse reçue:")
        print(f"   Status: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        print(f"   Body: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Test créé avec succès !")
            return True
        elif response.status_code == 403:
            print("   ❌ Erreur 403: Accès refusé")
            print("   💡 Vérifiez que l'utilisateur a bien le rôle 'teacher'")
            return False
        elif response.status_code == 401:
            print("   ❌ Erreur 401: Non authentifié")
            print("   💡 Vérifiez que le token est valide")
            return False
        else:
            print(f"   ❌ Erreur {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur lors de la requête: {e}")
        return False

def test_endpoint_access():
    """Test d'accès à l'endpoint sans authentification"""
    
    print("\n3️⃣ Test d'accès sans authentification...")
    
    try:
        response = requests.post(API_ENDPOINT, json={})
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 401:
            print("   ✅ Endpoint protégé correctement (401 attendu)")
        else:
            print(f"   ⚠️ Status inattendu: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")

if __name__ == "__main__":
    print("🚀 Démarrage des tests de l'endpoint adaptatif")
    print(f"📍 URL de test: {API_ENDPOINT}")
    print(f"⏰ Heure: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test d'accès sans authentification
    test_endpoint_access()
    
    # Test de création avec authentification
    success = test_create_adaptive_test()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Tous les tests ont réussi !")
    else:
        print("❌ Certains tests ont échoué")
    
    print("🏁 Fin des tests")
