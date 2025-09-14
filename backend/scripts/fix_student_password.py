#!/usr/bin/env python3
"""
Script pour corriger le mot de passe de salmane.hajouji@najah.ai
"""

import sqlite3
import os
import hashlib

def fix_student_password():
    """Corriger le mot de passe de salmane.hajouji@najah.ai"""
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'app.db')
    
    print(f"🔧 Correction du mot de passe pour salmane.hajouji@najah.ai")
    
    if not os.path.exists(db_path):
        print("❌ Base de données non trouvée!")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier l'utilisateur actuel
        cursor.execute("SELECT id, email, username, role, hashed_password FROM users WHERE email = 'salmane.hajouji@najah.ai';")
        student = cursor.fetchone()
        
        if not student:
            print("❌ Utilisateur salmane.hajouji@najah.ai non trouvé")
            return
        
        print(f"✅ Utilisateur trouvé: {student[1]}")
        print(f"   ID: {student[0]}")
        print(f"   Username: {student[2]}")
        print(f"   Role: {student[3]}")
        print(f"   Hash actuel: {student[4][:20]}...")
        
        # Créer un nouveau hash SHA256 simple
        password = "password123"
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        print(f"\n🔄 Mise à jour du mot de passe...")
        print(f"   Nouveau mot de passe: {password}")
        print(f"   Nouveau hash: {hashed_password}")
        
        # Mettre à jour le mot de passe
        cursor.execute(
            "UPDATE users SET hashed_password = ? WHERE email = ?",
            (hashed_password, 'salmane.hajouji@najah.ai')
        )
        
        conn.commit()
        print("✅ Mot de passe mis à jour avec succès!")
        
        # Vérifier la mise à jour
        cursor.execute("SELECT hashed_password FROM users WHERE email = 'salmane.hajouji@najah.ai';")
        new_hash = cursor.fetchone()[0]
        print(f"   Hash vérifié: {new_hash[:20]}...")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    fix_student_password() 