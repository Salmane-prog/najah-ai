#!/usr/bin/env python3
"""
Script pour vérifier le hash actuel
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text

def check_hash():
    """Vérifier le hash actuel"""
    
    engine = create_engine("sqlite:///../data/app.db")
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT hashed_password FROM users 
                WHERE email = 'salmane.hajouji@najah.ai'
            """))
            
            user = result.fetchone()
            
            if user:
                print(f"Hash actuel: {user[0][:50]}...")
            else:
                print("Utilisateur non trouvé")
            
    except Exception as e:
        print(f"Erreur: {str(e)}")

if __name__ == "__main__":
    check_hash() 