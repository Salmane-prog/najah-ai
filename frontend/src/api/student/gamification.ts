import { apiClient } from '../apiClient';

export interface UserPoints {
  user_id: number;
  total_points: number;
  achievements_points: number;
  challenges_points: number;
}

export interface Achievement {
  id: number;
  name: string;
  description: string;
  points: number;
  icon: string;
  category: string;
  unlocked: boolean;
  unlocked_at?: string;
  progress: {
    current: number;
    target: number;
  };
  completed: boolean;
}

export interface Challenge {
  id: number;
  name: string;
  description: string;
  points: number;
  icon: string;
  category: string;
  completed: boolean;
  completed_at?: string;
  progress: {
    current: number;
    target: number;
  };
  active: boolean;
}

export interface UserAchievements {
  user_id: number;
  achievements: Achievement[];
  total_achievements: number;
  unlocked_count: number;
}

export interface UserChallenges {
  user_id: number;
  challenges: Challenge[];
  total_challenges: number;
  completed_count: number;
}

export interface LeaderboardEntry {
  user_id: number;
  username: string;
  total_points: number;
  level: number;
}

export interface Leaderboard {
  leaderboard: LeaderboardEntry[];
  user_rank: number | null;
}

// Récupérer les points d'un utilisateur
export const fetchUserPoints = async (userId: number): Promise<UserPoints> => {
  const response = await apiClient.get(`/api/v1/gamification/test/user/${userId}/points`);
  return response.data;
};

// Récupérer les achievements d'un utilisateur
export const fetchUserAchievements = async (userId: number): Promise<UserAchievements> => {
  const response = await apiClient.get(`/api/v1/gamification/test/user/${userId}/achievements`);
  return response.data;
};

// Récupérer les challenges d'un utilisateur
export const fetchUserChallenges = async (userId: number): Promise<UserChallenges> => {
  const response = await apiClient.get(`/api/v1/gamification/test/user/${userId}/challenges`);
  return response.data;
};

// Débloquer un achievement
export const unlockAchievement = async (userId: number, achievementId: number) => {
  const response = await apiClient.post(`/api/v1/gamification/user/${userId}/achievements/${achievementId}/unlock`);
  return response.data;
};

// Compléter un challenge
export const completeChallenge = async (userId: number, challengeId: number) => {
  const response = await apiClient.post(`/api/v1/gamification/user/${userId}/challenges/${challengeId}/complete`);
  return response.data;
};

// Récupérer le leaderboard
export const fetchLeaderboard = async (): Promise<Leaderboard> => {
  const response = await apiClient.get('/api/v1/gamification/test/leaderboard');
  return response.data;
};

// Récupérer le niveau d'un utilisateur
export const fetchUserLevel = async (userId: number) => {
  const response = await apiClient.get(`/api/v1/gamification/test/user/${userId}/level`);
  return response.data;
}; 