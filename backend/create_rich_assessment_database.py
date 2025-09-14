#!/usr/bin/env python3
"""
Script pour créer une base de données riche avec des questions d'évaluation initiale
pour Najah AI - Évaluation des connaissances des étudiants
"""

import sqlite3
import os
from datetime import datetime, timedelta
import random

def create_database():
    """Créer la base de données avec toutes les tables nécessaires"""
    
    # Créer le dossier data s'il n'existe pas
    os.makedirs('./data', exist_ok=True)
    
    conn = sqlite3.connect('./data/app.db')
    cursor = conn.cursor()
    
    # Table des catégories de questions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS question_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            difficulty_level TEXT CHECK(difficulty_level IN ('débutant', 'intermédiaire', 'avancé')),
            subject_area TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table des questions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assessment_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER,
            question_text TEXT NOT NULL,
            question_type TEXT CHECK(question_type IN ('QCM', 'vrai_faux', 'texte_libre', 'association', 'ordre')),
            difficulty_level TEXT CHECK(difficulty_level IN ('débutant', 'intermédiaire', 'avancé')),
            points INTEGER DEFAULT 1,
            time_limit INTEGER DEFAULT 60,
            explanation TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES question_categories (id)
        )
    ''')
    
    # Table des réponses pour les questions QCM
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS question_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER,
            answer_text TEXT NOT NULL,
            is_correct BOOLEAN DEFAULT FALSE,
            order_index INTEGER DEFAULT 0,
            FOREIGN KEY (question_id) REFERENCES assessment_questions (id)
        )
    ''')
    
    # Table des évaluations
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            category_id INTEGER,
            total_points INTEGER DEFAULT 0,
            time_limit INTEGER DEFAULT 0,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES question_categories (id)
        )
    ''')
    
    # Table de liaison entre évaluations et questions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assessment_questions_link (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            assessment_id INTEGER,
            question_id INTEGER,
            order_index INTEGER DEFAULT 0,
            FOREIGN KEY (assessment_id) REFERENCES assessments (id),
            FOREIGN KEY (question_id) REFERENCES assessment_questions (id)
        )
    ''')
    
    # Table des résultats d'évaluation des étudiants
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_assessment_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            assessment_id INTEGER,
            score INTEGER DEFAULT 0,
            total_possible INTEGER DEFAULT 0,
            percentage REAL DEFAULT 0.0,
            time_taken INTEGER DEFAULT 0,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES users (id),
            FOREIGN KEY (assessment_id) REFERENCES assessments (id)
        )
    ''')
    
    # Table des réponses des étudiants
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            question_id INTEGER,
            assessment_id INTEGER,
            answer_text TEXT,
            selected_answer_id INTEGER,
            is_correct BOOLEAN,
            points_earned INTEGER DEFAULT 0,
            answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES users (id),
            FOREIGN KEY (question_id) REFERENCES assessment_questions (id),
            FOREIGN KEY (assessment_id) REFERENCES assessments (id),
            FOREIGN KEY (selected_answer_id) REFERENCES question_answers (id)
        )
    ''')
    
    conn.commit()
    return conn, cursor

def insert_categories(cursor):
    """Insérer les catégories de questions"""
    
    categories = [
        ('Mathématiques', 'Questions de mathématiques de base à avancées', 'débutant', 'Mathématiques'),
        ('Français', 'Grammaire, vocabulaire et compréhension', 'débutant', 'Langues'),
        ('Sciences', 'Concepts scientifiques fondamentaux', 'débutant', 'Sciences'),
        ('Histoire', 'Événements historiques importants', 'débutant', 'Sciences humaines'),
        ('Géographie', 'Connaissance du monde et des pays', 'débutant', 'Sciences humaines'),
        ('Logique', 'Raisonnement logique et résolution de problèmes', 'intermédiaire', 'Compétences cognitives'),
        ('Culture générale', 'Connaissances générales variées', 'intermédiaire', 'Culture générale'),
        ('Technologie', 'Concepts technologiques de base', 'intermédiaire', 'Technologie'),
        ('Arts', 'Histoire de l\'art et culture artistique', 'intermédiaire', 'Arts'),
        ('Philosophie', 'Pensée critique et réflexion philosophique', 'avancé', 'Philosophie')
    ]
    
    for category in categories:
        cursor.execute('''
            INSERT INTO question_categories (name, description, difficulty_level, subject_area)
            VALUES (?, ?, ?, ?)
        ''', category)
    
    print(f"✅ {len(categories)} catégories insérées")

def insert_math_questions(cursor):
    """Insérer des questions de mathématiques"""
    
    # Récupérer l'ID de la catégorie Mathématiques
    cursor.execute("SELECT id FROM question_categories WHERE name = 'Mathématiques'")
    math_category_id = cursor.fetchone()[0]
    
    math_questions = [
        {
            'question': 'Quel est le résultat de 15 + 27 ?',
            'type': 'QCM',
            'difficulty': 'débutant',
            'points': 1,
            'answers': [
                ('42', True),
                ('40', False),
                ('43', False),
                ('41', False)
            ]
        },
        {
            'question': 'Quel est le résultat de 8 × 7 ?',
            'type': 'QCM',
            'difficulty': 'débutant',
            'points': 1,
            'answers': [
                ('56', True),
                ('54', False),
                ('58', False),
                ('52', False)
            ]
        },
        {
            'question': 'Quel est le résultat de 100 ÷ 4 ?',
            'type': 'QCM',
            'difficulty': 'débutant',
            'points': 1,
            'answers': [
                ('25', True),
                ('20', False),
                ('30', False),
                ('15', False)
            ]
        },
        {
            'question': 'Quel est le carré de 9 ?',
            'type': 'QCM',
            'difficulty': 'intermédiaire',
            'points': 2,
            'answers': [
                ('81', True),
                ('72', False),
                ('90', False),
                ('64', False)
            ]
        },
        {
            'question': 'Quel est le résultat de 3² + 4² ?',
            'type': 'QCM',
            'difficulty': 'intermédiaire',
            'points': 2,
            'answers': [
                ('25', True),
                ('7', False),
                ('49', False),
                ('12', False)
            ]
        },
        {
            'question': 'Quel est le périmètre d\'un carré de côté 6 cm ?',
            'type': 'QCM',
            'difficulty': 'intermédiaire',
            'points': 2,
            'answers': [
                ('24 cm', True),
                ('36 cm', False),
                ('12 cm', False),
                ('18 cm', False)
            ]
        },
        {
            'question': 'Quel est l\'aire d\'un rectangle de longueur 8 cm et largeur 5 cm ?',
            'type': 'QCM',
            'difficulty': 'intermédiaire',
            'points': 2,
            'answers': [
                ('40 cm²', True),
                ('26 cm²', False),
                ('13 cm²', False),
                ('20 cm²', False)
            ]
        },
        {
            'question': 'Quel est le résultat de √16 ?',
            'type': 'QCM',
            'difficulty': 'intermédiaire',
            'points': 2,
            'answers': [
                ('4', True),
                ('8', False),
                ('2', False),
                ('16', False)
            ]
        },
        {
            'question': 'Quel est le résultat de 2³ × 2² ?',
            'type': 'QCM',
            'difficulty': 'avancé',
            'points': 3,
            'answers': [
                ('32', True),
                ('64', False),
                ('16', False),
                ('8', False)
            ]
        },
        {
            'question': 'Quel est le résultat de (5 + 3) × 2 ?',
            'type': 'QCM',
            'difficulty': 'avancé',
            'points': 3,
            'answers': [
                ('16', True),
                ('13', False),
                ('11', False),
                ('20', False)
            ]
        }
    ]
    
    for q_data in math_questions:
        # Insérer la question
        cursor.execute('''
            INSERT INTO assessment_questions (category_id, question_text, question_type, difficulty_level, points)
            VALUES (?, ?, ?, ?, ?)
        ''', (math_category_id, q_data['question'], q_data['type'], q_data['difficulty'], q_data['points']))
        
        question_id = cursor.lastrowid
        
        # Insérer les réponses
        for i, (answer_text, is_correct) in enumerate(q_data['answers']):
            cursor.execute('''
                INSERT INTO question_answers (question_id, answer_text, is_correct, order_index)
                VALUES (?, ?, ?, ?)
            ''', (question_id, answer_text, is_correct, i))
    
    print(f"✅ {len(math_questions)} questions de mathématiques insérées")

def insert_french_questions(cursor):
    """Insérer des questions de français"""
    
    cursor.execute("SELECT id FROM question_categories WHERE name = 'Français'")
    french_category_id = cursor.fetchone()[0]
    
    french_questions = [
        {
            'question': 'Quel est le pluriel de "cheval" ?',
            'type': 'QCM',
            'difficulty': 'débutant',
            'points': 1,
            'answers': [
                ('chevaux', True),
                ('chevals', False),
                ('chevales', False),
                ('chevalx', False)
            ]
        },
        {
            'question': 'Quel est le féminin de "beau" ?',
            'type': 'QCM',
            'difficulty': 'débutant',
            'points': 1,
            'answers': [
                ('belle', True),
                ('beau', False),
                ('beaux', False),
                ('belles', False)
            ]
        },
        {
            'question': 'Quel est le temps du verbe dans "Il mangeait" ?',
            'type': 'QCM',
            'difficulty': 'intermédiaire',
            'points': 2,
            'answers': [
                ('Imparfait', True),
                ('Présent', False),
                ('Futur', False),
                ('Passé composé', False)
            ]
        },
        {
            'question': 'Quel est le synonyme de "rapidement" ?',
            'type': 'QCM',
            'difficulty': 'intermédiaire',
            'points': 2,
            'answers': [
                ('vite', True),
                ('lentement', False),
                ('doucement', False),
                ('fortement', False)
            ]
        },
        {
            'question': 'Quel est l\'antonyme de "grand" ?',
            'type': 'QCM',
            'difficulty': 'débutant',
            'points': 1,
            'answers': [
                ('petit', True),
                ('moyen', False),
                ('large', False),
                ('haut', False)
            ]
        },
        {
            'question': 'Quel est le genre du mot "table" ?',
            'type': 'QCM',
            'difficulty': 'débutant',
            'points': 1,
            'answers': [
                ('féminin', True),
                ('masculin', False),
                ('neutre', False),
                ('commun', False)
            ]
        },
        {
            'question': 'Quel est le nombre du mot "yeux" ?',
            'type': 'QCM',
            'difficulty': 'débutant',
            'points': 1,
            'answers': [
                ('pluriel', True),
                ('singulier', False),
                ('duel', False),
                ('neutre', False)
            ]
        },
        {
            'question': 'Quel est le temps du verbe dans "J\'aurai fini" ?',
            'type': 'QCM',
            'difficulty': 'avancé',
            'points': 3,
            'answers': [
                ('Futur antérieur', True),
                ('Futur simple', False),
                ('Conditionnel présent', False),
                ('Subjonctif présent', False)
            ]
        },
        {
            'question': 'Quel est le mode du verbe dans "Qu\'il vienne" ?',
            'type': 'QCM',
            'difficulty': 'avancé',
            'points': 3,
            'answers': [
                ('Subjonctif', True),
                ('Indicatif', False),
                ('Conditionnel', False),
                ('Impératif', False)
            ]
        },
        {
            'question': 'Quel est le complément dans "Il mange une pomme" ?',
            'type': 'QCM',
            'difficulty': 'intermédiaire',
            'points': 2,
            'answers': [
                ('une pomme', True),
                ('Il', False),
                ('mange', False),
                ('Il mange', False)
            ]
        }
    ]
    
    for q_data in french_questions:
        cursor.execute('''
            INSERT INTO assessment_questions (category_id, question_text, question_type, difficulty_level, points)
            VALUES (?, ?, ?, ?, ?)
        ''', (french_category_id, q_data['question'], q_data['type'], q_data['difficulty'], q_data['points']))
        
        question_id = cursor.lastrowid
        
        for i, (answer_text, is_correct) in enumerate(q_data['answers']):
            cursor.execute('''
                INSERT INTO question_answers (question_id, answer_text, is_correct, order_index)
                VALUES (?, ?, ?, ?)
            ''', (question_id, answer_text, is_correct, i))
    
    print(f"✅ {len(french_questions)} questions de français insérées")

def insert_science_questions(cursor):
    """Insérer des questions de sciences"""
    
    cursor.execute("SELECT id FROM question_categories WHERE name = 'Sciences'")
    science_category_id = cursor.fetchone()[0]
    
    science_questions = [
        {
            'question': 'Quel est le symbole chimique de l\'oxygène ?',
            'type': 'QCM',
            'difficulty': 'débutant',
            'points': 1,
            'answers': [
                ('O', True),
                ('Ox', False),
                ('O2', False),
                ('Oxy', False)
            ]
        },
        {
            'question': 'Quel est le symbole chimique de l\'hydrogène ?',
            'type': 'QCM',
            'difficulty': 'débutant',
            'points': 1,
            'answers': [
                ('H', True),
                ('Hy', False),
                ('H2', False),
                ('Hyd', False)
            ]
        },
        {
            'question': 'Quel est le symbole chimique du carbone ?',
            'type': 'QCM',
            'difficulty': 'débutant',
            'points': 1,
            'answers': [
                ('C', True),
                ('Ca', False),
                ('Co', False),
                ('Cr', False)
            ]
        },
        {
            'question': 'Quel est le symbole chimique de l\'azote ?',
            'type': 'QCM',
            'difficulty': 'débutant',
            'points': 1,
            'answers': [
                ('N', True),
                ('Az', False),
                ('Ni', False),
                ('Ne', False)
            ]
        },
        {
            'question': 'Quel est le symbole chimique du fer ?',
            'type': 'QCM',
            'difficulty': 'intermédiaire',
            'points': 2,
            'answers': [
                ('Fe', True),
                ('Ir', False),
                ('Fr', False),
                ('F', False)
            ]
        },
        {
            'question': 'Quel est le symbole chimique de l\'or ?',
            'type': 'QCM',
            'difficulty': 'intermédiaire',
            'points': 2,
            'answers': [
                ('Au', True),
                ('Or', False),
                ('Ag', False),
                ('G', False)
            ]
        },
        {
            'question': 'Quel est le symbole chimique de l\'argent ?',
            'type': 'QCM',
            'difficulty': 'intermédiaire',
            'points': 2,
            'answers': [
                ('Ag', True),
                ('Ar', False),
                ('Au', False),
                ('S', False)
            ]
        },
        {
            'question': 'Quel est le symbole chimique du cuivre ?',
            'type': 'QCM',
            'difficulty': 'intermédiaire',
            'points': 2,
            'answers': [
                ('Cu', True),
                ('Co', False),
                ('Ca', False),
                ('C', False)
            ]
        },
        {
            'question': 'Quel est le symbole chimique du zinc ?',
            'type': 'QCM',
            'difficulty': 'intermédiaire',
            'points': 2,
            'answers': [
                ('Zn', True),
                ('Zr', False),
                ('Z', False),
                ('Zi', False)
            ]
        },
        {
            'question': 'Quel est le symbole chimique du plomb ?',
            'type': 'QCM',
            'difficulty': 'avancé',
            'points': 3,
            'answers': [
                ('Pb', True),
                ('Pl', False),
                ('P', False),
                ('Po', False)
            ]
        }
    ]
    
    for q_data in science_questions:
        cursor.execute('''
            INSERT INTO assessment_questions (category_id, question_text, question_type, difficulty_level, points)
            VALUES (?, ?, ?, ?, ?)
        ''', (science_category_id, q_data['question'], q_data['type'], q_data['difficulty'], q_data['points']))
        
        question_id = cursor.lastrowid
        
        for i, (answer_text, is_correct) in enumerate(q_data['answers']):
            cursor.execute('''
                INSERT INTO question_answers (question_id, answer_text, is_correct, order_index)
                VALUES (?, ?, ?, ?)
            ''', (question_id, answer_text, is_correct, i))
    
    print(f"✅ {len(science_questions)} questions de sciences insérées")

def insert_history_questions(cursor):
    """Insérer des questions d'histoire"""
    
    cursor.execute("SELECT id FROM question_categories WHERE name = 'Histoire'")
    history_category_id = cursor.fetchone()[0]
    
    history_questions = [
        {
            'question': 'En quelle année a eu lieu la Révolution française ?',
            'type': 'QCM',
            'difficulty': 'débutant',
            'points': 1,
            'answers': [
                ('1789', True),
                ('1799', False),
                ('1779', False),
                ('1809', False)
            ]
        },
        {
            'question': 'Quel roi de France était surnommé le "Roi Soleil" ?',
            'type': 'QCM',
            'difficulty': 'débutant',
            'points': 1,
            'answers': [
                ('Louis XIV', True),
                ('Louis XIII', False),
                ('Louis XV', False),
                ('Louis XVI', False)
            ]
        },
        {
            'question': 'En quelle année a eu lieu la Première Guerre mondiale ?',
            'type': 'QCM',
            'difficulty': 'débutant',
            'points': 1,
            'answers': [
                ('1914-1918', True),
                ('1918-1922', False),
                ('1910-1914', False),
                ('1916-1920', False)
            ]
        },
        {
            'question': 'Quel était le nom de la reine d\'Égypte célèbre pour sa beauté ?',
            'type': 'QCM',
            'difficulty': 'intermédiaire',
            'points': 2,
            'answers': [
                ('Cléopâtre', True),
                ('Néfertiti', False),
                ('Hatchepsout', False),
                ('Isis', False)
            ]
        },
        {
            'question': 'Quel empereur romain a construit le Colisée ?',
            'type': 'QCM',
            'difficulty': 'intermédiaire',
            'points': 2,
            'answers': [
                ('Vespasien', True),
                ('Néron', False),
                ('Auguste', False),
                ('Trajan', False)
            ]
        },
        {
            'question': 'En quelle année Christophe Colomb a-t-il découvert l\'Amérique ?',
            'type': 'QCM',
            'difficulty': 'débutant',
            'points': 1,
            'answers': [
                ('1492', True),
                ('1498', False),
                ('1488', False),
                ('1500', False)
            ]
        },
        {
            'question': 'Quel était le nom de la première femme dans l\'espace ?',
            'type': 'QCM',
            'difficulty': 'intermédiaire',
            'points': 2,
            'answers': [
                ('Valentina Terechkova', True),
                ('Sally Ride', False),
                ('Mae Jemison', False),
                ('Eileen Collins', False)
            ]
        },
        {
            'question': 'En quelle année a eu lieu la chute du mur de Berlin ?',
            'type': 'QCM',
            'difficulty': 'intermédiaire',
            'points': 2,
            'answers': [
                ('1989', True),
                ('1987', False),
                ('1991', False),
                ('1985', False)
            ]
        },
        {
            'question': 'Quel était le nom du premier président des États-Unis ?',
            'type': 'QCM',
            'difficulty': 'débutant',
            'points': 1,
            'answers': [
                ('George Washington', True),
                ('Thomas Jefferson', False),
                ('John Adams', False),
                ('Benjamin Franklin', False)
            ]
        },
        {
            'question': 'En quelle année a eu lieu la Déclaration d\'indépendance des États-Unis ?',
            'type': 'QCM',
            'difficulty': 'intermédiaire',
            'points': 2,
            'answers': [
                ('1776', True),
                ('1783', False),
                ('1765', False),
                ('1789', False)
            ]
        }
    ]
    
    for q_data in history_questions:
        cursor.execute('''
            INSERT INTO assessment_questions (category_id, question_text, question_type, difficulty_level, points)
            VALUES (?, ?, ?, ?, ?)
        ''', (history_category_id, q_data['question'], q_data['type'], q_data['difficulty'], q_data['points']))
        
        question_id = cursor.lastrowid
        
        for i, (answer_text, is_correct) in enumerate(q_data['answers']):
            cursor.execute('''
                INSERT INTO question_answers (question_id, answer_text, is_correct, order_index)
                VALUES (?, ?, ?, ?)
            ''', (question_id, answer_text, is_correct, i))
    
    print(f"✅ {len(history_questions)} questions d'histoire insérées")

def insert_geography_questions(cursor):
    """Insérer des questions de géographie"""
    
    cursor.execute("SELECT id FROM question_categories WHERE name = 'Géographie'")
    geography_category_id = cursor.fetchone()[0]
    
    geography_questions = [
        {
            'question': 'Quelle est la capitale de la France ?',
            'type': 'QCM',
            'difficulty': 'débutant',
            'points': 1,
            'answers': [
                ('Paris', True),
                ('Lyon', False),
                ('Marseille', False),
                ('Toulouse', False)
            ]
        },
        {
            'question': 'Quel est le plus grand océan du monde ?',
            'type': 'QCM',
            'difficulty': 'débutant',
            'points': 1,
            'answers': [
                ('Océan Pacifique', True),
                ('Océan Atlantique', False),
                ('Océan Indien', False),
                ('Océan Arctique', False)
            ]
        },
        {
            'question': 'Quel est le plus haut sommet du monde ?',
            'type': 'QCM',
            'difficulty': 'débutant',
            'points': 1,
            'answers': [
                ('Mont Everest', True),
                ('Mont K2', False),
                ('Mont Kilimandjaro', False),
                ('Mont Blanc', False)
            ]
        },
        {
            'question': 'Quel est le plus long fleuve du monde ?',
            'type': 'QCM',
            'difficulty': 'intermédiaire',
            'points': 2,
            'answers': [
                ('Le Nil', True),
                ('L\'Amazone', False),
                ('Le Mississippi', False),
                ('Le Yangtsé', False)
            ]
        },
        {
            'question': 'Quelle est la capitale du Japon ?',
            'type': 'QCM',
            'difficulty': 'débutant',
            'points': 1,
            'answers': [
                ('Tokyo', True),
                ('Kyoto', False),
                ('Osaka', False),
                ('Yokohama', False)
            ]
        },
        {
            'question': 'Quel est le plus grand désert du monde ?',
            'type': 'QCM',
            'difficulty': 'intermédiaire',
            'points': 2,
            'answers': [
                ('Le Sahara', True),
                ('Le désert d\'Arabie', False),
                ('Le désert de Gobi', False),
                ('Le désert du Kalahari', False)
            ]
        },
        {
            'question': 'Quelle est la capitale de l\'Australie ?',
            'type': 'QCM',
            'difficulty': 'intermédiaire',
            'points': 2,
            'answers': [
                ('Canberra', True),
                ('Sydney', False),
                ('Melbourne', False),
                ('Brisbane', False)
            ]
        },
        {
            'question': 'Quel est le plus grand pays du monde en superficie ?',
            'type': 'QCM',
            'difficulty': 'intermédiaire',
            'points': 2,
            'answers': [
                ('La Russie', True),
                ('Le Canada', False),
                ('La Chine', False),
                ('Les États-Unis', False)
            ]
        },
        {
            'question': 'Quelle est la capitale du Brésil ?',
            'type': 'QCM',
            'difficulty': 'intermédiaire',
            'points': 2,
            'answers': [
                ('Brasília', True),
                ('Rio de Janeiro', False),
                ('São Paulo', False),
                ('Salvador', False)
            ]
        },
        {
            'question': 'Quel est le plus petit pays du monde ?',
            'type': 'QCM',
            'difficulty': 'avancé',
            'points': 3,
            'answers': [
                ('Le Vatican', True),
                ('Monaco', False),
                ('San Marino', False),
                ('Liechtenstein', False)
            ]
        }
    ]
    
    for q_data in geography_questions:
        cursor.execute('''
            INSERT INTO assessment_questions (category_id, question_text, question_type, difficulty_level, points)
            VALUES (?, ?, ?, ?, ?)
        ''', (geography_category_id, q_data['question'], q_data['type'], q_data['difficulty'], q_data['points']))
        
        question_id = cursor.lastrowid
        
        for i, (answer_text, is_correct) in enumerate(q_data['answers']):
            cursor.execute('''
                INSERT INTO question_answers (question_id, answer_text, is_correct, order_index)
                VALUES (?, ?, ?, ?)
            ''', (question_id, answer_text, is_correct, i))
    
    print(f"✅ {len(geography_questions)} questions de géographie insérées")

def insert_logic_questions(cursor):
    """Insérer des questions de logique"""
    
    cursor.execute("SELECT id FROM question_categories WHERE name = 'Logique'")
    logic_category_id = cursor.fetchone()[0]
    
    logic_questions = [
        {
            'question': 'Si tous les chats sont des animaux et que Minou est un chat, alors Minou est...',
            'type': 'QCM',
            'difficulty': 'débutant',
            'points': 1,
            'answers': [
                ('un animal', True),
                ('un chat', False),
                ('Minou', False),
                ('tous les chats', False)
            ]
        },
        {
            'question': 'Quel nombre continue la suite : 2, 4, 6, 8, ... ?',
            'type': 'QCM',
            'difficulty': 'débutant',
            'points': 1,
            'answers': [
                ('10', True),
                ('9', False),
                ('11', False),
                ('12', False)
            ]
        },
        {
            'question': 'Quel nombre continue la suite : 1, 3, 5, 7, ... ?',
            'type': 'QCM',
            'difficulty': 'débutant',
            'points': 1,
            'answers': [
                ('9', True),
                ('8', False),
                ('10', False),
                ('11', False)
            ]
        },
        {
            'question': 'Si A = 1, B = 2, C = 3, alors D = ?',
            'type': 'QCM',
            'difficulty': 'intermédiaire',
            'points': 2,
            'answers': [
                ('4', True),
                ('5', False),
                ('3', False),
                ('6', False)
            ]
        },
        {
            'question': 'Quel nombre continue la suite : 1, 2, 4, 8, ... ?',
            'type': 'QCM',
            'difficulty': 'intermédiaire',
            'points': 2,
            'answers': [
                ('16', True),
                ('12', False),
                ('14', False),
                ('10', False)
            ]
        },
        {
            'question': 'Si 5 chats attrapent 5 souris en 5 minutes, combien de chats attrapent 10 souris en 10 minutes ?',
            'type': 'QCM',
            'difficulty': 'intermédiaire',
            'points': 2,
            'answers': [
                ('5 chats', True),
                ('10 chats', False),
                ('2 chats', False),
                ('20 chats', False)
            ]
        },
        {
            'question': 'Quel nombre continue la suite : 1, 1, 2, 3, 5, 8, ... ?',
            'type': 'QCM',
            'difficulty': 'avancé',
            'points': 3,
            'answers': [
                ('13', True),
                ('12', False),
                ('14', False),
                ('15', False)
            ]
        },
        {
            'question': 'Si un train roule à 60 km/h et qu\'il doit parcourir 120 km, combien de temps mettra-t-il ?',
            'type': 'QCM',
            'difficulty': 'intermédiaire',
            'points': 2,
            'answers': [
                ('2 heures', True),
                ('1 heure', False),
                ('3 heures', False),
                ('4 heures', False)
            ]
        },
        {
            'question': 'Quel nombre continue la suite : 2, 6, 12, 20, ... ?',
            'type': 'QCM',
            'difficulty': 'avancé',
            'points': 3,
            'answers': [
                ('30', True),
                ('28', False),
                ('32', False),
                ('26', False)
            ]
        },
        {
            'question': 'Si 3 ouvriers construisent un mur en 6 jours, combien d\'ouvriers faut-il pour construire le même mur en 2 jours ?',
            'type': 'QCM',
            'difficulty': 'avancé',
            'points': 3,
            'answers': [
                ('9 ouvriers', True),
                ('6 ouvriers', False),
                ('3 ouvriers', False),
                ('12 ouvriers', False)
            ]
        }
    ]
    
    for q_data in logic_questions:
        cursor.execute('''
            INSERT INTO assessment_questions (category_id, question_text, question_type, difficulty_level, points)
            VALUES (?, ?, ?, ?, ?)
        ''', (logic_category_id, q_data['question'], q_data['type'], q_data['difficulty'], q_data['points']))
        
        question_id = cursor.lastrowid
        
        for i, (answer_text, is_correct) in enumerate(q_data['answers']):
            cursor.execute('''
                INSERT INTO question_answers (question_id, answer_text, is_correct, order_index)
                VALUES (?, ?, ?, ?)
            ''', (question_id, answer_text, is_correct, i))
    
    print(f"✅ {len(logic_questions)} questions de logique insérées")

def create_assessments(cursor):
    """Créer des évaluations complètes"""
    
    assessments_data = [
        {
            'title': 'Évaluation Initiale - Mathématiques',
            'description': 'Test de connaissances en mathématiques de base',
            'category': 'Mathématiques',
            'total_points': 20,
            'time_limit': 30
        },
        {
            'title': 'Évaluation Initiale - Français',
            'description': 'Test de grammaire et vocabulaire français',
            'category': 'Français',
            'total_points': 20,
            'time_limit': 25
        },
        {
            'title': 'Évaluation Initiale - Sciences',
            'description': 'Test de connaissances scientifiques de base',
            'category': 'Sciences',
            'total_points': 20,
            'time_limit': 20
        },
        {
            'title': 'Évaluation Initiale - Histoire',
            'description': 'Test de connaissances historiques',
            'category': 'Histoire',
            'total_points': 20,
            'time_limit': 25
        },
        {
            'title': 'Évaluation Initiale - Géographie',
            'description': 'Test de connaissances géographiques',
            'category': 'Géographie',
            'total_points': 20,
            'time_limit': 20
        },
        {
            'title': 'Évaluation Initiale - Logique',
            'description': 'Test de raisonnement logique',
            'category': 'Logique',
            'total_points': 20,
            'time_limit': 30
        },
        {
            'title': 'Évaluation Complète - Niveau Débutant',
            'description': 'Test complet pour évaluer le niveau initial',
            'category': 'Culture générale',
            'total_points': 50,
            'time_limit': 60
        }
    ]
    
    for assessment_data in assessments_data:
        # Récupérer l'ID de la catégorie
        cursor.execute("SELECT id FROM question_categories WHERE name = ?", (assessment_data['category'],))
        category_id = cursor.fetchone()[0]
        
        # Créer l'évaluation
        cursor.execute('''
            INSERT INTO assessments (title, description, category_id, total_points, time_limit)
            VALUES (?, ?, ?, ?, ?)
        ''', (assessment_data['title'], assessment_data['description'], category_id, 
              assessment_data['total_points'], assessment_data['time_limit']))
        
        assessment_id = cursor.lastrowid
        
        # Récupérer les questions de la catégorie
        cursor.execute('''
            SELECT id FROM assessment_questions 
            WHERE category_id = ? 
            ORDER BY difficulty_level, RANDOM()
            LIMIT 10
        ''', (category_id,))
        
        questions = cursor.fetchall()
        
        # Lier les questions à l'évaluation
        for i, (question_id,) in enumerate(questions):
            cursor.execute('''
                INSERT INTO assessment_questions_link (assessment_id, question_id, order_index)
                VALUES (?, ?, ?)
            ''', (assessment_id, question_id, i))
    
    print(f"✅ {len(assessments_data)} évaluations créées")

def main():
    """Fonction principale"""
    print("🚀 Création de la base de données riche pour Najah AI...")
    
    try:
        # Créer la base de données et les tables
        conn, cursor = create_database()
        
        # Insérer les données
        insert_categories(cursor)
        insert_math_questions(cursor)
        insert_french_questions(cursor)
        insert_science_questions(cursor)
        insert_history_questions(cursor)
        insert_geography_questions(cursor)
        insert_logic_questions(cursor)
        
        # Créer les évaluations
        create_assessments(cursor)
        
        # Valider les changements
        conn.commit()
        
        # Afficher les statistiques
        cursor.execute("SELECT COUNT(*) FROM question_categories")
        categories_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM assessment_questions")
        questions_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM assessments")
        assessments_count = cursor.fetchone()[0]
        
        print(f"\n🎉 Base de données créée avec succès !")
        print(f"📊 Statistiques :")
        print(f"   • {categories_count} catégories de questions")
        print(f"   • {questions_count} questions d'évaluation")
        print(f"   • {assessments_count} évaluations créées")
        print(f"   • Base de données : ./data/app.db")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de la création : {e}")
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()
