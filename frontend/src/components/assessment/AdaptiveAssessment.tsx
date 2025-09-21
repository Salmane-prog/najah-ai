'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

interface Question {
  id: string;
  text: string;
  type: 'multiple_choice' | 'true_false' | 'short_answer';
  options?: string[];
  difficulty: number;
  cognitive_domain: string;
  estimated_time: number;
}

interface AssessmentSession {
  id: string;
  title: string;
  subject: string;
  currentQuestion: number;
  totalQuestions: number;
  timeRemaining: number;
  currentAbility: number;
  confidence: number;
  questions: Question[];
  responses: any[];
}

export default function AdaptiveAssessment() {
  const router = useRouter();
  const [session, setSession] = useState<AssessmentSession | null>(null);
  const [currentQuestion, setCurrentQuestion] = useState<Question | null>(null);
  const [selectedAnswer, setSelectedAnswer] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [showFeedback, setShowFeedback] = useState(false);
  const [feedback, setFeedback] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    // Simuler l'initialisation de la session d'évaluation adaptative
    setTimeout(() => {
      const mockSession: AssessmentSession = {
        id: 'adaptive-001',
        title: 'Évaluation Adaptative - Mathématiques',
        subject: 'Algèbre et Géométrie',
        currentQuestion: 1,
        totalQuestions: 15,
        timeRemaining: 2700, // 45 minutes
        currentAbility: 0.5, // Niveau initial
        confidence: 0.3,
        questions: [],
        responses: []
      };

      setSession(mockSession);
      loadNextQuestion(mockSession);
      setLoading(false);
    }, 1500);
  }, []);

  const loadNextQuestion = (currentSession: AssessmentSession) => {
    // Simuler le chargement de la prochaine question basée sur l'algorithme IRT
    const mockQuestion: Question = {
      id: `q${currentSession.currentQuestion}`,
      text: generateQuestionText(currentSession.currentQuestion, currentSession.currentAbility),
      type: 'multiple_choice',
      options: generateOptions(currentSession.currentQuestion),
      difficulty: calculateOptimalDifficulty(currentSession.currentAbility, currentSession.confidence),
      cognitive_domain: getCognitiveDomain(currentSession.currentQuestion),
      estimated_time: 120
    };

    setCurrentQuestion(mockQuestion);
    setSelectedAnswer('');
    setShowFeedback(false);
  };

  const generateQuestionText = (questionNumber: number, ability: number): string => {
    const questions = [
      'Résolvez l\'équation du second degré : x² - 5x + 6 = 0',
      'Calculez l\'aire d\'un cercle de rayon 7 cm',
      'Factorisez l\'expression : 2x² + 7x + 3',
      'Trouvez la dérivée de f(x) = 3x³ - 2x² + 5x - 1',
      'Résolvez le système d\'équations : 2x + y = 5 et x - 3y = -2'
    ];
    
    return questions[questionNumber % questions.length] || questions[0];
  };

  const generateOptions = (questionNumber: number): string[] => {
    const optionsSets = [
      ['x = 2 ou x = 3', 'x = -2 ou x = -3', 'x = 1 ou x = 6', 'Aucune solution'],
      ['49π cm²', '14π cm²', '98π cm²', '21π cm²'],
      ['(2x + 1)(x + 3)', '(2x + 3)(x + 1)', '(2x - 1)(x - 3)', 'Impossible à factoriser'],
      ['9x² - 4x + 5', '9x² - 4x + 4', '9x² - 2x + 5', '6x² - 4x + 5'],
      ['x = 2, y = 1', 'x = 1, y = 3', 'x = 3, y = -1', 'x = -1, y = 7']
    ];
    
    return optionsSets[questionNumber % optionsSets.length] || optionsSets[0];
  };

  const calculateOptimalDifficulty = (ability: number, confidence: number): number => {
    // Algorithme IRT simplifié pour calculer la difficulté optimale
    const baseDifficulty = ability;
    const confidenceAdjustment = (confidence - 0.5) * 0.2;
    return Math.max(0.1, Math.min(0.9, baseDifficulty + confidenceAdjustment));
  };

  const getCognitiveDomain = (questionNumber: number): string => {
    const domains = ['Compréhension', 'Application', 'Analyse', 'Évaluation', 'Création'];
    return domains[questionNumber % domains.length] || domains[0];
  };

  const handleAnswerSubmit = async () => {
    if (!selectedAnswer || !currentQuestion || !session) return;

    setIsSubmitting(true);

    // Simuler l'évaluation de la réponse et la mise à jour du modèle IRT
    setTimeout(() => {
      const isCorrect = Math.random() > 0.4; // 60% de chance de réussite pour la démo
      
      // Mise à jour du modèle IRT
      const newAbility = updateIRTModel(session.currentAbility, currentQuestion.difficulty, isCorrect);
      const newConfidence = updateConfidence(session.confidence, isCorrect);
      
      // Générer le feedback
      const newFeedback = generateFeedback(isCorrect, currentQuestion, newAbility);
      
      setFeedback(newFeedback);
      setShowFeedback(true);

      // Mettre à jour la session
      const updatedSession = {
        ...session,
        currentAbility: newAbility,
        confidence: newConfidence,
        currentQuestion: session.currentQuestion + 1,
        responses: [...session.responses, {
          questionId: currentQuestion.id,
          answer: selectedAnswer,
          isCorrect,
          timeSpent: 120
        }]
      };

      setSession(updatedSession);
      setIsSubmitting(false);

      // Passer à la question suivante après 3 secondes
      setTimeout(() => {
        if (updatedSession.currentQuestion <= updatedSession.totalQuestions) {
          loadNextQuestion(updatedSession);
        } else {
          // Fin de l'évaluation
          completeAssessment(updatedSession);
        }
      }, 3000);
    }, 1000);
  };

  const updateIRTModel = (currentAbility: number, difficulty: number, isCorrect: boolean): number => {
    // Algorithme IRT simplifié (Rasch model)
    const discrimination = 1.0;
    const guessing = 0.25;
    
    if (isCorrect) {
      // Réponse correcte : augmenter légèrement l'habileté
      return Math.min(1.0, currentAbility + 0.1 * (1 - currentAbility));
    } else {
      // Réponse incorrecte : diminuer légèrement l'habileté
      return Math.max(0.0, currentAbility - 0.1 * currentAbility);
    }
  };

  const updateConfidence = (currentConfidence: number, isCorrect: boolean): number => {
    if (isCorrect) {
      return Math.min(1.0, currentConfidence + 0.05);
    } else {
      return Math.max(0.0, currentConfidence - 0.1);
    }
  };

  const generateFeedback = (isCorrect: boolean, question: Question, newAbility: number): string => {
    if (isCorrect) {
      return `Excellent ! Votre réponse est correcte. Votre niveau d'habileté a augmenté à ${(newAbility * 100).toFixed(1)}%. Continuez ainsi !`;
    } else {
      return `Pas tout à fait. La bonne réponse était la première option. Votre niveau d'habileté est maintenant à ${(newAbility * 100).toFixed(1)}%. Ne vous découragez pas !`;
    }
  };

  const completeAssessment = (finalSession: AssessmentSession) => {
    // Calculer le score final et les recommandations
    const correctAnswers = finalSession.responses.filter(r => r.isCorrect).length;
    const finalScore = (correctAnswers / finalSession.totalQuestions) * 100;
    
    // Rediriger vers la page de résultats
    router.push(`/assessment/results?session=${finalSession.id}&score=${finalScore}&ability=${finalSession.currentAbility}`);
  };

  const formatTime = (seconds: number): string => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Initialisation de l'évaluation adaptative</h2>
          <p className="text-gray-600">Analyse de votre profil cognitif et génération des questions...</p>
        </div>
      </div>
    );
  }

  if (!session || !currentQuestion) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Erreur</h2>
          <p className="text-gray-600">Impossible de charger l'évaluation</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header de l'évaluation */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div>
              <h1 className="text-lg font-semibold text-gray-900">{session.title}</h1>
              <p className="text-sm text-gray-500">{session.subject}</p>
            </div>
            
            <div className="flex items-center space-x-4">
              {/* Progression */}
              <div className="text-center">
                <div className="text-sm font-medium text-gray-900">
                  Question {session.currentQuestion} / {session.totalQuestions}
                </div>
                <div className="w-32 bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${(session.currentQuestion / session.totalQuestions) * 100}%` }}
                  ></div>
                </div>
              </div>

              {/* Temps restant */}
              <div className="text-center">
                <div className="text-sm font-medium text-gray-900">
                  Temps restant
                </div>
                <div className="text-lg font-bold text-red-600">
                  {formatTime(session.timeRemaining)}
                </div>
              </div>

              {/* Niveau d'habileté actuel */}
              <div className="text-center">
                <div className="text-sm font-medium text-gray-900">
                  Niveau actuel
                </div>
                <div className="text-lg font-bold text-blue-600">
                  {(session.currentAbility * 100).toFixed(0)}%
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Contenu principal */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {showFeedback ? (
          /* Feedback de la question */
          <div className="bg-white rounded-lg shadow-lg p-8 text-center">
            <div className="mb-6">
              <span className="text-6xl">🎯</span>
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Feedback</h2>
            <p className="text-lg text-gray-700 mb-6">{feedback}</p>
            <div className="text-sm text-gray-500">
              Passage à la question suivante dans quelques secondes...
            </div>
          </div>
        ) : (
          /* Question actuelle */
          <div className="bg-white rounded-lg shadow-lg p-8">
            {/* En-tête de la question */}
            <div className="mb-6">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <span className="text-2xl">❓</span>
                  <span className="text-sm px-3 py-1 bg-blue-100 text-blue-800 rounded-full">
                    {currentQuestion.cognitive_domain}
                  </span>
                  <span className="text-sm px-3 py-1 bg-green-100 text-green-800 rounded-full">
                    Difficulté: {(currentQuestion.difficulty * 100).toFixed(0)}%
                  </span>
                </div>
                <div className="text-sm text-gray-500">
                  ⏱️ {currentQuestion.estimated_time}s estimés
                </div>
              </div>
              
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                Question {session.currentQuestion}
              </h2>
            </div>

            {/* Texte de la question */}
            <div className="mb-8">
              <p className="text-lg text-gray-800 leading-relaxed">{currentQuestion.text}</p>
            </div>

            {/* Options de réponse */}
            {currentQuestion.type === 'multiple_choice' && currentQuestion.options && (
              <div className="space-y-3 mb-8">
                {currentQuestion.options.map((option, index) => (
                  <label
                    key={index}
                    className={`flex items-center p-4 border-2 rounded-lg cursor-pointer transition-all duration-200 ${
                      selectedAnswer === option
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                    }`}
                  >
                    <input
                      type="radio"
                      name="answer"
                      value={option}
                      checked={selectedAnswer === option}
                      onChange={(e) => setSelectedAnswer(e.target.value)}
                      className="sr-only"
                    />
                    <div className={`w-5 h-5 rounded-full border-2 mr-3 ${
                      selectedAnswer === option
                        ? 'border-blue-500 bg-blue-500'
                        : 'border-gray-300'
                    }`}>
                      {selectedAnswer === option && (
                        <div className="w-2 h-2 bg-white rounded-full m-auto mt-1"></div>
                      )}
                    </div>
                    <span className="text-gray-800">{option}</span>
                  </label>
                ))}
              </div>
            )}

            {/* Bouton de soumission */}
            <div className="flex justify-between items-center">
              <button
                onClick={() => router.push('/assessment')}
                className="px-6 py-3 text-gray-600 hover:text-gray-800 transition-colors"
              >
                ← Retour aux évaluations
              </button>
              
              <button
                onClick={handleAnswerSubmit}
                disabled={!selectedAnswer || isSubmitting}
                className={`px-8 py-3 rounded-lg font-medium transition-all duration-200 ${
                  selectedAnswer && !isSubmitting
                    ? 'bg-blue-600 text-white hover:bg-blue-700 transform hover:scale-105'
                    : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                }`}
              >
                {isSubmitting ? (
                  <span className="flex items-center">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Évaluation...
                  </span>
                ) : (
                  'Valider la réponse'
                )}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}















