"use client";

import React, { useState, useEffect } from 'react';
import { Card } from '../Card';
import { BookOpen, Clock, Target, Play, CheckCircle, Eye } from 'lucide-react';

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
}

interface CompletedQuiz {
  id: number;
  quiz_id: number;
  score: number;
  max_score: number;
  percentage: number;
  completed: boolean;
  created_at: string;
}

interface AssignedQuizzesWidgetProps {
  assignedQuizzes: AssignedQuiz[];
  className?: string;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function AssignedQuizzesWidget({ assignedQuizzes, className = '' }: AssignedQuizzesWidgetProps) {
  const [loading, setLoading] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [completedQuizzes, setCompletedQuizzes] = useState<CompletedQuiz[]>([]);
  const [showCompletedQuizzes, setShowCompletedQuizzes] = useState(false);

  // Charger les quiz complétés
  useEffect(() => {
    const loadCompletedQuizzes = async () => {
      try {
        const token = localStorage.getItem('najah_token');
        const user = localStorage.getItem('najah_user');
        
        if (!token || !user) return;
        
        const userData = JSON.parse(user);
        const response = await fetch(`${API_BASE_URL}/api/v1/quiz_results/user/${userData.id}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        if (response.ok) {
          const data = await response.json();
          const completed = data.filter((quiz: any) => quiz.completed || quiz.is_completed);
          setCompletedQuizzes(completed);
        }
      } catch (error) {
        console.error('Erreur lors du chargement des quiz complétés:', error);
      }
    };
    
    loadCompletedQuizzes();
  }, []);

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

  const handleViewResults = (quizId: number) => {
    window.location.href = `/dashboard/student/quiz/${quizId}`;
  };

  const isQuizCompleted = (quizId: number) => {
    return completedQuizzes.some(quiz => quiz.quiz_id === quizId);
  };

  const getCompletedQuiz = (quizId: number) => {
    return completedQuizzes.find(quiz => quiz.quiz_id === quizId);
  };

  const cleanScore = (score: number, maxScore: number, percentage: number) => {
    // Nettoyer les scores anormaux
    let cleanScore = score;
    let cleanMaxScore = maxScore;
    let cleanPercentage = percentage;

    // Si le score est plus grand que le max, ajuster
    if (cleanScore > cleanMaxScore && cleanMaxScore > 0) {
      cleanScore = cleanMaxScore;
    }

    // Si le pourcentage est anormal (> 100%), le recalculer
    if (cleanPercentage > 100 && cleanMaxScore > 0) {
      cleanPercentage = Math.round((cleanScore / cleanMaxScore) * 100);
    }

    // S'assurer que le pourcentage est entre 0 et 100
    cleanPercentage = Math.max(0, Math.min(100, cleanPercentage));

    return {
      score: cleanScore,
      maxScore: cleanMaxScore,
      percentage: cleanPercentage
    };
  };

  const formatDate = (dateString: string) => {
    try {
      const date = new Date(dateString);
      if (isNaN(date.getTime())) {
        return 'Date invalide';
      }
      return date.toLocaleDateString('fr-FR', {
        day: 'numeric',
        month: 'short',
        year: 'numeric'
      });
    } catch (error) {
      return 'Date invalide';
    }
  };

  const getDifficultyColor = (level: string | undefined | null) => {
    if (!level) return 'text-gray-600 bg-gray-100';
    
    switch (level.toLowerCase()) {
      case 'easy': return 'text-green-600 bg-green-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      case 'hard': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getDifficultyText = (level: string | undefined | null) => {
    if (!level) return 'Non défini';
    
    switch (level.toLowerCase()) {
      case 'easy': return 'Facile';
      case 'medium': return 'Moyen';
      case 'hard': return 'Difficile';
      default: return level;
    }
  };

  // Séparer les quiz assignés et complétés
  const activeQuizzes = assignedQuizzes.filter(quiz => !isQuizCompleted(quiz.id));
  const completedQuizzesList = assignedQuizzes.filter(quiz => isQuizCompleted(quiz.id));

  return (
    <div className={`space-y-6 ${className}`}>
      <Card title="Mes Quiz" icon={<BookOpen />} className="p-6">
        {activeQuizzes.length === 0 && completedQuizzesList.length === 0 ? (
          <div className="text-center py-8">
            <BookOpen className="mx-auto text-gray-400 mb-4" size={48} />
            <h3 className="text-lg font-semibold text-gray-600 mb-2">Aucun quiz assigné</h3>
            <p className="text-gray-500">Tes professeurs t'assigneront des quiz ici.</p>
          </div>
        ) : (
          <div className="space-y-6">
            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
                {error}
              </div>
            )}
            
            {/* Quiz Actifs */}
            {activeQuizzes.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
                  <Play className="text-blue-600" size={20} />
                  Quiz à faire ({activeQuizzes.length})
                </h3>
                <div className="space-y-4 max-h-96 overflow-y-auto">
                  {activeQuizzes.map((quiz) => (
                    <div key={quiz.assignmentId} className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex-1">
                          <h3 className="text-lg font-semibold text-gray-800 mb-1">{quiz.title || 'Quiz sans titre'}</h3>
                          <p className="text-gray-600 text-sm mb-2">{quiz.subject || 'Matière non définie'}</p>
                          
                          <div className="flex items-center gap-4 text-sm text-gray-500 mb-3">
                            <div className="flex items-center gap-1">
                              <Target size={16} />
                              <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(quiz.level)}`}>
                                {getDifficultyText(quiz.level)}
                              </span>
                            </div>
                            <div className="flex items-center gap-1">
                              <Clock size={16} />
                              <span>{quiz.estimatedTime || 15} min</span>
                            </div>
                            <div className="flex items-center gap-1">
                              <BookOpen size={16} />
                              <span>{quiz.questionsCount || 0} questions</span>
                            </div>
                          </div>
                          
                          <div className="text-xs text-gray-500">
                            <p>Assigné le {quiz.assignedAt ? formatDate(quiz.assignedAt) : 'Date inconnue'}</p>
                            {quiz.dueDate && (
                              <p className="text-orange-600 font-medium">
                                À rendre avant le {formatDate(quiz.dueDate)}
                              </p>
                            )}
                          </div>
                        </div>
                        
                        <button
                          onClick={() => handleStartQuiz(quiz.id)}
                          disabled={loading === quiz.id}
                          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                          {loading === quiz.id ? (
                            <>
                              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                              Chargement...
                            </>
                          ) : (
                            <>
                              <Play size={16} />
                              Commencer
                            </>
                          )}
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Quiz Complétés */}
            {completedQuizzesList.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
                  <CheckCircle className="text-green-600" size={20} />
                  Quiz Complétés ({completedQuizzesList.length})
                </h3>
                <div className="space-y-4 max-h-96 overflow-y-auto">
                  {completedQuizzesList.map((quiz) => {
                    const completedQuiz = getCompletedQuiz(quiz.id);
                    return (
                      <div key={quiz.assignmentId} className="bg-green-50 border border-green-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                        <div className="flex items-start justify-between mb-3">
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-1">
                              <CheckCircle className="text-green-600" size={16} />
                              <h3 className="text-lg font-semibold text-gray-800">{quiz.title || 'Quiz sans titre'}</h3>
                            </div>
                            <p className="text-gray-600 text-sm mb-2">{quiz.subject || 'Matière non définie'}</p>
                            
                            {completedQuiz && (
                              <div className="mb-3">
                                <div className="flex items-center gap-4 text-sm">
                                  {(() => {
                                    const clean = cleanScore(completedQuiz.score, completedQuiz.max_score, completedQuiz.percentage);
                                    // Calculer le pourcentage manuellement si nécessaire
                                    let percentage = clean.percentage;
                                    if (isNaN(percentage) || percentage === 0) {
                                      percentage = clean.maxScore > 0 ? Math.round((clean.score / clean.maxScore) * 100) : 0;
                                    }
                                    return (
                                      <span className={`font-semibold ${percentage >= 80 ? 'text-green-600' : percentage >= 60 ? 'text-yellow-600' : 'text-red-600'}`}>
                                        Score: {clean.score}/{clean.maxScore} ({percentage}%)
                                      </span>
                                    );
                                  })()}
                                  <span className="text-gray-500">
                                    Complété le {formatDate(completedQuiz.created_at)}
                                  </span>
                                </div>
                              </div>
                            )}
                            
                            <div className="flex items-center gap-4 text-sm text-gray-500 mb-3">
                              <div className="flex items-center gap-1">
                                <Target size={16} />
                                <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(quiz.level)}`}>
                                  {getDifficultyText(quiz.level)}
                                </span>
                              </div>
                              <div className="flex items-center gap-1">
                                <Clock size={16} />
                                <span>{quiz.estimatedTime || 15} min</span>
                              </div>
                              <div className="flex items-center gap-1">
                                <BookOpen size={16} />
                                <span>{quiz.questionsCount || 0} questions</span>
                              </div>
                            </div>
                          </div>
                          
                          <button
                            onClick={() => handleViewResults(quiz.id)}
                            className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg font-semibold hover:bg-green-700 transition"
                          >
                            <Eye size={16} />
                            Consulter
                          </button>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}
          </div>
        )}
      </Card>
    </div>
  );
} 