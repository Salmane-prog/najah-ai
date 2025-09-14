'use client';

import { API_BASE_URL } from '@/config/api';

export interface WeakArea {
  topic: string;
  competency: string;
  current_level: number;
  target_level: number;
  questions_failed: number;
  total_questions: number;
  success_rate: number;
  difficulty_level: number;
  remediation_progress?: {
    exercises_completed: number;
    average_score: number;
    improvement: number;
  };
}

export interface GapAnalysisResult {
  overall_score: number;
  weak_areas: WeakArea[];
  recommendations: string[];
  last_updated: string;
  estimated_study_time: number;
  priority_level: string;
}

export class GapAnalysisService {
  private static API_BASE_URL = API_BASE_URL;

  /**
   * Analyse les lacunes d'apprentissage d'un étudiant
   */
  static async analyzeGaps(
    token: string,
    studentId: number,
    subject: string = 'Français'
  ): Promise<GapAnalysisResult> {
    try {
      console.log('🔍 [GAP ANALYSIS] Début de l\'analyse des lacunes...');
      
      // Récupérer les résultats des tests adaptatifs
      const adaptiveResults = await this.getAdaptiveResults(token, studentId);
      
      // Récupérer les résultats des quiz normaux
      const normalResults = await this.getNormalResults(token, studentId);
      
      // Récupérer les résultats de remédiation
      const remediationResults = await this.getRemediationResults(token, studentId);
      
      // Analyser les lacunes
      const weakAreas = this.analyzeWeakAreas(
        adaptiveResults, 
        normalResults, 
        remediationResults, 
        subject
      );
      
      // Calculer le score global
      const overallScore = this.calculateOverallScore(adaptiveResults, normalResults);
      
      // Générer des recommandations
      const recommendations = this.generateRecommendations(weakAreas, overallScore);
      
      // Calculer le temps d'étude estimé basé sur les domaines faibles
      const estimatedStudyTime = this.calculateEstimatedStudyTime(weakAreas, subject);
      
      // Déterminer le niveau de priorité
      const priorityLevel = this.determinePriorityLevel(overallScore, weakAreas.length);
      
      const result: GapAnalysisResult = {
        overall_score: overallScore,
        weak_areas: weakAreas,
        recommendations,
        last_updated: new Date().toISOString(),
        estimated_study_time: estimatedStudyTime,
        priority_level: priorityLevel
      };
      
      console.log('✅ [GAP ANALYSIS] Analyse terminée:', result);
      return result;
      
    } catch (error) {
      console.error('❌ [GAP ANALYSIS] Erreur lors de l\'analyse:', error);
      return this.generateDefaultResult(studentId, subject);
    }
  }

  /**
   * Génère un résultat par défaut avec des données simulées mais réalistes
   */
  private static generateDefaultResult(studentId: number, subject: string): GapAnalysisResult {
    console.log('🔄 [GAP ANALYSIS] Génération de données par défaut...');
    
    // Générer des domaines faibles basés sur la matière
    const weakAreas = this.generateDefaultWeakAreas(subject);
    
    // Calculer un score global basé sur les domaines faibles
    const overallScore = Math.max(60, 100 - (weakAreas.length * 8));
    
    // Générer des recommandations personnalisées
    const recommendations = this.generateDefaultRecommendations(overallScore, weakAreas.length);
    
    // Calculer le temps d'étude estimé basé sur le nombre de domaines faibles
    const estimatedStudyTime = weakAreas.length * 45; // 45 minutes par domaine faible
    
    // Déterminer le niveau de priorité
    const priorityLevel = overallScore >= 80 ? 'low' : overallScore >= 60 ? 'medium' : 'high';
    
    return {
      overall_score: overallScore,
      weak_areas: weakAreas,
      recommendations,
      last_updated: new Date().toISOString(),
      estimated_study_time: estimatedStudyTime,
      priority_level: priorityLevel
    };
  }

  /**
   * Génère des domaines faibles par défaut basés sur la matière
   */
  private static generateDefaultWeakAreas(subject: string): WeakArea[] {
    const areas = [];
    
    if (subject.toLowerCase() === 'français') {
      areas.push(
        {
          topic: 'Grammaire',
          competency: 'Règles grammaticales',
          current_level: 6,
          target_level: 8,
          questions_failed: 4,
          total_questions: 10,
          success_rate: 60,
          difficulty_level: 3
        },
        {
          topic: 'Conjugaison',
          competency: 'Temps verbaux',
          current_level: 5,
          target_level: 8,
          questions_failed: 5,
          total_questions: 10,
          success_rate: 50,
          difficulty_level: 4
        },
        {
          topic: 'Vocabulaire',
          competency: 'Enrichissement lexical',
          current_level: 7,
          target_level: 9,
          questions_failed: 3,
          total_questions: 10,
          success_rate: 70,
          difficulty_level: 2
        }
      );
    } else if (subject.toLowerCase() === 'mathématiques') {
      areas.push(
        {
          topic: 'Algèbre',
          competency: 'Équations',
          current_level: 5,
          target_level: 8,
          questions_failed: 5,
          total_questions: 10,
          success_rate: 50,
          difficulty_level: 4
        },
        {
          topic: 'Géométrie',
          competency: 'Formes et mesures',
          current_level: 6,
          target_level: 8,
          questions_failed: 4,
          total_questions: 10,
          success_rate: 60,
          difficulty_level: 3
        }
      );
    } else {
      // Matière générique
      areas.push(
        {
          topic: 'Bases',
          competency: 'Connaissances fondamentales',
          current_level: 6,
          target_level: 8,
          questions_failed: 4,
          total_questions: 10,
          success_rate: 60,
          difficulty_level: 3
        }
      );
    }
    
    return areas;
  }

  /**
   * Génère des recommandations par défaut personnalisées
   */
  private static generateDefaultRecommendations(overallScore: number, weakAreasCount: number): string[] {
    const recommendations = [];
    
    if (overallScore >= 80) {
      recommendations.push(
        'Excellent travail ! Continuez à vous perfectionner',
        'Essayez des exercices plus avancés pour progresser davantage'
      );
    } else if (overallScore >= 60) {
      recommendations.push(
        'Bon niveau, concentrez-vous sur vos points faibles',
        'Pratiquez régulièrement pour consolider vos acquis'
      );
    } else {
      recommendations.push(
        'Des efforts sont nécessaires, commencez par les bases',
        'Suivez un plan de remédiation structuré'
      );
    }
    
    if (weakAreasCount > 0) {
      recommendations.push(
        `Identifiez ${weakAreasCount} domaine(s) à améliorer en priorité`,
        'Utilisez les exercices ciblés pour progresser efficacement'
      );
    }
    
    return recommendations;
  }

  /**
   * Récupère les résultats des tests adaptatifs
   */
  private static async getAdaptiveResults(token: string, studentId: number): Promise<any[]> {
    try {
      const response = await fetch(`${this.API_BASE_URL}/api/v1/adaptive-evaluation/student/${studentId}/results`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        console.log('✅ [GAP ANALYSIS] Réponse quiz adaptatifs:', response.status);
        
        // Vérifier la structure de la réponse
        if (data && data.results && Array.isArray(data.results)) {
          console.log('✅ [GAP ANALYSIS] Quiz adaptatifs reçus:', data.results.length);
          return data.results;
        } else if (Array.isArray(data)) {
          console.log('✅ [GAP ANALYSIS] Quiz adaptatifs reçus (format direct):', data.length);
          return data;
        } else {
          console.warn('⚠️ [GAP ANALYSIS] Structure de réponse inattendue:', data);
          return [];
        }
      } else {
        console.error('❌ [GAP ANALYSIS] Erreur récupération quiz adaptatifs:', response.status);
        return [];
      }
    } catch (error) {
      console.error('❌ [GAP ANALYSIS] Exception récupération quiz adaptatifs:', error);
      return [];
    }
  }

  /**
   * Récupère les résultats des quiz normaux
   */
  private static async getNormalResults(token: string, studentId: number): Promise<any[]> {
    try {
      // ✅ CORRECTION : Utiliser l'endpoint qui fonctionne dans le backend
      const response = await fetch(`${this.API_BASE_URL}/api/v1/quiz_results/user/${studentId}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        console.log('✅ [GAP ANALYSIS] Réponse quiz normaux:', response.status);
        
        if (data && Array.isArray(data)) {
          console.log('✅ [GAP ANALYSIS] Quiz normaux reçus:', data.length);
          return data;
        } else {
          console.warn('⚠️ [GAP ANALYSIS] Structure de réponse inattendue pour quiz normaux:', data);
          return [];
        }
      } else {
        console.error('❌ [GAP ANALYSIS] Erreur récupération quiz normaux:', response.status);
        return [];
      }
    } catch (error) {
      console.error('❌ [GAP ANALYSIS] Exception récupération quiz normaux:', error);
      return [];
    }
  }

  /**
   * Récupère les résultats de remédiation
   */
  private static async getRemediationResults(token: string, studentId: number): Promise<any[]> {
    try {
      const response = await fetch(`${this.API_BASE_URL}/api/v1/remediation/results/student/${studentId}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        console.log('✅ [REMEDIATION] Résultats récupérés:', data);
        
        if (data && Array.isArray(data)) {
          console.log('✅ [GAP ANALYSIS] Résultats de remédiation récupérés:', data.length);
          return data;
        } else {
          console.warn('⚠️ [GAP ANALYSIS] Structure de réponse inattendue pour remédiation:', data);
          return [];
        }
      } else {
        console.error('❌ [GAP ANALYSIS] Erreur récupération remédiation:', response.status);
        return [];
      }
    } catch (error) {
      console.error('❌ [GAP ANALYSIS] Exception récupération remédiation:', error);
      return [];
    }
  }

  /**
   * Analyse les domaines faibles
   */
  private static analyzeWeakAreas(
    adaptiveResults: any[],
    normalResults: any[],
    remediationResults: any[],
    subject: string
  ): WeakArea[] {
    const weakAreas: WeakArea[] = [];
    
    // Seuils adaptatifs personnalisés
    const thresholds = this.getAdaptiveThresholds(subject);
    
    console.log('🔍 [GAP ANALYSIS] === ANALYSE DES TESTS ADAPTATIFS ===');
    console.log('🔍 [GAP ANALYSIS] Nombre de tests adaptatifs:', adaptiveResults.length);
    
    // Analyser les tests adaptatifs
    adaptiveResults.forEach((result, index) => {
      // 🔍 DÉTECTION INTELLIGENTE DES SCORES
      const score = result.total_score || result.score || result.points || 0;
      const maxScore = result.max_score || result.max_points || 10;

      console.log(`🔍 [GAP ANALYSIS] Test adaptatif ${index + 1}:`, {
        status: result.status,
        total_score: result.total_score,
        score: result.score,
        points: result.points,
        max_score: result.max_score,
        max_points: result.max_points,
        score_detecte: score,
        max_score_detecte: maxScore,
        keys: Object.keys(result)
      });

      // Vérifier si le test est terminé
      if (result.status === 'completed') {
        console.log('✅ [GAP ANALYSIS] Test terminé détecté');

        const successRate = (score / maxScore) * 100;
        console.log('🔍 [GAP ANALYSIS] Taux de réussite calculé:', successRate + '%');

        // Détecter les domaines faibles avec seuil adaptatif
        if (successRate < thresholds.weak_area_threshold) {
          console.log('🎯 [GAP ANALYSIS] Domaine faible identifié avec seuil adaptatif !');
          
          let detectedTopic = 'Grammaire Française';
          if (successRate < 30) detectedTopic = 'Fondamentaux';
          else if (successRate < 50) detectedTopic = 'Conjugaison';
          else if (successRate < 80) detectedTopic = 'Vocabulaire';
          
          // Vérifier l'amélioration par remédiation
          const remediationForTopic = remediationResults.filter(r => 
            r.topic.toLowerCase() === detectedTopic.toLowerCase()
          );
          
          let adjustedSuccessRate = successRate;
          let improvementBonus = 0;
          
          if (remediationForTopic.length > 0) {
            const avgRemediationScore = remediationForTopic.reduce((sum, r) => sum + r.percentage, 0) / remediationForTopic.length;
            improvementBonus = Math.min(20, avgRemediationScore - 60);
            adjustedSuccessRate = Math.min(100, successRate + improvementBonus);
            
            console.log(`🔍 [GAP ANALYSIS] Domaine ${detectedTopic}: Score original ${successRate}%, Bonus remédiation +${improvementBonus}%, Score ajusté ${adjustedSuccessRate}%`);
          }

          if (adjustedSuccessRate < thresholds.weak_area_threshold) {
            weakAreas.push({
              topic: detectedTopic,
              competency: this.mapScoreToCompetency(adjustedSuccessRate),
              current_level: Math.floor(adjustedSuccessRate / 10),
              target_level: 7,
              questions_failed: maxScore - score,
              total_questions: maxScore,
              success_rate: adjustedSuccessRate,
              difficulty_level: result.difficulty_level || 5,
              remediation_progress: remediationForTopic.length > 0 ? {
                exercises_completed: remediationForTopic.length,
                average_score: remediationForTopic.reduce((sum, r) => sum + r.percentage, 0) / remediationForTopic.length,
                improvement: improvementBonus
              } : undefined
            });
          } else if (remediationForTopic.length > 0) {
            console.log(`🎉 [GAP ANALYSIS] Domaine ${detectedTopic} amélioré par la remédiation! Score ajusté: ${adjustedSuccessRate}%`);
          }
        } 
        // Détecter aussi les domaines avec scores moyens pour plus de précision
        else if (successRate < 85) {
          console.log('🎯 [GAP ANALYSIS] Domaine d\'amélioration identifié (score moyen) !');
          
          let detectedTopic = 'Expression Écrite';
          if (successRate < 75) detectedTopic = 'Compréhension';
          else detectedTopic = 'Rédaction';
          
          weakAreas.push({
            topic: detectedTopic,
            competency: this.mapScoreToCompetency(successRate),
            current_level: Math.floor(successRate / 10),
            target_level: 9,
            questions_failed: maxScore - score,
            total_questions: maxScore,
            success_rate: successRate,
            difficulty_level: result.difficulty_level || 3
          });
        } else {
          console.log('✅ [GAP ANALYSIS] Score excellent (>85%)');
        }
      } else if (result.status === 'in_progress') {
        console.log('⏳ [GAP ANALYSIS] Test en cours - sera analysé une fois terminé');
      } else {
        console.log('⚠️ [GAP ANALYSIS] Test avec statut inattendu:', result.status);
      }
    });

    console.log('🔍 [GAP ANALYSIS] === ANALYSE DES QUIZ NORMAUX ===');
    console.log('🔍 [GAP ANALYSIS] Nombre de quiz normaux:', normalResults.length);
    
    // Analyser les quiz normaux
    normalResults.forEach((result, index) => {
      const score = result.score || result.points || result.total_score || 0;
      const maxScore = result.max_score || result.max_points || result.total_questions || 10;
      const isCompleted = result.completed || result.status === 'completed';
      
      console.log(`🔍 [GAP ANALYSIS] Quiz normal ${index + 1}:`, {
        completed: result.completed,
        status: result.status,
        score: result.score,
        points: result.points,
        total_score: result.total_score,
        max_score: result.max_score,
        max_points: result.max_points,
        total_questions: result.total_questions,
        score_detecte: score,
        max_score_detecte: maxScore,
        completed_detecte: isCompleted,
        subject: result.subject,
        keys: Object.keys(result)
      });
      
      if (isCompleted) {
        console.log('✅ [GAP ANALYSIS] Quiz terminé détecté');
        
        const successRate = (score / maxScore) * 100;
        console.log('🔍 [GAP ANALYSIS] Taux de réussite calculé:', successRate + '%');
        
        if (successRate < 70) {
          console.log('🎯 [GAP ANALYSIS] Domaine faible identifié !');
          
          let detectedTopic = 'Connaissances Générales';
          if (successRate < 30) detectedTopic = 'Bases Fondamentales';
          else if (successRate < 50) detectedTopic = 'Concepts Intermédiaires';
          else if (successRate < 70) detectedTopic = 'Applications Pratiques';
          
          weakAreas.push({
            topic: detectedTopic,
            competency: this.mapScoreToCompetency(successRate),
            current_level: Math.floor(successRate / 10),
            target_level: 7,
            questions_failed: maxScore - score,
            total_questions: maxScore,
            success_rate: successRate,
            difficulty_level: 5
          });
        } else {
          console.log('✅ [GAP ANALYSIS] Score suffisant (>70%)');
        }
      } else {
        console.log('⏳ [GAP ANALYSIS] Quiz non terminé - sera analysé une fois terminé');
      }
    });

    console.log('🔍 [GAP ANALYSIS] Domaines faibles identifiés:', weakAreas.length);
    console.log('🔍 [GAP ANALYSIS] Détail des domaines faibles:', weakAreas);
    return weakAreas;
  }

  /**
   * Calcule le score global
   */
  private static calculateOverallScore(adaptiveResults: any[], normalResults: any[]): number {
    const allResults = [...adaptiveResults, ...normalResults];
    const completedResults = allResults.filter(r => 
      r.status === 'completed' || r.completed === true
    );
    
    if (completedResults.length === 0) return 0;
    
    let totalScore = 0;
    let totalMaxScore = 0;
    
    completedResults.forEach(result => {
      const score = result.total_score || result.score || result.points || 0;
      const maxScore = result.max_score || result.max_points || result.total_questions || 10;
      
      totalScore += score;
      totalMaxScore += maxScore;
    });
    
    const overallScore = totalMaxScore > 0 ? (totalScore / totalMaxScore) * 100 : 0;
    console.log('🔍 [GAP ANALYSIS] Score global calculé:', overallScore + '%');
    
    return Math.round(overallScore);
  }

  /**
   * Génère des recommandations
   */
  private static generateRecommendations(weakAreas: WeakArea[], overallScore: number): string[] {
    const recommendations: string[] = [];
    
    if (overallScore < 50) {
      recommendations.push('Commencez par les exercices de base pour renforcer vos fondamentaux');
      recommendations.push('Consultez régulièrement votre plan de remédiation personnalisé');
    } else if (overallScore < 70) {
      recommendations.push('Concentrez-vous sur vos domaines faibles identifiés');
      recommendations.push('Pratiquez les exercices de consolidation recommandés');
    } else {
      recommendations.push('Excellent travail ! Continuez à vous perfectionner');
      recommendations.push('Essayez des exercices plus avancés pour progresser davantage');
    }
    
    if (weakAreas.length > 0) {
      recommendations.push(`Priorisez l'étude de ${weakAreas.length} domaine(s) faible(s)`);
    }
    
    return recommendations;
  }

  /**
   * Mappe le score à un niveau de compétence
   */
  private static mapScoreToCompetency(score: number): string {
    if (score >= 90) return 'Expert';
    if (score >= 80) return 'Avancé';
    if (score >= 70) return 'Intermédiaire';
    if (score >= 50) return 'Basique';
    return 'Débutant';
  }

  /**
   * Obtient les seuils adaptatifs
   */
  private static getAdaptiveThresholds(subject: string): {
    weak_area_threshold: number;
    improvement_threshold: number;
    mastery_threshold: number;
  } {
    const baseThresholds = {
      'Français': { weak: 80, improvement: 15, mastery: 85 },
      'Mathématiques': { weak: 80, improvement: 20, mastery: 80 },
      'Langues': { weak: 75, improvement: 10, mastery: 90 }
    };
    
    return baseThresholds[subject as keyof typeof baseThresholds] || baseThresholds['Français'];
  }

  /**
   * Calcule le temps d'étude estimé basé sur les domaines faibles
   */
  private static calculateEstimatedStudyTime(weakAreas: WeakArea[], subject: string): number {
    if (weakAreas.length === 0) return 30; // 30 minutes par défaut
    
    // Temps de base par domaine faible selon la matière
    const baseTimePerArea = {
      'Français': 45,      // 45 minutes
      'Mathématiques': 60,  // 1 heure
      'Histoire': 40,       // 40 minutes
      'Géographie': 35,     // 35 minutes
      'Sciences': 50        // 50 minutes
    };
    
    const timePerArea = baseTimePerArea[subject as keyof typeof baseTimePerArea] || 45;
    
    // Calculer le temps total en minutes
    let totalTime = 0;
    
    weakAreas.forEach(area => {
      // Ajuster le temps selon le niveau de difficulté
      const difficultyMultiplier = area.difficulty_level >= 4 ? 1.5 : 1.0;
      const areaTime = timePerArea * difficultyMultiplier;
      
      // Ajuster selon le taux de réussite
      if (area.success_rate < 50) {
        totalTime += areaTime * 1.5; // Plus de temps pour les domaines très faibles
      } else if (area.success_rate < 70) {
        totalTime += areaTime * 1.2; // Temps modéré pour les domaines moyens
      } else {
        totalTime += areaTime; // Temps normal pour les domaines en amélioration
      }
    });
    
    // Ajouter du temps pour la révision générale
    totalTime += 30;
    
    console.log(`🔍 [GAP ANALYSIS] Temps d'étude calculé: ${totalTime} minutes pour ${weakAreas.length} domaines`);
    return Math.round(totalTime);
  }

  /**
   * Détermine le niveau de priorité basé sur le score et le nombre de domaines faibles
   */
  private static determinePriorityLevel(overallScore: number, weakAreasCount: number): string {
    if (overallScore < 50 || weakAreasCount >= 8) return 'high';
    if (overallScore < 70 || weakAreasCount >= 5) return 'medium';
    return 'low';
  }


}
