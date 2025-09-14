import sqlite3

# Connexion à la base de données
conn = sqlite3.connect('data/app.db')
cursor = conn.cursor()

# Vérifier l'utilisateur superadmin
cursor.execute('SELECT id, email, role FROM users WHERE email = "superadmin@najah.ai"')
result = cursor.fetchone()

if result:
    print(f"User ID: {result[0]}")
    print(f"Email: {result[1]}")
    print(f"Role: {result[2]}")
else:
    print("Utilisateur non trouvé")

# Vérifier tous les utilisateurs admin
cursor.execute('SELECT id, email, role FROM users WHERE role = "admin"')
admin_users = cursor.fetchall()
print(f"\nUtilisateurs admin: {len(admin_users)}")
for user in admin_users:
    print(f"- {user[1]} (ID: {user[0]}, Role: {user[2]})")

conn.close() 