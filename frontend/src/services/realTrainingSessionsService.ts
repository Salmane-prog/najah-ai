import { apiClient } from '../utils/api';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// ============================================================================
// INTERFACES POUR LES SESSIONS D'ENTRAÎNEMENT IA RÉELLES
// ============================================================================

export interface TrainingSession {
  id: number;
  model_id: number;
  model_name: string;
  session_name: string;
  description: string;
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled' | 'paused';
  priority: 'low' | 'medium' | 'high' | 'critical';
  start_time: string;
  end_time: string | null;
  duration: number | null;
  progress: number;
  current_epoch: number;
  total_epochs: number;
  current_loss: number | null;
  current_accuracy: number | null;
  current_validation_loss: number | null;
  current_validation_accuracy: number | null;
  best_loss: number | null;
  best_accuracy: number | null;
  logs: string[];
  metrics: {
    training_loss: number[];
    validation_loss: number[];
    training_accuracy: number[];
    validation_accuracy: number[];
    learning_rate: number[];
    gradient_norm: number[];
  };
  hyperparameters: {
    learning_rate: number;
    batch_size: number;
    epochs: number;
    optimizer: string;
    loss_function: string;
    regularization: string;
    dropout_rate: number;
    early_stopping_patience: number;
  };
  dataset_info: {
    training_samples: number;
    validation_samples: number;
    test_samples: number;
    features_count: number;
    classes_count: number;
    data_augmentation: boolean;
  };
  hardware_info: {
    gpu_model: string;
    gpu_memory: number;
    cpu_cores: number;
    ram_gb: number;
    training_device: 'cpu' | 'gpu' | 'tpu';
  };
  created_by: number;
  created_at: string;
  updated_at: string;
}

export interface TrainingJob {
  id: number;
  session_id: number;
  session_name: string;
  job_type: 'training' | 'validation' | 'testing' | 'inference';
  status: 'queued' | 'running' | 'completed' | 'failed';
  priority: number;
  submitted_at: string;
  started_at: string | null;
  completed_at: string | null;
  estimated_duration: number;
  actual_duration: number | null;
  progress: number;
  current_step: string;
  error_message: string | null;
  resource_usage: {
    cpu_percent: number;
    memory_percent: number;
    gpu_percent: number;
    gpu_memory_percent: number;
  };
  logs: string[];
  created_by: number;
}

export interface TrainingMetrics {
  session_id: number;
  model_name: string;
  overall_performance: number;
  training_efficiency: number;
  validation_performance: number;
  overfitting_score: number;
  convergence_rate: number;
  stability_score: number;
  resource_efficiency: number;
  last_updated: string;
}

export interface TrainingComparison {
  id: number;
  comparison_name: string;
  description: string;
  sessions: number[];
  session_names: string[];
  comparison_metrics: {
    final_accuracy: number[];
    final_loss: number[];
    training_time: number[];
    convergence_epochs: number[];
    overfitting_score: number[];
  };
  created_at: string;
  created_by: number;
}

export interface TrainingSessionsData {
  sessions: TrainingSession[];
  total_sessions: number;
  active_sessions: number;
  completed_sessions: number;
  failed_sessions: number;
  average_duration: number;
  success_rate: number;
}

// ============================================================================
// FONCTIONS PRINCIPALES
// ============================================================================

export async function getRealTrainingSessions(token: string): Promise<TrainingSessionsData> {
  try {
    console.log('🔄 Récupération des vraies sessions d\'entraînement...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/training_sessions/`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Vraies sessions d\'entraînement récupérées:', data);
    return data;

  } catch (error) {
    console.error('❌ Erreur lors de la récupération des sessions:', error);
    throw error;
  }
}

export async function getTrainingSessionDetails(token: string, sessionId: number): Promise<TrainingSession> {
  try {
    console.log('🔄 Récupération des détails de la session d\'entraînement...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/training_sessions/${sessionId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Détails de la session récupérés:', data);
    return data;

  } catch (error) {
    console.error('❌ Erreur lors de la récupération des détails:', error);
    throw error;
  }
}

export async function getTrainingJobs(token: string, sessionId?: number): Promise<TrainingJob[]> {
  try {
    console.log('🔄 Récupération des jobs d\'entraînement...');
    
    let url = `${API_BASE_URL}/api/v1/training_sessions/jobs/`;
    if (sessionId) {
      url += `?session_id=${sessionId}`;
    }
    
    const response = await fetch(url, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Jobs d\'entraînement récupérés:', data);
    return data;

  } catch (error) {
    console.error('❌ Erreur lors de la récupération des jobs:', error);
    throw error;
  }
}

export async function getTrainingMetrics(token: string, sessionId?: number): Promise<TrainingMetrics[]> {
  try {
    console.log('🔄 Récupération des métriques d\'entraînement...');
    
    let url = `${API_BASE_URL}/api/v1/training_sessions/metrics/`;
    if (sessionId) {
      url += `?session_id=${sessionId}`;
    }
    
    const response = await fetch(url, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Métriques d\'entraînement récupérées:', data);
    return data;

  } catch (error) {
    console.error('❌ Erreur lors de la récupération des métriques:', error);
    throw error;
  }
}

export async function getTrainingComparisons(token: string): Promise<TrainingComparison[]> {
  try {
    console.log('🔄 Récupération des comparaisons d\'entraînement...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/training_sessions/comparisons/`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Comparaisons d\'entraînement récupérées:', data);
    return data;

  } catch (error) {
    console.error('❌ Erreur lors de la récupération des comparaisons:', error);
    throw error;
  }
}

export async function startTrainingSession(token: string, trainingConfig: any): Promise<TrainingSession> {
  try {
    console.log('🔄 Démarrage d\'une nouvelle session d\'entraînement...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/training_sessions/start`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(trainingConfig)
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Session d\'entraînement démarrée avec succès:', data);
    return data;

  } catch (error) {
    console.error('❌ Erreur lors du démarrage de la session:', error);
    throw error;
  }
}

export async function pauseTrainingSession(token: string, sessionId: number): Promise<void> {
  try {
    console.log('🔄 Pause de la session d\'entraînement...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/training_sessions/${sessionId}/pause`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    console.log('✅ Session d\'entraînement mise en pause');

  } catch (error) {
    console.error('❌ Erreur lors de la pause:', error);
    throw error;
  }
}

export async function resumeTrainingSession(token: string, sessionId: number): Promise<void> {
  try {
    console.log('🔄 Reprise de la session d\'entraînement...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/training_sessions/${sessionId}/resume`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    console.log('✅ Session d\'entraînement reprise');

  } catch (error) {
    console.error('❌ Erreur lors de la reprise:', error);
    throw error;
  }
}

export async function cancelTrainingSession(token: string, sessionId: number): Promise<void> {
  try {
    console.log('🔄 Annulation de la session d\'entraînement...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/training_sessions/${sessionId}/cancel`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    console.log('✅ Session d\'entraînement annulée');

  } catch (error) {
    console.error('❌ Erreur lors de l\'annulation:', error);
    throw error;
  }
}

export async function getRealTimeTrainingUpdates(token: string, sessionId: number): Promise<any> {
  try {
    console.log('🔄 Récupération des mises à jour en temps réel...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/training_sessions/${sessionId}/realtime`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Mises à jour en temps réel récupérées:', data);
    return data;

  } catch (error) {
    console.error('❌ Erreur lors de la récupération des mises à jour:', error);
    throw error;
  }
}

// ============================================================================
// FONCTIONS DE FALLBACK (DONNÉES MOCKÉES EN CAS D'ERREUR)
// ============================================================================

export function getMockTrainingSessions(): TrainingSessionsData {
  return {
    sessions: [
      {
        id: 1,
        model_id: 2,
        model_name: "Modèle de Prédiction de Performance",
        session_name: "Session d'entraînement #1",
        description: "Entraînement initial du modèle de prédiction",
        status: "running",
        priority: "high",
        start_time: "2024-01-20T14:00:00Z",
        end_time: null,
        duration: null,
        progress: 65,
        current_epoch: 98,
        total_epochs: 150,
        current_loss: 0.0234,
        current_accuracy: 0.8945,
        current_validation_loss: 0.0345,
        current_validation_accuracy: 0.8812,
        best_loss: 0.0212,
        best_accuracy: 0.9012,
        logs: [
          "Epoch 95/150 - loss: 0.0256 - accuracy: 0.8912 - val_loss: 0.0356 - val_accuracy: 0.8798",
          "Epoch 96/150 - loss: 0.0248 - accuracy: 0.8928 - val_loss: 0.0348 - val_accuracy: 0.8805",
          "Epoch 97/150 - loss: 0.0241 - accuracy: 0.8934 - val_loss: 0.0341 - val_accuracy: 0.8809",
          "Epoch 98/150 - loss: 0.0234 - accuracy: 0.8945 - val_loss: 0.0345 - val_accuracy: 0.8812"
        ],
        metrics: {
          training_loss: [0.1567, 0.1234, 0.0987, 0.0765, 0.0543, 0.0432, 0.0345, 0.0287, 0.0256, 0.0234],
          validation_loss: [0.1678, 0.1345, 0.1098, 0.0876, 0.0654, 0.0543, 0.0456, 0.0398, 0.0367, 0.0345],
          training_accuracy: [0.7234, 0.7891, 0.8234, 0.8567, 0.8789, 0.8912, 0.8987, 0.9045, 0.9089, 0.9123],
          validation_accuracy: [0.7123, 0.7789, 0.8123, 0.8456, 0.8678, 0.8801, 0.8876, 0.8934, 0.8978, 0.9012],
          learning_rate: [0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001],
          gradient_norm: [0.2345, 0.1987, 0.1654, 0.1432, 0.1234, 0.1098, 0.0987, 0.0876, 0.0765, 0.0654]
        },
        hyperparameters: {
          learning_rate: 0.0001,
          batch_size: 64,
          epochs: 150,
          optimizer: "adam",
          loss_function: "categorical_crossentropy",
          regularization: "l2",
          dropout_rate: 0.3,
          early_stopping_patience: 10
        },
        dataset_info: {
          training_samples: 75000,
          validation_samples: 15000,
          test_samples: 15000,
          features_count: 200,
          classes_count: 10,
          data_augmentation: true
        },
        hardware_info: {
          gpu_model: "NVIDIA RTX 4090",
          gpu_memory: 24,
          cpu_cores: 16,
          ram_gb: 64,
          training_device: "gpu"
        },
        created_by: 1,
        created_at: "2024-01-20T14:00:00Z",
        updated_at: "2024-01-20T15:30:00Z"
      },
      {
        id: 2,
        model_id: 1,
        model_name: "Modèle de Recommandation - Français",
        session_name: "Session d'entraînement #2",
        description: "Réentraînement avec nouvelles données",
        status: "completed",
        priority: "medium",
        start_time: "2024-01-18T10:00:00Z",
        end_time: "2024-01-18T11:00:00Z",
        duration: 3600,
        progress: 100,
        current_epoch: 100,
        total_epochs: 100,
        current_loss: 0.0156,
        current_accuracy: 0.9234,
        current_validation_loss: 0.0187,
        current_validation_accuracy: 0.9187,
        best_loss: 0.0156,
        best_accuracy: 0.9234,
        logs: [
          "Epoch 98/100 - loss: 0.0158 - accuracy: 0.9228 - val_loss: 0.0189 - val_accuracy: 0.9181",
          "Epoch 99/100 - loss: 0.0157 - accuracy: 0.9231 - val_loss: 0.0188 - val_accuracy: 0.9184",
          "Epoch 100/100 - loss: 0.0156 - accuracy: 0.9234 - val_loss: 0.0187 - val_accuracy: 0.9187"
        ],
        metrics: {
          training_loss: [0.1234, 0.0987, 0.0765, 0.0543, 0.0432, 0.0345, 0.0287, 0.0256, 0.0212, 0.0156],
          validation_loss: [0.1345, 0.1098, 0.0876, 0.0654, 0.0543, 0.0456, 0.0398, 0.0367, 0.0321, 0.0187],
          training_accuracy: [0.7891, 0.8234, 0.8567, 0.8789, 0.8912, 0.8987, 0.9045, 0.9089, 0.9123, 0.9234],
          validation_accuracy: [0.7789, 0.8123, 0.8456, 0.8678, 0.8801, 0.8876, 0.8934, 0.8978, 0.9012, 0.9187],
          learning_rate: [0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001],
          gradient_norm: [0.1987, 0.1654, 0.1432, 0.1234, 0.1098, 0.0987, 0.0876, 0.0765, 0.0654, 0.0543]
        },
        hyperparameters: {
          learning_rate: 0.001,
          batch_size: 32,
          epochs: 100,
          optimizer: "adam",
          loss_function: "binary_crossentropy",
          regularization: "l1",
          dropout_rate: 0.2,
          early_stopping_patience: 15
        },
        dataset_info: {
          training_samples: 50000,
          validation_samples: 10000,
          test_samples: 10000,
          features_count: 150,
          classes_count: 2,
          data_augmentation: false
        },
        hardware_info: {
          gpu_model: "NVIDIA RTX 3080",
          gpu_memory: 12,
          cpu_cores: 12,
          ram_gb: 32,
          training_device: "gpu"
        },
        created_by: 1,
        created_at: "2024-01-18T10:00:00Z",
        updated_at: "2024-01-18T11:00:00Z"
      }
    ],
    total_sessions: 2,
    active_sessions: 1,
    completed_sessions: 1,
    failed_sessions: 0,
    average_duration: 3600,
    success_rate: 100
  };
}

export function getMockTrainingJobs(): TrainingJob[] {
  return [
    {
      id: 1,
      session_id: 1,
      session_name: "Session d'entraînement #1",
      job_type: "training",
      status: "running",
      priority: 1,
      submitted_at: "2024-01-20T14:00:00Z",
      started_at: "2024-01-20T14:00:00Z",
      completed_at: null,
      estimated_duration: 7200,
      actual_duration: null,
      progress: 65,
      current_step: "Training epoch 98/150",
      error_message: null,
      resource_usage: {
        cpu_percent: 85,
        memory_percent: 72,
        gpu_percent: 95,
        gpu_memory_percent: 88
      },
      logs: [
        "Job started at 2024-01-20T14:00:00Z",
        "Training epoch 95/150 completed",
        "Training epoch 96/150 completed",
        "Training epoch 97/150 completed",
        "Training epoch 98/150 in progress..."
      ],
      created_by: 1
    }
  ];
}

// ============================================================================
// FONCTIONS AVEC FALLBACK
// ============================================================================

export async function getRealTrainingSessionsWithFallback(token: string): Promise<TrainingSessionsData> {
  try {
    return await getRealTrainingSessions(token);
  } catch (error) {
    console.warn('⚠️ Utilisation des données de fallback pour les sessions d\'entraînement:', error);
    return getMockTrainingSessions();
  }
}

export async function getTrainingJobsWithFallback(token: string, sessionId?: number): Promise<TrainingJob[]> {
  try {
    return await getTrainingJobs(token, sessionId);
  } catch (error) {
    console.warn('⚠️ Utilisation des données de fallback pour les jobs:', error);
    return getMockTrainingJobs();
  }
}



























