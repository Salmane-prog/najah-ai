'use client';

import React, { useState, useEffect } from 'react';
import { ArrowLeft, Brain, Users, TrendingUp, TrendingDown, Clock, Target, BarChart3, Eye, Zap, RefreshCw } from 'lucide-react';
import Link from 'next/link';
import { Card } from '../../../../../components/Card';
import Sidebar from '../../../../../components/Sidebar';
import { useAuth } from '../../../../../hooks/useAuth';
import { adaptiveEvaluationService } from '../../../../../services/adaptiveEvaluationService';

interface StudentActivity {
  id: number;
  name: string;
  testId: number;
  testTitle: string;
  currentQuestion: number;
  totalQuestions: number;
  difficulty: number;
  confidence: number;
  timeSpent: number;
  status: 'active' | 'completed' | 'paused';
  lastActivity: string;
}

interface TestPerformance {
  testId: number;
  title: string;
  activeStudents: number;
  averageDifficulty: number;
  averageConfidence: number;
  completionRate: number;
  averageTime: number;
}

export default function AdaptiveMonitoringPage() {
  const { user } = useAuth();
  const [activeStudents, setActiveStudents] = useState<StudentActivity[]>([]);
  const [testPerformance, setTestPerformance] = useState<TestPerformance[]>([]);
  const [selectedTest, setSelectedTest] = useState<number | null>(null);
  const [realTimeUpdates, setRealTimeUpdates] = useState(true);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Charger les données réelles
  const loadRealData = async () => {
    if (!user?.id) return;
    
    try {
      setIsLoading(true);
      setError(null);
      
      console.log('🔄 Chargement des données de monitoring réelles...');
      
      const monitoringData = await adaptiveEvaluationService.getRealTimeMonitoring(user.id);
      
      console.log('✅ Données de monitoring récupérées:', monitoringData);
      
      setActiveStudents(monitoringData.activities);
      setTestPerformance(monitoringData.performances);
      
    } catch (error) {
      console.error('❌ Erreur lors du chargement des données de monitoring:', error);
      setError('Erreur lors du chargement des données');
      
      // Fallback vers des données vides en cas d'erreur
      setActiveStudents([]);
      setTestPerformance([]);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadRealData();
  }, [user?.id]);

  // Rafraîchissement automatique des données réelles
  useEffect(() => {
    if (!user?.id || !realTimeUpdates) return;
    
    const interval = setInterval(() => {
      console.log('🔄 Rafraîchissement automatique des données de monitoring...');
      loadRealData();
    }, 30000); // Rafraîchir toutes les 30 secondes

    return () => clearInterval(interval);
  }, [user?.id, realTimeUpdates]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-green-600 bg-green-100';
      case 'completed': return 'text-blue-600 bg-blue-100';
      case 'paused': return 'text-yellow-600 bg-yellow-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active': return <TrendingUp className="w-4 h-4" />;
      case 'completed': return <Target className="w-4 h-4" />;
      case 'paused': return <Clock className="w-4 h-4" />;
      default: return <Clock className="w-4 h-4" />;
    }
  };

  const getDifficultyColor = (difficulty: number) => {
    if (difficulty <= 4) return 'text-green-600';
    if (difficulty <= 6) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.7) return 'text-green-600';
    if (confidence >= 0.5) return 'text-yellow-600';
    return 'text-red-600';
  };

  const filteredStudents = selectedTest 
    ? activeStudents.filter(student => student.testId === selectedTest)
    : activeStudents;

  if (isLoading) {
    return (
      <div className="flex h-screen bg-gray-50">
        <Sidebar />
        <div className="flex-1 ml-56 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-purple-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Chargement des données de monitoring...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex h-screen bg-gray-50">
        <Sidebar />
        <div className="flex-1 ml-56 p-8">
          <div className="bg-red-50 border border-red-200 rounded-2xl p-6 shadow-lg">
            <h2 className="text-red-800 font-semibold mb-2 text-lg">Erreur</h2>
            <p className="text-red-700">{error}</p>
            <button 
              onClick={loadRealData}
              className="mt-4 bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-xl"
            >
              Réessayer
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 ml-56 p-8 overflow-y-auto">
        {/* Header */}
        <div className="mb-8">
          <Link
            href="/dashboard/teacher/adaptive-evaluation"
            className="inline-flex items-center text-purple-600 hover:text-purple-700 mb-4"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Retour à l'évaluation adaptative
          </Link>
          <h1 className="text-3xl font-bold text-gray-900">Monitoring en Temps Réel</h1>
          <p className="text-gray-600 mt-2">
            Surveillez l'activité de vos tests adaptatifs et l'évolution des performances des élèves
          </p>
          <div className="mt-2 flex items-center space-x-2">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <span className="text-sm text-green-600 font-medium">Données en temps réel</span>
          </div>
        </div>

        {/* Contrôles */}
        <div className="mb-6 flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center space-x-4">
            <select
              value={selectedTest || ''}
              onChange={(e) => setSelectedTest(e.target.value ? parseInt(e.target.value) : null)}
              className="px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            >
              <option value="">Tous les tests</option>
              {testPerformance.map(test => (
                <option key={test.testId} value={test.testId}>{test.title}</option>
              ))}
            </select>
          </div>

          <div className="flex items-center space-x-4">
            <button
              onClick={loadRealData}
              disabled={isLoading}
              className="bg-purple-600 hover:bg-purple-700 disabled:bg-purple-400 text-white px-4 py-2 rounded-xl flex items-center space-x-2"
            >
              <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
              <span>{isLoading ? 'Chargement...' : 'Actualiser'}</span>
            </button>
            
            <label className="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={realTimeUpdates}
                onChange={(e) => setRealTimeUpdates(e.target.checked)}
                className="rounded border-gray-300 text-purple-600 focus:ring-purple-500"
              />
              <span className="text-sm text-gray-700">Mises à jour en temps réel</span>
            </label>
          </div>
        </div>

        {/* Statistiques globales */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="p-6">
            <div className="flex items-center space-x-3">
              <div className="p-3 bg-blue-100 rounded-xl">
                <Users className="h-6 w-6 text-blue-600" />
              </div>
              <div>
                <p className="text-sm font-medium text-gray-600">Élèves Actifs</p>
                <p className="text-2xl font-bold text-gray-900">
                  {activeStudents.filter(s => s.status === 'active').length}
                </p>
              </div>
            </div>
          </Card>
          
          <Card className="p-6">
            <div className="flex items-center space-x-3">
              <div className="p-3 bg-green-100 rounded-xl">
                <Target className="h-6 w-6 text-green-600" />
              </div>
              <div>
                <p className="text-sm font-medium text-gray-600">Tests Terminés</p>
                <p className="text-2xl font-bold text-gray-900">
                  {activeStudents.filter(s => s.status === 'completed').length}
                </p>
              </div>
            </div>
          </Card>
          
          <Card className="p-6">
            <div className="flex items-center space-x-3">
              <div className="p-3 bg-purple-100 rounded-xl">
                <BarChart3 className="h-6 w-6 text-purple-600" />
              </div>
              <div>
                <p className="text-sm font-medium text-gray-600">Tests en Cours</p>
                <p className="text-2xl font-bold text-gray-900">{testPerformance.length}</p>
              </div>
            </div>
          </Card>
          
          <Card className="p-6">
            <div className="flex items-center space-x-3">
              <div className="p-3 bg-orange-100 rounded-xl">
                <TrendingUp className="h-6 w-6 text-orange-600" />
              </div>
              <div>
                <p className="text-sm font-medium text-gray-600">Confiance Moyenne</p>
                <p className="text-2xl font-bold text-gray-900">
                  {Math.round(activeStudents.reduce((sum, s) => sum + s.confidence, 0) / activeStudents.length * 100)}%
                </p>
              </div>
            </div>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Activité des élèves en temps réel */}
          <div className="lg:col-span-2">
            <Card className="p-6 rounded-2xl">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-gray-900">Activité des Élèves</h2>
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                  <span className="text-sm text-gray-500">En temps réel</span>
                </div>
              </div>

              <div className="space-y-4">
                {filteredStudents.map((student) => (
                  <div key={student.id} className="border border-gray-200 rounded-xl p-4 hover:bg-gray-50 transition-colors">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center">
                          <span className="text-purple-600 font-semibold">
                            {student.name.split(' ').map(n => n[0]).join('')}
                          </span>
                        </div>
                        <div>
                          <div className="font-medium text-gray-900">{student.name}</div>
                          <div className="text-sm text-gray-500">{student.testTitle}</div>
                        </div>
                      </div>
                      
                      <div className="flex items-center space-x-2">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(student.status)}`}>
                          {student.status === 'active' ? 'En cours' : 
                           student.status === 'completed' ? 'Terminé' : 'En pause'}
                        </span>
                        {getStatusIcon(student.status)}
                      </div>
                    </div>

                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                      <div>
                        <div className="text-gray-500">Question</div>
                        <div className="font-medium text-gray-900">
                          {student.currentQuestion}/{student.totalQuestions}
                        </div>
                      </div>
                      
                      <div>
                        <div className="text-gray-500">Difficulté</div>
                        <div className={`font-medium ${getDifficultyColor(student.difficulty)}`}>
                          {student.difficulty.toFixed(1)}
                        </div>
                      </div>
                      
                      <div>
                        <div className="text-gray-500">Confiance</div>
                        <div className={`font-medium ${getConfidenceColor(student.confidence)}`}>
                          {Math.round(student.confidence * 100)}%
                        </div>
                      </div>
                      
                      <div>
                        <div className="text-gray-500">Temps</div>
                        <div className="font-medium text-gray-900">
                          {Math.floor(student.timeSpent / 60)}:{(student.timeSpent % 60).toString().padStart(2, '0')}
                        </div>
                      </div>
                    </div>

                    <div className="mt-3 pt-3 border-t border-gray-200">
                      <div className="flex items-center justify-between text-xs text-gray-500">
                        <span>Dernière activité: {student.lastActivity}</span>
                        <button className="text-purple-600 hover:text-purple-700 flex items-center space-x-1">
                          <Eye className="w-3 h-3" />
                          <span>Voir détails</span>
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          </div>

          {/* Performance des tests */}
          <div>
            <Card className="p-6 rounded-2xl">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Performance des Tests</h2>
              
              <div className="space-y-4">
                {testPerformance.map((test) => (
                  <div key={test.testId} className="border border-gray-200 rounded-xl p-4">
                    <h3 className="font-medium text-gray-900 mb-3">{test.title}</h3>
                    
                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">Élèves actifs</span>
                        <span className="font-medium text-blue-600">{test.activeStudents}</span>
                      </div>
                      
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">Difficulté moyenne</span>
                        <span className={`font-medium ${getDifficultyColor(test.averageDifficulty)}`}>
                          {test.averageDifficulty.toFixed(1)}
                        </span>
                      </div>
                      
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">Confiance moyenne</span>
                        <span className={`font-medium ${getConfidenceColor(test.averageConfidence)}`}>
                          {Math.round(test.averageConfidence * 100)}%
                        </span>
                      </div>
                      
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">Taux de completion</span>
                        <span className="font-medium text-green-600">{test.completionRate}%</span>
                      </div>
                      
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">Temps moyen</span>
                        <span className="font-medium text-gray-900">
                          {Math.floor(test.averageTime / 60)}:{(test.averageTime % 60).toString().padStart(2, '0')}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </Card>

            {/* Insights IA */}
            <Card className="p-6 mt-6 rounded-2xl">
              <div className="flex items-center mb-4">
                <Brain className="w-5 h-5 text-purple-600 mr-2" />
                <h3 className="text-lg font-semibold text-gray-900">Insights IA</h3>
              </div>
              
              <div className="space-y-3 text-sm">
                <div className="p-3 bg-purple-50 rounded-xl">
                  <div className="font-medium text-purple-800 mb-1">Adaptation en Temps Réel</div>
                  <p className="text-purple-700">
                    L'algorithme s'adapte automatiquement à chaque réponse des élèves
                  </p>
                </div>
                
                <div className="p-3 bg-blue-50 rounded-xl">
                  <div className="font-medium text-blue-800 mb-1">Optimisation des Questions</div>
                  <p className="text-blue-700">
                    Sélection intelligente basée sur les patterns d'apprentissage
                  </p>
                </div>
                
                <div className="p-3 bg-green-50 rounded-xl">
                  <div className="font-medium text-green-800 mb-1">Prédiction de Performance</div>
                  <p className="text-green-700">
                    Analyse prédictive pour identifier les difficultés potentielles
                  </p>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}



















