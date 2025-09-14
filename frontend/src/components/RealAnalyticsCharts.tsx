'use client';

import React, { useState, useEffect } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  RadialLinearScale,
} from 'chart.js';
import { Line, Bar, Doughnut, Radar, PolarArea } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  RadialLinearScale
);

interface AnalyticsData {
  classOverview: {
    totalClasses: number;
    totalStudents: number;
    activeStudents: number;
    averageScore: number;
    totalTests: number;
    completedTests: number;
  };
  weeklyProgress: Array<{
    week: string;
    averageScore: number;
    testsCompleted: number;
  }>;
  monthlyStats: Array<{
    month: string;
    testsCreated: number;
    testsCompleted: number;
  }>;
  testPerformances: Array<{
    id: number;
    title: string;
    subject: string;
    difficultyLevel: number;
    averageScore: number;
    participants: number;
    completionRate: number;
  }>;
  skills: {
    labels: string[];
    currentPerformance: number[];
    objectives: number[];
  };
  subjectDistribution: {
    labels: string[];
    data: number[];
  };
  difficultyLevels: {
    labels: string[];
    data: number[];
  };
}

export default function RealAnalyticsCharts() {
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchAnalyticsData();
  }, []);

  const fetchAnalyticsData = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('najah_token');
      
      if (!token) {
        throw new Error('Token d\'authentification manquant');
      }

      const headers = {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      };

      // Récupérer toutes les données analytics en parallèle
      const [classOverviewRes, weeklyProgressRes, monthlyStatsRes, testPerformancesRes, skillsRes, subjectDistRes, difficultyRes] = await Promise.all([
        fetch('http://localhost:8000/api/v1/analytics/class-overview', { headers }),
        fetch('http://localhost:8000/api/v1/analytics/weekly-progress', { headers }),
        fetch('http://localhost:8000/api/v1/analytics/monthly-stats', { headers }),
        fetch('http://localhost:8000/api/v1/analytics/test-performances', { headers }),
        fetch('http://localhost:8000/api/v1/analytics/skills-by-subject', { headers }),
        fetch('http://localhost:8000/api/v1/analytics/subject-distribution', { headers }),
        fetch('http://localhost:8000/api/v1/analytics/difficulty-levels', { headers })
      ]);

      if (!classOverviewRes.ok || !weeklyProgressRes.ok || !monthlyStatsRes.ok || !testPerformancesRes.ok || 
          !skillsRes.ok || !subjectDistRes.ok || !difficultyRes.ok) {
        throw new Error('Erreur lors de la récupération des données analytics');
      }

      const [classOverview, weeklyProgress, monthlyStats, testPerformances, skills, subjectDistribution, difficultyLevels] = await Promise.all([
        classOverviewRes.json(),
        weeklyProgressRes.json(),
        monthlyStatsRes.json(),
        testPerformancesRes.json(),
        skillsRes.json(),
        subjectDistRes.json(),
        difficultyRes.json()
      ]);

      setAnalyticsData({
        classOverview,
        weeklyProgress,
        monthlyStats: monthlyStats.monthly_data || [],
        weeklyProgress: weeklyProgress || [],
        testPerformances,
        skills,
        subjectDistribution,
        difficultyLevels
      });

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur inconnue');
      console.error('Erreur lors du chargement des analytics:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <span className="ml-3 text-gray-600">Chargement des analytics...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <div className="flex">
          <div className="text-red-600">
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-red-800">Erreur de chargement</h3>
            <p className="text-sm text-red-700 mt-1">{error}</p>
            <button
              onClick={fetchAnalyticsData}
              className="mt-2 text-sm text-red-600 hover:text-red-500 underline"
            >
              Réessayer
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!analyticsData) {
    return null;
  }

  // Configuration des graphiques
  const weeklyProgressChartData = {
    labels: analyticsData.weeklyProgress.map(item => item.week),
    datasets: [
      {
        label: 'Score Moyen (%)',
        data: analyticsData.weeklyProgress.map(item => item.averageScore),
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.4,
        fill: true,
      },
      {
        label: 'Tests Complétés',
        data: analyticsData.weeklyProgress.map(item => item.testsCompleted),
        borderColor: 'rgb(34, 197, 94)',
        backgroundColor: 'rgba(34, 197, 94, 0.1)',
        tension: 0.4,
        fill: false,
        yAxisID: 'y1',
      }
    ]
  };

  const monthlyStatsChartData = {
    labels: analyticsData.monthlyStats.map(item => item.month),
    datasets: [
      {
        label: 'Tests Créés',
        data: analyticsData.monthlyStats.map(item => item.testsCreated),
        backgroundColor: 'rgba(59, 130, 246, 0.8)',
        borderColor: 'rgb(59, 130, 246)',
        borderWidth: 1,
      },
      {
        label: 'Tests Complétés',
        data: analyticsData.monthlyStats.map(item => item.testsCompleted),
        backgroundColor: 'rgba(34, 197, 94, 0.8)',
        borderColor: 'rgb(34, 197, 94)',
        borderWidth: 1,
      }
    ]
  };

  const testPerformanceChartData = {
    labels: analyticsData.testPerformances.slice(0, 5).map(item => 
      item.title.length > 30 ? item.title.substring(0, 30) + '...' : item.title
    ),
    datasets: [
      {
        label: 'Score Moyen (%)',
        data: analyticsData.testPerformances.slice(0, 5).map(item => item.averageScore),
        backgroundColor: [
          'rgba(255, 99, 132, 0.8)',
          'rgba(54, 162, 235, 0.8)',
          'rgba(255, 206, 86, 0.8)',
          'rgba(75, 192, 192, 0.8)',
          'rgba(153, 102, 255, 0.8)',
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)',
        ],
        borderWidth: 2,
      }
    ]
  };

  // Nouveau graphique Radar pour les compétences (données réelles)
  const skillsRadarData = {
    labels: analyticsData.skills?.labels || ['Mathématiques', 'Français', 'Histoire', 'Sciences', 'Langues', 'Arts'],
    datasets: [
      {
        label: 'Performance Actuelle',
        data: analyticsData.skills?.currentPerformance || [0, 0, 0, 0, 0, 0],
        borderColor: 'rgb(147, 51, 234)',
        backgroundColor: 'rgba(147, 51, 234, 0.2)',
        borderWidth: 2,
      },
      {
        label: 'Objectif',
        data: analyticsData.skills?.objectives || [80, 80, 80, 80, 80, 80],
        borderColor: 'rgb(34, 197, 94)',
        backgroundColor: 'rgba(34, 197, 94, 0.2)',
        borderWidth: 2,
        borderDash: [5, 5],
      }
    ]
  };

  // Nouveau graphique Doughnut pour la répartition des matières (données réelles)
  const subjectDistributionData = {
    labels: analyticsData.subjectDistribution?.labels || ['Mathématiques', 'Français', 'Histoire', 'Sciences', 'Langues', 'Autres'],
    datasets: [
      {
        data: analyticsData.subjectDistribution?.data || [0, 0, 0, 0, 0, 0],
        backgroundColor: [
          'rgba(255, 99, 132, 0.8)',
          'rgba(54, 162, 235, 0.8)',
          'rgba(255, 206, 86, 0.8)',
          'rgba(75, 192, 192, 0.8)',
          'rgba(153, 102, 255, 0.8)',
          'rgba(201, 203, 207, 0.8)',
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)',
          'rgba(201, 203, 207, 1)',
        ],
        borderWidth: 2,
      }
    ]
  };

  // Nouveau graphique Polar Area pour les niveaux de difficulté (données réelles)
  const difficultyLevelData = {
    labels: analyticsData.difficultyLevels?.labels || ['Facile', 'Intermédiaire', 'Difficile', 'Expert'],
    datasets: [
      {
        data: analyticsData.difficultyLevels?.data || [0, 0, 0, 0],
        backgroundColor: [
          'rgba(34, 197, 94, 0.8)',
          'rgba(59, 130, 246, 0.8)',
          'rgba(245, 158, 11, 0.8)',
          'rgba(239, 68, 68, 0.8)',
        ],
        borderColor: [
          'rgba(34, 197, 94, 1)',
          'rgba(59, 130, 246, 1)',
          'rgba(245, 158, 11, 1)',
          'rgba(239, 68, 68, 1)',
        ],
        borderWidth: 2,
      }
    ]
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Analytics en Temps Réel',
      },
    },
    scales: {
      y: {
        type: 'linear' as const,
        display: true,
        position: 'left' as const,
        min: 0,
        max: 100,
      },
      y1: {
        type: 'linear' as const,
        display: true,
        position: 'right' as const,
        min: 0,
        grid: {
          drawOnChartArea: false,
        },
      },
    },
  };

  const barChartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Statistiques Mensuelles',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  const radarChartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Compétences par Matière',
      },
    },
    scales: {
      r: {
        beginAtZero: true,
        max: 100,
      },
    },
  };

  const doughnutChartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'right' as const,
      },
      title: {
        display: true,
        text: 'Répartition des Matières',
      },
    },
  };

  const polarAreaChartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Niveaux de Difficulté',
      },
    },
  };

  return (
    <div className="space-y-8">


      {/* Graphiques principaux */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Progrès hebdomadaire */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Progrès Hebdomadaire</h3>
          <Line data={weeklyProgressChartData} options={chartOptions} />
        </div>

        {/* Statistiques mensuelles */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Tests Créés vs Complétés</h3>
          <Bar data={monthlyStatsChartData} options={barChartOptions} />
        </div>
      </div>

      {/* Nouveaux graphiques avancés */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Compétences par matière (Radar) */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Compétences par Matière</h3>
          <Radar data={skillsRadarData} options={radarChartOptions} />
        </div>

        {/* Répartition des matières (Doughnut) */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Répartition des Matières</h3>
          <Doughnut data={subjectDistributionData} options={doughnutChartOptions} />
        </div>
      </div>

      {/* Niveaux de difficulté (Polar Area) */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Niveaux de Difficulté</h3>
        <div className="flex justify-center">
          <div className="w-96 h-96">
            <PolarArea data={difficultyLevelData} options={polarAreaChartOptions} />
          </div>
        </div>
      </div>

      {/* Performance des tests */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance des Tests</h3>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div>
            <Bar data={testPerformanceChartData} options={barChartOptions} />
          </div>
          <div className="space-y-4">
            <h4 className="font-medium text-gray-900">Top 5 des Tests</h4>
            {analyticsData.testPerformances.slice(0, 5).map((test, index) => (
              <div key={test.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center">
                  <span className="w-6 h-6 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-sm font-medium mr-3">
                    {index + 1}
                  </span>
                  <div>
                    <p className="font-medium text-gray-900 text-sm">{test.title}</p>
                    <p className="text-xs text-gray-500">{test.subject}</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="font-semibold text-gray-900">{test.averageScore}%</p>
                  <p className="text-xs text-gray-500">{test.participants} participants</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Bouton de rafraîchissement */}
      <div className="flex justify-center">
        <button
          onClick={fetchAnalyticsData}
          className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors"
        >
          Actualiser les Données
        </button>
      </div>
    </div>
  );
}
