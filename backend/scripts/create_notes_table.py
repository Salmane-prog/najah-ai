#!/usr/bin/env python3
"""
Script pour créer la table notes dans la base de données
"""

import sqlite3
import os
from pathlib import Path

def create_notes_table():
    """Créer la table notes dans la base de données."""
    
    # Chemin vers la base de données
    db_path = Path(__file__).parent.parent / "data" / "app.db"
    
    print(f"📁 Base de données: {db_path}")
    
    if not db_path.exists():
        print("❌ Base de données non trouvée!")
        return False
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 Vérification de l'existence de la table notes...")
        
        # Vérifier si la table existe déjà
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='notes'
        """)
        
        if cursor.fetchone():
            print("✅ Table 'notes' existe déjà!")
            return True
        
        print("📝 Création de la table 'notes'...")
        
        # Créer la table notes
        cursor.execute("""
            CREATE TABLE notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title VARCHAR(255) NOT NULL,
                content TEXT,
                subject VARCHAR(100),
                content_id INTEGER,
                tags TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (content_id) REFERENCES contents (id)
            )
        """)
        
        # Créer un index pour améliorer les performances
        cursor.execute("""
            CREATE INDEX idx_notes_user_id ON notes (user_id)
        """)
        
        cursor.execute("""
            CREATE INDEX idx_notes_subject ON notes (subject)
        """)
        
        cursor.execute("""
            CREATE INDEX idx_notes_created_at ON notes (created_at)
        """)
        
        # Valider les changements
        conn.commit()
        
        print("✅ Table 'notes' créée avec succès!")
        print("✅ Index créés pour optimiser les performances")
        
        # Vérifier la création
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='notes'
        """)
        
        if cursor.fetchone():
            print("✅ Vérification réussie: la table existe!")
            
            # Afficher la structure de la table
            cursor.execute("PRAGMA table_info(notes)")
            columns = cursor.fetchall()
            
            print("\n📋 Structure de la table 'notes':")
            print("┌─────┬─────────────┬─────────────┬─────┬─────────┬─────┐")
            print("│ cid │    name     │    type     │ not │  dflt   │ pk  │")
            print("├─────┼─────────────┼─────────────┼─────┼─────────┼─────┤")
            
            for col in columns:
                cid, name, type_, not_null, default, pk = col
                print(f"│ {cid:3} │ {name:11} │ {type_:11} │ {not_null:3} │ {default or 'NULL':7} │ {pk:3} │")
            
            print("└─────┴─────────────┴─────────────┴─────┴─────────┴─────┘")
            
        else:
            print("❌ Erreur: la table n'a pas été créée!")
            return False
            
    except sqlite3.Error as e:
        print(f"❌ Erreur SQLite: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False
    finally:
        if conn:
            conn.close()
    
    return True

def insert_sample_notes():
    """Insérer quelques notes d'exemple."""
    
    db_path = Path(__file__).parent.parent / "data" / "app.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("\n📝 Insertion de notes d'exemple...")
        
        # Récupérer un utilisateur étudiant
        cursor.execute("SELECT id FROM users WHERE role = 'student' LIMIT 1")
        student = cursor.fetchone()
        
        if not student:
            print("⚠️ Aucun étudiant trouvé, impossible d'insérer des notes d'exemple")
            return
        
        student_id = student[0]
        
        # Notes d'exemple
        sample_notes = [
            {
                "title": "Théorème de Pythagore",
                "content": """# Théorème de Pythagore

## Définition
Dans un triangle rectangle, le carré de l'hypoténuse est égal à la somme des carrés des deux autres côtés.

## Formule
a² + b² = c²

## Exemple
Si a = 3 et b = 4, alors c = 5 car 3² + 4² = 9 + 16 = 25 = 5²

## Applications
- Calcul de distances
- Architecture
- Navigation""",
                "subject": "Mathématiques",
                "tags": ["géométrie", "théorème", "triangle"]
            },
            {
                "title": "Règles de conjugaison",
                "content": """# Conjugaison française

## Présent de l'indicatif

### 1er groupe (-er)
- Je parle
- Tu parles
- Il/Elle parle
- Nous parlons
- Vous parlez
- Ils/Elles parlent

### 2ème groupe (-ir)
- Je finis
- Tu finis
- Il/Elle finit
- Nous finissons
- Vous finissez
- Ils/Elles finissent

## Exceptions importantes
- Aller: je vais, tu vas, il va...
- Être: je suis, tu es, il est...""",
                "subject": "Français",
                "tags": ["conjugaison", "grammaire", "présent"]
            },
            {
                "title": "Photosynthèse",
                "content": """# Photosynthèse

## Définition
Processus par lequel les plantes convertissent la lumière solaire en énergie chimique.

## Équation
6CO₂ + 6H₂O + lumière → C₆H₁₂O₆ + 6O₂

## Étapes principales
1. **Absorption de lumière** par la chlorophylle
2. **Réaction photochimique** dans les thylakoïdes
3. **Cycle de Calvin** dans le stroma
4. **Production de glucose** et d'oxygène

## Facteurs influençant la photosynthèse
- Intensité lumineuse
- Concentration en CO₂
- Température
- Disponibilité en eau""",
                "subject": "Sciences",
                "tags": ["biologie", "plantes", "énergie"]
            }
        ]
        
        for i, note in enumerate(sample_notes, 1):
            cursor.execute("""
                INSERT INTO notes (user_id, title, content, subject, tags, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, datetime('now'), datetime('now'))
            """, (
                student_id,
                note["title"],
                note["content"],
                note["subject"],
                ",".join(note["tags"])
            ))
            print(f"✅ Note {i} insérée: {note['title']}")
        
        conn.commit()
        print(f"✅ {len(sample_notes)} notes d'exemple insérées avec succès!")
        
    except sqlite3.Error as e:
        print(f"❌ Erreur lors de l'insertion des notes: {e}")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("🚀 CRÉATION DE LA TABLE NOTES")
    print("=" * 50)
    
    if create_notes_table():
        print("\n" + "=" * 50)
        insert_sample_notes()
        print("\n🎉 MIGRATION TERMINÉE AVEC SUCCÈS!")
    else:
        print("\n❌ ÉCHEC DE LA MIGRATION!") 