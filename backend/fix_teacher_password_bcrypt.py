#!/usr/bin/env python3
"""
Script pour corriger le mot de passe du professeur avec le bon hash bcrypt
"""

import sqlite3
import os
from pathlib import Path
import sys

# Ajouter le répertoire backend au path pour importer les modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.security import get_password_hash

def fix_teacher_password_bcrypt():
    """Corrige le mot de passe du professeur avec le bon hash bcrypt"""
    
    # Chemin vers la base de données
    db_path = Path(__file__).parent.parent / "data" / "app.db"
    
    if not db_path.exists():
        print(f"❌ Base de données non trouvée: {db_path}")
        return False
    
    print(f"🔧 Correction du mot de passe du professeur avec bcrypt...")
    print(f"   📁 Base de données: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Vérifier si la table users existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            print("❌ Table 'users' non trouvée")
            return False
        
        # Chercher le professeur salmane
        cursor.execute("SELECT id, username, email FROM users WHERE username = 'salmane' AND role = 'teacher'")
        teacher = cursor.fetchone()
        
        if teacher:
            teacher_id, username, email = teacher
            print(f"✅ Professeur trouvé: {email}")
            
            # Générer le bon hash bcrypt
            correct_password_hash = get_password_hash("salmane123@")
            
            cursor.execute("""
                UPDATE users 
                SET hashed_password = ?
                WHERE id = ?
            """, (correct_password_hash, teacher_id))
            
            conn.commit()
            print("✅ Mot de passe corrigé avec succès!")
            print(f"   📧 Email: {email}")
            print(f"   👤 Nom d'utilisateur: {username}")
            print(f"   🔑 Mot de passe: salmane123@")
            print(f"   🔐 Hash utilisé: bcrypt")
            
        else:
            print("❌ Professeur 'salmane' non trouvé")
            return False
        
        # Afficher tous les professeurs pour vérification
        print("\n📋 Liste de tous les professeurs:")
        cursor.execute("SELECT id, username, email FROM users WHERE role = 'teacher'")
        teachers = cursor.fetchall()
        for teacher_id, username, email in teachers:
            print(f"   • {username} ({email}) - ID: {teacher_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction du mot de passe: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    success = fix_teacher_password_bcrypt()
    if success:
        print("\n🎉 Correction terminée avec succès!")
        print("   Vous pouvez maintenant vous connecter avec:")
        print("   📧 Email: marie.dubois@najah.ai")
        print("   🔑 Mot de passe: salmane123@")
    else:
        print("\n❌ Échec de la correction") 