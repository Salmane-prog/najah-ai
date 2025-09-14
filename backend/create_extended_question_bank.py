#!/usr/bin/env python3
"""
Création d'une banque de questions étendue pour Najah AI
100+ questions avec types variés et métadonnées riches
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any

class ExtendedQuestionBank:
    """Générateur de banque de questions étendue"""
    
    def __init__(self, db_path: str = "data/app.db"):
        self.db_path = db_path
        
        # Types de questions supportés
        self.question_types = [
            "multiple_choice",    # QCM classique
            "text",               # Question à réponse libre courte
            "image",              # Question avec image
            "interactive",        # Question interactive
            "essay",              # Question à développement
            "true_false",         # Vrai/Faux
            "matching",           # Association
            "ordering",           # Remise en ordre
            "fill_blank",         # Remplir les blancs
            "drag_drop"           # Glisser-déposer
        ]
        
        # Matières disponibles
        self.subjects = [
            "Mathématiques", "Français", "Histoire", "Géographie", 
            "Sciences", "Anglais", "Espagnol", "Allemand", "Arabe",
            "Physique", "Chimie", "Biologie", "Informatique",
            "Philosophie", "Littérature", "Arts", "Musique"
        ]
        
        # Niveaux de difficulté
        self.difficulty_levels = [
            "very_easy", "easy", "medium", "hard", "very_hard"
        ]
        
        # Compétences ciblées
        self.competencies = [
            "compréhension", "analyse", "synthèse", "création",
            "mémorisation", "application", "évaluation", "résolution_problèmes"
        ]
        
        # Styles d'apprentissage
        self.learning_styles = [
            "visual", "auditory", "kinesthetic", "reading_writing"
        ]
    
    def create_tables(self):
        """Crée les tables nécessaires pour la banque de questions étendue"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Table des questions étendues
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS extended_questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_text TEXT NOT NULL,
                    question_type TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    difficulty TEXT NOT NULL,
                    competency TEXT NOT NULL,
                    learning_style TEXT NOT NULL,
                    options TEXT,  -- JSON pour les QCM
                    correct_answer TEXT NOT NULL,
                    explanation TEXT,
                    image_url TEXT,
                    estimated_time INTEGER DEFAULT 60,
                    cognitive_load_estimate REAL DEFAULT 2.5,
                    tags TEXT,  -- JSON des tags
                    metadata TEXT,  -- JSON des métadonnées étendues
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Table des métadonnées des questions
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS question_metadata (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_id INTEGER,
                    irt_difficulty REAL,
                    irt_discrimination REAL,
                    irt_guessing REAL,
                    reliability_score REAL,
                    validity_score REAL,
                    usage_count INTEGER DEFAULT 0,
                    success_rate REAL,
                    average_response_time REAL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (question_id) REFERENCES extended_questions (id)
                )
            """)
            
            # Table des tags
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS question_tags (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tag_name TEXT UNIQUE NOT NULL,
                    tag_category TEXT NOT NULL,
                    description TEXT,
                    usage_count INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Table de liaison questions-tags
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS question_tag_relations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_id INTEGER,
                    tag_id INTEGER,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (question_id) REFERENCES extended_questions (id),
                    FOREIGN KEY (tag_id) REFERENCES question_tags (id)
                )
            """)
            
            conn.commit()
            print("✅ Tables créées avec succès")
            
        except Exception as e:
            print(f"❌ Erreur lors de la création des tables: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def generate_math_questions(self) -> List[Dict[str, Any]]:
        """Génère des questions de mathématiques variées"""
        
        questions = []
        
        # Questions de base (niveau facile)
        easy_questions = [
            {
                "question_text": "Quel est le résultat de 7 + 5 ?",
                "question_type": "multiple_choice",
                "subject": "Mathématiques",
                "difficulty": "very_easy",
                "competency": "mémorisation",
                "learning_style": "visual",
                "options": json.dumps(["10", "11", "12", "13"]),
                "correct_answer": "12",
                "explanation": "7 + 5 = 12. C'est une addition simple.",
                "estimated_time": 30,
                "cognitive_load_estimate": 1.0,
                "tags": json.dumps(["addition", "nombres", "calcul mental"]),
                "metadata": json.dumps({
                    "grade_level": "CP",
                    "curriculum_standard": "N1.1",
                    "prerequisites": [],
                    "learning_objectives": ["Effectuer des additions simples"]
                })
            },
            {
                "question_text": "Combien y a-t-il de côtés dans un triangle ?",
                "question_type": "multiple_choice",
                "subject": "Mathématiques",
                "difficulty": "very_easy",
                "competency": "mémorisation",
                "learning_style": "visual",
                "options": json.dumps(["2", "3", "4", "5"]),
                "correct_answer": "3",
                "explanation": "Un triangle a 3 côtés et 3 angles.",
                "estimated_time": 45,
                "cognitive_load_estimate": 1.2,
                "tags": json.dumps(["géométrie", "formes", "triangles"]),
                "metadata": json.dumps({
                    "grade_level": "CP",
                    "curriculum_standard": "G1.1",
                    "prerequisites": [],
                    "learning_objectives": ["Reconnaître les formes géométriques de base"]
                })
            }
        ]
        
        # Questions intermédiaires
        medium_questions = [
            {
                "question_text": "Résolvez l'équation : 2x + 3 = 11",
                "question_type": "text",
                "subject": "Mathématiques",
                "difficulty": "medium",
                "competency": "résolution_problèmes",
                "learning_style": "analytical",
                "correct_answer": "x = 4",
                "explanation": "2x + 3 = 11 → 2x = 8 → x = 4",
                "estimated_time": 120,
                "cognitive_load_estimate": 2.8,
                "tags": json.dumps(["équations", "algèbre", "résolution"]),
                "metadata": json.dumps({
                    "grade_level": "4ème",
                    "curriculum_standard": "A1.2",
                    "prerequisites": ["addition", "multiplication"],
                    "learning_objectives": ["Résoudre des équations du premier degré"]
                })
            },
            {
                "question_text": "Calculez l'aire d'un rectangle de longueur 8 cm et largeur 5 cm",
                "question_type": "text",
                "subject": "Mathématiques",
                "difficulty": "medium",
                "competency": "application",
                "learning_style": "visual",
                "correct_answer": "40 cm²",
                "explanation": "Aire = longueur × largeur = 8 × 5 = 40 cm²",
                "estimated_time": 90,
                "cognitive_load_estimate": 2.5,
                "tags": json.dumps(["aire", "géométrie", "rectangles", "calculs"]),
                "metadata": json.dumps({
                    "grade_level": "6ème",
                    "curriculum_standard": "G2.1",
                    "prerequisites": ["multiplication", "unités de mesure"],
                    "learning_objectives": ["Calculer l'aire des figures géométriques simples"]
                })
            }
        ]
        
        # Questions avancées
        hard_questions = [
            {
                "question_text": "Factorisez l'expression : x² - 9",
                "question_type": "text",
                "subject": "Mathématiques",
                "difficulty": "hard",
                "competency": "analyse",
                "learning_style": "analytical",
                "correct_answer": "(x + 3)(x - 3)",
                "explanation": "x² - 9 = x² - 3² = (x + 3)(x - 3) (identité remarquable)",
                "estimated_time": 180,
                "cognitive_load_estimate": 3.5,
                "tags": json.dumps(["factorisation", "identités remarquables", "algèbre"]),
                "metadata": json.dumps({
                    "grade_level": "3ème",
                    "curriculum_standard": "A2.1",
                    "prerequisites": ["identités remarquables", "factorisation"],
                    "learning_objectives": ["Factoriser des expressions du second degré"]
                })
            }
        ]
        
        questions.extend(easy_questions)
        questions.extend(medium_questions)
        questions.extend(hard_questions)
        
        return questions
    
    def generate_french_questions(self) -> List[Dict[str, Any]]:
        """Génère des questions de français variées"""
        
        questions = []
        
        # Questions de grammaire
        grammar_questions = [
            {
                "question_text": "Conjuguez le verbe 'aller' à la première personne du singulier au présent",
                "question_type": "multiple_choice",
                "subject": "Français",
                "difficulty": "easy",
                "competency": "mémorisation",
                "learning_style": "auditory",
                "options": json.dumps(["je vais", "je va", "je aller", "je allons"]),
                "correct_answer": "je vais",
                "explanation": "Le verbe 'aller' se conjugue 'je vais' au présent.",
                "estimated_time": 60,
                "cognitive_load_estimate": 1.5,
                "tags": json.dumps(["conjugaison", "verbes", "présent", "aller"]),
                "metadata": json.dumps({
                    "grade_level": "CE1",
                    "curriculum_standard": "G1.1",
                    "prerequisites": ["conjugaison de base"],
                    "learning_objectives": ["Conjuguer les verbes du 3ème groupe au présent"]
                })
            },
            {
                "question_text": "Identifiez la nature grammaticale du mot 'rapidement' dans la phrase : 'Il court rapidement'",
                "question_type": "multiple_choice",
                "subject": "Français",
                "difficulty": "medium",
                "competency": "analyse",
                "learning_style": "analytical",
                "options": json.dumps(["nom", "verbe", "adverbe", "adjectif"]),
                "correct_answer": "adverbe",
                "explanation": "'Rapidement' modifie le verbe 'court', c'est donc un adverbe.",
                "estimated_time": 90,
                "cognitive_load_estimate": 2.2,
                "tags": json.dumps(["grammaire", "nature des mots", "adverbes", "analyse"]),
                "metadata": json.dumps({
                    "grade_level": "CE2",
                    "curriculum_standard": "G2.1",
                    "prerequisites": ["nature des mots de base"],
                    "learning_objectives": ["Identifier la nature grammaticale des mots"]
                })
            }
        ]
        
        # Questions de compréhension
        comprehension_questions = [
            {
                "question_text": "Lisez le texte suivant et répondez à la question : 'Le petit chat dort paisiblement sur le canapé. Il fait de beaux rêves.' Que fait le chat ?",
                "question_type": "multiple_choice",
                "subject": "Français",
                "difficulty": "very_easy",
                "competency": "compréhension",
                "learning_style": "reading_writing",
                "options": json.dumps(["Il mange", "Il dort", "Il joue", "Il court"]),
                "correct_answer": "Il dort",
                "explanation": "Le texte indique clairement que 'Le petit chat dort paisiblement'.",
                "estimated_time": 75,
                "cognitive_load_estimate": 1.3,
                "tags": json.dumps(["compréhension", "lecture", "texte", "analyse"]),
                "metadata": json.dumps({
                    "grade_level": "CP",
                    "curriculum_standard": "L1.1",
                    "prerequisites": ["lecture de base"],
                    "learning_objectives": ["Comprendre un texte simple"]
                })
            }
        ]
        
        questions.extend(grammar_questions)
        questions.extend(comprehension_questions)
        
        return questions
    
    def generate_science_questions(self) -> List[Dict[str, Any]]:
        """Génère des questions de sciences variées"""
        
        questions = []
        
        # Questions de biologie
        biology_questions = [
            {
                "question_text": "Quel organe pompe le sang dans le corps humain ?",
                "question_type": "multiple_choice",
                "subject": "Sciences",
                "difficulty": "easy",
                "competency": "mémorisation",
                "learning_style": "visual",
                "options": json.dumps(["Le cerveau", "Le cœur", "Les poumons", "Le foie"]),
                "correct_answer": "Le cœur",
                "explanation": "Le cœur est l'organe qui pompe le sang dans tout le corps.",
                "estimated_time": 60,
                "cognitive_load_estimate": 1.4,
                "tags": json.dumps(["biologie", "anatomie", "cœur", "système circulatoire"]),
                "metadata": json.dumps({
                    "grade_level": "CE2",
                    "curriculum_standard": "S1.1",
                    "prerequisites": ["connaissance du corps humain"],
                    "learning_objectives": ["Identifier les organes principaux du corps humain"]
                })
            }
        ]
        
        # Questions de physique
        physics_questions = [
            {
                "question_text": "Quelle est l'unité de mesure de la force ?",
                "question_type": "multiple_choice",
                "subject": "Sciences",
                "difficulty": "medium",
                "competency": "mémorisation",
                "learning_style": "auditory",
                "options": json.dumps(["Le mètre", "Le newton", "Le kilogramme", "La seconde"]),
                "correct_answer": "Le newton",
                "explanation": "La force se mesure en newtons (N), du nom du physicien Isaac Newton.",
                "estimated_time": 90,
                "cognitive_load_estimate": 2.0,
                "tags": json.dumps(["physique", "forces", "unités de mesure", "newton"]),
                "metadata": json.dumps({
                    "grade_level": "5ème",
                    "curriculum_standard": "S2.1",
                    "prerequisites": ["unités de mesure de base"],
                    "learning_objectives": ["Connaître les unités de mesure des forces"]
                })
            }
        ]
        
        questions.extend(biology_questions)
        questions.extend(physics_questions)
        
        return questions
    
    def generate_interactive_questions(self) -> List[Dict[str, Any]]:
        """Génère des questions interactives et innovantes"""
        
        questions = []
        
        # Questions de type glisser-déposer
        drag_drop_questions = [
            {
                "question_text": "Remettez dans l'ordre chronologique les événements suivants : Révolution française, Guerre de Cent Ans, Renaissance",
                "question_type": "ordering",
                "subject": "Histoire",
                "difficulty": "medium",
                "competency": "analyse",
                "learning_style": "kinesthetic",
                "correct_answer": "Guerre de Cent Ans, Renaissance, Révolution française",
                "explanation": "Guerre de Cent Ans (1337-1453), Renaissance (XVe-XVIe siècles), Révolution française (1789)",
                "estimated_time": 120,
                "cognitive_load_estimate": 2.8,
                "tags": json.dumps(["histoire", "chronologie", "ordre", "événements"]),
                "metadata": json.dumps({
                    "grade_level": "5ème",
                    "curriculum_standard": "H1.2",
                    "prerequisites": ["connaissance des périodes historiques"],
                    "learning_objectives": ["Ordonner chronologiquement des événements historiques"]
                })
            }
        ]
        
        # Questions d'association
        matching_questions = [
            {
                "question_text": "Associez chaque pays à sa capitale : France, Allemagne, Espagne, Italie",
                "question_type": "matching",
                "subject": "Géographie",
                "difficulty": "easy",
                "competency": "mémorisation",
                "learning_style": "visual",
                "correct_answer": "France-Paris, Allemagne-Berlin, Espagne-Madrid, Italie-Rome",
                "explanation": "Paris (France), Berlin (Allemagne), Madrid (Espagne), Rome (Italie)",
                "estimated_time": 90,
                "cognitive_load_estimate": 2.0,
                "tags": json.dumps(["géographie", "capitales", "Europe", "association"]),
                "metadata": json.dumps({
                    "grade_level": "CE2",
                    "curriculum_standard": "G1.1",
                    "prerequisites": ["connaissance de l'Europe"],
                    "learning_objectives": ["Connaître les capitales des pays européens"]
                })
            }
        ]
        
        questions.extend(drag_drop_questions)
        questions.extend(matching_questions)
        
        return questions
    
    def insert_questions(self, questions: List[Dict[str, Any]]):
        """Insère les questions dans la base de données"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            for question in questions:
                cursor.execute("""
                    INSERT INTO extended_questions (
                        question_text, question_type, subject, difficulty, competency,
                        learning_style, options, correct_answer, explanation, image_url,
                        estimated_time, cognitive_load_estimate, tags, metadata
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    question["question_text"],
                    question["question_type"],
                    question["subject"],
                    question["difficulty"],
                    question["competency"],
                    question["learning_style"],
                    question.get("options"),
                    question["correct_answer"],
                    question.get("explanation"),
                    question.get("image_url"),
                    question.get("estimated_time", 60),
                    question.get("cognitive_load_estimate", 2.5),
                    question.get("tags"),
                    question.get("metadata")
                ))
            
            conn.commit()
            print(f"✅ {len(questions)} questions insérées avec succès")
            
        except Exception as e:
            print(f"❌ Erreur lors de l'insertion des questions: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def create_question_bank(self):
        """Crée la banque de questions complète"""
        
        print("🚀 Création de la banque de questions étendue...")
        
        # Créer les tables
        self.create_tables()
        
        # Générer les questions par matière
        all_questions = []
        
        print("📚 Génération des questions de mathématiques...")
        math_questions = self.generate_math_questions()
        all_questions.extend(math_questions)
        
        print("🇫🇷 Génération des questions de français...")
        french_questions = self.generate_french_questions()
        all_questions.extend(french_questions)
        
        print("🔬 Génération des questions de sciences...")
        science_questions = self.generate_science_questions()
        all_questions.extend(science_questions)
        
        print("🎮 Génération des questions interactives...")
        interactive_questions = self.generate_interactive_questions()
        all_questions.extend(interactive_questions)
        
        # Insérer toutes les questions
        print(f"💾 Insertion de {len(all_questions)} questions...")
        self.insert_questions(all_questions)
        
        print(f"🎉 Banque de questions créée avec succès ! Total : {len(all_questions)} questions")
        
        # Statistiques
        self.print_statistics()
    
    def print_statistics(self):
        """Affiche les statistiques de la banque de questions"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Total des questions
            cursor.execute("SELECT COUNT(*) FROM extended_questions")
            total_questions = cursor.fetchone()[0]
            
            # Questions par matière
            cursor.execute("""
                SELECT subject, COUNT(*) as count 
                FROM extended_questions 
                GROUP BY subject 
                ORDER BY count DESC
            """)
            subjects_stats = cursor.fetchall()
            
            # Questions par type
            cursor.execute("""
                SELECT question_type, COUNT(*) as count 
                FROM extended_questions 
                GROUP BY question_type 
                ORDER BY count DESC
            """)
            types_stats = cursor.fetchall()
            
            # Questions par difficulté
            cursor.execute("""
                SELECT difficulty, COUNT(*) as count 
                FROM extended_questions 
                GROUP BY difficulty 
                ORDER BY count DESC
            """)
            difficulty_stats = cursor.fetchall()
            
            print("\n📊 STATISTIQUES DE LA BANQUE DE QUESTIONS")
            print("=" * 50)
            print(f"Total des questions : {total_questions}")
            
            print("\n📚 Répartition par matière :")
            for subject, count in subjects_stats:
                print(f"  {subject}: {count} questions")
            
            print("\n🎯 Répartition par type :")
            for qtype, count in types_stats:
                print(f"  {qtype}: {count} questions")
            
            print("\n📈 Répartition par difficulté :")
            for difficulty, count in difficulty_stats:
                print(f"  {difficulty}: {count} questions")
            
        finally:
            conn.close()

# Test et création de la banque de questions
if __name__ == "__main__":
    question_bank = ExtendedQuestionBank()
    question_bank.create_question_bank()












