'use client';

import React, { useState } from 'react';
import { ArrowLeft, Brain, Target, Clock, Users, BookOpen, Zap, Lightbulb } from 'lucide-react';
import Link from 'next/link';
import { frenchAIService } from '@/services';
import { QuestionValidation, QuestionValidationResult, GenerationStats } from '@/components';
import { useAuth } from '@/hooks/useAuthSimple';

interface TestConfig {
  subject: string;
  level: string;
  duration: number;
  questionCount: number;
  difficultyRange: [number, number];
  topics: string[];
  learningObjectives: string[];
  adaptiveType: 'cognitive' | 'performance' | 'hybrid';
}

export default function CreateAdaptiveTest() {
  const { user, token } = useAuth();
  const [step, setStep] = useState(1);
  const [testConfig, setTestConfig] = useState<TestConfig>({
    subject: '',
    level: '',
    duration: 30,
    questionCount: 20,
    difficultyRange: [3, 7],
    topics: [],
    learningObjectives: [],
    adaptiveType: 'hybrid'
  });

  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedTest, setGeneratedTest] = useState<any>(null);
  const [validationResult, setValidationResult] = useState<QuestionValidationResult | null>(null);

  const subjects = [
    'Mathématiques', 'Français', 'Histoire', 'Géographie', 'Sciences', 
    'Anglais', 'Espagnol', 'Physique', 'Chimie', 'Biologie'
  ];

  const levels = ['Débutant (1-3)', 'Intermédiaire (4-6)', 'Avancé (7-9)', 'Expert (10-12)'];

  const adaptiveTypes = [
    { value: 'cognitive', label: 'Cognitif', description: 'Adapte selon le style d\'apprentissage' },
    { value: 'performance', label: 'Performance', description: 'Adapte selon les résultats en temps réel' },
    { value: 'hybrid', label: 'Hybride', description: 'Combine les deux approches' }
  ];

  const handleNext = () => {
    if (step < 4) setStep(step + 1);
  };

  const handleBack = () => {
    if (step > 1) setStep(step - 1);
  };

  // La fonction generateRealisticQuestion a été remplacée par le service IA français

  const generateTestWithAI = async () => {
    setIsGenerating(true);
    
    try {
      console.log('🚀 Début de la génération IA...');
      console.log('📋 Configuration:', testConfig);
      
      // Utiliser le service IA français spécialisé
      const aiResponse = await frenchAIService.generateQuestions({
        subject: testConfig.subject,
        level: testConfig.level,
        questionCount: testConfig.questionCount,
        topics: testConfig.topics,
        learningObjectives: testConfig.learningObjectives
      });
      
      if (aiResponse.success) {
        console.log('✅ Questions générées avec succès:', aiResponse.questions.length);
        
        // Optimiser la distribution des difficultés
        const optimizedQuestions = frenchAIService.optimizeDifficultyDistribution(
          aiResponse.questions, 
          testConfig.questionCount
        );
        
        // Valider l'unicité des questions
        const uniquenessCheck = frenchAIService.validateQuestionUniqueness(optimizedQuestions);
        
        if (!uniquenessCheck.isValid) {
          console.warn('⚠️ Doublons détectés:', uniquenessCheck.duplicates);
          // Régénérer des variantes pour les doublons
          const uniqueQuestions = frenchAIService.generateIntelligentVariants(
            optimizedQuestions[0], 
            testConfig.questionCount
          );
          optimizedQuestions.splice(0, optimizedQuestions.length, ...uniqueQuestions);
          console.log('🔄 Variantes générées pour éviter les doublons');
        }
        
                const generatedTestData = {
          id: Date.now(),
          title: `Test ${testConfig.subject} - ${testConfig.level}`,
          subject: testConfig.subject,
          description: `Test adaptatif généré par ${aiResponse.generatedBy} pour ${testConfig.subject} - ${testConfig.level}`,
          difficulty_range_min: testConfig.difficultyRange[0],
          difficulty_range_max: testConfig.difficultyRange[1],
          estimated_duration: testConfig.duration,
          is_active: false,
          created_at: new Date().toISOString().split('T')[0],
          question_count: testConfig.questionCount,
          student_count: 0,
          questions: optimizedQuestions.map((q, index) => ({
            id: q.id,
            question: q.question,
            type: 'multiple_choice',
            difficulty: q.difficulty,
            options: q.options,
            correctAnswer: q.correctAnswer,
            explanation: q.explanation,
            learningObjective: q.learningObjective,
            topic: q.topic
          })),
          adaptiveRules: {
            difficultyAdjustment: 'progressive',
            questionSelection: 'intelligent',
            feedbackType: 'immediate'
          },
          generationInfo: {
            generatedBy: aiResponse.generatedBy,
            fallbackUsed: aiResponse.fallbackUsed,
            uniquenessValid: uniquenessCheck.isValid,
            questionCount: optimizedQuestions.length
          }
        };
        
        console.log('🎯 Test généré avec succès:', generatedTestData);
        setGeneratedTest(generatedTestData);
        setIsGenerating(false);
        setStep(5); // Afficher le test généré
        
        // Afficher les informations de génération
        if (aiResponse.fallbackUsed) {
          console.log('🔄 Test généré avec la banque locale étendue');
        } else {
          console.log('🤖 Test généré par IA avec succès');
        }
      } else {
        throw new Error('Échec de la génération des questions');
      }
      
    } catch (error) {
      console.error('❌ Erreur lors de la génération IA:', error);
      
      // Fallback vers la génération locale
      console.log('🔄 Utilisation du fallback local...');
      const fallbackQuestions = generateFallbackQuestions();
      
      const fallbackTestData = {
        id: Date.now(),
        title: `Test ${testConfig.subject} - ${testConfig.level}`,
        subject: testConfig.subject,
        description: `Test adaptatif généré localement pour ${testConfig.subject} - ${testConfig.level}`,
        difficulty_range_min: testConfig.difficultyRange[0],
        difficulty_range_max: testConfig.difficultyRange[1],
        estimated_duration: testConfig.duration,
        is_active: false,
        created_at: new Date().toISOString().split('T')[0],
        question_count: testConfig.questionCount,
        student_count: 0,
        questions: fallbackQuestions,
        adaptiveRules: {
          difficultyAdjustment: 'progressive',
          questionSelection: 'intelligent',
          feedbackType: 'immediate'
        },
        generationInfo: {
          generatedBy: 'Fallback local',
          fallbackUsed: true,
          uniquenessValid: true,
          questionCount: fallbackQuestions.length
        }
      };
      
      console.log('🎯 Test de fallback généré:', fallbackTestData);
      setGeneratedTest(fallbackTestData);
      setIsGenerating(false);
      setStep(5);
    }
  };

  // Fonction de fallback pour la génération locale
  const generateFallbackQuestions = () => {
    console.log('🔄 Génération de questions de fallback...');
    
    try {
      // Utiliser la banque de questions françaises étendue
      const { generateUniqueQuestions } = require('@/data');
      const fallbackQuestions = generateUniqueQuestions(testConfig.level, testConfig.questionCount);
      
      console.log(`✅ ${fallbackQuestions.length} questions de fallback générées`);
      return fallbackQuestions.map((q, index) => ({
        id: q.id,
        question: q.question,
        type: 'multiple_choice',
        difficulty: q.difficulty,
        options: q.options,
        correctAnswer: q.correctAnswer,
        explanation: q.explanation,
        learningObjective: q.learningObjective,
        topic: q.topic
      }));
      
    } catch (error) {
      console.error('❌ Erreur lors de la génération de fallback:', error);
      
      // Fallback ultime avec questions de base
      const baseQuestions = [
        {
          question: "Quel est l'article correct ? '___ chat'",
          options: ["Le", "La", "Les", "L'"],
          correctAnswer: 0,
          explanation: "Le mot 'chat' est masculin singulier, donc on utilise 'Le'",
          difficulty: 1,
          learningObjective: "Reconnaître les articles définis masculins"
        },
        {
          question: "Quel est l'article correct ? '___ maison'",
          options: ["Le", "La", "Les", "L'"],
          correctAnswer: 1,
          explanation: "Le mot 'maison' est féminin singulier, donc on utilise 'La'",
          difficulty: 1,
          learningObjective: "Reconnaître les articles définis féminins"
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
        },
        {
          question: "Dans la phrase 'Le chat mange', quel est le sujet ?",
          options: ["Le", "chat", "mange", "Le chat"],
          correctAnswer: 1,
          explanation: "Le sujet est 'chat' car c'est ce qui fait l'action de manger",
          difficulty: 2,
          learningObjective: "Identifier le sujet d'une phrase simple"
        }
      ];
      
      // Générer des questions uniques en utilisant la banque étendue
      const questions = [];
      for (let i = 0; i < testConfig.questionCount; i++) {
        const baseQuestion = baseQuestions[i % baseQuestions.length];
        const variant = {
          id: i + 1,
          question: baseQuestion.question.replace(/chat/g, ['chien', 'oiseau', 'poisson'][i % 3]),
          type: 'multiple_choice',
          options: baseQuestion.options,
          correctAnswer: baseQuestion.correctAnswer,
          explanation: baseQuestion.explanation,
          difficulty: Math.min(10, Math.max(1, baseQuestion.difficulty + (i % 3))),
          learningObjective: testConfig.learningObjectives[i % testConfig.learningObjectives.length] || baseQuestion.learningObjective,
          topic: 'Grammaire de base'
        };
        questions.push(variant);
      }
      
      return questions;
    }
  };

  const handlePreviewTest = (test: any) => {
    console.log('🚀 handlePreviewTest appelé avec:', test);
    
    if (!test) {
      console.error('❌ Test est undefined ou null');
      return;
    }
    
    if (!test.questions || !Array.isArray(test.questions)) {
      console.error('❌ Test.questions est invalide:', test.questions);
      return;
    }
    
    // Créer un ID unique pour ce test de prévisualisation
    const previewId = `preview_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    console.log('🔑 ID de prévisualisation généré:', previewId);
    
    // Stocker le test en localStorage avec un ID unique
    const testToStore = {
      ...test,
      previewId: previewId,
      storedAt: new Date().toISOString()
    };
    
    localStorage.setItem(`previewTest_${previewId}`, JSON.stringify(testToStore));
    
    // Stocker l'ID de prévisualisation actuel
    localStorage.setItem('currentPreviewId', previewId);
    
    console.log('💾 Test stocké en localStorage avec la clé:', `previewTest_${previewId}`);
    console.log('🔍 Prévisualisation du test:', {
      id: previewId,
      title: test.title,
      subject: test.subject,
      questionCount: test.questions?.length || 0
    });
    console.log('🔍 Structure complète du test stocké:', testToStore);
    console.log('🔍 Première question stockée:', test.questions?.[0]);
    
    // Vérifier que le test a bien été stocké
    const storedTest = localStorage.getItem(`previewTest_${previewId}`);
    if (storedTest) {
      console.log('✅ Test vérifié en localStorage:', JSON.parse(storedTest));
    } else {
      console.error('❌ Test non trouvé en localStorage après stockage');
    }
    
    // Ouvrir dans un nouvel onglet
    const previewUrl = `/dashboard/teacher/adaptive-evaluation/preview?previewId=${previewId}`;
    console.log('🌐 Ouverture de l\'URL:', previewUrl);
    window.open(previewUrl, '_blank');
  };

  const handleActivateTest = async (test: any) => {
    try {
      // Vérifier que l'utilisateur est connecté EN PREMIER
      if (!user || !token) {
        alert('❌ Utilisateur non connecté. Veuillez vous reconnecter.');
        return;
      }
      
      // Debug de l'utilisateur
      console.log('🔥 [DEBUG] User object complet:', user);
      console.log('🔥 [DEBUG] User ID:', user?.id);
      console.log('🔥 [DEBUG] Token:', token);
      
      // Appeler l'API backend pour créer le test
      console.log('🚀 Envoi de la requête de création du test...');
      console.log('📝 Données envoyées:', {
        title: test.title,
        subject: test.subject,
        description: test.description,
        difficulty_min: test.difficulty_range_min,
        difficulty_max: test.difficulty_range_max,
        estimated_duration: test.estimated_duration,
        adaptation_type: test.adaptiveType,
        learning_objectives: test.description,
        total_questions: test.question_count,
        created_by: user.id
      });
      
      console.log('🔑 Utilisateur connecté, envoi de la requête authentifiée...');

      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      };
      
      console.log("🔥 [DEBUG] Envoi de la requête à /create");
      console.log("🔥 [DEBUG] Headers:", headers);
      console.log("🔥 [DEBUG] Token:", token);
      console.log("🔥 [DEBUG] User ID:", user.id);
      console.log("🔥 [DEBUG] User object complet:", user);
      
      const requestBody = {
        title: test.title,
        subject: test.subject,
        description: test.description,
        difficulty_min: test.difficulty_range_min,
        difficulty_max: test.difficulty_range_max,
        estimated_duration: test.estimated_duration,
        adaptation_type: test.adaptiveType,
        learning_objectives: test.description,
        total_questions: test.question_count,
        created_by: user.id, // ID de l'utilisateur connecté
        questions: test.questions.map(q => ({
          question_text: q.question,
          question_type: q.type,
          difficulty_level: Math.min(q.difficulty, 10), // Limiter à 10 maximum
          learning_objective: q.learningObjective,
          options: q.options,
          correct_answer: q.options[q.correctAnswer],
          explanation: q.explanation
        }))
      };
      
      console.log("🔥 [DEBUG] Request body:", requestBody);
      
      const result = await fetch('/api/v1/adaptive-evaluation/create', {
        method: 'POST',
        headers,
        body: JSON.stringify(requestBody)
      });
      
      console.log("🔥 [DEBUG] Response status:", result.status);
      console.log("🔥 [DEBUG] Response headers:", result.headers);
      console.log("🔥 [DEBUG] Response ok:", result.ok);
      
      if (result.ok) {
        const responseData = await result.json();
        console.log('✅ Réponse du serveur:', responseData);
        
        if (responseData.success) {
          alert('✅ Test créé et activé avec succès dans la base de données !');
          
          // Stocker l'ID du test créé pour l'assignation
          const testId = responseData.test.id;
          localStorage.setItem('createdTestId', testId.toString());
          localStorage.setItem('testCreated', 'true');
          
          // Rediriger directement vers la liste des tests
          window.location.href = '/dashboard/teacher/adaptive-evaluation';
        } else {
          alert(`❌ Erreur lors de la création: ${responseData.error || 'Erreur inconnue'}`);
        }
      } else {
        console.error(`❌ Erreur HTTP ${result.status}: ${result.statusText}`);
        
        try {
          const errorData = await result.json();
          console.error('Erreur détaillée du serveur:', errorData);
          
          if (result.status === 403) {
            alert('❌ Erreur 403: Accès refusé. Vérifiez que vous êtes bien connecté en tant que professeur.');
          } else if (result.status === 401) {
            alert('❌ Erreur 401: Non authentifié. Veuillez vous reconnecter.');
          } else {
            alert(`❌ Erreur ${result.status}: ${errorData.detail || 'Erreur lors de la création du test'}`);
          }
        } catch (parseError) {
          console.error('Erreur lors du parsing de la réponse d\'erreur:', parseError);
          alert(`❌ Erreur ${result.status}: Impossible de lire le message d'erreur du serveur`);
        }
      }
    } catch (error) {
      console.error('Erreur lors de la création du test:', error);
      alert('❌ Erreur lors de la création du test. Vérifiez votre connexion.');
    }
  };

  const renderStep1 = () => (
    <div className="space-y-6">
      <div className="text-center">
        <Brain className="w-16 h-16 text-purple-600 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-gray-900">Configuration de Base</h2>
        <p className="text-gray-600">Définissez les paramètres fondamentaux de votre test adaptatif</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Matière <span className="text-red-500">*</span>
          </label>
          <select
            value={testConfig.subject}
            onChange={(e) => setTestConfig({...testConfig, subject: e.target.value})}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
          >
            <option value="">Sélectionnez une matière</option>
            {subjects.map(subject => (
              <option key={subject} value={subject}>{subject}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Niveau <span className="text-red-500">*</span>
          </label>
          <select
            value={testConfig.level}
            onChange={(e) => setTestConfig({...testConfig, level: e.target.value})}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
          >
            <option value="">Sélectionnez un niveau</option>
            {levels.map(level => (
              <option key={level} value={level}>{level}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Durée (minutes)
          </label>
          <input
            type="number"
            value={testConfig.duration}
            onChange={(e) => setTestConfig({...testConfig, duration: parseInt(e.target.value)})}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            min="10"
            max="120"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Nombre de questions
          </label>
          <input
            type="number"
            value={Number.isFinite(testConfig.questionCount as any) ? testConfig.questionCount : ''}
            onChange={(e) => {
              const raw = e.target.value;
              const next = raw === '' ? '' : Number.parseInt(raw, 10);
              setTestConfig({
                ...testConfig,
                questionCount: (Number.isNaN(next) ? 0 : (next as any))
              });
            }}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            min="5"
            max="50"
          />
        </div>
      </div>
    </div>
  );

  const renderStep2 = () => (
    <div className="space-y-6">
      <div className="text-center">
        <Target className="w-16 h-16 text-blue-600 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-gray-900">Objectifs d'Apprentissage</h2>
        <p className="text-gray-600">Définissez ce que vos élèves doivent maîtriser</p>
      </div>

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Thèmes à couvrir
          </label>
          <div className="grid grid-cols-2 gap-2">
            {['Théorie', 'Pratique', 'Application', 'Analyse', 'Synthèse', 'Évaluation'].map(topic => (
              <label key={topic} className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={testConfig.topics.includes(topic)}
                  onChange={(e) => {
                    if (e.target.checked) {
                      setTestConfig({...testConfig, topics: [...testConfig.topics, topic]});
                    } else {
                      setTestConfig({...testConfig, topics: testConfig.topics.filter(t => t !== topic)});
                    }
                  }}
                  className="rounded border-gray-300 text-purple-600 focus:ring-purple-500"
                />
                <span className="text-sm text-gray-700">{topic}</span>
              </label>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Objectifs d'apprentissage spécifiques
          </label>
          <textarea
            placeholder="Ex: L'élève doit être capable de résoudre des équations du premier degré..."
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            rows={4}
            value={testConfig.learningObjectives.join('\n')}
            onChange={(e) => setTestConfig({...testConfig, learningObjectives: e.target.value.split('\n').filter(obj => obj.trim())})}
          />
        </div>
      </div>
    </div>
  );

  const renderStep3 = () => (
    <div className="space-y-6">
      <div className="text-center">
        <Zap className="w-16 h-16 text-yellow-600 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-gray-900">Configuration Adaptative</h2>
        <p className="text-gray-600">Personnalisez l'algorithme d'adaptation de votre test</p>
      </div>

      <div className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Type d'adaptation
          </label>
          <div className="grid grid-cols-1 gap-3">
            {adaptiveTypes.map(type => (
              <label key={type.value} className="flex items-start space-x-3 p-3 border border-gray-200 rounded-lg cursor-pointer hover:border-purple-300">
                <input
                  type="radio"
                  name="adaptiveType"
                  value={type.value}
                  checked={testConfig.adaptiveType === type.value}
                  onChange={(e) => setTestConfig({...testConfig, adaptiveType: e.target.value as any})}
                  className="mt-1 rounded-full border-gray-300 text-purple-600 focus:ring-purple-500"
                />
                <div>
                  <div className="font-medium text-gray-900">{type.label}</div>
                  <div className="text-sm text-gray-600">{type.description}</div>
                </div>
              </label>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Plage de difficulté
          </label>
          <div className="flex items-center space-x-4">
            <input
              type="range"
              min="1"
              max="10"
              value={testConfig.difficultyRange[0]}
              onChange={(e) => setTestConfig({...testConfig, difficultyRange: [parseInt(e.target.value), testConfig.difficultyRange[1]]})}
              className="flex-1"
            />
            <span className="text-sm text-gray-600 min-w-[60px]">
              {testConfig.difficultyRange[0]} - {testConfig.difficultyRange[1]}
            </span>
          </div>
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>Très facile</span>
            <span>Très difficile</span>
          </div>
        </div>
      </div>
    </div>
  );

  const renderStep4 = () => (
    <div className="space-y-6">
      <div className="text-center">
        <Lightbulb className="w-16 h-16 text-green-600 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-gray-900">Récapitulatif & Génération</h2>
        <p className="text-gray-600">Vérifiez vos paramètres et lancez la génération IA</p>
      </div>

      <div className="bg-gray-50 rounded-lg p-6 space-y-4">
        <h3 className="font-semibold text-gray-900">Configuration du Test</h3>
        
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <span className="font-medium text-gray-700">Matière:</span>
            <span className="ml-2 text-gray-900">{testConfig.subject}</span>
          </div>
          <div>
            <span className="font-medium text-gray-700">Niveau:</span>
            <span className="ml-2 text-gray-900">{testConfig.level}</span>
          </div>
          <div>
            <span className="font-medium text-gray-700">Durée:</span>
            <span className="ml-2 text-gray-900">{testConfig.duration} min</span>
          </div>
          <div>
            <span className="font-medium text-gray-700">Questions:</span>
            <span className="ml-2 text-gray-900">{testConfig.questionCount}</span>
          </div>
          <div>
            <span className="font-medium text-gray-700">Difficulté:</span>
            <span className="ml-2 text-gray-900">{testConfig.difficultyRange[0]}-{testConfig.difficultyRange[1]}</span>
          </div>
          <div>
            <span className="font-medium text-gray-700">Type:</span>
            <span className="ml-2 text-gray-900 capitalize">{testConfig.adaptiveType}</span>
          </div>
        </div>

        <div className="pt-4">
          <h4 className="font-medium text-gray-700 mb-2">Thèmes sélectionnés:</h4>
          <div className="flex flex-wrap gap-2">
            {testConfig.topics.map(topic => (
              <span key={topic} className="px-2 py-1 bg-purple-100 text-purple-800 rounded-full text-xs">
                {topic}
              </span>
            ))}
          </div>
        </div>
      </div>

      <div className="text-center">
        <button
          onClick={generateTestWithAI}
          disabled={isGenerating}
          className="px-8 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg font-medium hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
        >
          {isGenerating ? (
            <div className="flex items-center space-x-2">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              <span>Génération en cours...</span>
            </div>
          ) : (
            <div className="flex items-center space-x-2">
              <Brain className="w-5 h-5" />
              <span>Générer le Test avec l'IA</span>
            </div>
          )}
        </button>
      </div>
    </div>
  );

  const renderStep5 = () => (
    <div className="space-y-6">
      <div className="text-center">
        <BookOpen className="w-16 h-16 text-green-600 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-gray-900">Test Généré par IA</h2>
        <p className="text-gray-600">Votre test adaptatif a été créé intelligemment</p>
      </div>

      {generatedTest && (
        <div className="space-y-6">
          <div className="bg-white border border-gray-200 rounded-lg p-6">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="text-xl font-semibold text-gray-900">{generatedTest.title}</h3>
                <p className="text-gray-600">
                  Test généré par {generatedTest.generationInfo?.generatedBy || 'IA'} le {new Date().toLocaleDateString()}
                </p>
                {generatedTest.generationInfo && (
                  <div className="mt-2 flex items-center space-x-4 text-sm">
                    <span className={`px-2 py-1 rounded-full ${
                      generatedTest.generationInfo.fallbackUsed 
                        ? 'bg-yellow-100 text-yellow-800' 
                        : 'bg-green-100 text-green-800'
                    }`}>
                      {generatedTest.generationInfo.fallbackUsed ? '🔄 Banque locale' : '🤖 IA'}
                    </span>
                    <span className={`px-2 py-1 rounded-full ${
                      generatedTest.generationInfo.uniquenessValid 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {generatedTest.generationInfo.uniquenessValid ? '✅ Questions uniques' : '⚠️ Doublons détectés'}
                    </span>
                    <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full">
                      📊 {generatedTest.generationInfo.questionCount} questions
                    </span>
                  </div>
                )}
              </div>
              {generatedTest && generatedTest.questions && generatedTest.questions.length > 0 && (
                             <div className="flex space-x-2">
                 <button 
                   onClick={() => handlePreviewTest(generatedTest)}
                   className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                 >
                   Prévisualiser
                 </button>
                 <button 
                   onClick={() => handleActivateTest(generatedTest)}
                   className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                 >
                   Activer
                 </button>
               </div>
              )}
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <div className="text-center p-3 bg-gray-50 rounded-lg">
                <div className="text-2xl font-bold text-blue-600">{generatedTest.questions.length}</div>
                <div className="text-sm text-gray-600">Questions</div>
              </div>
              <div className="text-center p-3 bg-gray-50 rounded-lg">
                <div className="text-2xl font-bold text-green-600">{testConfig.duration}</div>
                <div className="text-sm text-gray-600">Minutes</div>
              </div>
              <div className="text-center p-3 bg-gray-50 rounded-lg">
                <div className="text-2xl font-bold text-purple-600">{testConfig.difficultyRange[0]}-{testConfig.difficultyRange[1]}</div>
                <div className="text-sm text-gray-600">Difficulté</div>
              </div>
              <div className="text-center p-3 bg-gray-50 rounded-lg">
                <div className="text-2xl font-bold text-orange-600">{testConfig.adaptiveType}</div>
                <div className="text-sm text-gray-600">Type</div>
              </div>
            </div>

            {/* Composant de validation des questions */}
            <div className="mb-6">
              <QuestionValidation 
                questions={generatedTest.questions || []}
                onValidationComplete={setValidationResult}
              />
            </div>

            {/* Composant de statistiques de génération */}
            <div className="mb-6">
              <GenerationStats
                generatedBy={generatedTest.generationInfo?.generatedBy || 'Système'}
                fallbackUsed={generatedTest.generationInfo?.fallbackUsed || false}
                uniquenessValid={generatedTest.generationInfo?.uniquenessValid || true}
                questionCount={generatedTest.questions?.length || 0}
                topics={testConfig.topics}
                learningObjectives={testConfig.learningObjectives}
                qualityScore={validationResult?.qualityScore}
              />
            </div>

            <div className="space-y-4">
              <h4 className="font-semibold text-gray-900">Questions générées :</h4>
              {generatedTest.questions.slice(0, 3).map((question: any, index: number) => (
                <div key={question.id} className="p-3 bg-gray-50 rounded-lg">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="font-medium text-gray-900">Question {question.id}</div>
                      <div className="text-sm text-gray-600 mt-1">{question.question}</div>
                      <div className="text-xs text-gray-500 mt-2">
                        Difficulté: {question.difficulty} | Objectif: {question.learningObjective}
                      </div>
                    </div>
                    <div className="ml-4 text-xs text-gray-500">
                      {question.type}
                    </div>
                  </div>
                </div>
              ))}
              {generatedTest.questions.length > 3 && (
                <div className="text-center text-gray-500">
                  ... et {generatedTest.questions.length - 3} autres questions
                </div>
              )}
            </div>
          </div>

          <div className="flex justify-center space-x-4">
            <button
              onClick={() => setStep(1)}
              className="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Créer un autre test
            </button>
            <Link
              href="/dashboard/teacher/adaptive-evaluation"
              className="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
            >
              Retour aux tests
            </Link>
          </div>
        </div>
      )}
    </div>
  );

  const steps = [
    { title: 'Configuration', icon: Brain },
    { title: 'Objectifs', icon: Target },
    { title: 'Adaptation', icon: Zap },
    { title: 'Génération', icon: Lightbulb },
    { title: 'Résultat', icon: BookOpen }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto py-8 px-4">
        {/* Header */}
        <div className="mb-8">
          <Link
            href="/dashboard/teacher/adaptive-evaluation"
            className="inline-flex items-center text-purple-600 hover:text-purple-700 mb-4"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Retour à l'évaluation adaptative
          </Link>
          <h1 className="text-3xl font-bold text-gray-900">Créer un Test Adaptatif avec IA</h1>
          <p className="text-gray-600 mt-2">
            Utilisez l'intelligence artificielle pour générer des tests personnalisés et adaptatifs
          </p>
        </div>

        {/* Progress Steps */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            {steps.map((stepItem, index) => {
              const Icon = stepItem.icon;
              const isActive = step === index + 1;
              const isCompleted = step > index + 1;
              
              return (
                <div key={index} className="flex items-center">
                  <div className={`flex items-center justify-center w-10 h-10 rounded-full border-2 ${
                    isActive ? 'border-purple-600 bg-purple-600 text-white' :
                    isCompleted ? 'border-green-600 bg-green-600 text-white' :
                    'border-gray-300 bg-white text-gray-400'
                  }`}>
                    {isCompleted ? (
                      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                    ) : (
                      <Icon className="w-5 h-5" />
                    )}
                  </div>
                  {index < steps.length - 1 && (
                    <div className={`w-16 h-0.5 mx-2 ${
                      isCompleted ? 'bg-green-600' : 'bg-gray-300'
                    }`} />
                  )}
                </div>
              );
            })}
          </div>
          
          <div className="flex justify-between mt-2 text-sm text-gray-600">
            {steps.map((stepItem, index) => (
              <span key={index} className={`${
                step === index + 1 ? 'text-purple-600 font-medium' : ''
              }`}>
                {stepItem.title}
              </span>
            ))}
          </div>
        </div>

        {/* Step Content */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
          {step === 1 && renderStep1()}
          {step === 2 && renderStep2()}
          {step === 3 && renderStep3()}
          {step === 4 && renderStep4()}
          {step === 5 && renderStep5()}
        </div>

        {/* Navigation */}
        {step < 4 && (
          <div className="flex justify-between mt-8">
            <button
              onClick={handleBack}
              disabled={step === 1}
              className="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              Précédent
            </button>
            <button
              onClick={handleNext}
              disabled={!testConfig.subject || !testConfig.level}
              className="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              Suivant
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
