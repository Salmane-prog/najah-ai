#!/usr/bin/env python3
"""
Script pour tester la connexion de l'utilisateur créé
"""

import requests
import json

def test_user_login():
    """Teste la connexion de l'utilisateur de test"""
    
    print("🧪 Test de connexion de l'utilisateur de test...")
    
    # Données de connexion
    login_data = {
        "email": "teacher@example.com",
        "password": "teacher123"
    }
    
    try:
        # Appel à l'API de connexion
        response = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            json=login_data
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            print("✅ Connexion réussie !")
            print(f"Token: {token[:50]}...")
            
            # Tester le token avec l'endpoint protégé
            headers = {"Authorization": f"Bearer {token}"}
            
            print("\n🔍 Test de l'endpoint de génération d'évaluation...")
            test_response = requests.post(
                "http://localhost:8000/api/v1/ai-formative-evaluations/generate-evaluation/",
                headers=headers,
                json={
                    "title": "Test d'évaluation",
                    "subject": "Mathématiques",
                    "assessment_type": "project",
                    "description": "Test de génération d'évaluation formative",
                    "target_level": "intermediate",
                    "duration_minutes": 60,
                    "max_students": 30,
                    "learning_objectives": ["Compétence 1", "Compétence 2"],
                    "custom_requirements": "Aucune"
                }
            )
            
            print(f"Status: {test_response.status_code}")
            
            if test_response.status_code == 200:
                print("✅ L'endpoint protégé fonctionne avec le token de connexion !")
                print("🎯 L'API est maintenant prête à être utilisée !")
            else:
                print(f"❌ L'endpoint protégé ne fonctionne pas: {test_response.text}")
                
        else:
            print(f"❌ Échec de la connexion: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur lors du test de connexion: {e}")

if __name__ == "__main__":
    print("🔐 Test de connexion pour l'utilisateur de test")
    print("=" * 60)
    
    test_user_login()
    
    print("\n✅ Test terminé") 