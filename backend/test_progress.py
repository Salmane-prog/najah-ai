#!/usr/bin/env python3
"""
Script de test pour l'endpoint de suivi des progrès
"""

import requests
import json

def test_progress_endpoint():
    """Tester l'endpoint de suivi des progrès"""
    
    base_url = "http://localhost:8000"
    endpoint = "/api/v1/progress/student/30/metrics"
    
    print(f"🧪 Test de l'endpoint: {base_url}{endpoint}")
    
    try:
        # Test sans token (devrait retourner 401)
        response = requests.get(f"{base_url}{endpoint}")
        print(f"📊 Sans token: {response.status_code}")
        
        if response.status_code == 404:
            print("❌ Endpoint non trouvé - Vérifiez que le router est bien chargé")
        elif response.status_code == 401:
            print("✅ Endpoint trouvé mais authentification requise")
        else:
            print(f"📊 Réponse inattendue: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter au backend - Vérifiez qu'il est démarré")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_progress_endpoint()











