'use client';

import React, { useState, useEffect } from 'react';
import { TrendingUp, Users, Target, Award, Clock, CheckCircle, XCircle, AlertTriangle, BarChart3, Activity, Zap } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';

interface AdvancedAnalyticsProps {
  data?: {
    engagementRate: number;
    completionRate: number;
    averageTime: number;
    topPerformers: number;
    improvementTrend: number;
    challengesCompleted: number;
    badgesEarned: number;
    learningStreak: number;
    scoreDistribution: {
      excellent: number;
      good: number;
      average: number;
      needsImprovement: number;
    };
    dailyProgress: number[];
  };
}

interface Alert {
  type: 'warning' | 'success' | 'info';
  icon: string;
  title: string;
  message: string;
  action: string;
}

interface AdvancedMetricsData {
  engagementRate: number;
  completionRate: number;
  averageTime: number;
  topPerformers: number;
  improvementTrend: number;
  challengesCompleted: number;
  badgesEarned: number;
  learningStreak: number;
  scoreDistribution: {
    excellent: number;
    good: number;
    average: number;
    needsImprovement: number;
  };
  dailyProgress: number[];
  alerts: Alert[];
}

export default function AdvancedAnalyticsWidget({ data }: AdvancedAnalyticsProps) {
  const [metricsData, setMetricsData] = useState<AdvancedMetricsData | null>(null);
  const [loading, setLoading] = useState(true);
  const { token } = useAuth();

  // Données par défaut si aucune donnée n'est fournie
  const defaultData: AdvancedMetricsData = {
    engagementRate: 87,
    completionRate: 92,
    averageTime: 45,
    topPerformers: 15,
    improvementTrend: 12,
    challengesCompleted: 28,
    badgesEarned: 16,
    learningStreak: 7,
    scoreDistribution: {
      excellent: 35,
      good: 45,
      average: 15,
      needsImprovement: 5
    },
    dailyProgress: [85, 78, 92, 88, 95, 82, 90],
    alerts: [
      {
        type: "warning",
        icon: "AlertTriangle",
        title: "5 étudiants",
        message: "ont besoin d'un soutien supplémentaire en mathématiques",
        action: "Action requise"
      },
      {
        type: "success",
        icon: "CheckCircle",
        title: "12 étudiants",
        message: "excellent en sciences - considérer des défis avancés",
        action: "Opportunité"
      },
      {
        type: "info",
        icon: "Target",
        title: "Objectif atteint",
        message: "85% de réussite globale ce mois",
        action: "Succès"
      }
    ]
  };

  useEffect(() => {
    const fetchAdvancedMetrics = async () => {
      if (!token) {
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        console.log('🚀 Chargement des métriques avancées...');
        
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/dashboard/advanced-metrics`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        if (response.ok) {
          const data = await response.json();
          console.log('✅ Métriques avancées récupérées:', data);
          setMetricsData(data);
        } else {
          console.error('❌ Erreur lors du chargement des métriques avancées:', response.status);
        }
      } catch (error) {
        console.error('❌ Erreur lors du chargement des métriques avancées:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchAdvancedMetrics();
  }, [token]);

  // Utiliser les données de l'API si disponibles, sinon les données par défaut
  const analyticsData = data || metricsData || defaultData;

  if (loading) {
    return (
      <div className="bg-gray-50 rounded-xl p-4">
        <div className="flex items-center justify-center h-80">
          <div className="text-blue-600 animate-pulse">Chargement des métriques avancées...</div>
        </div>
      </div>
    );
  }

  return (
         <div className="bg-gray-50 rounded-xl p-4">
       {/* Header du Dashboard */}
       <div className="mb-6">
         <div className="flex items-center justify-between mb-4">
           <div>
             <h3 className="text-xl font-bold text-gray-900 flex items-center">
               <BarChart3 className="w-6 h-6 text-blue-600 mr-2" />
               Métriques Avancées
             </h3>
             <p className="text-gray-600 mt-1 text-sm">Vue d'ensemble complète des performances et tendances</p>
           </div>
           <div className="flex items-center space-x-3">
             {metricsData ? (
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
             <button className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1.5 rounded-lg text-xs font-medium transition-colors">
               Actualiser
             </button>
           </div>
         </div>
       </div>

             {/* Section 1: KPIs Principaux */}
       <div className="mb-6">
         <h4 className="text-base font-semibold text-gray-900 mb-3 flex items-center">
           <Activity className="w-4 h-4 text-blue-600 mr-2" />
           Indicateurs Clés de Performance
         </h4>
                 <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Taux d'engagement */}
                     <div className="bg-white rounded-lg p-4 border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
             <div className="flex items-center justify-between mb-3">
               <div className="p-2 bg-blue-100 rounded-lg">
                 <TrendingUp className="w-5 h-5 text-blue-600" />
               </div>
               <span className="text-xs font-medium text-blue-600 bg-blue-50 px-2 py-1 rounded-full">
                 +12% vs mois dernier
               </span>
             </div>
             <div>
               <p className="text-xs font-medium text-gray-600 mb-1">Taux d'Engagement</p>
               <p className="text-2xl font-bold text-blue-900">{analyticsData.engagementRate}%</p>
               <div className="mt-2">
                 <div className="w-full bg-gray-200 rounded-full h-1.5">
                   <div 
                     className="bg-gradient-to-r from-blue-500 to-blue-600 h-1.5 rounded-full transition-all duration-300"
                     style={{ width: `${analyticsData.engagementRate}%` }}
                   ></div>
                 </div>
                 <p className="text-xs text-gray-500 mt-1">Objectif: 95%</p>
               </div>
             </div>
           </div>

          {/* Taux de completion */}
          <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 bg-green-100 rounded-lg">
                <CheckCircle className="w-6 h-6 text-green-600" />
              </div>
              <span className="text-xs font-medium text-green-600 bg-green-50 px-2 py-1 rounded-full">
                +8% vs mois dernier
              </span>
            </div>
            <div>
              <p className="text-sm font-medium text-gray-600 mb-1">Taux de Completion</p>
              <p className="text-3xl font-bold text-green-900">{analyticsData.completionRate}%</p>
              <div className="mt-3">
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-gradient-to-r from-green-500 to-green-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${analyticsData.completionRate}%` }}
                  ></div>
                </div>
                <p className="text-xs text-gray-500 mt-1">Objectif: 98%</p>
              </div>
            </div>
          </div>

          {/* Temps moyen */}
          <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 bg-purple-100 rounded-lg">
                <Clock className="w-6 h-6 text-purple-600" />
              </div>
              <span className="text-xs font-medium text-purple-600 bg-purple-50 px-2 py-1 rounded-full">
                -5% vs mois dernier
              </span>
            </div>
            <div>
              <p className="text-sm font-medium text-gray-600 mb-1">Temps Moyen</p>
              <p className="text-3xl font-bold text-purple-900">{analyticsData.averageTime} min</p>
              <p className="text-xs text-gray-500 mt-1">Par session d'apprentissage</p>
              <div className="mt-2">
                <span className="text-xs text-purple-600 font-medium">Objectif: &lt;40 min</span>
              </div>
            </div>
          </div>

          {/* Top performers */}
          <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 bg-orange-100 rounded-lg">
                <Award className="w-6 h-6 text-orange-600" />
              </div>
              <span className="text-xs font-medium text-orange-600 bg-orange-50 px-2 py-1 rounded-full">
                +3 vs mois dernier
              </span>
            </div>
            <div>
              <p className="text-sm font-medium text-gray-600 mb-1">Top Performers</p>
              <p className="text-3xl font-bold text-orange-900">{analyticsData.topPerformers}</p>
              <p className="text-xs text-gray-500 mt-1">Étudiants excellents</p>
              <div className="mt-2">
                <span className="text-xs text-orange-600 font-medium">Top 10% de la classe</span>
              </div>
            </div>
          </div>
        </div>
      </div>

             {/* Section 2: Métriques Secondaires */}
       <div className="mb-6">
         <h4 className="text-base font-semibold text-gray-900 mb-3 flex items-center">
           <Zap className="w-4 h-4 text-purple-600 mr-2" />
           Métriques Détaillées
         </h4>
                 <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {/* Tendances d'amélioration */}
                     <div className="bg-white rounded-lg p-4 border border-gray-200 shadow-sm">
             <h5 className="text-sm font-medium text-gray-900 mb-3 flex items-center">
               <TrendingUp className="w-4 h-4 text-green-600 mr-2" />
               Tendances d'Amélioration
             </h5>
                         <div className="space-y-3">
               <div className="flex items-center justify-between p-2 bg-green-50 rounded-lg">
                 <span className="text-xs text-gray-700">Progression globale</span>
                 <span className="text-sm font-bold text-green-600">+{analyticsData.improvementTrend}%</span>
               </div>
               <div className="flex items-center justify-between p-2 bg-blue-50 rounded-lg">
                 <span className="text-xs text-gray-700">Défis complétés</span>
                 <span className="text-sm font-bold text-blue-600">{analyticsData.challengesCompleted}</span>
               </div>
               <div className="flex items-center justify-between p-2 bg-purple-50 rounded-lg">
                 <span className="text-xs text-gray-700">Badges obtenus</span>
                 <span className="text-sm font-bold text-purple-600">{analyticsData.badgesEarned}</span>
               </div>
               <div className="flex items-center justify-between p-2 bg-orange-50 rounded-lg">
                 <span className="text-xs text-gray-700">Série d'apprentissage</span>
                 <span className="text-sm font-bold text-orange-600">{analyticsData.learningStreak} jours</span>
               </div>
             </div>
          </div>

          {/* Indicateurs de performance */}
                     <div className="bg-white rounded-lg p-4 border border-gray-200 shadow-sm">
             <h5 className="text-sm font-medium text-gray-900 mb-3 flex items-center">
               <Target className="w-4 h-4 text-blue-600 mr-2" />
               Distribution des Scores
             </h5>
                         <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="w-4 h-4 bg-green-500 rounded-full"></div>
                  <span className="text-sm text-gray-700">Excellent (&gt;90%)</span>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="text-lg font-bold text-gray-900">{analyticsData.scoreDistribution.excellent}%</span>
                  <div className="w-20 bg-gray-200 rounded-full h-2">
                    <div className="bg-green-500 h-2 rounded-full" style={{ width: `${analyticsData.scoreDistribution.excellent}%` }}></div>
                  </div>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="w-4 h-4 bg-blue-500 rounded-full"></div>
                  <span className="text-sm text-gray-700">Bon (70-90%)</span>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="text-lg font-bold text-gray-900">{analyticsData.scoreDistribution.good}%</span>
                  <div className="w-20 bg-gray-200 rounded-full h-2">
                    <div className="bg-blue-500 h-2 rounded-full" style={{ width: `${analyticsData.scoreDistribution.good}%` }}></div>
                  </div>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="w-4 h-4 bg-yellow-500 rounded-full"></div>
                  <span className="text-sm text-gray-700">Moyen (50-70%)</span>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="text-lg font-bold text-gray-900">{analyticsData.scoreDistribution.average}%</span>
                  <div className="w-20 bg-gray-200 rounded-full h-2">
                    <div className="bg-yellow-500 h-2 rounded-full" style={{ width: `${analyticsData.scoreDistribution.average}%` }}></div>
                  </div>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="w-4 h-4 bg-red-500 rounded-full"></div>
                  <span className="text-sm text-gray-700">À améliorer (&lt;50%)</span>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="text-lg font-bold text-gray-900">{analyticsData.scoreDistribution.needsImprovement}%</span>
                  <div className="w-20 bg-gray-200 rounded-full h-2">
                    <div className="bg-red-500 h-2 rounded-full" style={{ width: `${analyticsData.scoreDistribution.needsImprovement}%` }}></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

             {/* Section 3: Progression Temporelle */}
       <div className="mb-6">
         <h4 className="text-base font-semibold text-gray-900 mb-3 flex items-center">
           <Activity className="w-4 h-4 text-indigo-600 mr-2" />
           Progression sur 7 Jours
         </h4>
                 <div className="bg-white rounded-lg p-4 border border-gray-200 shadow-sm">
          <div className="grid grid-cols-7 gap-3">
            {analyticsData.dailyProgress.map((percentage, i) => {
              const height = Math.max(20, Math.min(100, percentage));
              return (
                <div key={i} className="text-center">
                  <div className="text-xs text-gray-500 mb-2 font-medium">J{i + 1}</div>
                  <div className="relative w-full bg-gray-100 rounded-t-lg" style={{ height: '80px' }}>
                    <div 
                      className="absolute bottom-0 w-full bg-gradient-to-t from-indigo-500 to-indigo-600 rounded-t transition-all duration-300 hover:from-indigo-600 hover:to-indigo-700"
                      style={{ 
                        height: `${height}%`,
                        opacity: 0.9
                      }}
                    ></div>
                  </div>
                  <div className="text-xs font-semibold text-indigo-600 mt-2">{percentage}%</div>
                </div>
              );
            })}
          </div>
          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">Progression quotidienne des performances</p>
            <div className="flex justify-center space-x-4 mt-2">
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 bg-indigo-500 rounded-full"></div>
                <span className="text-xs text-gray-600">Performance</span>
              </div>
            </div>
          </div>
        </div>
      </div>

             {/* Section 4: Alertes et Recommandations */}
       <div className="mb-4">
         <h4 className="text-base font-semibold text-gray-900 mb-3 flex items-center">
           <AlertTriangle className="w-4 h-4 text-amber-600 mr-2" />
           Alertes et Recommandations
         </h4>
                 <div className="bg-gradient-to-r from-amber-50 to-orange-50 rounded-lg p-4 border border-amber-200">
           <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            {analyticsData.alerts.map((alert, index) => {
              const getIcon = (iconName: string) => {
                switch (iconName) {
                  case 'AlertTriangle':
                    return <AlertTriangle className="w-5 h-5 text-amber-600 mt-0.5" />;
                  case 'CheckCircle':
                    return <CheckCircle className="w-5 h-5 text-green-600 mt-0.5" />;
                  case 'Target':
                    return <Target className="w-5 h-5 text-blue-600 mt-0.5" />;
                  case 'Users':
                    return <Users className="w-5 h-5 text-purple-600 mt-0.5" />;
                  case 'TrendingDown':
                    return <TrendingUp className="w-5 h-5 text-red-600 mt-0.5" />;
                  default:
                    return <AlertTriangle className="w-5 h-5 text-amber-600 mt-0.5" />;
                }
              };

              const getAlertColors = (type: string) => {
                switch (type) {
                  case 'warning':
                    return {
                      bg: 'bg-amber-50',
                      border: 'border-amber-200',
                      text: 'text-amber-800',
                      action: 'text-amber-600'
                    };
                  case 'success':
                    return {
                      bg: 'bg-green-50',
                      border: 'border-green-200',
                      text: 'text-green-800',
                      action: 'text-green-600'
                    };
                  case 'info':
                    return {
                      bg: 'bg-blue-50',
                      border: 'border-blue-200',
                      text: 'text-blue-800',
                      action: 'text-blue-600'
                    };
                  default:
                    return {
                      bg: 'bg-amber-50',
                      border: 'border-amber-200',
                      text: 'text-amber-800',
                      action: 'text-amber-600'
                    };
                }
              };

              const colors = getAlertColors(alert.type);

              return (
                <div key={index} className={`flex items-start space-x-3 p-3 bg-white rounded-lg border ${colors.border}`}>
                  {getIcon(alert.icon)}
                  <div>
                    <p className={`text-sm font-medium ${colors.text}`}>
                      <strong>{alert.title}</strong> {alert.message}
                    </p>
                    <p className={`text-xs ${colors.action} mt-1`}>{alert.action}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

             {/* Footer du Dashboard */}
       <div className="text-center pt-3 border-t border-gray-200">
         <p className="text-xs text-gray-500">
           Dernière mise à jour : {new Date().toLocaleString('fr-FR')} | 
           <span className="text-blue-600 font-medium ml-1">Métriques Avancées</span>
         </p>
       </div>
    </div>
  );
}
