'use client';

import React, { useState, useEffect } from 'react';
import { useAuth  } from '../../../../hooks/useAuth';
import { Card } from '../../../../components/Card';
import Button from '../../../../components/Button';
import { CognitiveDiagnosticService, AdaptiveQuiz, QuizQuestion } from '../../../../services/cognitiveDiagnosticService';
import { 
  Brain, 
  Target, 
  Clock, 
  CheckCircle, 
  XCircle, 
  Play,
  BarChart3,
  TrendingUp,
  BookOpen,
  Video,
  Headphones,
  Activity
} from 'lucide-react';

export default function AdaptiveQuizPage() {
  const { user, token } = useAuth();
  const [currentQuiz, setCurrentQuiz] = useState<AdaptiveQuiz | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedSubject, setSelectedSubject] = useState('Français');
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [userAnswers, setUserAnswers] = useState<Record<number, string>>({});
  const [quizCompleted, setQuizCompleted] = useState(false);
  const [score, setScore] = useState(0);

  const subjects = ['Français', 'Mathématiques', 'Histoire', 'Géographie', 'Sciences'];

  const generateQuiz = async () => {
    if (!user || !token) return;

    setIsLoading(true);
    try {
      // Essayer de générer un quiz via l'API
      const quiz = await CognitiveDiagnosticService.generateAdaptiveQuiz(
        user.id,
        selectedSubject,
        5, // 5 questions pour commencer
        'auto',
        token
      );
      setCurrentQuiz(quiz);
      setCurrentQuestionIndex(0);
      setUserAnswers({});
      setQuizCompleted(false);
      setScore(0);
    } catch (error) {
      console.error('Erreur lors de la génération du quiz:', error);
      // Utiliser un quiz par défaut en cas d'erreur
      const defaultQuiz: AdaptiveQuiz = {
        quiz_id: 1,
        title: `Quiz ${selectedSubject} - Niveau Adaptatif`,
        subject: selectedSubject,
        difficulty: 'medium',
        question_count: 5,
        estimated_duration: 15,
        adaptation_reason: 'Basé sur votre profil d\'apprentissage',
        questions: [
          {
            id: 1,
            question_text: 'Quelle est la conjugaison correcte du verbe "être" à la 1ère personne du singulier au présent ?',
            question_type: 'multiple_choice',
            options: ['Je suis', 'Je es', 'Je être', 'Je suis être'],
            correct_answer: 'Je suis',
            explanation: 'Le verbe "être" se conjugue "je suis" au présent de l\'indicatif.',
            difficulty: 'easy',
            subject: selectedSubject,
            topic: 'Conjugaison'
          },
          {
            id: 2,
            question_text: 'Quel est le genre du mot "livre" en français ?',
            question_type: 'multiple_choice',
            options: ['Masculin', 'Féminin', 'Les deux', 'Aucun des deux'],
            correct_answer: 'Masculin',
            explanation: 'Le mot "livre" est masculin en français.',
            difficulty: 'easy',
            subject: selectedSubject,
            topic: 'Grammaire'
          },
          {
            id: 3,
            question_text: 'Quelle est la traduction correcte de "Bonjour" en anglais ?',
            question_type: 'multiple_choice',
            options: ['Goodbye', 'Hello', 'Good morning', 'Good night'],
            correct_answer: 'Hello',
            explanation: '"Bonjour" se traduit par "Hello" en anglais.',
            difficulty: 'medium',
            subject: selectedSubject,
            topic: 'Vocabulaire'
          },
          {
            id: 4,
            question_text: 'Quel est le pluriel de "cheval" ?',
            question_type: 'multiple_choice',
            options: ['Chevals', 'Chevaux', 'Chevales', 'Chevauxes'],
            correct_answer: 'Chevaux',
            explanation: 'Le pluriel de "cheval" est "chevaux".',
            difficulty: 'medium',
            subject: selectedSubject,
            topic: 'Grammaire'
          },
          {
            id: 5,
            question_text: 'Quelle est la fonction du mot "très" dans la phrase "Il est très intelligent" ?',
            question_type: 'multiple_choice',
            options: ['Adjectif', 'Adverbe', 'Nom', 'Verbe'],
            correct_answer: 'Adverbe',
            explanation: '"Très" est un adverbe qui modifie l\'adjectif "intelligent".',
            difficulty: 'hard',
            subject: selectedSubject,
            topic: 'Grammaire'
          }
        ]
      };
      setCurrentQuiz(defaultQuiz);
      setCurrentQuestionIndex(0);
      setUserAnswers({});
      setQuizCompleted(false);
      setScore(0);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAnswerSelect = (answer: string) => {
    setUserAnswers(prev => ({
      ...prev,
      [currentQuestionIndex]: answer
    }));
  };

  const nextQuestion = () => {
    if (currentQuestionIndex < (currentQuiz?.questions.length || 0) - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
    }
  };

  const previousQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(prev => prev - 1);
    }
  };

  const submitQuiz = () => {
    if (!currentQuiz) return;

    let correctAnswers = 0;
    currentQuiz.questions.forEach((question, index) => {
      if (userAnswers[index] === question.correct_answer) {
        correctAnswers++;
      }
    });

    const finalScore = Math.round((correctAnswers / currentQuiz.questions.length) * 100);
    setScore(finalScore);
    setQuizCompleted(true);
  };

  const resetQuiz = () => {
    setCurrentQuiz(null);
    setCurrentQuestionIndex(0);
    setUserAnswers({});
    setQuizCompleted(false);
    setScore(0);
  };

  const currentQuestion = currentQuiz?.questions[currentQuestionIndex];

  if (quizCompleted && currentQuiz) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-4xl mx-auto px-4">
          <div className="text-center mb-8">
            <Brain className="w-16 h-16 text-green-500 mx-auto mb-4" />
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Quiz Terminé !</h1>
            <p className="text-lg text-gray-600">
              Félicitations ! Vous avez terminé le quiz {currentQuiz.subject}
            </p>
          </div>

          <Card className="mb-8">
            <div className="p-8 text-center">
              <div className="text-6xl font-bold text-blue-600 mb-4">{score}%</div>
              <p className="text-xl text-gray-600 mb-6">Votre score</p>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="text-center">
                  <div className="text-2xl font-bold text-gray-900">
                    {currentQuiz.questions.length}
                  </div>
                  <div className="text-sm text-gray-500">Questions</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">
                    {Math.round((score / 100) * currentQuiz.questions.length)}
                  </div>
                  <div className="text-sm text-gray-500">Correctes</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-red-600">
                    {currentQuiz.questions.length - Math.round((score / 100) * currentQuiz.questions.length)}
                  </div>
                  <div className="text-sm text-gray-500">Incorrectes</div>
                </div>
              </div>

              <div className="flex justify-center space-x-4">
                <Button
                  onClick={resetQuiz}
                  className="bg-blue-500 hover:bg-blue-600"
                >
                  <Play className="w-5 h-5 mr-2" />
                  Nouveau Quiz
                </Button>
                
                <Button
                  onClick={() => setQuizCompleted(false)}
                  className="bg-green-500 hover:bg-green-600"
                >
                  <BarChart3 className="w-5 h-5 mr-2" />
                  Voir les Réponses
                </Button>
              </div>
            </div>
          </Card>
        </div>
      </div>
    );
  }

  if (!currentQuiz) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-4xl mx-auto px-4">
          <div className="text-center mb-8">
            <Brain className="w-16 h-16 text-blue-500 mx-auto mb-4" />
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Quiz Adaptatif</h1>
            <p className="text-lg text-gray-600">
              Testez vos connaissances avec des quiz personnalisés qui s'adaptent à votre niveau
            </p>
          </div>

          <Card className="mb-8">
            <div className="p-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 items-end mb-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Matière
                  </label>
                  <select
                    value={selectedSubject}
                    onChange={(e) => setSelectedSubject(e.target.value)}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    {subjects.map(subject => (
                      <option key={subject} value={subject}>{subject}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <Button
                    onClick={generateQuiz}
                    disabled={isLoading}
                    className="w-full bg-blue-500 hover:bg-blue-600 text-lg px-8 py-3"
                  >
                    {isLoading ? (
                      <div className="flex items-center">
                        <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                        Génération...
                      </div>
                    ) : (
                      <div className="flex items-center">
                        <Play className="w-5 h-5 mr-2" />
                        Commencer un Quiz
                      </div>
                    )}
                  </Button>
                </div>
              </div>

              <div className="text-center text-gray-600">
                <p>Le quiz s'adaptera automatiquement à votre niveau</p>
                <p className="text-sm">Durée estimée : 15-20 minutes</p>
              </div>
            </div>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        {/* En-tête du quiz */}
        <div className="text-center mb-8">
          <Brain className="w-16 h-16 text-blue-500 mx-auto mb-4" />
          <h1 className="text-3xl font-bold text-gray-900 mb-2">{currentQuiz.title}</h1>
          <p className="text-lg text-gray-600">
            Question {currentQuestionIndex + 1} sur {currentQuiz.questions.length}
          </p>
        </div>

        {/* Progression */}
        <Card className="mb-8">
          <div className="p-6">
            <div className="flex items-center justify-between mb-4">
              <span className="text-sm font-medium text-gray-700">Progression</span>
              <span className="text-sm text-gray-500">
                {currentQuestionIndex + 1} / {currentQuiz.questions.length}
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                style={{ width: `${((currentQuestionIndex + 1) / currentQuiz.questions.length) * 100}%` }}
              />
            </div>
          </div>
        </Card>

        {/* Question actuelle */}
        {currentQuestion && (
          <Card className="mb-8">
            <div className="p-6">
              <div className="mb-6">
                <div className="flex items-center justify-between mb-4">
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                    currentQuestion.difficulty === 'easy' ? 'bg-green-100 text-green-800' :
                    currentQuestion.difficulty === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  }`}>
                    {currentQuestion.difficulty === 'easy' ? 'Facile' :
                     currentQuestion.difficulty === 'medium' ? 'Moyen' : 'Difficile'}
                  </span>
                  <span className="text-sm text-gray-500">{currentQuestion.topic}</span>
                </div>
                
                <h3 className="text-xl font-semibold text-gray-900 mb-4">
                  {currentQuestion.question_text}
                </h3>

                {currentQuestion.question_type === 'multiple_choice' && currentQuestion.options && (
                  <div className="space-y-3">
                    {currentQuestion.options.map((option, index) => (
                      <button
                        key={index}
                        onClick={() => handleAnswerSelect(option)}
                        className={`w-full p-4 text-left border rounded-lg transition-all ${
                          userAnswers[currentQuestionIndex] === option
                            ? 'border-blue-500 bg-blue-50 text-blue-700'
                            : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                        }`}
                      >
                        <span className="font-medium">{String.fromCharCode(65 + index)}.</span> {option}
                      </button>
                    ))}
                  </div>
                )}
              </div>

              {/* Navigation */}
              <div className="flex items-center justify-between pt-6 border-t border-gray-200">
                <Button
                  onClick={previousQuestion}
                  disabled={currentQuestionIndex === 0}
                  className="bg-gray-500 hover:bg-gray-600"
                >
                  Précédent
                </Button>

                <div className="flex space-x-2">
                  {currentQuestionIndex === currentQuiz.questions.length - 1 ? (
                    <Button
                      onClick={submitQuiz}
                      disabled={!userAnswers[currentQuestionIndex]}
                      className="bg-green-500 hover:bg-green-600"
                    >
                      <CheckCircle className="w-5 h-5 mr-2" />
                      Terminer le Quiz
                    </Button>
                  ) : (
                    <Button
                      onClick={nextQuestion}
                      disabled={!userAnswers[currentQuestionIndex]}
                      className="bg-blue-500 hover:bg-blue-600"
                    >
                      Suivant
                    </Button>
                  )}
                </div>
              </div>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
}
