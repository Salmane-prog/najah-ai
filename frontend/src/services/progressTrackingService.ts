'use client';

import { API_BASE_URL } from '@/config/api';

export interface ProgressMetrics {
  student_id: number;
  subject: string;
  current_score: number;
  previous_score: number;
  improvement_rate: number;
  trend: 'improving' | 'declining' | 'stable';
  weak_areas_progress: WeakAreaProgress[];
  study_time_logged: number;
  quizzes_completed: number;
  last_updated: string;
}

export interface WeakAreaProgress {
  topic: string;
  initial_score: number;
  current_score: number;
  improvement: number;
  status: 'improved' | 'stable' | 'declining';
  exercises_completed: number;
  time_spent: number;
}

export interface PersonalizedRecommendations {
  student_id: number;
  subject: string;
  priority_areas: string[];
  study_schedule: StudySchedule;
  adaptive_difficulty: number;
  specific_exercises: string[];
  motivation_tips: string[];
}

export interface StudySchedule {
  daily_time: number;
  weekly_sessions: number;
  focus_areas: string[];
  rest_days: string[];
  peak_hours: string[];
}

export class ProgressTrackingService {
  private static API_BASE_URL = API_BASE_URL;

  /**
   * Récupère les métriques de progression d'un étudiant
   */
  static async getProgressMetrics(
    token: string,
    studentId: number,
    subject: string = 'Français'
  ): Promise<ProgressMetrics> {
    try {
      console.log('📊 [PROGRESS TRACKING] Récupération des métriques de progression...');
      
      const response = await fetch(`${this.API_BASE_URL}/api/v1/progress/student/${studentId}/metrics`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        console.log('✅ [PROGRESS TRACKING] Métriques récupérées:', data);
        return data;
      } else if (response.status === 404) {
        console.warn('⚠️ [PROGRESS TRACKING] Endpoint non trouvé, utilisation des métriques par défaut');
        // L'endpoint n'existe pas encore, utiliser les métriques par défaut
        return this.generateDefaultMetrics(studentId, subject);
      } else {
        console.error('❌ [PROGRESS TRACKING] Erreur HTTP:', response.status);
        // Retourner des métriques par défaut en cas d'erreur
        return this.generateDefaultMetrics(studentId, subject);
      }
    } catch (error) {
      console.error('❌ [PROGRESS TRACKING] Exception:', error);
      // En cas d'erreur réseau, utiliser les métriques par défaut
      return this.generateDefaultMetrics(studentId, subject);
    }
  }

  /**
   * Génère des métriques par défaut pour le développement
   */
  private static generateDefaultMetrics(studentId: number, subject: string): ProgressMetrics {
    const currentScore = Math.floor(Math.random() * 30) + 50; // 50-80%
    const previousScore = Math.max(0, currentScore - Math.floor(Math.random() * 20));
    const improvement = currentScore - previousScore;
    
    return {
      student_id: studentId,
      subject,
      current_score: currentScore,
      previous_score: previousScore,
      improvement_rate: improvement,
      trend: improvement > 0 ? 'improving' : improvement < 0 ? 'declining' : 'stable',
      weak_areas_progress: [
        {
          topic: 'Fondamentaux',
          initial_score: 20,
          current_score: 35,
          improvement: 15,
          status: 'improved',
          exercises_completed: 8,
          time_spent: 120
        },
        {
          topic: 'Conjugaison',
          initial_score: 40,
          current_score: 55,
          improvement: 15,
          status: 'improved',
          exercises_completed: 12,
          time_spent: 180
        }
      ],
      study_time_logged: 300, // 5 heures
      quizzes_completed: 15,
      last_updated: new Date().toISOString()
    };
  }

  /**
   * Génère des recommandations personnalisées
   */
  static async getPersonalizedRecommendations(
    token: string,
    studentId: number,
    subject: string = 'Français'
  ): Promise<PersonalizedRecommendations> {
    try {
      console.log('🎯 [PROGRESS TRACKING] Génération de recommandations personnalisées...');
      
      // Récupérer les métriques actuelles
      const metrics = await this.getProgressMetrics(token, studentId, subject);
      
      // Analyser les tendances pour personnaliser
      const recommendations = this.analyzeAndRecommend(metrics);
      
      console.log('✅ [PROGRESS TRACKING] Recommandations générées:', recommendations);
      return recommendations;
      
    } catch (error) {
      console.error('❌ [PROGRESS TRACKING] Erreur recommandations:', error);
      return this.generateDefaultRecommendations(studentId, subject);
    }
  }

  /**
   * Analyse les métriques et génère des recommandations
   */
  private static analyzeAndRecommend(metrics: ProgressMetrics): PersonalizedRecommendations {
    const { current_score, trend, weak_areas_progress } = metrics;
    
    // Déterminer les priorités basées sur le score et la tendance
    let priorityAreas: string[] = [];
    let adaptiveDifficulty = 5;
    let specificExercises: string[] = [];
    let motivationTips: string[] = [];

    if (current_score < 50) {
      priorityAreas = ['Fondamentaux', 'Bases théoriques'];
      adaptiveDifficulty = 3;
      specificExercises = ['Quiz de base', 'Exercices de révision'];
      motivationTips = ['Chaque petit progrès compte !', 'Commencez par les bases'];
    } else if (current_score < 70) {
      priorityAreas = weak_areas_progress
        .filter(area => area.status === 'declining' || area.improvement < 10)
        .map(area => area.topic);
      adaptiveDifficulty = 5;
      specificExercises = ['Exercices ciblés', 'Quiz de consolidation'];
      motivationTips = ['Vous êtes sur la bonne voie !', 'Concentrez-vous sur vos points faibles'];
    } else {
      priorityAreas = ['Perfectionnement', 'Défis avancés'];
      adaptiveDifficulty = 7;
      specificExercises = ['Quiz avancés', 'Problèmes complexes'];
      motivationTips = ['Excellent travail !', 'Continuez à vous dépasser'];
    }

    // Ajuster la difficulté selon la tendance
    if (trend === 'improving') {
      adaptiveDifficulty = Math.min(10, adaptiveDifficulty + 1);
    } else if (trend === 'declining') {
      adaptiveDifficulty = Math.max(1, adaptiveDifficulty - 1);
    }

    // Plan d'étude personnalisé
    const studySchedule: StudySchedule = {
      daily_time: current_score < 60 ? 45 : 30,
      weekly_sessions: current_score < 60 ? 5 : 3,
      focus_areas: priorityAreas,
      rest_days: ['Sunday'],
      peak_hours: current_score < 60 ? ['09:00', '15:00'] : ['10:00', '16:00']
    };

    return {
      student_id: metrics.student_id,
      subject: metrics.subject,
      priority_areas: priorityAreas,
      study_schedule: studySchedule,
      adaptive_difficulty: adaptiveDifficulty,
      specific_exercises: specificExercises,
      motivation_tips: motivationTips
    };
  }

  /**
   * Génère des recommandations par défaut
   */
  private static generateDefaultRecommendations(
    studentId: number,
    subject: string
  ): PersonalizedRecommendations {
    return {
      student_id: studentId,
      subject,
      priority_areas: ['Fondamentaux', 'Conjugaison'],
      study_schedule: {
        daily_time: 30,
        weekly_sessions: 4,
        focus_areas: ['Grammaire', 'Vocabulaire'],
        rest_days: ['Sunday'],
        peak_hours: ['09:00', '15:00']
      },
      adaptive_difficulty: 5,
      specific_exercises: ['Quiz de base', 'Exercices de révision'],
      motivation_tips: ['Chaque jour compte !', 'Vous progressez !']
    };
  }

  /**
   * Calcule les tendances sur plusieurs périodes
   */
  static calculateTrends(scores: number[]): {
    trend: 'improving' | 'declining' | 'stable';
    slope: number;
    confidence: number;
  } {
    if (scores.length < 2) {
      return { trend: 'stable', slope: 0, confidence: 0 };
    }

    // Calcul de la pente (méthode des moindres carrés)
    const n = scores.length;
    const x = Array.from({ length: n }, (_, i) => i);
    
    const sumX = x.reduce((a, b) => a + b, 0);
    const sumY = scores.reduce((a, b) => a + b, 0);
    const sumXY = x.reduce((sum, xi, i) => sum + xi * scores[i], 0);
    const sumX2 = x.reduce((sum, xi) => sum + xi * xi, 0);
    
    const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
    
    // Déterminer la tendance
    let trend: 'improving' | 'declining' | 'stable' = 'stable';
    if (slope > 2) trend = 'improving';
    else if (slope < -2) trend = 'declining';
    
    // Calculer la confiance (R²)
    const meanY = sumY / n;
    const ssRes = scores.reduce((sum, yi, i) => {
      const predicted = slope * i + (sumY / n - slope * sumX / n);
      return sum + Math.pow(yi - predicted, 2);
    }, 0);
    const ssTot = scores.reduce((sum, yi) => sum + Math.pow(yi - meanY, 2), 0);
    const confidence = ssTot > 0 ? 1 - (ssRes / ssTot) : 0;

    return { trend, slope, confidence };
  }

  /**
   * Ajuste dynamiquement les seuils de détection
   */
  static getAdaptiveThresholds(
    studentLevel: 'beginner' | 'intermediate' | 'advanced',
    subject: string
  ): {
    weak_area_threshold: number;
    improvement_threshold: number;
    mastery_threshold: number;
  } {
    const baseThresholds = {
      beginner: { weak: 60, improvement: 10, mastery: 80 },
      intermediate: { weak: 70, improvement: 15, mastery: 85 },
      advanced: { weak: 80, improvement: 20, mastery: 90 }
    };

    const thresholds = baseThresholds[studentLevel];
    
    // Ajuster selon la matière
    if (subject === 'Mathématiques') {
      thresholds.weak += 5;
      thresholds.mastery -= 5;
    } else if (subject === 'Langues') {
      thresholds.weak -= 5;
      thresholds.mastery += 5;
    }

    return {
      weak_area_threshold: thresholds.weak,
      improvement_threshold: thresholds.improvement,
      mastery_threshold: thresholds.mastery
    };
  }
}
