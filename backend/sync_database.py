#!/usr/bin/env python3
from core.database import SessionLocal
from models.user import User, UserRole
from core.security import get_password_hash
import sqlite3
import os

def sync_database_with_real_data():
    """Synchroniser la base de données avec les vraies données"""
    print("🔄 Synchronisation de la base de données...")
    
    db = SessionLocal()
    try:
        # Supprimer tous les utilisateurs existants
        print("🗑️ Suppression des anciens utilisateurs...")
        db.query(User).delete()
        db.commit()
        print("✅ Anciens utilisateurs supprimés")
        
        # Créer les utilisateurs réels basés sur votre interface
        real_users = [
            {
                "username": "admin",
                "email": "admin@najah.ai",
                "password": "admin123",
                "role": UserRole.teacher
            },
            {
                "username": "salmane",
                "email": "marie.dubois@najah.ai",
                "password": "salmane123@",
                "role": UserRole.teacher
            },
            {
                "username": "teacher2",
                "email": "ahmed.benali@najah.ai",
                "password": "teacher123",
                "role": UserRole.teacher
            },
            {
                "username": "student1",
                "email": "salmane.hajouji@najah.ai",
                "password": "student123",
                "role": UserRole.student
            },
            {
                "username": "student2",
                "email": "fatima.alami@najah.ai",
                "password": "student123",
                "role": UserRole.student
            },
            {
                "username": "student3",
                "email": "omar.benjelloun@najah.ai",
                "password": "student123",
                "role": UserRole.student
            },
            {
                "username": "teacher_test",
                "email": "teacher@test.com",
                "password": "password123",
                "role": UserRole.teacher
            },
            {
                "username": "student_test",
                "email": "student@test.com",
                "password": "password123",
                "role": UserRole.student
            },
            {
                "username": "marie.dubois",
                "email": "marie.dubois@example.com",
                "password": "password123",
                "role": UserRole.student
            },
            {
                "username": "jean.martin",
                "email": "jean.martin@example.com",
                "password": "password123",
                "role": UserRole.student
            },
            {
                "username": "sophie.bernard",
                "email": "sophie.bernard@example.com",
                "password": "password123",
                "role": UserRole.student
            },
            {
                "username": "pierre.durand",
                "email": "pierre.durand@example.com",
                "password": "password123",
                "role": UserRole.student
            },
            {
                "username": "superadmin",
                "email": "superadmin@najah.ai",
                "password": "admin123",
                "role": UserRole.admin
            }
        ]
        
        print("👥 Création des utilisateurs réels...")
        for user_data in real_users:
            hashed_password = get_password_hash(user_data["password"])
            new_user = User(
                username=user_data["username"],
                email=user_data["email"],
                hashed_password=hashed_password,
                role=user_data["role"]
            )
            db.add(new_user)
            print(f"   ✅ {user_data['email']} ({user_data['password']}) - {user_data['role']}")
        
        db.commit()
        print("✅ Synchronisation terminée!")
        
        # Afficher tous les utilisateurs
        print("\n📋 Liste des utilisateurs disponibles:")
        users = db.query(User).all()
        for user in users:
            print(f"   • {user.username} ({user.email}) - {user.role}")
            
    except Exception as e:
        print(f"❌ Erreur lors de la synchronisation: {e}")
        db.rollback()
    finally:
        db.close()

def test_login_marie():
    """Tester la connexion avec marie.dubois@najah.ai"""
    print("\n🔐 Test de connexion avec marie.dubois@najah.ai...")
    
    import requests
    import json
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            json={
                "email": "marie.dubois@najah.ai",
                "password": "salmane123@"
            },
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Connexion réussie!")
            print(f"   Token: {data.get('access_token', '')[:20]}...")
            print(f"   Role: {data.get('role', '')}")
            print(f"   ID: {data.get('id', '')}")
            print(f"   Name: {data.get('name', '')}")
            return True
        else:
            print("❌ Échec de connexion")
            try:
                error_data = response.json()
                print(f"   Erreur: {error_data.get('detail', '')}")
            except:
                print(f"   Réponse: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def test_all_accounts():
    """Tester tous les comptes"""
    print("\n🔐 Test de tous les comptes...")
    
    import requests
    
    test_accounts = [
        {"email": "marie.dubois@najah.ai", "password": "salmane123@", "name": "Marie (Teacher)"},
        {"email": "student@test.com", "password": "password123", "name": "Student Test"},
        {"email": "teacher@test.com", "password": "password123", "name": "Teacher Test"},
        {"email": "admin@najah.ai", "password": "admin123", "name": "Admin"},
        {"email": "superadmin@najah.ai", "password": "admin123", "name": "Super Admin"}
    ]
    
    for account in test_accounts:
        print(f"\n--- Test: {account['name']} ---")
        try:
            response = requests.post(
                "http://localhost:8000/api/v1/auth/login",
                json={
                    "email": account["email"],
                    "password": account["password"]
                },
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {account['name']}: Connexion réussie (Role: {data.get('role', '')})")
            else:
                print(f"❌ {account['name']}: Échec de connexion")
                
        except Exception as e:
            print(f"❌ {account['name']}: Erreur - {e}")

def main():
    print("🔄 Synchronisation de la base de données - Najah AI")
    print("=" * 60)
    
    # Synchroniser la base de données
    sync_database_with_real_data()
    
    # Tester la connexion
    test_login_marie()
    
    # Tester tous les comptes
    test_all_accounts()
    
    print("\n" + "=" * 60)
    print("🏁 Synchronisation terminée")
    print("\n📋 Comptes principaux:")
    print("   • marie.dubois@najah.ai (salmane123@) - Enseignant")
    print("   • student@test.com (password123) - Étudiant")
    print("   • teacher@test.com (password123) - Enseignant")
    print("   • admin@najah.ai (admin123) - Administrateur")

if __name__ == "__main__":
    main() 