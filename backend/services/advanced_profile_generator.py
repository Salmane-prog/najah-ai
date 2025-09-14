#!/usr/bin/env python3
"""
Service avancé de génération de profil étudiant avec analyse IA
Génère des profils détaillés basés sur les performances aux 20 questions
"""

from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Any, Optional
import json
import random
from datetime import datetime, timedelta
import math

class AdvancedProfileGenerator:
    """Générateur de profil étudiant avancé avec analyse IA"""
    
    def __init__(self, db: Session):
        self.db = db
        
    def generate_comprehensive_profile(self, student_id: int, test_id: int, final_score: float) -> Dict[str, Any]:
        """Générer un profil complet basé sur l'analyse des 20 réponses"""
        
        try:
            print(f"🧠 Génération du profil IA avancé pour l'étudiant {student_id}")
            
            # 1. Analyser les performances détaillées
            performance_analysis = self._analyze_detailed_performance(test_id)
            
            # 2. Déterminer le style d'apprentissage avec IA
            learning_style = self._determine_learning_style_ai(test_id, performance_analysis)
            
            # 3. Calculer le niveau français avec précision
            french_level = self._calculate_precise_french_level(final_score, performance_analysis)
            
            # 4. Analyser le rythme d'apprentissage
            preferred_pace = self._analyze_learning_pace(test_id, performance_analysis)
            
            # 5. Identifier les forces et faiblesses avec détail
            strengths_weaknesses = self._analyze_strengths_weaknesses(performance_analysis)
            
            # 6. Générer des recommandations personnalisées IA
            ai_recommendations = self._generate_ai_recommendations(
                french_level, learning_style, strengths_weaknesses, performance_analysis
            )
            
            # 7. Créer le profil cognitif détaillé
            cognitive_profile = self._create_cognitive_profile(
                test_id, final_score, performance_analysis, learning_style
            )
            
            # 8. Calculer des métriques avancées
            advanced_metrics = self._calculate_advanced_metrics(performance_analysis)
            
            profile = {
                'student_id': student_id,
                'learning_style': learning_style,
                'french_level': french_level,
                'preferred_pace': preferred_pace,
                'strengths': json.dumps(strengths_weaknesses['strengths']),
                'weaknesses': json.dumps(strengths_weaknesses['weaknesses']),
                'cognitive_profile': json.dumps(cognitive_profile),
                'ai_recommendations': json.dumps(ai_recommendations),
                'advanced_metrics': json.dumps(advanced_metrics),
                'confidence_score': self._calculate_confidence_score(performance_analysis),
                'generated_at': datetime.now().isoformat(),
                'test_id': test_id,
                'final_score': final_score
            }
            
            print(f"✅ Profil IA avancé généré avec succès")
            return profile
            
        except Exception as e:
            print(f"❌ Erreur génération profil avancé: {e}")
            return self._generate_fallback_profile(student_id, test_id, final_score)
    
    def _analyze_detailed_performance(self, test_id: int) -> Dict[str, Any]:
        """Analyser les performances détaillées question par question"""
        
        try:
            # Récupérer toutes les réponses du test
            result = self.db.execute(text("""
                SELECT 
                    qh.question_id,
                    qh.question_text,
                    qh.difficulty,
                    qh.topic,
                    qh.student_response,
                    qh.is_correct,
                    qh.asked_at
                FROM question_history qh
                WHERE qh.test_id = :test_id
                ORDER BY qh.asked_at ASC
            """), {"test_id": test_id})
            
            responses = []
            for row in result:
                responses.append({
                    'question_id': row[0],
                    'question_text': row[1],
                    'difficulty': row[2],
                    'topic': row[3],
                    'student_response': row[4],
                    'is_correct': bool(row[5]),
                    'asked_at': row[6]
                })
            
            # Analyser par difficulté
            difficulty_analysis = {}
            for difficulty in ['easy', 'medium', 'hard']:
                diff_responses = [r for r in responses if r['difficulty'] == difficulty]
                if diff_responses:
                    correct_count = sum(1 for r in diff_responses if r['is_correct'])
                    difficulty_analysis[difficulty] = {
                        'total': len(diff_responses),
                        'correct': correct_count,
                        'success_rate': (correct_count / len(diff_responses)) * 100,
                        'questions': diff_responses
                    }
            
            # Analyser par sujet
            topic_analysis = {}
            for response in responses:
                topic = response['topic']
                if topic not in topic_analysis:
                    topic_analysis[topic] = []
                topic_analysis[topic].append(response)
            
            # Calculer les statistiques par sujet
            for topic, topic_responses in topic_analysis.items():
                correct_count = sum(1 for r in topic_responses if r['is_correct'])
                topic_analysis[topic] = {
                    'responses': topic_responses,
                    'total': len(topic_responses),
                    'correct': correct_count,
                    'success_rate': (correct_count / len(topic_responses)) * 100
                }
            
            # Analyser la progression temporelle
            time_analysis = self._analyze_time_progression(responses)
            
            return {
                'responses': responses,
                'difficulty_analysis': difficulty_analysis,
                'topic_analysis': topic_analysis,
                'time_analysis': time_analysis,
                'total_questions': len(responses),
                'total_correct': sum(1 for r in responses if r['is_correct']),
                'overall_success_rate': (sum(1 for r in responses if r['is_correct']) / len(responses)) * 100 if responses else 0
            }
            
        except Exception as e:
            print(f"❌ Erreur analyse détaillée: {e}")
            return {'responses': [], 'difficulty_analysis': {}, 'topic_analysis': {}, 'time_analysis': {}}
    
    def _analyze_time_progression(self, responses: List[Dict]) -> Dict[str, Any]:
        """Analyser la progression temporelle des réponses"""
        
        if len(responses) < 2:
            return {}
        
        try:
            # Calculer les tendances de performance
            first_half = responses[:len(responses)//2]
            second_half = responses[len(responses)//2:]
            
            first_half_success = sum(1 for r in first_half if r['is_correct']) / len(first_half) * 100
            second_half_success = sum(1 for r in second_half if r['is_correct']) / len(second_half) * 100
            
            improvement = second_half_success - first_half_success
            
            return {
                'first_half_success_rate': first_half_success,
                'second_half_success_rate': second_half_success,
                'improvement_trend': improvement,
                'trend_analysis': 'amélioration' if improvement > 5 else 'stable' if abs(improvement) <= 5 else 'dégradation'
            }
            
        except Exception as e:
            print(f"❌ Erreur analyse temporelle: {e}")
            return {}
    
    def _determine_learning_style_ai(self, test_id: int, performance_analysis: Dict) -> str:
        """Déterminer le style d'apprentissage avec analyse IA"""
        
        try:
            # Analyser les patterns de réponse pour déduire le style
            difficulty_performance = performance_analysis.get('difficulty_analysis', {})
            topic_performance = performance_analysis.get('topic_analysis', {})
            
            # Analyse des scores par type de contenu
            visual_score = 0
            auditory_score = 0
            kinesthetic_score = 0
            
            # Analyser selon les sujets
            for topic, analysis in topic_performance.items():
                success_rate = analysis.get('success_rate', 0)
                
                if topic.lower() in ['grammaire', 'conjugaison', 'genre des noms']:
                    visual_score += success_rate * 0.3  # Ces sujets favorisent l'apprentissage visuel
                elif topic.lower() in ['prononciation', 'compréhension']:
                    auditory_score += success_rate * 0.4  # Ces sujets favorisent l'apprentissage auditif
                else:
                    kinesthetic_score += success_rate * 0.2  # Apprentissage par la pratique
            
            # Analyser la progression de difficulté
            easy_success = difficulty_performance.get('easy', {}).get('success_rate', 0)
            medium_success = difficulty_performance.get('medium', {}).get('success_rate', 0)
            hard_success = difficulty_performance.get('hard', {}).get('success_rate', 0)
            
            # Si performance constante à travers les difficultés -> visuel (méthodique)
            if abs(easy_success - medium_success) < 20 and abs(medium_success - hard_success) < 20:
                visual_score += 30
            # Si grande amélioration du facile au difficile -> kinesthésique (apprend en faisant)
            elif hard_success > easy_success + 20:
                kinesthetic_score += 25
            # Si meilleur sur facile/moyen -> auditif (besoin d'explication)
            elif easy_success > hard_success + 15:
                auditory_score += 20
            
            # Déterminer le style dominant
            scores = {
                'visual': visual_score,
                'auditory': auditory_score,
                'kinesthetic': kinesthetic_score
            }
            
            dominant_style = max(scores, key=scores.get)
            
            # Valider avec un seuil minimum
            if scores[dominant_style] > 15:
                return dominant_style
            else:
                return 'visual'  # Par défaut
                
        except Exception as e:
            print(f"❌ Erreur détermination style: {e}")
            return 'visual'
    
    def _calculate_precise_french_level(self, final_score: float, performance_analysis: Dict) -> str:
        """Calculer le niveau français avec plus de précision"""
        
        try:
            difficulty_analysis = performance_analysis.get('difficulty_analysis', {})
            
            # Analyser les performances par difficulté
            easy_success = difficulty_analysis.get('easy', {}).get('success_rate', 0)
            medium_success = difficulty_analysis.get('medium', {}).get('success_rate', 0)
            hard_success = difficulty_analysis.get('hard', {}).get('success_rate', 0)
            
            # Logique de niveau plus précise
            if hard_success >= 80:
                return 'C2'  # Maîtrise excellente des questions difficiles
            elif hard_success >= 60:
                return 'C1'  # Bonne maîtrise des questions difficiles
            elif medium_success >= 80 and hard_success >= 40:
                return 'B2'  # Excellente maîtrise du moyen + quelques difficiles
            elif medium_success >= 60:
                return 'B1'  # Bonne maîtrise du niveau moyen
            elif easy_success >= 80:
                return 'A2'  # Excellente maîtrise du niveau facile
            else:
                return 'A1'  # Niveau débutant
                
        except Exception as e:
            print(f"❌ Erreur calcul niveau: {e}")
            # Fallback basé sur le score global
            if final_score >= 90:
                return 'C1'
            elif final_score >= 80:
                return 'B2'
            elif final_score >= 70:
                return 'B1'
            elif final_score >= 60:
                return 'A2'
            else:
                return 'A1'
    
    def _analyze_learning_pace(self, test_id: int, performance_analysis: Dict) -> str:
        """Analyser le rythme d'apprentissage préféré"""
        
        try:
            time_analysis = performance_analysis.get('time_analysis', {})
            improvement_trend = time_analysis.get('improvement_trend', 0)
            
            # Analyser la consistance des performances
            difficulty_analysis = performance_analysis.get('difficulty_analysis', {})
            
            # Calculer la variance des performances
            success_rates = []
            for diff_data in difficulty_analysis.values():
                success_rates.append(diff_data.get('success_rate', 0))
            
            if len(success_rates) >= 2:
                variance = sum((x - sum(success_rates)/len(success_rates))**2 for x in success_rates) / len(success_rates)
                
                # Si faible variance et bonne amélioration -> rythme rapide
                if variance < 100 and improvement_trend > 10:
                    return 'rapide'
                # Si forte variance -> rythme lent (besoin de plus de temps)
                elif variance > 300:
                    return 'lent'
                else:
                    return 'moyen'
            
            return 'moyen'
            
        except Exception as e:
            print(f"❌ Erreur analyse rythme: {e}")
            return 'moyen'
    
    def _analyze_strengths_weaknesses(self, performance_analysis: Dict) -> Dict[str, List[str]]:
        """Analyser les forces et faiblesses détaillées"""
        
        try:
            strengths = []
            weaknesses = []
            
            # Analyser par difficulté
            difficulty_analysis = performance_analysis.get('difficulty_analysis', {})
            for difficulty, data in difficulty_analysis.items():
                success_rate = data.get('success_rate', 0)
                if success_rate >= 75:
                    strengths.append(f"Questions {difficulty} ({success_rate:.0f}%)")
                elif success_rate < 50:
                    weaknesses.append(f"Questions {difficulty} ({success_rate:.0f}%)")
            
            # Analyser par sujet
            topic_analysis = performance_analysis.get('topic_analysis', {})
            for topic, data in topic_analysis.items():
                success_rate = data.get('success_rate', 0)
                if success_rate >= 80:
                    strengths.append(f"{topic} ({success_rate:.0f}%)")
                elif success_rate < 60:
                    weaknesses.append(f"{topic} ({success_rate:.0f}%)")
            
            # Si pas de faiblesses identifiées, en inventer une constructive
            if not weaknesses:
                overall_rate = performance_analysis.get('overall_success_rate', 0)
                if overall_rate < 90:
                    weaknesses.append("Perfectionnement possible sur les détails")
                else:
                    weaknesses.append("Maintien du niveau d'excellence")
            
            return {
                'strengths': strengths[:5],  # Limiter à 5
                'weaknesses': weaknesses[:3]  # Limiter à 3
            }
            
        except Exception as e:
            print(f"❌ Erreur analyse forces/faiblesses: {e}")
            return {'strengths': [], 'weaknesses': []}
    
    def _generate_ai_recommendations(self, french_level: str, learning_style: str, 
                                   strengths_weaknesses: Dict, performance_analysis: Dict) -> List[Dict]:
        """Générer des recommandations personnalisées avec IA"""
        
        try:
            recommendations = []
            
            # Recommandations basées sur le niveau
            level_recommendations = {
                'A1': [
                    {
                        'title': 'Consolidation des Bases',
                        'description': 'Concentrez-vous sur le vocabulaire de base et les structures simples',
                        'priority': 'high',
                        'category': 'niveau',
                        'estimated_time': '20-30 min/jour',
                        'resources': ['Applications mobiles', 'Cartes de vocabulaire', 'Exercices répétitifs']
                    }
                ],
                'A2': [
                    {
                        'title': 'Expansion Vocabulaire',
                        'description': 'Élargissez votre vocabulaire et travaillez les temps du passé',
                        'priority': 'high',
                        'category': 'niveau',
                        'estimated_time': '25-35 min/jour',
                        'resources': ['Lectures simples', 'Conversations guidées', 'Exercices de conjugaison']
                    }
                ],
                'B1': [
                    {
                        'title': 'Structures Complexes',
                        'description': 'Maîtrisez les structures grammaticales complexes et l\'expression d\'opinion',
                        'priority': 'medium',
                        'category': 'niveau',
                        'estimated_time': '30-40 min/jour',
                        'resources': ['Articles de presse', 'Débats', 'Rédaction d\'opinions']
                    }
                ],
                'B2': [
                    {
                        'title': 'Nuances et Subtilités',
                        'description': 'Travaillez les nuances de la langue et l\'expression précise',
                        'priority': 'medium',
                        'category': 'niveau',
                        'estimated_time': '35-45 min/jour',
                        'resources': ['Littérature', 'Analyse de textes', 'Expression écrite avancée']
                    }
                ],
                'C1': [
                    {
                        'title': 'Perfectionnement Stylistique',
                        'description': 'Perfectionnez votre style et votre expression spontanée',
                        'priority': 'low',
                        'category': 'niveau',
                        'estimated_time': '40-50 min/jour',
                        'resources': ['Œuvres littéraires', 'Conférences', 'Rédaction créative']
                    }
                ],
                'C2': [
                    {
                        'title': 'Maintien de l\'Excellence',
                        'description': 'Maintenez votre niveau par une pratique régulière et variée',
                        'priority': 'low',
                        'category': 'niveau',
                        'estimated_time': '30-45 min/jour',
                        'resources': ['Actualités', 'Culture française', 'Création de contenu']
                    }
                ]
            }
            
            if french_level in level_recommendations:
                recommendations.extend(level_recommendations[french_level])
            
            # Recommandations basées sur le style d'apprentissage
            style_recommendations = {
                'visual': {
                    'title': 'Apprentissage Visuel Optimisé',
                    'description': 'Utilisez des supports visuels : cartes mentales, schémas, couleurs',
                    'priority': 'medium',
                    'category': 'style',
                    'estimated_time': '15-25 min/jour',
                    'resources': ['Cartes mentales', 'Infographies', 'Vidéos éducatives']
                },
                'auditory': {
                    'title': 'Apprentissage Auditif Personnalisé',
                    'description': 'Pratiquez avec des podcasts, musique française et conversations',
                    'priority': 'medium',
                    'category': 'style',
                    'estimated_time': '20-30 min/jour',
                    'resources': ['Podcasts français', 'Chansons', 'Conversations audio']
                },
                'kinesthetic': {
                    'title': 'Apprentissage Interactif',
                    'description': 'Apprenez par la pratique : jeux, exercices interactifs, mise en situation',
                    'priority': 'medium',
                    'category': 'style',
                    'estimated_time': '25-35 min/jour',
                    'resources': ['Jeux éducatifs', 'Roleplay', 'Exercices pratiques']
                }
            }
            
            if learning_style in style_recommendations:
                recommendations.append(style_recommendations[learning_style])
            
            # Recommandations basées sur les faiblesses
            weaknesses = strengths_weaknesses.get('weaknesses', [])
            if weaknesses:
                recommendations.append({
                    'title': 'Zones d\'Amélioration Ciblées',
                    'description': f'Travail spécifique sur : {", ".join(weaknesses[:2])}',
                    'priority': 'high',
                    'category': 'amélioration',
                    'estimated_time': '15-30 min/jour',
                    'resources': ['Exercices ciblés', 'Répétition espacée', 'Pratique intensive']
                })
            
            # Recommandation de routine
            recommendations.append({
                'title': 'Routine d\'Apprentissage Quotidienne',
                'description': 'Établissez une routine régulière pour maximiser vos progrès',
                'priority': 'low',
                'category': 'routine',
                'estimated_time': '10-15 min/jour',
                'resources': ['Planning personnel', 'Applications de suivi', 'Objectifs SMART']
            })
            
            return recommendations
            
        except Exception as e:
            print(f"❌ Erreur génération recommandations: {e}")
            return []
    
    def _create_cognitive_profile(self, test_id: int, final_score: float, 
                                performance_analysis: Dict, learning_style: str) -> Dict[str, Any]:
        """Créer un profil cognitif détaillé"""
        
        try:
            difficulty_analysis = performance_analysis.get('difficulty_analysis', {})
            topic_analysis = performance_analysis.get('topic_analysis', {})
            time_analysis = performance_analysis.get('time_analysis', {})
            
            # Calculer des scores cognitifs
            memory_score = self._calculate_memory_score(difficulty_analysis)
            reasoning_score = self._calculate_reasoning_score(difficulty_analysis, topic_analysis)
            attention_score = self._calculate_attention_score(performance_analysis)
            processing_speed = self._calculate_processing_speed(time_analysis)
            
            return {
                'test_id': test_id,
                'final_score': final_score,
                'cognitive_scores': {
                    'memory': memory_score,
                    'reasoning': reasoning_score,
                    'attention': attention_score,
                    'processing_speed': processing_speed
                },
                'learning_preferences': {
                    'dominant_style': learning_style,
                    'multimodal_score': self._calculate_multimodal_score(performance_analysis)
                },
                'difficulty_breakdown': difficulty_analysis,
                'topic_breakdown': topic_analysis,
                'temporal_analysis': time_analysis,
                'generated_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Erreur création profil cognitif: {e}")
            return {'test_id': test_id, 'final_score': final_score}
    
    def _calculate_memory_score(self, difficulty_analysis: Dict) -> float:
        """Calculer le score de mémoire basé sur la rétention d'information"""
        # Score basé sur la performance sur les questions faciles (rétention de base)
        easy_success = difficulty_analysis.get('easy', {}).get('success_rate', 0)
        return min(100, easy_success * 1.2)  # Boost pour encourager
    
    def _calculate_reasoning_score(self, difficulty_analysis: Dict, topic_analysis: Dict) -> float:
        """Calculer le score de raisonnement basé sur les questions complexes"""
        # Score basé sur les questions difficiles et la grammaire
        hard_success = difficulty_analysis.get('hard', {}).get('success_rate', 0)
        grammar_success = topic_analysis.get('Grammaire', {}).get('success_rate', 0)
        return (hard_success * 0.7 + grammar_success * 0.3)
    
    def _calculate_attention_score(self, performance_analysis: Dict) -> float:
        """Calculer le score d'attention basé sur la consistance"""
        difficulty_analysis = performance_analysis.get('difficulty_analysis', {})
        
        # Calculer la variance (faible variance = bonne attention)
        scores = [data.get('success_rate', 0) for data in difficulty_analysis.values()]
        if len(scores) >= 2:
            mean_score = sum(scores) / len(scores)
            variance = sum((x - mean_score)**2 for x in scores) / len(scores)
            # Convertir la variance en score d'attention (inverse)
            return max(0, 100 - (variance / 10))
        return 75  # Score par défaut
    
    def _calculate_processing_speed(self, time_analysis: Dict) -> float:
        """Calculer la vitesse de traitement basée sur l'amélioration temporelle"""
        improvement = time_analysis.get('improvement_trend', 0)
        # Plus d'amélioration = meilleure vitesse d'adaptation
        return max(0, min(100, 75 + improvement))
    
    def _calculate_multimodal_score(self, performance_analysis: Dict) -> float:
        """Calculer le score multimodal (adaptabilité à différents types de contenu)"""
        topic_analysis = performance_analysis.get('topic_analysis', {})
        
        if len(topic_analysis) >= 2:
            # Calculer la consistance entre différents sujets
            scores = [data.get('success_rate', 0) for data in topic_analysis.values()]
            mean_score = sum(scores) / len(scores)
            variance = sum((x - mean_score)**2 for x in scores) / len(scores)
            return max(0, 100 - (variance / 5))  # Faible variance = bonne adaptabilité
        return 75
    
    def _calculate_advanced_metrics(self, performance_analysis: Dict) -> Dict[str, Any]:
        """Calculer des métriques avancées pour l'analyse"""
        
        try:
            return {
                'consistency_index': self._calculate_consistency_index(performance_analysis),
                'learning_velocity': self._calculate_learning_velocity(performance_analysis),
                'adaptability_score': self._calculate_adaptability_score(performance_analysis),
                'mastery_distribution': self._calculate_mastery_distribution(performance_analysis),
                'prediction_confidence': self._calculate_prediction_confidence(performance_analysis)
            }
        except Exception as e:
            print(f"❌ Erreur métriques avancées: {e}")
            return {}
    
    def _calculate_consistency_index(self, performance_analysis: Dict) -> float:
        """Calculer l'indice de consistance des performances"""
        difficulty_analysis = performance_analysis.get('difficulty_analysis', {})
        scores = [data.get('success_rate', 0) for data in difficulty_analysis.values()]
        
        if len(scores) >= 2:
            mean_score = sum(scores) / len(scores)
            variance = sum((x - mean_score)**2 for x in scores) / len(scores)
            return max(0, 100 - math.sqrt(variance))
        return 75
    
    def _calculate_learning_velocity(self, performance_analysis: Dict) -> float:
        """Calculer la vélocité d'apprentissage"""
        time_analysis = performance_analysis.get('time_analysis', {})
        improvement = time_analysis.get('improvement_trend', 0)
        return max(0, min(100, 50 + improvement * 2))
    
    def _calculate_adaptability_score(self, performance_analysis: Dict) -> float:
        """Calculer le score d'adaptabilité"""
        topic_analysis = performance_analysis.get('topic_analysis', {})
        
        if len(topic_analysis) >= 3:
            scores = [data.get('success_rate', 0) for data in topic_analysis.values()]
            return min(scores) * 1.1  # Le score le plus faible détermine l'adaptabilité
        return 75
    
    def _calculate_mastery_distribution(self, performance_analysis: Dict) -> Dict[str, float]:
        """Calculer la distribution de maîtrise par niveau"""
        difficulty_analysis = performance_analysis.get('difficulty_analysis', {})
        
        return {
            'basic_mastery': difficulty_analysis.get('easy', {}).get('success_rate', 0),
            'intermediate_mastery': difficulty_analysis.get('medium', {}).get('success_rate', 0),
            'advanced_mastery': difficulty_analysis.get('hard', {}).get('success_rate', 0)
        }
    
    def _calculate_prediction_confidence(self, performance_analysis: Dict) -> float:
        """Calculer la confiance dans les prédictions du profil"""
        total_questions = performance_analysis.get('total_questions', 0)
        
        # Plus de questions = plus de confiance
        if total_questions >= 20:
            return 95
        elif total_questions >= 15:
            return 85
        elif total_questions >= 10:
            return 75
        else:
            return 60
    
    def _calculate_confidence_score(self, performance_analysis: Dict) -> float:
        """Calculer le score de confiance global du profil"""
        total_questions = performance_analysis.get('total_questions', 0)
        topic_count = len(performance_analysis.get('topic_analysis', {}))
        
        # Facteurs de confiance
        question_factor = min(100, (total_questions / 20) * 100)
        diversity_factor = min(100, (topic_count / 5) * 100)
        
        return (question_factor * 0.7 + diversity_factor * 0.3)
    
    def _generate_fallback_profile(self, student_id: int, test_id: int, final_score: float) -> Dict[str, Any]:
        """Générer un profil de fallback en cas d'erreur"""
        
        return {
            'student_id': student_id,
            'learning_style': 'visual',
            'french_level': 'A1' if final_score < 60 else 'A2' if final_score < 80 else 'B1',
            'preferred_pace': 'moyen',
            'strengths': json.dumps(['Motivation pour apprendre']),
            'weaknesses': json.dumps(['Données insuffisantes pour analyse détaillée']),
            'cognitive_profile': json.dumps({
                'test_id': test_id,
                'final_score': final_score,
                'fallback_mode': True
            }),
            'ai_recommendations': json.dumps([{
                'title': 'Continuer l\'apprentissage',
                'description': 'Poursuivez votre apprentissage pour générer un profil plus précis',
                'priority': 'medium',
                'category': 'général'
            }]),
            'confidence_score': 60.0,
            'generated_at': datetime.now().isoformat(),
            'test_id': test_id,
            'final_score': final_score
        }











