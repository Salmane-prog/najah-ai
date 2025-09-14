import { apiClient } from '../apiClient';

export interface AIRecommendation {
  id: number;
  user_id: number;
  recommendation_type: string;
  title: string;
  description?: string;
  content_id?: number;
  quiz_id?: number;
  learning_path_id?: number;
  confidence_score: number;
  reason?: string;
  is_accepted: boolean;
  is_dismissed: boolean;
  created_at: string;
}

export interface AITutoringSession {
  id: number;
  user_id: number;
  subject?: string;
  topic?: string;
  session_type: string;
  start_time: string;
  end_time?: string;
  duration?: number;
  status: string;
  notes?: string;
}

export interface AITutoringInteraction {
  id: number;
  session_id: number;
  user_message: string;
  ai_response: string;
  interaction_type: string;
  timestamp: string;
  user_satisfaction?: number;
}

export interface DifficultyDetection {
  id: number;
  user_id: number;
  subject: string;
  topic: string;
  difficulty_level: string;
  confidence_score: number;
  evidence?: any;
  detected_at: string;
  is_resolved: boolean;
  resolution_notes?: string;
}

export interface LearningAnalytics {
  id: number;
  user_id: number;
  analytics_type: string;
  data: any;
  insights?: string;
  recommendations?: any;
  created_at: string;
}

export interface AdaptiveContent {
  id: number;
  user_id: number;
  content_id: number;
  adaptation_type: string;
  original_content: any;
  adapted_content: any;
  adaptation_reason: string;
  created_at: string;
}

export interface CreateAIRecommendationData {
  recommendation_type: string;
  title: string;
  description?: string;
  content_id?: number;
  quiz_id?: number;
  learning_path_id?: number;
  confidence_score?: number;
  reason?: string;
}

export interface CreateAITutoringSessionData {
  subject?: string;
  topic?: string;
  session_type?: string;
}

export interface CreateAITutoringInteractionData {
  user_message: string;
  interaction_type?: string;
}

export interface CreateDifficultyDetectionData {
  subject: string;
  topic: string;
  difficulty_level: string;
  confidence_score?: number;
  evidence?: any;
}

class AIAdvancedAPI {
  // Recommandations IA
  async getAIRecommendations(recommendation_type?: string, limit?: number): Promise<AIRecommendation[]> {
    const params = new URLSearchParams();
    if (recommendation_type) params.append('recommendation_type', recommendation_type);
    if (limit) params.append('limit', limit.toString());
    
    return this.request(`/api/v1/ai-advanced/recommendations?${params.toString()}`);
  }

  async acceptAIRecommendation(recommendationId: number): Promise<void> {
    return this.request(`/api/v1/ai-advanced/recommendations/${recommendationId}/accept`, {
      method: 'POST',
    });
  }

  async dismissAIRecommendation(recommendationId: number): Promise<void> {
    return this.request(`/api/v1/ai-advanced/recommendations/${recommendationId}/dismiss`, {
      method: 'POST',
    });
  }

  // Sessions de tutorat IA
  async getAITutoringSessions(status?: string): Promise<AITutoringSession[]> {
    const params = new URLSearchParams();
    if (status) params.append('status', status);
    
    return this.request(`/api/v1/ai-advanced/tutoring/sessions?${params.toString()}`);
  }

  async createAITutoringSession(data: CreateAITutoringSessionData): Promise<AITutoringSession> {
    return this.request('/api/v1/ai-advanced/tutoring/sessions', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getAITutoringInteractions(sessionId: number): Promise<AITutoringInteraction[]> {
    return this.request(`/api/v1/ai-advanced/tutoring/sessions/${sessionId}/interactions`);
  }

  async createAITutoringInteraction(sessionId: number, data: CreateAITutoringInteractionData): Promise<AITutoringInteraction> {
    return this.request(`/api/v1/ai-advanced/tutoring/sessions/${sessionId}/interactions`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Détection de difficultés
  async getDifficultyDetections(subject?: string, is_resolved?: boolean): Promise<DifficultyDetection[]> {
    const params = new URLSearchParams();
    if (subject) params.append('subject', subject);
    if (is_resolved !== undefined) params.append('is_resolved', is_resolved.toString());
    
    return this.request(`/api/v1/ai-advanced/difficulty-detection?${params.toString()}`);
  }

  async createDifficultyDetection(data: CreateDifficultyDetectionData): Promise<DifficultyDetection> {
    return this.request('/api/v1/ai-advanced/difficulty-detection', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async resolveDifficultyDetection(detectionId: number, resolution_notes?: string): Promise<void> {
    const body = resolution_notes ? JSON.stringify({ resolution_notes }) : undefined;
    return this.request(`/api/v1/ai-advanced/difficulty-detection/${detectionId}/resolve`, {
      method: 'PUT',
      body,
    });
  }

  // Analytics d'apprentissage
  async getPerformanceAnalytics(subject?: string, period?: string): Promise<any> {
    const params = new URLSearchParams();
    if (subject) params.append('subject', subject);
    if (period) params.append('period', period);
    
    return this.request(`/api/v1/ai-advanced/analytics/performance?${params.toString()}`);
  }

  async getEngagementAnalytics(period?: string): Promise<any> {
    const params = new URLSearchParams();
    if (period) params.append('period', period);
    
    return this.request(`/api/v1/ai-advanced/analytics/engagement?${params.toString()}`);
  }

  private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const response = await apiClient.request<T>(endpoint, options);
    return response.data;
  }
}

export const aiAdvancedAPI = new AIAdvancedAPI();
