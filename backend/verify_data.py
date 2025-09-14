#!/usr/bin/env python3
import sqlite3

print("=== VÉRIFICATION DES DONNÉES ===")

db_path = "../data/app.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Vérifier les catégories
cursor.execute("SELECT COUNT(*) FROM categories;")
cat_count = cursor.fetchone()[0]
print(f"📚 Catégories: {cat_count}")

cursor.execute("SELECT name FROM categories LIMIT 5;")
categories = cursor.fetchall()
for cat in categories:
    print(f"  - {cat[0]}")

# Vérifier les quizzes
cursor.execute("SELECT COUNT(*) FROM quizzes;")
quiz_count = cursor.fetchone()[0]
print(f"\n📝 Quizzes: {quiz_count}")

cursor.execute("SELECT title, subject, level FROM quizzes LIMIT 5;")
quizzes = cursor.fetchall()
for quiz in quizzes:
    print(f"  - {quiz[0]} ({quiz[1]} - {quiz[2]})")

# Vérifier les questions
cursor.execute("SELECT COUNT(*) FROM questions;")
question_count = cursor.fetchone()[0]
print(f"\n❓ Questions: {question_count}")

cursor.execute("SELECT question_text, difficulty FROM questions LIMIT 3;")
questions = cursor.fetchall()
for q in questions:
    print(f"  - {q[0][:50]}... ({q[1]})")

conn.close()
print("\n✅ Vérification terminée") 