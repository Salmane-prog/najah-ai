import { apiClient } from '../apiClient';

export interface ScoreCorrection {
  id: number;
  user_id: number;
  quiz_result_id: number;
  original_score: number;
  corrected_score: number;
  score_adjustment: number;
  reason?: string;
  subject?: string;
  corrected_by: number;
  created_at: string;
  updated_at?: string;
}

export interface CorrectionStats {
  user_id: number;
  total_corrections: number;
  average_correction: number;
  corrections_by_subject: Array<{
    subject: string;
    count: number;
    average_adjustment: number;
  }>;
}

export interface CorrectionHistory {
  user_id: number;
  corrections: Array<{
    id: number;
    quiz_title: string;
    subject: string;
    original_score: number;
    corrected_score: number;
    adjustment: number;
    reason: string;
    created_at: string;
  }>;
  total_count: number;
}

// Récupérer les corrections d'un utilisateur
export const fetchUserCorrections = async (userId: number): Promise<{
  user_id: number;
  corrections: ScoreCorrection[];
  total_corrections: number;
}> => {
  const response = await apiClient.get(`/api/v1/score_corrections/user/${userId}/corrections`);
  return response.data;
};

// Récupérer les statistiques de corrections
export const fetchCorrectionStats = async (userId: number): Promise<CorrectionStats> => {
  const response = await apiClient.get(`/api/v1/score_corrections/user/${userId}/corrections/stats`);
  return response.data;
};

// Créer une correction de score
export const createScoreCorrection = async (userId: number, correctionData: {
  quiz_result_id: number;
  corrected_score: number;
  reason?: string;
}) => {
  const response = await apiClient.post(`/api/v1/score_corrections/user/${userId}/corrections`, correctionData);
  return response.data;
};

// Récupérer une correction spécifique
export const fetchScoreCorrection = async (userId: number, correctionId: number): Promise<ScoreCorrection> => {
  const response = await apiClient.get(`/api/v1/score_corrections/user/${userId}/corrections/${correctionId}`);
  return response.data;
};

// Mettre à jour une correction
export const updateScoreCorrection = async (userId: number, correctionId: number, correctionData: {
  corrected_score?: number;
  reason?: string;
}) => {
  const response = await apiClient.put(`/api/v1/score_corrections/user/${userId}/corrections/${correctionId}`, correctionData);
  return response.data;
};

// Supprimer une correction
export const deleteScoreCorrection = async (userId: number, correctionId: number) => {
  const response = await apiClient.delete(`/api/v1/score_corrections/user/${userId}/corrections/${correctionId}`);
  return response.data;
};

// Récupérer les corrections pour un quiz spécifique
export const fetchQuizCorrections = async (userId: number, quizResultId: number): Promise<{
  quiz_result_id: number;
  corrections: ScoreCorrection[];
  total_corrections: number;
}> => {
  const response = await apiClient.get(`/api/v1/score_corrections/user/${userId}/corrections/quiz/${quizResultId}`);
  return response.data;
};

// Récupérer l'historique des corrections
export const fetchCorrectionHistory = async (
  userId: number, 
  subject?: string, 
  limit: number = 20
): Promise<CorrectionHistory> => {
  const params = new URLSearchParams();
  if (subject) params.append('subject', subject);
  params.append('limit', limit.toString());
  
  const response = await apiClient.get(`/api/v1/score_corrections/user/${userId}/corrections/history?${params}`);
  return response.data;
}; 