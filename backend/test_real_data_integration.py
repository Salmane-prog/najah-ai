import requests
import json
from datetime import datetime, timedelta

def test_real_data_integration():
    """Test complet de l'intégration des données réelles"""
    
    print("🚀 Test d'intégration des données réelles")
    print("=" * 60)
    
    # Test 1: Données d'organisation réelles
    print("\n📚 Test des données d'organisation réelles...")
    try:
        response = requests.get("http://localhost:8000/api/v1/student-organization/homework")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            homeworks = response.json()
            print(f"✅ {len(homeworks)} devoirs récupérés")
            for hw in homeworks[:3]:
                print(f"  - {hw.get('title', 'N/A')} ({hw.get('status', 'N/A')})")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
    
    # Test 2: Analytics de productivité réels
    print("\n📊 Test des analytics de productivité réels...")
    try:
        response = requests.get("http://localhost:8000/api/v1/student-organization/analytics/productivity")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            analytics = response.json()
            print("✅ Analytics récupérés:")
            print(f"  - Temps d'étude: {analytics.get('study_time_hours', 0)}h")
            print(f"  - Productivité: {analytics.get('avg_productivity', 0)}/10")
            print(f"  - Completion devoirs: {analytics.get('homework_completion_rate', 0)}%")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
    
    # Test 3: Recommandations prioritaires
    print("\n🎯 Test des recommandations prioritaires...")
    try:
        response = requests.get("http://localhost:8000/api/v1/student-organization/recommendations/priority-tasks")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            recommendations = response.json()
            print(f"✅ {len(recommendations.get('recommendations', []))} recommandations")
            print(f"  - Urgentes: {recommendations.get('total_urgent', 0)}")
            print(f"  - Élevées: {recommendations.get('total_high', 0)}")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
    
    # Test 4: Notifications automatiques
    print("\n🔔 Test des notifications automatiques...")
    try:
        response = requests.get("http://localhost:8000/api/v1/notifications-auto/notifications")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            notifications = response.json()
            print(f"✅ {len(notifications)} notifications récupérées")
            for notif in notifications[:3]:
                print(f"  - {notif.get('title', 'N/A')} ({notif.get('type', 'N/A')})")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
    
    # Test 5: Rapports de progression
    print("\n📈 Test des rapports de progression...")
    try:
        response = requests.get("http://localhost:8000/api/v1/progress-reports/weekly-progress")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            progress = response.json()
            print(f"✅ Progression de {progress.get('student_name', 'N/A')}")
            print(f"  - Semaines analysées: {len(progress.get('weekly_progress', []))}")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
    
    # Test 6: Progression par matière
    print("\n📚 Test de la progression par matière...")
    try:
        response = requests.get("http://localhost:8000/api/v1/progress-reports/subject-progress")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            subject_progress = response.json()
            subjects = subject_progress.get('subjects_progress', {})
            print(f"✅ Progression sur {len(subjects)} matières")
            for subject, data in subjects.items():
                print(f"  - {subject}: {data.get('avg_progress', 0):.1f}%")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
    
    # Test 7: Recommandations personnalisées
    print("\n💡 Test des recommandations personnalisées...")
    try:
        response = requests.get("http://localhost:8000/api/v1/progress-reports/recommendations")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            recommendations = response.json()
            recs = recommendations.get('recommendations', [])
            print(f"✅ {len(recs)} recommandations personnalisées")
            for rec in recs[:3]:
                print(f"  - {rec.get('title', 'N/A')} ({rec.get('priority', 'N/A')})")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
    
    # Test 8: Assignations des professeurs
    print("\n👨‍🏫 Test des assignations des professeurs...")
    try:
        response = requests.get("http://localhost:8000/api/v1/teacher-assignments/homework")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            homeworks = response.json()
            print(f"✅ {len(homeworks)} devoirs assignés par les professeurs")
            for hw in homeworks[:3]:
                print(f"  - {hw.get('title', 'N/A')} ({hw.get('subject', 'N/A')})")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
    
    # Test 9: Statistiques des devoirs
    print("\n📊 Test des statistiques des devoirs...")
    try:
        response = requests.get("http://localhost:8000/api/v1/teacher-assignments/homework/stats")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            stats = response.json()
            print("✅ Statistiques des devoirs:")
            print(f"  - Total: {stats.get('total_homework', 0)}")
            print(f"  - Terminés: {stats.get('completed_homework', 0)}")
            print(f"  - En retard: {stats.get('overdue_homework', 0)}")
            print(f"  - Taux de completion: {stats.get('completion_rate', 0)}%")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
    
    # Test 10: Statistiques des objectifs
    print("\n🎯 Test des statistiques des objectifs...")
    try:
        response = requests.get("http://localhost:8000/api/v1/teacher-assignments/learning-goals/stats")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            stats = response.json()
            print("✅ Statistiques des objectifs:")
            print(f"  - Total: {stats.get('total_goals', 0)}")
            print(f"  - Actifs: {stats.get('active_goals', 0)}")
            print(f"  - Terminés: {stats.get('completed_goals', 0)}")
            print(f"  - Progression moyenne: {stats.get('average_progress', 0)}%")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Test d'intégration des données réelles terminé !")

if __name__ == "__main__":
    test_real_data_integration() 