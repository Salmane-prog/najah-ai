'use client';

import React, { useState, useEffect } from 'react';
import { useAuth  } from '../../../../hooks/useAuth';
import { Card } from '../../../../components/Card';
import Button from '../../../../components/Button';
import { 
  Database, 
  BarChart3, 
  TrendingUp, 
  Users, 
  Activity,
  Clock,
  Eye,
  Download,
  Filter,
  RefreshCw,
  PieChart,
  LineChart,
  Target,
  AlertCircle,
  CheckCircle,
  Zap,
  Brain,
  Settings,
  Play,
  Pause,
  Plus,
  BookOpen,
  Calendar
} from 'lucide-react';

interface DataCollection {
  id: number;
  collection_name: string;
  data_type: string;
  source: string;
  status: string;
  records_count: number;
  last_collection: string;
  next_collection: string;
  collection_frequency: string;
  data_quality_score: number;
}

interface LearningPattern {
  id: number;
  student_id: number;
  student_name: string;
  pattern_type: string;
  subject: string;
  time_of_day: string;
  session_duration: number;
  preferred_content_type: string;
  learning_style: string;
  confidence_level: number;
  detected_at: string;
}

interface BlockageDetection {
  id: number;
  student_id: number;
  student_name: string;
  subject: string;
  topic: string;
  blockage_type: string;
  severity_level: number;
  evidence: string[];
  confidence: number;
  detected_at: string;
  status: string;
}

interface ContinuousImprovement {
  id: number;
  improvement_type: string;
  description: string;
  impact_level: string;
  implementation_status: string;
  created_at: string;
  estimated_completion: string;
  success_metrics: string[];
}

export default function DataCollectionPage() {
  const { user, token } = useAuth();
  const [activeTab, setActiveTab] = useState('collection');
  const [dataCollections, setDataCollections] = useState<DataCollection[]>([]);
  const [learningPatterns, setLearningPatterns] = useState<LearningPattern[]>([]);
  const [blockages, setBlockages] = useState<BlockageDetection[]>([]);
  const [improvements, setImprovements] = useState<ContinuousImprovement[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [dateRange, setDateRange] = useState('week');

  // Mock data pour la démonstration
  useEffect(() => {
    setDataCollections([
      {
        id: 1,
        collection_name: "Interactions Utilisateur",
        data_type: "behavioral",
        source: "frontend_events",
        status: "active",
        records_count: 15420,
        last_collection: "2024-01-20 15:30:00",
        next_collection: "2024-01-20 16:00:00",
        collection_frequency: "30min",
        data_quality_score: 94.2
      },
      {
        id: 2,
        collection_name: "Performances d'Apprentissage",
        data_type: "academic",
        source: "quiz_results",
        status: "active",
        records_count: 3247,
        last_collection: "2024-01-20 14:45:00",
        next_collection: "2024-01-20 15:15:00",
        collection_frequency: "30min",
        data_quality_score: 98.7
      },
      {
        id: 3,
        collection_name: "Temps de Session",
        data_type: "engagement",
        source: "session_tracking",
        status: "paused",
        records_count: 8921,
        last_collection: "2024-01-20 12:00:00",
        next_collection: "2024-01-20 13:00:00",
        collection_frequency: "1h",
        data_quality_score: 91.5
      }
    ]);

    setLearningPatterns([
      {
        id: 1,
        student_id: 1,
        student_name: "Marie Dubois",
        pattern_type: "optimal_learning_time",
        subject: "Mathématiques",
        time_of_day: "09:00-11:00",
        session_duration: 120,
        preferred_content_type: "interactive_exercises",
        learning_style: "visual",
        confidence_level: 0.89,
        detected_at: "2024-01-20"
      },
      {
        id: 2,
        student_id: 2,
        student_name: "Ahmed Benali",
        pattern_type: "content_preference",
        subject: "Sciences",
        time_of_day: "14:00-16:00",
        session_duration: 90,
        preferred_content_type: "video_lessons",
        learning_style: "auditory",
        confidence_level: 0.92,
        detected_at: "2024-01-20"
      },
      {
        id: 3,
        student_id: 3,
        student_name: "Emma Martin",
        pattern_type: "learning_style_adaptation",
        subject: "Français",
        time_of_day: "16:00-18:00",
        session_duration: 75,
        preferred_content_type: "reading_materials",
        learning_style: "kinesthetic",
        confidence_level: 0.78,
        detected_at: "2024-01-20"
      }
    ]);

    setBlockages([
      {
        id: 1,
        student_id: 1,
        student_name: "Marie Dubois",
        subject: "Mathématiques",
        topic: "Équations du second degré",
        blockage_type: "conceptual_understanding",
        severity_level: 4,
        evidence: ["Temps de réponse élevé", "Erreurs répétées", "Abandon de session"],
        confidence: 0.87,
        detected_at: "2024-01-20",
        status: "active"
      },
      {
        id: 2,
        student_id: 3,
        student_name: "Emma Martin",
        subject: "Français",
        topic: "Conjugaison des verbes",
        blockage_type: "procedural_skill",
        severity_level: 3,
        evidence: ["Hésitations fréquentes", "Corrections multiples"],
        confidence: 0.76,
        detected_at: "2024-01-20",
        status: "resolved"
      }
    ]);

    setImprovements([
      {
        id: 1,
        improvement_type: "Algorithme de Recommandation",
        description: "Optimisation de l'algorithme de recommandation basé sur les patterns d'apprentissage",
        impact_level: "high",
        implementation_status: "in_progress",
        created_at: "2024-01-15",
        estimated_completion: "2024-02-15",
        success_metrics: ["Précision des recommandations", "Taux d'engagement", "Satisfaction utilisateur"]
      },
      {
        id: 2,
        improvement_type: "Détection de Blocages",
        description: "Amélioration de la détection précoce des points de blocage d'apprentissage",
        impact_level: "medium",
        implementation_status: "planned",
        created_at: "2024-01-18",
        estimated_completion: "2024-03-01",
        success_metrics: ["Temps de détection", "Précision de détection", "Taux de résolution"]
      }
    ]);
  }, []);

  const handleStartCollection = (collectionId: number) => {
    alert(`Démarrage de la collecte ${collectionId}`);
  };

  const handlePauseCollection = (collectionId: number) => {
    alert(`Pause de la collecte ${collectionId}`);
  };

  const handleExportData = (type: string) => {
    alert(`Export ${type} à implémenter`);
  };

  const handleRefreshData = () => {
    setIsLoading(true);
    setTimeout(() => setIsLoading(false), 1000);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-green-600 bg-green-100';
      case 'paused': return 'text-yellow-600 bg-yellow-100';
      case 'stopped': return 'text-red-600 bg-red-100';
      case 'resolved': return 'text-blue-600 bg-blue-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getImpactLevelColor = (level: string) => {
    switch (level) {
      case 'high': return 'text-red-600 bg-red-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      case 'low': return 'text-green-600 bg-green-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getImplementationStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'text-green-600 bg-green-100';
      case 'in_progress': return 'text-blue-600 bg-blue-100';
      case 'planned': return 'text-purple-600 bg-purple-100';
      case 'on_hold': return 'text-yellow-600 bg-yellow-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getDataQualityColor = (score: number) => {
    if (score >= 90) return 'text-green-600';
    if (score >= 80) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="flex min-h-screen bg-gray-100">
      <main className="flex-1 p-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2 flex items-center">
            <Database className="mr-3 text-blue-600" size={32} />
            Collecte et Analyse de Données
          </h1>
          <p className="text-gray-600">
            Supervisez la collecte de données, analysez les patterns d'apprentissage et améliorez continuellement le système
          </p>
        </div>

        {/* Contrôles */}
        <div className="flex justify-between items-center mb-6">
          <div className="flex space-x-4">
            <select
              value={dateRange}
              onChange={(e) => setDateRange(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="week">Cette semaine</option>
              <option value="month">Ce mois</option>
              <option value="quarter">Ce trimestre</option>
              <option value="year">Cette année</option>
            </select>
            
            <Button
              onClick={handleRefreshData}
              disabled={isLoading}
              className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-md flex items-center"
            >
              <RefreshCw className={`w-4 h-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
              Actualiser
            </Button>
          </div>

          <div className="flex space-x-2">
            <Button
              onClick={() => handleExportData('csv')}
              className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md flex items-center"
            >
              <Download className="w-4 h-4 mr-2" />
              Export CSV
            </Button>
            <Button
              onClick={() => handleExportData('json')}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md flex items-center"
            >
              <Download className="w-4 h-4 mr-2" />
              Export JSON
            </Button>
          </div>
        </div>

        {/* Onglets */}
        <div className="mb-6">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              <button
                onClick={() => setActiveTab('collection')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'collection'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Collecte de Données
              </button>
              <button
                onClick={() => setActiveTab('patterns')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'patterns'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Patterns d'Apprentissage
              </button>
              <button
                onClick={() => setActiveTab('blockages')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'blockages'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Détection de Blocages
              </button>
              <button
                onClick={() => setActiveTab('improvements')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'improvements'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Amélioration Continue
              </button>
            </nav>
          </div>
        </div>

        {/* Contenu des onglets */}
        {activeTab === 'collection' && (
          <div>
            <h2 className="text-2xl font-semibold text-gray-800 mb-6">Collecte de Données</h2>
            
            {/* Métriques de collecte */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
              <Card className="p-6 text-center">
                <div className="text-3xl font-bold text-blue-600 mb-2">
                  {dataCollections.length}
                </div>
                <div className="text-gray-600">Sources de Données</div>
              </Card>
              
              <Card className="p-6 text-center">
                <div className="text-3xl font-bold text-green-600 mb-2">
                  {dataCollections.filter(c => c.status === 'active').length}
                </div>
                <div className="text-gray-600">Collectes Actives</div>
              </Card>
              
              <Card className="p-6 text-center">
                <div className="text-3xl font-bold text-purple-600 mb-2">
                  {dataCollections.reduce((sum, c) => sum + c.records_count, 0).toLocaleString()}
                </div>
                <div className="text-gray-600">Enregistrements Totaux</div>
              </Card>
              
              <Card className="p-6 text-center">
                <div className="text-3xl font-bold text-orange-600 mb-2">
                  {Math.round(dataCollections.reduce((sum, c) => sum + c.data_quality_score, 0) / dataCollections.length)}%
                </div>
                <div className="text-gray-600">Qualité Moyenne</div>
              </Card>
            </div>

            {/* Sources de données */}
            <div className="grid gap-6">
              {dataCollections.map((collection) => (
                <Card key={collection.id} className="p-6">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center mb-2">
                        <h3 className="text-xl font-semibold text-gray-800 mr-3">
                          {collection.collection_name}
                        </h3>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(collection.status)}`}>
                          {collection.status === 'active' ? 'Actif' : 
                           collection.status === 'paused' ? 'En pause' : 'Arrêté'}
                        </span>
                      </div>
                      
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm mb-4">
                        <div className="flex items-center">
                          <Database className="w-4 h-4 mr-2 text-blue-500" />
                          <span className="text-gray-600">{collection.data_type}</span>
                        </div>
                        <div className="flex items-center">
                          <Activity className="w-4 h-4 mr-2 text-green-500" />
                          <span className="text-gray-600">{collection.source}</span>
                        </div>
                        <div className="flex items-center">
                          <Clock className="w-4 h-4 mr-2 text-purple-500" />
                          <span className="text-gray-600">{collection.collection_frequency}</span>
                        </div>
                        <div className="flex items-center">
                          <Target className="w-4 h-4 mr-2 text-orange-500" />
                          <span className={`font-medium ${getDataQualityColor(collection.data_quality_score)}`}>
                            {collection.data_quality_score}%
                          </span>
                        </div>
                      </div>
                      
                      <div className="text-sm text-gray-600">
                        <p>Dernière collecte: {collection.last_collection}</p>
                        <p>Prochaine collecte: {collection.next_collection}</p>
                        <p>Enregistrements: {collection.records_count.toLocaleString()}</p>
                      </div>
                    </div>
                    
                    <div className="flex space-x-2 ml-4">
                      {collection.status === 'active' ? (
                        <Button
                          onClick={() => handlePauseCollection(collection.id)}
                          className="bg-yellow-600 hover:bg-yellow-700 text-white p-2 rounded-md"
                          title="Mettre en pause"
                        >
                          <Pause className="w-4 h-4" />
                        </Button>
                      ) : (
                        <Button
                          onClick={() => handleStartCollection(collection.id)}
                          className="bg-green-600 hover:bg-green-700 text-white p-2 rounded-md"
                          title="Démarrer"
                        >
                          <Play className="w-4 h-4" />
                        </Button>
                      )}
                      <Button
                        onClick={() => alert(`Voir les détails de ${collection.collection_name}`)}
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

        {activeTab === 'patterns' && (
          <div>
            <h2 className="text-2xl font-semibold text-gray-800 mb-6">Patterns d'Apprentissage</h2>
            
            {/* Graphiques de patterns */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
              <Card className="p-6">
                <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
                  <PieChart className="w-5 h-5 mr-2 text-blue-500" />
                  Répartition des Styles d'Apprentissage
                </h3>
                <div className="text-gray-600 text-center py-8">
                  <PieChart className="w-16 h-16 mx-auto text-gray-400 mb-4" />
                  <p>Graphique circulaire des styles à implémenter</p>
                </div>
              </Card>
              
              <Card className="p-6">
                <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
                  <LineChart className="w-5 h-5 mr-2 text-green-500" />
                  Évolution des Patterns
                </h3>
                <div className="text-gray-600 text-center py-8">
                  <LineChart className="w-16 h-16 mx-auto text-gray-400 mb-4" />
                  <p>Graphique d'évolution à implémenter</p>
                </div>
              </Card>
            </div>

            {/* Liste des patterns */}
            <div className="grid gap-6">
              {learningPatterns.map((pattern) => (
                <Card key={pattern.id} className="p-6">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center mb-2">
                        <h3 className="text-xl font-semibold text-gray-800 mr-3">
                          {pattern.student_name}
                        </h3>
                        <span className="px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                          {pattern.pattern_type.replace('_', ' ')}
                        </span>
                      </div>
                      
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm mb-4">
                        <div className="flex items-center">
                          <BookOpen className="w-4 h-4 mr-2 text-blue-500" />
                          <span className="text-gray-600">{pattern.subject}</span>
                        </div>
                        <div className="flex items-center">
                          <Clock className="w-4 h-4 mr-2 text-green-500" />
                          <span className="text-gray-600">{pattern.time_of_day}</span>
                        </div>
                        <div className="flex items-center">
                          <Activity className="w-4 h-4 mr-2 text-purple-500" />
                          <span className="text-gray-600">{pattern.session_duration} min</span>
                        </div>
                        <div className="flex items-center">
                          <Target className="w-4 h-4 mr-2 text-orange-500" />
                          <span className="text-gray-600">{(pattern.confidence_level * 100).toFixed(1)}%</span>
                        </div>
                      </div>
                      
                      <div className="text-sm text-gray-600">
                        <p><strong>Type de contenu préféré:</strong> {pattern.preferred_content_type.replace('_', ' ')}</p>
                        <p><strong>Style d'apprentissage:</strong> {pattern.learning_style}</p>
                        <p><strong>Détecté le:</strong> {pattern.detected_at}</p>
                      </div>
                    </div>
                    
                    <div className="flex space-x-2 ml-4">
                      <Button
                        onClick={() => alert(`Voir les détails pour ${pattern.student_name}`)}
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

        {activeTab === 'blockages' && (
          <div>
            <h2 className="text-2xl font-semibold text-gray-800 mb-6">Détection de Blocages</h2>
            
            {/* Statistiques des blocages */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <Card className="p-6 text-center">
                <div className="text-3xl font-bold text-red-600 mb-2">
                  {blockages.length}
                </div>
                <div className="text-gray-600">Blocages Détectés</div>
              </Card>
              
              <Card className="p-6 text-center">
                <div className="text-3xl font-bold text-yellow-600 mb-2">
                  {blockages.filter(b => b.status === 'active').length}
                </div>
                <div className="text-gray-600">Blocages Actifs</div>
              </Card>
              
              <Card className="p-6 text-center">
                <div className="text-3xl font-bold text-green-600 mb-2">
                  {blockages.filter(b => b.status === 'resolved').length}
                </div>
                <div className="text-gray-600">Blocages Résolus</div>
              </Card>
            </div>

            {/* Liste des blocages */}
            <div className="grid gap-6">
              {blockages.map((blockage) => (
                <Card key={blockage.id} className="p-6">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center mb-2">
                        <h3 className="text-xl font-semibold text-gray-800 mr-3">
                          {blockage.student_name}
                        </h3>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(blockage.status)}`}>
                          {blockage.status === 'active' ? 'Actif' : 'Résolu'}
                        </span>
                        <span className={`ml-2 px-2 py-1 rounded-full text-xs font-medium ${
                          blockage.severity_level >= 4 ? 'bg-red-100 text-red-800' :
                          blockage.severity_level >= 3 ? 'bg-yellow-100 text-yellow-800' :
                          'bg-green-100 text-green-800'
                        }`}>
                          Niveau {blockage.severity_level}/5
                        </span>
                      </div>
                      
                      <div className="mb-3">
                        <p className="text-gray-600 font-medium">{blockage.subject} - {blockage.topic}</p>
                        <p className="text-gray-800">{blockage.blockage_type.replace('_', ' ')}</p>
                      </div>
                      
                      <div className="mb-3">
                        <p className="text-gray-600 font-medium">Évidence:</p>
                        <div className="flex flex-wrap gap-2">
                          {blockage.evidence.map((evidence, index) => (
                            <span key={index} className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                              {evidence}
                            </span>
                          ))}
                        </div>
                      </div>
                      
                      <div className="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm">
                        <div className="flex items-center">
                          <Target className="w-4 h-4 mr-2 text-blue-500" />
                          <span className="text-gray-600">Confiance: {(blockage.confidence * 100).toFixed(1)}%</span>
                        </div>
                        <div className="flex items-center">
                          <Clock className="w-4 h-4 mr-2 text-green-500" />
                          <span className="text-gray-600">Détecté: {blockage.detected_at}</span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex space-x-2 ml-4">
                      <Button
                        onClick={() => alert(`Plan de remédiation pour ${blockage.student_name}`)}
                        className="bg-green-600 hover:bg-green-700 text-white p-2 rounded-md"
                        title="Plan de remédiation"
                      >
                        <CheckCircle className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'improvements' && (
          <div>
            <h2 className="text-2xl font-semibold text-gray-800 mb-6">Amélioration Continue</h2>
            
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xl font-semibold text-gray-800">Initiatives d'Amélioration</h3>
              <Button
                onClick={() => alert("Nouvelle initiative à implémenter")}
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md flex items-center"
              >
                <Plus className="w-4 h-4 mr-2" />
                Nouvelle Initiative
              </Button>
            </div>

            <div className="grid gap-6">
              {improvements.map((improvement) => (
                <Card key={improvement.id} className="p-6">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center mb-2">
                        <h3 className="text-xl font-semibold text-gray-800 mr-3">
                          {improvement.improvement_type}
                        </h3>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getImpactLevelColor(improvement.impact_level)}`}>
                          Impact {improvement.impact_level}
                        </span>
                        <span className={`ml-2 px-2 py-1 rounded-full text-xs font-medium ${getImplementationStatusColor(improvement.implementation_status)}`}>
                          {improvement.implementation_status.replace('_', ' ')}
                        </span>
                      </div>
                      
                      <p className="text-gray-600 mb-4">{improvement.description}</p>
                      
                      <div className="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm mb-4">
                        <div className="flex items-center">
                          <Calendar className="w-4 h-4 mr-2 text-blue-500" />
                          <span className="text-gray-600">Créé: {improvement.created_at}</span>
                        </div>
                        <div className="flex items-center">
                          <Target className="w-4 h-4 mr-2 text-green-500" />
                          <span className="text-gray-600">Fin estimée: {improvement.estimated_completion}</span>
                        </div>
                      </div>
                      
                      <div>
                        <p className="text-gray-600 font-medium mb-2">Métriques de succès:</p>
                        <div className="flex flex-wrap gap-2">
                          {improvement.success_metrics.map((metric, index) => (
                            <span key={index} className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">
                              {metric}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex space-x-2 ml-4">
                      <Button
                        onClick={() => alert(`Voir les détails de ${improvement.improvement_type}`)}
                        className="bg-blue-600 hover:bg-blue-700 text-white p-2 rounded-md"
                        title="Voir les détails"
                      >
                        <Eye className="w-4 h-4" />
                      </Button>
                      <Button
                        onClick={() => alert(`Modifier ${improvement.improvement_type}`)}
                        className="bg-green-600 hover:bg-green-700 text-white p-2 rounded-md"
                        title="Modifier"
                      >
                        <Settings className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
