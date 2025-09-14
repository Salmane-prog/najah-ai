import { AIAnalyticsData, LearningAnalytics, AIPredictions, BlockageDetection, LearningPatterns, AIRecommendations } from '../types/aiAnalytics';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class AIAnalyticsService {
  private async makeAuthenticatedRequest(endpoint: string, options: RequestInit = {}) {
    // Récupérer le token depuis localStorage ou session
    const token = localStorage.getItem('authToken') || sessionStorage.getItem('authToken');
    
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      if (response.status === 401) {
        // Token expiré ou invalide
        console.warn('Token expiré ou invalide, utilisation des données par défaut');
        return null;
      } else if (response.status === 403) {
        // Permissions insuffisantes
        console.warn('Permissions insuffisantes, utilisation des données par défaut');
        return null;
      } else if (response.status === 404) {
        // Endpoint non trouvé
        console.warn('Endpoint non trouvé, utilisation des données par défaut');
        return null;
      } else {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }
    }

    return response.json();
  }

  async getAIAnalyticsData(): Promise<AIAnalyticsData> {
    try {
      const data = await this.makeAuthenticatedRequest('/api/v1/ai-analytics/ai-analytics/');
      if (data) {
        console.log('✅ Données AI Analytics réelles récupérées du backend');
        return data;
      }
    } catch (error) {
      console.warn('Erreur lors de la récupération des données AI Analytics réelles:', error);
    }

    // Fallback vers les données par défaut
    console.log('🔄 Utilisation des données AI Analytics par défaut');
    return this.getDefaultAIAnalyticsData();
  }

  async getLearningAnalytics(studentId: number): Promise<LearningAnalytics> {
    try {
      const data = await this.makeAuthenticatedRequest(`/api/v1/ai-analytics/ai-analytics/learning-analytics`);
      if (data) {
        console.log('✅ Learning Analytics réelles récupérées du backend');
        return data;
      }
    } catch (error) {
      console.warn('Erreur lors de la récupération des Learning Analytics réelles:', error);
    }

    // Fallback vers les données par défaut
    console.log('🔄 Utilisation des Learning Analytics par défaut');
    return this.getDefaultLearningAnalytics();
  }

  async getAIPredictions(studentId: number): Promise<AIPredictions> {
    try {
      const data = await this.makeAuthenticatedRequest(`/api/v1/ai-analytics/ai-analytics/predictions`);
      if (data) {
        console.log('✅ Prédictions IA réelles récupérées du backend');
        return data;
      }
    } catch (error) {
      console.warn('Erreur lors de la récupération des prédictions IA réelles:', error);
    }

    // Fallback vers les données par défaut
    console.log('🔄 Utilisation des prédictions IA par défaut');
    return this.getDefaultAIPredictions();
  }

  async getBlockageDetections(studentId: number): Promise<BlockageDetection> {
    try {
      const data = await this.makeAuthenticatedRequest(`/api/v1/ai-analytics/ai-analytics/blockages`);
      if (data) {
        console.log('✅ Détections de blocages réelles récupérées du backend');
        return data;
      }
    } catch (error) {
      console.warn('Erreur lors de la récupération des détections de blocages réelles:', error);
    }

    // Fallback vers les données par défaut
    console.log('🔄 Utilisation des détections de blocages par défaut');
    return this.getDefaultBlockageDetection();
  }

  async getLearningPatterns(studentId: number): Promise<LearningPatterns> {
    try {
      const data = await this.makeAuthenticatedRequest(`/api/v1/ai-analytics/ai-analytics/patterns`);
      if (data) {
        console.log('✅ Patterns d\'apprentissage réels récupérés du backend');
        return data;
      }
    } catch (error) {
      console.warn('Erreur lors de la récupération des patterns d\'apprentissage réels:', error);
    }

    // Fallback vers les données par défaut
    console.log('🔄 Utilisation des patterns d\'apprentissage par défaut');
    return this.getDefaultLearningPatterns();
  }

  async getAIRecommendations(studentId: number): Promise<AIRecommendations> {
    try {
      const data = await this.makeAuthenticatedRequest(`/api/v1/ai-analytics/ai-analytics/recommendations`);
      if (data) {
        console.log('✅ Recommandations IA réelles récupérées du backend');
        return data;
      }
    } catch (error) {
      console.warn('Erreur lors de la récupération des recommandations IA réelles:', error);
    }

    // Fallback vers les données par défaut
    console.log('🔄 Utilisation des recommandations IA par défaut');
    return this.getDefaultAIRecommendations();
  }

  // Données par défaut (fallback)
  private getDefaultAIAnalyticsData(): AIAnalyticsData {
    return {
      overview: {
        total_models: 5,
        active_models: 3,
        total_predictions: 1250,
        accuracy_rate: 87.5
      },
      recent_activity: [
        {
          id: 1,
          type: "model_training",
          description: "Modèle de prédiction de performance entraîné",
          timestamp: new Date().toISOString(),
          status: "completed"
        },
        {
          id: 2,
          type: "prediction_generated",
          description: "Nouvelles prédictions générées pour 15 étudiants",
          timestamp: new Date().toISOString(),
          status: "completed"
        }
      ],
      performance_metrics: {
        model_accuracy: 87.5,
        prediction_speed: 2.3,
        data_quality: 94.2,
        user_satisfaction: 8.7
      }
    };
  }

  private getDefaultLearningAnalytics(): LearningAnalytics {
    return {
      student_id: 1,
      learning_patterns: [
        {
          pattern_type: "study_time",
          frequency: "daily",
          duration: 45,
          effectiveness: 8.5
        },
        {
          pattern_type: "subject_preference",
          frequency: "weekly",
          duration: 120,
          effectiveness: 9.2
        }
      ],
      progress_trends: [
        { date: "2024-01-15", score: 75, trend: "up" },
        { date: "2024-01-16", score: 78, trend: "up" },
        { date: "2024-01-17", score: 82, trend: "up" }
      ],
      engagement_metrics: {
        session_count: 15,
        time_spent: 675,
        resource_access: 28,
        interaction_rate: 85.5
      }
    };
  }

  private getDefaultAIPredictions(): AIPredictions {
    return {
      student_id: 1,
      predictions: [
        {
          type: "performance",
          predicted_score: 82.5,
          confidence: 0.87,
          timeframe: "next_week",
          factors: ["study_time", "previous_scores", "engagement"]
        },
        {
          type: "difficulty",
          predicted_level: "intermediate",
          confidence: 0.79,
          timeframe: "next_quiz",
          factors: ["current_progress", "learning_patterns"]
        }
      ],
      accuracy_history: [
        { date: "2024-01-10", accuracy: 0.85 },
        { date: "2024-01-12", accuracy: 0.87 },
        { date: "2024-01-15", accuracy: 0.89 }
      ]
    };
  }

  private getDefaultBlockageDetection(): BlockageDetection {
    return {
      student_id: 1,
      detected_blockages: [
        {
          id: 1,
          subject: "Mathématiques",
          concept: "Équations du premier degré",
          severity: "medium",
          confidence: 0.82,
          symptoms: ["Scores faibles", "Temps de réponse élevé"],
          suggested_interventions: ["Révision des concepts de base", "Exercices supplémentaires"]
        }
      ],
      resolution_progress: 65,
      intervention_history: [
        {
          date: "2024-01-15",
          intervention: "Révision des concepts de base",
          effectiveness: 7.5
        }
      ]
    };
  }

  private getDefaultLearningPatterns(): LearningPatterns {
    return {
      student_id: 1,
      patterns: [
        {
          id: 1,
          name: "Progression linéaire",
          description: "Les étudiants progressent de manière linéaire",
          confidence: 0.85,
          support_count: 150,
          impact_score: 0.75
        },
        {
          id: 2,
          name: "Préférence matin",
          description: "Meilleure performance le matin",
          confidence: 0.78,
          support_count: 120,
          impact_score: 0.68
        }
      ],
      insights: [
        "Tendance à la progression constante",
        "Pic de performance entre 9h et 11h",
        "Meilleure rétention avec des sessions courtes"
      ]
    };
  }

  private getDefaultAIRecommendations(): AIRecommendations {
    return {
      student_id: 1,
      recommendations: [
        {
          id: 1,
          type: "content",
          title: "Révision des équations",
          description: "Exercices supplémentaires sur les équations du premier degré",
          priority: "high",
          confidence: 0.89,
          expected_impact: 0.75
        },
        {
          id: 2,
          type: "study_method",
          title: "Sessions courtes",
          description: "Privilégier des sessions de 30 minutes plutôt que 2h",
          priority: "medium",
          confidence: 0.76,
          expected_impact: 0.65
        }
      ],
      implementation_status: {
        accepted: 2,
        pending: 1,
        rejected: 0,
        total: 3
      }
    };
  }
}

export const aiAnalyticsService = new AIAnalyticsService();
export default aiAnalyticsService;

