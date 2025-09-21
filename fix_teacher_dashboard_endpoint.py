#!/usr/bin/env python3
"""
Script pour diagnostiquer et corriger le problème de l'endpoint teacher-dashboard
"""

import requests
import json

def diagnose_teacher_dashboard():
    """Diagnostiquer le problème de l'endpoint teacher-dashboard"""
    print("🔍 Diagnostic de l'endpoint teacher-dashboard")
    print("=" * 60)
    
    BASE_URL = "http://localhost:8000"
    
    # 1. Test de base du serveur
    print("\n1️⃣ Test de base du serveur...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ Serveur accessible")
        else:
            print(f"❌ Serveur accessible mais status inattendu: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Serveur non accessible: {e}")
        return False
    
    # 2. Test de l'endpoint principal teacher-dashboard
    print("\n2️⃣ Test de l'endpoint principal /api/v1/teacher-dashboard/...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/teacher-dashboard/", timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Endpoint principal accessible")
        else:
            print(f"❌ Endpoint principal non accessible: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # 3. Test de l'endpoint students
    print("\n3️⃣ Test de l'endpoint /api/v1/teacher-dashboard/students...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/teacher-dashboard/students", timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Endpoint students accessible")
        elif response.status_code == 401:
            print("⚠️ Endpoint accessible mais authentification requise")
        elif response.status_code == 404:
            print("❌ Endpoint students non trouvé (404)")
            print("💡 Problème de routage détecté")
        else:
            print(f"❌ Endpoint accessible mais status inattendu: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # 4. Test de l'endpoint analytics
    print("\n4️⃣ Test de l'endpoint /api/v1/teacher-dashboard/analytics...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/teacher-dashboard/analytics", timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Endpoint analytics accessible")
        elif response.status_code == 401:
            print("⚠️ Endpoint accessible mais authentification requise")
        elif response.status_code == 404:
            print("❌ Endpoint analytics non trouvé (404)")
        else:
            print(f"❌ Endpoint accessible mais status inattendu: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # 5. Test avec authentification (si possible)
    print("\n5️⃣ Test avec authentification...")
    try:
        # Essayer de se connecter avec un compte professeur
        login_response = requests.post(f"{BASE_URL}/api/v1/auth/login", json={
            "email": "marizee.dubois@najah.ai",
            "password": "password123"
        }, timeout=5)
        
        if login_response.status_code == 200:
            token = login_response.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}
            
            print("✅ Connexion réussie, test avec token...")
            
            # Test de l'endpoint students avec authentification
            response = requests.get(f"{BASE_URL}/api/v1/teacher-dashboard/students", headers=headers, timeout=10)
            print(f"Status avec auth: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Succès - {data.get('total_count', 0)} étudiants trouvés")
            elif response.status_code == 404:
                print("❌ Endpoint toujours 404 même avec authentification")
                print("💡 Problème de routage confirmé")
            else:
                print(f"⚠️ Status inattendu avec auth: {response.status_code}")
                print(f"Réponse: {response.text}")
        else:
            print(f"❌ Échec de connexion: {login_response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur lors du test d'authentification: {e}")
    
    print("\n" + "=" * 60)
    print("🏁 Diagnostic terminé")
    
    # Recommandations
    print("\n💡 Recommandations:")
    if response.status_code == 404:
        print("1. Vérifier la configuration des routes dans app.py")
        print("2. Vérifier que le serveur a redémarré après les modifications")
        print("3. Vérifier les logs du serveur pour plus de détails")
    else:
        print("1. L'endpoint semble fonctionner")
        print("2. Vérifier l'authentification et les permissions")
    
    return True

if __name__ == "__main__":
    diagnose_teacher_dashboard()









