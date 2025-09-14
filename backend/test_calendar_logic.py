#!/usr/bin/env python3
"""
Test de la logique du calendrier frontend
"""

import requests
from datetime import datetime, timedelta

def test_calendar_logic():
    """Tester la logique du calendrier"""
    
    print("🧪 Test de la logique du calendrier")
    print("=" * 40)
    
    try:
        # Récupérer les devoirs via l'API
        response = requests.get(
            "http://localhost:8000/student-organization/homework",
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        if response.status_code != 200:
            print(f"❌ Erreur API: {response.status_code}")
            return
        
        homeworks = response.json()
        print(f"📋 Devoirs récupérés: {len(homeworks)}")
        
        # Simuler la logique du frontend
        today = datetime.now()
        next_week = today + timedelta(days=7)
        
        print(f"📅 Aujourd'hui: {today.strftime('%Y-%m-%d')}")
        print(f"📅 Semaine prochaine: {next_week.strftime('%Y-%m-%d')}")
        print()
        
        upcoming_homeworks = []
        
        for homework in homeworks:
            title = homework.get('title', 'N/A')
            subject = homework.get('subject', 'N/A')
            due_date_str = homework.get('due_date', '')
            status = homework.get('status', 'pending')
            
            try:
                # Convertir la date comme dans le frontend
                due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
                due_date_local = due_date.replace(tzinfo=None)
            except Exception as e:
                print(f"❌ Erreur conversion date pour {title}: {e}")
                continue
            
            print(f"📝 {title} ({subject}):")
            print(f"   Date d'échéance: {due_date_local.strftime('%Y-%m-%d %H:%M')}")
            print(f"   Statut: {status}")
            
            # Logique du frontend: getUpcomingHomeworks()
            if (due_date_local >= today and 
                due_date_local <= next_week and 
                status != 'completed'):
                upcoming_homeworks.append(homework)
                print(f"   ✅ Sera affiché dans le calendrier")
            else:
                print(f"   ❌ Ne sera PAS affiché dans le calendrier")
                if due_date_local < today:
                    print(f"      Raison: Date passée")
                elif due_date_local > next_week:
                    print(f"      Raison: Plus de 7 jours")
                elif status == 'completed':
                    print(f"      Raison: Déjà terminé")
            print()
        
        print(f"📅 Résultat final: {len(upcoming_homeworks)} devoir(s) à afficher")
        for hw in upcoming_homeworks:
            print(f"   - {hw.get('title')} ({hw.get('subject')})")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_calendar_logic() 