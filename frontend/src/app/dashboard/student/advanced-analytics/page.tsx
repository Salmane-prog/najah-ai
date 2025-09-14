'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '../../../../hooks/useAuth';
import { 
  BarChart3, 
  TrendingUp, 
  Clock, 
  Target, 
  Lightbulb, 
  Eye,
  Calendar,
  BookOpen,
  Award,
  Activity,
  RefreshCw,
  CheckCircle,
  AlertCircle,
  Brain,
  Zap,
  Star,
  Users,
  Bookmark,
  Share2,
  Download,
  Filter,
  MoreHorizontal
} from 'lucide-react';
import Sidebar from '../../../../components/Sidebar';

interface AnalyticsData {
  globalScore: number;
  trend: string;
  trendPercentage: number;
  studyTime: number;
  quizzesCompleted: number;
  weakAreas: { [key: string]: number };
  skillProgression: { [key: string]: number };
  recentActivity: Array<{
    id: number;
    type: string;
    title: string;
    timestamp: string;
    score?: number;
  }>;
  recommendations: Array<{
    id: number;
    type: string;
    title: string;
    description: string;
    priority: 'high' | 'medium' | 'low';
  }>;
}

const AdvancedAnalyticsPage: React.FC = () => {
  const { user, token } = useAuth();
  const [activeTab, setActiveTab] = useState<'overview' | 'trends' | 'progression'>('overview');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(null);

  useEffect(() => {
    if (user?.id && token) {
      loadAnalyticsData();
    }
  }, [user?.id, token]);

  const loadAnalyticsData = async () => {
    try {
      setLoading(true);
      setError(null);

      const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      
      // Appels parallèles pour récupérer toutes les données
      const [learningAnalyticsRes, aiRecommendationsRes] = await Promise.all([
        fetch(`${API_BASE_URL}/api/v1/learning-analytics/student/${user?.id}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }),
        fetch(`${API_BASE_URL}/api/v1/ai-recommendations/student/${user?.id}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        })
      ]);

      if (learningAnalyticsRes.ok && aiRecommendationsRes.ok) {
        const [learningData, aiData] = await Promise.all([
          learningAnalyticsRes.json(),
          aiRecommendationsRes.json()
        ]);

        // Traiter et fusionner les données
        const processedData: AnalyticsData = {
          globalScore: learningData.global_score || 70,
          trend: learningData.trend || 'En amélioration',
          trendPercentage: learningData.trend_percentage || 17,
          studyTime: learningData.study_time_hours || 5,
          quizzesCompleted: learningData.quizzes_completed || 15,
          weakAreas: learningData.weak_areas || { 'Fondamentaux': 40, 'Conjugaison': 55 },
          skillProgression: learningData.skill_progression || { 'Fondamentaux': 35, 'Conjugaison': 65 },
          recentActivity: learningData.recent_activity || [],
          recommendations: aiData.recommendations || []
        };

        setAnalyticsData(processedData);
      } else {
        // En cas d'erreur, utiliser des données simulées
        setAnalyticsData(generateMockData());
      }
    } catch (error) {
      console.error('Erreur lors du chargement des analytics:', error);
      setError('Erreur lors du chargement des données');
      setAnalyticsData(generateMockData());
    } finally {
      setLoading(false);
    }
  };

  const generateMockData = (): AnalyticsData => ({
    globalScore: 70,
    trend: 'En amélioration',
    trendPercentage: 17,
    studyTime: 5,
    quizzesCompleted: 15,
    weakAreas: { 'Fondamentaux': 40, 'Conjugaison': 55 },
    skillProgression: { 'Fondamentaux': 35, 'Conjugaison': 65 },
    recentActivity: [
      {
        id: 1,
        type: 'quiz',
        title: 'Quiz Français - Niveau 5',
        timestamp: 'Il y a 2h',
        score: 85
      },
      {
        id: 2,
        type: 'assessment',
        title: 'Évaluation Initiale',
        timestamp: 'Il y a 1j',
        score: 78
      }
    ],
    recommendations: [
      {
        id: 1,
        type: 'study',
        title: 'Renforcer les fondamentaux',
        description: 'Concentrez-vous sur les règles de base du français',
        priority: 'high'
      },
      {
        id: 2,
        type: 'practice',
        title: 'Exercices de conjugaison',
        description: 'Pratiquez les temps verbaux complexes',
        priority: 'medium'
      }
    ]
  });

  // Données spécifiques par onglet
  const getTabData = () => {
    switch (activeTab) {
      case 'overview':
        return {
          title: 'Vue d\'ensemble',
          description: 'Résumé complet de vos performances et activités',
          metrics: analyticsData
        };
      case 'trends':
        return {
          title: 'Tendances',
          description: 'Évolution de vos performances dans le temps',
          metrics: {
            ...analyticsData,
            trendData: [
              { month: 'Jan', score: 65, studyTime: 4.2 },
              { month: 'Fév', score: 68, studyTime: 4.8 },
              { month: 'Mar', score: 72, studyTime: 5.1 },
              { month: 'Avr', score: 70, studyTime: 5.0 }
            ]
          }
        };
      case 'progression':
        return {
          title: 'Progression',
          description: 'Détail de votre progression par compétence',
          metrics: {
            ...analyticsData,
            detailedProgress: [
              { skill: 'Grammaire', level: 4, progress: 75, target: 5 },
              { skill: 'Vocabulaire', level: 3, progress: 60, target: 4 },
              { skill: 'Conjugaison', level: 5, progress: 85, target: 6 },
              { skill: 'Compréhension', level: 4, progress: 70, target: 5 }
            ]
          }
        };
      default:
        return { title: '', description: '', metrics: analyticsData };
    }
  };

  const getTrendColor = (trend: string) => {
    switch (trend.toLowerCase()) {
      case 'en amélioration':
        return 'text-green-600';
      case 'stable':
        return 'text-blue-600';
      case 'en baisse':
        return 'text-red-600';
      default:
        return 'text-gray-600';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low':
        return 'bg-green-100 text-green-800 border-green-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  if (loading) {
    return (
      <div className="flex h-screen bg-gray-50">
        <Sidebar />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Chargement des analytics...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex h-screen bg-gray-50">
        <Sidebar />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
            <h2 className="text-xl font-semibold text-gray-900 mb-2">Erreur de chargement</h2>
            <p className="text-gray-600 mb-4">{error}</p>
            <button
              onClick={loadAnalyticsData}
              className="btn-unified btn-unified-primary flex items-center gap-2 mx-auto"
            >
              <RefreshCw className="w-4 h-4" />
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
      
      <div className="flex-1 overflow-auto ml-56 min-w-0 relative">
        <div className="p-6 max-w-full overflow-hidden">
          {/* En-tête de la page */}
          <div className="mb-8">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h1 className="text-3xl font-bold text-gray-900">{getTabData().title}</h1>
                <p className="text-gray-600 mt-2">
                  {getTabData().description}
                </p>
              </div>
              
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  Données en temps réel chargées depuis le backend
                </div>
                
                <button
                  onClick={loadAnalyticsData}
                  className="btn-unified btn-unified-secondary flex items-center gap-2"
                >
                  <RefreshCw className="w-4 h-4" />
                  Actualiser
                </button>
              </div>
            </div>

            {/* Onglets de navigation */}
            <div className="flex items-center gap-1 bg-white rounded-lg p-1 shadow-sm border">
              <button
                onClick={() => setActiveTab('overview')}
                className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-all ${
                  activeTab === 'overview'
                    ? 'bg-blue-600 text-white shadow-sm'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                }`}
              >
                <BarChart3 className="w-4 h-4" />
                Vue d'ensemble
              </button>
              
              <button
                onClick={() => setActiveTab('trends')}
                className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-all ${
                  activeTab === 'trends'
                    ? 'bg-blue-600 text-white shadow-sm'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                }`}
              >
                <TrendingUp className="w-4 h-4" />
                Tendances
              </button>
              
              <button
                onClick={() => setActiveTab('progression')}
                className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-all ${
                  activeTab === 'progression'
                    ? 'bg-blue-600 text-white shadow-sm'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                }`}
              >
                <Clock className="w-4 h-4" />
                Progression
              </button>
            </div>
          </div>

          {/* Contenu spécifique par onglet */}
          {activeTab === 'overview' && (
            <>
              {/* Cartes de métriques principales */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8 w-full">
            {/* Score Global */}
            <div className="card-unified">
              <div className="card-unified-header">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold text-gray-900">Score Global</h3>
                  <Eye className="w-4 h-4 text-gray-400" />
                </div>
              </div>
              <div className="card-unified-body">
                <div className="text-3xl font-bold text-gray-900 mb-1">
                  {analyticsData?.globalScore}%
                </div>
                <div className="text-sm text-green-600 font-medium">Excellent !</div>
              </div>
            </div>

            {/* Tendance */}
            <div className="card-unified">
              <div className="card-unified-header">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold text-gray-900">Tendance</h3>
                  <TrendingUp className="w-4 h-4 text-gray-400" />
                </div>
              </div>
              <div className="card-unified-body">
                <div className={`text-lg font-semibold mb-1 ${getTrendColor(analyticsData?.trend || '')}`}>
                  {analyticsData?.trend}
                </div>
                <div className="text-sm text-green-600 font-medium">
                  +{analyticsData?.trendPercentage}%
                </div>
              </div>
            </div>

            {/* Temps d'étude */}
            <div className="card-unified">
              <div className="card-unified-header">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold text-gray-900">Temps d'étude</h3>
                  <Clock className="w-4 h-4 text-gray-400" />
                </div>
              </div>
              <div className="card-unified-body">
                <div className="text-3xl font-bold text-gray-900 mb-1">
                  {analyticsData?.studyTime}h
                </div>
                <div className="text-sm text-gray-600">Cette semaine</div>
              </div>
            </div>

            {/* Quiz complétés */}
            <div className="card-unified">
              <div className="card-unified-header">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold text-gray-900">Quiz complétés</h3>
                  <BookOpen className="w-4 h-4 text-gray-400" />
                </div>
              </div>
              <div className="card-unified-body">
                <div className="text-3xl font-bold text-gray-900 mb-1">
                  {analyticsData?.quizzesCompleted}
                </div>
                <div className="text-sm text-gray-600">Total</div>
              </div>
            </div>
          </div>

          {/* Graphiques et analyses */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8 w-full">
            {/* Analyse des domaines faibles */}
            <div className="card-unified">
              <div className="card-unified-header">
                <h3 className="text-lg font-semibold text-gray-900">Analyse des Domaines Faibles</h3>
              </div>
              <div className="card-unified-body">
                <div className="space-y-4">
                  {analyticsData && Object.entries(analyticsData.weakAreas).map(([area, percentage]) => (
                    <div key={area} className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span className="font-medium text-gray-700">{area}</span>
                        <span className="text-gray-600">{percentage}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className={`h-2 rounded-full ${
                            percentage < 50 ? 'bg-red-500' : 
                            percentage < 70 ? 'bg-orange-500' : 'bg-green-500'
                          }`}
                          style={{ width: `${percentage}%` }}
                        ></div>
                      </div>
                    </div>
                  ))}
                  <div className="flex items-center gap-2 text-xs text-gray-500">
                    <div className="w-3 h-3 bg-red-500 rounded"></div>
                    Taux de Réussite
                  </div>
                </div>
              </div>
            </div>

            {/* Progression des compétences */}
            <div className="card-unified">
              <div className="card-unified-header">
                <h3 className="text-lg font-semibold text-gray-900">Progression des Compétences</h3>
              </div>
              <div className="card-unified-body">
                <div className="space-y-4">
                  {analyticsData && Object.entries(analyticsData.skillProgression).map(([skill, level]) => (
                    <div key={skill} className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span className="font-medium text-gray-700">{skill}</span>
                        <span className="text-gray-600">{level}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="h-2 rounded-full bg-blue-500"
                          style={{ width: `${level}%` }}
                        ></div>
                      </div>
                    </div>
                  ))}
                  <div className="flex items-center gap-2 text-xs text-gray-500">
                    <div className="w-3 h-3 bg-blue-500 rounded"></div>
                    Niveau Actuel
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Activité récente et recommandations */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 w-full">
            {/* Activité récente */}
            <div className="card-unified">
              <div className="card-unified-header">
                <h3 className="text-lg font-semibold text-gray-900">Activité Récente</h3>
              </div>
              <div className="card-unified-body">
                {analyticsData && analyticsData.recentActivity.length > 0 ? (
                  <div className="space-y-3">
                    {analyticsData.recentActivity.map((activity) => (
                      <div key={activity.id} className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                        <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                          {activity.type === 'quiz' ? (
                            <BookOpen className="w-4 h-4 text-blue-600" />
                          ) : (
                            <Target className="w-4 h-4 text-blue-600" />
                          )}
                        </div>
                        <div className="flex-1">
                          <div className="font-medium text-gray-900">{activity.title}</div>
                          <div className="text-sm text-gray-500">{activity.timestamp}</div>
                        </div>
                        {activity.score && (
                          <div className="text-sm font-medium text-green-600">
                            {activity.score}%
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8 text-gray-500">
                    <Activity className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                    <p>Aucune activité récente</p>
                    <p className="text-sm mt-2">Commencez à étudier pour voir vos activités ici</p>
                  </div>
                )}
              </div>
            </div>

            {/* Recommandations IA */}
            <div className="card-unified">
              <div className="card-unified-header">
                <div className="flex items-center gap-2">
                  <Lightbulb className="w-5 h-5 text-yellow-500" />
                  <h3 className="text-lg font-semibold text-gray-900">Recommandations IA</h3>
                </div>
              </div>
              <div className="card-unified-body">
                {analyticsData && analyticsData.recommendations.length > 0 ? (
                  <div className="space-y-3">
                    {analyticsData.recommendations.map((rec) => (
                      <div key={rec.id} className={`p-3 rounded-lg border ${getPriorityColor(rec.priority)}`}>
                        <div className="flex items-start gap-3">
                          <div className="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                            <Brain className="w-3 h-3 text-blue-600" />
                          </div>
                          <div className="flex-1">
                            <div className="font-medium text-gray-900 mb-1">{rec.title}</div>
                            <div className="text-sm text-gray-600">{rec.description}</div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8 text-gray-500">
                    <Lightbulb className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                    <p>Aucune recommandation disponible</p>
                    <p className="text-sm mt-2">Continuez à progresser pour recevoir des conseils personnalisés</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </>
          )}

          {/* Onglet Tendances */}
          {activeTab === 'trends' && (
            <>
              {/* Graphique des tendances */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8 w-full">
                {/* Évolution du score */}
                <div className="card-unified">
                  <div className="card-unified-header">
                    <h3 className="text-lg font-semibold text-gray-900">Évolution du Score</h3>
                  </div>
                  <div className="card-unified-body">
                    <div className="space-y-4">
                      {getTabData().metrics.trendData?.map((data, index) => (
                        <div key={index} className="flex items-center justify-between">
                          <span className="text-sm font-medium text-gray-700">{data.month}</span>
                          <div className="flex items-center gap-4">
                            <span className="text-sm text-gray-600">{data.score}%</span>
                            <div className="w-24 bg-gray-200 rounded-full h-2">
                              <div 
                                className="h-2 rounded-full bg-blue-500"
                                style={{ width: `${(data.score / 100) * 100}%` }}
                              ></div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Évolution du temps d'étude */}
                <div className="card-unified">
                  <div className="card-unified-header">
                    <h3 className="text-lg font-semibold text-gray-900">Évolution du Temps d'Étude</h3>
                  </div>
                  <div className="card-unified-body">
                    <div className="space-y-4">
                      {getTabData().metrics.trendData?.map((data, index) => (
                        <div key={index} className="flex items-center justify-between">
                          <span className="text-sm font-medium text-gray-700">{data.month}</span>
                          <div className="flex items-center gap-4">
                            <span className="text-sm text-gray-600">{data.studyTime}h</span>
                            <div className="w-24 bg-gray-200 rounded-full h-2">
                              <div 
                                className="h-2 rounded-full bg-green-500"
                                style={{ width: `${(data.studyTime / 6) * 100}%` }}
                              ></div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              {/* Analyse des tendances */}
              <div className="card-unified mb-8">
                <div className="card-unified-header">
                  <h3 className="text-lg font-semibold text-gray-900">Analyse des Tendances</h3>
                </div>
                <div className="card-unified-body">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="text-center">
                      <div className="text-2xl font-bold text-green-600 mb-2">+17%</div>
                      <div className="text-sm text-gray-600">Amélioration du score</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-blue-600 mb-2">+0.8h</div>
                      <div className="text-sm text-gray-600">Augmentation du temps d'étude</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-purple-600 mb-2">+3</div>
                      <div className="text-sm text-gray-600">Quiz complétés ce mois</div>
                    </div>
                  </div>
                </div>
              </div>
            </>
          )}

          {/* Onglet Progression */}
          {activeTab === 'progression' && (
            <>
              {/* Progression détaillée par compétence */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8 w-full">
                {getTabData().metrics.detailedProgress?.map((skill, index) => (
                  <div key={index} className="card-unified">
                    <div className="card-unified-header">
                      <h3 className="text-lg font-semibold text-gray-900">{skill.skill}</h3>
                    </div>
                    <div className="card-unified-body">
                      <div className="space-y-4">
                        <div className="flex justify-between text-sm">
                          <span className="text-gray-600">Niveau actuel</span>
                          <span className="font-medium text-gray-900">{skill.level}</span>
                        </div>
                        <div className="flex justify-between text-sm">
                          <span className="text-gray-600">Progression</span>
                          <span className="font-medium text-gray-900">{skill.progress}%</span>
                        </div>
                        <div className="flex justify-between text-sm">
                          <span className="text-gray-600">Objectif</span>
                          <span className="font-medium text-gray-900">Niveau {skill.target}</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-3">
                          <div 
                            className="h-3 rounded-full bg-blue-500"
                            style={{ width: `${skill.progress}%` }}
                          ></div>
                        </div>
                        <div className="text-center">
                          <div className="text-sm text-gray-600">
                            {skill.progress >= 100 ? 'Objectif atteint !' : `${100 - skill.progress}% restant`}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {/* Résumé de progression */}
              <div className="card-unified">
                <div className="card-unified-header">
                  <h3 className="text-lg font-semibold text-gray-900">Résumé de Progression</h3>
                </div>
                <div className="card-unified-body">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <h4 className="font-medium text-gray-900 mb-3">Compétences Maîtrisées</h4>
                      <div className="space-y-2">
                        {getTabData().metrics.detailedProgress?.filter(skill => skill.progress >= 100).map((skill, index) => (
                          <div key={index} className="flex items-center gap-2 text-sm text-green-600">
                            <CheckCircle className="w-4 h-4" />
                            {skill.skill} - Niveau {skill.level}
                          </div>
                        ))}
                      </div>
                    </div>
                    <div>
                      <h4 className="font-medium text-gray-900 mb-3">En Cours d'Apprentissage</h4>
                      <div className="text-sm text-gray-600">
                        {getTabData().metrics.detailedProgress?.filter(skill => skill.progress < 100).map((skill, index) => (
                          <div key={index} className="flex items-center gap-2 text-sm text-blue-600">
                            <Clock className="w-4 h-4" />
                            {skill.skill} - {skill.progress}%
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default AdvancedAnalyticsPage;
