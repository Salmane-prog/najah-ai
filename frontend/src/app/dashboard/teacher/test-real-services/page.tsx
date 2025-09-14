'use client';

import { useState, useEffect } from 'react';
import { teacherDashboardService } from '../../../../services/teacherDashboardService';
import { aiAnalyticsService } from '../../../../services/aiAnalyticsService';
import { realAIModelsService } from '../../../../services/realAIModelsService';
import { TeacherDashboardData, TeacherAnalytics } from '../../../../types/teacherDashboard';
import { AIAnalyticsData } from '../../../../types/aiAnalytics';
import { AIModel } from '../../../../types/aiModels';

export default function TestRealServicesPage() {
  const [dashboardData, setDashboardData] = useState<TeacherDashboardData | null>(null);
  const [analyticsData, setAnalyticsData] = useState<TeacherAnalytics | null>(null);
  const [aiAnalyticsData, setAiAnalyticsData] = useState<AIAnalyticsData | null>(null);
  const [aiModels, setAiModels] = useState<AIModel[]>([]);
  const [loading, setLoading] = useState(false);
  const [logs, setLogs] = useState<string[]>([]);

  const addLog = (message: string) => {
    setLogs(prev => [...prev, `${new Date().toLocaleTimeString()}: ${message}`]);
  };

  const testAllServices = async () => {
    setLoading(true);
    setLogs([]);
    
    try {
      addLog('🚀 Début des tests des services connectés aux vrais endpoints...');
      
      // Test Teacher Dashboard Service
      addLog('📊 Test du service Teacher Dashboard...');
      const dashboard = await teacherDashboardService.getTeacherDashboardData();
      setDashboardData(dashboard);
      addLog('✅ Teacher Dashboard récupéré avec succès');
      
      // Test Teacher Analytics
      addLog('📈 Test du service Teacher Analytics...');
      const analytics = await teacherDashboardService.getTeacherAnalytics();
      setAnalyticsData(analytics);
      addLog('✅ Teacher Analytics récupéré avec succès');
      
      // Test AI Analytics Service
      addLog('🤖 Test du service AI Analytics...');
      const aiAnalytics = await aiAnalyticsService.getAIAnalyticsData();
      setAiAnalyticsData(aiAnalytics);
      addLog('✅ AI Analytics récupéré avec succès');
      
      // Test AI Models Service
      addLog('🧠 Test du service AI Models...');
      const models = await realAIModelsService.getRealAIModels();
      setAiModels(models);
      addLog('✅ AI Models récupéré avec succès');
      
      addLog('🎉 Tous les tests sont terminés avec succès !');
      
    } catch (error) {
      addLog(`❌ Erreur lors des tests: ${error}`);
    } finally {
      setLoading(false);
    }
  };

  const clearLogs = () => {
    setLogs([]);
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            🧪 Test des Services Connectés aux Vrais Endpoints
          </h1>
          <p className="text-gray-600 mb-6">
            Cette page teste la connexion entre le frontend et les vrais endpoints backend.
            Les services tentent d'abord de récupérer des données réelles, puis utilisent des données par défaut en cas d'échec.
          </p>
          
          <div className="flex gap-4 mb-6">
            <button
              onClick={testAllServices}
              disabled={loading}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-6 py-3 rounded-lg font-semibold transition-colors"
            >
              {loading ? '🔄 Test en cours...' : '🚀 Tester Tous les Services'}
            </button>
            
            <button
              onClick={clearLogs}
              className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-3 rounded-lg font-semibold transition-colors"
            >
              🗑️ Effacer les Logs
            </button>
          </div>
        </div>

        {/* Logs */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">📋 Logs des Tests</h2>
          <div className="bg-gray-900 text-green-400 p-4 rounded-lg font-mono text-sm max-h-96 overflow-y-auto">
            {logs.length === 0 ? (
              <span className="text-gray-500">Aucun log pour le moment. Cliquez sur "Tester Tous les Services" pour commencer.</span>
            ) : (
              logs.map((log, index) => (
                <div key={index} className="mb-1">
                  {log}
                </div>
              ))
            )}
          </div>
        </div>

        {/* Résultats des Tests */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Teacher Dashboard */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">📊 Teacher Dashboard</h2>
            {dashboardData ? (
              <div className="space-y-3">
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-blue-50 p-3 rounded-lg">
                    <div className="text-2xl font-bold text-blue-600">{dashboardData.overview.total_students}</div>
                    <div className="text-sm text-blue-800">Étudiants</div>
                  </div>
                  <div className="bg-green-50 p-3 rounded-lg">
                    <div className="text-2xl font-bold text-green-600">{dashboardData.overview.total_quizzes}</div>
                    <div className="text-sm text-green-800">Quiz</div>
                  </div>
                </div>
                <div className="text-sm text-gray-600">
                  Classes: {dashboardData.overview.total_classes} | 
                  Devoirs: {dashboardData.overview.total_assignments} | 
                  Soumissions en attente: {dashboardData.overview.pending_submissions}
                </div>
              </div>
            ) : (
              <div className="text-gray-500">Aucune donnée disponible</div>
            )}
          </div>

          {/* Teacher Analytics */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">📈 Teacher Analytics</h2>
            {analyticsData ? (
              <div className="space-y-3">
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-purple-50 p-3 rounded-lg">
                    <div className="text-2xl font-bold text-purple-600">{analyticsData.total_students}</div>
                    <div className="text-sm text-purple-800">Total Étudiants</div>
                  </div>
                  <div className="bg-orange-50 p-3 rounded-lg">
                    <div className="text-2xl font-bold text-orange-600">{analyticsData.total_quizzes}</div>
                    <div className="text-sm text-orange-800">Total Quiz</div>
                  </div>
                </div>
                <div className="text-sm text-gray-600">
                  {analyticsData.class_performances.length} classes analysées
                </div>
              </div>
            ) : (
              <div className="text-gray-500">Aucune donnée disponible</div>
            )}
          </div>

          {/* AI Analytics */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">🤖 AI Analytics</h2>
            {aiAnalyticsData ? (
              <div className="space-y-3">
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-indigo-50 p-3 rounded-lg">
                    <div className="text-2xl font-bold text-indigo-600">{aiAnalyticsData.overview.total_models}</div>
                    <div className="text-sm text-indigo-800">Modèles IA</div>
                  </div>
                  <div className="bg-pink-50 p-3 rounded-lg">
                    <div className="text-2xl font-bold text-pink-600">{aiAnalyticsData.overview.accuracy_rate}%</div>
                    <div className="text-sm text-pink-800">Précision</div>
                  </div>
                </div>
                <div className="text-sm text-gray-600">
                  {aiAnalyticsData.overview.active_models} modèles actifs | 
                  {aiAnalyticsData.overview.total_predictions} prédictions
                </div>
              </div>
            ) : (
              <div className="text-gray-500">Aucune donnée disponible</div>
            )}
          </div>

          {/* AI Models */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">🧠 AI Models</h2>
            {aiModels.length > 0 ? (
              <div className="space-y-3">
                <div className="text-2xl font-bold text-gray-900">{aiModels.length}</div>
                <div className="text-sm text-gray-600">Modèles disponibles</div>
                <div className="space-y-2">
                  {aiModels.slice(0, 3).map((model) => (
                    <div key={model.id} className="bg-gray-50 p-2 rounded text-sm">
                      <div className="font-medium">{model.name}</div>
                      <div className="text-gray-600 text-xs">
                        {model.model_type} • v{model.version} • {model.accuracy}% précision
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="text-gray-500">Aucun modèle disponible</div>
            )}
          </div>
        </div>

        {/* Instructions */}
        <div className="bg-blue-50 rounded-lg p-6 mt-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-3">💡 Comment interpréter les résultats</h3>
          <ul className="text-blue-800 space-y-2 text-sm">
            <li>• <strong>✅ Données réelles récupérées du backend</strong> : Le service a réussi à se connecter au backend et récupérer des données réelles</li>
            <li>• <strong>🔄 Utilisation des données par défaut</strong> : Le service n'a pas pu se connecter au backend et utilise des données de fallback</li>
            <li>• <strong>🔒 Non autorisé (authentification requise)</strong> : L'endpoint nécessite une authentification (token valide)</li>
            <li>• <strong>🚫 Interdit (permissions insuffisantes)</strong> : L'utilisateur n'a pas les permissions nécessaires</li>
            <li>• <strong>❌ Endpoint non trouvé</strong> : L'URL de l'endpoint n'existe pas</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
