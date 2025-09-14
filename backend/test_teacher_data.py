#!/usr/bin/env python3
"""
Script de test pour vérifier les endpoints des classes et étudiants de l'enseignant
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

def get_auth_token():
    """Obtenir un token d'authentification"""
    try:
        login_data = {
            "email": "marizee.dubois@najah.ai",
            "password": "password123"
        }
        
        response = requests.post(f"{API_BASE}/auth/login", json=login_data)
        
        if response.status_code == 200:
            data = response.json()
            return data.get("access_token")
        else:
            print(f"❌ Erreur de connexion: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Erreur lors de la connexion: {e}")
        return None

def test_teacher_classes(token):
    """Tester l'endpoint des classes de l'enseignant"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        print("🔄 Test de l'endpoint des classes...")
        response = requests.get(f"{API_BASE}/teacher/classes/", headers=headers)
        
        if response.status_code == 200:
            classes = response.json()
            print(f"✅ Classes récupérées: {len(classes)}")
            for cls in classes[:3]:  # Afficher les 3 premières
                print(f"  - {cls.get('name', 'N/A')} ({cls.get('student_count', 0)} étudiants)")
            return True
        else:
            print(f"❌ Erreur: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test des classes: {e}")
        return False

def test_teacher_targets(token):
    """Tester l'endpoint des cibles de l'enseignant"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        print("🔄 Test de l'endpoint des cibles...")
        response = requests.get(f"{API_BASE}/assignments/teacher/targets", headers=headers)
        
        if response.status_code == 200:
            targets = response.json()
            print(f"✅ Cibles récupérées:")
            print(f"  - Classes: {len(targets.get('classes', []))}")
            print(f"  - Étudiants: {len(targets.get('students', []))}")
            print(f"  - Total étudiants: {targets.get('total_students', 0)}")
            
            # Afficher quelques exemples
            if targets.get('classes'):
                print("  Classes:")
                for cls in targets['classes'][:2]:
                    print(f"    - {cls.get('name', 'N/A')} ({cls.get('student_count', 0)} étudiants)")
            
            if targets.get('students'):
                print("  Étudiants:")
                for student in targets['students'][:3]:
                    print(f"    - {student.get('name', 'N/A')} ({student.get('email', 'N/A')}) - {student.get('class_name', 'N/A')}")
            
            return True
        else:
            print(f"❌ Erreur: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test des cibles: {e}")
        return False

def main():
    """Fonction principale"""
    print("🧪 Test des endpoints des classes et étudiants de l'enseignant")
    print("=" * 60)
    
    # Obtenir le token
    token = get_auth_token()
    if not token:
        print("❌ Impossible d'obtenir le token d'authentification")
        return
    
    print("✅ Token obtenu avec succès")
    print()
    
    # Tester les endpoints
    success = True
    
    if not test_teacher_classes(token):
        success = False
    
    print()
    
    if not test_teacher_targets(token):
        success = False
    
    print()
    
    if success:
        print("🎉 Tous les tests ont réussi !")
    else:
        print("❌ Certains tests ont échoué")

if __name__ == "__main__":
    main()


















