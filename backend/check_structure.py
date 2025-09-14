#!/usr/bin/env python3
import sqlite3

print("=== VÉRIFICATION STRUCTURE ===")

db_path = "../data/app.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Vérifier la structure de la table questions
cursor.execute("PRAGMA table_info(questions);")
columns = cursor.fetchall()
print("📋 Structure table questions:")
for col in columns:
    print(f"  - {col[1]} ({col[2]})")

# Vérifier la structure de la table quizzes
cursor.execute("PRAGMA table_info(quizzes);")
columns = cursor.fetchall()
print("\n📋 Structure table quizzes:")
for col in columns:
    print(f"  - {col[1]} ({col[2]})")

# Vérifier les données existantes
cursor.execute("SELECT COUNT(*) FROM questions;")
question_count = cursor.fetchone()[0]
print(f"\n❓ Questions existantes: {question_count}")

cursor.execute("SELECT COUNT(*) FROM quizzes;")
quiz_count = cursor.fetchone()[0]
print(f"📝 Quizzes existants: {quiz_count}")

conn.close()
print("\n✅ Vérification terminée") 