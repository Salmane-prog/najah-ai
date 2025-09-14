'use client';

import React, { useState, useEffect } from 'react';
import { useAuth  } from '../../../../hooks/useAuth';
import { Card } from '../../../../components/Card';
import Button from '../../../../components/Button';
import { 
  Users, 
  TrendingUp, 
  BookOpen, 
  Target,
  Clock,
  Eye,
  Download,
  Calendar,
  Award,
  Activity,
  AlertCircle,
  CheckCircle,
  BarChart3,
  PieChart,
  LineChart,
  Brain,
  Star,
  Clock3,
  BookMarked
} from 'lucide-react';

interface ChildProgress {
  id: number;
  child_name: string;
  grade: string;
  overall_score: number;
  subjects: SubjectProgress[];
  learning_paths: LearningPathProgress[];
  recent_activities: RecentActivity[];
  recommendations: Recommendation[];
}

interface SubjectProgress {
  id: number;
  name: string;
  current_score: number;
  previous_score: number;
  improvement: number;
  topics_completed: number;
  total_topics: number;
  last_activity: string;
  status: 'excellent' | 'good' | 'needs_improvement' | 'at_risk';
}

interface LearningPathProgress {
  id: number;
  name: string;
  subject: string;
  progress_percentage: number;
  current_step: string;
  estimated_completion: string;
  difficulty_level: string;
  status: 'active' | 'completed' | 'paused';
}

interface RecentActivity {
  id: number;
  type: string;
  subject: string;
  description: string;
  score?: number;
  duration: number;
  timestamp: string;
}

interface Recommendation {
  id: number;
  type: string;
  title: string;
  description: string;
  priority: 'high' | 'medium' | 'low';
  action_required: boolean;
}

export default function ChildProgressPage() {
  const { user, token } = useAuth();
  const [activeTab, setActiveTab] = useState('overview');
  const [childProgress, setChildProgress] = useState<ChildProgress[]>([]);
  const [selectedChild, setSelectedChild] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // Mock data pour la démonstration
  useEffect(() => {
    setChildProgress([
      {
        id: 1,
        child_name: "Emma Martin",
        grade: "6ème",
        overall_score: 78.5,
        subjects: [
          {
            id: 1,
            name: "Français",
            current_score: 82.0,
            previous_score: 75.0,
            improvement: 7.0,
            topics_completed: 8,
            total_topics: 12,
            last_activity: "2024-01-20",
            status: 'good'
          },
          {
            id: 2,
            name: "Mathématiques",
            current_score: 74.5,
            previous_score: 68.0,
            improvement: 6.5,
            topics_completed: 6,
            total_topics: 10,
            last_activity: "2024-01-19",
            status: 'needs_improvement'
          },
          {
            id: 3,
            name: "Sciences",
            current_score: 89.0,
            previous_score: 85.0,
            improvement: 4.0,
            topics_completed: 10,
            total_topics: 12,
            last_activity: "2024-01-20",
            status: 'excellent'
          }
        ],
        learning_paths: [
          {
            id: 1,
            name: "Parcours Grammaire Française",
            subject: "Français",
            progress_percentage: 67,
            current_step: "Conjugaison des verbes",
            estimated_completion: "2024-02-15",
            difficulty_level: "Intermédiaire",
            status: 'active'
          },
          {
            id: 2,
            name: "Parcours Algèbre",
            subject: "Mathématiques",
            progress_percentage: 60,
            current_step: "Équations du premier degré",
            estimated_completion: "2024-02-20",
            difficulty_level: "Avancé",
            status: 'active'
          }
        ],
        recent_activities: [
          {
            id: 1,
            type: "quiz",
            subject: "Français",
            description: "Quiz de conjugaison - Imparfait",
            score: 85,
            duration: 15,
            timestamp: "2024-01-20 14:30"
          },
          {
            id: 2,
            type: "exercise",
            subject: "Mathématiques",
            description: "Exercices d'équations",
            score: 72,
            duration: 25,
            timestamp: "2024-01-20 10:15"
          },
          {
            id: 3,
            type: "reading",
            subject: "Sciences",
            description: "Lecture sur l'écosystème",
            duration: 20,
            timestamp: "2024-01-19 16:45"
          }
        ],
        recommendations: [
          {
            id: 1,
            type: "practice",
            title: "Renforcement en Mathématiques",
            description: "Emma pourrait bénéficier d'exercices supplémentaires en équations",
            priority: 'medium',
            action_required: false
          },
          {
            id: 2,
            type: "encouragement",
            title: "Excellent travail en Sciences",
            description: "Félicitez Emma pour ses excellents résultats en sciences",
            priority: 'low',
            action_required: false
          }
        ]
      }
    ]);
    
    if (childProgress.length > 0) {
      setSelectedChild(childProgress[0].id);
    }
  }, []);

  const handleExportReport = (type: string) => {
    alert(`Export ${type} à implémenter`);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'excellent': return 'text-green-600 bg-green-100';
      case 'good': return 'text-blue-600 bg-blue-100';
      case 'needs_improvement': return 'text-yellow-600 bg-yellow-100';
      case 'at_risk': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'excellent': return 'Excellent';
      case 'good': return 'Bon';
      case 'needs_improvement': return 'À améliorer';
      case 'at_risk': return 'À risque';
      default: return status;
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

  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'quiz': return <Target className="w-4 h-4 text-blue-500" />;
      case 'exercise': return <BookOpen className="w-4 h-4 text-green-500" />;
      case 'reading': return <BookMarked className="w-4 h-4 text-purple-500" />;
      case 'video': return <Activity className="w-4 h-4 text-orange-500" />;
      default: return <Activity className="w-4 h-4 text-gray-500" />;
    }
  };

  const selectedChildData = childProgress.find(child => child.id === selectedChild);

  if (!selectedChildData) {
    return (
      <div className="flex min-h-screen bg-gray-100 items-center justify-center">
        <div className="text-center">
          <Users className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">Aucun enfant sélectionné</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-gray-100">
      <main className="flex-1 p-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2 flex items-center">
            <Users className="mr-3 text-blue-600" size={32} />
            Suivi des Progrès de l'Enfant
          </h1>
          <p className="text-gray-600">
            Suivez les progrès académiques et les recommandations personnalisées pour {selectedChildData.child_name}
          </p>
        </div>

        {/* Sélection de l'enfant */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Sélectionner un enfant
          </label>
          <select
            value={selectedChild || ''}
            onChange={(e) => setSelectedChild(Number(e.target.value))}
            className="px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          >
            {childProgress.map((child) => (
              <option key={child.id} value={child.id}>
                {child.child_name} - {child.grade}
              </option>
            ))}
          </select>
        </div>

        {/* Informations générales */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="p-6 text-center">
            <div className="text-3xl font-bold text-blue-600 mb-2">
              {selectedChildData.overall_score}%
            </div>
            <div className="text-gray-600">Score Global</div>
          </Card>
          
          <Card className="p-6 text-center">
            <div className="text-3xl font-bold text-green-600 mb-2">
              {selectedChildData.subjects.length}
            </div>
            <div className="text-gray-600">Matières Suivies</div>
          </Card>
          
          <Card className="p-6 text-center">
            <div className="text-3xl font-bold text-purple-600 mb-2">
              {selectedChildData.learning_paths.filter(lp => lp.status === 'active').length}
            </div>
            <div className="text-gray-600">Parcours Actifs</div>
          </Card>
          
          <Card className="p-6 text-center">
            <div className="text-3xl font-bold text-orange-600 mb-2">
              {selectedChildData.recommendations.filter(r => r.priority === 'high').length}
            </div>
            <div className="text-gray-600">Recommandations Importantes</div>
          </Card>
        </div>

        {/* Onglets */}
        <div className="mb-6">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              <button
                onClick={() => setActiveTab('overview')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'overview'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Vue d'ensemble
              </button>
              <button
                onClick={() => setActiveTab('subjects')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'subjects'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Progrès par Matière
              </button>
              <button
                onClick={() => setActiveTab('learning_paths')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'learning_paths'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Parcours d'Apprentissage
              </button>
              <button
                onClick={() => setActiveTab('activities')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'activities'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Activités Récentes
              </button>
              <button
                onClick={() => setActiveTab('recommendations')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'recommendations'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Recommandations
              </button>
            </nav>
          </div>
        </div>

        {/* Contenu des onglets */}
        {activeTab === 'overview' && (
          <div>
            <h2 className="text-2xl font-semibold text-gray-800 mb-6">Vue d'ensemble de {selectedChildData.child_name}</h2>
            
            {/* Graphiques de progression */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
              <Card className="p-6">
                <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
                  <TrendingUp className="w-5 h-5 mr-2 text-blue-500" />
                  Progression Globale
                </h3>
                <div className="text-gray-600 text-center py-8">
                  <LineChart className="w-16 h-16 mx-auto text-gray-400 mb-4" />
                  <p>Graphique de progression à implémenter</p>
                </div>
              </Card>
              
              <Card className="p-6">
                <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
                  <PieChart className="w-5 h-5 mr-2 text-green-500" />
                  Répartition par Matière
                </h3>
                <div className="text-gray-600 text-center py-8">
                  <PieChart className="w-16 h-16 mx-auto text-gray-400 mb-4" />
                  <p>Graphique circulaire à implémenter</p>
                </div>
              </Card>
            </div>

            {/* Résumé des performances */}
            <Card className="p-6">
              <h3 className="text-xl font-semibold text-gray-800 mb-4">Résumé des Performances</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {selectedChildData.subjects.map((subject) => (
                  <div key={subject.id} className="text-center p-4 border border-gray-200 rounded-lg">
                    <h4 className="font-semibold text-gray-800 mb-2">{subject.name}</h4>
                    <div className="text-2xl font-bold text-blue-600 mb-2">{subject.current_score}%</div>
                    <div className={`text-sm px-2 py-1 rounded-full inline-block ${getStatusColor(subject.status)}`}>
                      {getStatusText(subject.status)}
                    </div>
                    <div className="text-sm text-gray-600 mt-2">
                      {subject.improvement > 0 ? '+' : ''}{subject.improvement}% vs période précédente
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          </div>
        )}

        {activeTab === 'subjects' && (
          <div>
            <h2 className="text-2xl font-semibold text-gray-800 mb-6">Progrès par Matière</h2>
            
            <div className="grid gap-6">
              {selectedChildData.subjects.map((subject) => (
                <Card key={subject.id} className="p-6">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center mb-3">
                        <h3 className="text-xl font-semibold text-gray-800 mr-3">
                          {subject.name}
                        </h3>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(subject.status)}`}>
                          {getStatusText(subject.status)}
                        </span>
                      </div>
                      
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm mb-4">
                        <div className="flex items-center">
                          <Target className="w-4 h-4 mr-2 text-blue-500" />
                          <span className="text-gray-600">Score: {subject.current_score}%</span>
                        </div>
                        <div className="flex items-center">
                          <TrendingUp className="w-4 h-4 mr-2 text-green-500" />
                          <span className="text-gray-600">Amélioration: {subject.improvement > 0 ? '+' : ''}{subject.improvement}%</span>
                        </div>
                        <div className="flex items-center">
                          <BookOpen className="w-4 h-4 mr-2 text-purple-500" />
                          <span className="text-gray-600">Progression: {subject.topics_completed}/{subject.total_topics}</span>
                        </div>
                        <div className="flex items-center">
                          <Clock className="w-4 h-4 mr-2 text-orange-500" />
                          <span className="text-gray-600">Dernière activité: {subject.last_activity}</span>
                        </div>
                      </div>
                      
                      {/* Barre de progression */}
                      <div className="mb-2">
                        <div className="flex justify-between text-sm text-gray-600 mb-1">
                          <span>Progression des sujets</span>
                          <span>{Math.round((subject.topics_completed / subject.total_topics) * 100)}%</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                            style={{ width: `${(subject.topics_completed / subject.total_topics) * 100}%` }}
                          ></div>
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex space-x-2 ml-4">
                      <Button
                        onClick={() => alert(`Voir les détails de ${subject.name}`)}
                        className="bg-blue-600 hover:bg-blue-700 text-white p-2 rounded-md"
                        title="Voir les détails"
                      >
                        <Eye className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'learning_paths' && (
          <div>
            <h2 className="text-2xl font-semibold text-gray-800 mb-6">Parcours d'Apprentissage</h2>
            
            <div className="grid gap-6">
              {selectedChildData.learning_paths.map((path) => (
                <Card key={path.id} className="p-6">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center mb-3">
                        <h3 className="text-xl font-semibold text-gray-800 mr-3">
                          {path.name}
                        </h3>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                          path.status === 'active' ? 'bg-green-100 text-green-800' :
                          path.status === 'completed' ? 'bg-blue-100 text-blue-800' :
                          'bg-yellow-100 text-yellow-800'
                        }`}>
                          {path.status === 'active' ? 'Actif' : 
                           path.status === 'completed' ? 'Terminé' : 'En pause'}
                        </span>
                      </div>
                      
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm mb-4">
                        <div className="flex items-center">
                          <BookOpen className="w-4 h-4 mr-2 text-blue-500" />
                          <span className="text-gray-600">{path.subject}</span>
                        </div>
                        <div className="flex items-center">
                          <Target className="w-4 h-4 mr-2 text-green-500" />
                          <span className="text-gray-600">Niveau: {path.difficulty_level}</span>
                        </div>
                        <div className="flex items-center">
                          <Clock className="w-4 h-4 mr-2 text-purple-500" />
                          <span className="text-gray-600">Fin estimée: {path.estimated_completion}</span>
                        </div>
                        <div className="flex items-center">
                          <Activity className="w-4 h-4 mr-2 text-orange-500" />
                          <span className="text-gray-600">Étape: {path.current_step}</span>
                        </div>
                      </div>
                      
                      {/* Barre de progression */}
                      <div className="mb-2">
                        <div className="flex justify-between text-sm text-gray-600 mb-1">
                          <span>Progression du parcours</span>
                          <span>{path.progress_percentage}%</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-green-600 h-2 rounded-full transition-all duration-300"
                            style={{ width: `${path.progress_percentage}%` }}
                          ></div>
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex space-x-2 ml-4">
                      <Button
                        onClick={() => alert(`Voir les détails de ${path.name}`)}
                        className="bg-blue-600 hover:bg-blue-700 text-white p-2 rounded-md"
                        title="Voir les détails"
                      >
                        <Eye className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'activities' && (
          <div>
            <h2 className="text-2xl font-semibold text-gray-800 mb-6">Activités Récentes</h2>
            
            <div className="grid gap-4">
              {selectedChildData.recent_activities.map((activity) => (
                <Card key={activity.id} className="p-4">
                  <div className="flex items-center">
                    <div className="flex-shrink-0 mr-4">
                      {getActivityIcon(activity.type)}
                    </div>
                    
                    <div className="flex-1">
                      <div className="flex items-center justify-between">
                        <div>
                          <h4 className="font-medium text-gray-800">{activity.description}</h4>
                          <p className="text-sm text-gray-600">{activity.subject} • {activity.timestamp}</p>
                        </div>
                        
                        <div className="flex items-center space-x-4 text-sm text-gray-600">
                          <div className="flex items-center">
                            <Clock3 className="w-4 h-4 mr-1" />
                            {activity.duration} min
                          </div>
                          {activity.score && (
                            <div className="flex items-center">
                              <Star className="w-4 h-4 mr-1 text-yellow-500" />
                              {activity.score}%
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'recommendations' && (
          <div>
            <h2 className="text-2xl font-semibold text-gray-800 mb-6">Recommandations Personnalisées</h2>
            
            <div className="grid gap-6">
              {selectedChildData.recommendations.map((recommendation) => (
                <Card key={recommendation.id} className="p-6">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center mb-2">
                        <h3 className="text-xl font-semibold text-gray-800 mr-3">
                          {recommendation.title}
                        </h3>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(recommendation.priority)}`}>
                          Priorité {recommendation.priority}
                        </span>
                        {recommendation.action_required && (
                          <span className="ml-2 px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">
                            Action requise
                          </span>
                        )}
                      </div>
                      
                      <p className="text-gray-600 mb-3">{recommendation.description}</p>
                      
                      <div className="text-sm text-gray-500">
                        Type: {recommendation.type.replace('_', ' ')}
                      </div>
                    </div>
                    
                    <div className="flex space-x-2 ml-4">
                      <Button
                        onClick={() => alert(`Voir les détails de la recommandation`)}
                        className="bg-blue-600 hover:bg-blue-700 text-white p-2 rounded-md"
                        title="Voir les détails"
                      >
                        <Eye className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        )}

        {/* Boutons d'export */}
        <div className="mt-8 flex justify-center space-x-4">
          <Button
            onClick={() => handleExportReport('pdf')}
            className="bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded-md flex items-center"
          >
            <Download className="w-4 h-4 mr-2" />
            Exporter le Rapport PDF
          </Button>
          <Button
            onClick={() => handleExportReport('excel')}
            className="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-md flex items-center"
          >
            <Download className="w-4 h-4 mr-2" />
            Exporter en Excel
          </Button>
        </div>
      </main>
    </div>
  );
}
