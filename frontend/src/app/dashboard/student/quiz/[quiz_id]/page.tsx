'use client';

import React, { useEffect, useState, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuthSimple';
import { CheckCircle } from 'lucide-react';
import { 
  getUnifiedQuiz, 
  getUnifiedQuizQuestions, 
  submitUnifiedQuiz,
  UnifiedQuiz,
  UnifiedQuestion,
  UnifiedQuizResult
} from '@/services/unifiedQuizService';

export default function StudentQuizPage({ params }: { params: Promise<{ quiz_id: string }> }) {
  const { quiz_id: quizId } = React.use(params);
  const { user, token } = useAuth();
  const [quiz, setQuiz] = useState<UnifiedQuiz | null>(null);
  const [questions, setQuestions] = useState<UnifiedQuestion[]>([]);
  const [answers, setAnswers] = useState<Record<number, any>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [submitted, setSubmitted] = useState(false);
  const [result, setResult] = useState<UnifiedQuizResult | null>(null);
  const [currentIdx, setCurrentIdx] = useState(0);
  const router = useRouter();
  const formRef = useRef<HTMLFormElement>(null);

  // Charger le quiz et vérifier s'il est déjà complété
  useEffect(() => {
    // Attendre que l'utilisateur soit complètement chargé
    if (!user || !token) {
      console.log('🔥 [DEBUG] User ou token manquant:', { user: !!user, token: !!token });
      setLoading(true);
      return;
    }

    setLoading(true);
    setError(null); // Effacer les erreurs précédentes
    console.log('🔥 [DEBUG] Chargement du quiz unifié:', quizId);
    console.log('🔥 [DEBUG] User ID:', user.id);

    const loadQuizData = async () => {
      try {
        console.log('🔥 [DEBUG] Début du chargement des données du quiz');
        console.log('🔥 [DEBUG] User ID:', user.id);
        console.log('🔥 [DEBUG] Token présent:', !!token);
        
        // Si c'est un test adaptatif et que l'ID n'existe pas, utiliser l'ID 47
        let actualQuizId = quizId;
        if (quizId === '45' || quizId === '46') {
          actualQuizId = '47'; // ID du test adaptatif de test
          console.log('🔄 [DEBUG] Utilisation de l\'ID de test adaptatif:', actualQuizId);
        }
        
        // Charger le quiz unifié
        const quizData = await getUnifiedQuiz(token, actualQuizId);
        setQuiz(quizData);
        console.log('🔥 [DEBUG] Quiz unifié chargé:', quizData);

        // Pour les tests adaptatifs, les questions sont déjà dans le quiz
        if (quizData.quiz_type === 'adaptive') {
          console.log('🔥 [DEBUG] Test adaptatif - récupération des questions depuis le quiz');
          // Les questions sont déjà dans le quiz pour les tests adaptatifs
          const questionsData = await getUnifiedQuizQuestions(token, actualQuizId, quizData.quiz_type);
          setQuestions(questionsData);
          console.log('🔥 [DEBUG] Questions chargées:', questionsData.length);
        } else {
          // Pour les quiz normaux, charger les questions séparément
          const questionsData = await getUnifiedQuizQuestions(token, actualQuizId, quizData.quiz_type);
          setQuestions(questionsData);
          console.log('🔥 [DEBUG] Questions chargées:', questionsData.length);
        }

        // Vérifier s'il y a déjà un résultat
        if (quizData.quiz_type === 'normal') {
          // Pour les quiz normaux, vérifier les résultats existants
          const resultsResponse = await fetch(`http://localhost:8000/api/v1/quiz_results/user/${user.id}`, {
            headers: { 'Authorization': `Bearer ${token}` }
          });
          
          if (resultsResponse.ok) {
            const resultsData = await resultsResponse.json();
            const existing = resultsData.find((r: any) => 
              r.quiz_id == actualQuizId && (r.completed || r.is_completed)
            );
            
            if (existing) {
              setResult(existing);
              setSubmitted(true);
              console.log('🔥 [DEBUG] Quiz déjà complété');
            }
          }
        } else {
          // Pour les tests adaptatifs, vérifier les tentatives existantes
          const resultsResponse = await fetch(`http://localhost:8000/api/v1/adaptive-evaluation/student/${user.id}/results`, {
            headers: { 'Authorization': `Bearer ${token}` }
          });
          
          if (resultsResponse.ok) {
            const resultsData = await resultsResponse.json();
            console.log('🔥 [DEBUG] Données de résultats reçues:', resultsData);
            
            // Vérifier que resultsData a la bonne structure
            if (resultsData && resultsData.results && Array.isArray(resultsData.results)) {
              const existing = resultsData.results.find((r: any) => 
                r.test_id == actualQuizId && r.status === 'completed'
              );
              
              if (existing) {
                setResult(existing);
                setSubmitted(true);
                console.log('🔥 [DEBUG] Test adaptatif déjà complété');
              }
            } else {
              console.log('⚠️ [DEBUG] Structure de résultats inattendue:', resultsData);
            }
          }
        }

        setLoading(false);
      } catch (error) {
        console.error('❌ Erreur lors du chargement:', error);
        setError('Erreur lors du chargement du quiz');
        setLoading(false);
      }
    };

    loadQuizData();
  }, [quizId, user, token]);

  const handleChange = (questionId: number, value: any) => {
    setAnswers(prev => ({ ...prev, [questionId]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    console.log('🔥 [DEBUG] handleSubmit called');
    console.log('🔥 [DEBUG] submitted:', submitted);
    console.log('🔥 [DEBUG] result:', result);
    
    if (!user || !token || !quiz) {
      setError('Données manquantes pour la soumission');
      return;
    }
    
    // Vérifier si le quiz est déjà complété
    if (submitted || result) {
      console.log('🔥 [DEBUG] Quiz already completed, blocking submission');
      setError('Ce quiz a déjà été complété. Vous ne pouvez pas le soumettre à nouveau.');
      return;
    }
    
    // Vérifier que toutes les questions ont une réponse
    const answeredCount = Object.keys(answers).length;
    const totalCount = questions.length;
    
    console.log('🔥 [DEBUG] Validation des réponses:', { answeredCount, totalCount, answers });
    
    if (answeredCount < totalCount) {
      setError(`Veuillez répondre à toutes les questions. ${totalCount - answeredCount} question(s) sans réponse.`);
      return;
    }
    
    console.log('🔥 [DEBUG] Proceeding with submission');
    setError(null);
    
    try {
      // Préparer les réponses au format unifié
      const formattedAnswers = Object.entries(answers).map(([question_id, answerIdx]) => {
        const question = questions.find((q: any) => q.id === Number(question_id));
        const opts = question?.options || [];
        return {
          question_id: Number(question_id),
          answer: opts[answerIdx] ?? answerIdx
        };
      });
      
      console.log('🔥 [DEBUG] Réponses formatées:', formattedAnswers);
      
      // Si c'est un test adaptatif et que l'ID n'existe pas, utiliser l'ID 47
      let actualQuizId = quizId;
      if (quizId === '45' || quizId === '46') {
        actualQuizId = '47'; // ID du test adaptatif de test
        console.log('🔄 [DEBUG] Utilisation de l\'ID de test adaptatif pour soumission:', actualQuizId);
      }
      
      // Soumettre le quiz unifié
      const result = await submitUnifiedQuiz(token, actualQuizId, quiz.quiz_type, formattedAnswers);
      setResult(result);
      setSubmitted(true);
      
      console.log('🔥 [DEBUG] Quiz soumis avec succès:', result);
      
      // 🔄 RAFRAÎCHIR LES DONNÉES DEPUIS LA BASE
      console.log('🔄 [DEBUG] Rafraîchissement des données depuis la base...');
      try {
        if (quiz.quiz_type === 'adaptive') {
          // Pour les tests adaptatifs, récupérer les vraies données
          const resultsResponse = await fetch(`http://localhost:8000/api/v1/adaptive-evaluation/student/${user.id}/results`, {
            headers: { 'Authorization': `Bearer ${token}` }
          });
          
          if (resultsResponse.ok) {
            const resultsData = await resultsResponse.json();
            console.log('🔄 [DEBUG] Données fraîches reçues:', resultsData);
            
            // Vérifier que resultsData a la bonne structure
            if (resultsData && resultsData.results && Array.isArray(resultsData.results)) {
              const freshResult = resultsData.results.find((r: any) => 
                r.test_id == actualQuizId && r.status === 'completed'
              );
              
              if (freshResult) {
                console.log('🔄 [DEBUG] Données fraîches récupérées:', freshResult);
                
                // Récupérer les détails complets de la tentative
                const attemptResponse = await fetch(`http://localhost:8000/api/v1/adaptive-evaluation/attempts/${freshResult.id}`, {
                  headers: { 'Authorization': `Bearer ${token}` }
                });
                
                if (attemptResponse.ok) {
                  const attemptData = await attemptResponse.json();
                  console.log('🔄 [DEBUG] Détails de la tentative récupérés:', attemptData);
                  
                  // Créer un objet résultat avec la structure attendue
                  const normalizedResult = {
                    id: freshResult.id,
                    quiz_id: freshResult.test_id,
                    quiz_type: 'adaptive',
                    student_id: freshResult.student_id,
                    score: attemptData.total_score || 0,
                    max_score: attemptData.max_score || 10,
                    percentage: attemptData.percentage || 0,
                    is_completed: true,
                    completed_at: freshResult.completed_at || freshResult.started_at,
                    time_spent: 0,
                    answers: []
                  };
                  
                  console.log('🔄 [DEBUG] Résultat normalisé:', normalizedResult);
                  setResult(normalizedResult);
                } else {
                  console.log('⚠️ [DEBUG] Impossible de récupérer les détails de la tentative');
                  setResult(freshResult);
                }
              }
            } else {
              console.log('⚠️ [DEBUG] Structure de données fraîches inattendue:', resultsData);
            }
          }
        }
      } catch (error) {
        console.error('❌ [DEBUG] Erreur lors du rafraîchissement:', error);
      }
      
      // Ne pas rediriger immédiatement, laisser l'utilisateur voir ses résultats
      
    } catch (error) {
      console.error('❌ Erreur lors de la soumission:', error);
      setError('Erreur lors de la soumission du quiz');
    }
  };

  // Navigation
  const handleNext = () => setCurrentIdx(idx => Math.min(idx + 1, questions.length - 1));
  const handlePrev = () => setCurrentIdx(idx => Math.max(idx - 1, 0));

  // Progression
  const progress = questions.length > 0 ? ((currentIdx + 1) / questions.length) * 100 : 0;

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-purple-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">
            {!user || !token ? 'Chargement de l\'utilisateur...' : 'Chargement du quiz...'}
          </p>
          {!user || !token ? (
            <p className="mt-2 text-sm text-gray-500">Veuillez patienter pendant la connexion...</p>
          ) : null}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-xl mx-auto p-6 bg-white rounded shadow mt-8">
        <button className="mb-4 text-blue-600 hover:underline" onClick={() => router.back()}>
          &larr; Retour
        </button>
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <h2 className="text-red-800 font-semibold mb-2">Erreur</h2>
          <p className="text-red-700">{error}</p>
          <div className="mt-4 text-sm text-red-600">
            <p>• Vérifiez que vous êtes bien connecté</p>
            <p>• Rafraîchissez la page si nécessaire</p>
            <p>• Contactez l'administrateur si le problème persiste</p>
          </div>
        </div>
      </div>
    );
  }

  if (!quiz) {
    return (
      <div className="max-w-xl mx-auto p-6 bg-white rounded shadow mt-8">
        <button className="mb-4 text-blue-600 hover:underline" onClick={() => router.back()}>
          &larr; Retour
        </button>
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <h2 className="text-yellow-800 font-semibold mb-2">Quiz non trouvé</h2>
          <p className="text-yellow-700">Le quiz demandé n'existe pas ou vous n'avez pas les permissions pour y accéder.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded shadow mt-8">
      <button className="mb-4 text-blue-600 hover:underline" onClick={() => router.back()}>
        &larr; Retour
      </button>

      {/* Affichage si le quiz est déjà complété */}
      {submitted && result && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-blue-600 font-semibold">✓ Quiz déjà complété</span>
          </div>
          <p className="text-blue-700 mb-2">
            Ce quiz a déjà été soumis avec un score de {result.score || 0}/{result.max_score || 10} ({result.percentage !== undefined ? result.percentage : Math.round(((result.score || 0) / (result.max_score || 10)) * 100)}%).
          </p>
          <div className="text-sm text-blue-600">
            <p>• Vous ne pouvez pas refaire ce quiz</p>
            <p>• Consultez vos résultats dans la page des quiz assignés</p>
          </div>
        </div>
      )}

      {/* Titre et informations du quiz */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">
          {quiz.title}
        </h1>
        <div className="flex flex-wrap gap-4 text-sm text-gray-600">
          <span>📚 {quiz.subject}</span>
          <span>⏱️ {quiz.estimated_duration} min</span>
          <span>❓ {quiz.total_questions} questions</span>
          <span className={`px-2 py-1 rounded text-xs ${
            quiz.quiz_type === 'adaptive' 
              ? 'bg-purple-100 text-purple-800' 
              : 'bg-blue-100 text-blue-800'
          }`}>
            {quiz.quiz_type === 'adaptive' ? 'Test Adaptatif' : 'Quiz Standard'}
          </span>
        </div>
        {quiz.description && (
          <p className="text-gray-700 mt-2">{quiz.description}</p>
        )}
      </div>

      {/* Progression */}
      {!submitted && questions.length > 0 && (
        <div className="mb-6">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm text-gray-600">
              Question {currentIdx + 1} sur {questions.length}
            </span>
            <span className="text-sm text-gray-600">{Math.round(progress)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-purple-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
          
          {/* Barre de progression des réponses */}
          <div className="mt-4">
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm text-gray-600">Réponses données</span>
              <span className="text-sm text-gray-600">
                {Object.keys(answers).length} / {questions.length}
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-green-500 h-2 rounded-full transition-all duration-300"
                style={{ width: `${(Object.keys(answers).length / questions.length) * 100}%` }}
              ></div>
            </div>
          </div>
        </div>
      )}

      {/* Formulaire du quiz */}
      {questions.length > 0 && !submitted && !result && (
        <form onSubmit={handleSubmit} ref={formRef}>
          {/* Navigation des questions */}
          <div className="flex justify-between items-center mb-6">
            <button
              type="button"
              onClick={handlePrev}
              disabled={currentIdx === 0}
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-300"
            >
              ← Précédente
            </button>
            
            {/* Indicateur de progression avec miniatures des questions */}
            <div className="flex items-center space-x-2">
              {questions.map((_, index) => (
                <button
                  key={index}
                  type="button"
                  onClick={() => setCurrentIdx(index)}
                  className={`w-8 h-8 rounded-full text-xs font-medium transition-all duration-200 ${
                    index === currentIdx
                      ? 'bg-purple-600 text-white'
                      : answers[questions[index].id] !== undefined
                      ? 'bg-green-500 text-white'
                      : 'bg-gray-200 text-gray-600 hover:bg-gray-300'
                  }`}
                  title={`Question ${index + 1}${answers[questions[index].id] !== undefined ? ' - Répondu' : ''}`}
                >
                  {index + 1}
                </button>
              ))}
            </div>
            
            <button
              type="button"
              onClick={handleNext}
              disabled={currentIdx === questions.length - 1}
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-300"
            >
              Suivante →
            </button>
          </div>

          {/* Question actuelle */}
          <div className="mb-6">
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
              <h3 className="text-lg font-semibold text-gray-800 mb-2">
                Question {currentIdx + 1} sur {questions.length}
              </h3>
              <p className="text-gray-700 leading-relaxed">
                {questions[currentIdx].question_text}
              </p>
            </div>
            
            {/* Options de réponse */}
            <div className="space-y-3">
              {questions[currentIdx].options.map((option, index) => (
                <label 
                  key={index} 
                  className={`flex items-center space-x-3 cursor-pointer p-3 rounded-lg border-2 transition-all duration-200 ${
                    answers[questions[currentIdx].id] === index
                      ? 'border-purple-500 bg-purple-50'
                      : 'border-gray-200 hover:border-purple-300 hover:bg-purple-25'
                  }`}
                >
                  <input
                    type="radio"
                    name={`question_${questions[currentIdx].id}`}
                    value={index}
                    checked={answers[questions[currentIdx].id] === index}
                    onChange={() => handleChange(questions[currentIdx].id, index)}
                    className="text-purple-600 focus:ring-purple-500"
                  />
                  <span className="text-gray-700 font-medium">{option}</span>
                </label>
              ))}
            </div>
            
            {/* Indicateur de réponse */}
            {answers[questions[currentIdx].id] !== undefined && (
              <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg">
                <div className="flex items-center space-x-2 text-green-700">
                  <CheckCircle className="h-5 w-5" />
                  <span className="font-medium">Réponse sélectionnée</span>
                </div>
              </div>
            )}
          </div>

          {/* Boutons de soumission */}
          <div className="flex justify-between items-center pt-6 border-t">
            <button
              type="button"
              onClick={() => router.back()}
              className="px-6 py-2 text-gray-600 border border-gray-300 rounded hover:bg-gray-50"
            >
              Annuler
            </button>
            
            <div className="flex space-x-3">
              {/* Bouton de prévisualisation */}
              <button
                type="button"
                onClick={() => {
                  const answeredCount = Object.keys(answers).length;
                  const totalCount = questions.length;
                  alert(`Résumé des réponses :\n\n✅ Répondues : ${answeredCount}/${totalCount}\n❌ Manquantes : ${totalCount - answeredCount}\n\nVoulez-vous continuer ou compléter les réponses manquantes ?`);
                }}
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
              >
                📋 Prévisualiser
              </button>
              
              {/* Bouton de soumission */}
              <button
                type="submit"
                disabled={Object.keys(answers).length < questions.length}
                className="px-6 py-2 bg-purple-600 text-white rounded hover:bg-purple-700 focus:ring-2 focus:ring-purple-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                🚀 Soumettre le quiz
              </button>
            </div>
          </div>
        </form>
      )}

      {/* Affichage des résultats */}
      {submitted && result && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-6">
          <h2 className="text-2xl font-bold text-green-800 mb-4">🎉 Quiz terminé !</h2>
          
          {/* Debug des valeurs */}
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3 mb-4 text-xs">
            <strong>Debug:</strong> score={result.score}, max_score={result.max_score}, percentage={result.percentage}
          </div>
          
          {/* Statistiques du score */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="text-center">
              <div className="text-3xl font-bold text-green-600">{result.score || 0}</div>
              <div className="text-sm text-green-700">Score obtenu</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-600">{result.max_score || 10}</div>
              <div className="text-sm text-blue-700">Score maximum</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-purple-600">
                {result.percentage !== undefined ? result.percentage : Math.round(((result.score || 0) / (result.max_score || 10)) * 100)}%
              </div>
              <div className="text-sm text-purple-700">Pourcentage</div>
            </div>
          </div>
          
          {/* Évaluation du score */}
          <div className="text-center mb-6">
            {result.percentage >= 80 && (
              <div className="text-green-700 font-semibold">🌟 Excellent travail !</div>
            )}
            {result.percentage >= 60 && result.percentage < 80 && (
              <div className="text-blue-700 font-semibold">👍 Bon travail !</div>
            )}
            {result.percentage >= 40 && result.percentage < 60 && (
              <div className="text-yellow-700 font-semibold">⚠️ Moyen, continuez à vous entraîner</div>
            )}
            {result.percentage < 40 && (
              <div className="text-red-700 font-semibold">💪 Courage, la prochaine fois sera meilleure !</div>
            )}
          </div>
          
          {/* Informations supplémentaires */}
          <div className="bg-white rounded-lg p-4 mb-6">
            <h3 className="font-semibold text-gray-800 mb-2">Informations du quiz :</h3>
            <div className="grid grid-cols-2 gap-4 text-sm text-gray-600">
              <div>
                <span className="font-medium">Type :</span> {quiz.quiz_type === 'adaptive' ? 'Test Adaptatif' : 'Quiz Standard'}
              </div>
              <div>
                <span className="font-medium">Matière :</span> {quiz.subject}
              </div>
              <div>
                <span className="font-medium">Questions :</span> {quiz.total_questions}
              </div>
              <div>
                <span className="font-medium">Terminé le :</span> {new Date().toLocaleDateString()}
              </div>
            </div>
          </div>
          
          {/* Boutons d'action */}
          <div className="flex justify-center space-x-4">
            <button
              onClick={() => router.push('/dashboard/student/quiz-assignments')}
              className="px-6 py-2 bg-purple-600 text-white rounded hover:bg-purple-700 transition-colors"
            >
              ← Retour aux quiz assignés
            </button>
            
            <button
              onClick={() => window.location.reload()}
              className="px-6 py-2 bg-gray-600 text-white rounded hover:bg-gray-700 transition-colors"
            >
              🔄 Recommencer le quiz
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
