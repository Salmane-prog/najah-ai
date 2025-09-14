#!/usr/bin/env python3
"""
Moteur d'Apprentissage Adaptatif pour Najah AI
Section 2.2 : Tests de positionnement adaptatifs et personnalisation du parcours
"""

import sqlite3
import json
import random
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import numpy as np

@dataclass
class StudentProfile:
    """Profil d'apprentissage de l'étudiant"""
    student_id: int
    learning_style: str  # 'visuel', 'auditif', 'kinesthésique', 'lecture-écriture'
    preferred_difficulty: str  # 'débutant', 'intermédiaire', 'avancé'
    strengths: List[str]  # matières fortes
    weaknesses: List[str]  # matières à améliorer
    response_time_pattern: Dict[str, float]  # temps moyen par type de question
    accuracy_pattern: Dict[str, float]  # précision par matière

@dataclass
class AdaptiveQuestion:
    """Question adaptative avec métadonnées"""
    question_id: int
    question_text: str
    difficulty: str
    category: str
    points: int
    answers: List[Dict]
    estimated_difficulty: float  # 0.0 à 1.0
    cognitive_load: float  # charge cognitive estimée

class AdaptiveLearningEngine:
    """Moteur d'apprentissage adaptatif principal"""
    
    def __init__(self, db_path: str = "./data/app.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect_db()
    
    def connect_db(self):
        """Connexion à la base de données"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            print("✅ Connexion à la base de données établie")
        except Exception as e:
            print(f"❌ Erreur de connexion : {e}")
    
    def get_student_profile(self, student_id: int) -> Optional[StudentProfile]:
        """Récupérer le profil d'apprentissage de l'étudiant"""
        try:
            # Récupérer les résultats précédents
            self.cursor.execute("""
                SELECT 
                    ass.category_id,
                    a.score,
                    a.total_possible,
                    a.time_taken,
                    q.difficulty_level,
                    c.name as category_name
                FROM student_assessment_results a
                JOIN assessments ass ON a.assessment_id = ass.id
                JOIN question_categories c ON ass.category_id = c.id
                JOIN assessment_questions_link aql ON ass.id = aql.assessment_id
                JOIN assessment_questions q ON aql.question_id = q.id
                WHERE a.student_id = ?
                ORDER BY a.completed_at DESC
                LIMIT 50
            """, (student_id,))
            
            results = self.cursor.fetchall()
            
            if not results:
                return self.create_default_profile(student_id)
            
            # Analyser les patterns
            category_performance = {}
            difficulty_preference = {}
            response_times = {}
            
            for result in results:
                category_id, score, total, time, difficulty, category_name = result
                
                if category_name not in category_performance:
                    category_performance[category_name] = []
                
                accuracy = score / total if total > 0 else 0
                category_performance[category_name].append(accuracy)
                
                if difficulty not in difficulty_preference:
                    difficulty_preference[difficulty] = []
                difficulty_preference[difficulty].append(accuracy)
                
                if category_name not in response_times:
                    response_times[category_name] = []
                response_times[category_name].append(time)
            
            # Calculer les moyennes
            avg_performance = {cat: np.mean(perfs) for cat, perfs in category_performance.items()}
            avg_difficulty = {diff: np.mean(perfs) for diff, perfs in difficulty_preference.items()}
            avg_response_time = {cat: np.mean(times) for cat, times in response_times.items()}
            
            # Déterminer les forces et faiblesses
            strengths = [cat for cat, perf in avg_performance.items() if perf > 0.7]
            weaknesses = [cat for cat, perf in avg_performance.items() if perf < 0.5]
            
            # Déterminer la difficulté préférée
            preferred_difficulty = max(avg_difficulty.items(), key=lambda x: x[1])[0]
            
            # Déterminer le style d'apprentissage (basé sur les patterns de temps)
            learning_style = self.detect_learning_style(avg_response_time)
            
            return StudentProfile(
                student_id=student_id,
                learning_style=learning_style,
                preferred_difficulty=preferred_difficulty,
                strengths=strengths,
                weaknesses=weaknesses,
                response_time_pattern=avg_response_time,
                accuracy_pattern=avg_performance
            )
            
        except Exception as e:
            print(f"❌ Erreur lors de la récupération du profil : {e}")
            return self.create_default_profile(student_id)
    
    def create_default_profile(self, student_id: int) -> StudentProfile:
        """Créer un profil par défaut pour un nouvel étudiant"""
        return StudentProfile(
            student_id=student_id,
            learning_style='visuel',  # style par défaut
            preferred_difficulty='débutant',
            strengths=[],
            weaknesses=[],
            response_time_pattern={},
            accuracy_pattern={}
        )
    
    def detect_learning_style(self, response_times: Dict[str, float]) -> str:
        """Détecter le style d'apprentissage basé sur les temps de réponse"""
        if not response_times:
            return 'visuel'
        
        # Analyser les patterns de temps par catégorie
        # Temps rapide = visuel, temps moyen = auditif, temps lent = kinesthésique
        avg_time = np.mean(list(response_times.values()))
        
        if avg_time < 30:  # moins de 30 secondes
            return 'visuel'
        elif avg_time < 60:  # 30-60 secondes
            return 'auditif'
        else:  # plus de 60 secondes
            return 'kinesthésique'
    
    def select_adaptive_question(self, student_id: int, category: str = None, 
                                current_difficulty: str = 'débutant') -> Optional[AdaptiveQuestion]:
        """Sélectionner la prochaine question adaptative"""
        try:
            profile = self.get_student_profile(student_id)
            
            # Déterminer la difficulté cible basée sur les performances récentes
            target_difficulty = self.calculate_target_difficulty(profile, current_difficulty)
            
            # Construire la requête de sélection
            query = """
                SELECT 
                    q.id, q.question_text, q.difficulty_level, q.points,
                    c.name as category_name,
                    qa.id as answer_id, qa.answer_text, qa.is_correct, qa.order_index
                FROM assessment_questions q
                JOIN question_categories c ON q.category_id = c.id
                JOIN question_answers qa ON q.id = qa.question_id
                WHERE q.difficulty_level = ?
            """
            params = [target_difficulty]
            
            if category:
                query += " AND c.name = ?"
                params.append(category)
            
            query += " ORDER BY RANDOM() LIMIT 1"
            
            self.cursor.execute(query, params)
            question_data = self.cursor.fetchall()
            
            if not question_data:
                return None
            
            # Organiser les données
            question_id = question_data[0][0]
            question_text = question_data[0][1]
            difficulty = question_data[0][2]
            points = question_data[0][3]
            category_name = question_data[0][4]
            
            # Organiser les réponses
            answers = []
            for row in question_data:
                answer_id, answer_text, is_correct, order_index = row[5:9]
                answers.append({
                    'id': answer_id,
                    'text': answer_text,
                    'is_correct': bool(is_correct),
                    'order_index': order_index
                })
            
            # Trier les réponses par ordre
            answers.sort(key=lambda x: x['order_index'])
            
            # Calculer la difficulté estimée et la charge cognitive
            estimated_difficulty = self.calculate_question_difficulty(difficulty, category_name, profile)
            cognitive_load = self.calculate_cognitive_load(question_text, answers, profile)
            
            return AdaptiveQuestion(
                question_id=question_id,
                question_text=question_text,
                difficulty=difficulty,
                category=category_name,
                points=points,
                answers=answers,
                estimated_difficulty=estimated_difficulty,
                cognitive_load=cognitive_load
            )
            
        except Exception as e:
            print(f"❌ Erreur lors de la sélection de question : {e}")
            return None
    
    def calculate_target_difficulty(self, profile: StudentProfile, current_difficulty: str) -> str:
        """Calculer la difficulté cible basée sur le profil et la difficulté actuelle"""
        difficulty_levels = ['débutant', 'intermédiaire', 'avancé']
        current_index = difficulty_levels.index(current_difficulty)
        
        # Analyser les performances récentes
        if profile.accuracy_pattern:
            recent_accuracy = np.mean(list(profile.accuracy_pattern.values()))
            
            if recent_accuracy > 0.8:  # Très bon
                # Augmenter la difficulté
                return difficulty_levels[min(current_index + 1, len(difficulty_levels) - 1)]
            elif recent_accuracy < 0.4:  # Faible
                # Diminuer la difficulté
                return difficulty_levels[max(current_index - 1, 0)]
            else:
                # Maintenir la difficulté actuelle
                return current_difficulty
        
        return current_difficulty
    
    def calculate_question_difficulty(self, base_difficulty: str, category: str, 
                                    profile: StudentProfile) -> float:
        """Calculer la difficulté estimée d'une question pour un étudiant spécifique"""
        base_scores = {'débutant': 0.3, 'intermédiaire': 0.6, 'avancé': 0.9}
        base_score = base_scores.get(base_difficulty, 0.5)
        
        # Ajuster selon les forces/faiblesses de l'étudiant
        if category in profile.strengths:
            base_score -= 0.2  # Plus facile
        elif category in profile.weaknesses:
            base_score += 0.2  # Plus difficile
        
        # Ajuster selon le style d'apprentissage
        if profile.learning_style == 'visuel' and 'géométrie' in category.lower():
            base_score -= 0.1
        elif profile.learning_style == 'auditif' and 'langues' in category.lower():
            base_score -= 0.1
        
        return max(0.0, min(1.0, base_score))
    
    def calculate_cognitive_load(self, question_text: str, answers: List[Dict], 
                               profile: StudentProfile) -> float:
        """Calculer la charge cognitive estimée d'une question"""
        base_load = 0.5
        
        # Facteurs de charge cognitive
        text_length = len(question_text)
        num_answers = len(answers)
        
        # Ajuster selon la longueur du texte
        if text_length > 100:
            base_load += 0.2
        elif text_length < 50:
            base_load -= 0.1
        
        # Ajuster selon le nombre de réponses
        if num_answers > 4:
            base_load += 0.1
        elif num_answers < 3:
            base_load -= 0.1
        
        # Ajuster selon le style d'apprentissage
        if profile.learning_style == 'visuel' and len(question_text) > 80:
            base_load += 0.1  # Plus de charge pour les textes longs
        
        return max(0.1, min(1.0, base_load))
    
    def process_student_answer(self, student_id: int, question_id: int, 
                             selected_answer_id: int, response_time: float) -> Dict:
        """Traiter la réponse de l'étudiant et ajuster le profil"""
        try:
            # Récupérer les informations de la question
            self.cursor.execute("""
                SELECT qa.is_correct, q.points, q.difficulty_level, c.name
                FROM question_answers qa
                JOIN assessment_questions q ON qa.question_id = q.id
                JOIN question_categories c ON q.category_id = c.id
                WHERE qa.id = ? AND q.id = ?
            """, (selected_answer_id, question_id))
            
            result = self.cursor.fetchone()
            if not result:
                return {"error": "Question non trouvée"}
            
            is_correct, points, difficulty, category = result
            
            # Calculer les points gagnés
            points_earned = points if is_correct else 0
            
            # Enregistrer la réponse
            self.cursor.execute("""
                INSERT INTO student_answers 
                (student_id, question_id, selected_answer_id, is_correct, points_earned)
                VALUES (?, ?, ?, ?, ?)
            """, (student_id, question_id, selected_answer_id, is_correct, points_earned))
            
            # Mettre à jour le profil d'apprentissage
            self.update_student_profile(student_id, category, is_correct, response_time, difficulty)
            
            # Calculer la prochaine difficulté recommandée
            next_difficulty = self.recommend_next_difficulty(student_id, is_correct, difficulty)
            
            return {
                "success": True,
                "is_correct": is_correct,
                "points_earned": points_earned,
                "next_difficulty": next_difficulty,
                "feedback": self.generate_feedback(is_correct, difficulty, category)
            }
            
        except Exception as e:
            print(f"❌ Erreur lors du traitement de la réponse : {e}")
            return {"error": str(e)}
    
    def update_student_profile(self, student_id: int, category: str, is_correct: bool, 
                             response_time: float, difficulty: str):
        """Mettre à jour le profil d'apprentissage de l'étudiant"""
        # Cette fonction mettrait à jour les statistiques en temps réel
        # Pour l'instant, on se contente d'enregistrer la réponse
        pass
    
    def recommend_next_difficulty(self, student_id: int, is_correct: bool, 
                                current_difficulty: str) -> str:
        """Recommander la prochaine difficulté basée sur la réponse"""
        difficulty_levels = ['débutant', 'intermédiaire', 'avancé']
        current_index = difficulty_levels.index(current_difficulty)
        
        if is_correct:
            # Réponse correcte : maintenir ou augmenter la difficulté
            if current_index < len(difficulty_levels) - 1:
                return difficulty_levels[current_index + 1]
            else:
                return current_difficulty
        else:
            # Réponse incorrecte : maintenir ou diminuer la difficulté
            if current_index > 0:
                return difficulty_levels[current_index - 1]
            else:
                return current_difficulty
    
    def generate_feedback(self, is_correct: bool, difficulty: str, category: str) -> str:
        """Générer un feedback personnalisé"""
        if is_correct:
            if difficulty == 'débutant':
                return f"Excellent ! Vous maîtrisez bien les bases de {category}."
            elif difficulty == 'intermédiaire':
                return f"Bravo ! Vous progressez bien en {category}."
            else:
                return f"Impressionnant ! Vous excellez en {category}."
        else:
            if difficulty == 'débutant':
                return f"Pas de panique ! Les bases de {category} demandent de la pratique."
            elif difficulty == 'intermédiaire':
                return f"Continuez à vous entraîner en {category}, vous y arriverez !"
            else:
                return f"Cette question de {category} était difficile. Revenez aux bases si nécessaire."
    
    def generate_learning_path(self, student_id: int, target_skills: List[str] = None) -> Dict:
        """Générer un parcours d'apprentissage personnalisé"""
        try:
            profile = self.get_student_profile(student_id)
            
            if not target_skills:
                # Utiliser les faiblesses identifiées
                target_skills = profile.weaknesses if profile.weaknesses else ['Mathématiques']
            
            learning_path = {
                "student_id": student_id,
                "target_skills": target_skills,
                "estimated_duration": "2-3 semaines",
                "modules": []
            }
            
            for skill in target_skills:
                # Créer un module pour chaque compétence
                module = self.create_skill_module(skill, profile)
                learning_path["modules"].append(module)
            
            return learning_path
            
        except Exception as e:
            print(f"❌ Erreur lors de la génération du parcours : {e}")
            return {"error": str(e)}
    
    def create_skill_module(self, skill: str, profile: StudentProfile) -> Dict:
        """Créer un module d'apprentissage pour une compétence"""
        # Déterminer le niveau de départ
        if skill in profile.strengths:
            start_level = 'intermédiaire'
        elif skill in profile.weaknesses:
            start_level = 'débutant'
        else:
            start_level = 'débutant'
        
        return {
            "skill": skill,
            "start_level": start_level,
            "target_level": "avancé",
            "estimated_questions": 20,
            "learning_style": profile.learning_style,
            "checkpoints": [
                {"level": "débutant", "questions": 5, "required_score": 0.8},
                {"level": "intermédiaire", "questions": 10, "required_score": 0.7},
                {"level": "avancé", "questions": 5, "required_score": 0.6}
            ]
        }
    
    def close(self):
        """Fermer la connexion à la base de données"""
        if self.conn:
            self.conn.close()

# Exemple d'utilisation
if __name__ == "__main__":
    engine = AdaptiveLearningEngine()
    
    # Test du moteur
    student_id = 1
    
    print("🧠 Test du Moteur d'Apprentissage Adaptatif")
    print("=" * 50)
    
    # Récupérer le profil de l'étudiant
    profile = engine.get_student_profile(student_id)
    print(f"📊 Profil de l'étudiant {student_id}:")
    print(f"   • Style d'apprentissage: {profile.learning_style}")
    print(f"   • Difficulté préférée: {profile.preferred_difficulty}")
    print(f"   • Forces: {', '.join(profile.strengths) if profile.strengths else 'Aucune'}")
    print(f"   • Faiblesses: {', '.join(profile.weaknesses) if profile.weaknesses else 'Aucune'}")
    
    # Sélectionner une question adaptative
    question = engine.select_adaptive_question(student_id, "Mathématiques")
    if question:
        print(f"\n❓ Question adaptative sélectionnée:")
        print(f"   • Catégorie: {question.category}")
        print(f"   • Difficulté: {question.difficulty}")
        print(f"   • Difficulté estimée: {question.estimated_difficulty:.2f}")
        print(f"   • Charge cognitive: {question.cognitive_load:.2f}")
        print(f"   • Question: {question.question_text[:50]}...")
    
    # Générer un parcours d'apprentissage
    learning_path = engine.generate_learning_path(student_id)
    print(f"\n🛤️ Parcours d'apprentissage généré:")
    print(f"   • Compétences cibles: {', '.join(learning_path['target_skills'])}")
    print(f"   • Durée estimée: {learning_path['estimated_duration']}")
    print(f"   • Modules: {len(learning_path['modules'])}")
    
    engine.close()
