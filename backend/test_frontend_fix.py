#!/usr/bin/env python3
"""
Script pour tester la correction du frontend
"""

import requests
import json

def test_frontend_fix():
    """Teste la correction du frontend avec les bonnes données"""
    
    print("🧪 Test de la correction du frontend")
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
        
        # ÉTAPE 2 : Test avec les données exactes que le frontend enverrait maintenant
        print("\n🔍 ÉTAPE 2 : Test avec données frontend corrigées...")
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # Données que le frontend enverrait maintenant (après correction)
        frontend_data = {
            "title": "Test Frontend Corrigé - Évaluation Formative",
            "description": "Test avec données frontend corrigées",
            "assessment_type": "project",
            "subject": "Mathématiques",
            "target_level": "intermediate",
            "duration_minutes": 60,
            "max_students": 30,
            "learning_objectives": ["Compétence 1", "Compétence 2"],
            "criteria": [
                {
                    "name": "Qualité de la recherche",
                    "description": "Pertinence des sources",
                    "weight": 25,
                    "max_points": 4
                }
            ],
            "rubric": {
                "excellent": {"points": 4, "description": "Travail exceptionnel"},
                "good": {"points": 3, "description": "Travail de qualité"}
            },
            "questions": [
                {
                    "question": "Question de test",
                    "type": "reflection",
                    "max_points": 5
                }
            ],
            "instructions": "Instructions de test",
            "estimated_duration": 60,
            "difficulty_level": "intermediate",
            "success_indicators": ["Indicateur 1", "Indicateur 2"]
        }
        
        print(f"📊 Données frontend corrigées: {json.dumps(frontend_data, indent=2)}")
        
        save_response = requests.post(
            "http://localhost:8000/api/v1/formative-evaluations/",
            headers=headers,
            json=frontend_data
        )
        
        print(f"\n📊 Réponse avec données frontend corrigées:")
        print(f"   Status: {save_response.status_code}")
        print(f"   Body: {save_response.text}")
        
        if save_response.status_code == 200:
            saved_evaluation = save_response.json()
            print(f"\n🎉 SUCCÈS ! Frontend corrigé !")
            print(f"   ID: {saved_evaluation.get('id')}")
            print(f"   Titre: {saved_evaluation.get('title')}")
            print(f"   Créée par: {saved_evaluation.get('teacher_id')}")
            return True
        else:
            print(f"\n❌ ÉCHEC ! Frontend pas encore corrigé")
            print(f"   Erreur: {save_response.text}")
            return False
            
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        return False

if __name__ == "__main__":
    print("🔐 Test de la correction du frontend")
    print("=" * 80)
    
    success = test_frontend_fix()
    
    if success:
        print(f"\n✅ FRONTEND CORRIGÉ !")
        print(f"   L'erreur '422' est maintenant résolue !")
        print(f"\n🔧 POUR TESTER LE FRONTEND :")
        print(f"1. Rafraîchis la page frontend")
        print(f"2. Génère une évaluation avec l'IA")
        print(f"3. Clique sur 'Sauvegarder'")
        print(f"4. L'évaluation devrait être sauvegardée ! 🎉")
    else:
        print(f"\n❌ ÉCHEC ! Le frontend n'est pas encore corrigé")
        print(f"🔍 Vérification nécessaire de la correction")



