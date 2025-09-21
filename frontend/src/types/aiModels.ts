// Types pour les AI Models

export interface AIModel {
  id: number;
  name: string;
  description: string;
  model_type: string;
  version: string;
  accuracy: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ModelTrainingSession {
  id: number;
  model_id: number;
  status: string;
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
  completed_at: string | null;
  created_at: string;
}

export interface ModelPrediction {
  id: number;
  model_id: number;
  student_id: number;
  prediction_type: string;
  predicted_value: number;
  confidence: number;
  actual_value: number;
  created_at: string;
}

export interface ModelPerformance {
  id: number;
  model_id: number;
  metric_name: string;
  metric_value: number;
  timestamp: string;
}


























