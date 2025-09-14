'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/hooks/useAuthSimple';
import { RemediationExerciseService, DiverseExercise } from '@/services/remediationExerciseService';
import { ArrowLeft, Clock, Target, CheckCircle, XCircle, Brain, RefreshCw } from 'lucide-react';
import { useRouter } from 'next/navigation';

interface QuizPageProps {
  params: {
    topic: string;
  };
}

export default function QuizPage({ params }: QuizPageProps) {
  const { user, token } = useAuth();
  const router = useRouter();
  // FIX: Unwrap params with React.use() as it's now a Promise in Next.js 15.4.1
  const { topic } = React.use(params);
  
  const [exercises, setExercises] = useState<DiverseExercise[]>([]);
  const [currentExerciseIndex, setCurrentExerciseIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);
  const [isAnswered, setIsAnswered] = useState(false);
  const [score, setScore] = useState(0);
  const [timeLeft, setTimeLeft] = useState(300); // 5 minutes
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (user && token) {
      loadExercises();
    }
  }, [user, token, topic]);

  useEffect(() => {
    if (timeLeft > 0 && !isAnswered) {
      const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
      return () => clearTimeout(timer);
    } else if (timeLeft === 0 && !isAnswered) {
      handleTimeout();
    }
  }, [timeLeft, isAnswered]);

  const loadExercises = async () => {
    try {
      setLoading(true);
      console.log('🎯 [QUIZ PAGE] Chargement des exercices pour le topic:', topic);
      
      // Récupérer des exercices diversifiés
      const response = await RemediationExerciseService.getDiverseExercises(
        topic,
        'facile',
        5 // 5 exercices
      );
      
      if (response.success && response.exercises.length > 0) {
        setExercises(response.exercises);
        console.log('✅ [QUIZ PAGE] Exercices chargés:', response.exercises.length);
      } else {
        // Fallback vers des exercices mock
        const mockResponse = await RemediationExerciseService.getDiverseExercises(
          topic,
          'facile',
          5,
          user?.id || 0
        );
        setExercises(mockResponse.exercises);
        console.log('⚠️ [QUIZ PAGE] Utilisation des exercices mock');
      }
    } catch (error) {
      console.error('❌ [QUIZ PAGE] Erreur:', error);
      setError('Erreur lors du chargement des exercices');
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerSelect = (answer: string) => {
    if (isAnswered) return;
    setSelectedAnswer(answer);
  };

  const handleSubmitAnswer = () => {
    if (!selectedAnswer || isAnswered) return;
    
    const currentExercise = exercises[currentExerciseIndex];
    const isCorrect = selectedAnswer === currentExercise.correct;
    
    if (isCorrect) {
      setScore(score + 1);
    }
    
    setIsAnswered(true);
    
    // Auto-avance après 2 secondes
    setTimeout(() => {
      if (currentExerciseIndex < exercises.length - 1) {
        nextExercise();
      } else {
        // Quiz terminé
        console.log('🎉 [QUIZ PAGE] Quiz terminé! Score:', score + (isCorrect ? 1 : 0));
      }
    }, 2000);
  };

  const nextExercise = () => {
    setCurrentExerciseIndex(currentExerciseIndex + 1);
    setSelectedAnswer(null);
    setIsAnswered(false);
  };

  const handleTimeout = () => {
    setIsAnswered(true);
    // Auto-avance après timeout
    setTimeout(() => {
      if (currentExerciseIndex < exercises.length - 1) {
        nextExercise();
      }
    }, 1000);
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const getTopicTitle = (topic: string) => {
    const titles: Record<string, string> = {
      'grammar': 'Grammaire Française',
      'conjugation': 'Conjugaison des Verbes',
      'vocabulary': 'Vocabulaire',
      'comprehension': 'Compréhension',
      'interactive': 'Exercices Interactifs'
    };
    return titles[topic] || topic.charAt(0).toUpperCase() + topic.slice(1);
  };

  const getTopicIcon = (topic: string) => {
    switch (topic) {
      case 'grammar': return <Brain className="w-6 h-6 text-purple-500" />;
      case 'conjugation': return <Target className="w-6 h-6 text-blue-500" />;
      case 'vocabulary': return <Brain className="w-6 h-6 text-green-500" />;
      case 'comprehension': return <Brain className="w-6 h-6 text-orange-500" />;
      default: return <Brain className="w-6 h-6 text-pink-500" />;
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement des exercices...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <XCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">Erreur de chargement</h3>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={() => router.back()}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Retour
          </button>
        </div>
      </div>
    );
  }

  if (exercises.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Brain className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">Aucun exercice disponible</h3>
          <p className="text-gray-600 mb-4">Aucun exercice trouvé pour ce topic</p>
          <button
            onClick={() => router.back()}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Retour
          </button>
        </div>
      </div>
    );
  }

  const currentExercise = exercises[currentExerciseIndex];
  const progress = ((currentExerciseIndex + 1) / exercises.length) * 100;
  const isLastExercise = currentExerciseIndex === exercises.length - 1;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <button
              onClick={() => router.back()}
              className="flex items-center gap-2 text-gray-600 hover:text-gray-800 transition-colors"
            >
              <ArrowLeft className="w-5 h-5" />
              Retour
            </button>
            
            <div className="text-center">
              <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-3 justify-center">
                {getTopicIcon(topic)}
                Quiz de Remédiation - {getTopicTitle(topic)}
              </h1>
            </div>
            
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 text-sm">
                <Clock className="w-4 h-4 text-gray-500" />
                <span className="font-mono">{formatTime(timeLeft)}</span>
              </div>
              <div className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                Score: {score}/{currentExerciseIndex + 1}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="max-w-4xl mx-auto px-4 py-4">
        <div className="mb-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-gray-600">
              Question {currentExerciseIndex + 1} sur {exercises.length}
            </span>
            <span className="text-sm font-medium text-gray-900">
              {Math.round(progress)}%
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
            <div 
              className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        </div>
      </div>

      {/* Exercise Card */}
      <div className="max-w-4xl mx-auto px-4 py-6">
        <div className="bg-white rounded-lg shadow-lg p-8">
          {/* Question */}
          <div className="mb-8">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-900">
                {currentExercise.question}
              </h2>
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                currentExercise.difficulty === 'facile' ? 'bg-green-100 text-green-800' :
                currentExercise.difficulty === 'intermédiaire' ? 'bg-yellow-100 text-yellow-800' :
                'bg-red-100 text-red-800'
              }`}>
                {currentExercise.difficulty.charAt(0).toUpperCase() + currentExercise.difficulty.slice(1)}
              </span>
            </div>
          </div>

          {/* Answer Options */}
          {currentExercise.options && (
            <div className="space-y-3 mb-8">
              {currentExercise.options.map((option, index) => (
                <label
                  key={index}
                  className={`flex items-center p-4 border-2 rounded-lg cursor-pointer transition-all ${
                    selectedAnswer === option
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
                  } ${isAnswered ? 'cursor-default' : ''}`}
                >
                  <input
                    type="radio"
                    name="answer"
                    value={option}
                    checked={selectedAnswer === option}
                    onChange={() => handleAnswerSelect(option)}
                    disabled={isAnswered}
                    className="sr-only"
                  />
                  <div className={`w-5 h-5 rounded-full border-2 mr-3 flex items-center justify-center ${
                    selectedAnswer === option
                      ? 'border-blue-500 bg-blue-500'
                      : 'border-gray-300'
                  }`}>
                    {selectedAnswer === option && (
                      <div className="w-2 h-2 bg-white rounded-full"></div>
                    )}
                  </div>
                  <span className="text-gray-900">{option}</span>
                  
                  {/* Feedback après réponse */}
                  {isAnswered && (
                    <div className="ml-auto">
                      {option === currentExercise.correct ? (
                        <CheckCircle className="w-6 h-6 text-green-500" />
                      ) : option === selectedAnswer ? (
                        <XCircle className="w-6 h-6 text-red-500" />
                      ) : null}
                    </div>
                  )}
                </label>
              ))}
            </div>
          )}

          {/* Explanation */}
          {isAnswered && (
            <div className="mb-8 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <h3 className="font-semibold text-blue-900 mb-2">Explication :</h3>
              <p className="text-blue-800">{currentExercise.explanation}</p>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex justify-between items-center">
            <div className="text-sm text-gray-600">
              Temps estimé : {currentExercise.estimated_time} min
            </div>
            
            <div className="flex gap-3">
              {!isAnswered ? (
                <button
                  onClick={handleSubmitAnswer}
                  disabled={!selectedAnswer}
                  className={`px-6 py-3 rounded-lg font-medium transition-colors ${
                    selectedAnswer
                      ? 'bg-blue-600 hover:bg-blue-700 text-white'
                      : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  }`}
                >
                  Valider la Réponse
                </button>
              ) : (
                <>
                  {!isLastExercise ? (
                    <button
                      onClick={nextExercise}
                      className="px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium transition-colors"
                    >
                      Question Suivante
                    </button>
                  ) : (
                    <button
                      onClick={() => router.push('/dashboard/student/remediation')}
                      className="px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-lg font-medium transition-colors"
                    >
                      Terminer le Quiz
                    </button>
                  )}
                </>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Quiz Summary */}
      {isLastExercise && isAnswered && (
        <div className="max-w-4xl mx-auto px-4 py-6">
          <div className="bg-gradient-to-r from-green-50 to-blue-50 rounded-lg border border-green-200 p-6 text-center">
            <h3 className="text-2xl font-bold text-green-800 mb-4">
              🎉 Quiz Terminé !
            </h3>
            <div className="text-4xl font-bold text-green-600 mb-2">
              {score}/{exercises.length}
            </div>
            <p className="text-green-700 mb-4">
              {score === exercises.length ? 'Parfait ! Toutes les réponses sont correctes !' :
               score >= exercises.length * 0.8 ? 'Excellent travail !' :
               score >= exercises.length * 0.6 ? 'Bon travail ! Continuez à vous entraîner.' :
               'Continuez à vous entraîner pour améliorer vos compétences.'}
            </p>
            <button
              onClick={() => router.push('/dashboard/student/remediation')}
              className="px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium transition-colors"
            >
              Retour à la Remédiation
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
