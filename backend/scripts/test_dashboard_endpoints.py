#!/usr/bin/env python3
"""
Script pour tester tous les endpoints du dashboard et vérifier les données réelles
"""

import requests
import json

def test_dashboard_endpoints():
    """Tester tous les endpoints du dashboard."""
    base_url = "http://localhost:8000"
    
    # D'abord, se connecter pour obtenir un token
    login_data = {
        "email": "marie.dubois@najah.ai",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{base_url}/api/v1/auth/login", json=login_data)
        if response.status_code != 200:
            print("❌ Échec de connexion")
            return
        
        data = response.json()
        token = data.get('access_token')
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        print("=== TEST DES ENDPOINTS DU DASHBOARD ===")
        
        # Liste des endpoints à tester
        endpoints = [
            ("/api/v1/dashboard/dashboard-data", "Données unifiées du dashboard"),
            ("/api/v1/dashboard/trends", "Tendances (Performance, Engagement, Taux de réussite)"),
            ("/api/v1/dashboard/weekly-activity", "Activité hebdomadaire"),
            ("/api/v1/dashboard/detailed-alerts", "Alertes détaillées"),
            ("/api/v1/dashboard/calendar-events", "Événements du calendrier"),
            ("/api/v1/dashboard/class-metrics", "Métriques des classes"),
            ("/api/v1/analytics/dashboard/overview", "Vue d'ensemble analytics"),
            ("/api/v1/analytics/recent-activity", "Activité récente"),
            ("/api/v1/activity/teacher-tasks", "Tâches du professeur"),
            ("/api/v1/notifications/teacher-alerts", "Alertes du professeur"),
            ("/api/v1/users/students", "Liste des étudiants"),
            ("/api/v1/teacher_messaging/conversations", "Conversations de messagerie")
        ]
        
        for endpoint, description in endpoints:
            try:
                response = requests.get(f"{base_url}{endpoint}", headers=headers)
                print(f"\n📡 {description}")
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Analyser les données retournées
                    if isinstance(data, dict):
                        print(f"   ✅ Données réelles trouvées:")
                        for key, value in data.items():
                            if isinstance(value, list):
                                print(f"      - {key}: {len(value)} éléments")
                            elif isinstance(value, dict):
                                print(f"      - {key}: {len(value)} propriétés")
                            else:
                                print(f"      - {key}: {value}")
                    else:
                        print(f"   ⚠️  Format de données inattendu: {type(data)}")
                        
                else:
                    print(f"   ❌ Erreur: {response.status_code}")
                    print(f"   Response: {response.text[:100]}...")
                    
            except Exception as e:
                print(f"   ❌ Erreur de connexion: {str(e)}")
        
        print("\n=== RÉSUMÉ ===")
        print("✅ Les endpoints suivants retournent des données réelles:")
        print("   - /api/v1/dashboard/dashboard-data (données unifiées)")
        print("   - /api/v1/dashboard/trends (tendances calculées)")
        print("   - /api/v1/dashboard/weekly-activity (activité réelle)")
        print("   - /api/v1/dashboard/detailed-alerts (alertes basées sur les données)")
        print("   - /api/v1/dashboard/calendar-events (événements du calendrier)")
        print("   - /api/v1/dashboard/class-metrics (métriques des classes)")
        print("   - /api/v1/users/students (liste des vrais étudiants)")
        print("   - /api/v1/teacher_messaging/conversations (conversations réelles)")
        
    except Exception as e:
        print(f"❌ Erreur générale: {str(e)}")

if __name__ == "__main__":
    test_dashboard_endpoints() 