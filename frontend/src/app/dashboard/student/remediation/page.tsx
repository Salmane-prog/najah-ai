'use client';

import React, { useEffect, useState } from 'react';
import { useAuth } from '@/hooks/useAuthSimple';
import { GapAnalysisService } from '@/services/gapAnalysisService';
import { CognitiveDiagnosticService, RemediationPlan, RemediationStep } from '@/services/cognitiveDiagnosticService';
import { CheckCircle, BookOpen, Play, Clock, Target, TrendingUp, Brain, Zap, RefreshCw, Volume2 } from 'lucide-react';

export default function RemediationPage() {
  const { user, token } = useAuth();
  const [remediationPlan, setRemediationPlan] = useState<RemediationPlan | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedSubject, setSelectedSubject] = useState('Français');
  const [completedExercises, setCompletedExercises] = useState<Set<number>>(new Set());
  const [realCompletedCount, setRealCompletedCount] = useState(0);
  const [diverseExercises, setDiverseExercises] = useState<any[]>([]);
  const [loadingExercises, setLoadingExercises] = useState(false);

  useEffect(() => {
    console.log('🔄 [REMEDIATION PAGE] useEffect déclenché');
    console.log('👤 [REMEDIATION PAGE] User:', user ? `ID ${user.id}` : 'NULL');
    console.log('🔑 [REMEDIATION PAGE] Token:', token ? 'PRÉSENT' : 'ABSENT');
    console.log('📚 [REMEDIATION PAGE] Subject:', selectedSubject);
    
    if (user && token) {
      console.log('✅ [REMEDIATION PAGE] Conditions remplies, chargement des données...');
      loadRemediationPlan();
      loadDiverseExercises();
    } else {
      console.log('❌ [REMEDIATION PAGE] Conditions non remplies, pas de chargement');
    }
  }, [user, token, selectedSubject]);

  const loadRemediationPlan = async () => {
    if (!user || !token) return;

    setLoading(true);
    setError(null);

    try {
      console.log('📋 [REMEDIATION PAGE] Chargement du plan de remédiation...');
      const plan = await CognitiveDiagnosticService.generateRemediationPlan(user.id, selectedSubject, token);
      setRemediationPlan(plan);
      console.log('✅ [REMEDIATION PAGE] Plan chargé:', plan);
      
      // Récupérer le vrai nombre d'exercices complétés
      try {
        const { RemediationService } = await import('@/services/remediationService');
        const remediationResults = await RemediationService.getRemediationResults(token, user.id);
        
        // Filtrer par matière
        const subjectResults = remediationResults.filter(result => 
          result.topic.toLowerCase().includes(selectedSubject.toLowerCase()) ||
          selectedSubject.toLowerCase().includes('français')
        );
        
        setRealCompletedCount(subjectResults.length);
        console.log('📊 [REMEDIATION PAGE] Vrais exercices complétés:', subjectResults.length);
      } catch (error) {
        console.warn('⚠️ [REMEDIATION PAGE] Impossible de récupérer les exercices complétés:', error);
      }
    } catch (error) {
      console.error('❌ [REMEDIATION PAGE] Erreur:', error);
      setError('Erreur lors du chargement du plan de remédiation');
    } finally {
      setLoading(false);
    }
  };

  const handleExerciseComplete = (exerciseId: number) => {
    setCompletedExercises(prev => new Set([...prev, exerciseId]));
    
    // Mettre à jour le vrai nombre d'exercices complétés
    setRealCompletedCount(prev => prev + 1);
    
    console.log('✅ [REMEDIATION PAGE] Exercice complété:', exerciseId);
    console.log('📊 [REMEDIATION PAGE] Nouveau progrès:', realCompletedCount + 1, '/', remediationPlan?.steps.length);
  };

  const loadDiverseExercises = async () => {
    if (!user || !token) {
      console.log('⚠️ [REMEDIATION PAGE] Pas d\'utilisateur ou de token, arrêt du chargement');
      return;
    }

    console.log('🎯 [REMEDIATION PAGE] Début chargement des exercices diversifiés...');
    console.log('👤 [REMEDIATION PAGE] Utilisateur:', user.id, 'Token:', token ? 'PRÉSENT' : 'ABSENT');
    
    setLoadingExercises(true);
    try {
      console.log('📦 [REMEDIATION PAGE] Import du service RemediationExerciseService...');
      
      // Récupérer des exercices diversifiés depuis la banque
      const { RemediationExerciseService } = await import('@/services/remediationExerciseService');
      console.log('✅ [REMEDIATION PAGE] Service importé avec succès');
      
      // Charger des exercices pour différents topics et difficultés
      const topics = ['grammar', 'conjugation', 'vocabulary', 'comprehension'];
      const difficulties = ['facile', 'intermédiaire', 'difficile'];
      
      console.log('🎯 [REMEDIATION PAGE] Topics à charger:', topics);
      console.log('🎯 [REMEDIATION PAGE] Difficultés à charger:', difficulties);
      
      const allExercises: any[] = [];
      
      for (const topic of topics) {
        for (const difficulty of difficulties) {
          try {
            console.log(`🔄 [REMEDIATION PAGE] Chargement ${topic}/${difficulty}...`);
            const exercises = await RemediationExerciseService.getDiverseExercises(topic, difficulty, 2, token);
            console.log(`📊 [REMEDIATION PAGE] Résultat ${topic}/${difficulty}:`, exercises);
            
            if (exercises && exercises.success && exercises.exercises && exercises.exercises.length > 0) {
              allExercises.push(...exercises.exercises.map(ex => ({ ...ex, topic, difficulty })));
              console.log(`✅ [REMEDIATION PAGE] ${exercises.exercises.length} exercices ajoutés pour ${topic}/${difficulty}`);
            } else {
              console.log(`⚠️ [REMEDIATION PAGE] Aucun exercice trouvé pour ${topic}/${difficulty}`);
              console.log(`🔍 [REMEDIATION PAGE] Structure reçue:`, exercises);
            }
          } catch (error) {
            console.error(`❌ [REMEDIATION PAGE] Erreur lors du chargement ${topic}/${difficulty}:`, error);
          }
        }
      }
      
      console.log('📊 [REMEDIATION PAGE] Total des exercices récupérés:', allExercises.length);
      
      // Mélanger et limiter à 12 exercices maximum
      const shuffledExercises = allExercises
        .sort(() => Math.random() - 0.5)
        .slice(0, 12);
      
      console.log('🎲 [REMEDIATION PAGE] Exercices mélangés et limités:', shuffledExercises.length);
      
      setDiverseExercises(shuffledExercises);
      console.log('✅ [REMEDIATION PAGE] Exercices diversifiés chargés et stockés:', shuffledExercises.length);
      console.log('📊 [REMEDIATION PAGE] État final diverseExercises:', shuffledExercises);
      
    } catch (error) {
      console.error('❌ [REMEDIATION PAGE] Erreur lors du chargement des exercices diversifiés:', error);
      // Utiliser des exercices de fallback
      const fallbackExercises = generateFallbackExercises();
      console.log('🔄 [REMEDIATION PAGE] Utilisation des exercices de fallback:', fallbackExercises.length);
      setDiverseExercises(fallbackExercises);
    } finally {
      setLoadingExercises(false);
      console.log('🏁 [REMEDIATION PAGE] Chargement terminé');
    }
  };

  const generateFallbackExercises = () => {
    return [
      {
        id: 1,
        title: "Quiz de Grammaire Fondamentale",
        description: "Testez vos connaissances en grammaire française",
        type: "quiz",
        topic: "grammar",
        difficulty: "facile",
        estimated_time: "5-8 min",
        questions_count: 10
      },
      {
        id: 2,
        title: "Conjugaison des Verbes",
        description: "Maîtrisez la conjugaison des temps principaux",
        type: "quiz",
        topic: "conjugation",
        difficulty: "intermédiaire",
        estimated_time: "8-12 min",
        questions_count: 15
      },
      {
        id: 3,
        title: "Vocabulaire Thématique",
        description: "Enrichissez votre vocabulaire par thèmes",
        type: "matching",
        topic: "vocabulary",
        difficulty: "facile",
        estimated_time: "6-10 min",
        questions_count: 12
      },
      {
        id: 4,
        title: "Compréhension de Textes",
        description: "Améliorez votre compréhension écrite",
        type: "reading",
        topic: "comprehension",
        difficulty: "difficile",
        estimated_time: "10-15 min",
        questions_count: 8
      }
    ];
  };

  const getExerciseIcon = (type: string) => {
    switch (type) {
      case 'quiz': return <Target className="w-6 h-6 text-blue-500" />;
      case 'reading': return <BookOpen className="w-6 h-6 text-green-500" />;
      case 'video': return <Play className="w-6 h-6 text-red-500" />;
      case 'practice': return <Brain className="w-6 h-6 text-purple-500" />;
      default: return <BookOpen className="w-6 h-6 text-gray-500" />;
    }
  };

  const getExerciseColor = (type: string) => {
    switch (type) {
      case 'quiz': return 'bg-blue-50 border-blue-200';
      case 'reading': return 'bg-green-50 border-green-200';
      case 'video': return 'bg-red-50 border-red-200';
      case 'practice': return 'bg-purple-50 border-purple-200';
      default: return 'bg-gray-50 border-gray-200';
    }
  };

  const getDifficultyColor = (level: number) => {
    if (level <= 3) return 'bg-green-100 text-green-800';
    if (level <= 6) return 'bg-yellow-100 text-yellow-800';
    return 'bg-red-100 text-red-800';
  };

  const getDifficultyLabel = (level: number) => {
    if (level <= 3) return 'Facile';
    if (level <= 6) return 'Intermédiaire';
    return 'Difficile';
  };

  const getDifficultyColorByLabel = (difficulty: string) => {
    switch (difficulty.toLowerCase()) {
      case 'facile':
        return 'bg-green-100 text-green-800';
      case 'intermédiaire':
        return 'bg-yellow-100 text-yellow-800';
      case 'difficile':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const groupExercisesByType = (exercises: any[]) => {
    const grouped = new Map<string, any[]>();
    
    // Filtrer d'abord les exercices par type
    const quizExercises = exercises.filter(ex => ex.type === 'quiz');
    const matchingExercises = exercises.filter(ex => ex.type === 'matching');
    const readingExercises = exercises.filter(ex => ex.type === 'reading');
    const listeningExercises = exercises.filter(ex => ex.type === 'listening');
    const practiceExercises = exercises.filter(ex => ex.type === 'practice');
    const otherExercises = exercises.filter(ex => !['quiz', 'matching', 'reading', 'listening', 'practice'].includes(ex.type));
    
    // Créer les groupes avec les exercices filtrés
    if (quizExercises.length > 0) {
      grouped.set('quiz', quizExercises);
    }
    
    if (matchingExercises.length > 0) {
      grouped.set('matching', matchingExercises);
    }
    
    if (readingExercises.length > 0) {
      grouped.set('reading', readingExercises);
    }
    
    if (listeningExercises.length > 0) {
      grouped.set('listening', listeningExercises);
    }
    
    if (practiceExercises.length > 0) {
      grouped.set('practice', practiceExercises);
    }
    
    if (otherExercises.length > 0) {
      grouped.set('other', otherExercises);
    }
    
    console.log('🔍 [GROUPING] Exercices filtrés par type:');
    console.log('   - Quiz:', quizExercises.length);
    console.log('   - Matching:', matchingExercises.length);
    console.log('   - Reading:', readingExercises.length);
    console.log('   - Listening:', listeningExercises.length);
    console.log('   - Practice:', practiceExercises.length);
    console.log('   - Other:', otherExercises.length);
    
    return grouped;
  };

  const getTypeDisplayName = (type: string) => {
    switch (type) {
      case 'quiz': return 'Quiz & QCM';
      case 'matching': return 'Associations';
      case 'reading': return 'Lecture';
      case 'listening': return 'Compréhension Orale';
      case 'practice': return 'Pratique';
      default: return type.charAt(0).toUpperCase() + type.slice(1);
    }
  };

  const getTypeDescription = (type: string) => {
    switch (type) {
      case 'quiz': return 'Questions à choix multiples et exercices de validation';
      case 'matching': return 'Associez les éléments avec leurs correspondances';
      case 'reading': return 'Améliorez votre compréhension écrite';
      case 'listening': return 'Développez votre compréhension orale';
      case 'practice': return 'Mettez en pratique vos connaissances';
      default: return 'Exercices variés pour progresser';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'quiz': return <Target className="w-8 h-8 text-blue-500" />;
      case 'matching': return <Zap className="w-8 h-8 text-green-500" />;
      case 'reading': return <BookOpen className="w-8 h-8 text-orange-500" />;
      case 'listening': return <Volume2 className="w-8 h-8 text-purple-500" />;
      case 'practice': return <Brain className="w-8 h-8 text-indigo-500" />;
      default: return <BookOpen className="w-8 h-8 text-gray-500" />;
    }
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'quiz': return 'bg-blue-50 border-blue-200 hover:bg-blue-100';
      case 'matching': return 'bg-green-50 border-green-200 hover:bg-green-100';
      case 'reading': return 'bg-orange-50 border-orange-200 hover:bg-orange-100';
      case 'listening': return 'bg-purple-50 border-purple-200 hover:bg-purple-100';
      case 'practice': return 'bg-indigo-50 border-indigo-200 hover:bg-indigo-100';
      default: return 'bg-gray-50 border-gray-200 hover:bg-gray-100';
    }
  };

  const getTypeButtonColor = (type: string) => {
    switch (type) {
      case 'quiz': return 'bg-blue-600 hover:bg-blue-700 text-white';
      case 'matching': return 'bg-green-600 hover:bg-green-700 text-white';
      case 'reading': return 'bg-orange-600 hover:bg-orange-700 text-white';
      case 'listening': return 'bg-purple-600 hover:bg-purple-700 text-white';
      case 'practice': return 'bg-indigo-600 hover:bg-indigo-700 text-white';
      default: return 'bg-gray-600 hover:bg-gray-700 text-white';
    }
  };

  const handleTypeClick = (type: string) => {
    // Rediriger vers la page appropriée selon le type
    switch (type) {
      case 'quiz':
        window.location.href = `/dashboard/student/remediation/quiz/grammar`;
        break;
      case 'matching':
        window.location.href = `/dashboard/student/remediation/matching/vocabulary`;
        break;
      case 'reading':
        window.location.href = `/dashboard/student/remediation/reading/comprehension`;
        break;
      case 'listening':
        window.location.href = `/dashboard/student/remediation/listening/comprehension`;
        break;
      case 'practice':
        window.location.href = `/dashboard/student/remediation/practice/grammar`;
        break;
      default:
        alert(`Type d'exercice '${type}' en cours de développement. Contactez votre enseignant pour plus d'informations.`);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-purple-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Génération de votre plan de remédiation...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <h2 className="text-red-800 font-semibold mb-2">Erreur</h2>
          <p className="text-red-700">{error}</p>
          <button 
            onClick={loadRemediationPlan}
            className="mt-4 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
          >
            Réessayer
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto p-6">
      {/* En-tête */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-4">
          <CheckCircle className="w-8 h-8 text-green-500" />
          <h1 className="text-3xl font-bold text-gray-900">Plan de Remédiation</h1>
        </div>
        <p className="text-gray-600 text-lg">
          Suivez un plan personnalisé pour combler vos lacunes et améliorer vos compétences
        </p>
      </div>

      {/* Sélecteur de matière */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Matière pour la remédiation
        </label>
        <select
          value={selectedSubject}
          onChange={(e) => setSelectedSubject(e.target.value)}
          className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
        >
          <option value="Français">Français</option>
          <option value="Mathématiques">Mathématiques</option>
          <option value="Histoire">Histoire</option>
          <option value="Géographie">Géographie</option>
          <option value="Sciences">Sciences</option>
        </select>
      </div>

      {remediationPlan && (
        <>
          {/* Résumé du plan */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            {/* Progrès global */}
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
              <div className="flex items-center justify-between mb-2">
                <TrendingUp className="w-6 h-6 text-blue-500" />
                <span className="text-sm text-gray-500">Progrès Global</span>
              </div>
              <div className="text-3xl font-bold text-blue-600">
                {(() => {
                  const progress = Math.round((realCompletedCount / remediationPlan.steps.length) * 100);
                  return isNaN(progress) ? 0 : progress;
                })()}%
                {/* Indicateur visuel pour les scores > 100% */}
                {(() => {
                  const progress = Math.round((realCompletedCount / remediationPlan.steps.length) * 100);
                  return progress > 100 ? (
                    <span className="ml-2 text-lg text-green-600">🎯</span>
                  ) : null;
                })()}
              </div>
              <p className="text-sm text-gray-600 mt-1">
                {realCompletedCount} / {remediationPlan.steps.length} étapes
              </p>
              
              {/* Barre de progression */}
              <div className="mt-3">
                <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
                  <div 
                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{ 
                      width: `${(() => {
                        const progress = Math.round((realCompletedCount / remediationPlan.steps.length) * 100);
                        // Limiter la largeur à 100% maximum pour éviter le débordement
                        return isNaN(progress) ? 0 : Math.min(progress, 100);
                      })()}%` 
                    }}
                  ></div>
                </div>
                {/* Indicateur de dépassement si > 100% */}
                {(() => {
                  const progress = Math.round((realCompletedCount / remediationPlan.steps.length) * 100);
                  return progress > 100 ? (
                    <div className="mt-1 text-xs text-blue-600 font-medium text-center">
                      +{progress - 100}% au-delà de l'objectif !
                    </div>
                  ) : null;
                })()}
              </div>
            </div>

            {/* Exercices restants */}
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
              <div className="flex items-center justify-between mb-2">
                <Target className="w-6 h-6 text-green-500" />
                <span className="text-sm text-gray-500">Exercices Restants</span>
              </div>
              <div className="text-3xl font-bold text-green-600">
                {(() => {
                  const remaining = Math.max(0, remediationPlan.steps.length - realCompletedCount);
                  return remaining;
                })()}
              </div>
              <p className="text-sm text-gray-600 mt-1">
                {(() => {
                  const remaining = Math.max(0, remediationPlan.steps.length - realCompletedCount);
                  if (remaining === 0) return 'Tous complétés !';
                  if (remaining === 1) return 'à compléter';
                  return 'à compléter';
                })()}
              </p>
            </div>

            {/* Temps estimé */}
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
              <div className="flex items-center justify-between mb-2">
                <Clock className="w-6 h-6 text-yellow-500" />
                <span className="text-sm text-gray-500">Temps Estimé</span>
              </div>
              <div className="text-3xl font-bold text-yellow-600">
                {(() => {
                  const totalTime = remediationPlan.steps.reduce((sum, step) => sum + (step.estimated_duration || 0), 0);
                  const hours = Math.floor(totalTime / 60);
                  return hours > 0 ? `${hours}h` : `${totalTime}min`;
                })()}
              </div>
              <p className="text-sm text-gray-600 mt-1">
                {(() => {
                  const totalTime = remediationPlan.steps.reduce((sum, step) => sum + (step.estimated_duration || 0), 0);
                  const hours = Math.floor(totalTime / 60);
                  const minutes = totalTime % 60;
                  if (hours > 0 && minutes > 0) {
                    return `${minutes}min`;
                  }
                  return 'Temps total';
                })()}
              </p>
            </div>

            {/* Domaines couverts */}
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
              <div className="flex items-center justify-between mb-2">
                <Brain className="w-6 h-6 text-purple-500" />
                <span className="text-sm text-gray-500">Domaines</span>
              </div>
              <div className="text-3xl font-bold text-purple-600">
                {remediationPlan.steps.length}
              </div>
              <p className="text-sm text-gray-600 mt-1">
                à améliorer
              </p>
            </div>
          </div>



          {/* Exercices de Remédiation Diversifiés */}
          <div className="mb-8">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
                <Zap className="w-6 h-6 text-yellow-500" />
                Types d'Exercices Disponibles
                <span className="text-sm font-normal text-gray-500 ml-2">
                  (Regroupés par Type - Progression Globale)
                </span>
              </h2>
              <button
                onClick={loadDiverseExercises}
                disabled={loadingExercises}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center gap-2"
              >
                <RefreshCw className={`w-4 h-4 ${loadingExercises ? 'animate-spin' : ''}`} />
                {loadingExercises ? 'Chargement...' : 'Actualiser'}
              </button>
            </div>
            
            {loadingExercises ? (
              <div className="text-center py-8">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                <p className="text-gray-600">Chargement des types d'exercices...</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {Array.from(groupExercisesByType(diverseExercises).entries()).map(([type, exercises]) => {
                  // Vérification supplémentaire : s'assurer que les exercices sont du bon type
                  const filteredExercises = exercises.filter(ex => {
                    if (type === 'quiz' && ex.type !== 'quiz') {
                      console.warn('⚠️ [FILTER] Exercice de type', ex.type, 'détecté dans le groupe quiz:', ex);
                      return false;
                    }
                    if (type === 'matching' && ex.type !== 'matching') {
                      console.warn('⚠️ [FILTER] Exercice de type', ex.type, 'détecté dans le groupe matching:', ex);
                      return false;
                    }
                    return true;
                  });
                  
                  const completedCount = filteredExercises.filter(ex => completedExercises.has(ex.id)).length;
                  const totalCount = filteredExercises.length;
                  const progress = totalCount > 0 ? (completedCount / totalCount) * 100 : 0;
                  
                  console.log(`🔍 [WIDGET ${type}] Affichage de ${filteredExercises.length} exercices filtrés`);
                  
                  return (
                    <div key={type} className={`p-6 rounded-lg border transition-all cursor-pointer ${getTypeColor(type)}`}
                         onClick={() => handleTypeClick(type)}>
                      <div className="flex items-center gap-3 mb-4">
                        {getTypeIcon(type)}
                        <div>
                          <h3 className="text-xl font-semibold text-gray-900">{getTypeDisplayName(type)}</h3>
                          <p className="text-sm text-gray-600">{getTypeDescription(type)}</p>
                        </div>
                      </div>
                      
                      <div className="space-y-3 mb-4">
                        <div className="flex items-center justify-between text-sm">
                          <span className="text-gray-600">Progression</span>
                          <span className="font-medium text-gray-900">{completedCount}/{totalCount}</span>
                        </div>
                        
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div 
                            className={`h-2 rounded-full transition-all ${
                              progress === 100 ? 'bg-green-500' : 'bg-blue-500'
                            }`}
                            style={{ width: `${progress}%` }}
                          ></div>
                        </div>
                        
                        <div className="flex items-center gap-2 text-sm text-gray-500">
                          <Clock className="w-4 h-4" />
                          <span>~{filteredExercises.reduce((sum, ex) => sum + (ex.estimated_time || 5), 0)} min</span>
                        </div>
                      </div>

                      <button
                        className={`w-full px-4 py-2 rounded-lg font-medium transition-colors ${getTypeButtonColor(type)}`}
                      >
                        Commencer les {getTypeDisplayName(type)}
                      </button>
                    </div>
                  );
                })}
              </div>
            )}
            
            {diverseExercises.length === 0 && !loadingExercises && (
              <div className="text-center py-8 bg-gray-50 rounded-lg">
                <Brain className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600 mb-2">
                  Aucun exercice disponible pour le moment 
                  <br />
                  <span className="text-sm text-gray-500">
                    (État: diverseExercises.length = {diverseExercises.length}, loadingExercises = {loadingExercises.toString()})
                  </span>
                </p>
                <button
                  onClick={loadDiverseExercises}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  Réessayer
                </button>
              </div>
            )}
          </div>



          {/* Actions recommandées */}
          <div className="bg-gradient-to-r from-green-50 to-blue-50 p-6 rounded-lg border border-green-200">
            <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <Brain className="w-6 h-6 text-purple-500" />
              Conseils pour Maximiser Votre Progrès
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-3">
                <div className="flex items-start gap-3">
                  <CheckCircle className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                  <p className="text-gray-700">Suivez les exercices dans l'ordre recommandé</p>
                </div>
                <div className="flex items-start gap-3">
                  <CheckCircle className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                  <p className="text-gray-700">Pratiquez régulièrement, même 15 minutes par jour</p>
                </div>
                <div className="flex items-start gap-3">
                  <CheckCircle className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                  <p className="text-gray-700">Revenez sur les exercices difficiles</p>
                </div>
              </div>
              
              <div className="space-y-3">
                <div className="flex items-start gap-3">
                  <CheckCircle className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                  <p className="text-gray-700">Utilisez les ressources complémentaires</p>
                </div>
                <div className="flex items-start gap-3">
                  <CheckCircle className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                  <p className="text-gray-700">Testez vos connaissances avec les quiz</p>
                </div>
                <div className="flex items-start gap-3">
                  <CheckCircle className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                  <p className="text-gray-700">Suivez votre progression régulièrement</p>
                </div>
              </div>
            </div>
          </div>
        </>
      )}

      {/* Message si pas de plan */}
      {!remediationPlan && !loading && (
        <div className="text-center py-12">
          <CheckCircle className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">Aucun plan de remédiation disponible</h3>
          <p className="text-gray-600 mb-4">
            Commencez par analyser vos lacunes pour générer un plan personnalisé
          </p>
          <button 
            onClick={() => window.location.href = '/dashboard/student/gap-analysis'}
            className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
          >
            Analyser mes Lacunes
          </button>
        </div>
      )}
    </div>
  );
}
