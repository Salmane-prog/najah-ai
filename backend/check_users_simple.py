#!/usr/bin/env python3
"""
Script simple pour vérifier les utilisateurs dans la base de données
"""

import sqlite3
import os

def check_users():
    """Vérifier les utilisateurs dans la base de données"""
    
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), "..", "data", "app.db")
    
    if not os.path.exists(db_path):
        print(f"Base de données non trouvée: {db_path}")
        return
    
    print(f"Connexion à la base de données: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier les tables existantes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"\nTables disponibles: {[t[0] for t in tables]}")
        
        # Vérifier la table users
        if ('users',) in tables:
            print("\n=== Table users ===")
            cursor.execute("SELECT id, email, role, name FROM users LIMIT 10")
            users = cursor.fetchall()
            
            if users:
                print("Utilisateurs disponibles:")
                for user in users:
                    print(f"  ID: {user[0]}, Email: {user[1]}, Role: {user[2]}, Nom: {user[3]}")
            else:
                print("Aucun utilisateur trouvé")
                
            # Compter le total
            cursor.execute("SELECT COUNT(*) FROM users")
            total = cursor.fetchone()[0]
            print(f"\nTotal d'utilisateurs: {total}")
            
        else:
            print("Table 'users' non trouvée")
        
        conn.close()
        
    except Exception as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    check_users()











