// Types pour les AI Analytics

export interface AIAnalyticsData {
  overview: {
    total_models: number;
    active_models: number;
    total_predictions: number;
    accuracy_rate: number;
  };
  recent_activity: Array<{
    id: number;
    type: string;
    description: string;
    timestamp: string;
    status: string;
  }>;
  performance_metrics: {
    model_accuracy: number;
    prediction_speed: number;
    data_quality: number;
    user_satisfaction: number;
  };
}

export interface LearningAnalytics {
  student_id: number;
  learning_patterns: Array<{
    pattern_type: string;
    frequency: string;
    duration: number;
    effectiveness: number;
  }>;
  progress_trends: Array<{
    date: string;
    score: number;
    trend: string;
  }>;
  engagement_metrics: {
    session_count: number;
    time_spent: number;
    resource_access: number;
    interaction_rate: number;
  };
}

export interface AIPredictions {
  student_id: number;
  predictions: Array<{
    type: string;
    predicted_score?: number;
    predicted_level?: string;
    confidence: number;
    timeframe: string;
    factors: string[];
  }>;
  accuracy_history: Array<{
    date: string;
    accuracy: number;
  }>;
}

export interface BlockageDetection {
  student_id: number;
  detected_blockages: Array<{
    id: number;
    subject: string;
    concept: string;
    severity: string;
    confidence: number;
    symptoms: string[];
    suggested_interventions: string[];
  }>;
  resolution_progress: number;
  intervention_history: Array<{
    date: string;
    intervention: string;
    effectiveness: number;
  }>;
}

export interface LearningPatterns {
  student_id: number;
  patterns: Array<{
    id: number;
    name: string;
    description: string;
    confidence: number;
    support_count: number;
    impact_score: number;
  }>;
  insights: string[];
}

export interface AIRecommendations {
  student_id: number;
  recommendations: Array<{
    id: number;
    type: string;
    title: string;
    description: string;
    priority: string;
    confidence: number;
    expected_impact: number;
  }>;
  implementation_status: {
    accepted: number;
    pending: number;
    rejected: number;
    total: number;
  };
}























