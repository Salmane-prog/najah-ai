"use client";

import React, { useState, useEffect } from 'react';
import { BarChart3, PieChart, TrendingUp, TrendingDown, Activity } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';

interface ChartData {
  labels: string[];
  datasets: {
    label: string;
    data: number[];
    backgroundColor: string[];
    borderColor: string[];
    borderWidth: number;
  }[];
}

interface AdvancedChartsWidgetProps {
  classId: number;
}

interface MonthlyProgressData {
  performance: {
    labels: string[];
    data: number[];
  };
  progression: {
    labels: string[];
    data: number[];
  };
  engagement: {
    labels: string[];
    data: number[];
  };
}

export default function AdvancedChartsWidget({ classId }: AdvancedChartsWidgetProps) {
  const [chartType, setChartType] = useState<'performance' | 'progression' | 'engagement'>('performance');
  const [loading, setLoading] = useState(true);
  const [monthlyData, setMonthlyData] = useState<MonthlyProgressData | null>(null);
  const { token } = useAuth();

  // Données par défaut pour les graphiques
  const defaultPerformanceData: ChartData = {
    labels: ['Math', 'Français', 'Sciences', 'Histoire', 'Géo'],
    datasets: [{
      label: 'Score Moyen',
      data: [75, 68, 82, 71, 79],
      backgroundColor: ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6'],
      borderColor: ['#2563EB', '#059669', '#D97706', '#DC2626', '#7C3AED'],
      borderWidth: 2
    }]
  };

  const defaultProgressionData: ChartData = {
    labels: ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4', 'Sem 5', 'Sem 6'],
    datasets: [{
      label: 'Progression',
      data: [65, 72, 78, 85, 82, 88],
      backgroundColor: ['rgba(59, 130, 246, 0.8)'],
      borderColor: ['#3B82F6'],
      borderWidth: 3
    }]
  };

  const defaultEngagementData: ChartData = {
    labels: ['Quiz', 'Cours', 'Exercices', 'Projets', 'Évaluations'],
    datasets: [{
      label: 'Taux de Participation',
      data: [85, 92, 78, 65, 88],
      backgroundColor: ['#10B981', '#3B82F6', '#F59E0B', '#EF4444', '#8B5CF6'],
      borderColor: ['#059669', '#2563EB', '#D97706', '#DC2626', '#7C3AED'],
      borderWidth: 2
    }]
  };

  useEffect(() => {
    const fetchMonthlyProgress = async () => {
      if (!token) {
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        console.log('🚀 Chargement des données de progression mensuelle...');
        
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/dashboard/monthly-progress`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        if (response.ok) {
          const data = await response.json();
          console.log('✅ Données de progression mensuelle récupérées:', data);
          setMonthlyData(data);
        } else {
          console.error('❌ Erreur lors du chargement des données de progression:', response.status);
        }
      } catch (error) {
        console.error('❌ Erreur lors du chargement des données de progression:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchMonthlyProgress();
  }, [token]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-80">
        <div className="text-blue-600 animate-pulse">Chargement des graphiques...</div>
      </div>
    );
  }

  const getCurrentData = () => {
    // Utiliser les données de l'API si disponibles, sinon les données par défaut
    const data = monthlyData || {
      performance: { labels: defaultPerformanceData.labels, data: defaultPerformanceData.datasets[0].data },
      progression: { labels: defaultProgressionData.labels, data: defaultProgressionData.datasets[0].data },
      engagement: { labels: defaultEngagementData.labels, data: defaultEngagementData.datasets[0].data }
    };

    switch (chartType) {
      case 'performance':
        return {
          labels: data.performance.labels,
          datasets: [{
            label: 'Score Moyen',
            data: data.performance.data,
            backgroundColor: ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6'],
            borderColor: ['#2563EB', '#059669', '#D97706', '#DC2626', '#7C3AED'],
            borderWidth: 2
          }]
        };
      case 'progression':
        return {
          labels: data.progression.labels,
          datasets: [{
            label: 'Progression',
            data: data.progression.data,
            backgroundColor: ['rgba(59, 130, 246, 0.8)'],
            borderColor: ['#3B82F6'],
            borderWidth: 3
          }]
        };
      case 'engagement':
        return {
          labels: data.engagement.labels,
          datasets: [{
            label: 'Taux de Participation',
            data: data.engagement.data,
            backgroundColor: ['#10B981', '#3B82F6', '#F59E0B', '#EF4444', '#8B5CF6'],
            borderColor: ['#059669', '#2563EB', '#D97706', '#DC2626', '#7C3AED'],
            borderWidth: 2
          }]
        };
      default:
        return {
          labels: data.performance.labels,
          datasets: [{
            label: 'Score Moyen',
            data: data.performance.data,
            backgroundColor: ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6'],
            borderColor: ['#2563EB', '#059669', '#D97706', '#DC2626', '#7C3AED'],
            borderWidth: 2
          }]
        };
    }
  };

  const currentData = getCurrentData();

  return (
    <div className="space-y-6">
      {/* Sélecteur de type de graphique */}
      <div className="flex justify-between items-center">
        <div className="flex space-x-2">
          <button
            onClick={() => setChartType('performance')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              chartType === 'performance'
                ? 'bg-blue-100 text-blue-700'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            Performance
          </button>
          <button
            onClick={() => setChartType('progression')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              chartType === 'progression'
                ? 'bg-green-100 text-green-700'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            Progression
          </button>
          <button
            onClick={() => setChartType('engagement')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              chartType === 'engagement'
                ? 'bg-purple-100 text-purple-700'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            Engagement
          </button>
        </div>
        
        {/* Indicateur de source des données */}
        <div className="flex items-center space-x-2">
          {monthlyData ? (
            <div className="flex items-center space-x-1 text-green-600">
              <Activity size={16} />
              <span className="text-xs font-medium">Données réelles</span>
            </div>
          ) : (
            <div className="flex items-center space-x-1 text-orange-600">
              <BarChart3 size={16} />
              <span className="text-xs font-medium">Données simulées</span>
            </div>
          )}
        </div>
      </div>

      {/* Graphique SVG personnalisé - CORRIGÉ pour éviter le débordement */}
      <div className="relative h-80 overflow-hidden">
        <svg className="w-full h-full" viewBox="0 0 500 250" preserveAspectRatio="xMidYMid meet">
          {/* Grille de fond */}
          <defs>
            <linearGradient id="chartGradient" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#3B82F6" stopOpacity="0.8"/>
              <stop offset="100%" stopColor="#3B82F6" stopOpacity="0.1"/>
            </linearGradient>
          </defs>

          {/* Lignes de grille */}
          {Array.from({ length: 5 }, (_, i) => (
            <line
              key={i}
              x1="0"
              y1={50 + i * 35}
              x2="500"
              y2={50 + i * 35}
              stroke="#E5E7EB"
              strokeWidth="1"
            />
          ))}

          {/* Données du graphique */}
          {chartType === 'performance' && (
            <>
              {/* Barres pour les performances - CORRIGÉ pour éviter le débordement */}
              {currentData.labels.map((label, index) => {
                const value = currentData.datasets[0].data[index];
                const height = (value / 100) * 120;
                const x = (index / currentData.labels.length) * 400 + 50;
                const y = 170 - height;
                
                return (
                  <g key={index}>
                    <rect
                      x={x}
                      y={y}
                      width="50"
                      height={height}
                      fill={currentData.datasets[0].backgroundColor[index]}
                      rx="4"
                    />
                    <text
                      x={x + 25}
                      y="190"
                      textAnchor="middle"
                      className="text-xs fill-gray-600 font-medium"
                      style={{ fontSize: '10px' }}
                    >
                      {label}
                    </text>
                    <text
                      x={x + 25}
                      y={y - 5}
                      textAnchor="middle"
                      className="text-xs fill-gray-900 font-bold"
                      style={{ fontSize: '10px' }}
                    >
                      {value}%
                    </text>
                  </g>
                );
              })}
            </>
          )}

          {chartType === 'progression' && (
            <>
              {/* Ligne de progression - CORRIGÉ pour éviter le débordement */}
              <path
                d={currentData.labels.map((label, index) => {
                  const value = currentData.datasets[0].data[index];
                  const x = (index / (currentData.labels.length - 1)) * 400 + 50;
                  const y = 170 - (value / 100) * 120;
                  return `${index === 0 ? 'M' : 'L'} ${x} ${y}`;
                }).join(' ')}
                stroke="#3B82F6"
                strokeWidth="3"
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              
              {/* Points sur la ligne - CORRIGÉ pour éviter le débordement */}
              {currentData.labels.map((label, index) => {
                const value = currentData.datasets[0].data[index];
                const x = (index / (currentData.labels.length - 1)) * 400 + 50;
                const y = 170 - (value / 100) * 120;
                
                return (
                  <g key={index}>
                    <circle
                      cx={x}
                      cy={y}
                      r="4"
                      fill="#3B82F6"
                      stroke="white"
                      strokeWidth="1"
                    />
                    <text
                      x={x}
                      y="190"
                      textAnchor="middle"
                      className="text-xs fill-gray-600 font-medium"
                      style={{ fontSize: '10px' }}
                    >
                      {label}
                    </text>
                  </g>
                );
              })}
            </>
          )}

          {chartType === 'engagement' && (
            <>
              {/* Graphique en secteurs pour l'engagement - CORRIGÉ pour éviter le débordement */}
              {currentData.labels.map((label, index) => {
                const value = currentData.datasets[0].data[index];
                const total = currentData.datasets[0].data.reduce((a, b) => a + b, 0);
                const percentage = (value / total) * 100;
                
                // Calcul des coordonnées pour le secteur
                const radius = 60;
                const centerX = 250;
                const centerY = 125;
                
                return (
                  <g key={index}>
                    <circle
                      cx={centerX}
                      cy={centerY}
                      r={radius}
                      fill="none"
                      stroke={currentData.datasets[0].backgroundColor[index]}
                      strokeWidth="20"
                      strokeDasharray={`${percentage * 3.6} ${360 - percentage * 3.6}`}
                      strokeDashoffset={index * 90}
                    />
                    <text
                      x={centerX}
                      y={centerY + 100}
                      textAnchor="middle"
                      className="text-xs fill-gray-600 font-medium"
                      style={{ fontSize: '10px' }}
                    >
                      {label}: {value}%
                    </text>
                  </g>
                );
              })}
            </>
          )}
        </svg>
      </div>

      {/* Statistiques rapides - CORRIGÉ pour éviter le débordement */}
      <div className="grid grid-cols-3 gap-4 pt-4 border-t border-gray-200">
        <div className="text-center p-3 bg-blue-50 rounded-lg">
          <div className="text-xl font-bold text-blue-600">
            {Math.max(...currentData.datasets[0].data)}
          </div>
          <div className="text-xs text-gray-500 font-medium">Maximum</div>
        </div>
        <div className="text-center p-3 bg-green-50 rounded-lg">
          <div className="text-xl font-bold text-green-600">
            {Math.round(currentData.datasets[0].data.reduce((a, b) => a + b, 0) / currentData.datasets[0].data.length)}
          </div>
          <div className="text-xs text-gray-500 font-medium">Moyenne</div>
        </div>
        <div className="text-center p-3 bg-purple-50 rounded-lg">
          <div className="text-xl font-bold text-purple-600">
            {Math.min(...currentData.datasets[0].data)}
          </div>
          <div className="text-xs text-gray-500 font-medium">Minimum</div>
        </div>
      </div>
    </div>
  );
} 