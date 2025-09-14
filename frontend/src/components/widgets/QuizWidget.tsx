"use client";

import React, { useEffect, useState } from 'react';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface Quiz {
  id: number;
  title: string;
  description?: string;
  subject: string;
  level: string;
  total_points: number;
  is_active: boolean;
  created_at: string;
  questions: Question[];
}

interface Question {
  id: number;
  question_text: string;
  question_type: 'mcq' | 'true_false' | 'text';
  points: number;
  order: number;
  options?: string[];
  correct_answer?: any;
}

interface QuizResult {
  id: number;
  student_id: number;
  score: number;
  max_score: number;
  percentage: number;
  is_completed: boolean;
  completed_at?: string;
}

function CreateQuizModal({ onClose, onCreated }: { onClose: () => void; onCreated: () => void }) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [subject, setSubject] = useState('');
  const [level, setLevel] = useState('medium');
  const [timeLimit, setTimeLimit] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem('najah_token');
      const res = await fetch(`${API_BASE_URL}/api/v1/quizzes/`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ 
          title, 
          description, 
          subject, 
          level,
          time_limit: timeLimit
        })
      });
      if (!res.ok) throw new Error('Erreur lors de la création du quiz');
      onCreated();
      onClose();
    } catch (err: any) {
      setError(err.message || 'Erreur inconnue');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-30">
      <form onSubmit={handleSubmit} className="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full relative">
        <button type="button" onClick={onClose} className="absolute top-4 right-4 text-gray-400 hover:text-blue-600 text-xl font-bold">×</button>
        <h3 className="text-2xl font-bold text-blue-700 mb-4">Nouveau Quiz</h3>
        
        <div className="mb-4">
          <label className="block text-gray-700 font-semibold mb-1">Titre</label>
          <input value={title} onChange={e => setTitle(e.target.value)} required className="w-full border rounded-lg px-3 py-2" />
        </div>
        
        <div className="mb-4">
          <label className="block text-gray-700 font-semibold mb-1">Description</label>
          <textarea value={description} onChange={e => setDescription(e.target.value)} className="w-full border rounded-lg px-3 py-2" />
        </div>
        
        <div className="mb-4">
          <label className="block text-gray-700 font-semibold mb-1">Matière</label>
          <input value={subject} onChange={e => setSubject(e.target.value)} required className="w-full border rounded-lg px-3 py-2" />
        </div>
        
        <div className="mb-4">
          <label className="block text-gray-700 font-semibold mb-1">Niveau</label>
          <select value={level} onChange={e => setLevel(e.target.value)} className="w-full border rounded-lg px-3 py-2">
            <option value="easy">Facile</option>
            <option value="medium">Moyen</option>
            <option value="hard">Difficile</option>
          </select>
        </div>
        
        <div className="mb-4">
          <label className="block text-gray-700 font-semibold mb-1">Limite de temps (minutes, optionnel)</label>
          <input type="number" value={timeLimit || ''} onChange={e => setTimeLimit(e.target.value ? Number(e.target.value) : null)} className="w-full border rounded-lg px-3 py-2" />
        </div>
        
        {error && <div className="text-red-600 mb-2">{error}</div>}
        <button type="submit" disabled={loading} className="px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition">
          {loading ? 'Création...' : 'Créer'}
        </button>
      </form>
    </div>
  );
}

function AddQuestionModal({ quizId, onClose, onAdded }: { quizId: number; onClose: () => void; onAdded: () => void }) {
  const [questionText, setQuestionText] = useState('');
  const [questionType, setQuestionType] = useState<'mcq' | 'true_false' | 'text'>('mcq');
  const [points, setPoints] = useState(1);
  const [options, setOptions] = useState(['', '', '', '']);
  const [correctAnswer, setCorrectAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem('najah_token');
      
      let questionData: any = {
        question_text: questionText,
        question_type: questionType,
        points: points
      };

      if (questionType === 'mcq') {
        questionData.options = options.filter(opt => opt.trim() !== '');
        questionData.correct_answer = parseInt(correctAnswer);
      } else if (questionType === 'true_false') {
        questionData.correct_answer = correctAnswer === 'true';
      } else {
        questionData.correct_answer = correctAnswer;
      }

      const res = await fetch(`${API_BASE_URL}/api/v1/quizzes/${quizId}/questions`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(questionData)
      });
      if (!res.ok) throw new Error('Erreur lors de l\'ajout de la question');
      onAdded();
      onClose();
    } catch (err: any) {
      setError(err.message || 'Erreur inconnue');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-30">
      <form onSubmit={handleSubmit} className="bg-white rounded-2xl shadow-2xl p-8 max-w-lg w-full relative max-h-[90vh] overflow-y-auto">
        <button type="button" onClick={onClose} className="absolute top-4 right-4 text-gray-400 hover:text-blue-600 text-xl font-bold">×</button>
        <h3 className="text-2xl font-bold text-blue-700 mb-4">Ajouter une Question</h3>
        
        <div className="mb-4">
          <label className="block text-gray-700 font-semibold mb-1">Question</label>
          <textarea value={questionText} onChange={e => setQuestionText(e.target.value)} required className="w-full border rounded-lg px-3 py-2" rows={3} />
        </div>
        
        <div className="mb-4">
          <label className="block text-gray-700 font-semibold mb-1">Type de question</label>
          <select value={questionType} onChange={e => setQuestionType(e.target.value as any)} className="w-full border rounded-lg px-3 py-2">
            <option value="mcq">QCM</option>
            <option value="true_false">Vrai/Faux</option>
            <option value="text">Texte libre</option>
          </select>
        </div>
        
        <div className="mb-4">
          <label className="block text-gray-700 font-semibold mb-1">Points</label>
          <input type="number" min="0" step="0.5" value={points} onChange={e => setPoints(Number(e.target.value))} className="w-full border rounded-lg px-3 py-2" />
        </div>
        
        {questionType === 'mcq' && (
          <div className="mb-4">
            <label className="block text-gray-700 font-semibold mb-1">Options</label>
            {options.map((option, index) => (
              <input key={index} value={option} onChange={e => {
                const newOptions = [...options];
                newOptions[index] = e.target.value;
                setOptions(newOptions);
              }} placeholder={`Option ${index + 1}`} className="w-full border rounded-lg px-3 py-2 mb-2" />
            ))}
            <label className="block text-gray-700 font-semibold mb-1 mt-4">Réponse correcte (numéro d'option)</label>
            <input type="number" min="0" max={options.length - 1} value={correctAnswer} onChange={e => setCorrectAnswer(e.target.value)} className="w-full border rounded-lg px-3 py-2" />
          </div>
        )}
        
        {questionType === 'true_false' && (
          <div className="mb-4">
            <label className="block text-gray-700 font-semibold mb-1">Réponse correcte</label>
            <select value={correctAnswer} onChange={e => setCorrectAnswer(e.target.value)} className="w-full border rounded-lg px-3 py-2">
              <option value="">Sélectionner</option>
              <option value="true">Vrai</option>
              <option value="false">Faux</option>
            </select>
          </div>
        )}
        
        {questionType === 'text' && (
          <div className="mb-4">
            <label className="block text-gray-700 font-semibold mb-1">Réponse correcte</label>
            <input value={correctAnswer} onChange={e => setCorrectAnswer(e.target.value)} className="w-full border rounded-lg px-3 py-2" />
          </div>
        )}
        
        {error && <div className="text-red-600 mb-2">{error}</div>}
        <button type="submit" disabled={loading} className="px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition">
          {loading ? 'Ajout...' : 'Ajouter'}
        </button>
      </form>
    </div>
  );
}

function QuizResultsModal({ quizId, onClose }: { quizId: number; onClose: () => void }) {
  const [results, setResults] = useState<QuizResult[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchResults = async () => {
      try {
        const token = localStorage.getItem('najah_token');
        const res = await fetch(`${API_BASE_URL}/api/v1/quizzes/${quizId}/results`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
          const data = await res.json();
          setResults(data);
        }
      } catch (error) {
        console.error('Erreur lors du chargement des résultats:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchResults();
  }, [quizId]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-30">
      <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-4xl w-full relative max-h-[90vh] overflow-y-auto">
        <button type="button" onClick={onClose} className="absolute top-4 right-4 text-gray-400 hover:text-blue-600 text-xl font-bold">×</button>
        <h3 className="text-2xl font-bold text-blue-700 mb-4">Résultats du Quiz</h3>
        
        {loading ? (
          <div className="text-center py-8">Chargement...</div>
        ) : results.length === 0 ? (
          <div className="text-center py-8 text-gray-500">Aucun résultat pour ce quiz</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full border-collapse border border-gray-300">
              <thead>
                <tr className="bg-gray-100">
                  <th className="border border-gray-300 px-4 py-2">Élève ID</th>
                  <th className="border border-gray-300 px-4 py-2">Score</th>
                  <th className="border border-gray-300 px-4 py-2">Pourcentage</th>
                  <th className="border border-gray-300 px-4 py-2">Statut</th>
                  <th className="border border-gray-300 px-4 py-2">Date</th>
                </tr>
              </thead>
              <tbody>
                {results.map((result) => (
                  <tr key={result.id}>
                    <td className="border border-gray-300 px-4 py-2">{result.student_id}</td>
                    <td className="border border-gray-300 px-4 py-2">{result.score}/{result.max_score}</td>
                    <td className="border border-gray-300 px-4 py-2">{result.percentage.toFixed(1)}%</td>
                    <td className="border border-gray-300 px-4 py-2">
                      <span className={`px-2 py-1 rounded text-sm ${result.is_completed ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                        {result.is_completed ? 'Terminé' : 'En cours'}
                      </span>
                    </td>
                    <td className="border border-gray-300 px-4 py-2">
                      {result.completed_at ? new Date(result.completed_at).toLocaleDateString() : '-'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

interface QuizWidgetProps {
  quizResults?: any[];
  className?: string;
}

export default function QuizWidget({ quizResults, className }: QuizWidgetProps) {
  const [quizzes, setQuizzes] = useState<Quiz[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showAddQuestionModal, setShowAddQuestionModal] = useState(false);
  const [showResultsModal, setShowResultsModal] = useState(false);
  const [selectedQuizId, setSelectedQuizId] = useState<number | null>(null);

  // Fonction réutilisable pour charger les quiz
  const fetchQuizzes = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const token = localStorage.getItem('najah_token');
      if (!token) {
        setError("Token d'authentification manquant");
        setLoading(false);
        return;
      }

      const response = await fetch(`${API_BASE_URL}/api/v1/quizzes/`, {
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }

      const data = await response.json();
      
      // Transformer les données pour correspondre à l'interface Quiz
      const transformedQuizzes = data.map((quiz: any) => ({
        id: quiz.id,
        title: quiz.title,
        description: quiz.description,
        subject: quiz.subject,
        level: quiz.difficulty || 'medium',
        total_points: quiz.max_score || 100,
        is_active: quiz.is_active,
        created_at: quiz.created_at,
        questions: quiz.questions || []
      }));

      setQuizzes(transformedQuizzes);
      setLoading(false);
      
    } catch (err) {
      console.error("Erreur lors du chargement des quiz:", err);
      setError("Erreur lors du chargement des quiz");
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchQuizzes();
  }, []);

  const handleDeleteQuiz = async (quizId: number) => {
    if (!confirm('Êtes-vous sûr de vouloir supprimer ce quiz ?')) return;
    
    try {
      const token = localStorage.getItem('najah_token');
      const res = await fetch(`${API_BASE_URL}/api/v1/quizzes/${quizId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        // Recharger les quiz après suppression
        fetchQuizzes();
      }
    } catch (error) {
      console.error('Erreur lors de la suppression:', error);
    }
  };

  if (loading) {
    return <div className="text-center py-8">Chargement des quiz...</div>;
  }

  return (
    <div className={`bg-white rounded-lg shadow-sm ${className || ''}`}>
      <div className="flex justify-between items-center mb-4 p-4 border-b">
        <h2 className="text-lg font-bold text-gray-800">Gestion des Quiz</h2>
        <button
          onClick={() => setShowCreateModal(true)}
          className="px-3 py-1 bg-blue-600 text-white rounded text-sm font-medium hover:bg-blue-700 transition"
        >
          Nouveau Quiz
        </button>
      </div>

      {quizzes.length === 0 ? (
        <div className="text-center py-6 text-gray-500 px-4">
          Aucun quiz créé. Commencez par créer votre premier quiz !
        </div>
      ) : (
        <div className="p-4 max-h-96 overflow-y-auto">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-1 xl:grid-cols-2 gap-4">
            {quizzes.map((quiz) => (
              <div key={quiz.id} className="border rounded-lg p-4 hover:shadow-md transition bg-gray-50">
                <div className="space-y-3">
                  <div>
                    <h3 className="text-base font-semibold text-gray-800 truncate">{quiz.title}</h3>
                    {quiz.description && (
                      <p className="text-gray-600 text-sm mt-1 line-clamp-2">{quiz.description}</p>
                    )}
                  </div>
                  
                  <div className="flex flex-wrap gap-2 text-xs text-gray-500">
                    <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded">{quiz.subject}</span>
                    <span className="bg-green-100 text-green-800 px-2 py-1 rounded">{quiz.level}</span>
                    <span className="bg-purple-100 text-purple-800 px-2 py-1 rounded">{quiz.total_points} pts</span>
                    <span className={`px-2 py-1 rounded ${quiz.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                      {quiz.is_active ? 'Actif' : 'Inactif'}
                    </span>
                  </div>
                  
                  <div className="text-xs text-gray-500">
                    Questions: {quiz.questions?.length || 0}
                  </div>
                  
                  <div className="flex gap-2 pt-2">
                    <button
                      onClick={() => {
                        setSelectedQuizId(quiz.id);
                        setShowAddQuestionModal(true);
                      }}
                      className="flex-1 px-2 py-1 bg-green-600 text-white rounded text-xs hover:bg-green-700 transition"
                    >
                      + Question
                    </button>
                    <button
                      onClick={() => {
                        setSelectedQuizId(quiz.id);
                        setShowResultsModal(true);
                      }}
                      className="flex-1 px-2 py-1 bg-purple-600 text-white rounded text-xs hover:bg-purple-700 transition"
                    >
                      Résultats
                    </button>
                    <button
                      onClick={() => handleDeleteQuiz(quiz.id)}
                      className="px-2 py-1 bg-red-600 text-white rounded text-xs hover:bg-red-700 transition"
                    >
                      ×
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {showCreateModal && (
        <CreateQuizModal
          onClose={() => setShowCreateModal(false)}
          onCreated={() => {
            setShowCreateModal(false);
            fetchQuizzes(); // Re-fetch quizzes after creation
          }}
        />
      )}

      {showAddQuestionModal && selectedQuizId && (
        <AddQuestionModal
          quizId={selectedQuizId}
          onClose={() => {
            setShowAddQuestionModal(false);
            setSelectedQuizId(null);
          }}
          onAdded={() => {
            setShowAddQuestionModal(false);
            setSelectedQuizId(null);
            fetchQuizzes(); // Re-fetch quizzes after adding question
          }}
        />
      )}

      {showResultsModal && selectedQuizId && (
        <QuizResultsModal
          quizId={selectedQuizId}
          onClose={() => {
            setShowResultsModal(false);
            setSelectedQuizId(null);
          }}
        />
      )}
    </div>
  );
} 