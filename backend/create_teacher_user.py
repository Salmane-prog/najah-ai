#!/usr/bin/env python3
"""
Script pour créer un utilisateur professeur avec un mot de passe connu
"""

import sqlite3
from passlib.context import CryptContext
from datetime import datetime

def create_teacher_user():
    """Créer un utilisateur professeur avec un mot de passe connu"""
    
    # Configuration du hashage de mot de passe
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    # Connexion à la base de données
    conn = sqlite3.connect('F:/IMT/stage/Yancode/Najah__AI/data/app.db')
    cursor = conn.cursor()
    
    # Vérifier si l'utilisateur existe déjà
    cursor.execute('SELECT id FROM users WHERE email = ?', ('test_teacher@najah.ai',))
    existing_user = cursor.fetchone()
    
    if existing_user:
        print('👤 Utilisateur test_teacher@najah.ai existe déjà')
        # Mettre à jour le mot de passe
        password_hash = pwd_context.hash('test123')
        cursor.execute('''
            UPDATE users 
            SET hashed_password = ?, updated_at = ?
            WHERE email = ?
        ''', (password_hash, datetime.utcnow().isoformat(), 'test_teacher@najah.ai'))
        print('✅ Mot de passe mis à jour')
    else:
        # Créer un nouvel utilisateur
        password_hash = pwd_context.hash('test123')
        cursor.execute('''
            INSERT INTO users (username, email, hashed_password, role, is_active, first_name, last_name, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            'test_teacher',
            'test_teacher@najah.ai',
            password_hash,
            'teacher',
            1,
            'Test',
            'Teacher',
            datetime.utcnow().isoformat()
        ))
        print('✅ Nouvel utilisateur créé')
    
    # Vérifier la création
    cursor.execute('SELECT id, email, username, role FROM users WHERE email = ?', ('test_teacher@najah.ai',))
    user = cursor.fetchone()
    
    if user:
        print(f'👤 Utilisateur créé:')
        print(f'   ID: {user[0]}')
        print(f'   Email: {user[1]}')
        print(f'   Username: {user[2]}')
        print(f'   Role: {user[3]}')
        print(f'   Mot de passe: test123')
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_teacher_user()








