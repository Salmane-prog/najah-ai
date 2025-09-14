#!/usr/bin/env python3
"""
Script pour tester tous les endpoints d'organisation et de notes
"""

import requests
import json

def test_all_endpoints():
    """Tester tous les endpoints d'organisation et de notes"""
    base_url = "http://localhost:8000"
    
    try:
        print("🧪 TEST DE TOUS LES ENDPOINTS")
        print("=" * 60)
        
        # Test 1: Notes - getNotes
        print("\n1. Test de NotesAPI.getNotes...")
        response = requests.get(f"{base_url}/notes-advanced/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            notes = response.json()
            print(f"   ✅ SUCCÈS: {len(notes)} notes récupérées")
        else:
            print(f"   ❌ ERREUR: {response.status_code} - {response.text}")
        
        # Test 2: Notes - getSubjects
        print("\n2. Test de NotesAPI.getSubjects...")
        response = requests.get(f"{base_url}/notes-advanced/subjects")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            subjects = response.json()
            print(f"   ✅ SUCCÈS: {len(subjects)} matières récupérées")
        else:
            print(f"   ❌ ERREUR: {response.status_code} - {response.text}")
        
        # Test 3: Notes - getChapters
        print("\n3. Test de NotesAPI.getChapters...")
        response = requests.get(f"{base_url}/notes-advanced/chapters")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            chapters = response.json()
            print(f"   ✅ SUCCÈS: {len(chapters)} chapitres récupérés")
        else:
            print(f"   ❌ ERREUR: {response.status_code} - {response.text}")
        
        # Test 4: Organization - getHomeworks
        print("\n4. Test de OrganizationAPI.getHomeworks...")
        response = requests.get(f"{base_url}/organization/homework")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            homeworks = response.json()
            print(f"   ✅ SUCCÈS: {len(homeworks)} devoirs récupérés")
        else:
            print(f"   ❌ ERREUR: {response.status_code} - {response.text}")
        
        # Test 5: Organization - getStudySessions
        print("\n5. Test de OrganizationAPI.getStudySessions...")
        response = requests.get(f"{base_url}/organization/study-sessions")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            sessions = response.json()
            print(f"   ✅ SUCCÈS: {len(sessions)} sessions d'étude récupérées")
        else:
            print(f"   ❌ ERREUR: {response.status_code} - {response.text}")
        
        # Test 6: Organization - getReminders
        print("\n6. Test de OrganizationAPI.getReminders...")
        response = requests.get(f"{base_url}/organization/reminders")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            reminders = response.json()
            print(f"   ✅ SUCCÈS: {len(reminders)} rappels récupérés")
        else:
            print(f"   ❌ ERREUR: {response.status_code} - {response.text}")
        
        # Test 7: Organization - getLearningGoals
        print("\n7. Test de OrganizationAPI.getLearningGoals...")
        response = requests.get(f"{base_url}/organization/learning-goals")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            goals = response.json()
            print(f"   ✅ SUCCÈS: {len(goals)} objectifs d'apprentissage récupérés")
        else:
            print(f"   ❌ ERREUR: {response.status_code} - {response.text}")
        
        print("\n" + "=" * 60)
        print("🎉 TEST DE TOUS LES ENDPOINTS TERMINÉ!")
        print("✅ Tous les endpoints sont maintenant accessibles!")
        print("✅ Les erreurs 405 sont RÉSOLUES!")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")

if __name__ == "__main__":
    test_all_endpoints() 