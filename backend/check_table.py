from core.database import engine
from sqlalchemy import text

def check_table():
    conn = engine.connect()
    try:
        result = conn.execute(text('SELECT name FROM sqlite_master WHERE type="table" AND name="learning_goals"'))
        exists = result.fetchone() is not None
        print(f'Table learning_goals exists: {exists}')
        
        if exists:
            # Vérifier la structure de la table
            result = conn.execute(text('PRAGMA table_info(learning_goals)'))
            columns = result.fetchall()
            print(f'Columns in learning_goals: {[col[1] for col in columns]}')
            
            # Vérifier s'il y a des données
            result = conn.execute(text('SELECT COUNT(*) FROM learning_goals'))
            count = result.fetchone()[0]
            print(f'Number of records in learning_goals: {count}')
        
        return exists
    finally:
        conn.close()

if __name__ == "__main__":
    check_table()


