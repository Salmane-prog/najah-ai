#!/usr/bin/env python3
"""
Script pour tester spécifiquement l'endpoint quizzes avec plus de détails.
"""

import requests
import json
import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_quizzes_endpoint():
    """Tester spécifiquement l'endpoint quizzes."""
    
    base_url = "http://localhost:8000"
    
    # 1. Se connecter pour obtenir un token
    print("🔐 Connexion pour obtenir un token...")
    
    login_data = {
        "email": "marie.dubois@najah.ai",
        "password": "salmane123@"
    }
    
    try:
        response = requests.post(f"{base_url}/api/v1/auth/login", json=login_data)
        print(f"Status login: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            token = token_data["access_token"]
            print(f"✅ Token obtenu: {token[:20]}...")
            
            # Headers avec token
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            print("\n🧪 Test spécifique de l'endpoint quizzes")
            print("=" * 50)
            
            # Test quizzes avec plus de détails
            print("\n🔍 Test: GET /api/v1/quizzes/")
            response = requests.get(f"{base_url}/api/v1/quizzes/", headers=headers)
            print(f"Status: {response.status_code}")
            print(f"Headers: {dict(response.headers)}")
            
            if response.status_code != 200:
                print(f"Error: {response.text}")
                try:
                    error_json = response.json()
                    print(f"Error JSON: {json.dumps(error_json, indent=2)}")
                except:
                    print("Pas de JSON dans la réponse d'erreur")
            else:
                print("✅ Succès")
                try:
                    data = response.json()
                    print(f"Nombre de quizzes: {len(data) if isinstance(data, list) else 'N/A'}")
                except:
                    print("Réponse non-JSON")
                
        else:
            print(f"❌ Échec de connexion: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    test_quizzes_endpoint() 