'use client';

import React, { useState, useEffect } from 'react';
import { useAuth  } from '../../../../hooks/useAuth';
import { Card } from '../../../../components/Card';
import Button from '../../../../components/Button';
import { 
  Brain, 
  Cpu, 
  Play,
  Pause,
  Settings,
  Plus,
  Edit,
  Trash2,
  Eye,
  Download,
  Upload,
  Activity,
  TrendingUp,
  AlertCircle,
  CheckCircle,
  Clock,
  Zap,
  Target,
  BarChart3
} from 'lucide-react';

interface AIModel {
  id: number;
  name: string;
  description: string;
  model_type: string;
  technology: string;
  version: string;
  training_status: string;
  deployment_status: string;
  accuracy: number;
  performance_metrics: any;
  created_at: string;
  last_trained_at: string;
}

interface TrainingSession {
  id: number;
  model_id: number;
  model_name: string;
  session_name: string;
  status: string;
  start_time: string;
  end_time: string;
  duration: number;
  accuracy: number;
  loss: number;
}

interface ModelPrediction {
  id: number;
  model_id: number;
  model_name: string;
  prediction_type: string;
  input_data: string;
  prediction_result: string;
  confidence: number;
  processing_time: number;
  timestamp: string;
}

export default function AIModelsPage() {
  const { user, token } = useAuth();
  const [activeTab, setActiveTab] = useState('models');
  const [models, setModels] = useState<AIModel[]>([]);
  const [trainingSessions, setTrainingSessions] = useState<TrainingSession[]>([]);
  const [predictions, setPredictions] = useState<ModelPrediction[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  // Mock data pour la démonstration
  useEffect(() => {
    setModels([
      {
        id: 1,
        name: "Modèle de Recommandation - Français",
        description: "Modèle de machine learning pour recommander du contenu en français",
        model_type: "recommendation_engine",
        technology: "Scikit-learn",
        version: "2.1.0",
        training_status: "trained",
        deployment_status: "production",
        accuracy: 87.5,
        performance_metrics: { precision: 0.89, recall: 0.86, f1: 0.87 },
        created_at: "2024-01-10",
        last_trained_at: "2024-01-18"
      },
      {
        id: 2,
        name: "Modèle de Prédiction de Performance",
        description: "Réseau de neurones pour prédire les performances des étudiants",
        model_type: "neural_network",
        technology: "TensorFlow",
        version: "1.5.0",
        training_status: "training",
        deployment_status: "staging",
        accuracy: 0,
        performance_metrics: { precision: 0, recall: 0, f1: 0 },
        created_at: "2024-01-15",
        last_trained_at: "2024-01-20"
      },
      {
        id: 3,
        name: "Modèle de Détection de Blocages",
        description: "Système expert pour identifier les points de blocage d'apprentissage",
        model_type: "expert_system",
        technology: "Custom Rules",
        version: "1.0.0",
        training_status: "not_trained",
        deployment_status: "not_deployed",
        accuracy: 0,
        performance_metrics: { precision: 0, recall: 0, f1: 0 },
        created_at: "2024-01-20",
        last_trained_at: ""
      }
    ]);

    setTrainingSessions([
      {
        id: 1,
        model_id: 2,
        model_name: "Modèle de Prédiction de Performance",
        session_name: "Session d'entraînement #1",
        status: "running",
        start_time: "2024-01-20 09:00:00",
        end_time: "",
        duration: 0,
        accuracy: 0,
        loss: 0
      },
      {
        id: 2,
        model_id: 1,
        model_name: "Modèle de Recommandation - Français",
        session_name: "Session d'entraînement #3",
        status: "completed",
        start_time: "2024-01-18 14:00:00",
        end_time: "2024-01-18 16:30:00",
        duration: 9000,
        accuracy: 87.5,
        loss: 0.12
      }
    ]);

    setPredictions([
      {
        id: 1,
        model_id: 1,
        model_name: "Modèle de Recommandation - Français",
        prediction_type: "Recommandation de contenu",
        input_data: "Étudiant: Marie, Niveau: Intermédiaire, Matière: Grammaire",
        prediction_result: "Exercices de conjugaison, niveau 4-5",
        confidence: 0.89,
        processing_time: 45,
        timestamp: "2024-01-20 10:30:00"
      },
      {
        id: 2,
        model_id: 1,
        model_name: "Modèle de Recommandation - Français",
        prediction_type: "Recommandation de contenu",
        input_data: "Étudiant: Ahmed, Niveau: Avancé, Matière: Littérature",
        prediction_result: "Textes classiques, analyse critique",
        confidence: 0.92,
        processing_time: 38,
        timestamp: "2024-01-20 11:15:00"
      }
    ]);
  }, []);

  const handleCreateModel = () => {
    alert("Création de modèle IA à implémenter");
  };

  const handleEditModel = (modelId: number) => {
    alert(`Édition du modèle ${modelId} à implémenter`);
  };

  const handleStartTraining = (modelId: number) => {
    alert(`Démarrage de l'entraînement pour le modèle ${modelId}`);
  };

  const handleDeployModel = (modelId: number) => {
    alert(`Déploiement du modèle ${modelId} à implémenter`);
  };

  const getStatusColor = (status: string, type: 'training' | 'deployment') => {
    if (type === 'training') {
      switch (status) {
        case 'not_trained': return 'text-gray-600 bg-gray-100';
        case 'training': return 'text-yellow-600 bg-yellow-100';
        case 'trained': return 'text-green-600 bg-green-100';
        case 'failed': return 'text-red-600 bg-red-100';
        default: return 'text-gray-600 bg-gray-100';
      }
    } else {
      switch (status) {
        case 'not_deployed': return 'text-gray-600 bg-gray-100';
        case 'testing': return 'text-blue-600 bg-blue-100';
        case 'staging': return 'text-purple-600 bg-purple-100';
        case 'production': return 'text-green-600 bg-green-100';
        case 'maintenance': return 'text-orange-600 bg-orange-100';
        default: return 'text-gray-600 bg-gray-100';
      }
    }
  };

  const getStatusText = (status: string, type: 'training' | 'deployment') => {
    if (type === 'training') {
      switch (status) {
        case 'not_trained': return 'Non entraîné';
        case 'training': return 'En entraînement';
        case 'trained': return 'Entraîné';
        case 'failed': return 'Échec';
        default: return status;
      }
    } else {
      switch (status) {
        case 'not_deployed': return 'Non déployé';
        case 'testing': return 'En test';
        case 'staging': return 'Staging';
        case 'production': return 'Production';
        case 'maintenance': return 'Maintenance';
        default: return status;
      }
    }
  };

  const getModelTypeIcon = (type: string) => {
    switch (type) {
      case 'neural_network': return <Brain className="w-5 h-5 text-purple-500" />;
      case 'recommendation_engine': return <Target className="w-5 h-5 text-blue-500" />;
      case 'expert_system': return <Cpu className="w-5 h-5 text-green-500" />;
      case 'nlp_model': return <Zap className="w-5 h-5 text-yellow-500" />;
      default: return <Brain className="w-5 h-5 text-gray-500" />;
    }
  };

  const formatDuration = (seconds: number) => {
    if (seconds === 0) return 'En cours...';
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    return `${hours}h ${minutes}m`;
  };

  return (
    <div className="flex min-h-screen bg-gray-100">
      <main className="flex-1 p-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2 flex items-center">
            <Brain className="mr-3 text-purple-600" size={32} />
            Modèles d'Intelligence Artificielle
          </h1>
          <p className="text-gray-600">
            Gérez vos modèles d'IA, supervisez l'entraînement et surveillez les performances
          </p>
        </div>

        {/* Onglets */}
        <div className="mb-6">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              <button
                onClick={() => setActiveTab('models')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'models'
                    ? 'border-purple-500 text-purple-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Modèles IA
              </button>
              <button
                onClick={() => setActiveTab('training')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'training'
                    ? 'border-purple-500 text-purple-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Sessions d'Entraînement
              </button>
              <button
                onClick={() => setActiveTab('predictions')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'predictions'
                    ? 'border-purple-500 text-purple-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Prédictions
              </button>
              <button
                onClick={() => setActiveTab('monitoring')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'monitoring'
                    ? 'border-purple-500 text-purple-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Monitoring
              </button>
            </nav>
          </div>
        </div>

        {/* Contenu des onglets */}
        {activeTab === 'models' && (
          <div>
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-semibold text-gray-800">Modèles d'IA</h2>
              <Button
                onClick={handleCreateModel}
                className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-md flex items-center"
              >
                <Plus className="w-4 h-4 mr-2" />
                Nouveau Modèle
              </Button>
            </div>

            <div className="grid gap-6">
              {models.map((model) => (
                <Card key={model.id} className="p-6">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center mb-3">
                        {getModelTypeIcon(model.model_type)}
                        <h3 className="text-xl font-semibold text-gray-800 ml-3">
                          {model.name}
                        </h3>
                      </div>
                      
                      <p className="text-gray-600 mb-4">{model.description}</p>
                      
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm mb-4">
                        <div className="flex items-center">
                          <Cpu className="w-4 h-4 mr-2 text-blue-500" />
                          <span className="text-gray-600">{model.technology}</span>
                        </div>
                        <div className="flex items-center">
                          <Settings className="w-4 h-4 mr-2 text-green-500" />
                          <span className="text-gray-600">v{model.version}</span>
                        </div>
                        <div className="flex items-center">
                          <Target className="w-4 h-4 mr-2 text-purple-500" />
                          <span className="text-gray-600">{model.accuracy > 0 ? `${model.accuracy}%` : 'N/A'}</span>
                        </div>
                        <div className="flex items-center">
                          <Clock className="w-4 h-4 mr-2 text-orange-500" />
                          <span className="text-gray-600">{model.last_trained_at || 'Jamais'}</span>
                        </div>
                      </div>
                      
                      <div className="flex space-x-2">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(model.training_status, 'training')}`}>
                          {getStatusText(model.training_status, 'training')}
                        </span>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(model.deployment_status, 'deployment')}`}>
                          {getStatusText(model.deployment_status, 'deployment')}
                        </span>
                      </div>
                    </div>
                    
                    <div className="flex space-x-2 ml-4">
                      <Button
                        onClick={() => alert(`Voir les détails de ${model.name}`)}
                        className="bg-blue-600 hover:bg-blue-700 text-white p-2 rounded-md"
                        title="Voir les détails"
                      >
                        <Eye className="w-4 h-4" />
                      </Button>
                      <Button
                        onClick={() => handleEditModel(model.id)}
                        className="bg-green-600 hover:bg-green-700 text-white p-2 rounded-md"
                        title="Modifier"
                      >
                        <Edit className="w-4 h-4" />
                      </Button>
                      {model.training_status === 'not_trained' && (
                        <Button
                          onClick={() => handleStartTraining(model.id)}
                          className="bg-yellow-600 hover:bg-yellow-700 text-white p-2 rounded-md"
                          title="Démarrer l'entraînement"
                        >
                          <Play className="w-4 h-4" />
                        </Button>
                      )}
                      {model.training_status === 'trained' && model.deployment_status !== 'production' && (
                        <Button
                          onClick={() => handleDeployModel(model.id)}
                          className="bg-purple-600 hover:bg-purple-700 text-white p-2 rounded-md"
                          title="Déployer"
                        >
                          <Upload className="w-4 h-4" />
                        </Button>
                      )}
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'training' && (
          <div>
            <h2 className="text-2xl font-semibold text-gray-800 mb-6">Sessions d'Entraînement</h2>
            
            <div className="grid gap-6">
              {trainingSessions.map((session) => (
                <Card key={session.id} className="p-6">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center mb-2">
                        <h3 className="text-xl font-semibold text-gray-800 mr-3">
                          {session.session_name}
                        </h3>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                          session.status === 'running' ? 'text-yellow-600 bg-yellow-100' :
                          session.status === 'completed' ? 'text-green-600 bg-green-100' :
                          'text-gray-600 bg-gray-100'
                        }`}>
                          {session.status === 'running' ? 'En cours' :
                           session.status === 'completed' ? 'Terminé' : session.status}
                        </span>
                      </div>
                      
                      <p className="text-gray-600 mb-3">Modèle: {session.model_name}</p>
                      
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                        <div className="flex items-center">
                          <Clock className="w-4 h-4 mr-2 text-blue-500" />
                          <span className="text-gray-600">Début: {session.start_time}</span>
                        </div>
                        <div className="flex items-center">
                          <Clock className="w-4 h-4 mr-2 text-green-500" />
                          <span className="text-gray-600">Fin: {session.end_time || 'En cours'}</span>
                        </div>
                        <div className="flex items-center">
                          <Activity className="w-4 h-4 mr-2 text-purple-500" />
                          <span className="text-gray-600">Durée: {formatDuration(session.duration)}</span>
                        </div>
                        <div className="flex items-center">
                          <Target className="w-4 h-4 mr-2 text-orange-500" />
                          <span className="text-gray-600">Précision: {session.accuracy > 0 ? `${session.accuracy}%` : 'N/A'}</span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex space-x-2 ml-4">
                      {session.status === 'running' && (
                        <Button
                          onClick={() => alert(`Arrêter l'entraînement de ${session.session_name}`)}
                          className="bg-red-600 hover:bg-red-700 text-white p-2 rounded-md"
                          title="Arrêter"
                        >
                          <Pause className="w-4 h-4" />
                        </Button>
                      )}
                      <Button
                        onClick={() => alert(`Voir les logs de ${session.session_name}`)}
                        className="bg-blue-600 hover:bg-blue-700 text-white p-2 rounded-md"
                        title="Voir les logs"
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

        {activeTab === 'predictions' && (
          <div>
            <h2 className="text-2xl font-semibold text-gray-800 mb-6">Prédictions Récentes</h2>
            
            <div className="grid gap-6">
              {predictions.map((prediction) => (
                <Card key={prediction.id} className="p-6">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center mb-2">
                        <h3 className="text-xl font-semibold text-gray-800 mr-3">
                          {prediction.model_name}
                        </h3>
                        <span className="px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                          {prediction.prediction_type}
                        </span>
                      </div>
                      
                      <div className="mb-3">
                        <p className="text-gray-600 font-medium">Données d'entrée:</p>
                        <p className="text-gray-800 text-sm bg-gray-50 p-2 rounded">{prediction.input_data}</p>
                      </div>
                      
                      <div className="mb-3">
                        <p className="text-gray-600 font-medium">Résultat:</p>
                        <p className="text-gray-800 text-sm bg-green-50 p-2 rounded">{prediction.prediction_result}</p>
                      </div>
                      
                      <div className="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm">
                        <div className="flex items-center">
                          <Target className="w-4 h-4 mr-2 text-blue-500" />
                          <span className="text-gray-600">Confiance: {(prediction.confidence * 100).toFixed(1)}%</span>
                        </div>
                        <div className="flex items-center">
                          <Zap className="w-4 h-4 mr-2 text-green-500" />
                          <span className="text-gray-600">Temps: {prediction.processing_time}ms</span>
                        </div>
                        <div className="flex items-center">
                          <Clock className="w-4 h-4 mr-2 text-purple-500" />
                          <span className="text-gray-600">{prediction.timestamp}</span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex space-x-2 ml-4">
                      <Button
                        onClick={() => alert(`Voir les détails de la prédiction`)}
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

        {activeTab === 'monitoring' && (
          <div>
            <h2 className="text-2xl font-semibold text-gray-800 mb-6">Monitoring des Modèles</h2>
            
            {/* Métriques de performance */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
              <Card className="p-6 text-center">
                <div className="text-3xl font-bold text-purple-600 mb-2">{models.length}</div>
                <div className="text-gray-600">Modèles Totaux</div>
              </Card>
              
              <Card className="p-6 text-center">
                <div className="text-3xl font-bold text-green-600 mb-2">
                  {models.filter(m => m.deployment_status === 'production').length}
                </div>
                <div className="text-gray-600">En Production</div>
              </Card>
              
              <Card className="p-6 text-center">
                <div className="text-3xl font-bold text-blue-600 mb-2">
                  {models.filter(m => m.training_status === 'trained').length}
                </div>
                <div className="text-gray-600">Entraînés</div>
              </Card>
              
              <Card className="p-6 text-center">
                <div className="text-3xl font-bold text-orange-600 mb-2">
                  {predictions.length}
                </div>
                <div className="text-gray-600">Prédictions Aujourd'hui</div>
              </Card>
            </div>

            {/* Graphiques de performance */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
              <Card className="p-6">
                <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
                  <TrendingUp className="w-5 h-5 mr-2 text-blue-500" />
                  Précision des Modèles
                </h3>
                <div className="text-gray-600 text-center py-8">
                  <BarChart3 className="w-16 h-16 mx-auto text-gray-400 mb-4" />
                  <p>Graphique de précision à implémenter</p>
                </div>
              </Card>
              
              <Card className="p-6">
                <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
                  <Activity className="w-5 h-5 mr-2 text-green-500" />
                  Temps de Traitement
                </h3>
                <div className="text-gray-600 text-center py-8">
                  <BarChart3 className="w-16 h-16 mx-auto text-gray-400 mb-4" />
                  <p>Graphique de performance à implémenter</p>
                </div>
              </Card>
            </div>

            {/* Alertes et notifications */}
            <Card className="p-6">
              <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
                <AlertCircle className="w-5 h-5 mr-2 text-orange-500" />
                Alertes et Notifications
              </h3>
              <div className="space-y-3">
                <div className="flex items-center p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                  <AlertCircle className="w-5 h-5 text-yellow-600 mr-3" />
                  <div>
                    <p className="text-yellow-800 font-medium">Modèle en entraînement depuis 2h</p>
                    <p className="text-yellow-700 text-sm">Le modèle "Prédiction de Performance" est en cours d'entraînement</p>
                  </div>
                </div>
                
                <div className="flex items-center p-3 bg-green-50 border border-green-200 rounded-lg">
                  <CheckCircle className="w-5 h-5 text-green-600 mr-3" />
                  <div>
                    <p className="text-green-800 font-medium">Modèle déployé avec succès</p>
                    <p className="text-green-700 text-sm">Le modèle "Recommandation - Français" est maintenant en production</p>
                  </div>
                </div>
              </div>
            </Card>
          </div>
        )}
      </main>
    </div>
  );
}
