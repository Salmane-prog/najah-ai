'use client';

import { API_BASE_URL } from '@/config/api';

export interface Badge {
  id: number;
  student_id: number;
  badge_type: string;
  badge_name: string;
  badge_description: string;
  badge_icon: string;
  earned_at: string;
  metadata: any;
}

export interface BadgeProgress {
  type: string;
  name: string;
  description: string;
  icon: string;
  condition: string;
  progress: number;
  max_progress: number;
  is_earned: boolean;
  earned_at?: string;
}

export interface Achievement {
  id: string;
  title: string;
  description: string;
  icon: string;
  category: 'speed' | 'accuracy' | 'consistency' | 'mastery';
  progress: number;
  max_progress: number;
  reward_points: number;
  is_unlocked: boolean;
}

export class GamificationService {
  /**
   * Récupère tous les badges d'un étudiant
   */
  static async getStudentBadges(
    token: string,
    studentId: number
  ): Promise<Badge[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/remediation/badges/student/${studentId}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Erreur lors de la récupération des badges');
      }

      const badges = await response.json();
      console.log('✅ [GAMIFICATION] Badges récupérés:', badges);
      return badges;
    } catch (error) {
      console.error('❌ [GAMIFICATION] Erreur récupération badges:', error);
      return [];
    }
  }

  /**
   * Récupère les badges disponibles et le progrès
   */
  static async getAvailableBadges(
    token: string,
    studentId: number
  ): Promise<BadgeProgress[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/remediation/badges/available/${studentId}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Erreur lors de la récupération des badges disponibles');
      }

      const data = await response.json();
      console.log('✅ [GAMIFICATION] Badges disponibles récupérés:', data);
      
      // Transformer en format BadgeProgress
      const badgeProgress: BadgeProgress[] = data.available_badges.map((badge: any) => ({
        type: badge.type,
        name: badge.name,
        description: badge.description,
        icon: badge.icon,
        condition: badge.condition,
        progress: 0,
        max_progress: 1,
        is_earned: false,
      }));

      return badgeProgress;
    } catch (error) {
      console.error('❌ [GAMIFICATION] Erreur récupération badges disponibles:', error);
      return [];
    }
  }

  /**
   * Calcule le progrès vers les badges
   */
  static calculateBadgeProgress(
    badges: Badge[],
    remediationResults: any[],
    progress: any[]
  ): BadgeProgress[] {
    const allBadges = [
      {
        type: "first_quiz",
        name: "Premier Quiz",
        description: "Complétez votre premier quiz de remédiation",
        icon: "🎯",
        condition: "Compléter 1 quiz",
        max_progress: 1
      },
      {
        type: "perfect_score",
        name: "Score Parfait",
        description: "Obtenez 100% sur un exercice",
        icon: "⭐",
        condition: "Score de 100%",
        max_progress: 1
      },
      {
        type: "speed_learner",
        name: "Apprenant Rapide",
        description: "Complétez un exercice en moins de 2 minutes",
        icon: "⚡",
        condition: "Temps < 2 minutes",
        max_progress: 1
      },
      {
        type: "topic_master",
        name: "Maître du Domaine",
        description: "Maîtrisez complètement un domaine (niveau 10)",
        icon: "👑",
        condition: "Niveau 10 dans un domaine",
        max_progress: 1
      },
      {
        type: "consistency",
        name: "Régularité",
        description: "Complétez 5 exercices consécutifs",
        icon: "📈",
        condition: "5 exercices consécutifs",
        max_progress: 5
      },
      {
        type: "improvement",
        name: "Progrès Constant",
        description: "Améliorez votre niveau de 3 points",
        icon: "🚀",
        condition: "Amélioration de 3 niveaux",
        max_progress: 3
      }
    ];

    return allBadges.map(badge => {
      const earnedBadge = badges.find(b => b.badge_type === badge.type);
      let currentProgress = 0;

      switch (badge.type) {
        case "first_quiz":
          currentProgress = remediationResults.length > 0 ? 1 : 0;
          break;
        case "perfect_score":
          currentProgress = remediationResults.filter(r => r.percentage === 100).length;
          break;
        case "speed_learner":
          currentProgress = remediationResults.filter(r => r.time_spent < 120).length;
          break;
        case "topic_master":
          currentProgress = progress.filter(p => p.current_level >= 10).length;
          break;
        case "consistency":
          currentProgress = Math.min(5, remediationResults.length);
          break;
        case "improvement":
          currentProgress = progress.reduce((sum, p) => sum + Math.max(0, p.improvement), 0);
          break;
      }

      return {
        ...badge,
        progress: Math.min(currentProgress, badge.max_progress),
        is_earned: !!earnedBadge,
        earned_at: earnedBadge?.earned_at
      };
    });
  }

  /**
   * Génère des achievements basés sur les performances
   */
  static generateAchievements(
    remediationResults: any[],
    progress: any[]
  ): Achievement[] {
    const achievements: Achievement[] = [];

    // Achievement: Speed Demon
    const avgTime = remediationResults.length > 0 
      ? remediationResults.reduce((sum, r) => sum + r.time_spent, 0) / remediationResults.length 
      : 0;
    
    if (avgTime < 180) { // Moins de 3 minutes en moyenne
      achievements.push({
        id: "speed_demon",
        title: "Démon de la Vitesse",
        description: "Complétez les exercices en moins de 3 minutes en moyenne",
        icon: "🏃‍♂️",
        category: "speed",
        progress: Math.max(0, 180 - avgTime),
        max_progress: 180,
        reward_points: 50,
        is_unlocked: true
      });
    }

    // Achievement: Accuracy Master
    const avgScore = remediationResults.length > 0 
      ? remediationResults.reduce((sum, r) => sum + r.percentage, 0) / remediationResults.length 
      : 0;
    
    if (avgScore >= 85) {
      achievements.push({
        id: "accuracy_master",
        title: "Maître de la Précision",
        description: "Maintenez un score moyen de 85% ou plus",
        icon: "🎯",
        category: "accuracy",
        progress: avgScore,
        max_progress: 100,
        reward_points: 75,
        is_unlocked: true
      });
    }

    // Achievement: Consistency King
    if (remediationResults.length >= 10) {
      achievements.push({
        id: "consistency_king",
        title: "Roi de la Régularité",
        description: "Complétez au moins 10 exercices de remédiation",
        icon: "👑",
        category: "consistency",
        progress: Math.min(20, remediationResults.length),
        max_progress: 20,
        reward_points: 100,
        is_unlocked: true
      });
    }

    // Achievement: Domain Master
    const masteredTopics = progress.filter(p => p.current_level >= 8).length;
    if (masteredTopics > 0) {
      achievements.push({
        id: "domain_master",
        title: "Maître des Domaines",
        description: `Maîtrisez ${masteredTopics} domaine(s) à un niveau élevé`,
        icon: "🌟",
        category: "mastery",
        progress: masteredTopics,
        max_progress: 3,
        reward_points: 150,
        is_unlocked: true
      });
    }

    return achievements;
  }

  /**
   * Calcule le niveau de gamification global
   */
  static calculateGamificationLevel(
    badges: Badge[],
    achievements: Achievement[],
    totalExercises: number
  ): {
    level: number;
    title: string;
    progress: number;
    nextLevel: number;
    totalPoints: number;
  } {
    const totalPoints = badges.length * 25 + achievements.reduce((sum, a) => sum + a.reward_points, 0);
    const level = Math.floor(totalPoints / 100) + 1;
    const progress = totalPoints % 100;
    const nextLevel = level + 1;

    const titles = [
      "Débutant", "Apprenti", "Étudiant", "Élève Avancé", "Expert",
      "Maître", "Grand Maître", "Légende", "Mythique", "Divin"
    ];

    return {
      level,
      title: titles[Math.min(level - 1, titles.length - 1)],
      progress,
      nextLevel,
      totalPoints
    };
  }

  /**
   * Génère des notifications de récompenses
   */
  static generateRewardNotifications(
    newBadges: Badge[],
    newAchievements: Achievement[]
  ): string[] {
    const notifications: string[] = [];

    newBadges.forEach(badge => {
      notifications.push(`🎉 Nouveau badge débloqué : ${badge.badge_name} !`);
    });

    newAchievements.forEach(achievement => {
      notifications.push(`🏆 Achievement débloqué : ${achievement.title} !`);
    });

    return notifications;
  }

  /**
   * Sauvegarde les préférences de gamification
   */
  static saveGamificationPreferences(
    studentId: number,
    preferences: {
      showNotifications: boolean;
      soundEnabled: boolean;
      theme: 'light' | 'dark' | 'auto';
    }
  ): void {
    try {
      localStorage.setItem(`gamification_prefs_${studentId}`, JSON.stringify(preferences));
    } catch (error) {
      console.error('❌ [GAMIFICATION] Erreur sauvegarde préférences:', error);
    }
  }

  /**
   * Récupère les préférences de gamification
   */
  static getGamificationPreferences(studentId: number): {
    showNotifications: boolean;
    soundEnabled: boolean;
    theme: 'light' | 'dark' | 'auto';
  } {
    try {
      const stored = localStorage.getItem(`gamification_prefs_${studentId}`);
      if (stored) {
        return JSON.parse(stored);
      }
    } catch (error) {
      console.error('❌ [GAMIFICATION] Erreur récupération préférences:', error);
    }

    return {
      showNotifications: true,
      soundEnabled: true,
      theme: 'auto'
    };
  }
}








