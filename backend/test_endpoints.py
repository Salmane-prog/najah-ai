#!/usr/bin/env python3
"""
Script simple pour tester nos endpoints
"""

import requests
import json

def test_endpoint(url, description):
    """Tester un endpoint"""
    print(f"\n🔍 Test: {description}")
    print(f"   URL: {url}")
    
    try:
        response = requests.get(url)
        print(f"   Status: {response.status_code}")
        
        if response.ok:
            data = response.json()
            print(f"   ✅ Succès!")
            print(f"   📊 Données reçues: {json.dumps(data, indent=2, ensure_ascii=False)}")
            return True
        else:
            print(f"   ❌ Erreur: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return False

def main():
    print("🧪 TEST DES ENDPOINTS")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # Tester tous nos endpoints (sans auth pour le moment)
    results = []
    
    results.append(test_endpoint(
        f"{base_url}/api/v1/cognitive_diagnostic/student/5/cognitive-profile-test",
        "Profil cognitif étudiant ID 5"
    ))
    
    results.append(test_endpoint(
        f"{base_url}/api/v1/french/initial-assessment/student/5/profile-test",
        "Profil d'apprentissage français étudiant ID 5 (TEST)"
    ))
    
    results.append(test_endpoint(
        f"{base_url}/api/v1/french/recommendations/student/5/test",
        "Recommandations françaises étudiant ID 5 (TEST)"
    ))
    
    # Résumé
    print("\n" + "=" * 50)
    successful = sum(results)
    total = len(results)
    print(f"📊 Résultats: {successful}/{total} tests réussis")
    
    if successful == total:
        print("🎉 Tous les endpoints fonctionnent!")
        print("👉 Votre page affichera maintenant des données réelles!")
    else:
        print("⚠️  Certains endpoints ont des problèmes")
        print("💡 Vérifiez les logs du serveur pour plus de détails")

if __name__ == "__main__":
    main()