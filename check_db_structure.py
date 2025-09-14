#!/usr/bin/env python3
import sqlite3

# Connexion à la base
conn = sqlite3.connect('data/app.db')
cursor = conn.cursor()

# Vérifier la structure de question_history
print("=== STRUCTURE DE question_history ===")
cursor.execute('PRAGMA table_info(question_history)')
columns = cursor.fetchall()
print("Colonnes:")
for col in columns:
    print(f"  {col[0]}: {col[1]} ({col[2]})")

# Vérifier les données
print("\n=== DONNÉES DE question_history ===")
cursor.execute('SELECT * FROM question_history LIMIT 1')
row = cursor.fetchone()
if row:
    print("Première ligne:")
    for i, val in enumerate(row):
        print(f"  {i}: {val}")

# Vérifier french_adaptive_tests
print("\n=== STRUCTURE DE french_adaptive_tests ===")
cursor.execute('PRAGMA table_info(french_adaptive_tests)')
columns = cursor.fetchall()
for col in columns:
    print(f"  {col[1]} ({col[2]})")

conn.close()
