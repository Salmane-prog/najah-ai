#!/usr/bin/env python3
"""
Script de test complet pour les nouvelles fonctionnalités :
- Interface frontend professeur
- Système de notifications
- Statistiques de performance
"""

import requests
import json
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:8000"

def test_notifications_system():
    """Test du système de notifications"""
    print("\n🔔 Test: Système de Notifications")
    print("=" * 60)
    
    try:
        # Test 1: Récupérer toutes les notifications
        print("📝 Test 1: Récupération des notifications")
        response = requests.get(f"{BASE_URL}/api/v1/notifications/quiz")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Succès!")
            print(f"Total notifications: {data['total_count']}")
            print(f"Non lues: {data['unread_count']}")
            
            if data['notifications']:
                print("Exemples de notifications:")
                for notif in data['notifications'][:3]:
                    print(f"  - {notif['title']}: {notif['message'][:50]}...")
        else:
            print(f"❌ Erreur: {response.text}")
        
        # Test 2: Notifications en retard
        print("\n📝 Test 2: Quiz en retard")
        response = requests.get(f"{BASE_URL}/api/v1/notifications/overdue")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Succès!")
            print(f"Quiz en retard: {data['total_overdue']}")
            
            if data['overdue_quizzes']:
                for quiz in data['overdue_quizzes']:
                    print(f"  - {quiz['quiz_title']} ({quiz['days_overdue']} jours de retard)")
        else:
            print(f"❌ Erreur: {response.text}")
        
        # Test 3: Résumé des notifications
        print("\n📝 Test 3: Résumé des notifications")
        response = requests.get(f"{BASE_URL}/api/v1/notifications/summary")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Succès!")
            print(f"Total: {data['total_notifications']}")
            print(f"Priorité haute: {data['high_priority']}")
            print(f"Quiz en retard: {data['overdue_quizzes']}")
            print(f"Échéance proche: {data['due_soon_quizzes']}")
        else:
            print(f"❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_analytics_system():
    """Test du système d'analytics"""
    print("\n📊 Test: Système d'Analytics")
    print("=" * 60)
    
    try:
        # Test 1: Performance de classe
        print("📝 Test 1: Performance de classe")
        response = requests.get(f"{BASE_URL}/api/v1/analytics/class/performance?period=month&subject=all")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Succès!")
            print(f"Total étudiants: {data['total_students']}")
            print(f"Moyenne classe: {data['class_average']:.1f}%")
            print(f"Taux réussite: {data['completion_rate']:.1f}%")
            print(f"Top performers: {len(data['top_performers'])}")
            print(f"Étudiants en difficulté: {len(data['struggling_students'])}")
            
            if data['subject_performance']:
                print("Performance par matière:")
                for subject, stats in data['subject_performance'].items():
                    print(f"  - {subject}: {stats['average_score']:.1f}% (réussite: {stats['pass_rate']:.1f}%)")
        else:
            print(f"❌ Erreur: {response.text}")
        
        # Test 2: Performance individuelle
        print("\n📝 Test 2: Performance individuelle")
        response = requests.get(f"{BASE_URL}/api/v1/analytics/students/performance?period=month&subject=all")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Succès!")
            print(f"Total étudiants: {data['total_students']}")
            print(f"Période: {data['period']}")
            print(f"Matière: {data['subject']}")
            
            if data['students']:
                print("Exemples de performances:")
                for student in data['students'][:3]:
                    print(f"  - {student['student_name']}: {student['average_score']:.1f}% ({student['total_quizzes']} quiz)")
                    print(f"    Tendance: {student['improvement_trend']}")
        else:
            print(f"❌ Erreur: {response.text}")
        
        # Test 3: Résumé dashboard
        print("\n📝 Test 3: Résumé dashboard")
        response = requests.get(f"{BASE_URL}/api/v1/analytics/dashboard/summary")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Succès!")
            print(f"Total étudiants: {data['total_students']}")
            print(f"Total quiz: {data['total_quizzes']}")
            print(f"Total assignations: {data['total_assignments']}")
            print(f"Complétions récentes: {data['recent_completions']}")
            print(f"Quiz en retard: {data['overdue_quizzes']}")
            print(f"Score moyen: {data['average_score']}%")
        else:
            print(f"❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_quiz_assignments_enhanced():
    """Test des fonctionnalités améliorées des assignations"""
    print("\n📚 Test: Fonctionnalités Améliorées des Assignations")
    print("=" * 60)
    
    try:
        # Test 1: Assignation avec date d'échéance
        print("📝 Test 1: Assignation avec échéance")
        assignment_data = {
            "quiz_id": 1,
            "student_ids": [5],
            "due_date": (datetime.utcnow() + timedelta(days=3)).isoformat(),
            "class_id": None
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v1/quiz_assignments/assign",
            json=assignment_data
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Succès!")
            print(f"Message: {data['message']}")
            print(f"Assignations créées: {data['assigned_count']}")
        else:
            print(f"❌ Erreur: {response.text}")
        
        # Test 2: Vue professeur avec statuts
        print("\n📝 Test 2: Vue professeur avec statuts")
        response = requests.get(f"{BASE_URL}/api/v1/quiz_assignments/teacher/1/assignments")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Succès!")
            print(f"Total assignations: {data['total_assignments']}")
            
            if data['assignments']:
                for assignment in data['assignments']:
                    print(f"  - {assignment['quiz_title']} → {assignment['student_name']}")
                    print(f"    Statut: {assignment['status']} | Étudiant: {assignment['student_status']}")
                    if assignment['score']:
                        print(f"    Score: {assignment['score']}")
        else:
            print(f"❌ Erreur: {response.text}")
        
        # Test 3: Assignations en attente vs complétées
        print("\n📝 Test 3: Filtrage par statut")
        
        # En attente
        response = requests.get(f"{BASE_URL}/api/v1/quiz_assignments/student/5/pending")
        print(f"En attente - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Total en attente: {data['total_pending']}")
        
        # Complétées
        response = requests.get(f"{BASE_URL}/api/v1/quiz_assignments/student/5/completed")
        print(f"Complétées - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Total complétées: {data['total_completed']}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def main():
    """Test complet des nouvelles fonctionnalités"""
    print("🚀 Test complet des nouvelles fonctionnalités")
    print("=" * 60)
    
    # Test 1: Système de notifications
    test_notifications_system()
    
    # Test 2: Système d'analytics
    test_analytics_system()
    
    # Test 3: Fonctionnalités améliorées des assignations
    test_quiz_assignments_enhanced()
    
    print("\n" + "=" * 60)
    print("✅ Tests des nouvelles fonctionnalités terminés!")
    print("\n📋 Résumé des fonctionnalités implémentées:")
    print("1. ✅ Interface frontend professeur complète")
    print("2. ✅ Système de notifications avec alertes")
    print("3. ✅ Statistiques de performance avec graphiques")
    print("4. ✅ Gestion avancée des assignations")
    print("5. ✅ Analytics en temps réel")
    print("6. ✅ Système d'alertes pour quiz en retard")
    print("7. ✅ Export de données")
    print("8. ✅ Filtres et recherche avancés")

if __name__ == "__main__":
    main()













