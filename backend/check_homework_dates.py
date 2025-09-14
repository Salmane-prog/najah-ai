#!/usr/bin/env python3
"""
Vérifier les dates des devoirs dans la base de données
"""

import sqlite3
from datetime import datetime, timedelta

def check_homework_dates():
    """Vérifier les dates des devoirs"""
    
    print("🔍 Vérification des dates des devoirs")
    print("=" * 40)
    
    # Connexion à la base de données
    conn = sqlite3.connect('../data/app.db')
    cursor = conn.cursor()
    
    try:
        # Récupérer tous les devoirs
        cursor.execute("""
            SELECT id, title, subject, due_date, status, assigned_to
            FROM homework
            ORDER BY due_date
        """)
        
        homeworks = cursor.fetchall()
        
        print(f"📋 Nombre total de devoirs: {len(homeworks)}")
        print()
        
        today = datetime.now()
        next_week = today + timedelta(days=7)
        
        for hw in homeworks:
            hw_id, title, subject, due_date_str, status, assigned_to = hw
            
            # Convertir la date
            try:
                due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
                due_date_local = due_date.replace(tzinfo=None)  # Enlever le timezone
            except:
                due_date_local = datetime.now()
            
            days_until_due = (due_date_local - today).days
            
            print(f"📝 Devoir {hw_id}:")
            print(f"   Titre: {title}")
            print(f"   Matière: {subject}")
            print(f"   Date d'échéance: {due_date_local.strftime('%Y-%m-%d %H:%M')}")
            print(f"   Jours restants: {days_until_due}")
            print(f"   Statut: {status}")
            print(f"   Assigné à: {assigned_to}")
            
            # Vérifier si c'est dans les 7 prochains jours
            if due_date_local >= today and due_date_local <= next_week and status != 'completed':
                print(f"   ✅ Sera affiché dans le calendrier")
            else:
                print(f"   ❌ Ne sera PAS affiché dans le calendrier")
            print()
        
        # Vérifier les devoirs qui devraient apparaître dans le calendrier
        print("📅 Devoirs qui devraient apparaître dans le calendrier:")
        calendar_homeworks = []
        
        for hw in homeworks:
            hw_id, title, subject, due_date_str, status, assigned_to = hw
            
            try:
                due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
                due_date_local = due_date.replace(tzinfo=None)
            except:
                continue
            
            if (due_date_local >= today and 
                due_date_local <= next_week and 
                status != 'completed' and
                assigned_to == 4):  # Étudiant Salmane
                calendar_homeworks.append(hw)
                print(f"   - {title} ({subject}) - {due_date_local.strftime('%Y-%m-%d')}")
        
        if not calendar_homeworks:
            print("   ❌ Aucun devoir à afficher dans le calendrier")
        else:
            print(f"   ✅ {len(calendar_homeworks)} devoir(s) à afficher")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_homework_dates() 