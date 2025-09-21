#!/usr/bin/env python3
"""
Script pour vérifier le statut du serveur backend
"""

import requests
import time

def check_backend_status():
    """Vérifier si le serveur backend est accessible"""
    print("🔍 Vérification du statut du serveur backend")
    print("=" * 50)
    
    # Test de base
    print("\n1️⃣ Test de base...")
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Serveur accessible")
            print(f"Réponse: {response.json()}")
        else:
            print(f"⚠️ Serveur accessible mais status inattendu: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Serveur non accessible - Connexion refusée")
        print("💡 Vérifiez que le serveur backend est démarré sur le port 8000")
        return False
    except requests.exceptions.Timeout:
        print("❌ Serveur non accessible - Timeout")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False
    
    # Test de la documentation
    print("\n2️⃣ Test de la documentation...")
    try:
        response = requests.get("http://localhost:8000/docs", timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Documentation accessible")
        else:
            print(f"⚠️ Documentation non accessible: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur documentation: {e}")
    
    # Test des endpoints principaux
    print("\n3️⃣ Test des endpoints principaux...")
    endpoints = [
        "/api/v1/teacher-dashboard/",
        "/api/v1/reports/teacher",
        "/api/v1/student_analytics/student/1"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"http://localhost:8000{endpoint}", timeout=5)
            print(f"{endpoint}: {response.status_code}")
        except Exception as e:
            print(f"{endpoint}: ❌ Erreur - {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Vérification terminée")
    return True

if __name__ == "__main__":
    check_backend_status()









