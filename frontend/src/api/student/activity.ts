import { apiClient } from '../apiClient';

export interface Activity {
  id: number;
  type: string;
  description: string;
  details: any;
  created_at: string;
  duration: number;
  score: number;
  quiz_title?: string;
  subject?: string;
  score_percentage?: number;
}

export interface ActivityStats {
  user_id: number;
  period: string;
  quiz_stats: {
    total_quizzes: number;
    average_score: number;
    total_duration: number;
  };
  learning_stats: {
    total_sessions: number;
    total_study_time: number;
  };
  daily_activities: Array<{
    date: string;
    count: number;
  }>;
}

export interface ActivityTimeline {
  user_id: number;
  timeline: Record<string, Activity[]>;
  days: number;
}

export interface ActivityAchievement {
  type: string;
  title: string;
  description: string;
  achieved: boolean;
  achieved_at?: string;
  count?: number;
  study_time?: number;
  streak_days?: number;
}

export interface ActivityAchievements {
  user_id: number;
  achievements: ActivityAchievement[];
  total_achievements: number;
}

// Récupérer l'activité récente d'un utilisateur
export const fetchRecentActivity = async (userId: number, limit: number = 10): Promise<{
  user_id: number;
  activities: Activity[];
  total_count: number;
}> => {
  const response = await apiClient.get(`/api/v1/activity/user/${userId}/recent?limit=${limit}`);
  return response.data;
};

// Récupérer les statistiques d'activité
export const fetchActivityStats = async (userId: number, period: string = 'week'): Promise<ActivityStats> => {
  const response = await apiClient.get(`/api/v1/activity/user/${userId}/stats?period=${period}`);
  return response.data;
};

// Enregistrer une nouvelle activité
export const logActivity = async (userId: number, activityData: {
  type: string;
  description: string;
  details?: any;
  duration?: number;
  score?: number;
  related_id?: number;
}) => {
  const response = await apiClient.post(`/api/v1/activity/user/${userId}/log`, activityData);
  return response.data;
};

// Récupérer la timeline d'activité
export const fetchActivityTimeline = async (userId: number, days: number = 7): Promise<ActivityTimeline> => {
  const response = await apiClient.get(`/api/v1/activity/user/${userId}/timeline?days=${days}`);
  return response.data;
};

// Récupérer les achievements basés sur l'activité
export const fetchActivityAchievements = async (userId: number): Promise<ActivityAchievements> => {
  const response = await apiClient.get(`/api/v1/activity/user/${userId}/achievements`);
  return response.data;
};

// Supprimer une activité
export const deleteActivity = async (userId: number, activityId: number) => {
  const response = await apiClient.delete(`/api/v1/activity/user/${userId}/activity/${activityId}`);
  return response.data;
}; 