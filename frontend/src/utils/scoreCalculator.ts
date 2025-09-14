// Utilitaire pour corriger les calculs de scores
export class ScoreCalculator {
  
  /**
   * Calcule le score en pourcentage correctement
   * @param score - Score obtenu
   * @param maxScore - Score maximum possible
   * @returns Pourcentage entre 0 et 100
   */
  static calculatePercentage(score: number, maxScore: number): number {
    if (maxScore === 0) return 0;
    
    // Correction pour le cas où maxScore = 1 (problème de données)
    if (maxScore === 1 && score > 1) {
      // Si le score est > 1 et maxScore = 1, on suppose que maxScore devrait être 100
      return Math.min(Math.round(score), 100);
    }
    
    return Math.round((score / maxScore) * 100);
  }

  /**
   * Calcule le score moyen d'une liste de quiz
   * @param quizResults - Liste des résultats de quiz
   * @returns Score moyen en pourcentage
   */
  static calculateAverageScore(quizResults: any[]): number {
    if (quizResults.length === 0) return 0;
    
    const validResults = quizResults.filter(result => 
      result.score !== null && 
      result.score !== undefined && 
      result.max_score && 
      result.max_score > 0
    );

    if (validResults.length === 0) return 0;

    const totalPercentage = validResults.reduce((sum, result) => {
      return sum + this.calculatePercentage(result.score, result.max_score);
    }, 0);

    return Math.round(totalPercentage / validResults.length);
  }

  /**
   * Calcule la progression XP
   * @param currentXp - XP actuel
   * @param xpToNextLevel - XP nécessaire pour le niveau suivant
   * @returns Pourcentage de progression
   */
  static calculateXpProgress(currentXp: number, xpToNextLevel: number): number {
    if (xpToNextLevel === 0) return 0;
    return Math.min(Math.round((currentXp / xpToNextLevel) * 100), 100);
  }

  /**
   * Calcule le niveau basé sur l'XP total
   * @param totalXp - XP total accumulé
   * @returns Niveau actuel
   */
  static calculateLevel(totalXp: number): number {
    return Math.floor(totalXp / 1000) + 1;
  }

  /**
   * Calcule le rang basé sur le niveau
   * @param level - Niveau actuel
   * @returns Rang (Débutant, Intermédiaire, Avancé, Expert)
   */
  static calculateRank(level: number): string {
    if (level >= 10) return 'Expert';
    if (level >= 7) return 'Avancé';
    if (level >= 4) return 'Intermédiaire';
    return 'Débutant';
  }

  /**
   * Valide et nettoie les données de score
   * @param data - Données brutes du backend
   * @returns Données nettoyées
   */
  static sanitizeScoreData(data: any): any {
    let score = data.score || 0;
    let maxScore = data.max_score || 1;
    
    // Correction pour le problème maxScore = 1
    if (maxScore === 1 && score > 1) {
      // Si le score est > 1 et maxScore = 1, on corrige maxScore
      maxScore = Math.max(score, 100); // Utilise le score ou 100 comme max
    }
    
    return {
      ...data,
      score: Math.max(0, score),
      max_score: Math.max(1, maxScore),
      percentage: this.calculatePercentage(score, maxScore)
    };
  }

  /**
   * Calcule les statistiques globales
   * @param quizResults - Liste des résultats de quiz
   * @returns Statistiques calculées
   */
  static calculateGlobalStats(quizResults: any[]): {
    totalQuizzes: number;
    completedQuizzes: number;
    averageScore: number;
    bestScore: number;
    totalPoints: number;
    level: number;
    rank: string;
  } {
    // Nettoyer les données avant calcul
    const cleanedQuizzes = quizResults.map(q => this.sanitizeScoreData(q));
    const completedQuizzes = cleanedQuizzes.filter(q => q.completed === true || q.completed === 1);
    const totalQuizzes = quizResults.length;
    const averageScore = this.calculateAverageScore(completedQuizzes);
    const bestScore = completedQuizzes.length > 0 
      ? Math.max(...completedQuizzes.map(q => q.percentage))
      : 0;
    const totalPoints = completedQuizzes.reduce((sum, q) => sum + (q.score || 0), 0);
    const level = this.calculateLevel(totalPoints);
    const rank = this.calculateRank(level);

    return {
      totalQuizzes,
      completedQuizzes: completedQuizzes.length,
      averageScore,
      bestScore,
      totalPoints,
      level,
      rank
    };
  }

  /**
   * Corrige les données de quiz avec max_score = 1
   * @param quizResults - Liste des résultats de quiz
   * @returns Données corrigées
   */
  static fixMaxScoreIssue(quizResults: any[]): any[] {
    return quizResults.map(quiz => {
      const score = quiz.score || 0;
      const maxScore = quiz.max_score || 1;
      
      // Si maxScore = 1 et score > 1, c'est un problème de données
      if (maxScore === 1 && score > 1) {
        return {
          ...quiz,
          max_score: Math.max(score, 100), // Corrige maxScore
          percentage: Math.min(Math.round(score), 100) // Calcule le bon pourcentage
        };
      }
      
      return {
        ...quiz,
        percentage: this.calculatePercentage(score, maxScore)
      };
    });
  }
} 