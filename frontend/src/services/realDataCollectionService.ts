import { apiClient } from '../utils/api';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// ============================================================================
// INTERFACES POUR LA COLLECTE DE DONNÉES RÉELLES
// ============================================================================

export interface DataSource {
  id: number;
  name: string;
  description: string;
  type: string;
  status: 'active' | 'inactive' | 'error';
  last_collection: string;
  next_collection: string;
  collection_frequency: number;
  data_quality: number;
  total_records: number;
  new_records_today: number;
  error_count: number;
  last_error: string | null;
  created_at: string;
  updated_at: string;
}

export interface DataCollectionActivity {
  id: number;
  source_id: number;
  source_name: string;
  source_type: string;
  status: 'active' | 'paused' | 'error';
  collection_type: string;
  table_name: string;
  frequency_minutes: number;
  data_quality: number;
  last_collection: string;
  next_collection: string;
  records_count: number;
  new_records_since_last: number;
  processing_time_seconds: number;
  error_message: string | null;
  created_by: number;
  created_at: string;
  updated_at: string;
}

export interface LearningPattern {
  id: number;
  pattern_name: string;
  description: string;
  pattern_type: string;
  confidence: number;
  support_count: number;
  total_occurrences: number;
  first_detected: string;
  last_observed: string;
  related_features: string[];
  impact_score: number;
  recommendations: string[];
  created_at: string;
}

export interface BlockageDetection {
  id: number;
  student_id: number;
  student_name: string;
  subject: string;
  topic: string;
  blockage_type: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  confidence: number;
  detected_at: string;
  symptoms: string[];
  root_cause: string;
  suggested_interventions: string[];
  status: 'active' | 'resolved' | 'monitoring';
  resolution_date: string | null;
  created_at: string;
}

export interface ContinuousImprovement {
  id: number;
  improvement_type: string;
  title: string;
  description: string;
  priority: 'low' | 'medium' | 'high' | 'critical';
  status: 'proposed' | 'approved' | 'in_progress' | 'completed' | 'cancelled';
  impact_area: string;
  expected_benefit: string;
  implementation_cost: 'low' | 'medium' | 'high';
  estimated_duration_days: number;
  assigned_to: number;
  assigned_name: string;
  progress_percentage: number;
  start_date: string | null;
  completion_date: string | null;
  created_at: string;
  updated_at: string;
}

export interface DataCollectionMetrics {
  total_sources: number;
  active_collections: number;
  total_records: number;
  average_quality: number;
  data_sources: DataSource[];
  collection_activities: DataCollectionActivity[];
  learning_patterns: LearningPattern[];
  blockage_detections: BlockageDetection[];
  continuous_improvements: ContinuousImprovement[];
}

// ============================================================================
// FONCTIONS PRINCIPALES
// ============================================================================

export async function getRealDataCollectionMetrics(token: string): Promise<DataCollectionMetrics> {
  try {
    console.log('🔄 Récupération des vraies métriques de collecte de données...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/data_collection/metrics/`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Vraies métriques de collecte récupérées:', data);
    return data;

  } catch (error) {
    console.error('❌ Erreur lors de la récupération des métriques:', error);
    throw error;
  }
}

export async function getDataSources(token: string): Promise<DataSource[]> {
  try {
    console.log('🔄 Récupération des sources de données...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/data_collection/sources/`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Sources de données récupérées:', data);
    return data;

  } catch (error) {
    console.error('❌ Erreur lors de la récupération des sources:', error);
    throw error;
  }
}

export async function getCollectionActivities(token: string): Promise<DataCollectionActivity[]> {
  try {
    console.log('🔄 Récupération des activités de collecte...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/data_collection/activities/`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Activités de collecte récupérées:', data);
    return data;

  } catch (error) {
    console.error('❌ Erreur lors de la récupération des activités:', error);
    throw error;
  }
}

export async function getLearningPatterns(token: string): Promise<LearningPattern[]> {
  try {
    console.log('🔄 Récupération des patterns d\'apprentissage...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/data_collection/learning-patterns/`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Patterns d\'apprentissage récupérés:', data);
    return data;

  } catch (error) {
    console.error('❌ Erreur lors de la récupération des patterns:', error);
    throw error;
  }
}

export async function getBlockageDetections(token: string): Promise<BlockageDetection[]> {
  try {
    console.log('🔄 Récupération des détections de blocages...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/data_collection/blockage-detections/`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Détections de blocages récupérées:', data);
    return data;

  } catch (error) {
    console.error('❌ Erreur lors de la récupération des blocages:', error);
    throw error;
  }
}

export async function getContinuousImprovements(token: string): Promise<ContinuousImprovement[]> {
  try {
    console.log('🔄 Récupération des améliorations continues...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/data_collection/continuous-improvements/`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Améliorations continues récupérées:', data);
    return data;

  } catch (error) {
    console.error('❌ Erreur lors de la récupération des améliorations:', error);
    throw error;
  }
}

export async function pauseDataCollection(token: string, activityId: number): Promise<void> {
  try {
    console.log('🔄 Pause de la collecte de données...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/data_collection/activities/${activityId}/pause`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    console.log('✅ Collecte de données mise en pause');

  } catch (error) {
    console.error('❌ Erreur lors de la pause:', error);
    throw error;
  }
}

export async function resumeDataCollection(token: string, activityId: number): Promise<void> {
  try {
    console.log('🔄 Reprise de la collecte de données...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/data_collection/activities/${activityId}/resume`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    console.log('✅ Collecte de données reprise');

  } catch (error) {
    console.error('❌ Erreur lors de la reprise:', error);
    throw error;
  }
}

export async function exportDataCollectionReport(token: string, format: 'csv' | 'json' | 'pdf'): Promise<Blob> {
  try {
    console.log('🔄 Export du rapport de collecte de données...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/data_collection/export/${format}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const blob = await response.blob();
    console.log('✅ Rapport exporté avec succès');
    return blob;

  } catch (error) {
    console.error('❌ Erreur lors de l\'export:', error);
    throw error;
  }
}

// ============================================================================
// FONCTIONS DE FALLBACK (DONNÉES MOCKÉES EN CAS D'ERREUR)
// ============================================================================

export function getMockDataCollectionMetrics(): DataCollectionMetrics {
  return {
    total_sources: 3,
    active_collections: 2,
    total_records: 27588,
    average_quality: 95,
    data_sources: [
      {
        id: 1,
        name: "Interactions Utilisateur",
        description: "Collecte des interactions utilisateur en temps réel",
        type: "behavioral",
        status: "active",
        last_collection: "2024-01-20T15:30:00Z",
        next_collection: "2024-01-20T16:00:00Z",
        collection_frequency: 30,
        data_quality: 94.2,
        total_records: 15420,
        new_records_today: 156,
        error_count: 3,
        last_error: "2024-01-20T12:15:00Z",
        created_at: "2024-01-15T09:00:00Z",
        updated_at: "2024-01-20T15:30:00Z"
      },
      {
        id: 2,
        name: "Performances d'Apprentissage",
        description: "Collecte des performances académiques des étudiants",
        type: "academic",
        status: "active",
        last_collection: "2024-01-20T14:45:00Z",
        next_collection: "2024-01-20T15:15:00Z",
        collection_frequency: 30,
        data_quality: 98.7,
        total_records: 3247,
        new_records_today: 23,
        error_count: 0,
        last_error: null,
        created_at: "2024-01-15T09:00:00Z",
        updated_at: "2024-01-20T14:45:00Z"
      },
      {
        id: 3,
        name: "Métriques Système",
        description: "Collecte des métriques de performance du système",
        type: "system",
        status: "inactive",
        last_collection: "2024-01-20T10:00:00Z",
        next_collection: "2024-01-20T16:00:00Z",
        collection_frequency: 360,
        data_quality: 92.1,
        total_records: 8921,
        new_records_today: 45,
        error_count: 7,
        last_error: "2024-01-20T14:30:00Z",
        created_at: "2024-01-15T09:00:00Z",
        updated_at: "2024-01-20T10:00:00Z"
      }
    ],
    collection_activities: [
      {
        id: 1,
        source_id: 1,
        source_name: "Interactions Utilisateur",
        source_type: "behavioral",
        status: "active",
        collection_type: "real_time",
        table_name: "frontend_events",
        frequency_minutes: 30,
        data_quality: 94.2,
        last_collection: "2024-01-20T15:30:00Z",
        next_collection: "2024-01-20T16:00:00Z",
        records_count: 15420,
        new_records_since_last: 156,
        processing_time_seconds: 45,
        error_message: null,
        created_by: 1,
        created_at: "2024-01-15T09:00:00Z",
        updated_at: "2024-01-20T15:30:00Z"
      },
      {
        id: 2,
        source_id: 2,
        source_name: "Performances d'Apprentissage",
        source_type: "academic",
        status: "active",
        collection_type: "batch",
        table_name: "quiz_results",
        frequency_minutes: 30,
        data_quality: 98.7,
        last_collection: "2024-01-20T14:45:00Z",
        next_collection: "2024-01-20T15:15:00Z",
        records_count: 3247,
        new_records_since_last: 23,
        processing_time_seconds: 12,
        error_message: null,
        created_by: 1,
        created_at: "2024-01-15T09:00:00Z",
        updated_at: "2024-01-20T14:45:00Z"
      }
    ],
    learning_patterns: [
      {
        id: 1,
        pattern_name: "Progression Mathématiques",
        description: "Pattern de progression typique en mathématiques",
        pattern_type: "progression",
        confidence: 0.89,
        support_count: 156,
        total_occurrences: 234,
        first_detected: "2024-01-10T09:00:00Z",
        last_observed: "2024-01-20T15:00:00Z",
        related_features: ["quiz_scores", "time_spent", "difficulty_level"],
        impact_score: 0.78,
        recommendations: ["Renforcer les bases", "Pratique régulière"],
        created_at: "2024-01-10T09:00:00Z"
      }
    ],
    blockage_detections: [
      {
        id: 1,
        student_id: 123,
        student_name: "Marie Dubois",
        subject: "Mathématiques",
        topic: "Fractions",
        blockage_type: "conceptual",
        severity: "medium",
        confidence: 0.85,
        detected_at: "2024-01-20T14:30:00Z",
        symptoms: ["Erreurs répétées", "Temps de réponse élevé"],
        root_cause: "Manque de compréhension des concepts de base",
        suggested_interventions: ["Révision des bases", "Exercices supplémentaires"],
        status: "active",
        resolution_date: null,
        created_at: "2024-01-20T14:30:00Z"
      }
    ],
    continuous_improvements: [
      {
        id: 1,
        improvement_type: "algorithm",
        title: "Optimisation de l'algorithme de recommandation",
        description: "Améliorer la précision des recommandations de contenu",
        priority: "high",
        status: "in_progress",
        impact_area: "user_experience",
        expected_benefit: "Augmentation de 15% de l'engagement",
        implementation_cost: "medium",
        estimated_duration_days: 14,
        assigned_to: 1,
        assigned_name: "Équipe IA",
        progress_percentage: 65,
        start_date: "2024-01-15T09:00:00Z",
        completion_date: null,
        created_at: "2024-01-10T09:00:00Z",
        updated_at: "2024-01-20T15:00:00Z"
      }
    ]
  };
}

// ============================================================================
// FONCTIONS AVEC FALLBACK
// ============================================================================

export async function getRealDataCollectionMetricsWithFallback(token: string): Promise<DataCollectionMetrics> {
  try {
    return await getRealDataCollectionMetrics(token);
  } catch (error) {
    console.warn('⚠️ Utilisation des données de fallback pour la collecte:', error);
    return getMockDataCollectionMetrics();
  }
}

export async function getDataSourcesWithFallback(token: string): Promise<DataSource[]> {
  try {
    return await getDataSources(token);
  } catch (error) {
    console.warn('⚠️ Utilisation des données de fallback pour les sources:', error);
    return getMockDataCollectionMetrics().data_sources;
  }
}

export async function getCollectionActivitiesWithFallback(token: string): Promise<DataCollectionActivity[]> {
  try {
    return await getCollectionActivities(token);
  } catch (error) {
    console.warn('⚠️ Utilisation des données de fallback pour les activités:', error);
    return getMockDataCollectionMetrics().collection_activities;
  }
}
























