'use client';

import React, { useState, useEffect } from 'react';
import { Card } from './Card';
import { 
  Users, 
  BookOpen, 
  BarChart3, 
  Clock,
  AlertCircle,
  CheckCircle,
  Target,
  MessageSquare,
  Settings,
  Plus,
  PieChart,
  TrendingUp,
  Activity,
  Eye,
  Edit,
  Trash2,
  X,
  Save,
  UserPlus,
  UserMinus
} from 'lucide-react';

interface AdvancedTeacherInterfaceProps {
  user: any;
  token: string;
}

interface ClassData {
  id: number;
  name: string;
  description: string;
  student_count: number;
  average_progress: number;
  level: string;
  subject: string;
}

interface LearningPathData {
  id: number;
  name: string;
  description: string;
  level: string;
  estimated_duration: number;
  is_adaptive: boolean;
  steps: any[];
}

interface RealTimeData {
  active_students: number;
  current_activities: any[];
  class_performances: any[];
  alerts: any[];
}

export default function AdvancedTeacherInterface({ user, token }: AdvancedTeacherInterfaceProps) {
  const [activeTab, setActiveTab] = useState<'overview' | 'classes' | 'paths' | 'realtime' | 'reports'>('overview');
  const [classes, setClasses] = useState<ClassData[]>([]);
  const [learningPaths, setLearningPaths] = useState<LearningPathData[]>([]);
  const [realTimeData, setRealTimeData] = useState<RealTimeData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // États pour les modales
  const [showCreateClass, setShowCreateClass] = useState(false);
  const [showCreatePath, setShowCreatePath] = useState(false);
  const [showEditClass, setShowEditClass] = useState(false);
  const [showEditPath, setShowEditPath] = useState(false);
  const [selectedClass, setSelectedClass] = useState<ClassData | null>(null);
  const [selectedPath, setSelectedPath] = useState<LearningPathData | null>(null);
  const [showClassDetails, setShowClassDetails] = useState(false);
  const [classStudents, setClassStudents] = useState<any[]>([]);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [classesRes, pathsRes, realtimeRes] = await Promise.allSettled([
        fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/teacher/classes/`, {
          headers: { 
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }),
        fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/teacher/learning-paths/`, {
          headers: { 
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }),
        fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/teacher/realtime/dashboard`, {
          headers: { 
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })
      ]);

      if (classesRes.status === 'fulfilled' && classesRes.value.ok) {
        const classesData = await classesRes.value.json();
        setClasses(classesData);
      }

      if (pathsRes.status === 'fulfilled' && pathsRes.value.ok) {
        const pathsData = await pathsRes.value.json();
        setLearningPaths(pathsData);
      }

      if (realtimeRes.status === 'fulfilled' && realtimeRes.value.ok) {
        const realtimeData = await realtimeRes.value.json();
        setRealTimeData(realtimeData);
      }

    } catch (err) {
      setError('Erreur lors du chargement des données');
      console.error('Erreur dashboard:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchClassStudents = async (classId: number) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/teacher/classes/${classId}/students`, {
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        const students = await response.json();
        setClassStudents(students);
      }
    } catch (err) {
      console.error('Erreur lors du chargement des étudiants:', err);
    }
  };

  const handleCreateClass = async (classData: any) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/teacher/classes/`, {
        method: 'POST',
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(classData)
      });
      
      if (response.ok) {
        setShowCreateClass(false);
        fetchDashboardData();
      }
    } catch (err) {
      console.error('Erreur lors de la création de la classe:', err);
    }
  };

  const handleCreatePath = async (pathData: any) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/teacher/learning-paths/`, {
        method: 'POST',
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(pathData)
      });
      
      if (response.ok) {
        setShowCreatePath(false);
        fetchDashboardData();
      }
    } catch (err) {
      console.error('Erreur lors de la création du parcours:', err);
    }
  };

  const handleDeleteClass = async (classId: number) => {
    if (!confirm('Êtes-vous sûr de vouloir supprimer cette classe ?')) return;
    
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/teacher/classes/${classId}`, {
        method: 'DELETE',
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        fetchDashboardData();
      }
    } catch (err) {
      console.error('Erreur lors de la suppression de la classe:', err);
    }
  };

  const handleDeletePath = async (pathId: number) => {
    if (!confirm('Êtes-vous sûr de vouloir supprimer ce parcours ?')) return;
    
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/teacher/learning-paths/${pathId}`, {
        method: 'DELETE',
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        fetchDashboardData();
      }
    } catch (err) {
      console.error('Erreur lors de la suppression du parcours:', err);
    }
  };

  const getTabIcon = (tab: string) => {
    switch (tab) {
      case 'overview': return <BarChart3 className="w-5 h-5" />;
      case 'classes': return <Users className="w-5 h-5" />;
      case 'paths': return <BookOpen className="w-5 h-5" />;
      case 'realtime': return <Activity className="w-5 h-5" />;
      case 'reports': return <PieChart className="w-5 h-5" />;
      default: return <BarChart3 className="w-5 h-5" />;
    }
  };

  const getTabLabel = (tab: string) => {
    switch (tab) {
      case 'overview': return 'Vue d\'ensemble';
      case 'classes': return 'Classes';
      case 'paths': return 'Parcours';
      case 'realtime': return 'Temps réel';
      case 'reports': return 'Rapports';
      default: return 'Vue d\'ensemble';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center p-8">
        <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
        <p className="text-red-600">{error}</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* En-tête */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Interface Enseignant Avancée</h1>
          <p className="text-gray-600">Bienvenue, {user?.username}</p>
        </div>
        <div className="flex space-x-2">
          <button 
            onClick={() => setShowCreateClass(true)}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center space-x-2 hover:bg-blue-700"
          >
            <Plus className="w-4 h-4" />
            <span>Nouvelle Classe</span>
          </button>
          <button 
            onClick={() => setShowCreatePath(true)}
            className="bg-green-600 text-white px-4 py-2 rounded-lg flex items-center space-x-2 hover:bg-green-700"
          >
            <Plus className="w-4 h-4" />
            <span>Nouveau Parcours</span>
          </button>
        </div>
      </div>

      {/* Navigation par onglets */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {(['overview', 'classes', 'paths', 'realtime', 'reports'] as const).map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`flex items-center space-x-2 py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === tab
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              {getTabIcon(tab)}
              <span>{getTabLabel(tab)}</span>
            </button>
          ))}
        </nav>
      </div>

      {/* Contenu des onglets */}
      <div className="mt-6">
        {activeTab === 'overview' && (
          <OverviewTab 
            classes={classes} 
            learningPaths={learningPaths} 
            realTimeData={realTimeData} 
          />
        )}
        {activeTab === 'classes' && (
          <ClassesTab 
            classes={classes} 
            token={token} 
            onRefresh={fetchDashboardData}
            onEdit={(classData: ClassData) => {
              setSelectedClass(classData);
              setShowEditClass(true);
            }}
            onDelete={handleDeleteClass}
            onViewDetails={(classData: ClassData) => {
              setSelectedClass(classData);
              setShowClassDetails(true);
              fetchClassStudents(classData.id);
            }}
          />
        )}
        {activeTab === 'paths' && (
          <LearningPathsTab 
            learningPaths={learningPaths} 
            token={token} 
            onRefresh={fetchDashboardData}
            onEdit={(pathData: LearningPathData) => {
              setSelectedPath(pathData);
              setShowEditPath(true);
            }}
            onDelete={handleDeletePath}
          />
        )}
        {activeTab === 'realtime' && (
          <RealTimeTab 
            realTimeData={realTimeData} 
            token={token} 
          />
        )}
        {activeTab === 'reports' && (
          <ReportsTab 
            classes={classes} 
            token={token} 
          />
        )}
      </div>

      {/* Modales */}
      {showCreateClass && (
        <CreateClassModal 
          onClose={() => setShowCreateClass(false)}
          onSubmit={handleCreateClass}
        />
      )}
      
      {showCreatePath && (
        <CreatePathModal 
          onClose={() => setShowCreatePath(false)}
          onSubmit={handleCreatePath}
        />
      )}
      
      {showEditClass && selectedClass && (
        <EditClassModal 
          classData={selectedClass}
          onClose={() => {
            setShowEditClass(false);
            setSelectedClass(null);
          }}
          onSubmit={handleCreateClass}
        />
      )}
      
      {showEditPath && selectedPath && (
        <EditPathModal 
          pathData={selectedPath}
          onClose={() => {
            setShowEditPath(false);
            setSelectedPath(null);
          }}
          onSubmit={handleCreatePath}
        />
      )}
      
      {showClassDetails && selectedClass && (
        <ClassDetailsModal 
          classData={selectedClass}
          students={classStudents}
          onClose={() => {
            setShowClassDetails(false);
            setSelectedClass(null);
            setClassStudents([]);
          }}
          token={token}
        />
      )}
    </div>
  );
}

// Composant Vue d'ensemble
function OverviewTab({ classes, learningPaths, realTimeData }: any) {
  return (
    <div className="space-y-6">
      {/* Statistiques principales */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <div className="flex items-center">
            <div className="p-3 bg-blue-100 rounded-lg">
              <Users className="w-6 h-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Classes</p>
              <p className="text-2xl font-bold text-gray-900">{classes.length}</p>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center">
            <div className="p-3 bg-green-100 rounded-lg">
              <BookOpen className="w-6 h-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Parcours</p>
              <p className="text-2xl font-bold text-gray-900">{learningPaths.length}</p>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center">
            <div className="p-3 bg-purple-100 rounded-lg">
              <Activity className="w-6 h-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Étudiants Actifs</p>
              <p className="text-2xl font-bold text-gray-900">{realTimeData?.active_students || 0}</p>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center">
            <div className="p-3 bg-orange-100 rounded-lg">
              <TrendingUp className="w-6 h-6 text-orange-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Progression Moy.</p>
              <p className="text-2xl font-bold text-gray-900">
                {classes.length > 0 
                  ? Math.round(classes.reduce((acc: number, c: any) => acc + c.average_progress, 0) / classes.length)
                  : 0}%
              </p>
            </div>
          </div>
        </Card>
      </div>

      {/* Alertes et notifications */}
      {realTimeData?.alerts && realTimeData.alerts.length > 0 && (
        <Card>
          <h3 className="text-lg font-semibold mb-4 flex items-center">
            <AlertCircle className="w-5 h-5 text-red-500 mr-2" />
            Alertes
          </h3>
          <div className="space-y-2">
            {realTimeData.alerts.map((alert: any, index: number) => (
              <div key={index} className="flex items-center p-3 bg-red-50 rounded-lg">
                <AlertCircle className="w-4 h-4 text-red-500 mr-2" />
                <span className="text-sm text-red-700">{alert.message}</span>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* Activités récentes */}
      {realTimeData?.current_activities && realTimeData.current_activities.length > 0 && (
        <Card>
          <h3 className="text-lg font-semibold mb-4 flex items-center">
            <Clock className="w-5 h-5 text-blue-500 mr-2" />
            Activités Récentes
          </h3>
          <div className="space-y-2">
            {realTimeData.current_activities.slice(0, 5).map((activity: any, index: number) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center">
                  <Activity className="w-4 h-4 text-blue-500 mr-2" />
                  <span className="text-sm text-gray-700">{activity.activity_type}</span>
                </div>
                <span className="text-xs text-gray-500">
                  {new Date(activity.timestamp).toLocaleTimeString()}
                </span>
              </div>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
}

// Composant Classes
function ClassesTab({ classes, token, onRefresh, onEdit, onDelete, onViewDetails }: any) {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold">Gestion des Classes</h2>
        <button 
          onClick={() => setShowCreateClass(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
        >
          <Plus className="w-4 h-4 inline mr-2" />
          Nouvelle Classe
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {classes.map((classData: any) => (
          <Card key={classData.id}>
            <div className="p-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-lg font-semibold">{classData.name}</h3>
                  <p className="text-sm text-gray-600">{classData.description}</p>
                </div>
                <div className="text-right">
                  <span className={`px-2 py-1 text-xs rounded-full ${
                    classData.is_active 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-red-100 text-red-800'
                  }`}>
                    {classData.is_active ? 'Active' : 'Inactive'}
                  </span>
                </div>
              </div>

              <div className="space-y-3">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Étudiants:</span>
                  <span className="font-medium">{classData.student_count}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Niveau:</span>
                  <span className="font-medium">{classData.level}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Matière:</span>
                  <span className="font-medium">{classData.subject}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Progression:</span>
                  <span className="font-medium">{Math.round(classData.average_progress)}%</span>
                </div>
              </div>

              <div className="mt-4 pt-4 border-t border-gray-200">
                <div className="flex space-x-2">
                  <button 
                    onClick={() => onViewDetails(classData)}
                    className="flex-1 bg-blue-100 text-blue-700 px-3 py-2 rounded text-sm hover:bg-blue-200"
                  >
                    <Eye className="w-4 h-4 inline mr-1" />
                    Voir
                  </button>
                  <button 
                    onClick={() => onEdit(classData)}
                    className="flex-1 bg-gray-100 text-gray-700 px-3 py-2 rounded text-sm hover:bg-gray-200"
                  >
                    <BarChart3 className="w-4 h-4 inline mr-1" />
                    Analytics
                  </button>
                  <button 
                    onClick={() => onDelete(classData.id)}
                    className="flex-1 bg-red-100 text-red-700 px-3 py-2 rounded text-sm hover:bg-red-200"
                  >
                    <Trash2 className="w-4 h-4 inline mr-1" />
                    Supprimer
                  </button>
                </div>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}

// Composant Parcours d'Apprentissage
function LearningPathsTab({ learningPaths, token, onRefresh, onEdit, onDelete }: any) {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold">Parcours d'Apprentissage</h2>
        <button 
          onClick={() => setShowCreatePath(true)}
          className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700"
        >
          <Plus className="w-4 h-4 inline mr-2" />
          Nouveau Parcours
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {learningPaths.map((path: any) => (
          <Card key={path.id}>
            <div className="p-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-lg font-semibold">{path.name}</h3>
                  <p className="text-sm text-gray-600">{path.description}</p>
                </div>
                <div className="text-right">
                  <span className={`px-2 py-1 text-xs rounded-full ${
                    path.is_adaptive 
                      ? 'bg-purple-100 text-purple-800' 
                      : 'bg-gray-100 text-gray-800'
                  }`}>
                    {path.is_adaptive ? 'Adaptatif' : 'Standard'}
                  </span>
                </div>
              </div>

              <div className="space-y-3">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Niveau:</span>
                  <span className="font-medium">{path.level}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Durée:</span>
                  <span className="font-medium">{path.estimated_duration} jours</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Étapes:</span>
                  <span className="font-medium">{path.steps?.length || 0}</span>
                </div>
              </div>

              <div className="mt-4 pt-4 border-t border-gray-200">
                <div className="flex space-x-2">
                  <button 
                    onClick={() => onEdit(path)}
                    className="flex-1 bg-blue-100 text-blue-700 px-3 py-2 rounded text-sm hover:bg-blue-200"
                  >
                    <Settings className="w-4 h-4 inline mr-1" />
                    Éditer
                  </button>
                  <button 
                    onClick={() => onDelete(path.id)}
                    className="flex-1 bg-red-100 text-red-700 px-3 py-2 rounded text-sm hover:bg-red-200"
                  >
                    <Trash2 className="w-4 h-4 inline mr-1" />
                    Supprimer
                  </button>
                </div>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}

// Composant Temps Réel
function RealTimeTab({ realTimeData, token }: any) {
  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">Suivi en Temps Réel</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Activités en cours */}
        <Card>
          <h3 className="text-lg font-semibold mb-4 flex items-center">
            <Activity className="w-5 h-5 text-blue-500 mr-2" />
            Activités en Cours
          </h3>
          <div className="space-y-3">
            {realTimeData?.current_activities?.slice(0, 10).map((activity: any, index: number) => (
              <div key={index} className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                <div className="flex items-center">
                  <div className="w-2 h-2 bg-blue-500 rounded-full mr-3"></div>
                  <div>
                    <p className="text-sm font-medium">{activity.activity_type}</p>
                    <p className="text-xs text-gray-500">Étudiant #{activity.student_id}</p>
                  </div>
                </div>
                <span className="text-xs text-gray-500">
                  {new Date(activity.timestamp).toLocaleTimeString()}
                </span>
              </div>
            ))}
          </div>
        </Card>

        {/* Performances des classes */}
        <Card>
          <h3 className="text-lg font-semibold mb-4 flex items-center">
            <BarChart3 className="w-5 h-5 text-green-500 mr-2" />
            Performances des Classes
          </h3>
          <div className="space-y-3">
            {realTimeData?.class_performances?.slice(0, 5).map((performance: any, index: number) => (
              <div key={index} className="p-3 bg-green-50 rounded-lg">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm font-medium">Classe #{performance.class_id}</span>
                  <span className="text-sm text-green-600">{performance.average_progress}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-green-500 h-2 rounded-full" 
                    style={{ width: `${performance.average_progress}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
}

// Composant Rapports
function ReportsTab({ classes, token }: any) {
  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">Rapports Avancés</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <h3 className="text-lg font-semibold mb-4">Rapports par Classe</h3>
          <div className="space-y-3">
            {classes.map((classData: any) => (
              <button
                key={classData.id}
                className="w-full text-left p-3 hover:bg-gray-50 rounded-lg border border-gray-200"
              >
                <div className="flex justify-between items-center">
                  <span className="font-medium">{classData.name}</span>
                  <span className="text-sm text-gray-500">
                    {classData.student_count} étudiants
                  </span>
                </div>
                <div className="flex justify-between items-center mt-1">
                  <span className="text-sm text-gray-600">Progression: {Math.round(classData.average_progress)}%</span>
                  <span className="text-xs text-blue-600">Voir rapport →</span>
                </div>
              </button>
            ))}
          </div>
        </Card>

        <Card>
          <h3 className="text-lg font-semibold mb-4">Rapports par Étudiant</h3>
          <div className="text-center py-8 text-gray-500">
            <Users className="w-12 h-12 mx-auto mb-4 text-gray-300" />
            <p>Sélectionnez une classe pour voir les rapports des étudiants</p>
          </div>
        </Card>
      </div>
    </div>
  );
} 

// Composant Modal de Création de Classe
function CreateClassModal({ onClose, onSubmit }: any) {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    level: 'primary',
    subject: '',
    max_students: 30
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold">Nouvelle Classe</h3>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
            <X className="w-5 h-5" />
          </button>
        </div>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Nom de la classe
            </label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({...formData, name: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={3}
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Niveau
            </label>
            <select
              value={formData.level}
              onChange={(e) => setFormData({...formData, level: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="primary">Primaire</option>
              <option value="middle">Collège</option>
              <option value="high">Lycée</option>
              <option value="university">Université</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Matière
            </label>
            <input
              type="text"
              value={formData.subject}
              onChange={(e) => setFormData({...formData, subject: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Nombre maximum d'étudiants
            </label>
            <input
              type="number"
              value={formData.max_students}
              onChange={(e) => setFormData({...formData, max_students: parseInt(e.target.value)})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              min="1"
              max="100"
            />
          </div>
          
          <div className="flex space-x-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
            >
              Annuler
            </button>
            <button
              type="submit"
              className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              Créer
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

// Composant Modal de Création de Parcours
function CreatePathModal({ onClose, onSubmit }: any) {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    objectives: '',
    level: 'intermediate',
    estimated_duration: 30,
    is_adaptive: false,
    steps: []
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold">Nouveau Parcours</h3>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
            <X className="w-5 h-5" />
          </button>
        </div>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Nom du parcours
            </label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({...formData, name: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={3}
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Objectifs
            </label>
            <textarea
              value={formData.objectives}
              onChange={(e) => setFormData({...formData, objectives: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={3}
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Niveau
            </label>
            <select
              value={formData.level}
              onChange={(e) => setFormData({...formData, level: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="beginner">Débutant</option>
              <option value="intermediate">Intermédiaire</option>
              <option value="advanced">Avancé</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Durée estimée (jours)
            </label>
            <input
              type="number"
              value={formData.estimated_duration}
              onChange={(e) => setFormData({...formData, estimated_duration: parseInt(e.target.value)})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              min="1"
              max="365"
            />
          </div>
          
          <div className="flex items-center">
            <input
              type="checkbox"
              id="is_adaptive"
              checked={formData.is_adaptive}
              onChange={(e) => setFormData({...formData, is_adaptive: e.target.checked})}
              className="mr-2"
            />
            <label htmlFor="is_adaptive" className="text-sm text-gray-700">
              Parcours adaptatif
            </label>
          </div>
          
          <div className="flex space-x-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
            >
              Annuler
            </button>
            <button
              type="submit"
              className="flex-1 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
            >
              Créer
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

// Composant Modal d'Édition de Classe
function EditClassModal({ classData, onClose, onSubmit }: any) {
  const [formData, setFormData] = useState({
    name: classData.name,
    description: classData.description || '',
    level: classData.level,
    subject: classData.subject || '',
    max_students: classData.max_students || 30
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold">Modifier la Classe</h3>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
            <X className="w-5 h-5" />
          </button>
        </div>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Nom de la classe
            </label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({...formData, name: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={3}
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Niveau
            </label>
            <select
              value={formData.level}
              onChange={(e) => setFormData({...formData, level: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="primary">Primaire</option>
              <option value="middle">Collège</option>
              <option value="high">Lycée</option>
              <option value="university">Université</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Matière
            </label>
            <input
              type="text"
              value={formData.subject}
              onChange={(e) => setFormData({...formData, subject: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Nombre maximum d'étudiants
            </label>
            <input
              type="number"
              value={formData.max_students}
              onChange={(e) => setFormData({...formData, max_students: parseInt(e.target.value)})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              min="1"
              max="100"
            />
          </div>
          
          <div className="flex space-x-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
            >
              Annuler
            </button>
            <button
              type="submit"
              className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              <Save className="w-4 h-4 inline mr-2" />
              Sauvegarder
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

// Composant Modal d'Édition de Parcours
function EditPathModal({ pathData, onClose, onSubmit }: any) {
  const [formData, setFormData] = useState({
    name: pathData.name,
    description: pathData.description || '',
    objectives: pathData.objectives || '',
    level: pathData.level,
    estimated_duration: pathData.estimated_duration,
    is_adaptive: pathData.is_adaptive,
    steps: pathData.steps || []
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold">Modifier le Parcours</h3>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
            <X className="w-5 h-5" />
          </button>
        </div>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Nom du parcours
            </label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({...formData, name: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={3}
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Objectifs
            </label>
            <textarea
              value={formData.objectives}
              onChange={(e) => setFormData({...formData, objectives: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={3}
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Niveau
            </label>
            <select
              value={formData.level}
              onChange={(e) => setFormData({...formData, level: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="beginner">Débutant</option>
              <option value="intermediate">Intermédiaire</option>
              <option value="advanced">Avancé</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Durée estimée (jours)
            </label>
            <input
              type="number"
              value={formData.estimated_duration}
              onChange={(e) => setFormData({...formData, estimated_duration: parseInt(e.target.value)})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              min="1"
              max="365"
            />
          </div>
          
          <div className="flex items-center">
            <input
              type="checkbox"
              id="is_adaptive_edit"
              checked={formData.is_adaptive}
              onChange={(e) => setFormData({...formData, is_adaptive: e.target.checked})}
              className="mr-2"
            />
            <label htmlFor="is_adaptive_edit" className="text-sm text-gray-700">
              Parcours adaptatif
            </label>
          </div>
          
          <div className="flex space-x-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
            >
              Annuler
            </button>
            <button
              type="submit"
              className="flex-1 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
            >
              <Save className="w-4 h-4 inline mr-2" />
              Sauvegarder
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

// Composant Modal de Détails de Classe
function ClassDetailsModal({ classData, students, onClose, token }: any) {
  const [showAddStudent, setShowAddStudent] = useState(false);
  const [newStudentId, setNewStudentId] = useState('');

  const handleAddStudent = async () => {
    if (!newStudentId) return;
    
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/teacher/classes/${classData.id}/students/${newStudentId}`, {
        method: 'POST',
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        setShowAddStudent(false);
        setNewStudentId('');
        // Recharger les étudiants
        window.location.reload();
      }
    } catch (err) {
      console.error('Erreur lors de l\'ajout de l\'étudiant:', err);
    }
  };

  const handleRemoveStudent = async (studentId: number) => {
    if (!confirm('Êtes-vous sûr de vouloir retirer cet étudiant ?')) return;
    
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/teacher/classes/${classData.id}/students/${studentId}`, {
        method: 'DELETE',
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        // Recharger les étudiants
        window.location.reload();
      }
    } catch (err) {
      console.error('Erreur lors du retrait de l\'étudiant:', err);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-4xl max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold">Détails de la Classe: {classData.name}</h3>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
            <X className="w-5 h-5" />
          </button>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Informations de la classe */}
          <div>
            <h4 className="text-md font-semibold mb-3">Informations de la Classe</h4>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-gray-600">Description:</span>
                <span>{classData.description || 'Aucune description'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Niveau:</span>
                <span>{classData.level}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Matière:</span>
                <span>{classData.subject || 'Non spécifiée'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Progression moyenne:</span>
                <span>{Math.round(classData.average_progress)}%</span>
              </div>
            </div>
          </div>
          
          {/* Gestion des étudiants */}
          <div>
            <div className="flex justify-between items-center mb-3">
              <h4 className="text-md font-semibold">Étudiants ({students.length})</h4>
              <button
                onClick={() => setShowAddStudent(true)}
                className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700"
              >
                <UserPlus className="w-4 h-4 inline mr-1" />
                Ajouter
              </button>
            </div>
            
            <div className="space-y-2 max-h-64 overflow-y-auto">
              {students.map((student: any) => (
                <div key={student.student_id} className="flex justify-between items-center p-2 bg-gray-50 rounded">
                  <div>
                    <div className="font-medium">{student.username}</div>
                    <div className="text-sm text-gray-600">Progression: {Math.round(student.progress_percentage)}%</div>
                  </div>
                  <button
                    onClick={() => handleRemoveStudent(student.student_id)}
                    className="text-red-600 hover:text-red-800"
                  >
                    <UserMinus className="w-4 h-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
        
        {/* Modal d'ajout d'étudiant */}
        {showAddStudent && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-60">
            <div className="bg-white rounded-lg p-4 w-full max-w-sm">
              <h5 className="text-md font-semibold mb-3">Ajouter un Étudiant</h5>
              <div className="space-y-3">
                <input
                  type="number"
                  placeholder="ID de l'étudiant"
                  value={newStudentId}
                  onChange={(e) => setNewStudentId(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                />
                <div className="flex space-x-2">
                  <button
                    onClick={() => setShowAddStudent(false)}
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md"
                  >
                    Annuler
                  </button>
                  <button
                    onClick={handleAddStudent}
                    className="flex-1 px-3 py-2 bg-blue-600 text-white rounded-md"
                  >
                    Ajouter
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
        
        <div className="mt-6 pt-4 border-t border-gray-200">
          <button
            onClick={onClose}
            className="w-full px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700"
          >
            Fermer
          </button>
        </div>
      </div>
    </div>
  );
} 