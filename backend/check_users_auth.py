#!/usr/bin/env python3
"""
Script pour vérifier les utilisateurs et leurs emails
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text

def check_users_auth():
    """Vérifier les utilisateurs et leurs emails"""
    
    # Créer une connexion directe à la base de données
    engine = create_engine("sqlite:///../data/app.db")
    
    try:
        with engine.connect() as conn:
            print("👥 Vérification des utilisateurs")
            print("=" * 40)
            
            # Récupérer tous les utilisateurs
            result = conn.execute(text("""
                SELECT id, username, email, role, is_active
                FROM users
                ORDER BY id
            """))
            users = result.fetchall()
            
            print(f"📊 Total utilisateurs: {len(users)}")
            print("\n📋 Liste des utilisateurs:")
            
            for user in users:
                print(f"   - ID: {user[0]}")
                print(f"     Username: {user[1]}")
                print(f"     Email: {user[2]}")
                print(f"     Role: {user[3]}")
                print(f"     Actif: {user[4]}")
                print()
            
            # Chercher les professeurs
            print("👨‍🏫 Professeurs:")
            teachers = [u for u in users if u[3] == 'teacher']
            for teacher in teachers:
                print(f"   - {teacher[1]} ({teacher[2]}) - ID: {teacher[0]}")
            
            # Chercher les étudiants
            print("\n👤 Étudiants:")
            students = [u for u in users if u[3] == 'student']
            for student in students:
                print(f"   - {student[1]} ({student[2]}) - ID: {student[0]}")
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")

if __name__ == "__main__":
    check_users_auth() 