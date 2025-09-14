#!/usr/bin/env python3
"""
Script pour tester la connexion à l'API de messagerie
"""

import requests
import json

def test_api_connection():
    """Tester la connexion à l'API."""
    base_url = "http://localhost:8000"
    
    print("=== TEST DE CONNEXION API ===")
    
    # Test 1: Vérifier si le serveur répond
    try:
        response = requests.get(f"{base_url}/docs")
        print(f"✅ Serveur accessible: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Serveur non accessible - Vérifiez que le backend est démarré")
        return
    except Exception as e:
        print(f"❌ Erreur de connexion: {str(e)}")
        return
    
    # Test 2: Vérifier l'endpoint de messagerie (sans auth)
    try:
        response = requests.get(f"{base_url}/api/v1/teacher_messaging/conversations")
        print(f"📡 Endpoint messagerie: {response.status_code}")
        if response.status_code == 401:
            print("✅ Endpoint protégé (normal)")
        else:
            print(f"⚠️  Status inattendu: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur endpoint: {str(e)}")
    
    # Test 3: Vérifier les headers CORS
    try:
        response = requests.options(f"{base_url}/api/v1/teacher_messaging/conversations")
        print(f"🌐 CORS headers: {response.status_code}")
        if 'access-control-allow-origin' in response.headers:
            print("✅ CORS configuré")
        else:
            print("⚠️  CORS non configuré")
    except Exception as e:
        print(f"❌ Erreur CORS: {str(e)}")
    
    print("\n=== RECOMMANDATIONS ===")
    print("1. Vérifiez que le backend est démarré sur le port 8000")
    print("2. Vérifiez que le frontend utilise la bonne URL d'API")
    print("3. Vérifiez que l'authentification fonctionne")
    print("4. Vérifiez les logs du navigateur pour plus de détails")

if __name__ == "__main__":
    test_api_connection() 