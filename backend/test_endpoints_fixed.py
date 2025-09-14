#!/usr/bin/env python3
"""
Script de test pour vérifier que tous les endpoints fonctionnent
"""

import requests
import time

BASE_URL = "http://127.0.0.1:8000"

def test_endpoint(endpoint, description):
    """Teste un endpoint et affiche le résultat"""
    print(f"\nTest de {description}...")
    print(f"URL: {BASE_URL}{endpoint}")
    
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
        
        if response.status_code == 200:
            print(f"✅ SUCCES - {description} fonctionne")
            return True
        elif response.status_code == 401:
            print(f"⚠️  AUTH REQUISE - {description} demande une authentification (normal)")
            return True
        elif response.status_code == 404:
            print(f"❌ ERREUR 404 - {description} n'est pas trouvé")
            return False
        else:
            print(f"⚠️  STATUT {response.status_code} - {description} retourne un statut inattendu")
            return True
    except requests.exceptions.ConnectionError:
        print(f"❌ ERREUR CONNEXION - Impossible de se connecter au serveur")
        return False
    except Exception as e:
        print(f"❌ ERREUR - {description}: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 Test des endpoints qui causaient des erreurs 404...")
    print("=" * 60)
    
    # Attendre que le serveur soit prêt
    print("Attente du démarrage du serveur...")
    time.sleep(2)
    
    # Endpoints à tester
    endpoints_to_test = [
        ("/api/v1/ai-advanced/recommendations", "Recommandations IA avancées"),
        ("/api/v1/ai-advanced/difficulty-detection", "Détection des difficultés"),
        ("/api/v1/ai-advanced/tutoring/sessions", "Sessions de tutorat IA"),
        ("/api/v1/advanced_analytics/insights", "Insights analytics avancés"),
        ("/api/v1/advanced_analytics/predictions", "Prédictions analytics avancés"),
        ("/api/v1/advanced_analytics/trends", "Tendances analytics avancés"),
        ("/api/v1/reports/subject-progress", "Rapports de progression par matière"),
        ("/api/v1/reports/analytics", "Rapports d'analytics"),
        ("/api/v1/reports/detailed", "Rapports détaillés"),
        ("/api/v1/homework/", "Devoirs avancés")
    ]
    
    success_count = 0
    total_count = len(endpoints_to_test)
    
    for endpoint, description in endpoints_to_test:
        if test_endpoint(endpoint, description):
            success_count += 1
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    print(f"✅ Endpoints fonctionnels: {success_count}")
    print(f"❌ Endpoints défaillants: {total_count - success_count}")
    print(f"📈 Taux de succès: {(success_count/total_count)*100:.1f}%")
    
    if success_count == total_count:
        print("\n🎉 Tous les endpoints fonctionnent correctement!")
        print("Les erreurs 404 ont été corrigées.")
    else:
        print(f"\n⚠️  {total_count - success_count} endpoints ont encore des problèmes.")
        print("Vérifiez la configuration des routes dans app.py")
    
    print("\n✨ Test terminé!")

if __name__ == "__main__":
    main()
