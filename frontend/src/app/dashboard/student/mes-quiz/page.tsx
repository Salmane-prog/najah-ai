"use client";
import React, { useEffect, useState, useContext } from 'react';
import { useAuth  } from '../../../../hooks/useAuth';
import Button from '../../../../components/Button';
import { Card } from '../../../../components/Card';
import { useRouter } from 'next/navigation';

interface QuizAssignment {
  id: number;
  quiz_id: number;
  title: string;
  due_date?: string;
  status?: string;
  // autres champs utiles
}

interface QuizQuestion {
  id: number;
  question: string;
  choices: string[];
  type: string;
}

interface Correction {
  question: string;
  student_answer: string;
  correct_answer: string;
  is_correct: boolean;
  points: number;
}

interface CompletedQuiz {
  id: number;
  quiz_id: number;
  score: number;
  max_score: number;
  percentage: number;
  created_at: string;
  completed?: boolean;
  is_completed?: boolean;
}

const getQuizKey = (quizId: number, userId: number) => `quiz_${quizId}_user_${userId}_answers`;

const MesQuizPage: React.FC = () => {
  const { user, token } = useAuth();
  const router = useRouter();
  const [quizList, setQuizList] = useState<QuizAssignment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedQuiz, setSelectedQuiz] = useState<QuizAssignment | null>(null);
  const [questions, setQuestions] = useState<QuizQuestion[]>([]);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [currentIdx, setCurrentIdx] = useState(0);
  const [submitting, setSubmitting] = useState(false);
  const [correction, setCorrection] = useState<{
    score: number;
    max_score: number;
    percentage: number;
    corrections: Correction[];
  } | null>(null);
  const [notification, setNotification] = useState<string | null>(null);
  const [notifVisible, setNotifVisible] = useState(false);
  const [completedQuizzes, setCompletedQuizzes] = useState<CompletedQuiz[]>([]);
  const [showCompletedQuizzes, setShowCompletedQuizzes] = useState(false);

  // WebSocket pour notifications temps réel avec animation
  useEffect(() => {
    if (!user || !token) return;
    const ws = new WebSocket(`${process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000'}/api/v1/ws/notifications/?token=${token}`);
    ws.onmessage = (event) => {
      setNotification(event.data);
      setNotifVisible(true);
      setTimeout(() => setNotifVisible(false), 3500);
    };
    return () => ws.close();
  }, [user, token]);

  // Sauvegarde auto des réponses
  useEffect(() => {
    if (!selectedQuiz || !user) return;
    const key = getQuizKey(selectedQuiz.quiz_id, user.id);
    localStorage.setItem(key, JSON.stringify(answers));
  }, [answers, selectedQuiz, user]);

  // Restauration auto des réponses
  useEffect(() => {
    if (!selectedQuiz || !user) return;
    const key = getQuizKey(selectedQuiz.quiz_id, user.id);
    const saved = localStorage.getItem(key);
    if (saved) setAnswers(JSON.parse(saved));
  }, [selectedQuiz, user]);

  useEffect(() => {
    const fetchQuizAssignments = async () => {
      setLoading(true);
      try {
        const res = await fetch(`/api/proxy/quizzes/assigned/?student_id=${user?.id}`);
        if (!res.ok) throw new Error('Erreur lors du chargement des quiz assignés');
        const data = await res.json();
        console.log('[DEBUG] Quiz assignés:', data);
        setQuizList(data);
        
        // Charger aussi les résultats des quiz complétés
        if (user?.id) {
          console.log('[DEBUG] Chargement des résultats pour user ID:', user.id);
          const resultsRes = await fetch(`/api/proxy/quiz_results/user/${user.id}`);
          if (resultsRes.ok) {
            const resultsData = await resultsRes.json();
            console.log('[DEBUG] Résultats bruts:', resultsData);
            const completed = resultsData.filter((r: CompletedQuiz) => r.completed || r.is_completed);
            console.log('[DEBUG] Quiz complétés filtrés:', completed);
            setCompletedQuizzes(completed);
          } else {
            console.log('[DEBUG] Erreur lors du chargement des résultats:', resultsRes.status);
          }
        }
      } catch (err: unknown) {
        const errorMessage = err instanceof Error ? err.message : 'Erreur inconnue';
        console.log('[DEBUG] Erreur:', errorMessage);
        setError(errorMessage);
      } finally {
        setLoading(false);
      }
    };
    fetchQuizAssignments();
  }, [user]);

  // Passage du quiz : charger les questions
  const handleStartQuiz = async (quiz: QuizAssignment) => {
    setSelectedQuiz(quiz);
    setCorrection(null);
    setAnswers({});
    setCurrentIdx(0);
    try {
      const res = await fetch(`/api/proxy/quizzes/${quiz.quiz_id}/start`);
      if (!res.ok) throw new Error('Erreur lors du chargement du quiz');
      const data = await res.json();
      setQuestions(data.questions);
    } catch (err) {
      setNotification('Erreur lors du chargement du quiz');
      setNotifVisible(true);
      setTimeout(() => setNotifVisible(false), 3500);
    }
  };

  // Gestion des réponses
  const handleAnswerChange = (questionId: number, value: string) => {
    setAnswers((prev) => ({ ...prev, [questionId]: value }));
  };

  // Soumission du quiz
  const handleSubmitQuiz = async () => {
    if (!selectedQuiz) return;
    
    // Vérifier si le quiz est déjà complété
    const status = getQuizStatus(selectedQuiz);
    if (status === 'corrigé') {
      setNotification('Ce quiz a déjà été complété. Vous ne pouvez pas le soumettre à nouveau.');
      setNotifVisible(true);
      setTimeout(() => setNotifVisible(false), 3500);
      return;
    }
    
    setSubmitting(true);
    setCorrection(null);
    try {
      const payload = questions.map((q) => ({ question_id: q.id, answer: answers[q.id] || '' }));
      const res = await fetch(`/api/proxy/quizzes/${selectedQuiz.quiz_id}/submit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error('Erreur lors de la soumission');
      const data = await res.json();
      setCorrection(data);
      // Nettoyer la sauvegarde locale après correction
      if (user) localStorage.removeItem(getQuizKey(selectedQuiz.quiz_id, user.id));
    } catch (err) {
      setNotification('Erreur lors de la soumission');
      setNotifVisible(true);
      setTimeout(() => setNotifVisible(false), 3500);
    } finally {
      setSubmitting(false);
    }
  };

  // Déterminer le statut du quiz (amélioré)
  const getQuizStatus = (quiz: QuizAssignment) => {
    console.log('[DEBUG] getQuizStatus pour quiz:', quiz.quiz_id);
    console.log('[DEBUG] completedQuizzes:', completedQuizzes);
    
    // Vérifier si le quiz est dans les résultats complétés
    const completedQuiz = completedQuizzes.find((cq: CompletedQuiz) => cq.quiz_id === quiz.quiz_id);
    console.log('[DEBUG] Quiz trouvé dans completedQuizzes:', completedQuiz);
    
    if (completedQuiz) {
      console.log('[DEBUG] Quiz marqué comme complété');
      return 'complété';
    }
    
    if (correction && selectedQuiz && quiz.id === selectedQuiz.id) return 'corrigé';
    if (user) {
      const key = getQuizKey(quiz.quiz_id, user.id);
      if (localStorage.getItem(key)) return 'en cours';
    }
    return quiz.status || 'non commencé';
  };

  // Navigation question par question
  const handleNext = () => setCurrentIdx((idx) => Math.min(idx + 1, questions.length - 1));
  const handlePrev = () => setCurrentIdx((idx) => Math.max(idx - 1, 0));

  return (
    <div className="container mx-auto py-8">
      {/* Notification animée */}
      {notification && (
        <div className={`fixed top-4 left-1/2 transform -translate-x-1/2 z-50 px-6 py-3 rounded shadow-lg transition-all duration-500 ${notifVisible ? 'opacity-100 scale-100 bg-blue-100 border border-blue-400 text-blue-700' : 'opacity-0 scale-95 pointer-events-none'}`}>{notification}</div>
      )}
      <h1 className="text-2xl font-bold mb-6">Mes quiz</h1>
      
      {/* Widget Quiz Complétés */}
      {completedQuizzes.length > 0 && (
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold">Quiz Complétés ({completedQuizzes.length})</h2>
            <button
              onClick={() => setShowCompletedQuizzes(!showCompletedQuizzes)}
              className="text-blue-600 hover:text-blue-800 font-medium"
            >
              {showCompletedQuizzes ? 'Masquer' : 'Voir'} les détails
            </button>
          </div>
          
          {showCompletedQuizzes && (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {completedQuizzes.map((quiz: CompletedQuiz) => (
                <div key={quiz.id} className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="text-green-600 font-semibold">✓ Complété</span>
                    <span className="text-sm text-gray-500">
                      {new Date(quiz.created_at).toLocaleDateString()}
                    </span>
                  </div>
                  <h3 className="font-semibold mb-2">Quiz #{quiz.quiz_id}</h3>
                  <div className="text-sm text-gray-600 mb-3">
                    Score: {quiz.score}/{quiz.max_score} ({quiz.percentage}%)
                  </div>
                  <button
                    onClick={() => window.location.href = `/dashboard/student/quiz/${quiz.quiz_id}`}
                    className="w-full px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 text-sm"
                  >
                    Consulter les résultats
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
      
      {/* Affichage passage quiz */}
      {selectedQuiz && questions.length > 0 && !correction && (
        <div className="max-w-2xl mx-auto bg-white rounded shadow p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">{selectedQuiz.title || `Quiz #${selectedQuiz.quiz_id}`}</h2>
          <div className="flex items-center justify-between mb-4">
            <span>Question {currentIdx + 1} / {questions.length}</span>
            <div className="flex gap-2">
              <Button onClick={handlePrev} disabled={currentIdx === 0} variant="secondary">Précédent</Button>
              {currentIdx < questions.length - 1 ? (
                <Button onClick={handleNext} variant="secondary">Suivant</Button>
              ) : (
                <Button onClick={handleSubmitQuiz} disabled={submitting} className="ml-2">{submitting ? 'Soumission...' : 'Soumettre'}</Button>
              )}
            </div>
          </div>
          <form onSubmit={e => { e.preventDefault(); handleSubmitQuiz(); }}>
            <div key={questions[currentIdx].id} className="mb-6">
              <div className="font-medium mb-2">{questions[currentIdx].question}</div>
              {questions[currentIdx].type === 'mcq' && (
                <div className="flex flex-col gap-2">
                  {questions[currentIdx].choices.map((choice, i) => (
                    <label key={i} className={`flex items-center gap-2 px-2 py-1 rounded cursor-pointer ${answers[questions[currentIdx].id] === String(i) ? 'bg-blue-100 border border-blue-400' : ''}`}>
                      <input
                        type="radio"
                        name={`q_${questions[currentIdx].id}`}
                        value={i}
                        checked={answers[questions[currentIdx].id] === String(i)}
                        onChange={() => handleAnswerChange(questions[currentIdx].id, String(i))}
                      />
                      {choice}
                    </label>
                  ))}
                </div>
              )}
              {questions[currentIdx].type === 'text' && (
                <input
                  type="text"
                  className="border rounded px-2 py-1 w-full"
                  value={answers[questions[currentIdx].id] || ''}
                  onChange={e => handleAnswerChange(questions[currentIdx].id, e.target.value)}
                />
              )}
              {questions[currentIdx].type === 'true_false' && (
                <div className="flex gap-4">
                  <label className={`px-2 py-1 rounded cursor-pointer ${answers[questions[currentIdx].id] === 'true' ? 'bg-blue-100 border border-blue-400' : ''}`}>
                    <input
                      type="radio"
                      name={`q_${questions[currentIdx].id}`}
                      value="true"
                      checked={answers[questions[currentIdx].id] === 'true'}
                      onChange={() => handleAnswerChange(questions[currentIdx].id, 'true')}
                    />
                    Vrai
                  </label>
                  <label className={`px-2 py-1 rounded cursor-pointer ${answers[questions[currentIdx].id] === 'false' ? 'bg-blue-100 border border-blue-400' : ''}`}>
                    <input
                      type="radio"
                      name={`q_${questions[currentIdx].id}`}
                      value="false"
                      checked={answers[questions[currentIdx].id] === 'false'}
                      onChange={() => handleAnswerChange(questions[currentIdx].id, 'false')}
                    />
                    Faux
                  </label>
                </div>
              )}
            </div>
          </form>
          <div className="flex justify-center gap-2 mt-4">
            {questions.map((_, idx) => (
              <span key={idx} className={`w-3 h-3 rounded-full inline-block mx-1 ${idx === currentIdx ? 'bg-blue-500' : 'bg-gray-300'}`}></span>
            ))}
          </div>
        </div>
      )}
      {/* Affichage correction */}
      {correction && (
        <div className="max-w-2xl mx-auto bg-green-50 rounded shadow p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Correction</h2>
          <div className="mb-2">Score : <span className="font-bold">{correction.score} / {correction.max_score}</span> ({correction.percentage.toFixed(1)}%)</div>
          <div className="mb-4">
            {correction.corrections.map((corr: Correction, idx: number) => (
              <div key={idx} className={`mb-2 p-2 rounded ${corr.is_correct ? 'bg-green-100' : 'bg-red-100'}`}>
                <div className="font-medium">{corr.question}</div>
                <div>Votre réponse : <span className="font-mono">{corr.student_answer}</span></div>
                <div>Bonne réponse : <span className="font-mono">{corr.correct_answer}</span></div>
                <div>{corr.is_correct ? '✔️ Bonne réponse' : '❌ Mauvaise réponse'} ({corr.points} pts)</div>
              </div>
            ))}
          </div>
          <Button onClick={() => { setSelectedQuiz(null); setQuestions([]); setCorrection(null); }}>Retour à la liste</Button>
        </div>
      )}
      {/* Liste des quiz assignés */}
      {!selectedQuiz && (
        <div className="grid gap-4">
          {quizList.length === 0 && !loading && <div>Aucun quiz assigné pour le moment.</div>}
          {quizList.map((quiz) => {
            const status = getQuizStatus(quiz);
            return (
              <Card key={quiz.id} className="flex flex-col md:flex-row items-center justify-between p-4">
                <div>
                  <div className="font-semibold text-lg">{quiz.title || `Quiz #${quiz.quiz_id}`}</div>
                  {quiz.due_date && <div className="text-sm text-gray-500">À rendre avant : {new Date(quiz.due_date).toLocaleDateString()}</div>}
                  <div className="text-sm mt-1">Statut : <span className={`font-semibold ${status === 'complété' ? 'text-green-600' : status === 'corrigé' ? 'text-green-600' : status === 'en cours' ? 'text-yellow-600' : 'text-gray-700'}`}>{status}</span></div>
                </div>
                <div className="flex gap-2 mt-2 md:mt-0">
                  {status === 'non commencé' && <Button onClick={() => handleStartQuiz(quiz)}>Commencer</Button>}
                  {status === 'en cours' && <Button onClick={() => handleStartQuiz(quiz)} variant="secondary">Continuer</Button>}
                  {status === 'complété' && <Button onClick={() => window.location.href = `/dashboard/student/quiz/${quiz.quiz_id}`} variant="secondary">Consulter</Button>}
                  {status === 'corrigé' && <Button onClick={() => handleStartQuiz(quiz)} variant="secondary">Voir correction</Button>}
                </div>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default MesQuizPage; 