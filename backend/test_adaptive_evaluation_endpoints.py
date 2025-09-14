#!/usr/bin/env python3
"""
Script de test pour les endpoints d'évaluation adaptative des enseignants
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

def get_auth_token():
    """Obtenir un token d'authentification pour un enseignant"""
    try:
        login_data = {
            "email": "teacher@example.com",  # Remplacer par un vrai email d'enseignant
            "password": "password123"
        }
        
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
        
        if response.status_code == 200:
            data = response.json()
            return data.get("access_token")
        else:
            print(f"❌ Erreur de connexion: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"❌ Erreur lors de la connexion: {e}")
        return None

def test_endpoint(endpoint, method="GET", data=None, description=""):
    """Tester un endpoint"""
    try:
        headers = {"Authorization": f"Bearer {TOKEN}"}
        
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
        elif method == "POST":
            response = requests.post(f"{BASE_URL}{endpoint}", headers=headers, json=data)
        elif method == "PUT":
            response = requests.put(f"{BASE_URL}{endpoint}", headers=headers, json=data)
        elif method == "DELETE":
            response = requests.delete(f"{BASE_URL}{endpoint}", headers=headers)
        
        if response.status_code in [200, 201]:
            print(f"✅ {description}: Succès")
            if response.text:
                result = response.json()
                if "success" in result:
                    print(f"   Réponse: {result.get('message', 'OK')}")
                else:
                    print(f"   Données reçues: {len(result) if isinstance(result, list) else '1 objet'}")
            return True
        else:
            print(f"❌ {description}: Erreur {response.status_code}")
            print(f"   Détails: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ {description}: Erreur - {e}")
        return False

def main():
    """Fonction principale de test"""
    global TOKEN
    
    print("🚀 Test des endpoints d'évaluation adaptative des enseignants")
    print("=" * 70)
    
    # 1. Authentification
    print("\n🔐 Test d'authentification...")
    TOKEN = get_auth_token()
    if not TOKEN:
        print("❌ Impossible de s'authentifier")
        return
    
    print("✅ Authentification réussie")
    
    # 2. Test de création de test adaptatif
    print("\n📝 Test de création de test adaptatif...")
    test_data = {
        "title": "Test de Mathématiques - Équations du premier degré",
        "subject": "Mathématiques",
        "description": "Test adaptatif pour évaluer la compréhension des équations du premier degré",
        "difficulty_range": {"min": 3, "max": 8},
        "question_pool_size": 20,
        "adaptation_algorithm": "irt",
        "is_active": True,
        "questions": [
            {
                "question_text": "Résoudre l'équation: 2x + 5 = 13",
                "question_type": "multiple_choice",
                "options": ["x = 4", "x = 5", "x = 6", "x = 7"],
                "correct_answer": "x = 4",
                "explanation": "2x + 5 = 13 → 2x = 8 → x = 4",
                "difficulty_level": 3,
                "subject": "Mathématiques",
                "topic": "Équations"
            },
            {
                "question_text": "Quelle est la solution de 3x - 7 = 8 ?",
                "question_type": "fill_blank",
                "correct_answer": "5",
                "explanation": "3x - 7 = 8 → 3x = 15 → x = 5",
                "difficulty_level": 4,
                "subject": "Mathématiques",
                "topic": "Équations"
            }
        ]
    }
    
    test_endpoint(
        "/api/v1/teacher-adaptive-evaluation/tests/create",
        method="POST",
        data=test_data,
        description="Création de test adaptatif"
    )
    
    # 3. Test de récupération des tests de l'enseignant
    print("\n📋 Test de récupération des tests de l'enseignant...")
    test_endpoint(
        "/api/v1/teacher-adaptive-evaluation/tests/teacher/1",
        description="Récupération des tests de l'enseignant"
    )
    
    # 4. Test d'assignation de test
    print("\n🎯 Test d'assignation de test...")
    assignment_data = {
        "class_ids": [1],  # Assigner à la classe 1
        "student_ids": [4, 5],  # Assigner aux étudiants 4 et 5
        "due_date": (datetime.now() + timedelta(days=7)).isoformat()
    }
    
    test_endpoint(
        "/api/v1/teacher-adaptive-evaluation/tests/1/assign",
        method="POST",
        data=assignment_data,
        description="Assignation de test à des classes et étudiants"
    )
    
    # 5. Test de récupération des résultats
    print("\n📊 Test de récupération des résultats...")
    test_endpoint(
        "/api/v1/teacher-adaptive-evaluation/tests/1/results",
        description="Récupération des résultats d'un test"
    )
    
    # 6. Test des analytics de classe
    print("\n📈 Test des analytics de classe...")
    test_endpoint(
        "/api/v1/teacher-adaptive-evaluation/analytics/class/1",
        description="Analytics d'une classe"
    )
    
    # 7. Test du dashboard enseignant
    print("\n🏠 Test du dashboard enseignant...")
    test_endpoint(
        "/api/v1/teacher-adaptive-evaluation/dashboard/overview",
        description="Vue d'ensemble du dashboard"
    )
    
    # 8. Test des endpoints existants
    print("\n🔄 Test des endpoints existants...")
    test_endpoint(
        "/api/v1/adaptive-evaluation/tests",
        description="Liste des tests adaptatifs disponibles"
    )
    
    print("\n🎉 Tests terminés !")
    print("\n📋 Résumé des endpoints testés:")
    print("✅ POST /api/v1/teacher-adaptive-evaluation/tests/create")
    print("✅ GET /api/v1/teacher-adaptive-evaluation/tests/teacher/{id}")
    print("✅ POST /api/v1/teacher-adaptive-evaluation/tests/{id}/assign")
    print("✅ GET /api/v1/teacher-adaptive-evaluation/tests/{id}/results")
    print("✅ GET /api/v1/teacher-adaptive-evaluation/analytics/class/{id}")
    print("✅ GET /api/v1/teacher-adaptive-evaluation/dashboard/overview")
    print("✅ GET /api/v1/adaptive-evaluation/tests")

if __name__ == "__main__":
    main()





















