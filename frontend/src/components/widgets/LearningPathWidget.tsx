'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '../../hooks/useAuth';
import { BookOpen, CheckCircle, Clock, TrendingUp, Play, Target, Award, MapPin, AlertCircle, RefreshCw } from 'lucide-react';
import SimpleIcon, { SimpleIconWithBackground } from '../ui/SimpleIcon';

interface LearningPath {
  id: number;
  title: string;
  subject: string;
  progress: number;
  current_step: number;
  total_steps: number;
  started_at: string;
  is_completed: boolean;
  difficulty: string;
  estimated_duration: number;
}

interface LearningPathStep {
  id: number;
  step_number: number;
  title: string;
  description: string;
  content_type: 'quiz' | 'content' | 'exercise' | 'assessment';
  estimated_duration: number;
  is_required: boolean;
  is_active: boolean;
  is_completed?: boolean;
}

interface LearningPathProgress {
  learning_path_id: number;
  student_id: number;
  current_step: number;
  total_steps: number;
  progress_percentage: number;
  performance_score: number;
  last_activity: string;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function LearningPathWidget({ className = '' }: { className?: string }) {
  const { user, token } = useAuth();
  const [learningPaths, setLearningPaths] = useState<LearningPath[]>([]);
  const [activePaths, setActivePaths] = useState<LearningPath[]>([]);
  const [completedPaths, setCompletedPaths] = useState<LearningPath[]>([]);
  const [selectedPath, setSelectedPath] = useState<LearningPath | null>(null);
  const [pathSteps, setPathSteps] = useState<LearningPathStep[]>([]);
  const [pathProgress, setPathProgress] = useState<LearningPathProgress | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showPathDetails, setShowPathDetails] = useState(false);
  const [averageProgress, setAverageProgress] = useState<number>(0);

  useEffect(() => {
    if (user?.id && token) {
      console.log('[LearningPathWidget] 🔐 Authentification OK:', { userId: user.id, hasToken: !!token });
      loadLearningPaths();
    } else {
      console.log('[LearningPathWidget] ❌ Authentification manquante:', { user: user?.id, hasToken: !!token });
    }
  }, [user?.id, token]);

  const loadLearningPaths = async () => {
    try {
      setLoading(true);
      setError(null);

      console.log('[LearningPathWidget] 📡 Chargement des parcours pour l\'utilisateur:', user?.id);

      // Appels parallèles pour récupérer les parcours d'apprentissage
      const [learningPathsRes] = await Promise.all([
        fetch(`${API_BASE_URL}/api/v1/student_learning_paths/student/${user?.id}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        })
      ]);

      console.log('[LearningPathWidget] 📊 Réponses API:', { 
        learningPathsStatus: learningPathsRes.status
      });

      if (learningPathsRes.ok) {
        const learningPathsData = await learningPathsRes.json();
        console.log('[LearningPathWidget] ✅ Parcours d\'apprentissage récupérés:', learningPathsData);
        
        // Traiter les données des parcours
        const allPaths = learningPathsData.learning_paths || learningPathsData || [];
        
        // Séparer les parcours actifs et terminés
        const active = allPaths.filter((path: any) => !path.is_completed);
        const completed = allPaths.filter((path: any) => path.is_completed);
        
        setActivePaths(active);
        setCompletedPaths(completed);
        setLearningPaths(allPaths);
        
        // Calculer la progression moyenne
        if (allPaths.length > 0) {
          const totalProgress = allPaths.reduce((sum: number, path: any) => sum + (path.progress || 0), 0);
          const averageProgress = totalProgress / allPaths.length;
          setAverageProgress(Math.round(averageProgress));
        }
      } else {
        console.log('[LearningPathWidget] ❌ Erreur parcours d\'apprentissage:', learningPathsRes.status, learningPathsRes.statusText);
        // En cas d'erreur, vider les listes
        setActivePaths([]);
        setCompletedPaths([]);
        setLearningPaths([]);
        setAverageProgress(0);
      }
    } catch (err) {
      console.error('[LearningPathWidget] 💥 Erreur lors du chargement des parcours:', err);
      setError('Erreur lors du chargement des parcours');
      // En cas d'erreur, vider les listes
      setActivePaths([]);
      setCompletedPaths([]);
      setLearningPaths([]);
    } finally {
      setLoading(false);
    }
  };

  // Fonction de rechargement forcé
  const forceRefresh = () => {
    console.log('[LearningPathWidget] 🔄 Rechargement forcé des parcours');
    setError(null);
    loadLearningPaths();
  };

  const startLearningPath = async (path: LearningPath) => {
    try {
      setError(null);

      console.log('[LearningPathWidget] 🚀 Démarrage du parcours:', path.id);

      const response = await fetch(`${API_BASE_URL}/api/v1/learning_paths/${path.id}/start`, {
        method: 'POST',
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error('Erreur lors du démarrage du parcours');
      }

      // Recharger les parcours
      await loadLearningPaths();
      console.log('[LearningPathWidget] ✅ Parcours démarré:', path.title);
    } catch (err) {
      console.error('[LearningPathWidget] 💥 Erreur lors du démarrage du parcours:', err);
      setError('Erreur lors du démarrage du parcours');
    }
  };

  const viewPathDetails = async (path: LearningPath) => {
    try {
      setError(null);
      setSelectedPath(path);

      console.log('[LearningPathWidget] 📊 Affichage des détails pour:', path.id);

      // Récupérer les étapes du parcours
      const stepsResponse = await fetch(`${API_BASE_URL}/api/v1/learning_paths/${path.id}/steps`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (stepsResponse.ok) {
        const stepsData = await stepsResponse.json();
        console.log('[LearningPathWidget] ✅ Étapes récupérées:', stepsData);
        setPathSteps(stepsData.steps || []);
      }

      // Récupérer la progression du parcours
      const progressResponse = await fetch(`${API_BASE_URL}/api/v1/learning_paths/${path.id}/progress`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (progressResponse.ok) {
        const progressData = await progressResponse.json();
        console.log('[LearningPathWidget] ✅ Progression récupérée:', progressData);
        setPathProgress(progressData);
      }

      setShowPathDetails(true);
    } catch (err) {
      console.error('[LearningPathWidget] 💥 Erreur lors de la récupération des détails:', err);
      setError('Erreur lors de la récupération des détails');
    }
  };

  const completeStep = async (stepId: number) => {
    try {
      setError(null);

      console.log('[LearningPathWidget] ✅ Complétion de l\'étape:', stepId);

      const response = await fetch(`${API_BASE_URL}/api/v1/learning_paths/${selectedPath?.id}/complete-step`, {
        method: 'POST',
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          step_id: stepId,
          completion_date: new Date().toISOString()
        })
      });

      if (!response.ok) {
        throw new Error('Erreur lors de la complétion de l\'étape');
      }

      // Recharger les détails du parcours
      if (selectedPath) {
        await viewPathDetails(selectedPath);
      }
    } catch (err) {
      console.error('[LearningPathWidget] 💥 Erreur lors de la complétion de l\'étape:', err);
      setError('Erreur lors de la complétion de l\'étape');
    }
  };

  const getContentTypeIcon = (contentType: string) => {
    switch (contentType) {
      case 'quiz':
        return <Target className="w-4 h-4 text-blue-500" />;
      case 'content':
        return <BookOpen className="w-4 h-4 text-green-500" />;
      case 'exercise':
        return <TrendingUp className="w-4 h-4 text-purple-500" />;
      case 'assessment':
        return <Award className="w-4 h-4 text-orange-500" />;
      default:
        return <BookOpen className="w-4 h-4 text-gray-500" />;
    }
  };

  const getContentTypeLabel = (contentType: string) => {
    switch (contentType) {
      case 'quiz':
        return 'Quiz';
      case 'content':
        return 'Contenu';
      case 'exercise':
        return 'Exercice';
      case 'assessment':
        return 'Évaluation';
      default:
        return 'Contenu';
    }
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty.toLowerCase()) {
      case 'easy':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'hard':
        return 'bg-red-100 text-red-800 border-red-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  if (loading) {
    return (
      <div className={`card-unified ${className}`}>
        <div className="card-unified-header">
          <div className="flex items-center gap-3">
            <SimpleIconWithBackground name="book-open" backgroundType="info" size="lg" />
            <h3 className="text-lg font-semibold">Parcours d'Apprentissage</h3>
          </div>
        </div>
        <div className="card-unified-body">
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
            <span className="ml-3 text-muted">Chargement des parcours...</span>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`card-unified ${className}`}>
        <div className="card-unified-header">
          <div className="flex items-center gap-3">
            <SimpleIconWithBackground name="book-open" backgroundType="info" size="lg" />
            <h3 className="text-lg font-semibold">Parcours d'Apprentissage</h3>
          </div>
        </div>
        <div className="card-unified-body">
          <div className="flex items-center justify-center py-8 text-danger">
            <AlertCircle className="w-5 h-5 mr-2" />
            {error}
          </div>
          <div className="flex justify-center mt-4">
            <button
              onClick={forceRefresh}
              className="btn-unified btn-unified-primary flex items-center gap-2"
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
    <div className={`space-y-6 ${className}`}>
      {/* En-tête du widget */}
      <div className="card-unified">
        <div className="card-unified-header">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <SimpleIconWithBackground name="book-open" backgroundType="info" size="lg" />
              <h3 className="text-lg font-semibold">Parcours d'Apprentissage</h3>
            </div>
            <button
              onClick={forceRefresh}
              className="btn-unified btn-unified-secondary flex items-center gap-2"
              title="Recharger les données"
            >
              <RefreshCw className="w-4 h-4" />
              Actualiser
            </button>
          </div>
        </div>
                 <div className="card-unified-body max-h-96 overflow-hidden">
           <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="text-center p-4 bg-blue-50 rounded-lg border border-blue-200">
              <div className="text-2xl font-bold text-blue-600">{activePaths.length}</div>
              <div className="text-sm text-blue-600">En cours</div>
            </div>
            <div className="text-center p-4 bg-green-50 rounded-lg border border-green-200">
              <div className="text-2xl font-bold text-green-600">{completedPaths.length}</div>
              <div className="text-sm text-green-600">Terminés</div>
            </div>
                         <div className="text-center p-4 bg-purple-50 rounded-lg border border-purple-200">
               <div className="text-2xl font-bold text-purple-600">
                 {(() => {
                   const totalProgress = activePaths.reduce((total, path) => total + (path.progress || 0), 0);
                   const avgProgress = activePaths.length > 0 ? totalProgress / activePaths.length : 0;
                   return isNaN(avgProgress) ? '0%' : `${Math.round(avgProgress)}%`;
                 })()}
               </div>
               <div className="text-sm text-purple-600">Progression moyenne</div>
             </div>
          </div>

                     {/* Parcours actifs */}
           {activePaths.length > 0 && (
             <div className="space-y-4">
               <h4 className="font-semibold text-primary flex items-center gap-2">
                 <Play className="w-4 h-4" />
                 Parcours en cours
               </h4>
               <div className="space-y-3 max-h-48 overflow-y-auto pr-2">
                {activePaths.map((path) => (
                  <div key={path.id} className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex-1">
                        <h5 className="font-semibold text-primary">{path.title}</h5>
                        <p className="text-sm text-secondary mb-2">{path.subject}</p>
                        <div className="flex items-center gap-4 text-xs text-muted">
                          <span className={`px-2 py-1 rounded-full text-xs font-medium border ${getDifficultyColor(path.difficulty)}`}>
                            {path.difficulty}
                          </span>
                          <span className="flex items-center gap-1">
                            <Clock className="w-3 h-3" />
                            {path.estimated_duration} min
                          </span>
                          <span className="flex items-center gap-1">
                            <MapPin className="w-3 h-3" />
                            Étape {path.current_step}/{path.total_steps}
                          </span>
                        </div>
                      </div>
                                             <div className="text-right">
                         <div className="text-lg font-bold text-primary">
                           {isNaN(path.progress) || path.progress === null ? '0%' : `${Math.round(path.progress)}%`}
                         </div>
                         <div className="text-xs text-muted">Progression</div>
                       </div>
                    </div>
                    
                    {/* Barre de progression */}
                    <div className="w-full bg-gray-200 rounded-full h-2 mb-3">
                                           <div 
                       className="bg-gradient-to-r from-blue-500 to-purple-600 h-2 rounded-full transition-all duration-300"
                       style={{ width: `${isNaN(path.progress) || path.progress === null ? 0 : Math.max(0, Math.min(100, path.progress))}%` }}
                     ></div>
                    </div>
                    
                    <div className="flex gap-2">
                      <button
                        onClick={() => viewPathDetails(path)}
                        className="btn-unified btn-unified-secondary flex items-center gap-2"
                      >
                        <BookOpen className="w-4 h-4" />
                        Voir détails
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

                     {/* Parcours terminés */}
           {completedPaths.length > 0 && (
             <div className="space-y-4">
               <h4 className="font-semibold text-primary flex items-center gap-2">
                 <CheckCircle className="w-4 h-4" />
                 Parcours terminés
               </h4>
               <div className="space-y-3 max-h-32 overflow-y-auto pr-2">
                {completedPaths.slice(0, 3).map((path) => (
                  <div key={path.id} className="p-4 bg-green-50 rounded-lg border border-green-200">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <h5 className="font-semibold text-primary">{path.title}</h5>
                        <p className="text-sm text-secondary mb-2">{path.subject}</p>
                        <div className="flex items-center gap-4 text-xs text-muted">
                          <span className={`px-2 py-1 rounded-full text-xs font-medium border ${getDifficultyColor(path.difficulty)}`}>
                            {path.difficulty}
                          </span>
                          <span className="flex items-center gap-1">
                            <Award className="w-3 h-3" />
                            Terminé
                          </span>
                        </div>
                      </div>
                      <button
                        onClick={() => viewPathDetails(path)}
                        className="btn-unified btn-unified-secondary flex items-center gap-2"
                      >
                        <BookOpen className="w-4 h-4" />
                        Voir détails
                      </button>
                    </div>
                  </div>
                ))}
              </div>
              
              {completedPaths.length > 3 && (
                <div className="text-center">
                  <button className="text-primary hover:text-primary-600 text-sm font-medium">
                    Voir tous les parcours terminés ({completedPaths.length})
                  </button>
                </div>
              )}
            </div>
          )}

                     {/* Aucun parcours */}
           {learningPaths.length === 0 && (
             <div className="text-center py-4">
              <BookOpen className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <p className="text-lg font-semibold text-gray-600 mb-2">Aucun parcours disponible</p>
              <p className="text-base text-gray-400">Vos professeurs vous assigneront des parcours d'apprentissage bientôt.</p>
              <button
                onClick={forceRefresh}
                className="btn-unified btn-unified-primary mt-4 flex items-center gap-2 mx-auto"
              >
                <RefreshCw className="w-4 h-4" />
                Actualiser
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Modal des détails du parcours */}
      {showPathDetails && selectedPath && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-4xl w-full mx-4 max-h-[80vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-bold text-primary">Détails du parcours : {selectedPath.title}</h3>
              <button
                onClick={() => setShowPathDetails(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                ✕
              </button>
            </div>
            
            <div className="space-y-6">
              {/* Informations générales */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 p-4 bg-gray-50 rounded-lg">
                <div className="text-center">
                  <div className="text-2xl font-bold text-primary">{selectedPath.subject}</div>
                  <div className="text-sm text-muted">Matière</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-primary">{selectedPath.difficulty}</div>
                  <div className="text-sm text-muted">Difficulté</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-primary">{selectedPath.estimated_duration} min</div>
                  <div className="text-sm text-muted">Durée estimée</div>
                </div>
              </div>

              {/* Progression globale */}
              {pathProgress && (
                <div className="p-4 bg-blue-50 rounded-lg">
                  <h4 className="font-semibold text-primary mb-3">Progression globale</h4>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-muted">Étape {pathProgress.current_step} sur {pathProgress.total_steps}</span>
                    <span className="text-lg font-bold text-primary">{Math.round(pathProgress.progress_percentage)}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div 
                      className="bg-gradient-to-r from-blue-500 to-purple-600 h-3 rounded-full transition-all duration-300"
                      style={{ width: `${pathProgress.progress_percentage}%` }}
                    ></div>
                  </div>
                </div>
              )}

              {/* Étapes du parcours */}
              <div>
                <h4 className="font-semibold text-primary mb-3">Étapes du parcours</h4>
                <div className="space-y-3">
                  {pathSteps.map((step, index) => (
                    <div 
                      key={step.id} 
                      className={`p-4 rounded-lg border-2 transition-all duration-300 ${
                        step.is_completed 
                          ? 'bg-green-50 border-green-200' 
                          : index === (selectedPath.current_step - 1)
                          ? 'bg-blue-50 border-blue-200'
                          : 'bg-gray-50 border-gray-200'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                            step.is_completed 
                              ? 'bg-green-500 text-white' 
                              : index === (selectedPath.current_step - 1)
                              ? 'bg-blue-500 text-white'
                              : 'bg-gray-300 text-gray-600'
                          }`}>
                            {step.is_completed ? (
                              <CheckCircle className="w-4 h-4" />
                            ) : (
                              <span className="text-sm font-bold">{step.step_number}</span>
                            )}
                          </div>
                          <div className="flex-1">
                            <h5 className={`font-semibold ${
                              step.is_completed 
                                ? 'text-green-700' 
                                : index === (selectedPath.current_step - 1)
                                ? 'text-blue-700'
                                : 'text-gray-600'
                            }`}>
                              {step.title}
                            </h5>
                            <p className="text-sm text-muted mb-2">{step.description}</p>
                            <div className="flex items-center gap-4 text-xs text-muted">
                              <span className="flex items-center gap-1">
                                {getContentTypeIcon(step.content_type)}
                                {getContentTypeLabel(step.content_type)}
                              </span>
                              <span className="flex items-center gap-1">
                                <Clock className="w-3 h-3" />
                                {step.estimated_duration} min
                              </span>
                              {step.is_required && (
                                <span className="px-2 py-1 bg-red-100 text-red-800 text-xs rounded-full">
                                  Obligatoire
                                </span>
                              )}
                            </div>
                          </div>
                        </div>
                        
                        {!step.is_completed && index === (selectedPath.current_step - 1) && (
                          <button
                            onClick={() => completeStep(step.id)}
                            className="btn-unified btn-unified-primary flex items-center gap-2"
                          >
                            <CheckCircle className="w-4 h-4" />
                            Terminer
                          </button>
                        )}
                        
                        {step.is_completed && (
                          <span className="px-3 py-1 bg-green-100 text-green-800 text-xs rounded-full font-medium">
                            Terminé
                          </span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="mt-6 flex justify-end">
              <button
                onClick={() => setShowPathDetails(false)}
                className="btn-unified btn-unified-primary"
              >
                Fermer
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}







