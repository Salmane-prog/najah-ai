import requests
import json
from datetime import datetime, timedelta

def test_organization_advanced_no_auth():
    """Test des nouvelles fonctionnalités avancées d'organisation (sans auth)"""
    
    base_url = "http://localhost:8000/organization-advanced"
    
    print("🚀 Test des fonctionnalités avancées d'organisation (sans auth)")
    print("=" * 60)
    
    # Test 1: Analytics de productivité
    print("\n📊 Test des analytics de productivité...")
    try:
        response = requests.get(f"{base_url}/analytics/productivity?days=30")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            analytics = response.json()
            print("✅ Analytics récupérés avec succès:")
            print(f"  - Temps d'étude: {analytics.get('study_time_hours', 0)}h")
            print(f"  - Productivité moyenne: {analytics.get('avg_productivity', 0)}/10")
            print(f"  - Taux de completion: {analytics.get('homework_completion_rate', 0)}%")
            print(f"  - Nombre de sessions: {analytics.get('sessions_count', 0)}")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
    
    # Test 2: Recommandations de tâches prioritaires
    print("\n🎯 Test des recommandations de tâches prioritaires...")
    try:
        response = requests.get(f"{base_url}/recommendations/priority-tasks")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            recommendations = response.json()
            print("✅ Recommandations récupérées avec succès:")
            print(f"  - Nombre de recommandations: {len(recommendations.get('recommendations', []))}")
            print(f"  - Tâches urgentes: {recommendations.get('total_urgent', 0)}")
            for i, rec in enumerate(recommendations.get('recommendations', [])[:3]):
                print(f"    {i+1}. {rec.get('title', 'N/A')} ({rec.get('priority', 'N/A')})")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
    
    # Test 3: Achievements
    print("\n🏆 Test des achievements...")
    try:
        response = requests.get(f"{base_url}/gamification/achievements")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            achievements = response.json()
            print("✅ Achievements récupérés avec succès:")
            print(f"  - Nombre d'achievements: {len(achievements.get('achievements', []))}")
            print(f"  - Achievements débloqués: {achievements.get('total_unlocked', 0)}")
            print(f"  - Total disponible: {achievements.get('total_available', 0)}")
            for i, achievement in enumerate(achievements.get('achievements', [])[:3]):
                status = "✅" if achievement.get('unlocked', False) else "⏳"
                print(f"    {status} {achievement.get('title', 'N/A')}")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
    
    # Test 4: Événements du calendrier
    print("\n📅 Test des événements du calendrier...")
    try:
        start_date = datetime.now().isoformat()
        end_date = (datetime.now() + timedelta(days=30)).isoformat()
        
        response = requests.get(f"{base_url}/calendar/events?start_date={start_date}&end_date={end_date}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            events = response.json()
            print("✅ Événements du calendrier récupérés avec succès:")
            print(f"  - Nombre d'événements: {len(events)}")
            for i, event in enumerate(events[:3]):
                print(f"    {i+1}. {event.get('title', 'N/A')} ({event.get('type', 'N/A')})")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Test des fonctionnalités avancées terminé !")

if __name__ == "__main__":
    test_organization_advanced_no_auth() 