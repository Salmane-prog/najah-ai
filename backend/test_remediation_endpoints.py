#!/usr/bin/env python3
"""
Script de test pour les endpoints de remédiation diversifiée
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
STUDENT_ID = 30  # ID de test

def test_exercise_statistics():
    """Test de l'endpoint des statistiques d'exercices"""
    print("📊 Test des statistiques d'exercices...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/remediation/exercises/statistics")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Statistiques récupérées avec succès!")
            print(f"Total d'exercices: {data['statistics']['total_exercises']}")
            print(f"Catégories: {', '.join(data['statistics']['categories'])}")
            print(f"Difficultés: {', '.join(data['statistics']['difficulties'])}")
        else:
            print(f"❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")

def test_diverse_exercises():
    """Test de l'endpoint des exercices diversifiés"""
    print("\n🎯 Test des exercices diversifiés...")
    
    try:
        # Test avec différents topics
        topics = ["grammar", "conjugation", "vocabulary"]
        
        for topic in topics:
            print(f"\n--- Test avec topic: {topic} ---")
            
            response = requests.get(
                f"{BASE_URL}/api/v1/remediation/exercises/diverse",
                params={
                    "topic": topic,
                    "difficulty": "facile",
                    "count": 2,
                    "student_id": STUDENT_ID
                }
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {data['total_found']} exercices trouvés pour {topic}")
                
                for i, exercise in enumerate(data['exercises'], 1):
                    print(f"  {i}. {exercise['question'][:50]}... ({exercise['difficulty']})")
            else:
                print(f"❌ Erreur: {response.text}")
                
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")

def test_remediation_plan():
    """Test de l'endpoint du plan de remédiation"""
    print("\n📋 Test du plan de remédiation...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/remediation/student/{STUDENT_ID}/plan",
            json={"subject": "français"}
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Plan de remédiation généré avec succès!")
            print(f"Nombre d'étapes: {len(data['steps'])}")
            
            for i, step in enumerate(data['steps'], 1):
                print(f"  {i}. {step['topic']} - {step['learning_objective'][:50]}...")
        else:
            print(f"❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")

def main():
    """Fonction principale de test"""
    print("🧪 TEST DES ENDPOINTS DE REMÉDIATION DIVERSIFIÉE")
    print("=" * 60)
    
    # Vérifier que le serveur est démarré
    try:
        response = requests.get(f"{BASE_URL}/docs")
        print("✅ Serveur backend accessible")
    except:
        print("❌ Serveur backend non accessible. Démarrez-le d'abord avec:")
        print("   python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000")
        return
    
    # Tests
    test_exercise_statistics()
    test_diverse_exercises()
    test_remediation_plan()
    
    print("\n🎉 Tests terminés!")

if __name__ == "__main__":
    main()
