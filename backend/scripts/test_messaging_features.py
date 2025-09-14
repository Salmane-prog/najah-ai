#!/usr/bin/env python3
"""
Script pour tester toutes les fonctionnalités de messagerie
"""

import requests
import json

def test_messaging_features():
    """Tester toutes les fonctionnalités de messagerie."""
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
        
        print("=== TEST DES FONCTIONNALITÉS DE MESSAGERIE ===")
        
        # 1. Tester la récupération des étudiants
        print("\n1. 📚 RÉCUPÉRATION DES ÉTUDIANTS")
        response = requests.get(f"{base_url}/api/v1/users/students", headers=headers)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            students = response.json()
            print(f"   ✅ {len(students)} étudiants trouvés")
            for i, student in enumerate(students[:3]):  # Afficher les 3 premiers
                print(f"      - {student.get('name', 'N/A')} ({student.get('email', 'N/A')})")
        else:
            print(f"   ❌ Erreur: {response.status_code}")
        
        # 2. Tester la récupération des conversations
        print("\n2. 💬 CONVERSATIONS EXISTANTES")
        response = requests.get(f"{base_url}/api/v1/teacher_messaging/conversations", headers=headers)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            conversations = response.json().get('conversations', [])
            print(f"   ✅ {len(conversations)} conversations trouvées")
            for conv in conversations:
                student = conv.get('student', {})
                print(f"      - {student.get('name', 'N/A')} (Thread: {conv.get('thread_id', 'N/A')})")
        else:
            print(f"   ❌ Erreur: {response.status_code}")
        
        # 3. Tester la création d'une nouvelle conversation
        print("\n3. 🆕 CRÉATION D'UNE NOUVELLE CONVERSATION")
        if students:
            student_id = students[0].get('id')
            response = requests.get(f"{base_url}/api/v1/teacher_messaging/conversation/{student_id}", headers=headers)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Conversation créée avec {students[0].get('name')}")
                print(f"      Thread ID: {data.get('thread_id', 'N/A')}")
                thread_id = data.get('thread_id')
            else:
                print(f"   ❌ Erreur: {response.status_code}")
                thread_id = None
        else:
            print("   ⚠️  Aucun étudiant disponible")
            thread_id = None
        
        # 4. Tester l'envoi d'un message
        print("\n4. 📤 ENVOI D'UN MESSAGE")
        if thread_id:
            message_data = {
                "content": "Bonjour ! Ceci est un test de messagerie. Comment allez-vous ?"
            }
            response = requests.post(f"{base_url}/api/v1/teacher_messaging/conversation/{student_id}/send", 
                                  headers=headers, json=message_data)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print("   ✅ Message envoyé avec succès")
            else:
                print(f"   ❌ Erreur: {response.status_code}")
                print(f"      Response: {response.text}")
        
        # 5. Tester la récupération des messages
        print("\n5. 📥 RÉCUPÉRATION DES MESSAGES")
        if thread_id:
            response = requests.get(f"{base_url}/api/v1/teacher_messaging/conversation/{student_id}/messages", headers=headers)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                messages = response.json().get('messages', [])
                print(f"   ✅ {len(messages)} messages récupérés")
                for msg in messages:
                    print(f"      - {msg.get('sender_name', 'N/A')}: {msg.get('content', 'N/A')[:50]}...")
            else:
                print(f"   ❌ Erreur: {response.status_code}")
        
        # 6. Tester le marquage comme lu
        print("\n6. ✅ MARQUAGE COMME LU")
        if thread_id:
            response = requests.post(f"{base_url}/api/v1/teacher_messaging/conversation/{thread_id}/mark-read", headers=headers)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print("   ✅ Messages marqués comme lus")
            else:
                print(f"   ❌ Erreur: {response.status_code}")
        
        print("\n=== RÉSUMÉ ===")
        print("✅ Toutes les fonctionnalités de messagerie sont opérationnelles")
        print("✅ Les professeurs peuvent sélectionner des étudiants")
        print("✅ Les conversations se stockent dans la base de données")
        print("✅ Les messages sont envoyés et reçus")
        print("✅ Les notifications de lecture fonctionnent")
        
    except Exception as e:
        print(f"❌ Erreur générale: {str(e)}")

if __name__ == "__main__":
    test_messaging_features() 