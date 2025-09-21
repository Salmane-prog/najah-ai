'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { 
  TrendingUp, 
  TrendingDown, 
  Users, 
  Target, 
  Clock, 
  Brain,
  Award,
  AlertTriangle,
  Lightbulb,
  BarChart3,
  PieChart,
  LineChart,
  Activity,
  Zap
} from 'lucide-react';
import { Line, Doughnut, Bar } from 'react-chartjs-2';
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
} from 'chart.js';

// Enregistrer Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

interface StudentPerformance {
  id: number;
  name: string;
  overall_score: number;
  subject_scores: Record<string, number>;
  improvement_rate: number;
  cognitive_profile: {
    attention_span: number;
    memory_strength: number;
    problem_solving: number;
  };
  learning_style: string;
  risk_level: 'low' | 'medium' | 'high';
}

interface ClassAnalytics {
  total_students: number;
  average_score: number;
  improvement_trend: number;
  subject_performance: Record<string, number>;
  cognitive_distribution: Record<string, number>;
  learning_style_distribution: Record<string, number>;
  risk_distribution: Record<string, number>;
}

interface TimeSeriesData {
  dates: string[];
  scores: number[];
  engagement: number[];
  cognitive_load: number[];
}

const AdvancedAnalyticsDashboard: React.FC = () => {
  const [selectedStudent, setSelectedStudent] = useState<number | null>(null);
  const [timeRange, setTimeRange] = useState<'week' | 'month' | 'quarter'>('month');
  const [viewMode, setViewMode] = useState<'overview' | 'detailed' | 'comparison'>('overview');
  const [isLoading, setIsLoading] = useState(false);

  // Données simulées
  const [classAnalytics, setClassAnalytics] = useState<ClassAnalytics>({
    total_students: 25,
    average_score: 78.5,
    improvement_trend: 5.2,
    subject_performance: {
      'Mathématiques': 82.3,
      'Français': 76.8,
      'Sciences': 79.1,
      'Histoire': 75.4,
      'Géographie': 80.2
    },
    cognitive_distribution: {
      'Visuel': 35,
      'Auditif': 28,
      'Kinesthésique': 22,
      'Mixte': 15
    },
    learning_style_distribution: {
      'Analytique': 40,
      'Créatif': 25,
      'Pragmatique': 20,
      'Réflexif': 15
    },
    risk_distribution: {
      'Faible': 60,
      'Moyen': 28,
      'Élevé': 12
    }
  });

  const [students, setStudents] = useState<StudentPerformance[]>([
    {
      id: 1,
      name: "Marie Dubois",
      overall_score: 92.5,
      subject_scores: {
        'Mathématiques': 95,
        'Français': 88,
        'Sciences': 94,
        'Histoire': 90,
        'Géographie': 95
      },
      improvement_rate: 8.5,
      cognitive_profile: {
        attention_span: 85,
        memory_strength: 90,
        problem_solving: 88
      },
      learning_style: "Analytique",
      risk_level: 'low'
    },
    {
      id: 2,
      name: "Thomas Martin",
      overall_score: 68.2,
      subject_scores: {
        'Mathématiques': 72,
        'Français': 65,
        'Sciences': 70,
        'Histoire': 68,
        'Géographie': 66
      },
      improvement_rate: -2.1,
      cognitive_profile: {
        attention_span: 45,
        memory_strength: 60,
        problem_solving: 55
      },
      learning_style: "Kinesthésique",
      risk_level: 'high'
    }
  ]);

  const [timeSeriesData, setTimeSeriesData] = useState<TimeSeriesData>({
    dates: ['1er Jan', '8 Jan', '15 Jan', '22 Jan', '29 Jan', '5 Fév'],
    scores: [75, 77, 79, 78, 81, 83],
    engagement: [70, 72, 75, 73, 78, 80],
    cognitive_load: [2.8, 2.6, 2.9, 2.7, 2.5, 2.4]
  });

  useEffect(() => {
    // Charger les données analytics
    loadAnalyticsData();
  }, [timeRange]);

  const loadAnalyticsData = async () => {
    setIsLoading(true);
    try {
      // Simulation de chargement des données
      await new Promise(resolve => setTimeout(resolve, 1000));
      // Ici, vous feriez un appel API réel
    } catch (error) {
      console.error('Erreur lors du chargement des données:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const getPerformanceColor = (score: number) => {
    if (score >= 90) return 'text-green-600';
    if (score >= 80) return 'text-blue-600';
    if (score >= 70) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'low': return 'bg-green-100 text-green-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'high': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getTrendIcon = (value: number) => {
    if (value > 0) return <TrendingUp className="w-4 h-4 text-green-600" />;
    if (value < 0) return <TrendingDown className="w-4 h-4 text-red-600" />;
    return <Activity className="w-4 h-4 text-gray-600" />;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        
        {/* Header avec contrôles */}
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              Dashboard Analytics Avancé
            </h1>
            <p className="text-gray-600 mt-2">
              Analyse complète des performances et recommandations personnalisées
            </p>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="flex bg-white rounded-lg border p-1">
              <Button
                variant={timeRange === 'week' ? 'default' : 'ghost'}
                size="sm"
                onClick={() => setTimeRange('week')}
              >
                Semaine
              </Button>
              <Button
                variant={timeRange === 'month' ? 'default' : 'ghost'}
                size="sm"
                onClick={() => setTimeRange('month')}
              >
                Mois
              </Button>
              <Button
                variant={timeRange === 'quarter' ? 'default' : 'ghost'}
                size="sm"
                onClick={() => setTimeRange('quarter')}
              >
                Trimestre
              </Button>
            </div>
            
            <div className="flex bg-white rounded-lg border p-1">
              <Button
                variant={viewMode === 'overview' ? 'default' : 'ghost'}
                size="sm"
                onClick={() => setViewMode('overview')}
              >
                Vue d'ensemble
              </Button>
              <Button
                variant={viewMode === 'detailed' ? 'default' : 'ghost'}
                size="sm"
                onClick={() => setViewMode('detailed')}
              >
                Détail
              </Button>
              <Button
                variant={viewMode === 'comparison' ? 'default' : 'ghost'}
                size="sm"
                onClick={() => setViewMode('comparison')}
              >
                Comparaison
              </Button>
            </div>
          </div>
        </div>

        {/* Métriques principales */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card className="bg-white shadow-lg">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Score Moyen Classe</p>
                  <p className="text-3xl font-bold text-gray-900">{classAnalytics.average_score}%</p>
                </div>
                <div className="p-3 bg-blue-100 rounded-full">
                  <Target className="w-6 h-6 text-blue-600" />
                </div>
              </div>
              <div className="flex items-center mt-4 text-sm">
                {getTrendIcon(classAnalytics.improvement_trend)}
                <span className={`ml-2 ${classAnalytics.improvement_trend > 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {classAnalytics.improvement_trend > 0 ? '+' : ''}{classAnalytics.improvement_trend}%
                </span>
                <span className="text-gray-500 ml-2">vs période précédente</span>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white shadow-lg">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Total Étudiants</p>
                  <p className="text-3xl font-bold text-gray-900">{classAnalytics.total_students}</p>
                </div>
                <div className="p-3 bg-green-100 rounded-full">
                  <Users className="w-6 h-6 text-green-600" />
                </div>
              </div>
              <div className="mt-4">
                <div className="flex items-center justify-between text-sm mb-2">
                  <span className="text-gray-600">Actifs cette semaine</span>
                  <span className="font-medium">22/25</span>
                </div>
                <Progress value={88} className="h-2" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white shadow-lg">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Temps d'Étude Moyen</p>
                  <p className="text-3xl font-bold text-gray-900">45 min</p>
                </div>
                <div className="p-3 bg-purple-100 rounded-full">
                  <Clock className="w-6 h-6 text-purple-600" />
                </div>
              </div>
              <div className="mt-4">
                <div className="flex items-center justify-between text-sm mb-2">
                  <span className="text-gray-600">Objectif quotidien</span>
                  <span className="font-medium">60 min</span>
                </div>
                <Progress value={75} className="h-2" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white shadow-lg">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Charge Cognitive</p>
                  <p className="text-3xl font-bold text-gray-900">2.8/5</p>
                </div>
                <div className="p-3 bg-orange-100 rounded-full">
                  <Brain className="w-6 h-6 text-orange-600" />
                </div>
              </div>
              <div className="mt-4">
                <div className="flex items-center justify-between text-sm mb-2">
                  <span className="text-gray-600">Niveau optimal</span>
                  <span className="font-medium">3.0/5</span>
                </div>
                <Progress value={56} className="h-2" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Graphiques et analyses */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          
          {/* Évolution temporelle des performances */}
          <Card className="bg-white shadow-lg">
            <CardHeader>
              <CardTitle className="flex items-center">
                <LineChart className="w-5 h-5 mr-2 text-blue-600" />
                Évolution des Performances
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-64">
                <Line
                  data={{
                    labels: timeSeriesData.dates,
                    datasets: [
                      {
                        label: 'Score Moyen (%)',
                        data: timeSeriesData.scores,
                        borderColor: 'rgb(59, 130, 246)',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        tension: 0.4,
                        fill: true
                      },
                      {
                        label: 'Engagement (%)',
                        data: timeSeriesData.engagement,
                        borderColor: 'rgb(147, 51, 234)',
                        backgroundColor: 'rgba(147, 51, 234, 0.1)',
                        tension: 0.4,
                        fill: false
                      }
                    ]
                  }}
                  options={{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                      legend: { position: 'top' },
                      tooltip: { mode: 'index', intersect: false }
                    },
                    scales: {
                      y: {
                        beginAtZero: true,
                        max: 100,
                        title: { display: true, text: 'Pourcentage (%)' }
                      }
                    }
                  }}
                />
              </div>
            </CardContent>
          </Card>

          {/* Répartition des styles d'apprentissage */}
          <Card className="bg-white shadow-lg">
            <CardHeader>
              <CardTitle className="flex items-center">
                <PieChart className="w-5 h-5 mr-2 text-green-600" />
                Styles d'Apprentissage
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-64">
                <Doughnut
                  data={{
                    labels: Object.keys(classAnalytics.cognitive_distribution),
                    datasets: [{
                      data: Object.values(classAnalytics.cognitive_distribution),
                      backgroundColor: [
                        'rgba(59, 130, 246, 0.8)',
                        'rgba(147, 51, 234, 0.8)',
                        'rgba(16, 185, 129, 0.8)',
                        'rgba(245, 158, 11, 0.8)'
                      ],
                      borderColor: [
                        'rgba(59, 130, 246, 1)',
                        'rgba(147, 51, 234, 1)',
                        'rgba(16, 185, 129, 1)',
                        'rgba(245, 158, 11, 1)'
                      ],
                      borderWidth: 2
                    }]
                  }}
                  options={{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                      legend: { position: 'bottom' },
                      tooltip: {
                        callbacks: {
                          label: function(context) {
                            const total = context.dataset.data.reduce((a: number, b: number) => a + b, 0);
                            const percentage = ((context.parsed / total) * 100).toFixed(1);
                            return `${context.label}: ${context.parsed} (${percentage}%)`;
                          }
                        }
                      }
                    }
                  }}
                />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Performance par matière */}
        <Card className="bg-white shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center">
              <BarChart3 className="w-5 h-5 mr-2 text-indigo-600" />
              Performance par Matière
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-80">
              <Bar
                data={{
                  labels: Object.keys(classAnalytics.subject_performance),
                  datasets: [{
                    label: 'Score Moyen (%)',
                    data: Object.values(classAnalytics.subject_performance),
                    backgroundColor: 'rgba(99, 102, 241, 0.8)',
                    borderColor: 'rgb(99, 102, 241)',
                    borderWidth: 2,
                    borderRadius: 8
                  }]
                }}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  plugins: {
                    legend: { display: false },
                    tooltip: {
                      callbacks: {
                        label: function(context) {
                          return `Score: ${context.parsed.y}%`;
                        }
                      }
                    }
                  },
                  scales: {
                    y: {
                      beginAtZero: true,
                      max: 100,
                      title: { display: true, text: 'Score (%)' }
                    }
                  }
                }}
              />
            </div>
          </CardContent>
        </Card>

        {/* Tableau des étudiants avec comparaison */}
        <Card className="bg-white shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center">
              <Users className="w-5 h-5 mr-2 text-gray-600" />
              Comparaison des Performances Étudiants
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left py-3 px-4 font-semibold text-gray-700">Étudiant</th>
                    <th className="text-center py-3 px-4 font-semibold text-gray-700">Score Global</th>
                    <th className="text-center py-3 px-4 font-semibold text-gray-700">Progression</th>
                    <th className="text-center py-3 px-4 font-semibold text-gray-700">Style</th>
                    <th className="text-center py-3 px-4 font-semibold text-gray-700">Risque</th>
                    <th className="text-center py-3 px-4 font-semibold text-gray-700">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {students.map((student) => (
                    <tr key={student.id} className="border-b hover:bg-gray-50">
                      <td className="py-3 px-4">
                        <div>
                          <div className="font-medium text-gray-900">{student.name}</div>
                          <div className="text-sm text-gray-500">ID: {student.id}</div>
                        </div>
                      </td>
                      <td className="py-3 px-4 text-center">
                        <span className={`text-lg font-bold ${getPerformanceColor(student.overall_score)}`}>
                          {student.overall_score}%
                        </span>
                      </td>
                      <td className="py-3 px-4 text-center">
                        <div className="flex items-center justify-center">
                          {getTrendIcon(student.improvement_rate)}
                          <span className={`ml-2 font-medium ${
                            student.improvement_rate > 0 ? 'text-green-600' : 'text-red-600'
                          }`}>
                            {student.improvement_rate > 0 ? '+' : ''}{student.improvement_rate}%
                          </span>
                        </div>
                      </td>
                      <td className="py-3 px-4 text-center">
                        <Badge variant="outline">{student.learning_style}</Badge>
                      </td>
                      <td className="py-3 px-4 text-center">
                        <Badge className={getRiskColor(student.risk_level)}>
                          {student.risk_level === 'low' ? 'Faible' : 
                           student.risk_level === 'medium' ? 'Moyen' : 'Élevé'}
                        </Badge>
                      </td>
                      <td className="py-3 px-4 text-center">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => setSelectedStudent(student.id)}
                        >
                          <Lightbulb className="w-4 h-4 mr-2" />
                          Détails
                        </Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>

        {/* Recommandations et insights */}
        <Card className="bg-white shadow-lg border-l-4 border-blue-500">
          <CardHeader>
            <CardTitle className="flex items-center text-blue-600">
              <Lightbulb className="w-5 h-5 mr-2" />
              Recommandations et Insights IA
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              
              {/* Recommandations générales */}
              <div className="space-y-4">
                <h4 className="font-semibold text-gray-800">🎯 Recommandations Générales</h4>
                <div className="space-y-3">
                  <div className="flex items-start p-3 bg-blue-50 rounded-lg">
                    <Zap className="w-5 h-5 text-blue-600 mr-3 mt-0.5" />
                    <div>
                      <p className="font-medium text-blue-800">Renforcer les mathématiques</p>
                      <p className="text-sm text-blue-600">3 étudiants ont des difficultés en algèbre</p>
                    </div>
                  </div>
                  
                  <div className="flex items-start p-3 bg-green-50 rounded-lg">
                    <Award className="w-5 h-5 text-green-600 mr-3 mt-0.5" />
                    <div>
                      <p className="font-medium text-green-800">Encourager l'excellence</p>
                      <p className="text-sm text-green-600">Marie Dubois montre un potentiel exceptionnel</p>
                    </div>
                  </div>
                  
                  <div className="flex items-start p-3 bg-orange-50 rounded-lg">
                    <AlertTriangle className="w-5 h-5 text-orange-600 mr-3 mt-0.5" />
                    <div>
                      <p className="font-medium text-orange-800">Surveillance requise</p>
                      <p className="text-sm text-orange-600">Thomas Martin nécessite un suivi rapproché</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Insights cognitifs */}
              <div className="space-y-4">
                <h4 className="font-semibold text-gray-800">🧠 Insights Cognitifs</h4>
                <div className="space-y-3">
                  <div className="p-3 bg-purple-50 rounded-lg">
                    <p className="font-medium text-purple-800">Distribution des styles</p>
                    <p className="text-sm text-purple-600">
                      La classe est majoritairement analytique (40%), 
                      ce qui favorise les matières logiques
                    </p>
                  </div>
                  
                  <div className="p-3 bg-indigo-50 rounded-lg">
                    <p className="font-medium text-indigo-800">Charge cognitive optimale</p>
                    <p className="text-sm text-indigo-600">
                      La charge cognitive moyenne de 2.8/5 est 
                      dans la zone d'apprentissage optimal
                    </p>
                  </div>
                  
                  <div className="p-3 bg-teal-50 rounded-lg">
                    <p className="font-medium text-teal-800">Tendances d'engagement</p>
                    <p className="text-sm text-teal-600">
                      L'engagement augmente de 10% ce mois, 
                      indiquant une motivation croissante
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default AdvancedAnalyticsDashboard;












