'use client';

import React, { useState } from 'react';
import Sidebar from '../../../../components/Sidebar';
import { useAuth  } from '../../../../hooks/useAuth';
import { getTeacherDashboardData } from '../../../../services/teacherDashboardService';
import { getAIAnalyticsData } from '../../../../services/aiAnalyticsService';
import { 
  Play, 
  CheckCircle, 
  XCircle, 
  AlertTriangle,
  Database,
  Brain,
  RefreshCw
} from 'lucide-react';

interface TestResult {
  name: string;
  success: boolean;
  data?: any;
  error?: string;
  loading: boolean;
}

export default function TestServicesPage() {
  const { user, token } = useAuth();
  const [testResults, setTestResults] = useState<TestResult[]>([
    { name: 'Teacher Dashboard Service', success: false, loading: false },
    { name: 'AI Analytics Service', success: false, loading: false }
  ]);
  const [isRunning, setIsRunning] = useState(false);

  const runTests = async () => {
    if (!token) {
      alert('Token non disponible. Veuillez vous connecter.');
      return;
    }

    setIsRunning(true);
    setTestResults(prev => prev.map(test => ({ ...test, loading: true })));

    try {
      // Test 1: Teacher Dashboard Service
      console.log('🧪 Test du Teacher Dashboard Service...');
      try {
        const dashboardData = await getTeacherDashboardData(token);
        console.log('✅ Teacher Dashboard Service - Succès:', dashboardData);
        
        setTestResults(prev => prev.map(test => 
          test.name === 'Teacher Dashboard Service' 
            ? { ...test, success: true, data: dashboardData, loading: false }
            : test
        ));
      } catch (error) {
        console.error('❌ Teacher Dashboard Service - Erreur:', error);
        setTestResults(prev => prev.map(test => 
          test.name === 'Teacher Dashboard Service' 
            ? { ...test, success: false, error: error instanceof Error ? error.message : 'Erreur inconnue', loading: false }
            : test
        ));
      }

      // Test 2: AI Analytics Service
      console.log('🧪 Test du AI Analytics Service...');
      try {
        const aiData = await getAIAnalyticsData(token);
        console.log('✅ AI Analytics Service - Succès:', aiData);
        
        setTestResults(prev => prev.map(test => 
          test.name === 'AI Analytics Service' 
            ? { ...test, success: true, data: aiData, loading: false }
            : test
        ));
      } catch (error) {
        console.error('❌ AI Analytics Service - Erreur:', error);
        setTestResults(prev => prev.map(test => 
          test.name === 'AI Analytics Service' 
            ? { ...test, success: false, error: error instanceof Error ? error.message : 'Erreur inconnue', loading: false }
            : test
        ));
      }

    } catch (error) {
      console.error('❌ Erreur générale lors des tests:', error);
    } finally {
      setIsRunning(false);
    }
  };

  const getStatusIcon = (result: TestResult) => {
    if (result.loading) {
      return <RefreshCw className="w-5 h-5 text-blue-500 animate-spin" />;
    }
    if (result.success) {
      return <CheckCircle className="w-5 h-5 text-green-500" />;
    }
    return <XCircle className="w-5 h-5 text-red-500" />;
  };

  const getStatusColor = (result: TestResult) => {
    if (result.loading) return 'border-blue-200 bg-blue-50';
    if (result.success) return 'border-green-200 bg-green-50';
    return 'border-red-200 bg-red-50';
  };

  if (!token) {
    return (
      <div className="flex min-h-screen bg-gray-50">
        <Sidebar />
        <div className="flex-1 ml-56 p-8">
          <div className="text-center">
            <AlertTriangle className="w-16 h-16 text-red-500 mx-auto mb-4" />
            <h1 className="text-2xl font-bold text-gray-900 mb-2">Authentification requise</h1>
            <p className="text-gray-600">Veuillez vous connecter pour tester les services</p>
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
          <h1 className="text-3xl font-bold text-gray-900">Test des Services Frontend</h1>
          <p className="text-gray-600 mt-2">Vérification du fonctionnement des services avec les endpoints backend</p>
        </div>

        {/* Test Controls */}
        <div className="mb-6">
          <button
            onClick={runTests}
            disabled={isRunning}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center text-lg"
          >
            <Play className="w-5 h-5 mr-2" />
            {isRunning ? 'Tests en cours...' : 'Lancer les tests'}
          </button>
        </div>

        {/* Test Results */}
        <div className="space-y-4">
          {testResults.map((result, index) => (
            <div key={index} className={`border rounded-lg p-6 ${getStatusColor(result)}`}>
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-3">
                  {getStatusIcon(result)}
                  <h3 className="text-lg font-semibold text-gray-900">{result.name}</h3>
                </div>
                <div className="flex items-center space-x-2">
                  {result.loading && (
                    <span className="text-blue-600 text-sm">Test en cours...</span>
                  )}
                  {!result.loading && result.success && (
                    <span className="text-green-600 text-sm font-medium">✅ Succès</span>
                  )}
                  {!result.loading && !result.success && (
                    <span className="text-red-600 text-sm font-medium">❌ Échec</span>
                  )}
                </div>
              </div>

              {result.loading && (
                <div className="text-center py-4">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                  <p className="text-gray-600 mt-2">Test en cours...</p>
                </div>
              )}

              {!result.loading && result.success && result.data && (
                <div>
                  <h4 className="text-md font-medium text-gray-900 mb-2">Données récupérées:</h4>
                  <div className="bg-white rounded-lg p-4 border">
                    <pre className="text-sm text-gray-800 overflow-auto max-h-48">
                      {JSON.stringify(result.data, null, 2)}
                    </pre>
                  </div>
                </div>
              )}

              {!result.loading && !result.success && result.error && (
                <div>
                  <h4 className="text-md font-medium text-red-900 mb-2">Erreur:</h4>
                  <div className="bg-red-50 rounded-lg p-4 border border-red-200">
                    <p className="text-red-800">{result.error}</p>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Summary */}
        <div className="mt-8 bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Résumé des Tests</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-gray-900">
                {testResults.filter(r => r.success).length}
              </div>
              <div className="text-sm text-gray-600">Tests réussis</div>
            </div>
            
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-gray-900">
                {testResults.filter(r => !r.success && !r.loading).length}
              </div>
              <div className="text-sm text-gray-600">Tests échoués</div>
            </div>
            
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-gray-900">
                {testResults.filter(r => r.loading).length}
              </div>
              <div className="text-sm text-gray-600">En cours</div>
            </div>
          </div>

          <div className="mt-6 p-4 bg-blue-50 rounded-lg">
            <h4 className="font-medium text-blue-900 mb-2">Instructions:</h4>
            <ul className="text-blue-800 text-sm space-y-1">
              <li>• Cliquez sur "Lancer les tests" pour vérifier les services</li>
              <li>• Les tests vérifient la connexion avec les endpoints backend</li>
              <li>• Assurez-vous que le serveur backend est démarré sur le port 8000</li>
              <li>• Vérifiez que vous êtes connecté avec un compte professeur</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}



























