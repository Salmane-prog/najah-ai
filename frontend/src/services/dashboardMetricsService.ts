import { API_BASE_URL } from '../api/config';

export interface DashboardMetrics {
  // Métriques principales
  quizzesCompleted: number;
  averageScore: number;
  consecutiveDays: number;
  badgesEarned: number;
  
  // Progression de niveau
  currentLevel: number;
  currentXP: number;
  levelProgress: number;
  nextLevelXP: number;
  
  // Points et réalisations
  totalPoints: number;
  achievementPoints: number;
  challengePoints: number;
  
  // Challenges et activité
  challengesCompleted: number;
  totalQuizzes: number;
  bestScore: number;
  
  // Données pour graphiques
  performanceHistory: PerformanceData[];
  subjectProgress: SubjectProgress[];
  gamificationData: GamificationData;
}

export interface PerformanceData {
  date: string;
  score: number;
  type: 'adaptive' | 'remediation' | 'assigned';
}

export interface SubjectProgress {
  subject: string;
  progress: number;
  weakAreas: string[];
}

export interface GamificationData {
  badges: Badge[];
  level: number;
  totalXP: number;
  streak: number;
}

export interface Badge {
  id: string;
  name: string;
  description: string;
  type: 'achievement' | 'expertise' | 'improvement';
  points: number;
  earnedAt: string;
}

export class DashboardMetricsService {
  /**
   * Récupère toutes les métriques du dashboard en temps réel
   */
  static async getDashboardMetrics(token: string, studentId: number): Promise<DashboardMetrics> {
    try {
      console.log('📊 [DASHBOARD] Récupération des métriques en temps réel...');
      
      // Récupérer toutes les données sources
      const [
        adaptiveResults,
        remediationResults,
        assignedQuizResults,
        badges
      ] = await Promise.all([
        this.getAdaptiveQuizResults(token, studentId),
        this.getRemediationResults(token, studentId),
        this.getAssignedQuizResults(token, studentId),
        this.getStudentBadges(token, studentId)
      ]);
      
      console.log('📊 [DASHBOARD] Données sources récupérées:', {
        adaptive: adaptiveResults.length,
        remediation: remediationResults.length,
        assigned: assignedQuizResults.length,
        badges: badges.length
      });
      
      // Calculer les métriques unifiées
      const metrics = this.calculateUnifiedMetrics(
        adaptiveResults,
        remediationResults,
        assignedQuizResults,
        badges
      );
      
      console.log('✅ [DASHBOARD] Métriques calculées:', metrics);
      return metrics;
      
    } catch (error) {
      console.error('❌ [DASHBOARD] Erreur récupération métriques:', error);
      throw new Error('Erreur lors de la récupération des métriques du dashboard');
    }
  }
  
  /**
   * Récupère les résultats des quiz adaptatifs
   */
  private static async getAdaptiveQuizResults(token: string, studentId: number): Promise<any[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/adaptive-evaluation/student/${studentId}/results`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (response.ok) {
        const data = await response.json();
        return data.results || [];
      }
      return [];
    } catch (error) {
      console.warn('⚠️ [DASHBOARD] Erreur quiz adaptatifs:', error);
      return [];
    }
  }
  
  /**
   * Récupère les résultats de remédiation
   */
  private static async getRemediationResults(token: string, studentId: number): Promise<any[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/remediation/results/student/${studentId}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (response.ok) {
        const data = await response.json();
        return data || [];
      }
      return [];
    } catch (error) {
      console.warn('⚠️ [DASHBOARD] Erreur résultats remédiation:', error);
      return [];
    }
  }
  
  /**
   * Récupère les résultats des quiz assignés
   */
  private static async getAssignedQuizResults(token: string, studentId: number): Promise<any[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/quiz_results/user/${studentId}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (response.ok) {
        const data = await response.json();
        return data.results || [];
      }
      return [];
    } catch (error) {
      console.warn('⚠️ [DASHBOARD] Erreur quiz assignés:', error);
      return [];
    }
  }
  
  /**
   * Récupère les badges de l'étudiant
   */
  private static async getStudentBadges(token: string, studentId: number): Promise<Badge[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/remediation/badges/student/${studentId}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (response.ok) {
        const data = await response.json();
        return data.badges || [];
      }
      return [];
    } catch (error) {
      console.warn('⚠️ [DASHBOARD] Erreur badges:', error);
      return [];
    }
  }
  
  /**
   * Calcule toutes les métriques unifiées
   */
  private static calculateUnifiedMetrics(
    adaptiveResults: any[],
    remediationResults: any[],
    assignedResults: any[],
    badges: Badge[]
  ): DashboardMetrics {
    // Combiner tous les résultats
    const allResults = [
      ...adaptiveResults.map(r => ({ ...r, type: 'adaptive' as const })),
      ...remediationResults.map(r => ({ ...r, type: 'remediation' as const })),
      ...assignedResults.map(r => ({ ...r, type: 'assigned' as const }))
    ];
    
    // Filtrer les résultats terminés
    const completedResults = allResults.filter(r => 
      r.status === 'completed' || r.is_completed || r.completed_at
    );
    
    // Calculer les scores
    const scores = completedResults.map(r => {
      const score = r.total_score || r.score || r.points || 0;
      const maxScore = r.max_score || r.max_points || 10;
      return maxScore > 0 ? (score / maxScore) * 100 : 0;
    });
    
    // Métriques principales
    const quizzesCompleted = completedResults.length;
    const averageScore = scores.length > 0 ? scores.reduce((a, b) => a + b, 0) / scores.length : 0;
    const bestScore = scores.length > 0 ? Math.max(...scores) : 0;
    
    // Calculer les points et XP
    const totalPoints = completedResults.reduce((sum, r) => sum + (r.points || 0), 0);
    const achievementPoints = badges.reduce((sum, b) => sum + b.points, 0);
    const challengePoints = totalPoints - achievementPoints;
    
    // Calculer le niveau et XP
    const currentLevel = Math.floor(totalPoints / 100) + 1;
    const currentXP = totalPoints % 100;
    const nextLevelXP = 100 - currentXP;
    const levelProgress = (currentXP / 100) * 100;
    
    // Calculer les jours consécutifs (simplifié)
    const today = new Date();
    const consecutiveDays = Math.min(7, Math.floor(totalPoints / 10)); // Approximation
    
    // Générer l'historique de performance
    const performanceHistory = this.generatePerformanceHistory(completedResults);
    
    // Générer les données de progression par matière
    const subjectProgress = this.generateSubjectProgress(completedResults);
    
    // Générer les données de gamification
    const gamificationData = this.generateGamificationData(badges, totalPoints, consecutiveDays);
    
    return {
      quizzesCompleted,
      averageScore: Math.round(averageScore * 100) / 100,
      consecutiveDays,
      badgesEarned: badges.length,
      
      currentLevel,
      currentXP,
      levelProgress: Math.round(levelProgress * 100) / 100,
      nextLevelXP,
      
      totalPoints,
      achievementPoints,
      challengePoints,
      
      challengesCompleted: Math.floor(totalPoints / 50), // Approximation
      totalQuizzes: allResults.length,
      bestScore: Math.round(bestScore * 100) / 100,
      
      performanceHistory,
      subjectProgress,
      gamificationData
    };
  }
  
  /**
   * Génère l'historique de performance
   */
  private static generatePerformanceHistory(results: any[]): PerformanceData[] {
    const history: PerformanceData[] = [];
    const last6Months = 6;
    
    for (let i = last6Months - 1; i >= 0; i--) {
      const date = new Date();
      date.setMonth(date.getMonth() - i);
      
      // Filtrer les résultats du mois
      const monthResults = results.filter(r => {
        const resultDate = new Date(r.completed_at || r.created_at || Date.now());
        return resultDate.getMonth() === date.getMonth() && 
               resultDate.getFullYear() === date.getFullYear();
      });
      
      // Calculer le score moyen du mois
      const monthScores = monthResults.map(r => {
        const score = r.total_score || r.score || r.points || 0;
        const maxScore = r.max_score || r.max_points || 10;
        return maxScore > 0 ? (score / maxScore) * 100 : 0;
      });
      
      const monthAverage = monthScores.length > 0 
        ? monthScores.reduce((a, b) => a + b, 0) / monthScores.length 
        : 0;
      
      history.push({
        date: date.toLocaleDateString('fr-FR', { month: 'short' }),
        score: Math.round(monthAverage * 100) / 100,
        type: monthResults.length > 0 ? monthResults[0].type : 'adaptive'
      });
    }
    
    return history;
  }
  
  /**
   * Génère la progression par matière
   */
  private static generateSubjectProgress(results: any[]): SubjectProgress[] {
    const subjects: { [key: string]: { scores: number[], topics: string[] } } = {};
    
    results.forEach(result => {
      const subject = result.subject || result.topic || 'Général';
      const score = result.total_score || result.score || result.points || 0;
      const maxScore = result.max_score || result.max_points || 10;
      const percentage = maxScore > 0 ? (score / maxScore) * 100 : 0;
      
      if (!subjects[subject]) {
        subjects[subject] = { scores: [], topics: [] };
      }
      
      subjects[subject].scores.push(percentage);
      
      if (result.topic && !subjects[subject].topics.includes(result.topic)) {
        subjects[subject].topics.push(result.topic);
      }
    });
    
    return Object.entries(subjects).map(([subject, data]) => ({
      subject,
      progress: Math.round((data.scores.reduce((a, b) => a + b, 0) / data.scores.length) * 100) / 100,
      weakAreas: data.topics.filter(topic => {
        const topicScores = data.scores.filter((_, index) => 
          results[index]?.topic === topic
        );
        return topicScores.length > 0 && 
               (topicScores.reduce((a, b) => a + b, 0) / topicScores.length) < 70;
      })
    }));
  }
  
  /**
   * Génère les données de gamification
   */
  private static generateGamificationData(
    badges: Badge[], 
    totalPoints: number, 
    consecutiveDays: number
  ): GamificationData {
    return {
      badges,
      level: Math.floor(totalPoints / 100) + 1,
      totalXP: totalPoints,
      streak: consecutiveDays
    };
  }
}
