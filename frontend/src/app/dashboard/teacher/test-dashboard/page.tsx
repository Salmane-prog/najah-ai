'use client';

import React, { useState, useEffect } from 'react';
import Sidebar from '../../../../components/Sidebar';
import { useAuth  } from '../../../../hooks/useAuth';
import { getTeacherDashboardData } from '../../../../services/teacherDashboardService';
import { getAIAnalyticsData } from '../../../../services/aiAnalyticsService';
import { 
  BarChart3, 
  TrendingUp, 
  Users, 
  BookOpen, 
  Clock, 
  AlertTriangle, 
  CheckCircle,
  RefreshCw,
  Database,
  Activity,
  Brain,
  Target
} from 'lucide-react';

interface DashboardTestData {
  teacherDashboard: any;
  aiAnalytics: any;
  loading: boolean;
  error: string | null;
}

export default function TestDashboardPage() {
  const { user, token } = useAuth();
  const [testData, setTestData] = useState<DashboardTestData>({
    teacherDashboard: null,
    aiAnalytics: null,
    loading: false,
    error: null
  });

  const testEndpoints = async () => {
    if (!token) {
      setTestData(prev => ({ ...prev, error: 'Token non disponible' }));
      return;
    }

    setTestData(prev => ({ ...prev, loading: true, error: null }));

    try {
      console.log('🧪 Test des endpoints backend...');

      // Test 1: Teacher Dashboard
      console.log('📊 Test du Teacher Dashboard...');
      const dashboardData = await getTeacherDashboardData(token);
      console.log('✅ Teacher Dashboard récupéré:', dashboardData);

      // Test 2: AI Analytics
      console.log('🤖 Test des AI Analytics...');
      const aiData = await getAIAnalyticsData(token);
      console.log('✅ AI Analytics récupéré:', aiData);

      setTestData({
        teacherDashboard: dashboardData,
        aiAnalytics: aiData,
        loading: false,
        error: null
      });

    } catch (error) {
      console.error('❌ Erreur lors du test:', error);
      setTestData(prev => ({ 
        ...prev, 
        loading: false, 
        error: `Erreur: ${error instanceof Error ? error.message : 'Erreur inconnue'}` 
      }));
    }
  };

  useEffect(() => {
    if (token) {
      testEndpoints();
    }
  }, [token]);

  const formatData = (data: any) => {
    if (!data) return 'Aucune donnée';
    return JSON.stringify(data, null, 2);
  };

  if (!token) {
    return (
      <div className="flex min-h-screen bg-gray-50">
        <Sidebar />
        <div className="flex-1 ml-56 p-8">
          <div className="text-center">
            <AlertTriangle className="w-16 h-16 text-red-500 mx-auto mb-4" />
            <h1 className="text-2xl font-bold text-gray-900 mb-2">Authentification requise</h1>
            <p className="text-gray-600">Veuillez vous connecter pour tester les endpoints</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 ml-56 p-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Test des Endpoints Backend</h1>
          <p className="text-gray-600 mt-2">Vérification du fonctionnement des nouveaux endpoints avec données réelles</p>
        </div>

        {/* Test Controls */}
        <div className="mb-6">
          <button
            onClick={testEndpoints}
            disabled={testData.loading}
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50 flex items-center"
          >
            <RefreshCw className={`w-4 h-4 mr-2 ${testData.loading ? 'animate-spin' : ''}`} />
            {testData.loading ? 'Test en cours...' : 'Relancer les tests'}
          </button>
        </div>

        {/* Error Display */}
        {testData.error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-md">
            <div className="flex items-center">
              <AlertTriangle className="w-5 h-5 text-red-400 mr-2" />
              <span className="text-red-800">{testData.error}</span>
            </div>
          </div>
        )}

        {/* Results Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Teacher Dashboard Results */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center mb-4">
              <Database className="w-6 h-6 text-blue-600 mr-2" />
              <h2 className="text-xl font-semibold text-gray-900">Teacher Dashboard</h2>
            </div>
            
            {testData.loading ? (
              <div className="text-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                <p className="text-gray-600 mt-2">Test en cours...</p>
              </div>
            ) : testData.teacherDashboard ? (
              <div>
                <div className="mb-4">
                  <h3 className="text-lg font-medium text-gray-900 mb-2">Données récupérées:</h3>
                  <div className="grid grid-cols-2 gap-4 mb-4">
                    <div className="bg-blue-50 p-3 rounded-lg">
                      <div className="text-2xl font-bold text-blue-600">
                        {testData.teacherDashboard.overview?.classes || 0}
                      </div>
                      <div className="text-sm text-blue-600">Classes</div>
                    </div>
                    <div className="bg-green-50 p-3 rounded-lg">
                      <div className="text-2xl font-bold text-green-600">
                        {testData.teacherDashboard.overview?.students || 0}
                      </div>
                      <div className="text-sm text-green-600">Étudiants</div>
                    </div>
                  </div>
                </div>
                
                <details className="mt-4">
                  <summary className="cursor-pointer text-sm font-medium text-gray-700 hover:text-gray-900">
                    Voir les données complètes
                  </summary>
                  <pre className="mt-2 p-3 bg-gray-100 rounded text-xs overflow-auto max-h-64">
                    {formatData(testData.teacherDashboard)}
                  </pre>
                </details>
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500">
                <Database className="w-12 h-12 mx-auto mb-2 text-gray-300" />
                <p>Aucune donnée récupérée</p>
              </div>
            )}
          </div>

          {/* AI Analytics Results */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center mb-4">
              <Brain className="w-6 h-6 text-purple-600 mr-2" />
              <h2 className="text-xl font-semibold text-gray-900">AI Analytics</h2>
            </div>
            
            {testData.loading ? (
              <div className="text-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600 mx-auto"></div>
                <p className="text-gray-600 mt-2">Test en cours...</p>
              </div>
            ) : testData.aiAnalytics ? (
              <div>
                <div className="mb-4">
                  <h3 className="text-lg font-medium text-gray-900 mb-2">Données récupérées:</h3>
                  <div className="grid grid-cols-2 gap-4 mb-4">
                    <div className="bg-purple-50 p-3 rounded-lg">
                      <div className="text-2xl font-bold text-purple-600">
                        {testData.aiAnalytics.predictions?.total_predictions || 0}
                      </div>
                      <div className="text-sm text-purple-600">Prédictions</div>
                    </div>
                    <div className="bg-orange-50 p-3 rounded-lg">
                      <div className="text-2xl font-bold text-orange-600">
                        {testData.aiAnalytics.blockages?.total_blockages || 0}
                      </div>
                      <div className="text-sm text-orange-600">Blocages</div>
                    </div>
                  </div>
                </div>
                
                <details className="mt-4">
                  <summary className="cursor-pointer text-sm font-medium text-gray-700 hover:text-gray-900">
                    Voir les données complètes
                  </summary>
                  <pre className="mt-2 p-3 bg-gray-100 rounded text-xs overflow-auto max-h-64">
                    {formatData(testData.aiAnalytics)}
                  </pre>
                </details>
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500">
                <Brain className="w-12 h-12 mx-auto mb-2 text-gray-300" />
                <p>Aucune donnée récupérée</p>
              </div>
            )}
          </div>
        </div>

        {/* Status Summary */}
        <div className="mt-8 bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Résumé des Tests</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="flex items-center p-3 rounded-lg bg-gray-50">
              <div className={`w-3 h-3 rounded-full mr-3 ${
                testData.teacherDashboard ? 'bg-green-500' : 'bg-gray-300'
              }`}></div>
              <span className="text-sm font-medium">
                Teacher Dashboard: {testData.teacherDashboard ? '✅ Fonctionne' : '❌ Échec'}
              </span>
            </div>
            
            <div className="flex items-center p-3 rounded-lg bg-gray-50">
              <div className={`w-3 h-3 rounded-full mr-3 ${
                testData.aiAnalytics ? 'bg-green-500' : 'bg-gray-300'
              }`}></div>
              <span className="text-sm font-medium">
                AI Analytics: {testData.aiAnalytics ? '✅ Fonctionne' : '❌ Échec'}
              </span>
            </div>
            
            <div className="flex items-center p-3 rounded-lg bg-gray-50">
              <div className={`w-3 h-3 rounded-full mr-3 ${
                testData.error ? 'bg-red-500' : 'bg-green-500'
              }`}></div>
              <span className="text-sm font-medium">
                Statut: {testData.error ? '❌ Erreur' : '✅ OK'}
              </span>
            </div>
          </div>
        </div>

        {/* Instructions */}
        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-2">Instructions de Test</h3>
          <div className="text-blue-800 text-sm space-y-2">
            <p>• Cette page teste la connexion entre le frontend et les nouveaux endpoints backend</p>
            <p>• Les tests vérifient que les données réelles sont récupérées depuis la base de données</p>
            <p>• Si les tests échouent, vérifiez que le serveur backend est démarré sur le port 8000</p>
            <p>• Les données affichées proviennent directement de votre base de données SQLite</p>
          </div>
        </div>
      </div>
    </div>
  );
}



























