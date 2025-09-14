#!/usr/bin/env python3
"""
Script simple pour tester l'API OpenAI.
"""
import requests
import json

def test_openai_status():
    """Test du statut de l'API OpenAI."""
    print("🧪 Test du statut OpenAI...")
    try:
        response = requests.get("http://localhost:8000/api/v1/ai-openai/status")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ Succès!")
            print(f"Status: {data.get('status')}")
            print(f"Stats: {data.get('stats')}")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

def test_openai_with_auth():
    """Test avec authentification."""
    print("\n🔐 Test avec authentification...")
    
    # Login
    login_data = {
        "email": "marie.dubois@najah.ai",
        "password": "salmane123@"
    }
    
    try:
        # Essayer de se connecter
        response = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            json=login_data
        )
        print(f"Status login: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            token = token_data["access_token"]
            print(f"✅ Token obtenu: {token[:20]}...")
            
            # Test de génération de quiz
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            quiz_data = {
                "topic": "Mathématiques",
                "difficulty": "medium",
                "student_level": "intermediate"
            }
            
            response = requests.post(
                "http://localhost:8000/api/v1/ai-openai/generate-quiz",
                json=quiz_data,
                headers=headers
            )
            
            print(f"Status génération quiz: {response.status_code}")
            if response.status_code == 200:
                quiz_result = response.json()
                print("✅ Quiz généré avec succès!")
                print(f"Question: {quiz_result['question']['question']}")
                print(f"Options: {quiz_result['question']['options']}")
                print(f"Réponse correcte: {quiz_result['question']['correct_answer']}")
            else:
                print(f"❌ Erreur génération: {response.text}")
        else:
            print(f"❌ Échec de connexion: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

def test_openai_direct():
    """Test direct du service OpenAI."""
    print("\n🤖 Test direct du service OpenAI...")
    try:
        from services.openai_service import OpenAIService
        
        service = OpenAIService()
        print("✅ Service OpenAI initialisé")
        
        # Test de génération de quiz
        quiz = service.generate_quiz_question(
            topic="Mathématiques",
            difficulty="medium",
            student_level="intermediate"
        )
        
        print("✅ Quiz généré directement!")
        print(f"Question: {quiz['question']}")
        print(f"Options: {quiz['options']}")
        print(f"Réponse correcte: {quiz['correct_answer']}")
        print(f"Explication: {quiz['explanation']}")
        
    except Exception as e:
        print(f"❌ Erreur service direct: {str(e)}")

if __name__ == "__main__":
    print("🚀 Test de l'intégration OpenAI")
    print("=" * 50)
    
    test_openai_status()
    test_openai_direct()
    test_openai_with_auth()
    
    print("\n✅ Tests terminés!") 