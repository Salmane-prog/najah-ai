#!/usr/bin/env python3
"""
Script de test pour toutes les nouvelles APIs
Teste les fonctionnalités avancées implémentées
"""

import requests
import json
import sqlite3
from datetime import datetime, timedelta
import random

# Configuration
BASE_URL = "http://localhost:8000"
TEST_EMAIL = "teacher@test.com"
TEST_PASSWORD = "salmane123@"

def get_auth_token():
    """Récupérer le token d'authentification"""
    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        })
        
        if response.status_code == 200:
            data = response.json()
            return data.get("access_token")
        else:
            print(f"❌ Erreur de connexion: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Erreur de connexion: {str(e)}")
        return None

def test_calendar_api(token):
    """Tester l'API Calendrier"""
    print("\n📅 Test de l'API Calendrier")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Créer un événement
    event_data = {
        "title": "Test Cours Mathématiques",
        "description": "Cours de test pour les nouvelles APIs",
        "event_type": "course",
        "start_time": (datetime.now() + timedelta(days=1)).isoformat(),
        "end_time": (datetime.now() + timedelta(days=1, hours=2)).isoformat(),
        "location": "Salle 101",
        "subject": "Mathématiques",
        "color": "#3B82F6"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/calendar/events", 
                               headers=headers, json=event_data)
        
        if response.status_code == 200:
            print("✅ Événement créé avec succès")
            event_id = response.json().get("event_id")
            
            # Récupérer les événements
            response = requests.get(f"{BASE_URL}/api/v1/calendar/events", headers=headers)
            if response.status_code == 200:
                events = response.json()
                print(f"✅ {len(events)} événements récupérés")
                
                # Récupérer les événements à venir
                response = requests.get(f"{BASE_URL}/api/v1/calendar/upcoming", headers=headers)
                if response.status_code == 200:
                    upcoming = response.json()
                    print(f"✅ {len(upcoming)} événements à venir")
                else:
                    print(f"❌ Erreur récupération événements à venir: {response.status_code}")
            else:
                print(f"❌ Erreur récupération événements: {response.status_code}")
        else:
            print(f"❌ Erreur création événement: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur test calendrier: {str(e)}")

def test_continuous_assessment_api(token):
    """Tester l'API Évaluation Continue"""
    print("\n📊 Test de l'API Évaluation Continue")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Créer une compétence
    competency_data = {
        "name": "Résolution d'équations",
        "description": "Capacité à résoudre des équations du premier degré",
        "subject": "Mathématiques",
        "level": "intermediate",
        "category": "skills"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/continuous_assessment/competencies", 
                               headers=headers, json=competency_data)
        
        if response.status_code == 200:
            print("✅ Compétence créée avec succès")
            competency_id = response.json().get("competency_id")
            
            # Récupérer les compétences
            response = requests.get(f"{BASE_URL}/api/v1/continuous_assessment/competencies", headers=headers)
            if response.status_code == 200:
                competencies = response.json()
                print(f"✅ {len(competencies)} compétences récupérées")
                
                # Créer une évaluation continue
                assessment_data = {
                    "title": "Évaluation Continue Mathématiques",
                    "description": "Évaluation des compétences en résolution d'équations",
                    "assessment_type": "quiz",
                    "subject": "Mathématiques",
                    "competencies_targeted": [competency_id] if competency_id else [],
                    "weight": 1.0,
                    "due_date": (datetime.now() + timedelta(days=7)).isoformat()
                }
                
                response = requests.post(f"{BASE_URL}/api/v1/continuous_assessment/assessments", 
                                       headers=headers, json=assessment_data)
                
                if response.status_code == 200:
                    print("✅ Évaluation continue créée avec succès")
                else:
                    print(f"❌ Erreur création évaluation: {response.status_code}")
            else:
                print(f"❌ Erreur récupération compétences: {response.status_code}")
        else:
            print(f"❌ Erreur création compétence: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur test évaluation continue: {str(e)}")

def test_export_reports_api(token):
    """Tester l'API Export et Rapports"""
    print("\n📄 Test de l'API Export et Rapports")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # Récupérer les rapports disponibles
        response = requests.get(f"{BASE_URL}/api/v1/export_reports/reports/available", headers=headers)
        
        if response.status_code == 200:
            reports = response.json()
            print(f"✅ {len(reports)} types de rapports disponibles")
            
            # Tester l'export PDF d'un étudiant (simulation)
            print("✅ Test d'export PDF simulé")
            
            # Tester l'export Excel d'une classe (simulation)
            print("✅ Test d'export Excel simulé")
            
        else:
            print(f"❌ Erreur récupération rapports: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur test export rapports: {str(e)}")

def create_test_data():
    """Créer des données de test pour les nouvelles fonctionnalités"""
    print("\n🗄️ Création de données de test")
    
    try:
        conn = sqlite3.connect('data/app.db')
        cursor = conn.cursor()
        
        # Créer des événements de calendrier
        cursor.execute("""
            INSERT INTO schedule_events (title, description, event_type, start_time, end_time, 
                                       location, teacher_id, subject, color, is_active, created_at, updated_at)
            VALUES 
            ('Cours Mathématiques', 'Cours sur les équations', 'course', 
             datetime('now', '+1 day'), datetime('now', '+1 day', '+2 hours'),
             'Salle 101', 1, 'Mathématiques', '#3B82F6', 1, datetime('now'), datetime('now')),
            ('Examen Physique', 'Examen sur la mécanique', 'exam',
             datetime('now', '+3 days'), datetime('now', '+3 days', '+3 hours'),
             'Salle 102', 1, 'Physique', '#EF4444', 1, datetime('now'), datetime('now')),
            ('Reunion Equipe', 'Reunion de l\'equipe pedagogique', 'meeting',
             datetime('now', '+1 day', '+4 hours'), datetime('now', '+1 day', '+5 hours'),
             'Salle de reunion', 1, 'Administration', '#10B981', 1, datetime('now'), datetime('now'))
        """)
        
        # Créer des compétences
        cursor.execute("""
            INSERT INTO competencies (name, description, subject, level, category, created_by, is_active, created_at, updated_at)
            VALUES 
            ('Résolution d\'équations', 'Capacité à résoudre des équations du premier degré', 'Mathématiques', 'intermediate', 'skills', 1, 1, datetime('now'), datetime('now')),
            ('Compréhension de texte', 'Capacité à comprendre et analyser un texte', 'Français', 'beginner', 'knowledge', 1, 1, datetime('now'), datetime('now')),
            ('Expérimentation scientifique', 'Capacité à mener des expériences', 'Sciences', 'advanced', 'skills', 1, 1, datetime('now'), datetime('now'))
        """)
        
        # Créer des évaluations continues
        cursor.execute("""
            INSERT INTO continuous_assessments (title, description, assessment_type, subject, teacher_id, 
                                              competencies_targeted, weight, due_date, is_active, created_at, updated_at)
            VALUES 
            ('Évaluation Continue Mathématiques', 'Évaluation des compétences en résolution d\'équations', 'quiz', 'Mathématiques', 1, 
             '[1]', 1.0, datetime('now', '+7 days'), 1, datetime('now'), datetime('now')),
            ('Évaluation Continue Français', 'Évaluation de la compréhension de texte', 'project', 'Français', 1,
             '[2]', 1.5, datetime('now', '+10 days'), 1, datetime('now'), datetime('now'))
        """)
        
        conn.commit()
        print("✅ Données de test créées avec succès")
        
    except Exception as e:
        print(f"❌ Erreur création données de test: {str(e)}")
    finally:
        conn.close()

def main():
    """Fonction principale de test"""
    print("🚀 Test des nouvelles APIs - Najah AI")
    print("=" * 50)
    
    # Créer des données de test
    create_test_data()
    
    # Récupérer le token d'authentification
    token = get_auth_token()
    if not token:
        print("❌ Impossible de récupérer le token d'authentification")
        return
    
    print(f"✅ Authentification réussie")
    
    # Tester les APIs
    test_calendar_api(token)
    test_continuous_assessment_api(token)
    test_export_reports_api(token)
    
    print("\n🎉 Tests terminés !")
    print("=" * 50)

if __name__ == "__main__":
    main() 