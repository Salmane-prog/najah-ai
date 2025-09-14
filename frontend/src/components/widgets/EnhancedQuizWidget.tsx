'use client';

import React, { useState, useEffect } from 'react';
import { BookOpen, Clock, Target, Play, CheckCircle, Eye, Calendar, Star, AlertCircle, Trophy } from 'lucide-react';

interface AssignedQuiz {
  id: number;
  title: string;
  subject: string;
  level: string;
  estimatedTime: number;
  questionsCount: number;
  assignedAt: string;
  dueDate?: string;
  assignmentId: number;
  description?: string;
  difficulty?: string;
}

interface CompletedQuiz {
  id: number;
  quiz_id: number;
  score: number;
  max_score: number;
  percentage: number;
  completed: boolean;
  created_at: string;
  answers?: QuizAnswer[];
}

interface QuizAnswer {
  question_id: number;
  question_text: string;
  student_answer: string;
  correct_answer: string;
  is_correct: boolean;
  explanation?: string;
}

interface EnhancedQuizWidgetProps {
  className?: string;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function EnhancedQuizWidget({ className = '' }: EnhancedQuizWidgetProps) {
  const [loading, setLoading] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [assignedQuizzes, setAssignedQuizzes] = useState<AssignedQuiz[]>([]);
  const [completedQuizzes, setCompletedQuizzes] = useState<CompletedQuiz[]>([]);
  const [showCompletedQuizzes, setShowCompletedQuizzes] = useState(false);
  const [selectedQuiz, setSelectedQuiz] = useState<CompletedQuiz | null>(null);
  const [showAnswers, setShowAnswers] = useState(false);
  const [filter, setFilter] = useState<'all' | 'pending' | 'completed'>('all');

  // Charger les quiz assignés et complétés
  useEffect(() => {
    loadQuizData();
  }, []);

  const loadQuizData = async () => {
    try {
      const token = localStorage.getItem('najah_token');
      const user = localStorage.getItem('najah_user');
      
      if (!token || !user) return;
      
      const userData = JSON.parse(user);
      
      // Charger les quiz assignés
      const assignedResponse = await fetch(`${API_BASE_URL}/api/v1/quizzes/assigned/${userData.id}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (assignedResponse.ok) {
        const assignedData = await assignedResponse.json();
        console.log('Quiz assignés reçus:', assignedData); // Debug
        
        // Traiter la réponse de l'API
        let quizzes = [];
        if (Array.isArray(assignedData)) {
          // Si c'est directement un tableau (notre endpoint)
          quizzes = assignedData.map((assignment: any) => ({
            id: assignment.quiz_id,
            title: assignment.quiz?.title || 'Quiz sans titre',
            subject: assignment.quiz?.subject || 'Matière non spécifiée',
            level: assignment.quiz?.level || 'Niveau non spécifié',
            estimatedTime: assignment.quiz?.time_limit || 30,
            questionsCount: assignment.quiz?.questions?.length || 5,
            assignedAt: assignment.assigned_at || assignment.created_at || new Date().toISOString(),
            dueDate: assignment.due_date,
            assignmentId: assignment.id,
            description: assignment.quiz?.description || '',
            difficulty: assignment.quiz?.difficulty || 'medium'
          }));
        } else if (assignedData.quizzes && Array.isArray(assignedData.quizzes)) {
          // Si c'est un objet avec une propriété quizzes (ancien format)
          quizzes = assignedData.quizzes;
        }
        
        setAssignedQuizzes(quizzes);
        console.log('Quiz traités:', quizzes); // Debug
      } else {
        console.error('Erreur API quiz assignés:', assignedResponse.status, assignedResponse.statusText);
      }
      
      // Charger les quiz complétés
      const completedResponse = await fetch(`${API_BASE_URL}/api/v1/quiz_results/user/${userData.id}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (completedResponse.ok) {
        const data = await completedResponse.json();
        const completed = data.filter((quiz: any) => quiz.completed || quiz.is_completed);
        setCompletedQuizzes(completed);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des quiz:', error);
    }
  };

  const handleStartQuiz = async (quizId: number) => {
    setLoading(quizId);
    setError(null);
    
    try {
      const token = localStorage.getItem('najah_token');
      if (!token) {
        setError('Non authentifié');
        return;
      }

      // Rediriger vers la page de quiz
      window.location.href = `/dashboard/student/quiz/${quizId}`;
    } catch (err: any) {
      setError(err.message || 'Erreur lors du démarrage du quiz');
    } finally {
      setLoading(null);
    }
  };

  const handleViewAnswers = async (quiz: CompletedQuiz) => {
    try {
      const token = localStorage.getItem('najah_token');
      if (!token) return;

      // Charger les détails des réponses
      const response = await fetch(`${API_BASE_URL}/api/v1/quiz_results/${quiz.id}/answers`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const answersData = await response.json();
        setSelectedQuiz({ ...quiz, answers: answersData });
        setShowAnswers(true);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des réponses:', error);
    }
  };

  const isQuizCompleted = (quizId: number) => {
    return completedQuizzes.some(quiz => quiz.quiz_id === quizId);
  };

  const getCompletedQuiz = (quizId: number) => {
    return completedQuizzes.find(quiz => quiz.quiz_id === quizId);
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty?.toLowerCase()) {
      case 'facile': return 'bg-green-100 text-green-800';
      case 'moyen': return 'bg-yellow-100 text-yellow-800';
      case 'difficile': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getScoreColor = (percentage: number) => {
    if (percentage >= 80) return 'text-green-600';
    if (percentage >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const filteredQuizzes = (assignedQuizzes || []).filter(quiz => {
    if (filter === 'pending') return !isQuizCompleted(quiz.id);
    if (filter === 'completed') return isQuizCompleted(quiz.id);
    return true;
  });

  return (
    <div className={`bg-white rounded-xl shadow-lg p-6 card-enhanced hover-lift-enhanced ${className}`}>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-gray-800 flex items-center gap-2">
          <BookOpen className="w-6 h-6 text-blue-600" />
          Quiz Assignés
        </h2>
        <div className="flex gap-2">
          <button
            onClick={() => setFilter('all')}
            className={`px-3 py-1 rounded-lg text-sm font-medium transition-colors ${
              filter === 'all' 
                ? 'bg-blue-600 text-white' 
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            Tous
          </button>
          <button
            onClick={() => setFilter('pending')}
            className={`px-3 py-1 rounded-lg text-sm font-medium transition-colors ${
              filter === 'pending' 
                ? 'bg-yellow-600 text-white' 
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            À faire
          </button>
          <button
            onClick={() => setFilter('completed')}
            className={`px-3 py-1 rounded-lg text-sm font-medium transition-colors ${
              filter === 'completed' 
                ? 'bg-green-600 text-white' 
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            Complétés
          </button>
        </div>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
          {error}
        </div>
      )}

      <div className="space-y-4">
        {filteredQuizzes.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <BookOpen className="w-12 h-12 mx-auto mb-3 text-gray-300" />
            <p className="text-lg font-medium">Aucun quiz {filter === 'pending' ? 'à faire' : filter === 'completed' ? 'complété' : 'assigné'}</p>
            <p className="text-sm">Vos professeurs vous assigneront des quiz bientôt</p>
          </div>
        ) : (
          filteredQuizzes.map((quiz) => {
            const isCompleted = isQuizCompleted(quiz.id);
            const completedQuiz = getCompletedQuiz(quiz.id);
            
            return (
              <div
                key={quiz.id}
                className={`p-4 rounded-lg border transition-all duration-200 hover-focus ${
                  isCompleted 
                    ? 'border-green-200 bg-green-50' 
                    : 'border-gray-200 bg-gray-50'
                }`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="font-semibold text-gray-800">{quiz.title}</h3>
                      {quiz.difficulty && (
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(quiz.difficulty)}`}>
                          {quiz.difficulty}
                        </span>
                      )}
                      {isCompleted && (
                        <CheckCircle className="w-5 h-5 text-green-600" />
                      )}
                    </div>
                    
                    <div className="flex items-center gap-4 text-sm text-gray-600 mb-3">
                      <span className="flex items-center gap-1">
                        <BookOpen className="w-4 h-4" />
                        {quiz.subject}
                      </span>
                      <span className="flex items-center gap-1">
                        <Target className="w-4 h-4" />
                        {quiz.level}
                      </span>
                      <span className="flex items-center gap-1">
                        <Clock className="w-4 h-4" />
                        {quiz.estimatedTime} min
                      </span>
                      <span className="flex items-center gap-1">
                        <Star className="w-4 h-4" />
                        {quiz.questionsCount} questions
                      </span>
                    </div>

                    {quiz.description && (
                      <p className="text-sm text-gray-600 mb-3">{quiz.description}</p>
                    )}

                    {quiz.dueDate && (
                      <div className="flex items-center gap-1 text-sm text-gray-600 mb-3">
                        <Calendar className="w-4 h-4" />
                        <span>Date limite: {new Date(quiz.dueDate).toLocaleDateString('fr-FR')}</span>
                      </div>
                    )}

                    {isCompleted && completedQuiz && (
                      <div className="flex items-center gap-3 mb-3">
                        <div className={`text-lg font-bold ${getScoreColor(completedQuiz.percentage)}`}>
                          Score: {completedQuiz.score}/{completedQuiz.max_score} ({completedQuiz.percentage}%)
                        </div>
                        {completedQuiz.percentage >= 80 && (
                          <Trophy className="w-5 h-5 text-yellow-500" />
                        )}
                      </div>
                    )}
                  </div>

                  <div className="flex flex-col gap-2 ml-4">
                    {isCompleted ? (
                      <button
                        onClick={() => handleViewAnswers(completedQuiz!)}
                        className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
                      >
                        <Eye className="w-4 h-4" />
                        Voir réponses
                      </button>
                    ) : (
                      <button
                        onClick={() => handleStartQuiz(quiz.id)}
                        disabled={loading === quiz.id}
                        className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 transition-colors text-sm font-medium"
                      >
                        {loading === quiz.id ? (
                          <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                        ) : (
                          <Play className="w-4 h-4" />
                        )}
                        Commencer
                      </button>
                    )}
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>

      {/* Modal pour afficher les réponses */}
      {showAnswers && selectedQuiz && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-4xl w-full mx-4 max-h-[80vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-bold text-gray-800">Réponses du Quiz</h3>
              <button
                onClick={() => setShowAnswers(false)}
                className="text-gray-500 hover:text-gray-700"
              >
                ✕
              </button>
            </div>
            
            <div className="space-y-4">
              {selectedQuiz.answers?.map((answer, index) => (
                <div
                  key={answer.question_id}
                  className={`p-4 rounded-lg border ${
                    answer.is_correct 
                      ? 'border-green-200 bg-green-50' 
                      : 'border-red-200 bg-red-50'
                  }`}
                >
                  <div className="flex items-start gap-3">
                    <div className={`w-6 h-6 rounded-full flex items-center justify-center text-sm font-bold ${
                      answer.is_correct 
                        ? 'bg-green-500 text-white' 
                        : 'bg-red-500 text-white'
                    }`}>
                      {index + 1}
                    </div>
                    <div className="flex-1">
                      <p className="font-medium text-gray-800 mb-2">{answer.question_text}</p>
                      
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-2">
                        <div>
                          <p className="text-sm font-medium text-gray-600 mb-1">Votre réponse:</p>
                          <p className={`text-sm p-2 rounded ${
                            answer.is_correct 
                              ? 'bg-green-100 text-green-800' 
                              : 'bg-red-100 text-red-800'
                          }`}>
                            {answer.student_answer}
                          </p>
                        </div>
                        <div>
                          <p className="text-sm font-medium text-gray-600 mb-1">Réponse correcte:</p>
                          <p className="text-sm p-2 rounded bg-blue-100 text-blue-800">
                            {answer.correct_answer}
                          </p>
                        </div>
                      </div>
                      
                      {answer.explanation && (
                        <div className="mt-2 p-2 bg-blue-50 rounded">
                          <p className="text-sm font-medium text-blue-800 mb-1">Explication:</p>
                          <p className="text-sm text-blue-700">{answer.explanation}</p>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
            
            <div className="mt-6 flex justify-end">
              <button
                onClick={() => setShowAnswers(false)}
                className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
              >
                Fermer
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
