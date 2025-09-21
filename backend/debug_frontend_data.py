#!/usr/bin/env python3
"""
Script pour déboguer les données envoyées par le frontend
"""

import requests
import json

def debug_frontend_request():
    """Débogue une requête du frontend pour voir les données exactes"""
    
    print("🔍 Débogage des données envoyées par le frontend")
    print("=" * 70)
    
    # ÉTAPE 1 : Connexion
    print("\n🔐 ÉTAPE 1 : Connexion...")
    
    login_data = {
        "email": "marizee.dubois@najah.ai",
        "password": "password123"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            json=login_data
        )
        
        if response.status_code != 200:
            print(f"❌ Échec de la connexion: {response.text}")
            return None
        
        data = response.json()
        token = data.get("access_token")
        print(f"✅ Connexion réussie ! Token: {token[:50]}...")
        
        # ÉTAPE 2 : Test avec des données minimales (comme le frontend pourrait envoyer)
        print("\n🔍 ÉTAPE 2 : Test avec données minimales...")
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # Données minimales que le frontend pourrait envoyer
        minimal_data = {
            "title": "Test Frontend - Évaluation Formative",
            "subject": "Mathématiques",
            "description": "Test avec données minimales",
            "assessment_type": "project",
            "target_level": "intermediate",
            "duration_minutes": 60,
            "max_students": 30,
            "learning_objectives": ["Compétence 1"]
        }
        
        print(f"📊 Données minimales envoyées: {json.dumps(minimal_data, indent=2)}")
        
        save_response = requests.post(
            "http://localhost:8000/api/v1/formative-evaluations/",
            headers=headers,
            json=minimal_data
        )
        
        print(f"\n📊 Réponse avec données minimales:")
        print(f"   Status: {save_response.status_code}")
        print(f"   Body: {save_response.text}")
        
        if save_response.status_code == 200:
            print(f"\n✅ SUCCÈS avec données minimales !")
            return True
        else:
            print(f"\n❌ ÉCHEC avec données minimales")
            print(f"   Erreur: {save_response.text}")
            
            # ÉTAPE 3 : Test avec données encore plus minimales
            print(f"\n🔍 ÉTAPE 3 : Test avec données ultra-minimales...")
            
            ultra_minimal = {
                "title": "Test Ultra-Minimal",
                "subject": "Mathématiques",
                "description": "Test ultra-minimal",
                "assessment_type": "project",
                "target_level": "intermediate",
                "duration_minutes": 60,
                "max_students": 30,
                "learning_objectives": ["Compétence 1"]
            }
            
            print(f"📊 Données ultra-minimales: {json.dumps(ultra_minimal, indent=2)}")
            
            ultra_response = requests.post(
                "http://localhost:8000/api/v1/formative-evaluations/",
                headers=headers,
                json=ultra_minimal
            )
            
            print(f"\n📊 Réponse ultra-minimale:")
            print(f"   Status: {ultra_response.status_code}")
            print(f"   Body: {ultra_response.text}")
            
            return False
            
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Débogage des données frontend")
    print("=" * 80)
    
    success = debug_frontend_request()
    
    if success:
        print(f"\n✅ Le problème n'est pas les données minimales")
        print(f"🔍 Vérifiez la structure exacte envoyée par le frontend")
    else:
        print(f"\n❌ Le problème est dans la validation des données")
        print(f"🔍 Vérifiez le modèle Pydantic FormativeEvaluationCreate")


















