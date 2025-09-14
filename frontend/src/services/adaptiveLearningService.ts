import { apiClient } from '../api/config';

export interface AdaptiveLearningPath {
  id: number;
  title: string;
  description: string;
  subject: string;
  level: string;
  difficulty: string;
  estimated_duration: number;
  is_followed: boolean;
  progress?: number;
  is_completed?: boolean;
  started_at?: string;
  current_step?: number;
  total_steps?: number;
  adaptive_features: {
    personalized_content: boolean;
    difficulty_adjustment: boolean;
    remediation_paths: boolean;
    cognitive_adaptation: boolean;
  };
  recommendations: {
    reason: string;
    confidence_score: number;
    learning_style_match: string;
    cognitive_profile_match: string;
  };
}

export interface LearningStep {
  id: number;
  title: string;
  description: string;
  content_type: string;
  estimated_duration: number;
  is_completed: boolean;
  is_locked: boolean;
  difficulty: 'easy' | 'medium' | 'hard';
  adaptive_content?: {
    original_difficulty: string;
    adapted_difficulty: string;
    adaptation_reason: string;
  };
}

export interface StudentProfile {
  french_level: string;
  learning_style: string;
  cognitive_profile: {
    memory_type: string;
    attention_span: string;
    problem_solving: string;
  };
  strengths: string[];
  areas_for_improvement: string[];
  learning_preferences: {
    preferred_content_types: string[];
    preferred_difficulty: string;
    preferred_pace: string;
  };
}

export class AdaptiveLearningService {
  private static API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  /**
   * Récupère le profil d'apprentissage de l'étudiant
   */
  static async getStudentProfile(studentId: number, token: string): Promise<StudentProfile> {
    try {
      const response = await fetch(`${this.API_BASE_URL}/api/v1/french/initial-assessment/student/${studentId}/profile`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`Erreur lors de la récupération du profil: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Erreur getStudentProfile:', error);
      throw error;
    }
  }

  /**
   * Génère un parcours d'apprentissage adaptatif basé sur le profil
   */
  static async generateAdaptivePath(
    studentId: number, 
    subject: string, 
    token: string
  ): Promise<AdaptiveLearningPath> {
    try {
      const response = await fetch(`${this.API_BASE_URL}/api/v1/french/learning-paths/generate`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          student_id: studentId,
          subject: subject,
          adaptive: true
        })
      });

      if (!response.ok) {
        throw new Error(`Erreur lors de la génération du parcours: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Erreur generateAdaptivePath:', error);
      throw error;
    }
  }

  /**
   * Récupère les recommandations personnalisées
   */
  static async getPersonalizedRecommendations(
    studentId: number, 
    token: string
  ): Promise<any[]> {
    try {
      const response = await fetch(`${this.API_BASE_URL}/api/v1/french/recommendations/student/${studentId}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`Erreur lors de la récupération des recommandations: ${response.status}`);
      }

      const data = await response.json();
      return data.recommendations || [];
    } catch (error) {
      console.error('Erreur getPersonalizedRecommendations:', error);
      throw error;
    }
  }

  /**
   * Commence un parcours d'apprentissage
   */
  static async startLearningPath(
    studentId: number, 
    learningPathId: number, 
    token: string
  ): Promise<boolean> {
    try {
      const response = await fetch(`${this.API_BASE_URL}/api/v1/student_learning_paths/${learningPathId}/start`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          student_id: studentId
        })
      });

      return response.ok;
    } catch (error) {
      console.error('Erreur startLearningPath:', error);
      return false;
    }
  }

  /**
   * Met à jour la progression d'une étape
   */
  static async updateStepProgress(
    stepId: number, 
    isCompleted: boolean, 
    performance: number, 
    token: string
  ): Promise<boolean> {
    try {
      const response = await fetch(`${this.API_BASE_URL}/api/v1/learning_steps/${stepId}/complete`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          is_completed: isCompleted,
          performance_score: performance,
          completed_at: new Date().toISOString()
        })
      });

      return response.ok;
    } catch (error) {
      console.error('Erreur updateStepProgress:', error);
      return false;
    }
  }

  /**
   * Analyse les performances et adapte le contenu
   */
  static async analyzePerformanceAndAdapt(
    studentId: number, 
    subject: string, 
    token: string
  ): Promise<{
    difficulty_adjustment: string;
    content_recommendations: string[];
    remediation_suggestions: string[];
  }> {
    try {
      const response = await fetch(`${this.API_BASE_URL}/api/v1/ai/adaptive-analysis`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          student_id: studentId,
          subject: subject,
          analysis_type: 'performance_adaptation'
        })
      });

      if (!response.ok) {
        throw new Error(`Erreur lors de l'analyse: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Erreur analyzePerformanceAndAdapt:', error);
      throw error;
    }
  }

  /**
   * Génère des exercices de remédiation personnalisés
   */
  static async generateRemediationExercises(
    studentId: number, 
    difficulty: string, 
    subject: string, 
    token: string
  ): Promise<any[]> {
    try {
      const response = await fetch(`${this.API_BASE_URL}/api/v1/ai/remediation-exercises`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          student_id: studentId,
          difficulty_level: difficulty,
          subject: subject,
          exercise_type: 'remediation'
        })
      });

      if (!response.ok) {
        throw new Error(`Erreur lors de la génération des exercices: ${response.status}`);
      }

      const data = await response.json();
      return data.exercises || [];
    } catch (error) {
      console.error('Erreur generateRemediationExercises:', error);
      throw error;
    }
  }
}

