'use client';

import React, { useState, useEffect } from 'react';
import { Card } from '@/components/Card';
import Button from '@/components/Button';
import Sidebar from '@/components/Sidebar';
import { 
  Brain, 
  Plus,
  RefreshCw, 
  Share2, 
  Eye,
  Edit, 
  BarChart3,
  Users,
  Clock, 
  Target,
  TrendingUp,
  CheckCircle,
  AlertCircle,
  BookOpen,
  List
} from 'lucide-react';
import { useAuth } from '@/hooks/useAuthSimple';
import { adaptiveEvaluationService } from '@/services/adaptiveEvaluationService';
import { formativeEvaluationService, FormativeEvaluation } from '@/services/formativeEvaluationService';
import { analyticsService } from '@/services/analyticsService';
import { PerformanceMetrics, TestPerformance } from '@/types/analytics';
import { 
  AdaptiveTest, 
  Class, 
  User, 
  AssignmentData 
} from '@/types/adaptiveEvaluation';
import AssignmentModal from '@/components/AssignmentModal';
import RealTimeAnalytics from '@/components/RealTimeAnalytics';

import RealAnalyticsCharts from '@/components/RealAnalyticsCharts';


export default function AdaptiveEvaluationPage() {
  const { user } = useAuth();
  const [tests, setTests] = useState<AdaptiveTest[]>([]);
  const [formativeEvaluations, setFormativeEvaluations] = useState<FormativeEvaluation[]>([]);
  const [classes, setClasses] = useState<Class[]>([]);
  const [students, setStudents] = useState<User[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isLoadingFormative, setIsLoadingFormative] = useState(false);
  const [isLoadingClasses, setIsLoadingClasses] = useState(false);
  const [isLoadingStudents, setIsLoadingStudents] = useState(false);
  const [analytics, setAnalytics] = useState<PerformanceMetrics | null>(null);
  const [testPerformance, setTestPerformance] = useState<TestPerformance[]>([]);
  const [isLoadingAnalytics, setIsLoadingAnalytics] = useState(false);
  const [showAssignmentModal, setShowAssignmentModal] = useState(false);
  const [selectedTest, setSelectedTest] = useState<AdaptiveTest | null>(null);
  const [notification, setNotification] = useState<{ message: string; type: 'success' | 'error' | 'info' } | null>(null);
  const [showAllTests, setShowAllTests] = useState(false); // Nouveau état pour afficher tous les tests
  const [activeTab, setActiveTab] = useState<'tests' | 'formative' | 'analytics'>('tests'); // Onglet actif


  // Charger les données au montage du composant
  useEffect(() => {
    if (user && user.id) {
      loadData();
    }
  }, [user]);

  // Rafraîchir automatiquement toutes les 30 secondes
  useEffect(() => {
    if (!user?.id) return;
    
    const interval = setInterval(() => {
      console.log('🔄 Rafraîchissement automatique des données...');
      loadData();
    }, 30000); // 30 secondes

    return () => clearInterval(interval);
  }, [user]);

  // Écouter les événements de création de test depuis d'autres onglets
  useEffect(() => {
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === 'testCreated' && e.newValue === 'true') {
        console.log('🔄 Test créé détecté, rafraîchissement des données...');
        loadData();
        // Réinitialiser le flag
        localStorage.removeItem('testCreated');
      }
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, []);

  const loadData = async () => {
    setIsLoading(true);
    try {
      console.log('🔄 Chargement des données...');
      
      // Charger les tests selon le mode sélectionné
      let testsData;
      if (showAllTests) {
        testsData = await adaptiveEvaluationService.getAllTestsIncludingInactive();
        console.log('📊 Chargement de tous les tests (actifs + inactifs)');
      } else {
        // Utiliser l'endpoint simple
        testsData = await adaptiveEvaluationService.getAllTestsSimple();
        console.log('📊 Chargement des tests actifs uniquement (endpoint simple)');
      }
      
      if (testsData.tests && testsData.tests.length > 0) {
        console.log(`✅ ${testsData.tests.length} tests chargés`);
        setTests(testsData.tests);
      } else {
        console.log('⚠️ Aucun test trouvé');
        setTests([]);
      }
      
      // Charger les évaluations formatives
      await loadFormativeEvaluations();
      
      // Charger les classes et étudiants
      await loadClassesAndStudents();
      
      // Charger les analytics
      await loadAnalytics();
      
    } catch (error) {
      console.error('❌ Erreur lors du chargement des données:', error);
      setTests([]);
    } finally {
      setIsLoading(false);
      
      // Masquer la notification après 3 secondes
      setTimeout(() => setNotification(null), 3000);
    }
  };

  const loadFormativeEvaluations = async () => {
    setIsLoadingFormative(true);
    try {
      const evaluations = await formativeEvaluationService.getAllEvaluations();
      console.log(`📊 ${evaluations.length} évaluations formatives chargées`);
      setFormativeEvaluations(evaluations);
    } catch (error) {
      console.error('❌ Erreur lors du chargement des évaluations formatives:', error);
      setFormativeEvaluations([]);
    } finally {
      setIsLoadingFormative(false);
    }
  };

  const loadAnalytics = async () => {
    setIsLoadingAnalytics(true);
    try {
      console.log('📊 Chargement des analytics...');
      
      // Charger les analytics du tableau de bord
      const dashboardAnalytics = await analyticsService.getPerformanceMetrics();
      setAnalytics(dashboardAnalytics);
      console.log('📊 Analytics du tableau de bord chargés:', dashboardAnalytics);
      
      // Charger les analytics de performance des tests
      const performanceAnalytics = await analyticsService.getTestPerformances();
      setTestPerformance(performanceAnalytics);
      console.log('📈 Analytics de performance chargés:', performanceAnalytics);
      
    } catch (error) {
      console.error('❌ Erreur lors du chargement des analytics:', error);
      setNotification({
        message: 'Erreur lors du chargement des analytics',
        type: 'error'
      });
    } finally {
      setIsLoadingAnalytics(false);
    }
  };

  const loadClassesAndStudents = async () => {
    if (!user?.id) return;

    setIsLoadingClasses(true);
    setIsLoadingStudents(true);

    try {
      const [classesData, studentsData] = await Promise.all([
        adaptiveEvaluationService.getTeacherClasses(user.id),
        adaptiveEvaluationService.getTeacherStudents(user.id)
      ]);

      setClasses(classesData);
      setStudents(studentsData);
    } catch (error) {
      console.error('Erreur lors du chargement des classes/étudiants:', error);
    } finally {
      setIsLoadingClasses(false);
      setIsLoadingStudents(false);
    }
  };

  const handleAssignTest = (test: AdaptiveTest) => {
    setSelectedTest(test);
    setShowAssignmentModal(true);
  };

  const handleAssignmentSubmit = async (assignmentData: AssignmentData) => {
    if (!selectedTest) return;

    try {
      const result = await adaptiveEvaluationService.assignTest(
        selectedTest.id, 
        assignmentData
      );

      if (result.success) {
        alert(`✅ Test assigné avec succès à ${result.assignments.length} cibles !`);
        // Recharger les données pour mettre à jour les statistiques
        loadData();
      }
    } catch (error) {
      console.error('Erreur lors de l\'assignation:', error);
      alert('❌ Erreur lors de l\'assignation du test');
    }
  };

  // Fonction pour obtenir la couleur du type d'adaptation
  const getAdaptationTypeColor = (type: string) => {
    switch (type) {
      case 'difficulty':
        return 'bg-blue-100 text-blue-800';
      case 'cognitive':
        return 'bg-purple-100 text-purple-800';
      case 'performance':
        return 'bg-green-100 text-green-800';
      case 'hybrid':
        return 'bg-orange-100 text-orange-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  // Fonction pour prévisualiser un test
  const handlePreviewTest = async (test: AdaptiveTest) => {
    console.log('🚀 handlePreviewTest appelé depuis la liste avec:', test);
    
    if (!test) {
      console.error('❌ Test est undefined ou null');
        return;
      }
      
    try {
      // Essayer de récupérer les vraies questions depuis la page de création
      console.log('🔍 Tentative de récupération des vraies questions...');
      
      // Vérifier s'il y a des questions récentes dans localStorage
      const recentTests = [];
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key && key.startsWith('previewTest_')) {
          try {
            const testData = JSON.parse(localStorage.getItem(key) || '{}');
            if (testData.subject === test.subject && testData.questions && testData.questions.length > 0) {
              recentTests.push(testData);
            }
          } catch (e) {
            // Ignorer les erreurs de parsing
          }
        }
      }
      
      // Trier par date de création (plus récent en premier)
      recentTests.sort((a, b) => new Date(b.storedAt || 0).getTime() - new Date(a.storedAt || 0).getTime());
      
      let questionsToUse = [];
      let source = 'démo';
      
      if (recentTests.length > 0) {
        // Utiliser les vraies questions du test le plus récent
        const mostRecentTest = recentTests[0];
        questionsToUse = mostRecentTest.questions;
        source = 'vraies questions récupérées';
        console.log('✅ Vraies questions trouvées:', mostRecentTest.title, 'avec', questionsToUse.length, 'questions');
      } else {
        // Fallback : générer des questions de démonstration
        console.log('⚠️ Aucune vraie question trouvée, génération de questions de démonstration...');
        questionsToUse = generateDemoQuestions(test);
        source = 'questions de démonstration';
      }
      
      // Créer un ID unique pour ce test de prévisualisation
      const previewId = `preview_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      
      console.log('🔑 ID de prévisualisation généré:', previewId);
      console.log('📚 Source des questions:', source);
      
      // Convertir le test au format attendu par la page de prévisualisation
      const testToStore = {
            id: test.id,
            title: test.title,
            subject: test.subject,
        description: test.description || `Test adaptatif pour ${test.subject}`,
        difficulty_range_min: test.difficulty_min || 1,
        difficulty_range_max: test.difficulty_max || 10,
            estimated_duration: test.estimated_duration || 30,
        question_count: test.total_questions || questionsToUse.length,
        adaptiveType: test.adaptation_type || 'cognitive',
        learning_objectives: test.learning_objectives || `Test adaptatif pour ${test.subject}`,
        is_active: test.is_active || false,
        created_at: test.created_at || new Date().toISOString(),
        questions: questionsToUse,
        previewId: previewId,
        storedAt: new Date().toISOString(),
        questionSource: source
      };
      
      localStorage.setItem(`previewTest_${previewId}`, JSON.stringify(testToStore));
      
      // Stocker l'ID de prévisualisation actuel
      localStorage.setItem('currentPreviewId', previewId);
      
      console.log('💾 Test stocké en localStorage avec la clé:', `previewTest_${previewId}`);
      console.log('🔍 Prévisualisation du test:', {
        id: previewId,
        title: testToStore.title,
        subject: testToStore.subject,
        questionCount: testToStore.questions.length,
        source: source
      });
      
      // Vérifier que le test a bien été stocké
      const storedTest = localStorage.getItem(`previewTest_${previewId}`);
      if (storedTest) {
        console.log('✅ Test vérifié en localStorage:', JSON.parse(storedTest));
      } else {
        console.error('❌ Test non trouvé en localStorage après stockage');
      }
      
      // Ouvrir dans un nouvel onglet avec l'ID unique
      const previewUrl = `/dashboard/teacher/adaptive-evaluation/preview?previewId=${previewId}`;
      console.log('🌐 Ouverture de l\'URL:', previewUrl);
      window.open(previewUrl, '_blank');
      
    } catch (error) {
      console.error('❌ Erreur lors de la prévisualisation:', error);
      
      // Fallback en cas d'erreur
      const previewId = `preview_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      const demoQuestions = generateDemoQuestions(test);
      
      const testToStore = {
        ...test,
        questions: demoQuestions,
        previewId: previewId,
        storedAt: new Date().toISOString(),
        questionSource: 'fallback (erreur)'
      };
      
      localStorage.setItem(`previewTest_${previewId}`, JSON.stringify(testToStore));
      localStorage.setItem('currentPreviewId', previewId);
      
      const previewUrl = `/dashboard/teacher/adaptive-evaluation/preview?previewId=${previewId}`;
      window.open(previewUrl, '_blank');
    }
  };

  // Fonction pour générer des questions de démonstration
  const generateDemoQuestions = (test: AdaptiveTest) => {
    const questionCount = test.total_questions || 10;
    const questions = [];
    
    // Questions de base selon la matière
    const baseQuestions = {
      'Français': [
        {
          question: "Quel est l'article correct ? '___ chat'",
          options: ["Le", "La", "Les", "L'"],
          correctAnswer: 0,
          explanation: "Le mot 'chat' est masculin singulier, donc on utilise 'Le'",
          difficulty: 1,
          learningObjective: "Reconnaître les articles définis masculins"
        },
        {
          question: "Comment se conjugue 'être' à la 1ère personne du singulier ?",
          options: ["suis", "es", "est", "sont"],
          correctAnswer: 0,
          explanation: "Le verbe 'être' à la 1ère personne du singulier se conjugue 'suis'",
          difficulty: 2,
          learningObjective: "Conjuguer le verbe être au présent"
        },
        {
          question: "Quel est le contraire de 'grand' ?",
          options: ["petit", "gros", "long", "court"],
          correctAnswer: 0,
          explanation: "Le contraire de 'grand' est 'petit'",
          difficulty: 1,
          learningObjective: "Reconnaître les antonymes"
        }
      ],
      'Géographie': [
        {
          question: "Quelle est la capitale de la France ?",
          options: ["Lyon", "Marseille", "Paris", "Bordeaux"],
          correctAnswer: 2,
          explanation: "Paris est la capitale de la France",
          difficulty: 1,
          learningObjective: "Connaître les capitales européennes"
        },
        {
          question: "Quel est le plus grand pays du monde ?",
          options: ["Chine", "États-Unis", "Russie", "Canada"],
          correctAnswer: 2,
          explanation: "La Russie est le plus grand pays du monde par sa superficie",
          difficulty: 2,
          learningObjective: "Connaître la géographie mondiale"
        }
      ],
      'Mathématiques': [
        {
          question: "Quel est le résultat de 7 + 5 ?",
          options: ["10", "11", "12", "13"],
          correctAnswer: 2,
          explanation: "7 + 5 = 12",
          difficulty: 1,
          learningObjective: "Additionner des nombres entiers"
        },
        {
          question: "Quel est le double de 8 ?",
          options: ["12", "14", "16", "18"],
          correctAnswer: 2,
          explanation: "Le double de 8 est 16 (8 × 2 = 16)",
          difficulty: 1,
          learningObjective: "Multiplier par 2"
        }
      ]
    };
    
    // Sélectionner les questions de base selon la matière
    const subjectQuestions = baseQuestions[test.subject as keyof typeof baseQuestions] || baseQuestions['Français'];
    
    // Générer des questions variées
    for (let i = 0; i < questionCount; i++) {
      const baseQuestion = subjectQuestions[i % subjectQuestions.length];
      const variant = {
        id: i + 1,
        question: baseQuestion.question,
        type: 'multiple_choice',
        difficulty: Math.min(10, Math.max(1, baseQuestion.difficulty + (i % 3))),
        options: baseQuestion.options,
        correctAnswer: baseQuestion.correctAnswer,
        explanation: baseQuestion.explanation,
        learningObjective: baseQuestion.learningObjective
      };
      questions.push(variant);
    }
    
    return questions;
  };

  // Prévisualiser une évaluation formative
  const handlePreviewFormative = (evaluation: FormativeEvaluation) => {
    try {
      console.log('🔍 Tentative de prévisualisation de l\'évaluation formative:', evaluation);
      
      // Générer un ID unique pour la prévisualisation
      const previewId = `formativePreview_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      console.log('🆔 ID de prévisualisation formative généré:', previewId);
      
      // Stocker dans localStorage avec l'ID unique
      localStorage.setItem(`formativePreview_${previewId}`, JSON.stringify(evaluation));
      console.log('💾 Évaluation formative stockée dans localStorage avec la clé:', `formativePreview_${previewId}`);
      
      // Ouvrir la page de prévisualisation formative avec l'ID
      const previewUrl = `/dashboard/teacher/adaptive-evaluation/preview-formative?previewId=${previewId}`;
      console.log('🔗 URL de prévisualisation formative:', previewUrl);
      window.open(previewUrl, '_blank');
      
    } catch (error) {
      console.error('❌ Erreur lors de la prévisualisation formative:', error);
      alert('Erreur lors de la prévisualisation de l\'évaluation formative');
    }
  };

  // Modifier une évaluation formative
  const handleEditFormative = (evaluation: FormativeEvaluation) => {
    try {
      console.log('✏️ Tentative de modification de l\'évaluation formative:', evaluation);
      
      // Ouvrir la page de modification avec l'ID de l'évaluation
      const editUrl = `/dashboard/teacher/adaptive-evaluation/edit-assessment?id=${evaluation.id}`;
      console.log('🔗 URL de modification:', editUrl);
      window.open(editUrl, '_blank');
      
    } catch (error) {
      console.error('❌ Erreur lors de l\'ouverture de la modification:', error);
      alert('Erreur lors de l\'ouverture de la page de modification');
    }
  };

  const handleToggleTestStatus = async (test: AdaptiveTest) => {
    try {
      let result;
      if (test.is_active) {
        // Désactiver le test
        result = await adaptiveEvaluationService.deactivateTest(test.id);
        if (result.success) {
          setNotification({ 
            message: `✅ Test "${test.title}" désactivé avec succès`, 
            type: 'success' 
          });
        }
      } else {
        // Activer le test
        result = await adaptiveEvaluationService.activateTest(test.id);
        if (result.success) {
          setNotification({ 
            message: `✅ Test "${test.title}" activé avec succès`, 
            type: 'success' 
          });
        }
      }

      if (result.success) {
        // Recharger les données pour mettre à jour l'affichage
        loadData();
      } else {
        setNotification({ 
          message: `❌ Erreur lors de la modification du statut: ${result.error}`, 
          type: 'error' 
        });
      }
    } catch (error) {
      console.error('Erreur lors de la modification du statut:', error);
      setNotification({ 
        message: '❌ Erreur lors de la modification du statut du test', 
        type: 'error' 
      });
    }
  };



  const handleDeactivateTest = async (test: AdaptiveTest) => {
    try {
      const result = await adaptiveEvaluationService.deactivateTest(test.id);
      if (result.success) {
        setNotification({ 
          message: `✅ Test "${test.title}" désactivé avec succès`, 
          type: 'success' 
        });
        // Recharger les données
        loadData();
      } else {
        setNotification({ 
          message: `❌ Erreur lors de la désactivation: ${result.error}`, 
          type: 'error' 
        });
      }
    } catch (error) {
      console.error('Erreur lors de la désactivation:', error);
      setNotification({ 
        message: '❌ Erreur lors de la désactivation du test', 
        type: 'error' 
      });
    }
  };

  const getDifficultyColor = (min: number, max: number) => {
    const avg = (min + max) / 2;
    if (avg <= 3) return 'text-green-600 bg-green-100';
    if (avg <= 6) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };



  if (isLoading) {
    return (
      <div className="flex h-screen bg-gray-50">
        <Sidebar />
        <div className="flex-1 ml-56 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-purple-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Chargement des données...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 ml-56 p-8 overflow-y-auto">
      {/* Header */}
      <div className="text-center mb-8">
        <div className="flex items-center justify-center mb-4">
          <Brain className="w-12 h-12 text-purple-600 mr-4" />
          <h1 className="text-4xl font-bold text-gray-900">Évaluation Adaptative</h1>
        </div>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
             Gérez vos tests adaptatifs et évaluations formatives pour un apprentissage personnalisé
             </p>
           </div>

      {/* Notification */}
      {notification && (
        <div className={`mb-6 p-4 rounded-lg border ${
          notification.type === 'success' 
            ? 'bg-green-50 border-green-200 text-green-800' 
            : notification.type === 'error'
            ? 'bg-red-50 border-red-200 text-red-800'
            : 'bg-blue-50 border-blue-200 text-blue-800'
        }`}>
          <div className="flex items-center justify-between">
            <span>{notification.message}</span>
            <button 
              onClick={() => setNotification(null)}
              className="text-gray-500 hover:text-gray-700"
            >
              ×
            </button>
         </div>
        </div>
      )}

      {/* Tip */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-8">
        <div className="flex items-center space-x-2 text-blue-800">
          <Eye className="w-5 h-5" />
          <span className="font-medium">Astuce :</span>
          <span>Cliquez sur le titre d&apos;un test pour le prévisualiser directement !</span>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex space-x-1 bg-gray-100 p-1 rounded-lg mb-8">
              <button
                onClick={() => setActiveTab('tests')}
          className={`flex-1 py-2 px-4 rounded-md font-medium transition-colors ${
                  activeTab === 'tests'
              ? 'bg-white text-purple-600 shadow-sm'
              : 'text-gray-600 hover:text-gray-800'
                }`}
              >
                Tests Adaptatifs
              </button>
              <button
          onClick={() => setActiveTab('formative')}
          className={`flex-1 py-2 px-4 rounded-md font-medium transition-colors ${
            activeTab === 'formative'
              ? 'bg-white text-purple-600 shadow-sm'
              : 'text-gray-600 hover:text-gray-800'
                }`}
              >
                Évaluations Formatives
              </button>
              <button
                onClick={() => setActiveTab('analytics')}
          className={`flex-1 py-2 px-4 rounded-md font-medium transition-colors ${
                  activeTab === 'analytics'
              ? 'bg-white text-purple-600 shadow-sm'
              : 'text-gray-600 hover:text-gray-800'
                }`}
              >
                Analytics
              </button>
          </div>
          
      {/* Action Buttons */}
      <div className="flex justify-between items-center mb-8">
        <div className="flex space-x-4">
              <Button 
            onClick={loadData}
                disabled={isLoading}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white px-4 py-2 rounded-xl flex items-center space-x-2"
              >
            <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
            <span>{isLoading ? 'Chargement...' : 'Actualiser'}</span>
              </Button>
          
          <Button
            onClick={() => {
              setShowAllTests(!showAllTests);
              // Recharger les données avec le nouveau mode
              setTimeout(() => loadData(), 100);
            }}
            className={`px-4 py-2 rounded-xl flex items-center space-x-2 ${
              showAllTests 
                ? 'bg-orange-600 hover:bg-orange-700 text-white' 
                : 'bg-gray-600 hover:bg-gray-700 text-white'
            }`}
          >
            <Eye className="w-4 h-4" />
            <span>{showAllTests ? 'Tests Actifs Seulement' : 'Tous les Tests'}</span>
          </Button>
        </div>

        <div className="flex space-x-4">
          <Button
            onClick={() => {
              // Ouvrir dans le même onglet pour éviter les problèmes de synchronisation
              window.location.href = '/dashboard/teacher/adaptive-evaluation/create-test';
            }}
            className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-xl flex items-center space-x-2"
          >
            <Plus className="w-4 h-4" />
            <span>+ Créer un Test</span>
          </Button>

          <Button
            onClick={() => {
              window.location.href = '/dashboard/teacher/adaptive-evaluation/results';
            }}
            className="bg-orange-600 hover:bg-orange-700 text-white px-4 py-2 rounded-xl flex items-center space-x-2"
          >
            <TrendingUp className="w-4 h-4" />
            <span>Voir Résultats</span>
          </Button>
              </div>
            </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <Card className="p-6">
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-blue-100 rounded-xl">
              <Brain className="h-6 w-6 text-blue-600" />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-600">Tests Créés</p>
              <p className="text-2xl font-bold text-gray-900">{tests.length}</p>
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-green-100 rounded-xl">
              <CheckCircle className="h-6 w-6 text-green-600" />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-600">Tests Actifs</p>
              <p className="text-2xl font-bold text-gray-900">{tests.filter(t => t.is_active).length}</p>
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-purple-100 rounded-xl">
              <Users className="h-6 w-6 text-purple-600" />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-600">Classes</p>
              <p className="text-2xl font-bold text-gray-900">{classes.length}</p>
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-orange-100 rounded-xl">
              <Target className="h-6 w-6 text-orange-600" />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-600">Étudiants</p>
              <p className="text-2xl font-bold text-gray-900">{students.length}</p>
            </div>
          </div>
        </Card>
      </div>

      {/* Content based on active tab */}
      {activeTab === 'tests' && (
        <>
          {/* Tests Section */}
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Tests Adaptatifs</h2>
        
        
        {!isLoading && tests.length === 0 ? (
          <Card className="p-12 text-center rounded-2xl">
            <Brain className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-xl font-medium text-gray-900 mb-2">Aucun test créé</h3>
            <p className="text-gray-600 mb-6">
              Commencez par créer votre premier test adaptatif pour évaluer vos étudiants
            </p>
            <Button
              onClick={() => window.open('/dashboard/teacher/adaptive-evaluation/create-test', '_blank')}
              className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-xl"
            >
              <Plus className="w-4 h-4 mr-2" />
              Créer un Test
                  </Button>
          </Card>
        ) : isLoading ? (
          <Card className="p-12 text-center rounded-2xl">
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-purple-600 mx-auto mb-4"></div>
            <h3 className="text-xl font-medium text-gray-900 mb-2">Chargement des tests...</h3>
            <p className="text-gray-600">Veuillez patienter</p>
          </Card>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            
            {tests.map((test, index) => (
              <Card 
                key={test.id} 
                className="p-6 hover:shadow-xl transition-all duration-200 cursor-pointer group rounded-2xl"
                           onClick={() => handlePreviewTest(test)}
                         >
                {/* Header */}
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <h3 className="text-xl font-semibold text-gray-800 mb-2 group-hover:text-purple-600 transition-colors">
                             {test.title}
                         </h3>
                    <div className="flex items-center space-x-2 mb-2">
                         <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                           test.is_active 
                             ? 'bg-green-100 text-green-800' 
                             : 'bg-gray-100 text-gray-800'
                         }`}>
                           {test.is_active ? 'Actif' : 'Inactif'}
                         </span>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getAdaptationTypeColor(test.adaptation_type)}`}>
                        {test.adaptation_type}
                      </span>
                    </div>
                       </div>
                      
                  {/* Indicateur de clic */}
                  <div className="opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                    <Eye className="w-5 h-5 text-purple-500" />
                  </div>
                </div>

                {/* Description */}
                <p className="text-gray-600 mb-4 line-clamp-2">{test.description}</p>

                {/* Test Info */}
                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div className="flex items-center space-x-2 text-sm text-gray-600">
                    <Target className="w-4 h-4" />
                    <span>Niveau {test.difficulty_min}-{test.difficulty_max}</span>
                        </div>
                  <div className="flex items-center space-x-2 text-sm text-gray-600">
                    <Clock className="w-4 h-4" />
                    <span>{test.estimated_duration} min</span>
                        </div>
                  <div className="flex items-center space-x-2 text-sm text-gray-600">
                    <Users className="w-4 h-4" />
                    <span>{test.total_questions} questions</span>
                        </div>
                  <div className="flex items-center space-x-2 text-sm text-gray-600">
                    <TrendingUp className="w-4 h-4" />
                    <span>{test.subject}</span>
                        </div>
                      </div>

                {/* Learning Objectives */}
                {test.learning_objectives && (
                  <div className="mb-4 p-3 bg-blue-50 rounded-lg">
                    <h4 className="text-sm font-medium text-blue-800 mb-1">Objectifs d&apos;apprentissage :</h4>
                    <p className="text-sm text-blue-700 line-clamp-2">{test.learning_objectives}</p>
                    </div>
                )}
                    
                {/* Actions */}
                <div className="flex items-center justify-between pt-4 border-t border-gray-100">
                  <div className="flex space-x-2">
                        <Button
                      onClick={(e) => {
                        e.stopPropagation(); // Empêcher la propagation du clic
                        handleAssignTest(test);
                      }}
                      className="bg-purple-600 hover:bg-purple-700 text-white px-3 py-2 rounded-xl text-sm flex items-center"
                      aria-label="Assigner le test"
                    >
                      <Share2 className="w-4 h-4 mr-1" />
                      Assigner
                        </Button>
                    
                        <Button
                      onClick={(e) => {
                        e.stopPropagation(); // Empêcher la propagation du clic
                        handleToggleTestStatus(test);
                      }}
                      className={`px-3 py-2 rounded-xl text-sm flex items-center ${
                          test.is_active
                          ? 'bg-red-600 hover:bg-red-700 text-white'
                            : 'bg-green-600 hover:bg-green-700 text-white'
                        }`}
                      aria-label={test.is_active ? 'Désactiver le test' : 'Activer le test'}
                    >
                      {test.is_active ? (
                        <>
                          <AlertCircle className="w-4 h-4 mr-1" />
                          Désactiver
                        </>
                      ) : (
                        <>
                          <CheckCircle className="w-4 h-4 mr-1" />
                          Activer
                        </>
                      )}
                      </Button>
                    </div>

                  <div className="text-xs text-gray-500">
                    Créé le {new Date(test.created_at).toLocaleDateString('fr-FR')}
                  </div>
                </div>
                
                {/* Indicateur de clic en bas */}
                <div className="mt-4 text-center opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                  <span className="text-sm text-purple-600 font-medium">Cliquez pour prévisualiser</span>
                  </div>
                </Card>
            ))}
            </div>
        )}
          </div>
        </>
      )}

             {activeTab === 'formative' && (
         <>
           {/* Évaluations Formatives Section */}
           <div className="mb-8">
             <h2 className="text-2xl font-bold text-gray-900 mb-6">Évaluations Formatives</h2>


             {!isLoadingFormative && formativeEvaluations.length === 0 ? (
               <Card className="p-12 text-center rounded-2xl">
                 <BookOpen className="w-16 h-16 text-orange-300 mx-auto mb-4" />
                 <h3 className="text-xl font-medium text-gray-900 mb-2">Aucune évaluation formative créée</h3>
                 <p className="text-gray-600 mb-6">
                                        Commencez par créer votre première évaluation formative avec l&apos;IA
                 </p>
                 <Button
                   onClick={() => window.open('/dashboard/teacher/adaptive-evaluation/create-assessment', '_blank')}
                   className="bg-orange-600 hover:bg-orange-700 text-white px-6 py-3 rounded-xl"
               >
                 <Plus className="w-4 h-4 mr-2" />
                   Créer une Évaluation
                 </Button>
               </Card>
             ) : isLoadingFormative ? (
               <Card className="p-12 text-center rounded-2xl">
                 <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-orange-600 mx-auto mb-4"></div>
                 <h3 className="text-xl font-medium text-gray-900 mb-2">Chargement des évaluations...</h3>
                 <p className="text-gray-600">Veuillez patienter</p>
               </Card>
             ) : (
               <div className="space-y-6">
                 {/* Header avec bouton de création */}
                 <div className="flex items-center justify-between">
                   <h3 className="text-lg font-medium text-gray-900">
                     {formativeEvaluations.length} évaluation{formativeEvaluations.length > 1 ? 's' : ''} formative{formativeEvaluations.length > 1 ? 's' : ''}
                   </h3>
                   <Button
                     onClick={() => window.open('/dashboard/teacher/adaptive-evaluation/create-assessment', '_blank')}
                     className="bg-orange-600 hover:bg-orange-700 text-white px-4 py-2 rounded-xl"
                   >
                     <Plus className="w-4 h-4 mr-2" />
                     Créer une Évaluation
                   </Button>
            </div>

                 {/* Liste des évaluations */}
                 <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                   {formativeEvaluations.map((evaluation, index) => (
                     <Card key={evaluation.id || index} className="p-6 hover:shadow-xl transition-all duration-200 rounded-2xl">
                       {/* Header */}
                       <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                           <h3 className="text-xl font-semibold text-gray-800 mb-2">
                             {evaluation.title}
                        </h3>
                           <div className="flex items-center space-x-2 mb-2">
                             <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                               evaluation.is_active
                                 ? 'bg-green-100 text-green-800'
                                 : 'bg-gray-100 text-gray-800'
                             }`}>
                               {evaluation.is_active ? 'Active' : 'Inactive'}
                             </span>
                             <span className="px-2 py-1 rounded-full text-xs font-medium bg-orange-100 text-orange-800">
                               {evaluation.assessment_type}
                        </span>
                      </div>
                        </div>
                        </div>

                       {/* Description */}
                       <p className="text-gray-600 mb-4 line-clamp-2">{evaluation.description}</p>

                       {/* Informations */}
                       <div className="grid grid-cols-2 gap-4 mb-4">
                         <div className="flex items-center space-x-2 text-sm text-gray-600">
                           <Target className="w-4 h-4" />
                           <span>Niveau {evaluation.target_level || 'Non défini'}</span>
                        </div>
                         <div className="flex items-center space-x-2 text-sm text-gray-600">
                           <Clock className="w-4 h-4" />
                           <span>{evaluation.duration_minutes || 0} min</span>
                        </div>
                         <div className="flex items-center space-x-2 text-sm text-gray-600">
                           <Users className="w-4 h-4" />
                           <span>Max {evaluation.max_students}</span>
                         </div>
                         <div className="flex items-center space-x-2 text-sm text-gray-600">
                           <BookOpen className="w-4 h-4" />
                           <span>{evaluation.questions?.length || 0} questions</span>
                      </div>
                    </div>
                    
                       {/* Actions */}
                       <div className="flex items-center justify-between pt-4 border-t border-gray-100">
                         <div className="flex space-x-2">
                           <Button
                             onClick={() => handlePreviewFormative(evaluation)}
                             className="text-orange-600 border-orange-200 hover:bg-orange-50 border border-orange-200 px-3 py-2 rounded-xl text-sm"
                           >
                             <Eye className="w-4 h-4 mr-1" />
                             Prévisualiser
                           </Button>
                           <Button
                             onClick={() => handleEditFormative(evaluation)}
                             className="text-blue-600 border-blue-200 hover:bg-blue-50 border border-blue-200 px-3 py-2 rounded-xl text-sm"
                           >
                             <Edit className="w-4 h-4 mr-1" />
                             Modifier
                           </Button>
                         </div>

                         <div className="text-xs text-gray-500">
                           Créée le {new Date(evaluation.created_at).toLocaleDateString('fr-FR')}
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          </div>
             )}
           </div>
         </>
        )}

        {activeTab === 'analytics' && (
        <>
          {/* Analytics Section avec Onglets */}
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Analytics Avancés</h2>
            
            {isLoadingAnalytics ? (
              <div className="flex justify-center items-center py-12">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                <span className="ml-3 text-gray-600">Chargement des analytics...</span>
                </div>
            ) : analytics ? (
              <div className="space-y-6">
                {/* Onglets Analytics */}
                <div className="border-b border-gray-200">
                  <nav className="-mb-px flex space-x-8">
                    <button
                      className="py-2 px-1 border-b-2 font-medium text-sm border-blue-500 text-blue-600"
                    >
                      Vue d&apos;ensemble
                    </button>

                  </nav>
                </div>

                {/* Contenu de la Vue d'ensemble */}
                <div className="space-y-6">
                  {/* Nouveau composant avec de vraies données */}
                  <RealAnalyticsCharts />
                </div>


                    </div>
                  ) : (
              <Card className="p-8 text-center rounded-2xl">
                <div className="flex flex-col items-center space-y-4">
                  <AlertCircle className="h-16 w-16 text-red-400" />
                  <h3 className="text-xl font-semibold text-gray-900">Erreur de chargement</h3>
                  <p className="text-gray-600 max-w-md">
                    Impossible de charger les analytics. Veuillez réessayer.
                  </p>
                  <Button onClick={loadAnalytics} className="bg-blue-600 hover:bg-blue-700 rounded-xl">
                    <RefreshCw className="h-4 h-4 mr-2" />
                    Réessayer
                  </Button>
                    </div>
              </Card>
                  )}
                </div>
        </>
      )}

      {/* Assignment Modal */}
      {selectedTest && (
        <AssignmentModal
          isOpen={showAssignmentModal}
          onClose={() => setShowAssignmentModal(false)}
          testTitle={selectedTest.title}
          onSubmit={handleAssignmentSubmit}
          classes={classes}
          students={students}
          isLoadingClasses={isLoadingClasses}
          isLoadingStudents={isLoadingStudents}
        />
      )}
      </div>
    </div>
  );
}
