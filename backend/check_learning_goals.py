from core.database import engine
from sqlalchemy import text

def check_learning_goals():
    conn = engine.connect()
    try:
        # Vérifier tous les objectifs d'apprentissage
        result = conn.execute(text('SELECT id, title, user_id, created_at FROM learning_goals ORDER BY id DESC LIMIT 10'))
        goals = result.fetchall()
        
        print(f'Objectifs d\'apprentissage trouvés: {len(goals)}')
        for goal in goals:
            print(f'  - ID: {goal[0]}, Titre: {goal[1]}, User ID: {goal[2]}, Créé: {goal[3]}')
        
        # Vérifier l'utilisateur connecté
        result = conn.execute(text('SELECT id, email, username, role FROM users WHERE email = "salmane.hajouji@najah.ai"'))
        user = result.fetchone()
        
        if user:
            print(f'\nUtilisateur connecté:')
            print(f'  - ID: {user[0]}, Email: {user[1]}, Username: {user[2]}, Role: {user[3]}')
            
            # Vérifier les objectifs de cet utilisateur
            result = conn.execute(text('SELECT id, title, user_id FROM learning_goals WHERE user_id = :user_id'), {"user_id": user[0]})
            user_goals = result.fetchall()
            
            print(f'\nObjectifs de l\'utilisateur {user[0]}: {len(user_goals)}')
            for goal in user_goals:
                print(f'  - ID: {goal[0]}, Titre: {goal[1]}, User ID: {goal[2]}')
        else:
            print('\nUtilisateur non trouvé')
        
        return goals
    finally:
        conn.close()

if __name__ == "__main__":
    check_learning_goals()
