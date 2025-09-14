"use client";
import React, { useState, useEffect } from 'react';
import { useAuth } from '../../../../hooks/useAuth';
import { useRouter } from 'next/navigation';
import { Card } from '../../../../components/Card';
import Button from '../../../../components/Button';
import { StudentProfile } from '../../../../services/adaptiveLearningService';
import { CognitiveDiagnosticService, CognitiveProfile, GapAnalysis, RemediationPlan } from '../../../../services/cognitiveDiagnosticService';
import { 
  Map, 
  Target, 
  CheckCircle, 
  Clock, 
  Star, 
  TrendingUp,
  BookOpen,
  Video,
  FileText,
  Award,
  Users,
  Calendar,
  ArrowRight,
  Play,
  Pause,
  Lock,
  Unlock,
  BarChart3,
  Lightbulb,
  Bookmark,
  Share2,
  Brain,
  Zap,
  Activity
} from 'lucide-react';
import Sidebar from '../../../../components/Sidebar';

interface LearningPath {
  id: number;
  title: string;
  description: string;
  subject: string;
  level: string;
  difficulty: string;
  estimated_duration: number;
  is_followed: boolean;
  progress?: number;
  is_completed?: boolean;
  started_at?: string;
  current_step?: number;
  total_steps?: number;
  // Propriétés optionnelles qui peuvent ne pas être présentes
  category?: string;
  steps?: LearningStep[];
  rating?: number;
  enrolled_students?: number;
  created_by?: string;
  created_at?: string;
  tags?: string[];
  prerequisites?: string[];
  outcomes?: string[];
  is_enrolled?: boolean;
}

interface LearningStep {
  id: number;
  title: string;
  description: string;
  type: 'video' | 'reading' | 'quiz' | 'project' | 'assignment';
  duration: number; // en minutes
  is_completed: boolean;
  is_locked: boolean;
  resources: Resource[];
  estimated_time: number;
  difficulty: 'easy' | 'medium' | 'hard';
}

interface Resource {
  id: number;
  title: string;
  type: 'video' | 'pdf' | 'link' | 'quiz';
  url: string;
  duration?: number;
  is_completed: boolean;
}

const LearningPathPage: React.FC = () => {
  const { user, token } = useAuth();
  const router = useRouter();
  const [learningPaths, setLearningPaths] = useState<LearningPath[]>([]);
  const [selectedPath, setSelectedPath] = useState<LearningPath | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<'all' | 'enrolled' | 'completed' | 'recommended'>('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [showPathDetails, setShowPathDetails] = useState(false);
  const [currentStep, setCurrentStep] = useState<LearningStep | null>(null);
  const [studentProfile, setStudentProfile] = useState<StudentProfile | null>(null);

  // États pour le diagnostic cognitif avancé
  const [cognitiveProfile, setCognitiveProfile] = useState<CognitiveProfile | null>(null);
  const [gapAnalysis, setGapAnalysis] = useState<GapAnalysis | null>(null);
  const [remediationPlan, setRemediationPlan] = useState<RemediationPlan | null>(null);
  const [isAnalyzingGaps, setIsAnalyzingGaps] = useState(false);
  const [isGeneratingRemediation, setIsGeneratingRemediation] = useState(false);
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [isGeneratingPath, setIsGeneratingPath] = useState(false);
  const [remediationProgress, setRemediationProgress] = useState(0);
  const [realRemediationProgress, setRealRemediationProgress] = useState(0);

  useEffect(() => {
    const fetchLearningPaths = async () => {
      try {
        const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
        const response = await fetch(`${API_BASE_URL}/api/v1/student_learning_paths/student/${user?.id}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.ok) {
          const data = await response.json();
          console.log('Parcours reçus:', data);
          setLearningPaths(data.learning_paths || []);
        } else if (response.status === 401) {
          console.warn('Token expiré, aucun parcours disponible');
          setLearningPaths([]);
        } else {
          console.error('Erreur API:', response.status, response.statusText);
        }
      } catch (error) {
        console.error('Erreur lors du chargement des parcours:', error);
        setLearningPaths([]);
      } finally {
        setLoading(false);
      }
     };

         const fetchCognitiveDiagnostic = async () => {
      try {
        if (user) {
          const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
          
          // Charger le profil cognitif avancé (version test sans auth)
          const cognitiveResponse = await fetch(`${API_BASE_URL}/api/v1/cognitive_diagnostic/student/${user.id}/cognitive-profile-test`);
          if (cognitiveResponse.ok) {
            const cognitive = await cognitiveResponse.json();
            setCognitiveProfile(cognitive);
          }
          
          // Analyser les lacunes d'apprentissage (version test sans auth)
          const gapsResponse = await fetch(`${API_BASE_URL}/api/v1/gap_analysis/student/${user.id}/analyze-test`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ subject: 'Français' })
          });
          if (gapsResponse.ok) {
            const gaps = await gapsResponse.json();
            setGapAnalysis(gaps);
          }
          
          // Générer le plan de remédiation (version test sans auth)
          const remediationResponse = await fetch(`${API_BASE_URL}/api/v1/remediation/student/${user.id}/plan-test`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ subject: 'Français' })
          });
          if (remediationResponse.ok) {
            const remediation = await remediationResponse.json();
            setRemediationPlan(remediation);
            
            console.log('🔍 [DEBUG] Données remédiation reçues:', remediation);
            
            // Mettre à jour la progression des exercices de remédiation
            if (remediation.progress !== undefined) {
              setRemediationProgress(remediation.progress);
              console.log('🔍 [DEBUG] Progression remédiation définie:', remediation.progress);
            } else {
              console.log('⚠️ [DEBUG] Pas de progression dans les données remédiation');
              // Essayer de calculer la progression à partir des étapes
              if (remediation.plan_steps && remediation.current_step) {
                const calculatedProgress = Math.round((remediation.current_step / remediation.plan_steps.length) * 100);
                setRemediationProgress(calculatedProgress);
                console.log('🔍 [DEBUG] Progression calculée à partir des étapes:', calculatedProgress);
              }
            }
          }
        }
      } catch (error) {
        console.error('Erreur lors du chargement du diagnostic cognitif:', error);
        // En cas d'erreur, on ne charge rien - pas de données par défaut
        setCognitiveProfile(null);
        setGapAnalysis(null);
        setRemediationPlan(null);
      }
    };

         const fetchStudentProfile = async () => {
      try {
        if (user) {
          const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
          const response = await fetch(`${API_BASE_URL}/api/v1/french/initial-assessment/student/${user.id}/profile-test`);
          
          if (response.ok) {
            const profile = await response.json();
            setStudentProfile(profile);
          } else {
            console.warn('Profil étudiant non trouvé');
            setStudentProfile(null);
          }
        }
      } catch (error) {
        console.error('Erreur lors du chargement du profil étudiant:', error);
        setStudentProfile(null);
      }
    };

           const fetchRecommendations = async () => {
    try {
      if (user) {
        const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
        const response = await fetch(`${API_BASE_URL}/api/v1/french/recommendations/student/${user.id}/test`);
        
        // Récupérer la vraie progression des exercices de remédiation
        try {
          const remediationResultsResponse = await fetch(`${API_BASE_URL}/api/v1/remediation/results/student/${user.id}`, {
            headers: { 'Authorization': `Bearer ${token}` }
          });
          
          if (remediationResultsResponse.ok) {
            const remediationResults = await remediationResultsResponse.json();
            console.log('🔍 [DEBUG] Résultats remédiation réels:', remediationResults);
            
            if (remediationResults.length > 0) {
              // Calculer la progression basée sur les résultats réels
              const totalScore = remediationResults.reduce((sum, result) => sum + (result.score || 0), 0);
              const totalMaxScore = remediationResults.reduce((sum, result) => sum + (result.max_score || 0), 0);
              
              if (totalMaxScore > 0) {
                const realProgress = Math.round((totalScore / totalMaxScore) * 100);
                setRealRemediationProgress(realProgress);
                console.log('🔍 [DEBUG] Progression réelle calculée:', realProgress, '%');
              }
            }
          }
        } catch (error) {
          console.warn('⚠️ [DEBUG] Erreur récupération progression réelle:', error);
        }
          
          if (response.ok) {
            const data = await response.json();
            setRecommendations(data.recommendations || []);
          } else {
            console.warn('Recommandations non trouvées');
            setRecommendations([]);
          }
        }
      } catch (error) {
        console.error('Erreur lors du chargement des recommandations:', error);
        setRecommendations([]);
      }
    };

    if (user) {
      fetchLearningPaths();
      fetchCognitiveDiagnostic();
      fetchStudentProfile();
      fetchRecommendations();
    }
  }, [user, token]);

  const handlePathSelect = (path: LearningPath) => {
    setSelectedPath(path);
    setShowPathDetails(true);
  };

  const handleStepComplete = async (stepId: number) => {
    try {
      const response = await fetch(`/api/v1/learning_steps/${stepId}/complete`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (response.ok) {
        // Mettre à jour l'état local
        setSelectedPath(prev => prev ? {
          ...prev,
          steps: prev.steps.map(step => 
            step.id === stepId ? { ...step, is_completed: true } : step
          ),
          progress: calculateProgress(prev.steps.map(step => 
            step.id === stepId ? { ...step, is_completed: true } : step
          ))
        } : null);
      }
    } catch (error) {
      console.error('Erreur lors de la complétion de l\'étape:', error);
    }
  };

  const handleEnrollPath = async (pathId: number) => {
    try {
      const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const response = await fetch(`${API_BASE_URL}/api/v1/student_learning_paths/${pathId}/start`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
             if (response.ok) {
         setLearningPaths(prev => prev.map(path => 
           path.id === pathId ? { ...path, is_followed: true } : path
         ));
       }
    } catch (error) {
      console.error('Erreur lors de l\'inscription:', error);
    }
  };

  const handleGenerateAdaptivePath = async (subject: string) => {
    if (!user || !token) return;
    
    setIsGeneratingPath(true);
    try {
      // Pour l'instant, on simule la génération d'un parcours
      const newPath: LearningPath = {
        id: Date.now(), // ID temporaire
        title: `Parcours ${subject} personnalisé`,
        description: `Parcours adaptatif généré pour ${subject}`,
        subject: subject,
        level: 'beginner',
        difficulty: 'easy',
        estimated_duration: 30,
        is_followed: true,
        progress: 0,
        is_completed: false,
        started_at: new Date().toISOString(),
        current_step: 1,
        total_steps: 5
      };
      
      // Ajouter le nouveau parcours à la liste
      setLearningPaths(prev => [...prev, newPath]);
      
    } catch (error) {
      console.error('Erreur lors de la génération du parcours adaptatif:', error);
    } finally {
      setIsGeneratingPath(false);
    }
  };

  const handleStartAdaptiveQuiz = async () => {
    console.log('🔍 [DEBUG] handleStartAdaptiveQuiz appelée');
    console.log('🔍 [DEBUG] User:', user);
    console.log('🔍 [DEBUG] Token:', token ? 'Présent' : 'Absent');
    
    if (!user || !token) {
      console.log('❌ [DEBUG] Utilisateur non connecté ou token manquant');
      alert('Vous devez être connecté pour commencer un quiz');
      return;
    }

    console.log('✅ [DEBUG] Utilisateur connecté, début de la création du quiz');
    console.log('🔍 [DEBUG] User ID:', user.id);
    console.log('🔍 [DEBUG] User Role:', user.role);

    try {
      // Créer un quiz adaptatif pour l'étudiant
      const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const requestBody = {
        subject: 'Français',
        difficulty_level: 5,
        num_questions: 10
      };
      
      console.log('🔍 [DEBUG] API_BASE_URL:', API_BASE_URL);
      console.log('🔍 [DEBUG] Endpoint:', `${API_BASE_URL}/api/v1/adaptive-evaluation/generate-test/${user.id}`);
      console.log('🔍 [DEBUG] Request Body:', requestBody);
      console.log('🔍 [DEBUG] Headers:', {
        'Authorization': `Bearer ${token.substring(0, 20)}...`,
        'Content-Type': 'application/json'
      });
      
      console.log('🚀 [DEBUG] Envoi de la requête fetch...');
      
      const response = await fetch(`${API_BASE_URL}/api/v1/adaptive-evaluation/generate-test/${user.id}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      });

      console.log('📡 [DEBUG] Réponse reçue:', response);
      console.log('📡 [DEBUG] Status:', response.status);
      console.log('📡 [DEBUG] Status Text:', response.statusText);
      console.log('📡 [DEBUG] Headers:', Object.fromEntries(response.headers.entries()));

      if (response.ok) {
        console.log('✅ [DEBUG] Réponse OK, parsing du JSON...');
        const quizData = await response.json();
        console.log('🎉 [DEBUG] Quiz adaptatif créé avec succès:', quizData);
        console.log('🔍 [DEBUG] Test ID:', quizData.test_id);
        console.log('🔍 [DEBUG] Titre:', quizData.title);
        
        console.log('🔄 [DEBUG] Redirection vers:', `/dashboard/student/quiz/${quizData.test_id}`);
        // Rediriger vers le quiz avec l'ID généré
        router.push(`/dashboard/student/quiz/${quizData.test_id}`);
      } else {
        console.log('❌ [DEBUG] Réponse non OK, parsing de l\'erreur...');
        const errorData = await response.json();
        console.error('❌ [DEBUG] Erreur lors de la création du quiz:', errorData);
        console.error('❌ [DEBUG] Status:', response.status);
        console.error('❌ [DEBUG] Status Text:', response.statusText);
        alert('Erreur lors de la création du quiz adaptatif');
      }
    } catch (error) {
      console.error('💥 [DEBUG] Exception lors de la création du quiz:', error);
      console.error('💥 [DEBUG] Type d\'erreur:', typeof error);
      console.error('💥 [DEBUG] Message d\'erreur:', error.message);
      console.error('💥 [DEBUG] Stack trace:', error.stack);
      alert('Erreur lors de la création du quiz adaptatif');
    }
  };

  const calculateProgress = (steps: LearningStep[]) => {
    const completedSteps = steps.filter(step => step.is_completed).length;
    return steps.length > 0 ? (completedSteps / steps.length) * 100 : 0;
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return 'bg-green-100 text-green-800';
      case 'intermediate': return 'bg-yellow-100 text-yellow-800';
      case 'advanced': return 'bg-red-100 text-red-800';
      case 'easy': return 'bg-green-100 text-green-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'hard': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getStepIcon = (type: string) => {
    switch (type) {
      case 'video': return <Video className="w-5 h-5" />;
      case 'reading': return <FileText className="w-5 h-5" />;
      case 'quiz': return <BookOpen className="w-5 h-5" />;
      case 'project': return <Award className="w-5 h-5" />;
      case 'assignment': return <Target className="w-5 h-5" />;
      default: return <BookOpen className="w-5 h-5" />;
    }
  };

  const formatDuration = (minutes: number) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return hours > 0 ? `${hours}h ${mins}min` : `${mins}min`;
  };

  const filteredPaths = learningPaths.filter(path => {
    const matchesSearch = path.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         path.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         (path.tags && path.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase())));
    
    if (filter === 'enrolled') return matchesSearch && path.is_followed;
    if (filter === 'completed') return matchesSearch && (path.is_completed || path.progress === 100);
    if (filter === 'recommended') return matchesSearch && (!path.is_followed && path.progress === 0);
    
    return matchesSearch;
  });

  if (loading) {
    return (
      <div className="flex min-h-screen bg-gray-50">
        <Sidebar />
        <div className="flex-1 flex items-center justify-center ml-64">
          <div className="text-blue-600 animate-pulse text-xl font-bold">
            Chargement des parcours...
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 ml-64 overflow-y-auto">
        <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Parcours d'Apprentissage</h1>
          <p className="text-gray-600">Suivez des parcours structurés pour progresser efficacement</p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card>
            <div className="p-6 text-center">
              <Map className="w-8 h-8 text-blue-500 mx-auto mb-2" />
              <div className="text-2xl font-bold text-gray-900">{learningPaths.length}</div>
              <div className="text-sm text-gray-500">Parcours disponibles</div>
            </div>
          </Card>
          <Card>
            <div className="p-6 text-center">
              <Target className="w-8 h-8 text-green-500 mx-auto mb-2" />
              <div className="text-2xl font-bold text-gray-900">
                                 {learningPaths.filter(p => p.is_followed).length}
              </div>
              <div className="text-sm text-gray-500">Parcours suivis</div>
            </div>
          </Card>
          <Card>
            <div className="p-6 text-center">
              <CheckCircle className="w-8 h-8 text-purple-500 mx-auto mb-2" />
              <div className="text-2xl font-bold text-gray-900">
                                 {learningPaths.filter(p => p.is_completed || p.progress === 100).length}
              </div>
              <div className="text-sm text-gray-500">Parcours terminés</div>
            </div>
          </Card>
          <Card>
            <div className="p-6 text-center">
              <TrendingUp className="w-8 h-8 text-orange-500 mx-auto mb-2" />
              <div className="text-2xl font-bold text-gray-900">
                {(() => {
                  // Calculer la progression moyenne en incluant les exercices de remédiation
                  let totalProgress = 0;
                  let totalItems = 0;
                  
                  // Debug: Afficher les données disponibles
                  console.log('🔍 [DEBUG] Données pour calcul progression:', {
                    learningPaths: learningPaths.length,
                    learningPathsProgress: learningPaths.map(p => ({ id: p.id, progress: p.progress })),
                    remediationProgress,
                    gapAnalysis: gapAnalysis ? { overall_score: gapAnalysis.overall_score } : null
                  });
                  
                  // Progression des learning paths
                  if (learningPaths.length > 0) {
                    const pathsProgress = learningPaths.reduce((acc, p) => acc + (p.progress || 0), 0);
                    totalProgress += pathsProgress;
                    totalItems += learningPaths.length;
                    console.log('🔍 [DEBUG] Learning paths progress:', pathsProgress, 'items:', learningPaths.length);
                  }
                  
                  // Progression des exercices de remédiation
                  if (realRemediationProgress > 0) {
                    totalProgress += realRemediationProgress;
                    totalItems += 1;
                    console.log('🔍 [DEBUG] Progression réelle remédiation:', realRemediationProgress);
                  } else if (remediationProgress > 0) {
                    totalProgress += remediationProgress;
                    totalItems += 1;
                    console.log('🔍 [DEBUG] Progression plan remédiation:', remediationProgress);
                  }
                  
                  // Progression des quiz adaptatifs (si disponible)
                  if (gapAnalysis && gapAnalysis.overall_score !== undefined) {
                    totalProgress += gapAnalysis.overall_score;
                    totalItems += 1;
                    console.log('🔍 [DEBUG] Gap analysis score:', gapAnalysis.overall_score);
                  }
                  
                  console.log('🔍 [DEBUG] Total progress:', totalProgress, 'Total items:', totalItems);
                  
                  // Éviter la division par zéro
                  if (totalItems === 0) return '0%';
                  
                  const averageProgress = Math.round(totalProgress / totalItems);
                  console.log('🔍 [DEBUG] Average progress calculated:', averageProgress);
                  return isNaN(averageProgress) ? '0%' : `${averageProgress}%`;
                })()}
              </div>
              <div className="text-sm text-gray-500">Progression moyenne</div>
            </div>
          </Card>
        </div>

        {/* Profil d'apprentissage et recommandations - Seulement si données réelles */}
        {studentProfile && (
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Votre Profil d'Apprentissage</h2>
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Profil cognitif */}
              <Card>
                <div className="p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                    <Lightbulb className="w-5 h-5 text-blue-500 mr-2" />
                    Profil Cognitif
                  </h3>
                  {studentProfile ? (
                    <div className="space-y-3">
                      <div className="flex justify-between">
                        <span className="text-gray-600">Niveau Français:</span>
                        <span className="px-2 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">
                          {studentProfile.french_level || 'Non défini'}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Style d'apprentissage:</span>
                        <span className="px-2 py-1 bg-yellow-100 text-yellow-800 text-sm rounded-full">
                          {studentProfile.learning_style || 'Non défini'}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Type de mémoire:</span>
                        <span className="px-2 py-1 bg-purple-100 text-purple-800 text-sm rounded-full">
                          {studentProfile.cognitive_profile?.memory_type || 'Non défini'}
                        </span>
                      </div>
                    </div>
                  ) : (
                    <div className="text-center py-4">
                      <p className="text-gray-500">Aucun profil disponible</p>
                      <p className="text-sm text-gray-400">Complétez des quiz pour générer votre profil</p>
                    </div>
                  )}
                </div>
              </Card>

              {/* Forces et améliorations */}
              <Card>
                <div className="p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                    <Star className="w-5 h-5 text-green-500 mr-2" />
                    Vos Forces
                  </h3>
                  {studentProfile ? (
                    <div className="space-y-2">
                      {studentProfile.strengths && studentProfile.strengths.length > 0 ? (
                        studentProfile.strengths.map((strength, index) => (
                          <div key={index} className="flex items-center text-green-700">
                            <CheckCircle className="w-4 h-4 mr-2" />
                            {strength}
                          </div>
                        ))
                      ) : (
                        <div className="text-gray-500 text-sm">Aucune force identifiée</div>
                      )}
                    </div>
                  ) : (
                    <div className="text-center py-4">
                      <p className="text-gray-500">Données non disponibles</p>
                      <p className="text-sm text-gray-400">Complétez des quiz pour identifier vos forces</p>
                    </div>
                  )}
                </div>
              </Card>

              {/* Axes d'amélioration */}
              <Card>
                <div className="p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                    <Target className="w-5 h-5 text-orange-500 mr-2" />
                    Axes d'Amélioration
                  </h3>
                  {studentProfile ? (
                    <div className="space-y-2">
                      {studentProfile.areas_for_improvement && studentProfile.areas_for_improvement.length > 0 ? (
                        studentProfile.areas_for_improvement.map((area, index) => (
                          <div key={index} className="flex items-center text-orange-700">
                            <TrendingUp className="w-4 h-4 mr-2" />
                            {area}
                          </div>
                        ))
                      ) : (
                        <div className="text-gray-500 text-sm">Aucun axe d'amélioration identifié</div>
                      )}
                    </div>
                  ) : (
                    <div className="text-center py-4">
                      <p className="text-gray-500">Données non disponibles</p>
                      <p className="text-sm text-gray-400">Complétez des quiz pour identifier vos axes d'amélioration</p>
                    </div>
                  )}
                </div>
              </Card>
            </div>

                         {/* Recommandations personnalisées */}
             {recommendations && recommendations.length > 0 && (
               <div className="mt-6">
                 <h3 className="text-xl font-semibold text-gray-900 mb-4">Recommandations Personnalisées</h3>
                 <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                   {recommendations.slice(0, 6).map((rec, index) => (
                    <Card key={index} className="hover:shadow-lg transition-shadow">
                      <div className="p-4">
                        <h4 className="font-medium text-gray-900 mb-2">{rec.title}</h4>
                        <p className="text-sm text-gray-600 mb-3">{rec.description}</p>
                        <div className="flex items-center justify-between">
                          <span className="text-xs text-gray-500">{rec.type}</span>
                          <Button
                            size="sm"
                            onClick={() => handleGenerateAdaptivePath(rec.subject || 'Français')}
                            disabled={isGeneratingPath}
                            className="bg-blue-500 hover:bg-blue-600"
                          >
                            {isGeneratingPath ? 'Génération...' : 'Générer Parcours'}
                          </Button>
                        </div>
                      </div>
                    </Card>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Navigation vers les fonctionnalités avancées */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Fonctionnalités Avancées</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <Card className="hover:shadow-lg transition-shadow cursor-pointer">
              <div className="p-6 text-center">
                <Brain className="w-12 h-12 text-purple-500 mx-auto mb-3" />
                <h3 className="font-semibold text-gray-900 mb-2">Quiz Adaptatifs</h3>
                <p className="text-sm text-gray-600 mb-4">Testez vos connaissances avec des quiz qui s'adaptent à votre niveau</p>
                <Button
                  onClick={() => {
                    console.log('🔍 [DEBUG] Bouton "Commencer" cliqué');
                    console.log('🔍 [DEBUG] Appel de handleStartAdaptiveQuiz');
                    handleStartAdaptiveQuiz();
                  }}
                  className="w-full bg-purple-500 hover:bg-purple-600"
                  disabled={!user || !token}
                >
                  Commencer
                </Button>
              </div>
            </Card>

            <Card className="hover:shadow-lg transition-shadow cursor-pointer">
              <div className="p-6 text-center">
                <Target className="w-12 h-12 text-red-500 mx-auto mb-3" />
                <h3 className="font-semibold text-gray-900 mb-2">Analyse des Lacunes</h3>
                <p className="text-sm text-gray-600 mb-4">Identifiez vos points faibles et obtenez un plan de remédiation</p>
                <Button
                  onClick={() => window.location.href = '/dashboard/student/gap-analysis'}
                  className="w-full bg-red-500 hover:bg-red-600"
                >
                  Analyser
                </Button>
              </div>
            </Card>

            <Card className="hover:shadow-lg transition-shadow cursor-pointer">
              <div className="p-6 text-center">
                <CheckCircle className="w-12 h-12 text-green-500 mx-auto mb-3" />
                <h3 className="font-semibold text-gray-900 mb-2">Plan de Remédiation</h3>
                <p className="text-sm text-gray-600 mb-4">Suivez un plan personnalisé pour combler vos lacunes</p>
                <Button
                  onClick={() => window.location.href = '/dashboard/student/remediation'}
                  className="w-full bg-green-500 hover:bg-green-600"
                >
                  Suivre
                </Button>
              </div>
            </Card>

            <Card className="hover:shadow-lg transition-shadow cursor-pointer">
              <div className="p-6 text-center">
                <Zap className="w-12 h-12 text-yellow-500 mx-auto mb-3" />
                <h3 className="font-semibold text-gray-900 mb-2">IA Avancée</h3>
                <p className="text-sm text-gray-600 mb-4">Découvrez les insights intelligents de votre tuteur IA</p>
                <Button
                  onClick={() => window.location.href = '/dashboard/student/ai-advanced'}
                  className="w-full bg-yellow-500 hover:bg-yellow-600"
                >
                  Explorer
                </Button>
              </div>
            </Card>
          </div>
        </div>

        {/* Diagnostic Cognitif Avancé - Seulement si données réelles */}
        {cognitiveProfile && (
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Diagnostic Cognitif Avancé</h2>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Profil Cognitif Détaillé */}
              <Card>
                <div className="p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                    <Brain className="w-5 h-5 text-purple-500 mr-2" />
                    Profil Cognitif Détaillé
                  </h3>
                  <div className="space-y-4">
                    {/* Style d'apprentissage */}
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">Style d'Apprentissage Principal</h4>
                      <div className="flex items-center justify-between">
                        <span className="text-gray-600">{cognitiveProfile.learning_style.primary_style}</span>
                        <span className="px-2 py-1 bg-purple-100 text-purple-800 text-sm rounded-full">
                          {Math.round(cognitiveProfile.learning_style.confidence_score * 100)}% confiance
                        </span>
                      </div>
                    </div>

                    {/* Capacités cognitives */}
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">Capacités Cognitives</h4>
                      <div className="space-y-2">
                        {cognitiveProfile.cognitive_strengths && cognitiveProfile.cognitive_strengths.length > 0 ? (
                          cognitiveProfile.cognitive_strengths.map((strength, index) => (
                            <div key={index} className="flex items-center justify-between">
                              <span className="text-gray-600">{strength}</span>
                              <div className="flex items-center space-x-2">
                                <div className="w-20 bg-gray-200 rounded-full h-2">
                                  <div
                                    className="bg-blue-500 h-2 rounded-full"
                                    style={{ width: '100%' }}
                                  />
                                </div>
                                <span className="text-sm text-gray-500 w-8">100%</span>
                              </div>
                            </div>
                          ))
                        ) : (
                          <div className="text-gray-500 text-sm">Aucune capacité cognitive identifiée</div>
                        )}
                      </div>
                    </div>

                    {/* Préférences d'apprentissage */}
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">Préférences d'Apprentissage</h4>
                      <div className="space-y-2">
                        <div className="flex items-center justify-between">
                          <span className="text-gray-600">Style d'apprentissage</span>
                          <span className="px-2 py-1 bg-blue-100 text-blue-800 text-sm rounded-full capitalize">
                            {cognitiveProfile.learning_style}
                          </span>
                        </div>
                        <div className="flex items-center justify-between">
                          <span className="text-gray-600">Score de confiance</span>
                          <span className="px-2 py-1 bg-green-100 text-green-800 text-sm rounded-full">
                            {cognitiveProfile.confidence_score}/100
                          </span>
                        </div>
                        <div className="flex items-center justify-between">
                          <span className="text-gray-600">Total quiz</span>
                          <span className="px-2 py-1 bg-yellow-100 text-yellow-800 text-sm rounded-full">
                            {cognitiveProfile.total_quizzes}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </Card>

              {/* Analyse des Lacunes */}
              <Card>
                <div className="p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                    <Target className="w-5 h-5 text-red-500 mr-2" />
                    Analyse des Lacunes
                  </h3>
                  {gapAnalysis ? (
                    <div className="space-y-4">
                      <div className="flex items-center justify-between">
                        <span className="text-gray-600">Niveau de priorité</span>
                        <span className={`px-2 py-1 text-sm rounded-full ${
                          gapAnalysis.priority_level === 'high' ? 'bg-red-100 text-red-800' :
                          gapAnalysis.priority_level === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-green-100 text-green-800'
                        }`}>
                          {gapAnalysis.priority_level.toUpperCase()}
                        </span>
                      </div>
                      
                      <div className="space-y-3">
                        {gapAnalysis.identified_gaps.slice(0, 3).map((gap, index) => (
                          <div key={index} className="p-3 bg-gray-50 rounded-lg">
                            <div className="flex items-center justify-between mb-2">
                              <h5 className="font-medium text-gray-900">{gap.topic}</h5>
                              <span className={`px-2 py-1 text-xs rounded-full ${
                                gap.gap_size === 'large' ? 'bg-red-100 text-red-800' :
                                gap.gap_size === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                                'bg-green-100 text-green-800'
                              }`}>
                                {gap.gap_size}
                              </span>
                            </div>
                            <div className="text-sm text-gray-600">
                              <div className="flex justify-between mb-1">
                                <span>Niveau actuel: {gap.current_level}</span>
                                <span>Objectif: {gap.target_level}</span>
                              </div>
                              <div className="text-xs text-gray-500">
                                Impact: {gap.impact_score}/10
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>

                      <Button
                        onClick={() => setIsAnalyzingGaps(true)}
                        disabled={isAnalyzingGaps}
                        className="w-full bg-blue-500 hover:bg-blue-600"
                      >
                        {isAnalyzingGaps ? 'Analyse en cours...' : 'Analyser les Lacunes'}
                      </Button>
                    </div>
                  ) : (
                    <div className="text-center py-8">
                      <Target className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                      <p className="text-gray-500">Aucune analyse des lacunes disponible</p>
                      <Button
                        onClick={() => setIsAnalyzingGaps(true)}
                        disabled={isAnalyzingGaps}
                        className="mt-4 bg-blue-500 hover:bg-blue-600"
                      >
                        {isAnalyzingGaps ? 'Analyse en cours...' : 'Lancer l\'Analyse'}
                      </Button>
                    </div>
                  )}
                </div>
              </Card>
            </div>

            {/* Plan de Remédiation */}
            {remediationPlan && (
              <div className="mt-6">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">Plan de Remédiation Personnalisé</h3>
                <Card>
                  <div className="p-6">
                    <div className="flex items-center justify-between mb-4">
                      <div>
                        <h4 className="font-medium text-gray-900">Progression du Plan</h4>
                        <p className="text-sm text-gray-600">
                          {remediationPlan.current_step || 1} / {remediationPlan.plan_steps?.length || 0} étapes complétées
                        </p>
                      </div>
                      <div className="text-right">
                        <div className="text-2xl font-bold text-blue-600">
                          {Math.round(remediationPlan.progress || 0)}%
                        </div>
                        <div className="text-sm text-gray-500">Complété</div>
                      </div>
                    </div>

                    <div className="w-full bg-gray-200 rounded-full h-3 mb-6">
                      <div
                        className="bg-blue-500 h-3 rounded-full transition-all duration-300"
                        style={{ width: `${remediationPlan.progress || 0}%` }}
                      />
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                      {remediationPlan.plan_steps && remediationPlan.plan_steps.length > 0 ? (
                        remediationPlan.plan_steps.map((step, index) => (
                        <div
                          key={step.step_number}
                          className={`p-4 rounded-lg border ${
                            index < remediationPlan.current_step
                              ? 'bg-green-50 border-green-200'
                              : index === remediationPlan.current_step
                              ? 'bg-blue-50 border-blue-200'
                              : 'bg-gray-50 border-gray-200'
                          }`}
                        >
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-sm font-medium text-gray-900">
                              Étape {step.step_number}
                            </span>
                            {index < (remediationPlan.current_step || 1) && (
                              <CheckCircle className="w-4 h-4 text-green-500" />
                            )}
                          </div>
                          <h5 className="font-medium text-gray-900 mb-2">{step.topic}</h5>
                          <p className="text-sm text-gray-600 mb-3">{step.learning_objective}</p>
                          
                          <div className="flex items-center justify-between text-xs text-gray-500">
                            <span className="flex items-center">
                              <Clock className="w-3 h-3 mr-1" />
                              {step.estimated_duration} min
                            </span>
                            <span className="px-2 py-1 bg-gray-100 rounded-full">
                              {step.content_type}
                            </span>
                          </div>
                        </div>
                      ))
                      ) : (
                        <div className="col-span-full text-center py-8 text-gray-500">
                          Aucune étape de remédiation disponible
                        </div>
                      )}
                    </div>
                  </div>
                </Card>
              </div>
            )}
          </div>
        )}

        {/* Controls */}
        <div className="flex flex-col sm:flex-row gap-4 mb-6">
          <div className="flex-1">
            <div className="relative">
              <Map className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Rechercher un parcours..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
          <div className="flex gap-2">
            {['all', 'enrolled', 'completed', 'recommended'].map((filterType) => (
              <button
                key={filterType}
                onClick={() => setFilter(filterType as any)}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  filter === filterType
                    ? 'bg-blue-500 text-white'
                    : 'bg-white text-gray-700 hover:bg-gray-50'
                }`}
              >
                {filterType === 'all' && 'Tous'}
                {filterType === 'enrolled' && 'Suivis'}
                {filterType === 'completed' && 'Terminés'}
                {filterType === 'recommended' && 'Recommandés'}
              </button>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Liste des parcours */}
          <div className="lg:col-span-2">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {filteredPaths.map((path) => (
                <Card key={path.id} className="hover:shadow-lg transition-shadow cursor-pointer">
                  <div onClick={() => handlePathSelect(path)}>
                    {/* Header */}
                    <div className="p-6">
                      <div className="flex items-start justify-between mb-4">
                        <div className="flex-1">
                          <h3 className="font-bold text-lg text-gray-900 mb-2">{path.title}</h3>
                          <p className="text-sm text-gray-600 line-clamp-2 mb-3">{path.description}</p>
                        </div>
                                                 <div className="flex items-center space-x-1">
                           <Star className="w-4 h-4 text-yellow-400 fill-current" />
                           <span className="text-sm font-medium">{path.rating || 0}</span>
                         </div>
                      </div>

                                             {/* Tags */}
                       {path.tags && path.tags.length > 0 && (
                         <div className="flex flex-wrap gap-2 mb-4">
                           {path.tags.slice(0, 3).map((tag, index) => (
                             <span
                               key={index}
                               className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
                             >
                               {tag}
                             </span>
                           ))}
                           {path.tags.length > 3 && (
                             <span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">
                               +{path.tags.length - 3}
                             </span>
                           )}
                         </div>
                       )}

                      {/* Stats */}
                      <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                                                 <div className="flex items-center space-x-1">
                           <Clock className="w-4 h-4" />
                           <span>{path.estimated_duration || 0}h</span>
                         </div>
                         <div className="flex items-center space-x-1">
                           <Users className="w-4 h-4" />
                           <span>{path.enrolled_students || 0}</span>
                         </div>
                         <div className="flex items-center space-x-1">
                           <Target className="w-4 h-4" />
                           <span>{path.steps ? path.steps.length : 0} étapes</span>
                         </div>
                      </div>

                                             {/* Progress */}
                       {path.is_followed && path.progress !== undefined && (
                         <div className="mb-4">
                           <div className="flex justify-between text-sm mb-1">
                             <span className="text-gray-600">Progression</span>
                             <span className="text-blue-600 font-medium">{Math.round(path.progress)}%</span>
                           </div>
                           <div className="w-full bg-gray-200 rounded-full h-2">
                             <div
                               className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                               style={{ width: `${path.progress}%` }}
                             />
                           </div>
                         </div>
                       )}

                      {/* Footer */}
                      <div className="flex items-center justify-between">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(path.difficulty)}`}>
                          {path.difficulty}
                        </span>
                                                 {!path.is_followed ? (
                           <Button
                             size="sm"
                             onClick={(e) => {
                               e.stopPropagation();
                               handleEnrollPath(path.id);
                             }}
                             className="bg-blue-500 hover:bg-blue-600"
                           >
                             S'inscrire
                           </Button>
                         ) : (path.is_completed || path.progress === 100) ? (
                           <div className="flex items-center text-green-600 text-sm">
                             <CheckCircle className="w-4 h-4 mr-1" />
                             Terminé
                           </div>
                         ) : (
                           <div className="flex items-center text-blue-600 text-sm">
                             <Play className="w-4 h-4 mr-1" />
                             Continuer
                           </div>
                         )}
                      </div>
                    </div>
                  </div>
                </Card>
              ))}
            </div>

            {filteredPaths.length === 0 && (
              <div className="text-center py-12">
                <Map className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-600 mb-2">Aucun parcours trouvé</h3>
                <p className="text-gray-500">Essayez de modifier vos filtres ou recherchez un autre parcours</p>
              </div>
            )}
          </div>

          {/* Détails du parcours sélectionné */}
          {selectedPath && showPathDetails && (
            <div className="lg:col-span-1">
              <Card>
                <div className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h2 className="text-xl font-bold text-gray-900">Détails du parcours</h2>
                    <button
                      onClick={() => setShowPathDetails(false)}
                      className="text-gray-400 hover:text-gray-600"
                    >
                      ×
                    </button>
                  </div>

                  <div className="mb-6">
                    <h3 className="font-semibold text-gray-900 mb-2">{selectedPath.title}</h3>
                    <p className="text-sm text-gray-600 mb-4">{selectedPath.description}</p>

                                         {/* Progress */}
                     {selectedPath.is_followed && selectedPath.progress !== undefined && (
                       <div className="mb-4">
                         <div className="flex justify-between text-sm mb-1">
                           <span className="text-gray-600">Progression globale</span>
                           <span className="text-blue-600 font-medium">
                             {selectedPath.steps ? `${selectedPath.steps.filter(s => s.is_completed).length}/${selectedPath.steps.length}` : '0/0'} étapes
                           </span>
                         </div>
                         <div className="w-full bg-gray-200 rounded-full h-3">
                           <div
                             className="bg-blue-500 h-3 rounded-full transition-all duration-300"
                             style={{ width: `${selectedPath.progress}%` }}
                           />
                         </div>
                       </div>
                     )}

                                         {/* Outcomes */}
                     {selectedPath.outcomes && selectedPath.outcomes.length > 0 && (
                       <div className="mb-4">
                         <h4 className="font-medium text-gray-900 mb-2">Ce que vous apprendrez</h4>
                         <ul className="space-y-1">
                           {selectedPath.outcomes.map((outcome, index) => (
                             <li key={index} className="flex items-center text-sm text-gray-600">
                               <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
                               {outcome}
                             </li>
                           ))}
                         </ul>
                       </div>
                     )}

                     {/* Prerequisites */}
                     {selectedPath.prerequisites && selectedPath.prerequisites.length > 0 && (
                       <div className="mb-4">
                         <h4 className="font-medium text-gray-900 mb-2">Prérequis</h4>
                         <ul className="space-y-1">
                           {selectedPath.prerequisites.map((prereq, index) => (
                             <li key={index} className="flex items-center text-sm text-gray-600">
                               <Target className="w-4 h-4 text-blue-500 mr-2" />
                               {prereq}
                             </li>
                           ))}
                         </ul>
                       </div>
                     )}
                  </div>

                                     {/* Steps */}
                   <div>
                     <h4 className="font-semibold text-gray-900 mb-3">Étapes du parcours</h4>
                     <div className="space-y-3">
                       {selectedPath.steps && selectedPath.steps.map((step, index) => (
                        <div
                          key={step.id}
                          className={`p-3 rounded-lg border ${
                            step.is_completed
                              ? 'bg-green-50 border-green-200'
                              : step.is_locked
                              ? 'bg-gray-50 border-gray-200'
                              : 'bg-white border-gray-200 hover:border-blue-300'
                          }`}
                        >
                          <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-3">
                              <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                                step.is_completed
                                  ? 'bg-green-500 text-white'
                                  : step.is_locked
                                  ? 'bg-gray-300 text-gray-500'
                                  : 'bg-blue-500 text-white'
                              }`}>
                                {step.is_completed ? (
                                  <CheckCircle className="w-4 h-4" />
                                ) : step.is_locked ? (
                                  <Lock className="w-4 h-4" />
                                ) : (
                                  <span className="text-sm font-medium">{index + 1}</span>
                                )}
                              </div>
                              <div className="flex-1">
                                <h5 className="font-medium text-gray-900">{step.title}</h5>
                                <div className="flex items-center space-x-2 text-sm text-gray-500">
                                  {getStepIcon(step.type)}
                                  <span>{formatDuration(step.duration)}</span>
                                  <span className={`px-1 py-0.5 rounded text-xs ${getDifficultyColor(step.difficulty)}`}>
                                    {step.difficulty}
                                  </span>
                                </div>
                              </div>
                            </div>
                            {!step.is_locked && !step.is_completed && (
                              <Button
                                size="sm"
                                onClick={() => handleStepComplete(step.id)}
                                className="bg-blue-500 hover:bg-blue-600"
                              >
                                Terminer
                              </Button>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </Card>
            </div>
          )}
        </div>
        </div>
      </div>
    </div>
  );
};

export default LearningPathPage; 