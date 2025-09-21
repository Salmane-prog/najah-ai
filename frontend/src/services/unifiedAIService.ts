import { apiClient } from '../utils/api';
import { 
  getRealAIModelsWithFallback, 
  getTrainingSessionsWithFallback,
  getModelPredictionsWithFallback,
  AIModelsData,
  TrainingSession
} from './realAIModelsService';
import { 
  getRealDataCollectionMetricsWithFallback,
  DataCollectionMetrics 
} from './realDataCollectionService';
import { 
  getRealTrainingSessionsWithFallback,
  TrainingSessionsData 
} from './realTrainingSessionsService';

// ============================================================================
// SERVICE UNIFIÉ POUR TOUTES LES FONCTIONNALITÉS AI
// ============================================================================

export interface UnifiedAIData {
  models: AIModelsData;
  dataCollection: DataCollectionMetrics;
  trainingSessions: TrainingSessionsData;
  lastUpdated: string;
  dataSource: 'real' | 'fallback';
}

export interface AIStatus {
  models_status: 'connected' | 'fallback' | 'error';
  data_collection_status: 'connected' | 'fallback' | 'error';
  training_sessions_status: 'connected' | 'fallback' | 'error';
  overall_status: 'fully_connected' | 'partially_connected' | 'fallback_mode';
  error_count: number;
  last_check: string;
}

// ============================================================================
// FONCTIONS PRINCIPALES
// ============================================================================

export async function getAllUnifiedAIData(token: string): Promise<UnifiedAIData> {
  try {
    console.log('🔄 Récupération de toutes les données AI unifiées...');
    
    // Récupérer toutes les données en parallèle
    const [modelsData, dataCollectionData, trainingSessionsData] = await Promise.all([
      getRealAIModelsWithFallback(token),
      getRealDataCollectionMetricsWithFallback(token),
      getRealTrainingSessionsWithFallback(token)
    ]);

    const unifiedData: UnifiedAIData = {
      models: modelsData,
      dataCollection: dataCollectionData,
      trainingSessions: trainingSessionsData,
      lastUpdated: new Date().toISOString(),
      dataSource: 'real'
    };

    console.log('✅ Données AI unifiées récupérées avec succès:', unifiedData);
    return unifiedData;

  } catch (error) {
    console.error('❌ Erreur lors de la récupération des données AI unifiées:', error);
    
    // En cas d'erreur, retourner des données de fallback
    const fallbackData: UnifiedAIData = {
      models: await getRealAIModelsWithFallback(token),
      dataCollection: await getRealDataCollectionMetricsWithFallback(token),
      trainingSessions: await getRealTrainingSessionsWithFallback(token),
      lastUpdated: new Date().toISOString(),
      dataSource: 'fallback'
    };

    console.warn('⚠️ Utilisation des données de fallback pour AI unifiées');
    return fallbackData;
  }
}

export async function getAIStatus(token: string): Promise<AIStatus> {
  try {
    console.log('🔄 Vérification du statut des services AI...');
    
    const status: AIStatus = {
      models_status: 'connected',
      data_collection_status: 'connected',
      training_sessions_status: 'connected',
      overall_status: 'fully_connected',
      error_count: 0,
      last_check: new Date().toISOString()
    };

    // Vérifier chaque service individuellement
    try {
      await getRealAIModelsWithFallback(token);
    } catch (error) {
      status.models_status = 'fallback';
      status.error_count++;
    }

    try {
      await getRealDataCollectionMetricsWithFallback(token);
    } catch (error) {
      status.data_collection_status = 'fallback';
      status.error_count++;
    }

    try {
      await getRealTrainingSessionsWithFallback(token);
    } catch (error) {
      status.training_sessions_status = 'fallback';
      status.error_count++;
    }

    // Déterminer le statut global
    if (status.error_count === 0) {
      status.overall_status = 'fully_connected';
    } else if (status.error_count < 3) {
      status.overall_status = 'partially_connected';
    } else {
      status.overall_status = 'fallback_mode';
    }

    console.log('✅ Statut AI vérifié:', status);
    return status;

  } catch (error) {
    console.error('❌ Erreur lors de la vérification du statut AI:', error);
    
    return {
      models_status: 'error',
      data_collection_status: 'error',
      training_sessions_status: 'error',
      overall_status: 'fallback_mode',
      error_count: 3,
      last_check: new Date().toISOString()
    };
  }
}

export async function getAIModelsSummary(token: string): Promise<{
  total_models: number;
  active_models: number;
  training_models: number;
  deployed_models: number;
  average_performance: number;
}> {
  try {
    const modelsData = await getRealAIModelsWithFallback(token);
    
    return {
      total_models: modelsData.total_models,
      active_models: modelsData.active_models,
      training_models: modelsData.training_models,
      deployed_models: modelsData.deployed_models,
      average_performance: modelsData.average_performance
    };
  } catch (error) {
    console.error('❌ Erreur lors de la récupération du résumé des modèles:', error);
    return {
      total_models: 0,
      active_models: 0,
      training_models: 0,
      deployed_models: 0,
      average_performance: 0
    };
  }
}

export async function getDataCollectionSummary(token: string): Promise<{
  total_sources: number;
  active_collections: number;
  total_records: number;
  average_quality: number;
}> {
  try {
    const dataCollectionData = await getRealDataCollectionMetricsWithFallback(token);
    
    return {
      total_sources: dataCollectionData.total_sources,
      active_collections: dataCollectionData.active_collections,
      total_records: dataCollectionData.total_records,
      average_quality: dataCollectionData.average_quality
    };
  } catch (error) {
    console.error('❌ Erreur lors de la récupération du résumé de collecte:', error);
    return {
      total_sources: 0,
      active_collections: 0,
      total_records: 0,
      average_quality: 0
    };
  }
}

export async function getTrainingSessionsSummary(token: string): Promise<{
  total_sessions: number;
  active_sessions: number;
  completed_sessions: number;
  failed_sessions: number;
  success_rate: number;
}> {
  try {
    const trainingSessionsData = await getRealTrainingSessionsWithFallback(token);
    
    return {
      total_sessions: trainingSessionsData.total_sessions,
      active_sessions: trainingSessionsData.active_sessions,
      completed_sessions: trainingSessionsData.completed_sessions,
      failed_sessions: trainingSessionsData.failed_sessions,
      success_rate: trainingSessionsData.success_rate
    };
  } catch (error) {
    console.error('❌ Erreur lors de la récupération du résumé des sessions:', error);
    return {
      total_sessions: 0,
      active_sessions: 0,
      completed_sessions: 0,
      failed_sessions: 0,
      success_rate: 0
    };
  }
}

// ============================================================================
// FONCTIONS DE MONITORING ET DEBUGGING
// ============================================================================

export async function refreshAllAIData(token: string): Promise<UnifiedAIData> {
  try {
    console.log('🔄 Actualisation de toutes les données AI...');
    
    // Forcer la récupération des vraies données
    const [modelsData, dataCollectionData, trainingSessionsData] = await Promise.all([
      getRealAIModelsWithFallback(token),
      getRealDataCollectionMetricsWithFallback(token),
      getRealTrainingSessionsWithFallback(token)
    ]);

    const refreshedData: UnifiedAIData = {
      models: modelsData,
      dataCollection: dataCollectionData,
      trainingSessions: trainingSessionsData,
      lastUpdated: new Date().toISOString(),
      dataSource: 'real'
    };

    console.log('✅ Données AI actualisées avec succès:', refreshedData);
    return refreshedData;

  } catch (error) {
    console.error('❌ Erreur lors de l\'actualisation des données AI:', error);
    throw error;
  }
}

export function getAIDataHealthIndicator(data: UnifiedAIData): {
  status: 'healthy' | 'warning' | 'critical';
  message: string;
  details: string[];
} {
  const details: string[] = [];
  let warningCount = 0;
  let criticalCount = 0;

  // Vérifier les modèles IA
  if (data.models.total_models === 0) {
    details.push('Aucun modèle IA disponible');
    criticalCount++;
  } else if (data.models.active_models === 0) {
    details.push('Aucun modèle IA actif');
    warningCount++;
  }

  // Vérifier la collecte de données
  if (data.dataCollection.total_sources === 0) {
    details.push('Aucune source de données configurée');
    criticalCount++;
  } else if (data.dataCollection.active_collections === 0) {
    details.push('Aucune collecte de données active');
    warningCount++;
  }

  // Vérifier les sessions d'entraînement
  if (data.trainingSessions.total_sessions === 0) {
    details.push('Aucune session d\'entraînement disponible');
    warningCount++;
  }

  // Déterminer le statut global
  let status: 'healthy' | 'warning' | 'critical' = 'healthy';
  let message = 'Tous les services AI fonctionnent correctement';

  if (criticalCount > 0) {
    status = 'critical';
    message = 'Services AI critiques non disponibles';
  } else if (warningCount > 0) {
    status = 'warning';
    message = 'Certains services AI nécessitent attention';
  }

  return {
    status,
    message,
    details
  };
}

// ============================================================================
// FONCTIONS D'EXPORT ET RAPPORTS
// ============================================================================

export async function exportAIReport(token: string, format: 'json' | 'csv'): Promise<Blob> {
  try {
    console.log('🔄 Export du rapport AI...');
    
    const aiData = await getAllUnifiedAIData(token);
    const status = await getAIStatus(token);
    const health = getAIDataHealthIndicator(aiData);
    
    const reportData = {
      timestamp: new Date().toISOString(),
      status,
      health,
      summary: {
        models: await getAIModelsSummary(token),
        dataCollection: await getDataCollectionSummary(token),
        trainingSessions: await getTrainingSessionsSummary(token)
      },
      data: aiData
    };

    if (format === 'json') {
      const blob = new Blob([JSON.stringify(reportData, null, 2)], {
        type: 'application/json'
      });
      return blob;
    } else {
      // Format CSV simplifié
      const csvContent = `Timestamp,Status,Models,Data Sources,Training Sessions,Health Status\n${reportData.timestamp},${status.overall_status},${reportData.summary.models.total_models},${reportData.summary.dataCollection.total_sources},${reportData.summary.trainingSessions.total_sessions},${health.status}`;
      const blob = new Blob([csvContent], { type: 'text/csv' });
      return blob;
    }

  } catch (error) {
    console.error('❌ Erreur lors de l\'export du rapport AI:', error);
    throw error;
  }
}



























