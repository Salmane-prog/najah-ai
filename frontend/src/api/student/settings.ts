import { apiClient } from '../apiClient';

export interface UserSettings {
  id: number;
  user_id: number;
  theme: string;
  language: string;
  notifications_enabled: boolean;
  email_notifications: boolean;
  push_notifications: boolean;
  study_reminders: boolean;
  privacy_level: string;
  show_progress: boolean;
  show_leaderboard: boolean;
  daily_goal: number;
  weekly_goal: number;
  difficulty_preference: string;
  auto_save: boolean;
  created_at: string;
  updated_at: string;
}

export interface PrivacySettings {
  privacy_level: string;
  show_progress: boolean;
  show_leaderboard: boolean;
}

export interface NotificationSettings {
  notifications_enabled: boolean;
  email_notifications: boolean;
  push_notifications: boolean;
  study_reminders: boolean;
}

export interface UserGoals {
  daily_goal: number;
  weekly_goal: number;
  difficulty_preference: string;
}

// Récupérer les réglages d'un utilisateur
export const fetchUserSettings = async (userId: number): Promise<UserSettings> => {
  const response = await apiClient.get(`/api/v1/settings/user/${userId}`);
  return response.data;
};

// Mettre à jour les réglages d'un utilisateur
export const updateUserSettings = async (userId: number, settings: Partial<UserSettings>) => {
  const response = await apiClient.put(`/api/v1/settings/user/${userId}`, settings);
  return response.data;
};

// Récupérer les paramètres de confidentialité
export const fetchPrivacySettings = async (userId: number): Promise<PrivacySettings> => {
  const response = await apiClient.get(`/api/v1/settings/user/${userId}/privacy`);
  return response.data;
};

// Mettre à jour les paramètres de confidentialité
export const updatePrivacySettings = async (userId: number, privacy: Partial<PrivacySettings>) => {
  const response = await apiClient.put(`/api/v1/settings/user/${userId}/privacy`, privacy);
  return response.data;
};

// Récupérer les paramètres de notifications
export const fetchNotificationSettings = async (userId: number): Promise<NotificationSettings> => {
  const response = await apiClient.get(`/api/v1/settings/user/${userId}/notifications`);
  return response.data;
};

// Mettre à jour les paramètres de notifications
export const updateNotificationSettings = async (userId: number, notifications: Partial<NotificationSettings>) => {
  const response = await apiClient.put(`/api/v1/settings/user/${userId}/notifications`, notifications);
  return response.data;
};

// Récupérer les objectifs d'un utilisateur
export const fetchUserGoals = async (userId: number): Promise<UserGoals> => {
  const response = await apiClient.get(`/api/v1/settings/user/${userId}/goals`);
  return response.data;
};

// Mettre à jour les objectifs d'un utilisateur
export const updateUserGoals = async (userId: number, goals: Partial<UserGoals>) => {
  const response = await apiClient.put(`/api/v1/settings/user/${userId}/goals`, goals);
  return response.data;
}; 