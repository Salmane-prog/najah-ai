#!/usr/bin/env python3
"""
Script de test pour vérifier que tous les endpoints fonctionnent correctement
"""

import requests
import json

def test_endpoints():
    base_url = "http://localhost:8000"
    
    print("🔍 TEST DES ENDPOINTS")
    print("=" * 50)
    
    # Test 1: Analytics Overview
    print("\n1. Test Analytics Overview:")
    try:
        response = requests.get(f"{base_url}/api/v1/analytics/dashboard/overview")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Classes: {data.get('classes', 0)}")
            print(f"   ✅ Étudiants: {data.get('students', 0)}")
            print(f"   ✅ Quiz: {data.get('quizzes', 0)}")
        else:
            print(f"   ❌ Erreur: {response.text}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    # Test 2: Gap Analysis Dashboard Data
    print("\n2. Test Gap Analysis Dashboard Data:")
    try:
        response = requests.get(f"{base_url}/api/v1/gap_analysis/dashboard-data")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Étudiants: {len(data.get('students', []))}")
            print(f"   ✅ Types d'analyse: {len(data.get('analysis_types', []))}")
            print(f"   ✅ Score de lacunes: {data.get('gap_score', 0)}%")
        else:
            print(f"   ❌ Erreur: {response.text}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    # Test 3: Adaptive Quizzes Dashboard Data
    print("\n3. Test Adaptive Quizzes Dashboard Data:")
    try:
        response = requests.get(f"{base_url}/api/v1/adaptive_quizzes/dashboard-data")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Étudiants: {len(data.get('students', []))}")
            print(f"   ✅ Matières: {len(data.get('subjects', []))}")
            print(f"   ✅ Niveau actuel: {data.get('current_level', 'N/A')}")
            print(f"   ✅ Quiz complétés: {data.get('completed_quizzes', 0)}")
            print(f"   ✅ Score moyen: {data.get('average_score', 0)}%")
        else:
            print(f"   ❌ Erreur: {response.text}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    # Test 4: Class Groups
    print("\n4. Test Class Groups:")
    try:
        response = requests.get(f"{base_url}/api/v1/class_groups/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Classes: {len(data)}")
            if data:
                first_class = data[0]
                print(f"   ✅ Première classe: {first_class.get('name', 'N/A')}")
        else:
            print(f"   ❌ Erreur: {response.text}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Tests terminés !")

if __name__ == "__main__":
    test_endpoints() 