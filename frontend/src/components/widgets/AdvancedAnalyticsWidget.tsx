'use client';

import React, { useState, useEffect } from 'react';
import { useAuth  } from '../../hooks/useAuth';
import { 
  BarChart3, 
  TrendingUp, 
  Users, 
  Target, 
  Brain, 
  Lightbulb,
  AlertTriangle,
  CheckCircle,
  Clock,
  Activity
} from 'lucide-react';

interface AIInsight {
  type: 'prediction' | 'recommendation' | 'alert' | 'trend';
  title: string;
  description: string;
  confidence: number;
  priority: 'low' | 'medium' | 'high';
  action_required: boolean;
  created_at: string;
}

interface PerformancePrediction {
  student_id: number;
  student_name: string;
  predicted_score: number;
  confidence: number;
  risk_level: 'low' | 'medium' | 'high';
  recommendations: string[];
}

interface LearningTrend {
  period: string;
  average_score: number;
  participation_rate: number;
  engagement_level: number;
  trend_direction: 'up' | 'down' | 'stable';
}

export default function AdvancedAnalyticsWidget() {
  const { user, token } = useAuth();
  const [aiInsights, setAiInsights] = useState<AIInsight[]>([]);
  const [predictions, setPredictions] = useState<PerformancePrediction[]>([]);
  const [trends, setTrends] = useState<LearningTrend[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'insights' | 'predictions' | 'trends'>('insights');

  useEffect(() => {
    if (token) {
      fetchAdvancedAnalytics();
    }
  }, [token]);

  const fetchAdvancedAnalytics = async () => {
    try {
      setLoading(true);
      
      // Récupérer les insights IA
      const insightsResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/advanced_analytics/insights`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (insightsResponse.ok) {
        const insightsData = await insightsResponse.json();
        setAiInsights(insightsData.insights || []);
      }
      
      // Récupérer les prédictions de performance
      const predictionsResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/advanced_analytics/predictions`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (predictionsResponse.ok) {
        const predictionsData = await predictionsResponse.json();
        setPredictions(predictionsData.predictions || []);
      }
      
      // Récupérer les tendances d'apprentissage
      const trendsResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/advanced_analytics/trends`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (trendsResponse.ok) {
        const trendsData = await trendsResponse.json();
        setTrends(trendsData.trends || []);
      }
      
    } catch (err) {
      console.error('Erreur lors du chargement des analytics avancées:', err);
    } finally {
      setLoading(false);
    }
  };

  const getInsightIcon = (type: string) => {
    switch (type) {
      case 'prediction': return <Brain size={16} className="text-blue-600" />;
      case 'recommendation': return <Lightbulb size={16} className="text-yellow-600" />;
      case 'alert': return <AlertTriangle size={16} className="text-red-600" />;
      case 'trend': return <TrendingUp size={16} className="text-green-600" />;
      default: return <Activity size={16} className="text-gray-600" />;
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'border-red-500 bg-red-50';
      case 'medium': return 'border-yellow-500 bg-yellow-50';
      case 'low': return 'border-green-500 bg-green-50';
      default: return 'border-gray-300 bg-gray-50';
    }
  };

  const getRiskLevelColor = (risk: string) => {
    switch (risk) {
      case 'high': return 'text-red-600 bg-red-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      case 'low': return 'text-green-600 bg-green-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getTrendIcon = (direction: string) => {
    switch (direction) {
      case 'up': return <TrendingUp size={14} className="text-green-600" />;
      case 'down': return <TrendingUp size={14} className="text-red-600 transform rotate-180" />;
      case 'stable': return <Activity size={14} className="text-gray-600" />;
      default: return <Activity size={14} className="text-gray-600" />;
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-6">
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
          <Brain className="text-blue-600" size={24} />
          <h2 className="text-xl font-bold text-gray-800">Analytics Avancées IA</h2>
        </div>
        <button
          onClick={fetchAdvancedAnalytics}
          className="px-3 py-1 text-sm bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition"
        >
          Actualiser
        </button>
      </div>

      {/* Navigation par onglets */}
      <div className="flex space-x-1 bg-gray-100 rounded-lg p-1 mb-6">
        {[
          { id: 'insights', label: 'Insights IA', icon: <Brain size={16} /> },
          { id: 'predictions', label: 'Prédictions', icon: <Target size={16} /> },
          { id: 'trends', label: 'Tendances', icon: <TrendingUp size={16} /> }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`flex items-center gap-2 px-4 py-2 rounded-md font-medium transition ${
              activeTab === tab.id
                ? 'bg-white text-blue-700 shadow-sm'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            {tab.icon}
            {tab.label}
          </button>
        ))}
      </div>

      {/* Contenu des onglets */}
      {activeTab === 'insights' && (
        <div className="space-y-4">
          {aiInsights.length > 0 ? (
            aiInsights.map((insight, index) => (
              <div
                key={index}
                className={`p-4 rounded-lg border-l-4 ${getPriorityColor(insight.priority)}`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-start gap-3 flex-1">
                    {getInsightIcon(insight.type)}
                    <div className="flex-1">
                      <h3 className="font-semibold text-gray-800 mb-1">{insight.title}</h3>
                      <p className="text-sm text-gray-600 mb-2">{insight.description}</p>
                      <div className="flex items-center gap-4 text-xs text-gray-500">
                        <span>Confiance: {insight.confidence}%</span>
                        <span>Priorité: {insight.priority}</span>
                        {insight.action_required && (
                          <span className="text-red-600 font-medium">Action requise</span>
                        )}
                      </div>
                    </div>
                  </div>
                  {insight.action_required && (
                    <button className="px-3 py-1 text-xs bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                      Agir
                    </button>
                  )}
                </div>
              </div>
            ))
          ) : (
            <div className="text-center py-8">
              <Brain className="mx-auto text-gray-400 mb-2" size={32} />
              <p className="text-gray-600">Aucun insight IA disponible</p>
              <p className="text-sm text-gray-500">Les insights apparaîtront ici</p>
            </div>
          )}
        </div>
      )}

      {activeTab === 'predictions' && (
        <div className="space-y-4">
          {predictions.length > 0 ? (
            predictions.map((prediction, index) => (
              <div key={index} className="border rounded-lg p-4 hover:shadow-md transition">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="font-semibold text-gray-800">{prediction.student_name}</h3>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getRiskLevelColor(prediction.risk_level)}`}>
                    {prediction.risk_level.toUpperCase()}
                  </span>
                </div>
                
                <div className="grid grid-cols-2 gap-4 mb-3">
                  <div>
                    <p className="text-sm text-gray-600">Score prédit</p>
                    <p className="text-lg font-bold text-gray-800">{prediction.predicted_score}%</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Confiance</p>
                    <p className="text-lg font-bold text-gray-800">{prediction.confidence}%</p>
                  </div>
                </div>
                
                <div>
                  <p className="text-sm text-gray-600 mb-2">Recommandations:</p>
                  <ul className="space-y-1">
                    {prediction.recommendations.slice(0, 2).map((rec, recIndex) => (
                      <li key={recIndex} className="text-xs text-gray-700 flex items-center gap-1">
                        <CheckCircle size={12} className="text-green-600" />
                        {rec}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ))
          ) : (
            <div className="text-center py-8">
              <Target className="mx-auto text-gray-400 mb-2" size={32} />
              <p className="text-gray-600">Aucune prédiction disponible</p>
              <p className="text-sm text-gray-500">Les prédictions apparaîtront ici</p>
            </div>
          )}
        </div>
      )}

      {activeTab === 'trends' && (
        <div className="space-y-4">
          {trends.length > 0 ? (
            trends.map((trend, index) => (
              <div key={index} className="border rounded-lg p-4 hover:shadow-md transition">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="font-semibold text-gray-800">{trend.period}</h3>
                  {getTrendIcon(trend.trend_direction)}
                </div>
                
                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <p className="text-sm text-gray-600">Score moyen</p>
                    <p className="text-lg font-bold text-gray-800">{trend.average_score}%</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Taux participation</p>
                    <p className="text-lg font-bold text-gray-800">{trend.participation_rate}%</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Engagement</p>
                    <p className="text-lg font-bold text-gray-800">{trend.engagement_level}/10</p>
                  </div>
                </div>
                
                <div className="mt-3 pt-3 border-t">
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-gray-500">Tendance:</span>
                    <span className={`text-xs font-medium ${
                      trend.trend_direction === 'up' ? 'text-green-600' :
                      trend.trend_direction === 'down' ? 'text-red-600' : 'text-gray-600'
                    }`}>
                      {trend.trend_direction === 'up' ? 'Amélioration' :
                       trend.trend_direction === 'down' ? 'Baisse' : 'Stable'}
                    </span>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="text-center py-8">
              <TrendingUp className="mx-auto text-gray-400 mb-2" size={32} />
              <p className="text-gray-600">Aucune tendance disponible</p>
              <p className="text-sm text-gray-500">Les tendances apparaîtront ici</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
} 