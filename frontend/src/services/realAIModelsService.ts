import { AIModel, ModelTrainingSession, ModelPrediction, ModelPerformance } from '../types/aiModels';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class RealAIModelsService {
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

  async getRealAIModels(): Promise<AIModel[]> {
    try {
      const data = await this.makeAuthenticatedRequest('/api/v1/ai-models/ai_models/');
      if (data) {
        console.log('✅ Modèles IA réels récupérés du backend');
        return data;
      }
    } catch (error) {
      console.warn('Erreur lors de la récupération des modèles IA réels:', error);
    }

    // Fallback vers les données par défaut
    console.log('🔄 Utilisation des modèles IA par défaut');
    return this.getDefaultAIModels();
  }

  async getModelDetails(modelId: number): Promise<AIModel | null> {
    try {
      const data = await this.makeAuthenticatedRequest(`/api/v1/ai-models/ai_models/${modelId}`);
      if (data) {
        console.log('✅ Détails du modèle IA récupérés du backend');
        return data;
      }
    } catch (error) {
      console.warn('Erreur lors de la récupération des détails du modèle IA:', error);
    }

    // Fallback vers les données par défaut
    console.log('🔄 Utilisation des détails du modèle IA par défaut');
    return this.getDefaultAIModelById(modelId);
  }

  async getTrainingSessions(): Promise<ModelTrainingSession[]> {
    try {
      const data = await this.makeAuthenticatedRequest('/api/v1/ai-models/ai_models/training-sessions/');
      if (data) {
        console.log('✅ Sessions d\'entraînement réelles récupérées du backend');
        return data;
      }
    } catch (error) {
      console.warn('Erreur lors de la récupération des sessions d\'entraînement réelles:', error);
    }

    // Fallback vers les données par défaut
    console.log('🔄 Utilisation des sessions d\'entraînement par défaut');
    return this.getDefaultTrainingSessions();
  }

  async getModelPredictions(): Promise<ModelPrediction[]> {
    try {
      const data = await this.makeAuthenticatedRequest('/api/v1/ai-models/ai_models/predictions/');
      if (data) {
        console.log('✅ Prédictions du modèle réelles récupérées du backend');
        return data;
      }
    } catch (error) {
      console.warn('Erreur lors de la récupération des prédictions du modèle réelles:', error);
    }

    // Fallback vers les données par défaut
    console.log('🔄 Utilisation des prédictions du modèle par défaut');
    return this.getDefaultModelPredictions();
  }

  async getModelPerformance(): Promise<ModelPerformance[]> {
    try {
      const data = await this.makeAuthenticatedRequest('/api/v1/ai-models/ai_models/performance/');
      if (data) {
        console.log('✅ Performance du modèle réelle récupérée du backend');
        return data;
      }
    } catch (error) {
      console.warn('Erreur lors de la récupération de la performance du modèle réelle:', error);
    }

    // Fallback vers les données par défaut
    console.log('🔄 Utilisation de la performance du modèle par défaut');
    return this.getDefaultModelPerformance();
  }

  async startModelTraining(modelId: number): Promise<boolean> {
    try {
      const data = await this.makeAuthenticatedRequest(`/api/v1/ai-models/ai_models/${modelId}/train`, {
        method: 'POST'
      });
      if (data) {
        console.log('✅ Entraînement du modèle démarré avec succès');
        return true;
      }
    } catch (error) {
      console.warn('Erreur lors du démarrage de l\'entraînement du modèle:', error);
    }

    return false;
  }

  async deployModel(modelId: number): Promise<boolean> {
    try {
      const data = await this.makeAuthenticatedRequest(`/api/v1/ai-models/ai_models/${modelId}/deploy`, {
        method: 'POST'
      });
      if (data) {
        console.log('✅ Modèle déployé avec succès');
        return true;
      }
    } catch (error) {
      console.warn('Erreur lors du déploiement du modèle:', error);
    }

    return false;
  }

  // Données par défaut (fallback)
  private getDefaultAIModels(): AIModel[] {
    return [
      {
        id: 1,
        name: "Modèle de Prédiction de Performance",
        description: "Modèle ML pour prédire les performances des étudiants",
        model_type: "neural_network",
        version: "2.1.0",
        accuracy: 87.5,
        is_active: true,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      },
      {
        id: 2,
        name: "Modèle de Détection de Blocages",
        description: "Modèle pour identifier les difficultés d'apprentissage",
        model_type: "random_forest",
        version: "1.8.2",
        accuracy: 82.3,
        is_active: true,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      },
      {
        id: 3,
        name: "Modèle de Recommandations",
        description: "Système de recommandations personnalisées",
        model_type: "collaborative_filtering",
        version: "1.5.0",
        accuracy: 79.8,
        is_active: false,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      }
    ];
  }

  private getDefaultAIModelById(modelId: number): AIModel | null {
    const models = this.getDefaultAIModels();
    return models.find(model => model.id === modelId) || null;
  }

  private getDefaultTrainingSessions(): ModelTrainingSession[] {
    return [
      {
        id: 1,
        model_id: 1,
        status: "completed",
        training_data_source: "student_performance_data",
        training_data_size: 5000,
        validation_data_size: 1000,
        epochs: 100,
        batch_size: 32,
        learning_rate: 0.001,
        optimizer: "adam",
        loss_function: "binary_crossentropy",
        training_accuracy: 89.2,
        validation_accuracy: 87.5,
        training_loss: 0.23,
        validation_loss: 0.31,
        started_at: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
        completed_at: new Date().toISOString(),
        created_at: new Date().toISOString()
      },
      {
        id: 2,
        model_id: 2,
        status: "training",
        training_data_source: "learning_patterns_data",
        training_data_size: 3000,
        validation_data_size: 600,
        epochs: 50,
        batch_size: 64,
        learning_rate: 0.01,
        optimizer: "sgd",
        loss_function: "categorical_crossentropy",
        training_accuracy: 0,
        validation_accuracy: 0,
        training_loss: 0,
        validation_loss: 0,
        started_at: new Date().toISOString(),
        completed_at: null,
        created_at: new Date().toISOString()
      }
    ];
  }

  private getDefaultModelPredictions(): ModelPrediction[] {
    return [
      {
        id: 1,
        model_id: 1,
        student_id: 1,
        prediction_type: "performance",
        predicted_value: 85.5,
        confidence: 0.87,
        actual_value: 87.2,
        created_at: new Date().toISOString()
      },
      {
        id: 2,
        model_id: 1,
        student_id: 2,
        prediction_type: "performance",
        predicted_value: 78.3,
        confidence: 0.82,
        actual_value: 79.1,
        created_at: new Date().toISOString()
      }
    ];
  }

  private getDefaultModelPerformance(): ModelPerformance[] {
    return [
      {
        id: 1,
        model_id: 1,
        metric_name: "accuracy",
        metric_value: 87.5,
        timestamp: new Date().toISOString()
      },
      {
        id: 2,
        model_id: 1,
        metric_name: "precision",
        metric_value: 85.2,
        timestamp: new Date().toISOString()
      },
      {
        id: 3,
        model_id: 1,
        metric_name: "recall",
        metric_value: 88.7,
        timestamp: new Date().toISOString()
      }
    ];
  }
}

// Fonctions avec fallback pour l'export
export async function getRealAIModelsWithFallback(token: string) {
  try {
    const service = new RealAIModelsService();
    return await service.getRealAIModels();
  } catch (error) {
    console.warn('Erreur lors de la récupération des modèles IA, utilisation du fallback:', error);
    const service = new RealAIModelsService();
    return service.getDefaultAIModels();
  }
}

export async function getTrainingSessionsWithFallback(token: string) {
  try {
    const service = new RealAIModelsService();
    return await service.getTrainingSessions();
  } catch (error) {
    console.warn('Erreur lors de la récupération des sessions d\'entraînement, utilisation du fallback:', error);
    const service = new RealAIModelsService();
    return service.getDefaultTrainingSessions();
  }
}

export async function getModelPredictionsWithFallback(token: string) {
  try {
    const service = new RealAIModelsService();
    return await service.getModelPredictions();
  } catch (error) {
    console.warn('Erreur lors de la récupération des prédictions, utilisation du fallback:', error);
    const service = new RealAIModelsService();
    return service.getDefaultModelPredictions();
  }
}

export const realAIModelsService = new RealAIModelsService();
export default realAIModelsService;

