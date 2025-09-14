// Service pour les modèles d'IA
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// ============================================================================
// INTERFACES
// ============================================================================

export interface AIModel {
  id: number;
  name: string;
  model_type: 'ml_algorithm' | 'neural_network' | 'expert_system';
  algorithm: string;
  version: string;
  description: string;
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
  mse: number;
  hyperparameters: Record<string, any>;
  model_config: Record<string, any>;
  feature_importance: Record<string, number>;
  training_data_size: number;
  training_duration: number;
  created_at: string;
  updated_at: string;
  is_active: boolean;
}

export interface ModelTrainingSession {
  id: number;
  model_id: number;
  session_name: string;
  training_data_source: string;
  training_data_size: number;
  validation_data_size: number;
  epochs: number;
  batch_size: number;
  learning_rate: number;
  optimizer: string;
  loss_function: string;
  training_accuracy: number;
  validation_accuracy: number;
  training_loss: number;
  validation_loss: number;
  started_at: string;
  completed_at?: string;
  status: 'running' | 'completed' | 'failed';
}

export interface ModelPrediction {
  id: number;
  model_id: number;
  student_id: number;
  input_features: Record<string, any>;
  prediction_type: string;
  predicted_value: number;
  confidence_score: number;
  prediction_interval: Record<string, number>;
  prediction_timestamp: string;
  processing_time: number;
}

export interface ModelDeployment {
  id: number;
  model_id: number;
  environment: string;
  deployment_url: string;
  deployment_config: Record<string, any>;
  scaling_config: Record<string, any>;
  monitoring_config: Record<string, any>;
  deployed_at: string;
  status: string;
  health_check: Record<string, any>;
}

export interface DataCollection {
  id: number;
  student_id: number;
  data_type: string;
  data_source: string;
  raw_data: Record<string, any>;
  processed_data: Record<string, any>;
  metadata: Record<string, any>;
  data_quality_score: number;
  completeness: number;
  accuracy: number;
  collected_at: string;
  processed_at?: string;
}

export interface LearningPatternAnalysis {
  id: number;
  student_id: number;
  pattern_type: string;
  pattern_data: Record<string, any>;
  confidence_score: number;
  pattern_strength: number;
  insights: string[];
  recommendations: string[];
  analyzed_at: string;
  last_updated: string;
}

export interface ContinuousImprovement {
  id: number;
  model_id: number;
  improvement_type: string;
  improvement_metric: number;
  improvement_percentage: number;
  user_feedback: Record<string, any>;
  validation_results: Record<string, any>;
  improvement_date: string;
  validated_at?: string;
}

// ============================================================================
// SERVICE PRINCIPAL
// ============================================================================

export class AIModelsService {
  private static API_BASE_URL = API_BASE_URL;

  /**
   * Récupérer tous les modèles d'IA
   */
  static async getAIModels(
    modelType?: string,
    algorithm?: string,
    isActive?: boolean,
    token: string
  ): Promise<AIModel[]> {
    try {
      const params = new URLSearchParams();
      if (modelType) params.append('model_type', modelType);
      if (algorithm) params.append('algorithm', algorithm);
      if (isActive !== undefined) params.append('is_active', isActive.toString());

      const response = await fetch(
        `${this.API_BASE_URL}/api/v1/ai-models/models?${params}`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      if (!response.ok) {
        if (response.status === 401 || response.status === 403 || response.status === 404) {
          console.warn(`Erreur ${response.status}, utilisation des données par défaut`);
          return this.getDefaultAIModels();
        }
        throw new Error(`Erreur lors de la récupération des modèles: ${response.status}`);
      }

      const data = await response.json();
      return data.models || [];
    } catch (error) {
      console.error('Erreur getAIModels:', error);
      return this.getDefaultAIModels();
    }
  }

  /**
   * Récupérer un modèle d'IA spécifique
   */
  static async getAIModel(
    modelId: number,
    token: string
  ): Promise<AIModel> {
    try {
      const response = await fetch(
        `${this.API_BASE_URL}/api/v1/ai-models/models/${modelId}`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      if (!response.ok) {
        throw new Error(`Erreur lors de la récupération du modèle: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Erreur getAIModel:', error);
      throw error;
    }
  }

  /**
   * Créer un nouveau modèle d'IA
   */
  static async createAIModel(
    modelData: {
      name: string;
      model_type: string;
      algorithm: string;
      version?: string;
      description?: string;
      hyperparameters?: Record<string, any>;
      model_config?: Record<string, any>;
      feature_importance?: Record<string, number>;
    },
    token: string
  ): Promise<{
    model_id: number;
    name: string;
    status: string;
    created_at: string;
  }> {
    try {
      const response = await fetch(
        `${this.API_BASE_URL}/api/v1/ai-models/models`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(modelData)
        }
      );

      if (!response.ok) {
        throw new Error(`Erreur lors de la création du modèle: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Erreur createAIModel:', error);
      throw error;
    }
  }

  /**
   * Mettre à jour un modèle d'IA
   */
  static async updateAIModel(
    modelId: number,
    modelData: Record<string, any>,
    token: string
  ): Promise<{
    model_id: number;
    name: string;
    status: string;
    updated_at: string;
  }> {
    try {
      const response = await fetch(
        `${this.API_BASE_URL}/api/v1/ai-models/models/${modelId}`,
        {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(modelData)
        }
      );

      if (!response.ok) {
        throw new Error(`Erreur lors de la mise à jour du modèle: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Erreur updateAIModel:', error);
      throw error;
    }
  }

  /**
   * Récupérer les sessions d'entraînement d'un modèle
   */
  static async getModelTrainingSessions(
    modelId: number,
    status?: string,
    token: string
  ): Promise<{
    model_id: number;
    training_sessions: ModelTrainingSession[];
  }> {
    try {
      const params = new URLSearchParams();
      if (status) params.append('status', status);

      const response = await fetch(
        `${this.API_BASE_URL}/api/v1/ai-models/models/${modelId}/training-sessions?${params}`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      if (!response.ok) {
        if (response.status === 401 || response.status === 403 || response.status === 404) {
          console.warn(`Erreur ${response.status}, utilisation des données par défaut`);
          return this.getDefaultTrainingSessions(modelId);
        }
        throw new Error(`Erreur lors de la récupération des sessions: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Erreur getModelTrainingSessions:', error);
      return this.getDefaultTrainingSessions(modelId);
    }
  }

  /**
   * Démarrer l'entraînement d'un modèle
   */
  static async startModelTraining(
    modelId: number,
    trainingConfig: {
      session_name?: string;
      training_data_source?: string;
      training_data_size?: number;
      validation_data_size?: number;
      epochs?: number;
      batch_size?: number;
      learning_rate?: number;
      optimizer?: string;
      loss_function?: string;
    },
    token: string
  ): Promise<{
    session_id: number;
    model_id: number;
    status: string;
    started_at: string;
  }> {
    try {
      const response = await fetch(
        `${this.API_BASE_URL}/api/v1/ai-models/models/${modelId}/train`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(trainingConfig)
        }
      );

      if (!response.ok) {
        throw new Error(`Erreur lors du démarrage de l'entraînement: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Erreur startModelTraining:', error);
      throw error;
    }
  }

  /**
   * Faire une prédiction avec un modèle
   */
  static async makePrediction(
    modelId: number,
    predictionData: {
      student_id: number;
      input_features: Record<string, any>;
      prediction_type: string;
      predicted_value?: number;
      confidence_score?: number;
      prediction_interval?: Record<string, number>;
      processing_time?: number;
    },
    token: string
  ): Promise<{
    prediction_id: number;
    model_id: number;
    predicted_value: number;
    confidence_score: number;
    prediction_interval: Record<string, number>;
    processing_time: number;
    prediction_timestamp: string;
  }> {
    try {
      const response = await fetch(
        `${this.API_BASE_URL}/api/v1/ai-models/models/${modelId}/predict`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(predictionData)
        }
      );

      if (!response.ok) {
        throw new Error(`Erreur lors de la prédiction: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Erreur makePrediction:', error);
      throw error;
    }
  }

  /**
   * Récupérer les déploiements d'un modèle
   */
  static async getModelDeployments(
    modelId: number,
    environment?: string,
    token: string
  ): Promise<{
    model_id: number;
    deployments: ModelDeployment[];
  }> {
    try {
      const params = new URLSearchParams();
      if (environment) params.append('environment', environment);

      const response = await fetch(
        `${this.API_BASE_URL}/api/v1/ai-models/models/${modelId}/deployments?${params}`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      if (!response.ok) {
        if (response.status === 401 || response.status === 403 || response.status === 404) {
          console.warn(`Erreur ${response.status}, utilisation des données par défaut`);
          return this.getDefaultDeployments(modelId);
        }
        throw new Error(`Erreur lors de la récupération des déploiements: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Erreur getModelDeployments:', error);
      return this.getDefaultDeployments(modelId);
    }
  }

  /**
   * Déployer un modèle
   */
  static async deployModel(
    modelId: number,
    deploymentConfig: {
      environment: string;
      deployment_url?: string;
      deployment_config?: Record<string, any>;
      scaling_config?: Record<string, any>;
      monitoring_config?: Record<string, any>;
    },
    token: string
  ): Promise<{
    deployment_id: number;
    model_id: number;
    environment: string;
    status: string;
    deployed_at: string;
  }> {
    try {
      const response = await fetch(
        `${this.API_BASE_URL}/api/v1/ai-models/models/${modelId}/deploy`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(deploymentConfig)
        }
      );

      if (!response.ok) {
        throw new Error(`Erreur lors du déploiement: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Erreur deployModel:', error);
      throw error;
    }
  }

  /**
   * Collecter des données d'apprentissage
   */
  static async collectLearningData(
    data: {
      student_id: number;
      data_type: string;
      data_source: string;
      raw_data?: Record<string, any>;
      processed_data?: Record<string, any>;
      metadata?: Record<string, any>;
      data_quality_score?: number;
      completeness?: number;
      accuracy?: number;
    },
    token: string
  ): Promise<{
    collection_id: number;
    student_id: number;
    data_type: string;
    status: string;
    collected_at: string;
  }> {
    try {
      const response = await fetch(
        `${this.API_BASE_URL}/api/v1/ai-models/data-collection`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        }
      );

      if (!response.ok) {
        throw new Error(`Erreur lors de la collecte de données: ${response.status}`);
      }

      const responseData = await response.json();
      return responseData;
    } catch (error) {
      console.error('Erreur collectLearningData:', error);
      throw error;
    }
  }

  /**
   * Analyser les patterns d'apprentissage
   */
  static async analyzeLearningPatterns(
    analysisRequest: {
      student_id: number;
      pattern_type: string;
      pattern_data?: Record<string, any>;
      confidence_score?: number;
      pattern_strength?: number;
      insights?: string[];
      recommendations?: string[];
    },
    token: string
  ): Promise<{
    analysis_id: number;
    student_id: number;
    pattern_type: string;
    confidence_score: number;
    pattern_strength: number;
    analyzed_at: string;
  }> {
    try {
      const response = await fetch(
        `${this.API_BASE_URL}/api/v1/ai-models/pattern-analysis`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(analysisRequest)
        }
      );

      if (!response.ok) {
        throw new Error(`Erreur lors de l'analyse des patterns: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Erreur analyzeLearningPatterns:', error);
      throw error;
    }
  }

  // ============================================================================
  // DONNÉES PAR DÉFAUT
  // ============================================================================

  private static getDefaultAIModels(): AIModel[] {
    return [
      {
        id: 1,
        name: "Modèle de Recommandation Français",
        model_type: "ml_algorithm",
        algorithm: "collaborative_filtering",
        version: "1.0",
        description: "Modèle de recommandation basé sur la collaboration entre utilisateurs",
        accuracy: 0.82,
        precision: 0.79,
        recall: 0.85,
        f1_score: 0.82,
        mse: 0.18,
        hyperparameters: { "k": 10, "learning_rate": 0.01 },
        model_config: { "algorithm": "collaborative_filtering", "similarity": "cosine" },
        feature_importance: { "user_behavior": 0.4, "content_features": 0.35, "performance": 0.25 },
        training_data_size: 10000,
        training_duration: 2.5,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        is_active: true
      },
      {
        id: 2,
        name: "Modèle de Prédiction de Performance",
        model_type: "neural_network",
        algorithm: "lstm",
        version: "2.1",
        description: "Réseau de neurones LSTM pour prédire les performances futures",
        accuracy: 0.88,
        precision: 0.86,
        recall: 0.89,
        f1_score: 0.87,
        mse: 0.12,
        hyperparameters: { "layers": 3, "units": 128, "dropout": 0.2 },
        model_config: { "architecture": "lstm", "sequence_length": 10 },
        feature_importance: { "historical_performance": 0.45, "engagement": 0.3, "difficulty": 0.25 },
        training_data_size: 25000,
        training_duration: 8.5,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        is_active: true
      },
      {
        id: 3,
        name: "Système Expert de Remédiation",
        model_type: "expert_system",
        algorithm: "rule_based",
        version: "1.5",
        description: "Système expert basé sur des règles pour la remédiation",
        accuracy: 0.75,
        precision: 0.73,
        recall: 0.77,
        f1_score: 0.75,
        mse: 0.25,
        hyperparameters: { "confidence_threshold": 0.8, "rule_weight": 1.0 },
        model_config: { "type": "rule_based", "inference": "forward_chaining" },
        feature_importance: { "error_patterns": 0.5, "concept_mastery": 0.3, "learning_style": 0.2 },
        training_data_size: 5000,
        training_duration: 1.0,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        is_active: true
      }
    ];
  }

  private static getDefaultTrainingSessions(modelId: number) {
    return {
      model_id: modelId,
      training_sessions: [
        {
          id: 1,
          model_id: modelId,
          session_name: "Training Session 1",
          training_data_source: "student_performance_data",
          training_data_size: 10000,
          validation_data_size: 2000,
          epochs: 100,
          batch_size: 32,
          learning_rate: 0.001,
          optimizer: "adam",
          loss_function: "categorical_crossentropy",
          training_accuracy: 0.85,
          validation_accuracy: 0.82,
          training_loss: 0.15,
          validation_loss: 0.18,
          started_at: new Date().toISOString(),
          completed_at: new Date().toISOString(),
          status: "completed"
        }
      ]
    };
  }

  private static getDefaultDeployments(modelId: number) {
    return {
      model_id: modelId,
      deployments: [
        {
          id: 1,
          model_id: modelId,
          environment: "production",
          deployment_url: "https://api.example.com/models/1",
          deployment_config: { "version": "1.0", "environment": "production" },
          scaling_config: { "min_instances": 2, "max_instances": 10 },
          monitoring_config: { "metrics": ["accuracy", "latency"], "alerts": true },
          deployed_at: new Date().toISOString(),
          status: "active",
          health_check: { "status": "healthy", "last_check": new Date().toISOString() }
        }
      ]
    };
  }
}





