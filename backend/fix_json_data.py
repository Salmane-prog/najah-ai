#!/usr/bin/env python3
"""
Script pour corriger les données JSON invalides dans la base de données
"""

import sys
import os
import json
import sqlite3
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import get_db
from models.quiz import Question, Quiz
from sqlalchemy.orm import Session

def fix_json_data():
    print("=== CORRECTION DES DONNÉES JSON ===")
    
    # Connexion directe à SQLite pour inspection
    db_path = "../data/app.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print(f"📊 Inspection de la base de données: {db_path}")
    
    # Vérifier les tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"Tables trouvées: {[table[0] for table in tables]}")
    
    # Vérifier les questions avec des données JSON
    print("\n🔍 Inspection des questions...")
    cursor.execute("SELECT id, question_text, options, correct_answer FROM questions LIMIT 10;")
    questions = cursor.fetchall()
    
    for q in questions:
        print(f"Question {q[0]}: {q[1][:50]}...")
        print(f"  Options: {q[2]}")
        print(f"  Correct: {q[3]}")
        
        # Tester le parsing JSON
        try:
            if q[2]:
                options = json.loads(q[2])
                print(f"  ✅ Options JSON valides")
        except json.JSONDecodeError as e:
            print(f"  ❌ Options JSON invalides: {e}")
            # Corriger les options
            if q[2] and q[2].strip():
                try:
                    # Essayer de corriger
                    fixed_options = q[2].replace("'", '"')
                    json.loads(fixed_options)
                    print(f"  🔧 Correction possible")
                    
                    # Mettre à jour la base
                    cursor.execute(
                        "UPDATE questions SET options = ? WHERE id = ?",
                        (fixed_options, q[0])
                    )
                    print(f"  ✅ Question {q[0]} corrigée")
                except:
                    print(f"  ❌ Impossible de corriger")
        
        try:
            if q[3]:
                correct = json.loads(q[3])
                print(f"  ✅ Correct JSON valide")
        except json.JSONDecodeError as e:
            print(f"  ❌ Correct JSON invalide: {e}")
    
    conn.commit()
    conn.close()
    
    print("\n✅ Correction terminée")

if __name__ == "__main__":
    fix_json_data() 