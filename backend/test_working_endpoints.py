#!/usr/bin/env python3
"""
Script pour tester les endpoints qui fonctionnent
et vérifier qu'ils retournent des données
"""

import requests
import json
import os

def test_french_optimized_endpoints():
    """Tester les endpoints french-optimized"""
    
    base_url = "http://localhost:8000"
    student_id = 30
    
    print("🔍 TEST DES ENDPOINTS FRENCH-OPTIMIZED")
    print("=" * 50)
    
    # 1. Tester /api/v1/french-optimized/student/start
    print("\n1. 🚀 Test POST /api/v1/french-optimized/student/start")
    try:
        response = requests.post(
            f"{base_url}/api/v1/french-optimized/student/start",
            json={"student_id": student_id},
            headers={"Content-Type": "application/json"}
        )
        
        print(f"   Status: {response.status_code}")
        if response.ok:
            data = response.json()
            print(f"   ✅ Succès! Données reçues: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"   ❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"   💥 Exception: {e}")
    
    # 2. Tester /api/v1/french-optimized/student/{id}/profile
    print("\n2. 👤 Test GET /api/v1/french-optimized/student/{id}/profile")
    try:
        response = requests.get(
            f"{base_url}/api/v1/french-optimized/student/{student_id}/profile",
            headers={"Content-Type": "application/json"}
        )
        
        print(f"   Status: {response.status_code}")
        if response.ok:
            data = response.json()
            print(f"   ✅ Succès! Profil reçu: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"   ❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"   💥 Exception: {e}")

def test_student_learning_paths_endpoints():
    """Tester les endpoints student_learning_paths"""
    
    base_url = "http://localhost:8000"
    student_id = 30
    
    print("\n🔍 TEST DES ENDPOINTS STUDENT_LEARNING_PATHS")
    print("=" * 50)
    
    # 1. Tester /api/v1/student_learning_paths/student/{id}
    print("\n1. 🗺️ Test GET /api/v1/student_learning_paths/student/{id}")
    try:
        response = requests.get(
            f"{base_url}/api/v1/student_learning_paths/student/{student_id}",
            headers={"Content-Type": "application/json"}
        )
        
        print(f"   Status: {response.status_code}")
        if response.ok:
            data = response.json()
            print(f"   ✅ Succès! Parcours reçus: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"   ❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"   💥 Exception: {e}")

def test_old_endpoints_for_comparison():
    """Tester les anciens endpoints pour comparaison"""
    
    base_url = "http://localhost:8000"
    student_id = 30
    
    print("\n🔍 TEST DES ANCIENS ENDPOINTS (POUR COMPARAISON)")
    print("=" * 50)
    
    # 1. Tester /api/v1/assessments/student/{id}/pending
    print("\n1. 📝 Test GET /api/v1/assessments/student/{id}/pending")
    try:
        response = requests.get(
            f"{base_url}/api/v1/assessments/student/{student_id}/pending",
            headers={"Content-Type": "application/json"}
        )
        
        print(f"   Status: {response.status_code}")
        if response.ok:
            data = response.json()
            print(f"   ✅ Succès! Données reçues: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"   ❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"   💥 Exception: {e}")
    
    # 2. Tester /api/v1/learning_paths/student/{id}/active
    print("\n2. 🗺️ Test GET /api/v1/learning_paths/student/{id}/active")
    try:
        response = requests.get(
            f"{base_url}/api/v1/learning_paths/student/{student_id}/active",
            headers={"Content-Type": "application/json"}
        )
        
        print(f"   Status: {response.status_code}")
        if response.ok:
            data = response.json()
            print(f"   ✅ Succès! Données reçues: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"   ❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"   💥 Exception: {e}")

if __name__ == "__main__":
    print("🚀 TEST DES ENDPOINTS QUI FONCTIONNENT")
    print("=" * 60)
    print("📍 Base URL: http://localhost:8000")
    print("👤 Student ID: 30")
    print()
    
    test_french_optimized_endpoints()
    test_student_learning_paths_endpoints()
    test_old_endpoints_for_comparison()
    
    print("\n🎯 RÉSUMÉ DES TESTS")
    print("=" * 30)
    print("✅ Endpoints qui fonctionnent → À utiliser dans les widgets")
    print("❌ Endpoints qui ne fonctionnent pas → À remplacer")
    print("🔄 Maintenant, modifions les widgets !")
