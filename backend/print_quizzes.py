from sqlalchemy import create_engine, text

# Chemin utilisé par le backend (adapter si besoin)
DATABASE_URL = "sqlite:///../data/app.db"

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    result = conn.execute(text("SELECT id, title, created_by, created_at FROM quizzes"))
    print("id | title | created_by | created_at")
    print("-" * 60)
    for row in result:
        print(f"{row.id} | {row.title} | {row.created_by} | {row.created_at}")