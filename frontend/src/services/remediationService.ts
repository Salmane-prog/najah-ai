'use client';

import { API_BASE_URL } from '@/config/api';

export interface RemediationResult {
  id: string;
  student_id: number;
  topic: string;
  exercise_type: 'quiz' | 'reading' | 'practice';
  score: number;
  max_score: number;
  percentage: number;
  time_spent: number;
  completed_at: string;
  weak_areas_improved: string[];
}

export interface RemediationProgress {
  topic: string;
  current_level: number;
  previous_level: number;
  improvement: number;
  exercises_completed: number;
  total_exercises: number;
  success_rate: number;
}

export class RemediationService {
  /**
   * Enregistre un résultat de remédiation
   */
  static async saveRemediationResult(
    token: string,
    result: Omit<RemediationResult, 'id' | 'completed_at'>
  ): Promise<RemediationResult> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/remediation/results`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          ...result,
          completed_at: new Date().toISOString(),
        }),
      });

      if (!response.ok) {
        throw new Error('Erreur lors de la sauvegarde du résultat');
      }

      const savedResult = await response.json();
      console.log('✅ [REMEDIATION] Résultat sauvegardé:', savedResult);
      return savedResult;
    } catch (error) {
      console.error('❌ [REMEDIATION] Erreur sauvegarde:', error);
      // Fallback: sauvegarder en localStorage pour développement
      return this.saveToLocalStorage(result);
    }
  }

  /**
   * Récupère tous les résultats de remédiation d'un étudiant
   */
  static async getRemediationResults(
    token: string,
    studentId: number
  ): Promise<RemediationResult[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/remediation/results/student/${studentId}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Erreur lors de la récupération des résultats');
      }

      const results = await response.json();
      console.log('✅ [REMEDIATION] Résultats récupérés:', results);
      return results;
    } catch (error) {
      console.error('❌ [REMEDIATION] Erreur récupération:', error);
      // Fallback: récupérer depuis localStorage
      return this.getFromLocalStorage(studentId);
    }
  }

  /**
   * Calcule le progrès de remédiation par domaine
   */
  static async getRemediationProgress(
    token: string,
    studentId: number
  ): Promise<RemediationProgress[]> {
    try {
      const results = await this.getRemediationResults(token, studentId);
      
      // Grouper par domaine
      const progressByTopic: { [key: string]: RemediationProgress } = {};
      
      results.forEach(result => {
        if (!progressByTopic[result.topic]) {
          progressByTopic[result.topic] = {
            topic: result.topic,
            current_level: 0,
            previous_level: 0,
            improvement: 0,
            exercises_completed: 0,
            total_exercises: 0,
            success_rate: 0,
          };
        }
        
        const progress = progressByTopic[result.topic];
        progress.exercises_completed++;
        progress.success_rate = ((progress.success_rate * (progress.exercises_completed - 1)) + result.percentage) / progress.exercises_completed;
        
        // Calculer le niveau basé sur le pourcentage de réussite
        const newLevel = Math.floor(result.percentage / 10);
        progress.previous_level = progress.current_level;
        progress.current_level = newLevel;
        progress.improvement = progress.current_level - progress.previous_level;
      });
      
      return Object.values(progressByTopic);
    } catch (error) {
      console.error('❌ [REMEDIATION] Erreur calcul progrès:', error);
      return [];
    }
  }

  /**
   * Met à jour l'analyse des lacunes avec les résultats de remédiation
   */
  static async updateGapAnalysis(
    token: string,
    studentId: number,
    subject: string
  ): Promise<any> {
    try {
      const remediationResults = await this.getRemediationResults(token, studentId);
      const remediationProgress = await this.getRemediationProgress(token, studentId);
      
      // Filtrer les résultats par matière
      const subjectResults = remediationResults.filter(result => 
        result.topic.toLowerCase().includes(subject.toLowerCase()) ||
        subject.toLowerCase().includes('français')
      );
      
      // Calculer l'amélioration globale
      const overallImprovement = remediationProgress.reduce((total, progress) => {
        return total + progress.improvement;
      }, 0);
      
      // Mettre à jour les domaines faibles
      const updatedWeakAreas = remediationProgress
        .filter(progress => progress.current_level < 7) // Niveau cible
        .map(progress => ({
          topic: progress.topic,
          current_level: progress.current_level,
          target_level: 7,
          improvement: progress.improvement,
          success_rate: progress.success_rate,
          exercises_completed: progress.exercises_completed,
        }));
      
      console.log('✅ [REMEDIATION] Analyse des lacunes mise à jour:', {
        overallImprovement,
        updatedWeakAreas,
        totalExercises: subjectResults.length,
      });
      
      return {
        overallImprovement,
        updatedWeakAreas,
        totalExercises: subjectResults.length,
        lastUpdate: new Date().toISOString(),
      };
    } catch (error) {
      console.error('❌ [REMEDIATION] Erreur mise à jour analyse:', error);
      return null;
    }
  }

  /**
   * Sauvegarde en localStorage (fallback pour développement)
   */
  private static saveToLocalStorage(result: Omit<RemediationResult, 'id' | 'completed_at'>): RemediationResult {
    const id = `remediation_${Date.now()}_${Math.random()}`;
    const savedResult: RemediationResult = {
      ...result,
      id,
      completed_at: new Date().toISOString(),
    };
    
    const existing = this.getFromLocalStorage(result.student_id);
    existing.push(savedResult);
    localStorage.setItem(`remediation_results_${result.student_id}`, JSON.stringify(existing));
    
    console.log('💾 [REMEDIATION] Sauvegardé en localStorage:', savedResult);
    return savedResult;
  }

  /**
   * Récupère depuis localStorage (fallback pour développement)
   */
  private static getFromLocalStorage(studentId: number): RemediationResult[] {
    try {
      const stored = localStorage.getItem(`remediation_results_${studentId}`);
      return stored ? JSON.parse(stored) : [];
    } catch (error) {
      console.error('❌ [REMEDIATION] Erreur localStorage:', error);
      return [];
    }
  }

  /**
   * Synchronise les résultats avec le backend
   */
  static async syncWithBackend(token: string, studentId: number): Promise<boolean> {
    try {
      const localResults = this.getFromLocalStorage(studentId);
      
      if (localResults.length === 0) {
        console.log('✅ [REMEDIATION] Aucun résultat local à synchroniser');
        return true;
      }
      
      // Envoyer chaque résultat au backend
      for (const result of localResults) {
        await this.saveRemediationResult(token, {
          student_id: result.student_id,
          topic: result.topic,
          exercise_type: result.exercise_type,
          score: result.score,
          max_score: result.max_score,
          percentage: result.percentage,
          time_spent: result.time_spent,
          weak_areas_improved: result.weak_areas_improved,
        });
      }
      
      // Vider le localStorage après synchronisation
      localStorage.removeItem(`remediation_results_${studentId}`);
      console.log('✅ [REMEDIATION] Synchronisation terminée');
      
      return true;
    } catch (error) {
      console.error('❌ [REMEDIATION] Erreur synchronisation:', error);
      return false;
    }
  }
}
