'use client';

import React, { useState, useEffect } from 'react';
import { ArrowLeft, BarChart3, TrendingUp, TrendingDown, Users, Target, Clock, CheckCircle, XCircle, AlertCircle, Download, Filter } from 'lucide-react';
import Link from 'next/link';

interface Assessment {
  id: number;
  title: string;
  subject: string;
  assessment_type: string;
  due_date: string;
  status: string;
  student_count: number;
  average_score: number;
  config?: any;
}

interface AnalyticsData {
  overallStats: {
    totalStudents: number;
    activeStudents: number;
    completedStudents: number;
    averageScore: number;
    completionRate: number;
  };
  performanceMetrics: {
    excellent: number;
    good: number;
    average: number;
    belowAverage: number;
    needsImprovement: number;
  };
  progressTrends: {
    date: string;
    activeStudents: number;
    completedStudents: number;
    averageScore: number;
  }[];
  timeAnalysis: {
    averageTimeToComplete: number;
    fastestCompletion: number;
    slowestCompletion: number;
    timeDistribution: {
      range: string;
      count: number;
      percentage: number;
    }[];
  };
  criteriaAnalysis: {
    criterion: string;
    averageScore: number;
    strength: 'high' | 'medium' | 'low';
    studentCount: number;
  }[];
}

export default function AnalyticsPage({ params }: { params: { id: string } }) {
  const [assessment, setAssessment] = useState<Assessment | null>(null);
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);
  const [selectedPeriod, setSelectedPeriod] = useState<string>('all');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Récupérer l'évaluation depuis localStorage
    const allAssessments = JSON.parse(localStorage.getItem('formativeAssessments') || '[]');
    const defaultAssessments = [
      {
        id: 1,
        title: "Projet de Recherche - Écologie",
        subject: "Sciences",
        assessment_type: "project",
        due_date: "2024-02-15",
        status: "active",
        student_count: 22,
        average_score: 78.5
      },
      {
        id: 2,
        title: "Présentation Orale - Littérature",
        subject: "Français",
        assessment_type: "presentation",
        due_date: "2024-02-10",
        status: "completed",
        student_count: 25,
        average_score: 82.3
      },
      {
        id: 3,
        title: "Discussion Critique - Philosophie",
        subject: "Philosophie",
        assessment_type: "discussion",
        due_date: "2024-02-20",
        status: "active",
        student_count: 20,
        average_score: 0
      }
    ];

    const allAssessmentsCombined = [...defaultAssessments, ...allAssessments];
    const foundAssessment = allAssessmentsCombined.find(a => a.id === parseInt(params.id));
    
    if (foundAssessment) {
      setAssessment(foundAssessment);
      
      // Générer des données d'analytics simulées
      const mockAnalytics: AnalyticsData = {
        overallStats: {
          totalStudents: foundAssessment.student_count || 0,
          activeStudents: Math.floor((foundAssessment.student_count || 0) * 0.7),
          completedStudents: Math.floor((foundAssessment.student_count || 0) * 0.3),
          averageScore: foundAssessment.average_score || 75,
          completionRate: 30
        },
        performanceMetrics: {
          excellent: Math.floor((foundAssessment.student_count || 0) * 0.2),
          good: Math.floor((foundAssessment.student_count || 0) * 0.3),
          average: Math.floor((foundAssessment.student_count || 0) * 0.3),
          belowAverage: Math.floor((foundAssessment.student_count || 0) * 0.15),
          needsImprovement: Math.floor((foundAssessment.student_count || 0) * 0.05)
        },
        progressTrends: Array.from({ length: 14 }, (_, i) => ({
          date: new Date(Date.now() - (13 - i) * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
          activeStudents: Math.floor((foundAssessment.student_count || 0) * (0.5 + Math.random() * 0.4)),
          completedStudents: Math.floor((foundAssessment.student_count || 0) * (0.1 + Math.random() * 0.3)),
          averageScore: Math.floor(70 + Math.random() * 25)
        })),
        timeAnalysis: {
          averageTimeToComplete: Math.floor(120 + Math.random() * 180),
          fastestCompletion: Math.floor(45 + Math.random() * 60),
          slowestCompletion: Math.floor(300 + Math.random() * 120),
          timeDistribution: [
            { range: "0-60 min", count: Math.floor((foundAssessment.student_count || 0) * 0.2), percentage: 20 },
            { range: "60-120 min", count: Math.floor((foundAssessment.student_count || 0) * 0.4), percentage: 40 },
            { range: "120-180 min", count: Math.floor((foundAssessment.student_count || 0) * 0.25), percentage: 25 },
            { range: "180+ min", count: Math.floor((foundAssessment.student_count || 0) * 0.15), percentage: 15 }
          ]
        },
        criteriaAnalysis: [
          { criterion: "Qualité du contenu", averageScore: 82, strength: 'high', studentCount: foundAssessment.student_count || 0 },
          { criterion: "Structure et organisation", averageScore: 75, strength: 'medium', studentCount: foundAssessment.student_count || 0 },
          { criterion: "Créativité", averageScore: 68, strength: 'medium', studentCount: foundAssessment.student_count || 0 },
          { criterion: "Présentation", averageScore: 71, strength: 'medium', studentCount: foundAssessment.student_count || 0 },
          { criterion: "Réflexion critique", averageScore: 65, strength: 'low', studentCount: foundAssessment.student_count || 0 }
        ]
      };
      
      setAnalytics(mockAnalytics);
    }
    
    setIsLoading(false);
  }, [params.id]);

  const getStrengthColor = (strength: string) => {
    switch (strength) {
      case 'high': return 'text-green-600 bg-green-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      case 'low': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getStrengthLabel = (strength: string) => {
    switch (strength) {
      case 'high': return 'Fort';
      case 'medium': return 'Moyen';
      case 'low': return 'Faible';
      default: return strength;
    }
  };

  const formatTime = (minutes: number) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return hours > 0 ? `${hours}h ${mins}min` : `${mins}min`;
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement des analytics...</p>
        </div>
      </div>
    );
  }

  if (!assessment || !analytics) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <XCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Données non trouvées</h2>
          <p className="text-gray-600 mb-4">Impossible de charger les analytics pour cette évaluation.</p>
          <Link
            href="/dashboard/teacher/adaptive-evaluation"
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Retour aux évaluations
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto py-8 px-4">
        {/* Header */}
        <div className="mb-8">
          <Link
            href={`/dashboard/teacher/adaptive-evaluation/view-assessment/${assessment.id}`}
            className="inline-flex items-center text-blue-600 hover:text-blue-700 mb-4"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Retour à l'évaluation
          </Link>
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Analytics de l'Évaluation</h1>
              <p className="text-gray-600 mt-2">{assessment.title}</p>
            </div>
            <div className="flex items-center space-x-3">
              <select
                value={selectedPeriod}
                onChange={(e) => setSelectedPeriod(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="all">Toute la période</option>
                <option value="week">7 derniers jours</option>
                <option value="month">30 derniers jours</option>
                <option value="quarter">3 derniers mois</option>
              </select>
              <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center">
                <Download className="w-4 h-4 mr-2" />
                Exporter
              </button>
            </div>
          </div>
        </div>

        {/* Statistiques générales */}
        <div className="grid grid-cols-1 md:grid-cols-5 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center">
              <Users className="w-8 h-8 text-blue-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Étudiants</p>
                <p className="text-2xl font-bold text-gray-900">{analytics.overallStats.totalStudents}</p>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center">
              <Target className="w-8 h-8 text-green-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Actifs</p>
                <p className="text-2xl font-bold text-gray-900">{analytics.overallStats.activeStudents}</p>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center">
              <CheckCircle className="w-8 h-8 text-blue-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Terminés</p>
                <p className="text-2xl font-bold text-gray-900">{analytics.overallStats.completedStudents}</p>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center">
              <BarChart3 className="w-8 h-8 text-purple-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Score Moyen</p>
                <p className="text-2xl font-bold text-gray-900">{analytics.overallStats.averageScore}%</p>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center">
              <TrendingUp className="w-8 h-8 text-orange-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Taux de Réussite</p>
                <p className="text-2xl font-bold text-gray-900">{analytics.overallStats.completionRate}%</p>
              </div>
            </div>
          </div>
        </div>

        {/* Métriques de performance */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Répartition des Performances</h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <div className="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
                  <span className="text-sm text-gray-700">Excellent (90-100%)</span>
                </div>
                <span className="text-sm font-medium text-gray-900">{analytics.performanceMetrics.excellent}</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <div className="w-3 h-3 bg-blue-500 rounded-full mr-3"></div>
                  <span className="text-sm text-gray-700">Bon (80-89%)</span>
                </div>
                <span className="text-sm font-medium text-gray-900">{analytics.performanceMetrics.good}</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <div className="w-3 h-3 bg-yellow-500 rounded-full mr-3"></div>
                  <span className="text-sm text-gray-700">Moyen (70-79%)</span>
                </div>
                <span className="text-sm font-medium text-gray-900">{analytics.performanceMetrics.average}</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <div className="w-3 h-3 bg-orange-500 rounded-full mr-3"></div>
                  <span className="text-sm text-gray-700">En dessous (60-69%)</span>
                </div>
                <span className="text-sm font-medium text-gray-900">{analytics.performanceMetrics.belowAverage}</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <div className="w-3 h-3 bg-red-500 rounded-full mr-3"></div>
                  <span className="text-sm text-gray-700">À améliorer (&lt;60%)</span>
                </div>
                <span className="text-sm font-medium text-gray-900">{analytics.performanceMetrics.needsImprovement}</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Analyse Temporelle</h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-700">Temps moyen de réalisation</span>
                <span className="text-sm font-medium text-gray-900">{formatTime(analytics.timeAnalysis.averageTimeToComplete)}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-700">Réalisation la plus rapide</span>
                <span className="text-sm font-medium text-gray-900">{formatTime(analytics.timeAnalysis.fastestCompletion)}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-700">Réalisation la plus lente</span>
                <span className="text-sm font-medium text-gray-900">{formatTime(analytics.timeAnalysis.slowestCompletion)}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Analyse des critères */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Analyse par Critères d'Évaluation</h3>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Critère
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Score Moyen
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Force
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Étudiants Évalués
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {analytics.criteriaAnalysis.map((criterion, index) => (
                  <tr key={index} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">{criterion.criterion}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{criterion.averageScore}%</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStrengthColor(criterion.strength)}`}>
                        {getStrengthLabel(criterion.strength)}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{criterion.studentCount}</div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Tendances de progression */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Tendances de Progression (14 derniers jours)</h3>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Date
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Étudiants Actifs
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Étudiants Terminés
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Score Moyen
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {analytics.progressTrends.map((trend, index) => (
                  <tr key={index} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{trend.date}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{trend.activeStudents}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{trend.completedStudents}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{trend.averageScore}%</div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Distribution du temps */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Distribution du Temps de Réalisation</h3>
          <div className="space-y-4">
            {analytics.timeAnalysis.timeDistribution.map((timeRange, index) => (
              <div key={index} className="flex items-center justify-between">
                <span className="text-sm text-gray-700">{timeRange.range}</span>
                <div className="flex items-center space-x-3">
                  <div className="w-32 bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-blue-600 h-2 rounded-full"
                      style={{ width: `${timeRange.percentage}%` }}
                    ></div>
                  </div>
                  <span className="text-sm font-medium text-gray-900 w-16 text-right">
                    {timeRange.count} ({timeRange.percentage}%)
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
