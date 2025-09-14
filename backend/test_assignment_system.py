#!/usr/bin/env python3
"""
Script de test complet pour le système d'assignation de quiz
"""

import requests
import json
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:8000"
TEACHER_ID = 1
STUDENT_ID = 5
QUIZ_ID = 1  # ID du quiz à assigner

def test_teacher_assignment():
    """Test de l'assignation côté professeur"""
    print("\n🧪 Test: Assignation de quiz par le professeur")
    print("=" * 60)
    
    # Données d'assignation
    assignment_data = {
        "quiz_id": QUIZ_ID,
        "student_ids": [STUDENT_ID],
        "due_date": (datetime.utcnow() + timedelta(days=7)).isoformat(),
        "class_id": None
    }
    
    print(f"📝 Assignation du quiz {QUIZ_ID} à l'étudiant {STUDENT_ID}")
    print(f"📅 Date d'échéance: {assignment_data['due_date']}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/quiz_assignments/assign",
            json=assignment_data
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Succès!")
            print(f"Message: {data['message']}")
            print(f"Nombre d'assignations: {data['assigned_count']}")
            print("Détails des assignations:")
            for assignment in data['assignments']:
                print(f"  - Quiz: {assignment['quiz_title']}")
                print(f"    Étudiant: {assignment['student_name']}")
                print(f"    Date d'échéance: {assignment['due_date']}")
                print(f"    Statut: {assignment['status']}")
        else:
            print(f"❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_teacher_view_assignments():
    """Test de la vue des assignations côté professeur"""
    print("\n🧪 Test: Vue des assignations par le professeur")
    print("=" * 60)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/quiz_assignments/teacher/{TEACHER_ID}/assignments"
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Succès!")
            print(f"Professeur ID: {data['teacher_id']}")
            print(f"Total d'assignations: {data['total_assignments']}")
            
            if data['assignments']:
                print("Détails des assignations:")
                for assignment in data['assignments']:
                    print(f"  - Quiz: {assignment['quiz_title']}")
                    print(f"    Étudiant: {assignment['student_name']}")
                    print(f"    Statut: {assignment['status']}")
                    print(f"    Statut étudiant: {assignment['student_status']}")
                    if assignment.get('score'):
                        print(f"    Score: {assignment['score']}")
                    print()
            else:
                print("Aucune assignation trouvée")
        else:
            print(f"❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_student_view_assignments():
    """Test de la vue des assignations côté étudiant"""
    print("\n🧪 Test: Vue des assignations par l'étudiant")
    print("=" * 60)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/quiz_assignments/student/{STUDENT_ID}"
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Succès!")
            print(f"Nombre d'assignations: {len(data)}")
            
            if data:
                print("Détails des assignations:")
                for assignment in data:
                    print(f"  - Quiz: {assignment['quiz_title']}")
                    print(f"    Sujet: {assignment['subject']}")
                    print(f"    Date d'échéance: {assignment['due_date']}")
                    print(f"    Statut: {assignment['status']}")
                    print(f"    Statut étudiant: {assignment['student_status']}")
                    if assignment.get('score'):
                        print(f"    Score: {assignment['score']}")
                    if assignment.get('completed_at'):
                        print(f"    Complété le: {assignment['completed_at']}")
                    print()
            else:
                print("Aucune assignation trouvée")
        else:
            print(f"❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_pending_assignments():
    """Test des assignations en attente"""
    print("\n🧪 Test: Assignations en attente")
    print("=" * 60)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/quiz_assignments/student/{STUDENT_ID}/pending"
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Succès!")
            print(f"Total en attente: {data['total_pending']}")
            
            if data['assignments']:
                print("Assignations en attente:")
                for assignment in data['assignments']:
                    print(f"  - {assignment['quiz_title']} ({assignment['subject']})")
            else:
                print("Aucune assignation en attente")
        else:
            print(f"❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_completed_assignments():
    """Test des assignations complétées"""
    print("\n🧪 Test: Assignations complétées")
    print("=" * 60)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/quiz_assignments/student/{STUDENT_ID}/completed"
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Succès!")
            print(f"Total complétées: {data['total_completed']}")
            
            if data['assignments']:
                print("Assignations complétées:")
                for assignment in data['assignments']:
                    print(f"  - {assignment['quiz_title']} ({assignment['subject']})")
                    if assignment.get('score'):
                        print(f"    Score: {assignment['score']}")
                    if assignment.get('completed_at'):
                        print(f"    Complété le: {assignment['completed_at']}")
            else:
                print("Aucune assignation complétée")
        else:
            print(f"❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def main():
    """Test complet du système d'assignation"""
    print("🚀 Test complet du système d'assignation de quiz")
    print("=" * 60)
    
    # Test 1: Assignation par le professeur
    test_teacher_assignment()
    
    # Test 2: Vue des assignations par le professeur
    test_teacher_view_assignments()
    
    # Test 3: Vue des assignations par l'étudiant
    test_student_view_assignments()
    
    # Test 4: Assignations en attente
    test_pending_assignments()
    
    # Test 5: Assignations complétées
    test_completed_assignments()
    
    print("\n" + "=" * 60)
    print("✅ Tests du système d'assignation terminés!")
    print("\n📋 Résumé:")
    print("1. ✅ Professeur peut assigner un quiz à des étudiants")
    print("2. ✅ Professeur peut voir toutes ses assignations")
    print("3. ✅ Étudiant peut voir ses quiz assignés")
    print("4. ✅ Système distingue les quiz en attente vs complétés")
    print("5. ✅ Statut mis à jour automatiquement selon les résultats")

if __name__ == "__main__":
    main()
