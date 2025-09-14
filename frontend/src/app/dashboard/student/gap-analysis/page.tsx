'use client';

import React, { useEffect, useState } from 'react';
import { useAuth } from '@/hooks/useAuthSimple';
import { GapAnalysisService, GapAnalysis, WeakArea } from '@/services/gapAnalysisService';
import { Target, TrendingUp, Clock, AlertTriangle, CheckCircle, BookOpen, Brain, Zap, BarChart3, PieChart, Activity, TrendingDown, Star } from 'lucide-react';

// Import et configuration de Chart.js
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  BarElement,
  ArcElement,
  RadialLinearScale,
} from 'chart.js';

// Enregistrement des composants Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  BarElement,
  ArcElement,
  RadialLinearScale
);

// Import des composants de graphiques
import { Bar, Doughnut, Radar } from 'react-chartjs-2';

export default function GapAnalysisPage() {
  const { user, token } = useAuth();
  const [gapAnalysis, setGapAnalysis] = useState<GapAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedSubject, setSelectedSubject] = useState('Français');

  // Configuration des graphiques Chart.js
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const,
        labels: {
          font: {
            size: 12,
            weight: 'bold'
          },
          color: '#374151'
        }
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: '#fff',
        bodyColor: '#fff',
        borderColor: '#6366f1',
        borderWidth: 1,
        cornerRadius: 8,
        displayColors: true
      }
    }
  };

  // Données pour le graphique en barres des scores par domaine
  const getBarChartData = () => {
    if (!gapAnalysis) return null;
    
    const labels = gapAnalysis.weak_areas.map(area => area.topic);
    const scores = gapAnalysis.weak_areas.map(area => area.success_rate);
    const colors = gapAnalysis.weak_areas.map(area => {
      if (area.success_rate >= 70) return 'rgba(34, 197, 94, 0.8)';
      if (area.success_rate >= 50) return 'rgba(251, 191, 36, 0.8)';
      return 'rgba(239, 68, 68, 0.8)';
    });

    return {
      labels,
      datasets: [{
        label: 'Score (%)',
        data: scores,
        backgroundColor: colors,
        borderColor: colors.map(color => color.replace('0.8', '1')),
        borderWidth: 2,
        borderRadius: 8,
        borderSkipped: false,
        barThickness: 20,
        maxBarThickness: 30
      }]
    };
  };

  // Données pour le graphique circulaire des niveaux
  const getDoughnutChartData = () => {
    if (!gapAnalysis) return null;
    
    const mastered = gapAnalysis.weak_areas.filter(area => area.success_rate >= 70).length;
    const inProgress = gapAnalysis.weak_areas.filter(area => area.success_rate >= 50 && area.success_rate < 70).length;
    const toImprove = gapAnalysis.weak_areas.filter(area => area.success_rate < 50).length;

    return {
      labels: ['Maîtrisés', 'En cours', 'À améliorer'],
      datasets: [{
        data: [mastered, inProgress, toImprove],
        backgroundColor: [
          'rgba(34, 197, 94, 0.8)',
          'rgba(251, 191, 36, 0.8)',
          'rgba(239, 68, 68, 0.8)'
        ],
        borderColor: [
          'rgba(34, 197, 94, 1)',
          'rgba(251, 191, 36, 1)',
          'rgba(239, 68, 68, 1)'
        ],
        borderWidth: 3,
        cutout: '60%'
      }]
    };
  };

  // Données pour le graphique radar des compétences
  const getRadarChartData = () => {
    if (!gapAnalysis) return null;
    
    const labels = gapAnalysis.weak_areas.slice(0, 6).map(area => area.topic);
    const scores = gapAnalysis.weak_areas.slice(0, 6).map(area => area.success_rate);
    const targets = gapAnalysis.weak_areas.slice(0, 6).map(area => area.target_level * 10);

    return {
      labels,
      datasets: [
        {
          label: 'Niveau actuel',
          data: scores,
          backgroundColor: 'rgba(99, 102, 241, 0.2)',
          borderColor: 'rgba(99, 102, 241, 1)',
          borderWidth: 3,
          pointBackgroundColor: 'rgba(99, 102, 241, 1)',
          pointBorderColor: '#fff',
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: 'rgba(99, 102, 241, 1)'
        },
        {
          label: 'Niveau cible',
          data: targets,
          backgroundColor: 'rgba(34, 197, 94, 0.2)',
          borderColor: 'rgba(34, 197, 94, 1)',
          borderWidth: 2,
          borderDash: [5, 5],
          pointBackgroundColor: 'rgba(34, 197, 94, 1)',
          pointBorderColor: '#fff',
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: 'rgba(34, 197, 94, 1)'
        }
      ]
    };
  };

  useEffect(() => {
    if (user && token) {
      loadGapAnalysis();
    }
  }, [user, token, selectedSubject]);

  const loadGapAnalysis = async () => {
    if (!user || !token) return;

    setLoading(true);
    setError(null);

    try {
      console.log('🔍 [GAP ANALYSIS PAGE] Chargement de l\'analyse...');
      console.log('🔍 [GAP ANALYSIS PAGE] User ID:', user.id);
      console.log('🔍 [GAP ANALYSIS PAGE] Token présent:', !!token);
      console.log('🔍 [GAP ANALYSIS PAGE] Matière sélectionnée:', selectedSubject);
      
      const analysis = await GapAnalysisService.analyzeGaps(token, user.id, selectedSubject);
      console.log('✅ [GAP ANALYSIS PAGE] Analyse reçue:', analysis);
      
      setGapAnalysis(analysis);
      console.log('✅ [GAP ANALYSIS PAGE] Analyse chargée dans l\'état');
    } catch (error) {
      console.error('❌ [GAP ANALYSIS PAGE] Erreur:', error);
      setError('Erreur lors du chargement de l\'analyse des lacunes');
    } finally {
      setLoading(false);
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'text-red-600 bg-red-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      case 'low': return 'text-green-600 bg-green-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getPriorityIcon = (priority: string) => {
    switch (priority) {
      case 'high': return <AlertTriangle className="w-5 h-5" />;
      case 'medium': return <Clock className="w-5 h-5" />;
      case 'low': return <CheckCircle className="w-5 h-5" />;
      default: return <Clock className="w-5 h-5" />;
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-blue-600';
    if (score >= 40) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreMessage = (score: number) => {
    if (score >= 80) return 'Excellent niveau !';
    if (score >= 60) return 'Bon niveau, continuez !';
    if (score >= 40) return 'Niveau moyen, des efforts sont nécessaires';
    return 'Niveau faible, remédiation urgente';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-purple-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Analyse de vos lacunes en cours...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <h2 className="text-red-800 font-semibold mb-2">Erreur</h2>
          <p className="text-red-700">{error}</p>
          <button 
            onClick={loadGapAnalysis}
            className="mt-4 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
          >
            Réessayer
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto p-6">
      {/* En-tête */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-4">
          <Target className="w-8 h-8 text-red-500" />
          <h1 className="text-3xl font-bold text-gray-900">Analyse des Lacunes</h1>
        </div>
        <p className="text-gray-600 text-lg">
          Identifiez vos points faibles et obtenez un plan de remédiation personnalisé
        </p>
      </div>

      {/* Sélecteur de matière */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Matière à analyser
        </label>
        <select
          value={selectedSubject}
          onChange={(e) => setSelectedSubject(e.target.value)}
          className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
        >
          <option value="Français">Français</option>
          <option value="Mathématiques">Mathématiques</option>
          <option value="Histoire">Histoire</option>
          <option value="Géographie">Géographie</option>
          <option value="Sciences">Sciences</option>
        </select>
      </div>

      {gapAnalysis && (
        <>
          {/* Résumé global */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            {/* Score global */}
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
              <div className="flex items-center justify-between mb-2">
                <TrendingUp className="w-6 h-6 text-blue-500" />
                <span className="text-sm text-gray-500">Score Global</span>
              </div>
              <div className={`text-3xl font-bold ${getScoreColor(gapAnalysis.overall_score)}`}>
                {gapAnalysis.overall_score}%
              </div>
              <p className="text-sm text-gray-600 mt-1">
                {getScoreMessage(gapAnalysis.overall_score)}
              </p>
            </div>

            {/* Niveau de priorité */}
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
              <div className="flex items-center justify-between mb-2">
                {getPriorityIcon(gapAnalysis.priority_level)}
                <span className="text-sm text-gray-500">Priorité</span>
              </div>
              <div className={`text-lg font-semibold px-3 py-1 rounded-full text-sm ${getPriorityColor(gapAnalysis.priority_level)}`}>
                {gapAnalysis.priority_level === 'high' ? 'Élevée' : 
                 gapAnalysis.priority_level === 'medium' ? 'Moyenne' : 'Faible'}
              </div>
              <p className="text-sm text-gray-600 mt-1">
                {gapAnalysis.priority_level === 'high' ? 'Action immédiate requise' :
                 gapAnalysis.priority_level === 'medium' ? 'Amélioration recommandée' : 'Maintenance du niveau'}
              </p>
            </div>

            {/* Temps d'étude estimé */}
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
              <div className="flex items-center justify-between mb-2">
                <Clock className="w-6 h-6 text-green-500" />
                <span className="text-sm text-gray-500">Temps d'étude</span>
              </div>
              <div className="text-3xl font-bold text-green-600">
                {Math.round(gapAnalysis.estimated_study_time / 60)}h
              </div>
              <p className="text-sm text-gray-600 mt-1">
                {gapAnalysis.estimated_study_time % 60 > 0 && `${gapAnalysis.estimated_study_time % 60}min`}
              </p>
            </div>

            {/* Domaines faibles */}
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
              <div className="flex items-center justify-between mb-2">
                <AlertTriangle className="w-6 h-6 text-red-500" />
                <span className="text-sm text-gray-500">Lacunes</span>
              </div>
              <div className="text-3xl font-bold text-red-600">
                {gapAnalysis.weak_areas.length}
              </div>
              <p className="text-sm text-gray-600 mt-1">
                domaines à améliorer
              </p>
            </div>
          </div>

          {/* Graphiques professionnels interactifs */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            {/* Graphique en barres 3D des scores par domaine */}
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <BarChart3 className="w-5 h-5 text-blue-500" />
                Scores par Domaine (Graphique 3D)
              </h3>
              <div className="h-80 relative">
                {getBarChartData() && (
                  <Bar 
                    data={getBarChartData()!}
                    options={{
                      ...chartOptions,
                      scales: {
                        y: {
                          beginAtZero: true,
                          max: 100,
                          grid: {
                            color: 'rgba(156, 163, 175, 0.2)'
                          },
                          ticks: {
                            color: '#6b7280',
                            font: { size: 12 }
                          }
                        },
                        x: {
                          grid: {
                            display: false
                          },
                          ticks: {
                            color: '#6b7280',
                            font: { size: 11 },
                            maxRotation: 45
                          }
                        }
                      },
                      plugins: {
                        ...chartOptions.plugins,
                        title: {
                          display: true,
                          text: 'Performance par Compétence',
                          color: '#374151',
                          font: { size: 16, weight: 'bold' }
                        }
                      }
                    }}
                  />
                )}
              </div>
            </div>

            {/* Graphique circulaire interactif des niveaux */}
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <PieChart className="w-5 h-5 text-purple-500" />
                Répartition des Niveaux (Donut Chart)
              </h3>
              <div className="h-80 relative">
                {getDoughnutChartData() && (
                  <Doughnut 
                    data={getDoughnutChartData()!}
                    options={{
                      ...chartOptions,
                      plugins: {
                        ...chartOptions.plugins,
                        title: {
                          display: true,
                          text: 'Distribution des Compétences',
                          color: '#374151',
                          font: { size: 16, weight: 'bold' }
                        }
                      }
                    }}
                  />
                )}
              </div>
            </div>
          </div>

          {/* Graphique radar des compétences */}
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 mb-8">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <Star className="w-5 h-5 text-indigo-500" />
              Profil des Compétences (Radar Chart)
            </h3>
            <div className="h-96 relative">
              {getRadarChartData() && (
                <Radar 
                  data={getRadarChartData()!}
                  options={{
                    ...chartOptions,
                    scales: {
                      r: {
                        beginAtZero: true,
                        max: 100,
                        grid: {
                          color: 'rgba(156, 163, 175, 0.2)'
                        },
                        angleLines: {
                          color: 'rgba(156, 163, 175, 0.3)'
                        },
                        pointLabels: {
                          color: '#374151',
                          font: { size: 12, weight: 'bold' }
                        },
                        ticks: {
                          color: '#6b7280',
                          font: { size: 10 },
                          stepSize: 20
                        }
                      }
                    },
                    plugins: {
                      ...chartOptions.plugins,
                      title: {
                        display: true,
                        text: 'Comparaison Niveau Actuel vs Objectif',
                        color: '#374151',
                        font: { size: 16, weight: 'bold' }
                      }
                    }
                  }}
                />
              )}
            </div>
          </div>

          {/* Historique des performances */}
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 mb-8">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <Activity className="w-5 h-5 text-green-500" />
              Historique des Performances
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="text-center p-4 bg-blue-50 rounded-lg">
                <div className="text-2xl font-bold text-blue-600 mb-1">
                  {gapAnalysis.weak_areas.reduce((sum, area) => sum + area.total_questions, 0)}
                </div>
                <div className="text-sm text-gray-600">Questions totales</div>
              </div>
              <div className="text-center p-4 bg-green-50 rounded-lg">
                <div className="text-2xl font-bold text-green-600 mb-1">
                  {gapAnalysis.weak_areas.reduce((sum, area) => sum + (area.total_questions - area.questions_failed), 0)}
                </div>
                <div className="text-sm text-gray-600">Réponses correctes</div>
              </div>
              <div className="text-center p-4 bg-red-50 rounded-lg">
                <div className="text-2xl font-bold text-red-600 mb-1">
                  {gapAnalysis.weak_areas.reduce((sum, area) => sum + area.questions_failed, 0)}
                </div>
                <div className="text-sm text-gray-600">Erreurs commises</div>
              </div>
            </div>
          </div>

          {/* Résumé statistique des domaines */}
          {gapAnalysis.weak_areas.length > 0 && (
            <div className="mb-6">
              <div className="bg-gradient-to-r from-red-50 to-orange-50 p-4 rounded-lg border border-red-200">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <AlertTriangle className="w-5 h-5 text-red-500" />
                    <div>
                      <h3 className="font-semibold text-red-800">Résumé des Domaines Faibles</h3>
                      <p className="text-sm text-red-600">
                        {(() => {
                          const uniqueTopics = [...new Set(gapAnalysis.weak_areas.map(area => area.topic))];
                          const totalTests = gapAnalysis.weak_areas.length;
                          const avgScore = Math.round(
                            gapAnalysis.weak_areas.reduce((sum, area) => sum + area.success_rate, 0) / totalTests
                          );
                          return `${uniqueTopics.length} domaines uniques • ${totalTests} tests analysés • Score moyen: ${avgScore}%`;
                        })()}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold text-red-600">
                      {gapAnalysis.weak_areas.length}
                    </div>
                    <div className="text-sm text-red-600">tests</div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Domaines faibles optimisés et regroupés */}
          {gapAnalysis.weak_areas.length > 0 && (
            <div className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                <AlertTriangle className="w-6 h-6 text-red-500" />
                Domaines Identifiés comme Faibles (Optimisé)
              </h2>
              
              <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 max-h-96 overflow-y-auto">
                  {(() => {
                    // Regrouper les domaines par type et calculer les moyennes
                    const groupedAreas = gapAnalysis.weak_areas.reduce((acc, area) => {
                      const key = area.topic;
                      if (!acc[key]) {
                        acc[key] = {
                          topic: key,
                          areas: [],
                          avgSuccessRate: 0,
                          totalQuestions: 0,
                          totalFailed: 0,
                          avgCurrentLevel: 0,
                          maxTargetLevel: 0,
                          competency: area.competency
                        };
                      }
                      acc[key].areas.push(area);
                      return acc;
                    }, {} as any);

                    // Calculer les moyennes pour chaque groupe
                    Object.values(groupedAreas).forEach((group: any) => {
                      group.avgSuccessRate = Math.round(
                        group.areas.reduce((sum: number, a: any) => sum + a.success_rate, 0) / group.areas.length
                      );
                      group.totalQuestions = group.areas.reduce((sum: number, a: any) => sum + a.total_questions, 0);
                      group.totalFailed = group.areas.reduce((sum: number, a: any) => sum + a.questions_failed, 0);
                      group.avgCurrentLevel = Math.round(
                        group.areas.reduce((sum: number, a: any) => sum + a.current_level, 0) / group.areas.length
                      );
                      group.maxTargetLevel = Math.max(...group.areas.map((a: any) => a.target_level));
                    });

                    return Object.values(groupedAreas).map((group: any, index) => (
                      <div key={index} className="bg-gradient-to-br from-gray-50 to-white p-4 rounded-lg border border-gray-200 hover:shadow-md transition-all duration-200">
                        {/* En-tête avec score et titre */}
                        <div className="flex items-center justify-between mb-3">
                          <h3 className="text-sm font-semibold text-gray-900 truncate">{group.topic}</h3>
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                            group.avgSuccessRate >= 70 ? 'bg-green-100 text-green-800' :
                            group.avgSuccessRate >= 50 ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                            {group.avgSuccessRate}%
                      </span>
                    </div>
                    
                        {/* Métriques compactes */}
                        <div className="space-y-2 text-xs">
                          <div className="flex justify-between">
                            <span className="text-gray-500">Niveau:</span>
                            <span className="font-medium">{group.avgCurrentLevel}/10</span>
                      </div>
                          <div className="flex justify-between">
                            <span className="text-gray-500">Objectif:</span>
                            <span className="font-medium">{group.maxTargetLevel}/10</span>
                      </div>
                          <div className="flex justify-between">
                            <span className="text-gray-500">Erreurs:</span>
                            <span className="font-medium">{group.totalFailed}/{group.totalQuestions}</span>
                      </div>
                    </div>

                        {/* Barre de progression compacte */}
                        <div className="mt-3">
                          <div className="flex justify-between text-xs text-gray-400 mb-1">
                        <span>Progression</span>
                            <span>{group.avgCurrentLevel}/{group.maxTargetLevel}</span>
                      </div>
                          <div className="w-full bg-gray-200 rounded-full h-1.5">
                            <div 
                              className={`h-1.5 rounded-full transition-all duration-300 ${
                                group.avgSuccessRate >= 70 ? 'bg-green-500' :
                                group.avgSuccessRate >= 50 ? 'bg-yellow-500' :
                                'bg-red-500'
                              }`}
                              style={{ width: `${(group.avgCurrentLevel / group.maxTargetLevel) * 100}%` }}
                        ></div>
                      </div>
                    </div>

                        {/* Indicateur de répétition */}
                        {group.areas.length > 1 && (
                          <div className="mt-2 text-center">
                            <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                              {group.areas.length} tests
                            </span>
                          </div>
                        )}
                      </div>
                    ));
                  })()}
                  </div>
              </div>
            </div>
          )}

          {/* Recommandations */}
          {gapAnalysis.recommendations.length > 0 && (
            <div className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                <Brain className="w-6 h-6 text-purple-500" />
                Recommandations Personnalisées
              </h2>
              
              <div className="bg-gradient-to-r from-purple-50 to-blue-50 p-6 rounded-lg border border-purple-200">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {gapAnalysis.recommendations.map((rec, index) => (
                    <div key={index} className="flex items-start gap-3">
                      <CheckCircle className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                      <p className="text-gray-700">{rec}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Notifications de progrès */}
          <div className="bg-gradient-to-r from-green-50 to-blue-50 p-6 rounded-lg border border-green-200 mb-8">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <CheckCircle className="w-5 h-5 text-green-500" />
              Notifications de Progrès
            </h3>
            <div className="space-y-3">
              <div className="flex items-center gap-3 p-3 bg-white rounded-lg shadow-sm">
                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                <span className="text-sm text-gray-700">
                  <strong>Progrès détecté :</strong> Votre score global a augmenté de 5% ce mois
                </span>
              </div>
              <div className="flex items-center gap-3 p-3 bg-white rounded-lg shadow-sm">
                <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                <span className="text-sm text-gray-700">
                  <strong>Objectif atteint :</strong> Vous avez maîtrisé 2 domaines sur {gapAnalysis.weak_areas.length}
                </span>
              </div>
              <div className="flex items-center gap-3 p-3 bg-white rounded-lg shadow-sm">
                <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                <span className="text-sm text-gray-700">
                  <strong>Recommandation :</strong> Concentrez-vous sur la conjugaison pour progresser davantage
                </span>
              </div>
            </div>
          </div>

          {/* Actions recommandées */}
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <Zap className="w-6 h-6 text-yellow-500" />
              Actions Recommandées
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center p-4 bg-blue-50 rounded-lg hover:shadow-md transition-all duration-200">
                <BookOpen className="w-12 h-12 text-blue-500 mx-auto mb-3" />
                <h3 className="font-semibold text-gray-900 mb-2">Plan de Remédiation</h3>
                <p className="text-sm text-gray-600 mb-3">
                  Suivez un plan personnalisé pour combler vos lacunes
                </p>
                <button 
                  onClick={() => window.location.href = '/dashboard/student/remediation'}
                  className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
                >
                  Commencer
                </button>
              </div>

              <div className="text-center p-4 bg-green-50 rounded-lg hover:shadow-md transition-all duration-200">
                <Target className="w-12 h-12 text-green-500 mx-auto mb-3" />
                <h3 className="font-semibold text-gray-900 mb-2">Quiz Ciblés</h3>
                <p className="text-sm text-gray-600 mb-3">
                  Pratiquez avec des exercices adaptés à votre niveau
                </p>
                <button 
                  onClick={() => window.location.href = '/dashboard/student/learning-path'}
                  className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition-colors"
                >
                  Pratiquer
                </button>
              </div>

              <div className="text-center p-4 bg-purple-50 rounded-lg hover:shadow-md transition-all duration-200">
                <Brain className="w-12 h-12 text-purple-500 mx-auto mb-3" />
                <h3 className="font-semibold text-gray-900 mb-2">IA Avancée</h3>
                <p className="text-sm text-gray-600 mb-3">
                  Découvrez des insights intelligents de votre tuteur IA
                </p>
                <button 
                  onClick={() => window.location.href = '/dashboard/student/ai-advanced'}
                  className="px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700 transition-colors"
                >
                  Explorer
                </button>
              </div>
            </div>
          </div>
        </>
      )}

      {/* Message si pas de données */}
      {!gapAnalysis && !loading && (
        <div className="text-center py-12">
          <Target className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">Aucune donnée disponible</h3>
          <p className="text-gray-600 mb-4">
            Commencez par passer quelques quiz pour générer une analyse de vos lacunes
          </p>
          <button 
            onClick={() => window.location.href = '/dashboard/student/learning-path'}
            className="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
          >
            Commencer un Quiz
          </button>
        </div>
      )}
    </div>
  );
}
