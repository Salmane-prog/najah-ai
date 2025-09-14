import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { CheckCircle, XCircle, Clock, Target, Trophy, ArrowRight, ArrowLeft } from 'lucide-react';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface QuizQuestion {
  id: string;
  question: string;
  options: string[];
  correct_answer: number;
  explication: string;
}

interface QuizData {
  quiz_id: number;
  title: string;
  subject: string;
  difficulty: string;
  question_count: number;
  estimated_duration: number;
  adaptation_reason: string;
  questions: QuizQuestion[];
}

interface StudentQuizProps {
  quizData: QuizData | null;
  onQuizComplete: (score: number, results: any) => void;
  onClose: () => void;
}

const StudentQuiz: React.FC<StudentQuizProps> = ({ quizData, onQuizComplete, onClose }) => {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState<number[]>([]);
  const [showResults, setShowResults] = useState(false);
  const [timeLeft, setTimeLeft] = useState(0);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (quizData) {
      setTimeLeft(quizData.estimated_duration * 60); // Convertir en secondes
      setAnswers(new Array(quizData.questions.length).fill(-1));
    }
  }, [quizData]);

  useEffect(() => {
    if (timeLeft > 0 && !showResults) {
      const timer = setInterval(() => {
        setTimeLeft(prev => {
          if (prev <= 1) {
            handleSubmitQuiz();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
      return () => clearInterval(timer);
    }
  }, [timeLeft, showResults]);

  const handleAnswerSelect = (answerIndex: number) => {
    const newAnswers = [...answers];
    newAnswers[currentQuestionIndex] = answerIndex;
    setAnswers(newAnswers);
  };

  const handleNextQuestion = () => {
    if (currentQuestionIndex < (quizData?.questions.length || 0) - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    }
  };

  const handlePreviousQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
    }
  };

  const handleSubmitQuiz = async () => {
    if (!quizData) return;

    setLoading(true);
    try {
      // Calculer le score
      let correctAnswers = 0;
      const results = quizData.questions.map((question, index) => {
        const isCorrect = answers[index] === question.correct_answer;
        if (isCorrect) correctAnswers++;
        return {
          question: question.question,
          userAnswer: answers[index] >= 0 ? question.options[answers[index]] : "Non répondu",
          correctAnswer: question.options[question.correct_answer],
          isCorrect,
          explication: question.explication
        };
      });

      const score = Math.round((correctAnswers / quizData.questions.length) * 100);
      
      // Envoyer les résultats au serveur
      const response = await fetch(`${API_BASE_URL}/api/v1/adaptive_quizzes/${quizData.quiz_id}/submit-test`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          answers: answers,
          student_id: 1, // À adapter selon l'étudiant connecté
          score: score
        })
      });

      if (response.ok) {
        setShowResults(true);
        onQuizComplete(score, results);
      }
    } catch (error) {
      console.error('Erreur lors de la soumission:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!quizData) {
    return (
      <Card className="w-full max-w-4xl mx-auto">
        <CardContent className="p-6">
          <p className="text-center text-gray-500">Aucun quiz disponible</p>
        </CardContent>
      </Card>
    );
  }

  const currentQuestion = quizData.questions[currentQuestionIndex];
  const progress = ((currentQuestionIndex + 1) / quizData.questions.length) * 100;
  const answeredQuestions = answers.filter(answer => answer !== -1).length;

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  if (showResults) {
    return (
      <Card className="w-full max-w-4xl mx-auto">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Trophy className="h-5 w-5 text-yellow-500" />
            Résultats du Quiz
          </CardTitle>
        </CardHeader>
        <CardContent className="p-6">
          <div className="text-center mb-6">
            <h3 className="text-2xl font-bold mb-2">{quizData.title}</h3>
            <p className="text-gray-600">{quizData.adaptation_reason}</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">
                {Math.round((answers.filter((answer, index) => 
                  answer === quizData.questions[index].correct_answer
                ).length / quizData.questions.length) * 100)}%
              </div>
              <div className="text-sm text-gray-600">Score</div>
            </div>
            <div className="text-center p-4 bg-green-50 rounded-lg">
              <div className="text-2xl font-bold text-green-600">
                {answers.filter((answer, index) => 
                  answer === quizData.questions[index].correct_answer
                ).length}
              </div>
              <div className="text-sm text-gray-600">Réponses correctes</div>
            </div>
            <div className="text-center p-4 bg-purple-50 rounded-lg">
              <div className="text-2xl font-bold text-purple-600">
                {quizData.questions.length}
              </div>
              <div className="text-sm text-gray-600">Questions totales</div>
            </div>
          </div>

          <div className="space-y-4">
            {quizData.questions.map((question, index) => {
              const userAnswer = answers[index];
              const isCorrect = userAnswer === question.correct_answer;
              
              return (
                <div key={question.id} className={`border rounded-lg p-4 ${isCorrect ? 'bg-green-50' : 'bg-red-50'}`}>
                  <div className="flex items-start gap-2 mb-3">
                    <span className={`rounded-full w-6 h-6 flex items-center justify-center text-sm font-medium ${
                      isCorrect ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
                    }`}>
                      {isCorrect ? <CheckCircle className="h-4 w-4" /> : <XCircle className="h-4 w-4" />}
                    </span>
                    <p className="text-gray-800 font-medium">{question.question}</p>
                  </div>
                  
                  <div className="ml-8 space-y-2">
                    {question.options.map((option, optionIndex) => (
                      <div key={optionIndex} className={`p-2 rounded ${
                        optionIndex === question.correct_answer ? 'bg-green-100 border-green-300' :
                        optionIndex === userAnswer && !isCorrect ? 'bg-red-100 border-red-300' :
                        'bg-gray-50'
                      }`}>
                        <span className="text-gray-700">{option}</span>
                        {optionIndex === question.correct_answer && (
                          <CheckCircle className="h-4 w-4 text-green-600 inline ml-2" />
                        )}
                        {optionIndex === userAnswer && !isCorrect && (
                          <XCircle className="h-4 w-4 text-red-600 inline ml-2" />
                        )}
                      </div>
                    ))}
                  </div>
                  
                  <div className="mt-3 p-3 bg-blue-50 rounded">
                    <p className="text-sm text-blue-700">
                      <strong>Explication :</strong> {question.explication}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>

          <div className="flex gap-2 mt-6">
            <Button onClick={onClose} variant="outline" className="flex-1">
              Retour au Dashboard
            </Button>
            <Button onClick={() => window.location.reload()} className="flex-1">
              Nouveau Quiz
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="w-full max-w-4xl mx-auto">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <Target className="h-5 w-5" />
            {quizData.title}
          </CardTitle>
          <Badge variant="secondary">
            <Clock className="h-4 w-4 mr-1" />
            {formatTime(timeLeft)}
          </Badge>
        </div>
      </CardHeader>
      
      <CardContent className="p-6">
        {/* Barre de progression */}
        <div className="mb-6">
          <div className="flex justify-between text-sm text-gray-600 mb-2">
            <span>Question {currentQuestionIndex + 1} sur {quizData.questions.length}</span>
            <span>{answeredQuestions}/{quizData.questions.length} répondues</span>
          </div>
          <Progress value={progress} className="h-2" />
        </div>

        {/* Question actuelle */}
        <div className="space-y-6">
          <div className="flex items-start gap-2 mb-4">
            <span className="bg-blue-500 text-white rounded-full w-8 h-8 flex items-center justify-center text-sm font-medium">
              {currentQuestionIndex + 1}
            </span>
            <p className="text-lg font-medium text-gray-800">{currentQuestion.question}</p>
          </div>
          
          <div className="space-y-3">
            {currentQuestion.options.map((option, optionIndex) => (
              <label 
                key={optionIndex} 
                className={`flex items-center gap-3 p-3 border rounded-lg cursor-pointer transition-colors ${
                  answers[currentQuestionIndex] === optionIndex 
                    ? 'bg-blue-100 border-blue-300' 
                    : 'bg-gray-50 hover:bg-gray-100'
                }`}
              >
                <input 
                  type="radio" 
                  name={`question-${currentQuestion.id}`}
                  value={optionIndex}
                  checked={answers[currentQuestionIndex] === optionIndex}
                  onChange={() => handleAnswerSelect(optionIndex)}
                  className="text-blue-600"
                />
                <span className="text-gray-700">{option}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Navigation */}
        <div className="flex justify-between mt-8">
          <Button 
            onClick={handlePreviousQuestion} 
            disabled={currentQuestionIndex === 0}
            variant="outline"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Précédent
          </Button>
          
          <div className="flex gap-2">
            {currentQuestionIndex < quizData.questions.length - 1 ? (
              <Button onClick={handleNextQuestion}>
                Suivant
                <ArrowRight className="h-4 w-4 ml-2" />
              </Button>
            ) : (
              <Button 
                onClick={handleSubmitQuiz} 
                disabled={loading || answeredQuestions < quizData.questions.length}
                className="bg-green-600 hover:bg-green-700"
              >
                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Soumission...
                  </>
                ) : (
                  <>
                    <Trophy className="h-4 w-4 mr-2" />
                    Terminer le Quiz
                  </>
                )}
              </Button>
            )}
          </div>
        </div>

        {/* Indicateur de réponses */}
        <div className="mt-4 flex flex-wrap gap-1">
          {quizData.questions.map((_, index) => (
            <div
              key={index}
              className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-medium ${
                answers[index] !== -1 
                  ? 'bg-green-500 text-white' 
                  : 'bg-gray-200 text-gray-600'
              }`}
            >
              {index + 1}
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

export default StudentQuiz; 