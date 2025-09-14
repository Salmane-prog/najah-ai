import { apiClient } from '@/utils/api';

export interface RealStudentPerformance {
  id: number;
  name: string;
  studyTime: number;
  quizzesPassed: string;
  averageScore: number;
  engagement: number;
}

export interface RealClassOverview {
  activeStudents: number;
  averageScore: number;
  averageEngagement: number;
  averageStudyTime: number;
}

export interface RealProgressData {
  week: string;
  averageScore: number;
  testsCompleted: number;
}

export interface RealSubjectData {
  month: string;
  testsCreated: number;
  testsCompleted: number;
}

export interface RealAIPrediction {
  studentId: number;
  studentName: string;
  predictionType: string;
  prediction: number;
  confidence: number;
  riskLevel: 'low' | 'medium' | 'high';
  recommendation: string;
}

export interface RealLearningBlockage {
  studentId: number;
  studentName: string;
  subject: string;
  topic: string;
  difficulty: string;
  level: number;
  tags: string[];
  date: string;
  failedAttempts: number;
  averageScore: number;
  worstScore: number;
  timeSpent: number;
  confidence: number;
}

export const realAnalyticsService = {
  // Récupérer la vue d'ensemble de la classe
  async getClassOverview(): Promise<RealClassOverview> {
    try {
      const response = await apiClient.get('/api/v1/analytics/class-overview');
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération de la vue d\'ensemble:', error);
      // Retourner des données par défaut en cas d'erreur
      return {
        activeStudents: 0,
        averageScore: 0,
        averageEngagement: 0,
        averageStudyTime: 0
      };
    }
  },

  // Récupérer les performances détaillées des étudiants
  async getStudentPerformances(): Promise<RealStudentPerformance[]> {
    try {
      const response = await apiClient.get('/api/v1/analytics/student-performances');
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des performances:', error);
      return [];
    }
  },

  // Récupérer les données de progression hebdomadaire
  async getWeeklyProgress(): Promise<RealProgressData[]> {
    try {
      const response = await apiClient.get('/api/v1/analytics/weekly-progress');
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération de la progression:', error);
      return [];
    }
  },

  // Récupérer les statistiques mensuelles par matière
  async getMonthlyStats(): Promise<RealSubjectData[]> {
    try {
      const response = await apiClient.get('/api/v1/analytics/monthly-stats');
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des stats mensuelles:', error);
      return [];
    }
  },

  // Récupérer les prédictions IA
  async getAIPredictions(): Promise<RealAIPrediction[]> {
    try {
      const response = await apiClient.get('/api/v1/analytics/ai-predictions');
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des prédictions IA:', error);
      return [];
    }
  },

  // Récupérer la détection de blocages
  async getLearningBlockages(): Promise<RealLearningBlockage[]> {
    try {
      const response = await apiClient.get('/api/v1/analytics/learning-blockages');
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des blocages:', error);
      return [];
    }
  },

  // Récupérer les prédictions IA
  async getAIPredictions(): Promise<any[]> {
    try {
      const response = await apiClient.get('/api/v1/analytics/ai-predictions');
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des prédictions IA:', error);
      return [];
    }
  },

  // Récupérer les analytics détaillées
  async getDetailedAnalytics(): Promise<any[]> {
    try {
      const response = await apiClient.get('/api/v1/analytics/detailed-analytics');
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des analytics détaillées:', error);
      return [];
    }
  },

  // Récupérer les données de progression hebdomadaire
  async getWeeklyProgress(): Promise<any[]> {
    try {
      console.log('🔍 Service: Appel de getWeeklyProgress...');
      const response = await apiClient.get('/api/v1/analytics/weekly-progress');
      console.log('🔍 Service: Réponse reçue:', response.data);
      console.log('🔍 Service: Type de réponse:', typeof response.data);
      console.log('🔍 Service: Est un tableau:', Array.isArray(response.data));
      return response.data;
    } catch (error) {
      console.error('❌ Service: Erreur lors de la récupération de la progression hebdomadaire:', error);
      return [];
    }
  },

  // Récupérer les statistiques mensuelles
  async getMonthlyStats(): Promise<any[]> {
    try {
      console.log('🔍 Service: Appel de getMonthlyStats...');
      const response = await apiClient.get('/api/v1/analytics/monthly-stats');
      console.log('🔍 Service: Réponse reçue:', response.data);
      console.log('🔍 Service: Type de réponse:', typeof response.data);
      console.log('🔍 Service: Est un tableau:', Array.isArray(response.data));
      return response.data;
    } catch (error) {
      console.error('❌ Service: Erreur lors de la récupération des statistiques mensuelles:', error);
      return [];
    }
  },

  // Récupérer la performance par difficulté
  async getDifficultyPerformance(): Promise<any[]> {
    try {
      console.log('🔍 Service: Appel de getDifficultyPerformance...');
      const response = await apiClient.get('/api/v1/analytics/difficulty-performance');
      console.log('🔍 Service: Réponse reçue:', response.data);
      return response.data;
    } catch (error) {
      console.error('❌ Service: Erreur lors de la récupération de la performance par difficulté:', error);
      return [];
    }
  },

  // Récupérer les tendances d'engagement
  async getEngagementTrends(): Promise<any[]> {
    try {
      console.log('🔍 Service: Appel de getEngagementTrends...');
      const response = await apiClient.get('/api/v1/analytics/engagement-trends');
      console.log('🔍 Service: Réponse reçue:', response.data);
      return response.data;
    } catch (error) {
      console.error('❌ Service: Erreur lors de la récupération des tendances d\'engagement:', error);
      return [];
    }
  },

  // Récupérer la distribution des scores
  async getScoreDistribution(): Promise<any[]> {
    try {
      console.log('🔍 Service: Appel de getScoreDistribution...');
      const response = await apiClient.get('/api/v1/analytics/score-distribution');
      console.log('🔍 Service: Réponse reçue:', response.data);
      return response.data;
    } catch (error) {
      console.error('❌ Service: Erreur lors de la récupération de la distribution des scores:', error);
      return [];
    }
  },

  // Récupérer les tendances d'apprentissage
  async getLearningTrends(): Promise<any[]> {
    try {
      console.log('🔍 Service: Appel de getLearningTrends...');
      const response = await apiClient.get('/api/v1/analytics/learning-trends');
      console.log('🔍 Service: Réponse reçue:', response.data);
      return response.data;
    } catch (error) {
      console.error('❌ Service: Erreur lors de la récupération des tendances d\'apprentissage:', error);
      return [];
    }
  },

  // Générer un rapport
  async generateReport(reportType: string): Promise<{ success: boolean; message: string }> {
    try {
      const response = await apiClient.post('/api/v1/analytics/generate-report', { type: reportType });
      return { success: true, message: 'Rapport généré avec succès' };
    } catch (error) {
      console.error('Erreur lors de la génération du rapport:', error);
      return { success: false, message: 'Erreur lors de la génération du rapport' };
    }
  }
};

