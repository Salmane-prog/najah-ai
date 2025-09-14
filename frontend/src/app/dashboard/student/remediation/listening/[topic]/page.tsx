'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { useAuth } from '@/hooks/useAuthSimple';
import { BookOpen, Play, Volume2, CheckCircle, ArrowLeft, Clock, Target } from 'lucide-react';

interface ListeningExercise {
  id: string;
  type: string;
  title: string;
  audio_file: string;
  transcript: string;
  questions: Array<{
    question: string;
    options: string[];
    correct: string;
    explanation: string;
  }>;
  difficulty: string;
  topic: string;
  estimated_time: number;
}

export default function ListeningExercisePage() {
  const { topic } = useParams();
  const { user, token } = useAuth();
  const [exercise, setExercise] = useState<ListeningExercise | null>(null);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState<string[]>([]);
  const [showResults, setShowResults] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (user && token) {
      loadListeningExercise();
    }
  }, [user, token, topic]);

  const loadListeningExercise = async () => {
    try {
      setLoading(true);
      
      // Simuler le chargement d'un exercice de compréhension orale
      // En production, cela viendrait de l'API
      const mockExercise: ListeningExercise = {
        id: "comp_aud_001",
        type: "listening",
        title: "Les Saisons",
        audio_file: "seasons_fr.mp3",
        transcript: "Il y a quatre saisons en France : le printemps, l'été, l'automne et l'hiver. Chaque saison a ses caractéristiques. Le printemps apporte les fleurs et la chaleur douce. L'été est chaud et ensoleillé. L'automne amène les feuilles colorées et la fraîcheur. L'hiver apporte le froid et parfois la neige.",
        questions: [
          {
            question: "Combien y a-t-il de saisons en France ?",
            options: ["3", "4", "5", "6"],
            correct: "4",
            explanation: "Le transcript mentionne 'quatre saisons'."
          },
          {
            question: "Quelle saison amène les fleurs ?",
            options: ["L'été", "L'automne", "Le printemps", "L'hiver"],
            correct: "Le printemps",
            explanation: "Le transcript dit 'Le printemps apporte les fleurs'."
          },
          {
            question: "Quelle saison est caractérisée par la neige ?",
            options: ["Le printemps", "L'été", "L'automne", "L'hiver"],
            correct: "L'hiver",
            explanation: "Le transcript mentionne 'L'hiver apporte le froid et parfois la neige'."
          }
        ],
        difficulty: "facile",
        topic: topic as string,
        estimated_time: 5
      };

      setExercise(mockExercise);
      setSelectedAnswers(new Array(mockExercise.questions.length).fill(''));
      
    } catch (error) {
      console.error('Erreur lors du chargement de l\'exercice:', error);
      setError('Impossible de charger l\'exercice de compréhension orale');
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerSelect = (questionIndex: number, answer: string) => {
    const newAnswers = [...selectedAnswers];
    newAnswers[questionIndex] = answer;
    setSelectedAnswers(newAnswers);
  };

  const handleSubmit = () => {
    if (selectedAnswers.every(answer => answer !== '')) {
      setShowResults(true);
    } else {
      alert('Veuillez répondre à toutes les questions avant de valider.');
    }
  };

  const calculateScore = () => {
    if (!exercise) return 0;
    let correct = 0;
    exercise.questions.forEach((question, index) => {
      if (selectedAnswers[index] === question.correct) {
        correct++;
      }
    });
    return Math.round((correct / exercise.questions.length) * 100);
  };

  const resetExercise = () => {
    setCurrentQuestion(0);
    setSelectedAnswers(new Array(exercise?.questions.length || 0).fill(''));
    setShowResults(false);
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement de l'exercice de compréhension orale...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="text-center py-12">
          <div className="bg-red-50 border border-red-200 rounded-lg p-6">
            <p className="text-red-600 mb-4">{error}</p>
            <button
              onClick={loadListeningExercise}
              className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
            >
              Réessayer
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!exercise) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="text-center py-12">
          <p className="text-gray-600">Aucun exercice de compréhension orale disponible.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* En-tête */}
      <div className="mb-6">
        <button
          onClick={() => window.history.back()}
          className="flex items-center gap-2 text-blue-600 hover:text-blue-700 mb-4"
        >
          <ArrowLeft className="w-4 h-4" />
          Retour à la remédiation
        </button>
        
        <div className="bg-gradient-to-r from-purple-50 to-blue-50 p-6 rounded-lg border border-purple-200">
          <div className="flex items-center gap-3 mb-4">
            <Volume2 className="w-8 h-8 text-purple-600" />
            <h1 className="text-3xl font-bold text-gray-900">{exercise.title}</h1>
          </div>
          
          <div className="flex flex-wrap gap-4 text-sm text-gray-600">
            <div className="flex items-center gap-2">
              <Target className="w-4 h-4" />
              <span className="capitalize">{exercise.topic}</span>
            </div>
            <div className="flex items-center gap-2">
              <div className={`px-2 py-1 rounded-full text-xs font-medium ${
                exercise.difficulty === 'facile' ? 'bg-green-100 text-green-800' :
                exercise.difficulty === 'intermédiaire' ? 'bg-yellow-100 text-yellow-800' :
                'bg-red-100 text-red-800'
              }`}>
                {exercise.difficulty}
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Clock className="w-4 h-4" />
              <span>{exercise.estimated_time} min</span>
            </div>
          </div>
        </div>
      </div>

      {!showResults ? (
        <div className="space-y-6">
          {/* Section Audio */}
          <div className="bg-white p-6 rounded-lg border border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <Play className="w-5 h-5 text-purple-600" />
              Écoutez l'audio
            </h2>
            
            <div className="text-center py-8">
              <div className="bg-purple-100 rounded-full w-24 h-24 flex items-center justify-center mx-auto mb-4">
                <Volume2 className="w-12 h-12 text-purple-600" />
              </div>
              <p className="text-gray-600 mb-4">
                {isPlaying ? 'Lecture en cours...' : 'Cliquez pour écouter l\'audio'}
              </p>
              <button
                onClick={() => setIsPlaying(!isPlaying)}
                className={`px-6 py-3 rounded-lg font-medium transition-colors ${
                  isPlaying 
                    ? 'bg-red-600 hover:bg-red-700 text-white' 
                    : 'bg-purple-600 hover:bg-purple-700 text-white'
                }`}
              >
                {isPlaying ? 'Arrêter' : 'Écouter l\'Audio'}
              </button>
              <p className="text-sm text-gray-500 mt-2">
                Note: L'audio est simulé pour cet exercice
              </p>
            </div>
          </div>

          {/* Questions */}
          <div className="bg-white p-6 rounded-lg border border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              Questions ({currentQuestion + 1}/{exercise.questions.length})
            </h2>
            
            <div className="space-y-6">
              {exercise.questions.map((question, index) => (
                <div key={index} className={`p-4 rounded-lg border ${
                  index === currentQuestion ? 'border-blue-300 bg-blue-50' : 'border-gray-200'
                }`}>
                  <h3 className="font-medium text-gray-900 mb-3">
                    Question {index + 1}: {question.question}
                  </h3>
                  
                  <div className="space-y-2">
                    {question.options.map((option, optionIndex) => (
                      <label key={optionIndex} className="flex items-center gap-3 cursor-pointer">
                        <input
                          type="radio"
                          name={`question-${index}`}
                          value={option}
                          checked={selectedAnswers[index] === option}
                          onChange={() => handleAnswerSelect(index, option)}
                          className="w-4 h-4 text-purple-600 border-gray-300 focus:ring-purple-500"
                        />
                        <span className="text-gray-700">{option}</span>
                      </label>
                    ))}
                  </div>
                </div>
              ))}
            </div>
            
            <div className="mt-6 flex justify-between">
              <button
                onClick={() => setCurrentQuestion(Math.max(0, currentQuestion - 1))}
                disabled={currentQuestion === 0}
                className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Précédent
              </button>
              
              {currentQuestion < exercise.questions.length - 1 ? (
                <button
                  onClick={() => setCurrentQuestion(currentQuestion + 1)}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  Suivant
                </button>
              ) : (
                <button
                  onClick={handleSubmit}
                  className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
                >
                  Valider mes Réponses
                </button>
              )}
            </div>
          </div>
        </div>
      ) : (
        /* Résultats */
        <div className="bg-white p-6 rounded-lg border border-gray-200">
          <div className="text-center mb-6">
            <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Exercice Terminé !</h2>
            <p className="text-gray-600">Votre score: <span className="font-bold text-blue-600">{calculateScore()}%</span></p>
          </div>
          
          <div className="space-y-4 mb-6">
            {exercise.questions.map((question, index) => {
              const isCorrect = selectedAnswers[index] === question.correct;
              return (
                <div key={index} className={`p-4 rounded-lg border ${
                  isCorrect ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'
                }`}>
                  <div className="flex items-center gap-2 mb-2">
                    {isCorrect ? (
                      <CheckCircle className="w-5 h-5 text-green-600" />
                    ) : (
                      <div className="w-5 h-5 rounded-full border-2 border-red-600 flex items-center justify-center">
                        <span className="text-red-600 text-xs">✗</span>
                      </div>
                    )}
                    <span className="font-medium text-gray-900">
                      Question {index + 1}: {question.question}
                    </span>
                  </div>
                  
                  <div className="ml-7 space-y-2">
                    <p className="text-sm">
                      <span className="font-medium">Votre réponse:</span> 
                      <span className={isCorrect ? 'text-green-700' : 'text-red-700'}>
                        {' '}{selectedAnswers[index]}
                      </span>
                    </p>
                    {!isCorrect && (
                      <p className="text-sm">
                        <span className="font-medium">Réponse correcte:</span> 
                        <span className="text-green-700"> {question.correct}</span>
                      </p>
                    )}
                    <p className="text-sm text-gray-600">
                      <span className="font-medium">Explication:</span> {question.explanation}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
          
          <div className="flex justify-center gap-4">
            <button
              onClick={resetExercise}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Recommencer
            </button>
            <button
              onClick={() => window.history.back()}
              className="px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700"
            >
              Retour à la Remédiation
            </button>
          </div>
        </div>
      )}
    </div>
  );
}






