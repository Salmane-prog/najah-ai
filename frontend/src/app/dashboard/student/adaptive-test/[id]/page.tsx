'use client';

import React, { useState, useEffect, useRef } from 'react';
import { ArrowLeft, Brain, Target, Clock, TrendingUp, TrendingDown, Zap, Eye, BarChart3 } from 'lucide-react';
import Link from 'next/link';
import { AdaptiveAlgorithmEngine, StudentResponse } from '../../../../../services/adaptiveAlgorithmService';

interface Question {
  id: number;
  question: string;
  type: string;
  difficulty: number;
  options: string[];
  correctAnswer: number;
  explanation: string;
  learningObjective: string;
}

interface Test {
  id: number;
  title: string;
  subject: string;
  description: string;
  difficulty_range_min: number;
  difficulty_range_max: number;
  estimated_duration: number;
  question_count: number;
  questions: Question[];
}

export default function AdaptiveTestPage({ params }: { params: { id: string } }) {
  const [test, setTest] = useState<Test | null>(null);
  const [currentQuestion, setCurrentQuestion] = useState<Question | null>(null);
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [isAnswered, setIsAnswered] = useState(false);
  const [showExplanation, setShowExplanation] = useState(false);
  const [adaptiveEngine, setAdaptiveEngine] = useState<AdaptiveAlgorithmEngine | null>(null);
  const [questionStartTime, setQuestionStartTime] = useState<number>(0);
  const [showAdaptiveInsights, setShowAdaptiveInsights] = useState(false);
  const [nextQuestionRecommendation, setNextQuestionRecommendation] = useState<any>(null);
  const [testCompleted, setTestCompleted] = useState(false);
  const [finalResults, setFinalResults] = useState<any>(null);

  const questionTimerRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    // Simuler la récupération du test depuis une API
    const mockTest: Test = {
      id: parseInt(params.id),
      title: "Test Adaptatif Français - Grammaire",
      subject: "Français",
      description: "Test intelligent qui s'adapte à votre niveau",
      difficulty_range_min: 3,
      difficulty_range_max: 8,
      estimated_duration: 25,
      question_count: 15,
      questions: [
        {
          id: 1,
          question: "Quelle est la forme correcte du verbe 'aller' à la 3ème personne du pluriel du présent ?",
          type: "multiple_choice",
          difficulty: 4,
          options: ["vont", "allez", "allons", "va"],
          correctAnswer: 0,
          explanation: "Le verbe 'aller' à la 3ème personne du pluriel du présent se conjugue 'vont'.",
          learningObjective: "Conjugaison des verbes irréguliers"
        },
        {
          id: 2,
          question: "Dans la phrase 'Les enfants jouent dans le jardin', quel est le sujet ?",
          type: "multiple_choice",
          difficulty: 3,
          options: ["jouent", "dans", "le jardin", "Les enfants"],
          correctAnswer: 3,
          explanation: "Le sujet est 'Les enfants' car c'est ce qui fait l'action de jouer.",
          learningObjective: "Identification du sujet"
        },
        {
          id: 3,
          question: "Quelle est la règle d'accord pour l'adjectif qualificatif ?",
          type: "multiple_choice",
          difficulty: 6,
          options: ["Il s'accorde toujours avec le nom", "Il ne s'accorde jamais", "Il s'accorde selon le contexte", "Il s'accorde avec le verbe"],
          correctAnswer: 0,
          explanation: "L'adjectif qualificatif s'accorde toujours en genre et en nombre avec le nom qu'il qualifie.",
          learningObjective: "Accord des adjectifs"
        },
        {
          id: 4,
          question: "Qu'est-ce qu'un complément d'objet direct (COD) ?",
          type: "multiple_choice",
          difficulty: 5,
          options: ["Un mot qui complète le sujet", "Un mot qui complète le verbe sans préposition", "Un mot qui indique le temps", "Un mot qui indique le lieu"],
          correctAnswer: 1,
          explanation: "Le COD complète le verbe sans préposition et répond à la question 'quoi ?' ou 'qui ?'.",
          learningObjective: "Fonctions grammaticales"
        },
        {
          id: 5,
          question: "Comment se forme le passé composé avec l'auxiliaire 'être' ?",
          type: "multiple_choice",
          difficulty: 7,
          options: ["Auxiliaire + participe passé", "Auxiliaire + infinitif", "Auxiliaire + radical", "Auxiliaire + terminaison"],
          correctAnswer: 0,
          explanation: "Le passé composé se forme avec l'auxiliaire 'être' suivi du participe passé qui s'accorde avec le sujet.",
          learningObjective: "Formation des temps composés"
        }
      ]
    };

    setTest(mockTest);
    
    // Initialiser le moteur d'adaptation
    const engine = new AdaptiveAlgorithmEngine(
      mockTest.questions,
      [mockTest.difficulty_range_min, mockTest.difficulty_range_max]
    );
    setAdaptiveEngine(engine);
    
    // Commencer avec la première question
    setCurrentQuestion(mockTest.questions[0]);
    setQuestionStartTime(Date.now());
  }, [params.id]);

  useEffect(() => {
    if (currentQuestion) {
      setQuestionStartTime(Date.now());
      setSelectedAnswer(null);
      setIsAnswered(false);
      setShowExplanation(false);
    }
  }, [currentQuestion]);

  const handleAnswerSelect = (answerIndex: number) => {
    if (isAnswered) return;
    setSelectedAnswer(answerIndex);
  };

  const handleSubmitAnswer = () => {
    if (selectedAnswer === null || !currentQuestion || !adaptiveEngine) return;

    const timeSpent = (Date.now() - questionStartTime) / 1000; // en secondes
    const isCorrect = selectedAnswer === currentQuestion.correctAnswer;

    // Traiter la réponse avec l'algorithme d'adaptation
    const response: StudentResponse = {
      questionId: currentQuestion.id,
      selectedAnswer,
      correctAnswer: currentQuestion.correctAnswer,
      timeSpent,
      difficulty: currentQuestion.difficulty,
      isCorrect
    };

    adaptiveEngine.processResponse(response);
    setIsAnswered(true);
    setShowExplanation(true);

    // Obtenir la recommandation pour la prochaine question
    const recommendation = adaptiveEngine.selectNextQuestion();
    setNextQuestionRecommendation(recommendation);

    // Afficher les insights adaptatifs
    setTimeout(() => {
      setShowAdaptiveInsights(true);
    }, 2000);
  };

  const handleNextQuestion = () => {
    if (!adaptiveEngine || !nextQuestionRecommendation) {
      // Test terminé
      setTestCompleted(true);
      const results = adaptiveEngine?.generatePersonalizedFeedback();
      setFinalResults(results);
      return;
    }

    // Trouver la prochaine question recommandée
    const nextQuestion = test?.questions.find(q => q.id === nextQuestionRecommendation.questionId);
    if (nextQuestion) {
      setCurrentQuestion(nextQuestion);
      setNextQuestionRecommendation(null);
      setShowAdaptiveInsights(false);
    }
  };

  const getDifficultyColor = (difficulty: number) => {
    if (difficulty <= 4) return 'text-green-600 bg-green-100';
    if (difficulty <= 6) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const getDifficultyLabel = (difficulty: number) => {
    if (difficulty <= 3) return 'Facile';
    if (difficulty <= 5) return 'Intermédiaire';
    if (difficulty <= 7) return 'Difficile';
    return 'Très difficile';
  };

  if (!test || !currentQuestion) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement du test adaptatif...</p>
        </div>
      </div>
    );
  }

  if (testCompleted && finalResults) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-4xl mx-auto py-8 px-4">
          <div className="mb-8">
            <Link
              href="/dashboard/student"
              className="inline-flex items-center text-purple-600 hover:text-purple-700 mb-4"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Retour au tableau de bord
            </Link>
            <h1 className="text-3xl font-bold text-gray-900">Test Terminé !</h1>
            <p className="text-gray-600 mt-2">Analyse intelligente de vos performances</p>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
            <div className="text-center mb-8">
              <Brain className="w-20 h-20 text-purple-600 mx-auto mb-4" />
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Analyse Adaptative Complète</h2>
              <p className="text-gray-600">L'IA a analysé vos réponses pour personnaliser votre apprentissage</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <div className="text-2xl font-bold text-blue-600">
                  {adaptiveEngine?.getProgress().percentage}%
                </div>
                <div className="text-sm text-gray-600">Score Final</div>
              </div>
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <div className="text-2xl font-bold text-green-600">
                  {Math.round((adaptiveEngine?.getConfidenceLevel() || 0) * 100)}%
                </div>
                <div className="text-sm text-gray-600">Niveau de Confiance</div>
              </div>
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <div className="text-2xl font-bold text-purple-600">
                  {adaptiveEngine?.getCurrentDifficulty().toFixed(1)}
                </div>
                <div className="text-sm text-gray-600">Difficulté Finale</div>
              </div>
            </div>

            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">Message Personnalisé</h3>
                <div className="p-4 bg-purple-50 rounded-lg">
                  <p className="text-purple-800">{finalResults.message}</p>
                </div>
              </div>

              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">Suggestions d'Amélioration</h3>
                <ul className="space-y-2">
                  {finalResults.suggestions.map((suggestion, index) => (
                    <li key={index} className="flex items-start space-x-2">
                      <div className="w-2 h-2 bg-purple-600 rounded-full mt-2 flex-shrink-0"></div>
                      <span className="text-gray-700">{suggestion}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">Prochaines Étapes</h3>
                <ul className="space-y-2">
                  {finalResults.nextSteps.map((step, index) => (
                    <li key={index} className="flex items-start space-x-2">
                      <div className="w-2 h-2 bg-green-600 rounded-full mt-2 flex-shrink-0"></div>
                      <span className="text-gray-700">{step}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            <div className="mt-8 flex justify-center space-x-4">
              <Link
                href="/dashboard/student"
                className="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Retour au Tableau de Bord
              </Link>
              <button
                onClick={() => window.location.reload()}
                className="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
              >
                Recommencer le Test
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto py-8 px-4">
        {/* Header */}
        <div className="mb-8">
          <Link
            href="/dashboard/student"
            className="inline-flex items-center text-purple-600 hover:text-purple-700 mb-4"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Retour au tableau de bord
          </Link>
          <h1 className="text-3xl font-bold text-gray-900">{test.title}</h1>
          <p className="text-gray-600 mt-2">{test.description}</p>
        </div>

        {/* Informations du test et insights adaptatifs */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          {/* Informations du test */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                <div>
                  <div className="text-2xl font-bold text-blue-600">{test.question_count}</div>
                  <div className="text-sm text-gray-600">Questions</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-green-600">{test.estimated_duration}</div>
                  <div className="text-sm text-gray-600">Minutes</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-purple-600">
                    {test.difficulty_range_min}-{test.difficulty_range_max}
                  </div>
                  <div className="text-sm text-gray-600">Difficulté</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-orange-600">{test.subject}</div>
                  <div className="text-sm text-gray-600">Matière</div>
                </div>
              </div>
            </div>
          </div>

          {/* Insights adaptatifs en temps réel */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <Brain className="w-5 h-5 mr-2 text-purple-600" />
              IA Adaptative
            </h3>
            
            {adaptiveEngine && (
              <div className="space-y-4">
                <div className="text-center p-3 bg-purple-50 rounded-lg">
                  <div className="text-lg font-bold text-purple-600">
                    {Math.round(adaptiveEngine.getConfidenceLevel() * 100)}%
                  </div>
                  <div className="text-xs text-purple-600">Confiance</div>
                </div>
                
                <div className="text-center p-3 bg-blue-50 rounded-lg">
                  <div className="text-lg font-bold text-blue-600">
                    {adaptiveEngine.getCurrentDifficulty().toFixed(1)}
                  </div>
                  <div className="text-xs text-blue-600">Difficulté Actuelle</div>
                </div>
                
                <div className="text-center p-3 bg-green-50 rounded-lg">
                  <div className="text-lg font-bold text-green-600">
                    {adaptiveEngine.getProgress().percentage}%
                  </div>
                  <div className="text-xs text-green-600">Progression</div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Question actuelle */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 mb-6">
          <div className="mb-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-900">
                Question {currentQuestion.id}
              </h2>
              <div className="flex items-center space-x-4">
                <span className={`px-3 py-1 rounded-full text-xs font-medium ${getDifficultyColor(currentQuestion.difficulty)}`}>
                  {getDifficultyLabel(currentQuestion.difficulty)}
                </span>
                <span className="text-sm text-gray-500">
                  Niveau {currentQuestion.difficulty}
                </span>
              </div>
            </div>
            
            <p className="text-lg text-gray-700 mb-6">{currentQuestion.question}</p>
            
            <div className="space-y-3">
              {currentQuestion.options.map((option, index) => (
                <label
                  key={index}
                  className={`flex items-center p-4 border rounded-lg cursor-pointer transition-colors ${
                    selectedAnswer === index
                      ? 'border-purple-500 bg-purple-50'
                      : 'border-gray-200 hover:border-purple-300'
                  } ${isAnswered ? 'cursor-default' : ''}`}
                >
                  <input
                    type="radio"
                    name={`question-${currentQuestion.id}`}
                    value={index}
                    checked={selectedAnswer === index}
                    onChange={() => handleAnswerSelect(index)}
                    disabled={isAnswered}
                    className="mr-3 text-purple-600 focus:ring-purple-500"
                  />
                  <span className="text-gray-700">{option}</span>
                  
                  {isAnswered && index === currentQuestion.correctAnswer && (
                    <div className="ml-auto text-green-600">
                      ✓ Correct
                    </div>
                  )}
                  
                  {isAnswered && selectedAnswer === index && index !== currentQuestion.correctAnswer && (
                    <div className="ml-auto text-red-600">
                      ✗ Incorrect
                    </div>
                  )}
                </label>
              ))}
            </div>
          </div>

          {/* Bouton de soumission */}
          {!isAnswered && (
            <div className="text-center">
              <button
                onClick={handleSubmitAnswer}
                disabled={selectedAnswer === null}
                className="px-8 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                Valider la Réponse
              </button>
            </div>
          )}

          {/* Explication et bouton suivant */}
          {isAnswered && (
            <div className="space-y-4">
              <div className="p-4 bg-blue-50 rounded-lg">
                <h4 className="font-medium text-blue-900 mb-2">Explication :</h4>
                <p className="text-blue-800">{currentQuestion.explanation}</p>
              </div>
              
              <div className="text-center">
                <button
                  onClick={handleNextQuestion}
                  className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                >
                  Question Suivante
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Insights adaptatifs après réponse */}
        {showAdaptiveInsights && nextQuestionRecommendation && (
          <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg border border-purple-200 p-6">
            <div className="flex items-center mb-4">
              <Zap className="w-6 h-6 text-purple-600 mr-2" />
              <h3 className="text-lg font-semibold text-purple-900">Insight IA</h3>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <h4 className="font-medium text-purple-800 mb-2">Prochaine Question Sélectionnée</h4>
                <p className="text-purple-700 text-sm">{nextQuestionRecommendation.reason}</p>
              </div>
              
              <div>
                <h4 className="font-medium text-purple-800 mb-2">Objectif d'Apprentissage</h4>
                <p className="text-purple-700 text-sm">{nextQuestionRecommendation.learningObjective}</p>
              </div>
            </div>
            
            <div className="mt-4 p-3 bg-white rounded-lg">
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-600">Difficulté Prévue :</span>
                <span className="font-medium text-purple-600">
                  {nextQuestionRecommendation.expectedDifficulty.toFixed(1)}
                </span>
              </div>
              <div className="flex items-center justify-between text-sm mt-1">
                <span className="text-gray-600">Niveau de Confiance IA :</span>
                <span className="font-medium text-purple-600">
                  {Math.round(nextQuestionRecommendation.confidence * 100)}%
                </span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
