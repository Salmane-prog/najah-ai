import sqlite3

# Connexion à la base de données
conn = sqlite3.connect('data/app.db')
cursor = conn.cursor()

print("📊 Utilisateurs existants dans la base de données:")
print("=" * 50)

# Récupérer tous les utilisateurs
cursor.execute('SELECT id, username, email, role FROM users ORDER BY role, username')
users = cursor.fetchall()

for user in users:
    print(f"ID: {user[0]:<3} | Username: {user[1]:<15} | Email: {user[2]:<25} | Role: {user[3]}")

print("\n🔍 Utilisateurs professeur:")
print("-" * 30)
cursor.execute('SELECT id, username, email, role FROM users WHERE role = "teacher"')
teachers = cursor.fetchall()

for teacher in teachers:
    print(f"ID: {teacher[0]:<3} | Username: {teacher[1]:<15} | Email: {teacher[2]:<25} | Role: {teacher[3]}")

conn.close() 