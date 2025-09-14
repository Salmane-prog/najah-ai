#!/usr/bin/env python3
"""
Script de test pour vérifier les nouveaux endpoints
Projet : NaJA7 AI - Adaptive and Intelligent Tutoring System
"""

import requests
import json
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

def test_forum_endpoints():
    """Tester les endpoints du forum"""
    print("🧪 TEST DES ENDPOINTS FORUM")
    print("=" * 50)
    
    # Test 1: Récupérer les catégories du forum
    try:
        response = requests.get(f"{API_BASE}/forum/categories")
        print(f"✅ GET /forum/categories - Status: {response.status_code}")
        if response.status_code == 200:
            categories = response.json()
            print(f"   📊 {len(categories)} catégories trouvées")
    except Exception as e:
        print(f"❌ GET /forum/categories - Erreur: {e}")
    
    # Test 2: Récupérer les tags du forum
    try:
        response = requests.get(f"{API_BASE}/forum/tags")
        print(f"✅ GET /forum/tags - Status: {response.status_code}")
        if response.status_code == 200:
            tags = response.json()
            print(f"   📊 {len(tags)} tags trouvés")
    except Exception as e:
        print(f"❌ GET /forum/tags - Erreur: {e}")
    
    print()

def test_organization_endpoints():
    """Tester les endpoints d'organisation"""
    print("🧪 TEST DES ENDPOINTS ORGANISATION")
    print("=" * 50)
    
    # Test 1: Récupérer les devoirs
    try:
        response = requests.get(f"{API_BASE}/organization/homework")
        print(f"✅ GET /organization/homework - Status: {response.status_code}")
        if response.status_code == 200:
            homework = response.json()
            print(f"   📊 {len(homework)} devoirs trouvés")
    except Exception as e:
        print(f"❌ GET /organization/homework - Erreur: {e}")
    
    # Test 2: Récupérer les sessions d'étude
    try:
        response = requests.get(f"{API_BASE}/organization/study-sessions")
        print(f"✅ GET /organization/study-sessions - Status: {response.status_code}")
        if response.status_code == 200:
            sessions = response.json()
            print(f"   📊 {len(sessions)} sessions trouvées")
    except Exception as e:
        print(f"❌ GET /organization/study-sessions - Erreur: {e}")
    
    # Test 3: Récupérer les rappels
    try:
        response = requests.get(f"{API_BASE}/organization/reminders")
        print(f"✅ GET /organization/reminders - Status: {response.status_code}")
        if response.status_code == 200:
            reminders = response.json()
            print(f"   📊 {len(reminders)} rappels trouvés")
    except Exception as e:
        print(f"❌ GET /organization/reminders - Erreur: {e}")
    
    # Test 4: Récupérer les objectifs d'apprentissage
    try:
        response = requests.get(f"{API_BASE}/organization/learning-goals")
        print(f"✅ GET /organization/learning-goals - Status: {response.status_code}")
        if response.status_code == 200:
            goals = response.json()
            print(f"   📊 {len(goals)} objectifs trouvés")
    except Exception as e:
        print(f"❌ GET /organization/learning-goals - Erreur: {e}")
    
    print()

def test_database_tables():
    """Vérifier que les tables ont été créées"""
    print("🧪 VÉRIFICATION DES TABLES DE BASE DE DONNÉES")
    print("=" * 50)
    
    import sqlite3
    import os
    
    db_path = "F:/IMT/stage/Yancode/Najah__AI/data/app.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Tables à vérifier
        new_tables = [
            'forum_moderation', 'forum_votes', 'forum_categories', 'forum_tags', 
            'thread_tags', 'forum_reports', 'note_tags', 'note_shares', 
            'note_versions', 'note_comments', 'homework', 'study_sessions', 
            'reminders', 'learning_goals', 'user_favorites', 'collections', 
            'collection_items', 'content_history', 'content_recommendations',
            'playlists', 'playlist_items', 'user_interface_preferences', 
            'level_objectives', 'user_objective_progress'
        ]
        
        existing_tables = []
        missing_tables = []
        
        for table in new_tables:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
            if cursor.fetchone():
                existing_tables.append(table)
                print(f"  ✅ {table}")
            else:
                missing_tables.append(table)
                print(f"  ❌ {table}")
        
        print(f"\n📊 RÉSULTATS :")
        print(f"✅ Tables créées : {len(existing_tables)}/{len(new_tables)}")
        print(f"❌ Tables manquantes : {len(missing_tables)}")
        
        if missing_tables:
            print(f"\n⚠️  TABLES MANQUANTES :")
            for table in missing_tables:
                print(f"  - {table}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification des tables: {e}")
    
    print()

def test_server_status():
    """Tester le statut du serveur"""
    print("🧪 TEST DU STATUT DU SERVEUR")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ GET / - Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   📄 Réponse: {response.text[:100]}...")
    except Exception as e:
        print(f"❌ GET / - Erreur: {e}")
        print("   💡 Assurez-vous que le serveur est démarré avec: python app.py")
    
    print()

def main():
    """Fonction principale de test"""
    print("🚀 TEST DES NOUVELLES FONCTIONNALITÉS - NAJA7 AI")
    print("=" * 60)
    print()
    
    # Test du statut du serveur
    test_server_status()
    
    # Test des tables de base de données
    test_database_tables()
    
    # Test des endpoints (nécessite que le serveur soit démarré)
    print("💡 Pour tester les endpoints, démarrez le serveur avec:")
    print("   cd backend && python app.py")
    print("   Puis exécutez ce script dans un autre terminal")
    print()
    
    # Test des endpoints (commenté car le serveur n'est pas démarré)
    # test_forum_endpoints()
    # test_organization_endpoints()
    
    print("🎉 TESTS TERMINÉS !")
    print()
    print("📋 PROCHAINES ÉTAPES :")
    print("1. Démarrer le serveur: cd backend && python app.py")
    print("2. Tester les endpoints avec ce script")
    print("3. Commencer le développement frontend")
    print("4. Intégrer les nouvelles fonctionnalités dans l'interface")

if __name__ == "__main__":
    main() 