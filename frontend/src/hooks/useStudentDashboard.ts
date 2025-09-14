import { useState, useEffect, useCallback } from 'react';
import { useAuth } from './useAuth';
import { fetchStudentDashboard } from '../api/student/dashboard';
import { fetchUserPoints, fetchUserAchievements, fetchUserChallenges, fetchLeaderboard, fetchUserLevel } from '../api/student/gamification';
import { fetchRecentActivity, fetchActivityStats } from '../api/student/activity';
import { fetchCorrectionStats } from '../api/student/scoreCorrections';
import { ScoreCalculator } from '../utils/scoreCalculator';

export interface DashboardData {
  // Données principales
  stats: {
    totalQuizzes: number;
    completedQuizzes: number;
    averageScore: number;
    currentStreak: number;
    totalPoints: number;
    level: number;
    xpToNextLevel: number;
    currentXp: number;
    rank: string;
    bestScore: number;
  };
  
  // Gamification unifiée
  gamification: {
    points: {
      total_points: number;
      achievements_points: number;
      challenges_points: number;
    };
    level: {
      level: number;
      current_xp: number;
      xp_to_next_level: number;
      progress_percentage: number;
    };
    achievements: {
      unlocked_count: number;
      total_achievements: number;
      achievements: Array<{
        id: number;
        name: string;
        unlocked: boolean;
      }>;
    };
    challenges: {
      completed_count: number;
      total_challenges: number;
      challenges: Array<{
        id: number;
        name: string;
        completed: boolean;
      }>;
    };
    leaderboard: {
      leaderboard: Array<{
        user_id: number;
        username: string;
        total_points: number;
      }>;
      user_rank: number;
    };
  };
  
  // Autres données
  availableQuizzes: any[];
  assignedQuizzes: any[];
  recentActivity: any[];
  activityStats: any;
  correctionStats: any;
  recommendations: any[];
  badges: any[];
  messages: any[];
}

export function useStudentDashboard() {
  const { user, token } = useAuth();
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fonction de calcul unifiée pour l'XP et la progression
  const calculateUnifiedStats = useCallback((quizResults: any[], gamificationData: any) => {
    // Calcul des stats de base avec ScoreCalculator
    const baseStats = ScoreCalculator.calculateGlobalStats(quizResults);
    
    // Récupération des données de gamification
    const points = gamificationData?.points || {};
    const level = gamificationData?.level || {};
    
    // Calcul unifié de l'XP et du niveau
    const totalPoints = points.total_points || baseStats.totalPoints || 0;
    const currentLevel = level.level || baseStats.level || 1;
    
    // Calcul de l'XP pour le niveau suivant (formule : 1000 * niveau)
    const xpToNextLevel = 1000 * currentLevel;
    
    // XP actuel dans le niveau (reste de la division)
    const currentXp = totalPoints % xpToNextLevel;
    
    // Pourcentage de progression vers le niveau suivant
    const progressPercentage = Math.min(100, (currentXp / xpToNextLevel) * 100);
    
    return {
      totalPoints,
      level: currentLevel,
      xpToNextLevel,
      currentXp,
      progressPercentage,
      rank: baseStats.rank || 'Débutant'
    };
  }, []);

  // Fonction de chargement des données
  const loadDashboardData = useCallback(async () => {
    if (!token || !user?.id) return;
    
    try {
      setLoading(true);
      setError(null);
      
      // Chargement parallèle de toutes les données
      const [
        dashboardRes,
        pointsRes,
        achievementsRes,
        challengesRes,
        leaderboardRes,
        levelRes,
        activityRes,
        activityStatsRes,
        correctionStatsRes
      ] = await Promise.all([
        fetchStudentDashboard(token, user.id),
        fetchUserPoints(user.id),
        fetchUserAchievements(user.id),
        fetchUserChallenges(user.id),
        fetchLeaderboard(),
        fetchUserLevel(user.id),
        fetchRecentActivity(user.id, 6),
        fetchActivityStats(user.id, 'week'),
        fetchCorrectionStats(user.id)
      ]);

      // Données de gamification
      const gamificationData = {
        points: pointsRes,
        achievements: achievementsRes,
        challenges: challengesRes,
        leaderboard: leaderboardRes,
        level: levelRes
      };

      // Calcul des stats unifiées
      const quizResults = dashboardRes.availableQuizzes || [];
      const unifiedStats = calculateUnifiedStats(quizResults, gamificationData);
      
      // Calcul des stats avec ScoreCalculator
      const calculatedStats = ScoreCalculator.calculateGlobalStats(quizResults);
      
      // DEBUG: Afficher les données calculées
      console.log('🔍 useStudentDashboard - Données calculées:', {
        quizResultsCount: quizResults.length,
        calculatedStats,
        dashboardResStats: dashboardRes.stats,
        unifiedStats
      });

      // Mise à jour des données de gamification avec les stats unifiées
      const updatedGamification = {
        ...gamificationData,
        level: {
          ...gamificationData.level,
          level: unifiedStats.level,
          current_xp: unifiedStats.currentXp,
          xp_to_next_level: unifiedStats.xpToNextLevel,
          progress_percentage: unifiedStats.progressPercentage
        },
        points: {
          ...gamificationData.points,
          total_points: unifiedStats.totalPoints
        }
      };

      // Construction des données finales synchronisées
      const synchronizedData: DashboardData = {
        stats: {
          totalQuizzes: calculatedStats.totalQuizzes || 0,
          completedQuizzes: calculatedStats.completedQuizzes || 0,
          averageScore: calculatedStats.averageScore || 0,
          currentStreak: calculatedStats.currentStreak || 0,
          totalPoints: unifiedStats.totalPoints,
          level: unifiedStats.level,
          xpToNextLevel: unifiedStats.xpToNextLevel,
          currentXp: unifiedStats.currentXp,
          rank: unifiedStats.rank,
          bestScore: calculatedStats.bestScore || 0
        },
        gamification: updatedGamification,
        availableQuizzes: dashboardRes.availableQuizzes || [],
        assignedQuizzes: dashboardRes.assignedQuizzes || [],
        recentActivity: activityRes || [],
        activityStats: activityStatsRes || {},
        correctionStats: correctionStatsRes || {},
        recommendations: dashboardRes.recommendations || [],
        badges: dashboardRes.badges || [],
        messages: dashboardRes.messages || []
      };

      setData(synchronizedData);
    } catch (err: any) {
      console.error('Erreur lors du chargement du dashboard:', err);
      setError(err.message || 'Erreur lors du chargement des données');
    } finally {
      setLoading(false);
    }
  }, [token, user?.id, calculateUnifiedStats]);

  // Rechargement des données
  const refreshData = useCallback(() => {
    loadDashboardData();
  }, [loadDashboardData]);

  // Chargement initial
  useEffect(() => {
    loadDashboardData();
  }, [loadDashboardData]);

  return {
    data,
    loading,
    error,
    refreshData,
    // Données calculées pour faciliter l'accès
    stats: data?.stats,
    gamification: data?.gamification,
    quizzes: data?.availableQuizzes || [],
    assignedQuizzes: data?.assignedQuizzes || [],
    recentActivity: data?.recentActivity || [],
    recommendations: data?.recommendations || [],
    badges: data?.badges || [],
    messages: data?.messages || []
  };
}
