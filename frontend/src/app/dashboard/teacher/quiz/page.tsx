'use client';

import React, { useState, useEffect } from "react";
import Sidebar from '../../../../components/Sidebar';
import { useClassGroups } from "@/hooks/useClassGroups";
import { useStudents } from "@/hooks/useStudents";
import { useAuth  } from '@/hooks/useAuth';
import { BookOpen, FileText, Download, Share2, Target, Users, User, Plus, Eye, CheckCircle, Clock } from 'lucide-react';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const works = [
  { value: "antigone", label: "Antigone" },
  { value: "la_boite_a_merveilles", label: "La Boîte à Merveilles" },
  { value: "dernier_jour_d_un_condamne", label: "Le Dernier Jour d'un Condamné" },
];
const difficulties = [
  { value: "facile", label: "Facile" },
  { value: "moyen", label: "Moyen" },
  { value: "difficile", label: "Difficile" },
];

interface Quiz {
  id: number;
  title: string;
  subject: string;
  level: string;
  created_at: string;
  max_score: number;
  time_limit: number;
  created_by: number;
}

interface QuizResult {
  id: number;
  quiz_id: number;
  student_id: number;
  score: number;
  max_score: number;
  percentage: number;
  is_completed: boolean;
  completed_at: string;
  student: {
    username: string;
    email: string;
  };
  quiz: {
    title: string;
    subject: string;
  };
}

export default function QuizGeneratorPage() {
  const { token, isAuthenticated, user } = useAuth();
  const [sujet, setSujet] = useState(works[0].value);
  const [niveau, setNiveau] = useState("");
  const [nombre, setNombre] = useState(5);
  const [chapitre, setChapitre] = useState("");
  const [scene, setScene] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [quiz, setQuiz] = useState<any>(null);
  const [showAssign, setShowAssign] = useState(false);
  const [assignTarget, setAssignTarget] = useState<{ type: 'class' | 'student'; id: string }>({ type: 'class', id: '' });
  const [assignLoading, setAssignLoading] = useState(false);
  const [assignError, setAssignError] = useState("");
  const [assignSuccess, setAssignSuccess] = useState("");
  const { data: classes } = useClassGroups();
  const { data: students } = useStudents();

  // États pour les quiz créés et les résultats
  const [teacherQuizzes, setTeacherQuizzes] = useState<Quiz[]>([]);
  const [quizResults, setQuizResults] = useState<QuizResult[]>([]);
  const [loadingQuizzes, setLoadingQuizzes] = useState(false);
  const [loadingResults, setLoadingResults] = useState(false);
  const [activeTab, setActiveTab] = useState<'generate' | 'my-quizzes' | 'completed'>('generate');

  // États pour les modales de détails
  const [selectedQuiz, setSelectedQuiz] = useState<Quiz | null>(null);
  const [selectedResult, setSelectedResult] = useState<QuizResult | null>(null);
  const [showQuizDetails, setShowQuizDetails] = useState(false);
  const [showResultDetails, setShowResultDetails] = useState(false);
  const [loadingDetails, setLoadingDetails] = useState(false);
  const [quizDetails, setQuizDetails] = useState<any>(null);
  const [resultDetails, setResultDetails] = useState<any>(null);

  // Fonction pour voir les détails d'un quiz
  const handleViewQuizDetails = async (quiz: Quiz) => {
    setSelectedQuiz(quiz);
    setShowQuizDetails(true);
    setLoadingDetails(true);
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/quizzes/${quiz.id}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setQuizDetails(data);
      } else {
        console.error('Erreur lors du chargement des détails du quiz');
      }
    } catch (error) {
      console.error('Erreur réseau:', error);
    } finally {
      setLoadingDetails(false);
    }
  };

  // Fonction pour voir les détails d'un résultat
  const handleViewResultDetails = async (result: QuizResult) => {
    setSelectedResult(result);
    setShowResultDetails(true);
    setLoadingDetails(true);
    
    console.log('[DEBUG] Chargement des détails du résultat:', result.id);
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/quizzes/results/${result.id}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      console.log('[DEBUG] Réponse du serveur:', response.status, response.statusText);
      
      if (response.ok) {
        const data = await response.json();
        console.log('[DEBUG] Données reçues:', data);
        setResultDetails(data);
      } else {
        const errorText = await response.text();
        console.error('[DEBUG] Erreur serveur:', response.status, errorText);
        
        // Si l'endpoint ne fonctionne pas, utiliser les données de base
        console.log('[DEBUG] Utilisation des données de base du résultat');
        setResultDetails({
          student_name: result.student?.username,
          quiz_title: result.quiz?.title,
          score: result.score,
          max_score: result.max_score,
          percentage: result.percentage,
          is_completed: result.is_completed,
          completed_at: result.completed_at,
          answers: [] // Pas de réponses détaillées disponibles
        });
      }
    } catch (error) {
      console.error('[DEBUG] Erreur réseau:', error);
      
      // En cas d'erreur, utiliser les données de base
      setResultDetails({
        student_name: result.student?.username,
        quiz_title: result.quiz?.title,
        score: result.score,
        max_score: result.max_score,
        percentage: result.percentage,
        is_completed: result.is_completed,
        completed_at: result.completed_at,
        answers: [] // Pas de réponses détaillées disponibles
      });
    } finally {
      setLoadingDetails(false);
    }
  };

  // Fonction pour partager un quiz
  const handleShareQuiz = async (quiz: Quiz) => {
    // Pour l'instant, on affiche juste une alerte
    alert(`Fonctionnalité de partage pour le quiz "${quiz.title}" - À implémenter`);
  };

  // Vérifier l'authentification au chargement
  useEffect(() => {
    if (!isAuthenticated || !token) {
      setError("Veuillez vous connecter pour accéder à cette page.");
      setTimeout(() => {
        window.location.href = '/login';
      }, 2000);
      return;
    }
    
    const verifyToken = async () => {
      try {
        console.log("Test de connectivité à l'API...");
        console.log("URL de test:", `${API_BASE_URL}/api/v1/auth/me`);
        
        const response = await fetch(`${API_BASE_URL}/api/v1/auth/me`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        
        console.log("Réponse de vérification:", response.status, response.statusText);
        
        if (!response.ok) {
          setError("Session expirée. Veuillez vous reconnecter.");
          setTimeout(() => {
            window.location.href = '/login';
          }, 2000);
          return;
        }
        
        setError("");
        console.log("Token valide, utilisateur connecté");
      } catch (error) {
        console.error("Erreur de vérification du token:", error);
        setError("Erreur de connexion. Veuillez vous reconnecter.");
        setTimeout(() => {
          window.location.href = '/login';
        }, 2000);
      }
    };
    
    verifyToken();
  }, [isAuthenticated, token]);

  // Charger les quiz créés par le professeur
  const loadTeacherQuizzes = async () => {
    if (!token) return;
    
    setLoadingQuizzes(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/quizzes/teacher/${user?.id}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setTeacherQuizzes(data);
      } else {
        console.error('Erreur lors du chargement des quiz');
      }
    } catch (error) {
      console.error('Erreur réseau:', error);
    } finally {
      setLoadingQuizzes(false);
    }
  };

  // Charger les résultats de quiz complétés
  const loadQuizResults = async () => {
    if (!token || !user?.id) return;
    
    setLoadingResults(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/quizzes/teacher/${user.id}/completed`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        console.log('[DEBUG] Quiz complétés reçus:', data);
        setQuizResults(data);
      } else {
        console.error('Erreur lors du chargement des résultats:', response.status, response.statusText);
      }
    } catch (error) {
      console.error('Erreur réseau:', error);
    } finally {
      setLoadingResults(false);
    }
  };

  // Charger les données quand l'onglet change
  useEffect(() => {
    if (activeTab === 'my-quizzes') {
      loadTeacherQuizzes();
    } else if (activeTab === 'completed') {
      loadQuizResults();
    }
  }, [activeTab, token, user?.id]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setQuiz(null);
    
    console.log("=== DÉBUT DIAGNOSTIC ===");
    console.log("API_BASE_URL:", API_BASE_URL);
    console.log("Type de API_BASE_URL:", typeof API_BASE_URL);
    console.log("Token présent:", !!token);
    console.log("Token:", token);
    
    if (!API_BASE_URL || API_BASE_URL === 'undefined') {
      console.error('[ERROR] API_BASE_URL is undefined or invalid:', API_BASE_URL);
      setError('Erreur de configuration: URL de l\'API non définie');
      setLoading(false);
      return;
    }

    const requestBody = {
      sujet,
      niveau: niveau || null,
      nombre,
      type_qcm: null,
      chapitre: chapitre || null,
      scene: scene || null
    };

    console.log('[DEBUG] Request body:', requestBody);
    console.log('[DEBUG] Full URL:', `${API_BASE_URL}/api/v1/ai/generate-qcm/`);

    try {
      // Test de connectivité
      console.log('[DEBUG] Test de connectivité...');
      const testResponse = await fetch(`${API_BASE_URL}/api/v1/ai/test/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      console.log('[DEBUG] Test response:', testResponse.status, testResponse.statusText);

      const requestOptions = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(requestBody)
      };

      console.log('[DEBUG] Making request with options:', requestOptions);
      
      const response = await fetch(`${API_BASE_URL}/api/v1/ai/generate-qcm/`, requestOptions);
      
      console.log('[DEBUG] Response status:', response.status);
      console.log('[DEBUG] Response statusText:', response.statusText);
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error('[DEBUG] Error response:', errorText);
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      console.log('[DEBUG] Success response:', data);
      
      setQuiz(data);
      setError("");
      
      // Recharger les quiz après génération
      loadTeacherQuizzes();
      
    } catch (error: any) {
      console.error('[DEBUG] Fetch error:', error);
      console.error('[DEBUG] Error name:', error.name);
      console.error('[DEBUG] Error message:', error.message);
      setError(`Erreur lors de la génération: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleAssign = async (e: React.FormEvent) => {
    e.preventDefault();
    setAssignLoading(true);
    setAssignError("");
    setAssignSuccess("");
    
    try {
      const quiz_id = quiz?.quiz_id;
      if (!quiz_id) {
        setAssignError("Quiz non généré ou quiz_id manquant");
        setAssignLoading(false);
        return;
      }
      const body: any = { quiz_id };
      if (assignTarget.type === 'class') body.class_id = Number(assignTarget.id);
      if (assignTarget.type === 'student') body.student_id = Number(assignTarget.id);
      const res = await fetch(`${API_BASE_URL}/api/v1/quizzes/assign/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(body),
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Erreur lors de l'assignation");
      }
      setAssignSuccess("Quiz assigné avec succès !");
    } catch (e: any) {
      setAssignError(e.message);
    } finally {
      setAssignLoading(false);
    }
  };

  const [selecteds, setSelecteds] = useState<(number | null)[]>(() => quiz?.qcm ? quiz.qcm.map(() => null) : []);

  useEffect(() => {
    setSelecteds(quiz?.qcm ? quiz.qcm.map(() => null) : []);
  }, [quiz?.qcm]);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar userType="teacher" />
      <div className="flex-1 overflow-auto pl-0 md:pl-56">
        <div className="p-6">
          {/* Header */}
          <div className="mb-6">
            <h1 className="text-3xl font-bold text-gray-800 mb-2">Gestion des Quiz</h1>
            <p className="text-gray-600">Créez, gérez et suivez les quiz de vos étudiants</p>
          </div>

          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-800">{error}</p>
            </div>
          )}

          {/* Onglets */}
          <div className="mb-6">
            <div className="border-b border-gray-200">
              <nav className="-mb-px flex space-x-8">
                <button
                  onClick={() => setActiveTab('generate')}
                  className={`py-2 px-1 border-b-2 font-medium text-sm ${
                    activeTab === 'generate'
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <Plus className="inline w-4 h-4 mr-2" />
                  Générer un Quiz
                </button>
                <button
                  onClick={() => setActiveTab('my-quizzes')}
                  className={`py-2 px-1 border-b-2 font-medium text-sm ${
                    activeTab === 'my-quizzes'
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <FileText className="inline w-4 h-4 mr-2" />
                  Mes Quiz ({teacherQuizzes.length})
                </button>
                <button
                  onClick={() => setActiveTab('completed')}
                  className={`py-2 px-1 border-b-2 font-medium text-sm ${
                    activeTab === 'completed'
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <CheckCircle className="inline w-4 h-4 mr-2" />
                  Quiz Complétés ({quizResults.length})
                </button>
              </nav>
            </div>
          </div>

          {/* Contenu des onglets */}
          {activeTab === 'generate' && (
            <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
              <div className="flex items-center gap-3 mb-6">
                <BookOpen className="text-blue-600" size={24} />
                <h2 className="text-xl font-bold text-gray-800">Configuration du Quiz</h2>
              </div>
              
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Œuvre</label>
                    <select 
                      value={sujet} 
                      onChange={e => setSujet(e.target.value)} 
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      {works.map(w => <option key={w.value} value={w.value}>{w.label}</option>)}
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Nombre de questions</label>
                    <input 
                      type="number" 
                      min={1} 
                      max={30} 
                      value={nombre} 
                      onChange={e => setNombre(Number(e.target.value))} 
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" 
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Difficulté</label>
                    <select 
                      value={niveau} 
                      onChange={e => setNiveau(e.target.value)} 
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="">Toutes</option>
                      {difficulties.map(d => <option key={d.value} value={d.value}>{d.label}</option>)}
                    </select>
                  </div>
                  
                  {sujet === "antigone" ? (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Scène</label>
                      <input 
                        type="text" 
                        value={scene} 
                        onChange={e => setScene(e.target.value)} 
                        placeholder="Ex: Scène 1" 
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" 
                      />
                    </div>
                  ) : (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Chapitre</label>
                      <input 
                        type="text" 
                        value={chapitre} 
                        onChange={e => setChapitre(e.target.value)} 
                        placeholder="Ex: Chapitre 1" 
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" 
                      />
                    </div>
                  )}
                </div>
                
                <div className="flex items-center gap-4">
                  <button 
                    type="submit" 
                    disabled={loading} 
                    className="flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
                  >
                    <Target size={16} />
                    {loading ? "Génération..." : "Générer le Quiz"}
                  </button>
                </div>
              </form>

              {/* Affichage du quiz généré */}
              {quiz && (
                <div className="mt-8 pt-6 border-t border-gray-200">
                  <div className="flex items-center gap-3 mb-4">
                    <FileText className="text-green-600" size={20} />
                    <h3 className="text-lg font-semibold text-gray-800">{quiz.title}</h3>
                  </div>
                  
                  <div className="bg-gray-50 rounded-lg p-4 mb-6">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                      <div>
                        <span className="font-medium text-gray-600">Questions:</span>
                        <span className="ml-2 text-gray-800">{quiz.questions?.length || 0}</span>
                      </div>
                      <div>
                        <span className="font-medium text-gray-600">Score max:</span>
                        <span className="ml-2 text-gray-800">{quiz.questions?.length || 0} points</span>
                      </div>
                      <div>
                        <span className="font-medium text-gray-600">Temps:</span>
                        <span className="ml-2 text-gray-800">15 min</span>
                      </div>
                      <div>
                        <span className="font-medium text-gray-600">ID Quiz:</span>
                        <span className="ml-2 text-gray-800">{quiz.quiz_id}</span>
                      </div>
                    </div>
                  </div>

                  {/* Questions */}
                  <div className="space-y-4">
                    {quiz.questions?.map((q: any, idx: number) => {
                      // Séparer le texte de la question des options
                      const questionText = q.question_text || '';
                      
                      let cleanQuestionText = questionText;
                      let extractedOptions: string[] = [];
                      
                      // Méthode 1: Chercher le point d'interrogation comme fin de question
                      const questionEndIndex = questionText.indexOf('?');
                      if (questionEndIndex !== -1) {
                        // Le texte de la question s'arrête au point d'interrogation
                        cleanQuestionText = questionText.substring(0, questionEndIndex + 1).trim();
                        
                        // Tout ce qui suit le point d'interrogation sont les options
                        const optionsText = questionText.substring(questionEndIndex + 1).trim();
                        
                        // Extraire les options avec regex améliorée - plus précise
                        const optionRegex = /([A-E]\)[^A-E]*?)(?=[A-E]\)|Réponse correcte|Explication|$)/g;
                        const matches = optionsText.match(optionRegex);
                        
                        if (matches && matches.length > 0) {
                          // Nettoyer les options - supprimer les doublons et préfixes incorrects
                          const cleanedOptions = matches
                            .map(match => match.trim())
                            .filter(option => {
                              // Supprimer les options qui sont des doublons (ex: "E) B) ...")
                              const cleanOption = option.replace(/^[A-E]\)\s*[A-E]\)/, (match) => {
                                // Garder seulement la première lettre et supprimer la duplication
                                return match.substring(0, 2);
                              });
                              return cleanOption.length > 2; // Garder seulement les options valides
                            })
                            .map(option => {
                              // Nettoyer les préfixes dupliqués
                              return option.replace(/^([A-E])\)\s*[A-E]\)/, '$1)');
                            });
                          
                          // Supprimer les doublons de contenu (même texte d'option)
                          const uniqueOptions: string[] = [];
                          const seenContent = new Set<string>();
                          
                          cleanedOptions.forEach(option => {
                            const content = option.replace(/^[A-E]\)\s*/, '').trim();
                            if (!seenContent.has(content) && content.length > 0) {
                              seenContent.add(content);
                              uniqueOptions.push(option);
                            }
                          });
                          
                          extractedOptions = uniqueOptions;
                        }
                      } else {
                        // Méthode 2: Fallback - chercher les options directement dans le texte
                        const hasOptionsInText = questionText.includes('A)') || questionText.includes('B)') || questionText.includes('C)') || questionText.includes('D)');
                        
                        if (hasOptionsInText) {
                          // Extraire les options du texte de la question
                          const optionRegex = /([A-E]\)[^A-E]*?)(?=[A-E]\)|Réponse correcte|Explication|$)/g;
                          const matches = questionText.match(optionRegex);
                          
                          if (matches) {
                            // Le texte de la question est tout ce qui précède la première option
                            const firstOptionIndex = questionText.indexOf(matches[0]);
                            cleanQuestionText = questionText.substring(0, firstOptionIndex).trim();
                            
                            // Nettoyer les options
                            const cleanedOptions = matches
                              .map(match => match.trim())
                              .filter(option => {
                                const cleanOption = option.replace(/^[A-E]\)\s*[A-E]\)/, (match) => {
                                  return match.substring(0, 2);
                                });
                                return cleanOption.length > 2;
                              })
                              .map(option => {
                                return option.replace(/^([A-E])\)\s*[A-E]\)/, '$1)');
                              });
                            
                            // Supprimer les doublons de contenu (même texte d'option)
                            const uniqueOptions: string[] = [];
                            const seenContent = new Set<string>();
                            
                            cleanedOptions.forEach(option => {
                              const content = option.replace(/^[A-E]\)\s*/, '').trim();
                              if (!seenContent.has(content) && content.length > 0) {
                                seenContent.add(content);
                                uniqueOptions.push(option);
                              }
                            });
                            
                            extractedOptions = uniqueOptions;
                          }
                        }
                      }
                      
                      // Utiliser les options extraites ou celles fournies par l'API
                      const optionsToDisplay = extractedOptions.length > 0 ? extractedOptions : (q.options || []);
                      
                      return (
                        <div key={idx} className="bg-white border border-gray-200 rounded-lg p-4">
                          <div className="flex items-start gap-3">
                            <span className="flex-shrink-0 w-6 h-6 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-sm font-medium">
                              {idx + 1}
                            </span>
                            <div className="flex-1">
                              <p className="text-gray-800 mb-3 font-medium">{cleanQuestionText}</p>
                              <div className="space-y-2">
                                {optionsToDisplay.map((option: string, optIdx: number) => {
                                  // Nettoyer l'option pour l'affichage
                                  const cleanOption = option.replace(/^[A-E]\)\s*/, '').trim();
                                  return (
                                    <div key={optIdx} className="flex items-center gap-2">
                                      <span className="w-4 h-4 bg-gray-100 text-gray-600 rounded flex items-center justify-center text-xs font-medium">
                                        {String.fromCharCode(65 + optIdx)}
                                      </span>
                                      <span className="text-gray-700">{cleanOption}</span>
                                    </div>
                                  );
                                })}
                              </div>
                              <div className="mt-3 pt-3 border-t border-gray-100">
                                <span className="text-sm font-medium text-green-700">
                                  Réponse correcte: {q.correct_answer}
                                </span>
                              </div>
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>

                  {/* Section d'assignation */}
                  <div className="mt-8 pt-6 border-t border-gray-200">
                    <button 
                      className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700" 
                      onClick={() => setShowAssign(v => !v)}
                    >
                      <Share2 size={16} />
                      Assigner ce quiz
                    </button>
                    
                    {showAssign && (
                      <form onSubmit={handleAssign} className="mt-6 p-6 border border-gray-200 rounded-lg bg-gray-50">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Assigner à</label>
                            <select 
                              value={assignTarget.type} 
                              onChange={e => setAssignTarget(t => ({ ...t, type: e.target.value as 'class' | 'student', id: '' }))} 
                              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                            >
                              <option value="class">Classe</option>
                              <option value="student">Élève</option>
                            </select>
                          </div>
                          
                          {assignTarget.type === 'class' ? (
                            <div>
                              <label className="block text-sm font-medium text-gray-700 mb-2">Classe</label>
                              <select 
                                value={assignTarget.id} 
                                onChange={e => setAssignTarget(t => ({ ...t, id: e.target.value }))} 
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                              >
                                <option value="">-- Sélectionner --</option>
                                {classes && classes.map(c => (
                                  <option key={c.id} value={c.id}>{c.name}</option>
                                ))}
                              </select>
                            </div>
                          ) : (
                            <div>
                              <label className="block text-sm font-medium text-gray-700 mb-2">Élève</label>
                              <select 
                                value={assignTarget.id} 
                                onChange={e => setAssignTarget(t => ({ ...t, id: e.target.value }))} 
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                              >
                                <option value="">-- Sélectionner --</option>
                                {students && students.map(s => (
                                  <option key={s.id} value={s.id}>{s.username} ({s.email})</option>
                                ))}
                              </select>
                            </div>
                          )}
                        </div>
                        
                        <div className="mt-6">
                          <button 
                            type="submit" 
                            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50" 
                            disabled={assignLoading || !assignTarget.id}
                          >
                            {assignLoading ? "Assignation..." : "Assigner"}
                          </button>
                        </div>
                        
                        {assignError && (
                          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
                            <p className="text-red-800">{assignError}</p>
                          </div>
                        )}
                        
                        {assignSuccess && (
                          <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg">
                            <p className="text-green-800">{assignSuccess}</p>
                          </div>
                        )}
                      </form>
                    )}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Onglet Mes Quiz */}
          {activeTab === 'my-quizzes' && (
            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex items-center gap-3 mb-6">
                <FileText className="text-blue-600" size={24} />
                <h2 className="text-xl font-bold text-gray-800">Mes Quiz Créés</h2>
              </div>

              {loadingQuizzes ? (
                <div className="text-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                  <p className="mt-2 text-gray-600">Chargement des quiz...</p>
                </div>
              ) : teacherQuizzes.length === 0 ? (
                <div className="text-center py-8">
                  <FileText className="mx-auto h-12 w-12 text-gray-400" />
                  <h3 className="mt-2 text-sm font-medium text-gray-900">Aucun quiz créé</h3>
                  <p className="mt-1 text-sm text-gray-500">Commencez par générer votre premier quiz.</p>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Titre</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Matière</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Niveau</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Score Max</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Créé le</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {teacherQuizzes.map((quiz) => (
                        <tr key={quiz.id}>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm font-medium text-gray-900">{quiz.title}</div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm text-gray-900">{quiz.subject}</div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800">
                              {quiz.level}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {quiz.max_score} points
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {formatDate(quiz.created_at)}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                            <button 
                              onClick={() => handleViewQuizDetails(quiz)}
                              className="text-blue-600 hover:text-blue-900 mr-3"
                              title="Voir les détails"
                            >
                              <Eye className="w-4 h-4" />
                            </button>
                            <button 
                              onClick={() => handleShareQuiz(quiz)}
                              className="text-green-600 hover:text-green-900"
                              title="Partager"
                            >
                              <Share2 className="w-4 h-4" />
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          )}

          {/* Onglet Quiz Complétés */}
          {activeTab === 'completed' && (
            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex items-center gap-3 mb-6">
                <CheckCircle className="text-green-600" size={24} />
                <h2 className="text-xl font-bold text-gray-800">Quiz Complétés par les Étudiants</h2>
              </div>

              {loadingResults ? (
                <div className="text-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                  <p className="mt-2 text-gray-600">Chargement des résultats...</p>
                </div>
              ) : quizResults.length === 0 ? (
                <div className="text-center py-8">
                  <CheckCircle className="mx-auto h-12 w-12 text-gray-400" />
                  <h3 className="mt-2 text-sm font-medium text-gray-900">Aucun quiz complété</h3>
                  <p className="mt-1 text-sm text-gray-500">Les résultats apparaîtront ici quand les étudiants auront complété des quiz.</p>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Étudiant</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Quiz</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Score</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Pourcentage</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Statut</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Complété le</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {quizResults.map((result) => (
                        <tr key={result.id}>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="flex items-center">
                              <User className="w-4 h-4 text-gray-400 mr-2" />
                              <div>
                                <div className="text-sm font-medium text-gray-900">{result.student?.username}</div>
                                <div className="text-sm text-gray-500">{result.student?.email}</div>
                              </div>
                            </div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm text-gray-900">{result.quiz?.title}</div>
                            <div className="text-sm text-gray-500">{result.quiz?.subject}</div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm text-gray-900">
                              {result.score}/{result.max_score}
                            </div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                              result.percentage >= 80 ? 'bg-green-100 text-green-800' :
                              result.percentage >= 60 ? 'bg-yellow-100 text-yellow-800' :
                              'bg-red-100 text-red-800'
                            }`}>
                              {result.percentage.toFixed(1)}%
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            {result.is_completed ? (
                              <span className="inline-flex items-center px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800">
                                <CheckCircle className="w-3 h-3 mr-1" />
                                Complété
                              </span>
                            ) : (
                              <span className="inline-flex items-center px-2 py-1 text-xs font-semibold rounded-full bg-yellow-100 text-yellow-800">
                                <Clock className="w-3 h-3 mr-1" />
                                En cours
                              </span>
                            )}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {result.completed_at ? formatDate(result.completed_at) : '-'}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                            <button 
                              onClick={() => handleViewResultDetails(result)}
                              className="text-blue-600 hover:text-blue-900"
                              title="Voir les détails"
                            >
                              <Eye className="w-4 h-4" />
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          )}

          {/* Modale pour les détails d'un quiz */}
          {showQuizDetails && (
            <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
              <div className="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
                <div className="mt-3">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-medium text-gray-900">
                      Détails du Quiz: {selectedQuiz?.title}
                    </h3>
                    <button
                      onClick={() => setShowQuizDetails(false)}
                      className="text-gray-400 hover:text-gray-600"
                    >
                      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </div>
                  
                  {loadingDetails ? (
                    <div className="text-center py-8">
                      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                      <p className="mt-2 text-gray-600">Chargement des détails...</p>
                    </div>
                  ) : quizDetails ? (
                    <div className="space-y-4">
                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700">Titre</label>
                          <p className="mt-1 text-sm text-gray-900">{quizDetails.title}</p>
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700">Matière</label>
                          <p className="mt-1 text-sm text-gray-900">{quizDetails.subject}</p>
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700">Niveau</label>
                          <p className="mt-1 text-sm text-gray-900">{quizDetails.level}</p>
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700">Score Maximum</label>
                          <p className="mt-1 text-sm text-gray-900">{quizDetails.max_score} points</p>
                        </div>
                      </div>
                      
                      {quizDetails.questions && quizDetails.questions.length > 0 && (
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">Questions</label>
                          <div className="space-y-3">
                            {quizDetails.questions.map((question: any, index: number) => (
                              <div key={index} className="border rounded-lg p-3">
                                <p className="font-medium text-sm text-gray-900 mb-2">
                                  Question {index + 1}: {question.question_text}
                                </p>
                                {question.options && (
                                  <div className="space-y-1">
                                    {question.options.map((option: string, optIndex: number) => (
                                      <div key={optIndex} className="flex items-center">
                                        <span className="text-xs text-gray-500 mr-2">
                                          {String.fromCharCode(65 + optIndex)}.
                                        </span>
                                        <span className="text-sm text-gray-700">{option}</span>
                                      </div>
                                    ))}
                                  </div>
                                )}
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  ) : (
                    <p className="text-gray-500">Aucun détail disponible</p>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Modale pour les détails d'un résultat */}
          {showResultDetails && (
            <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
              <div className="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
                <div className="mt-3">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-medium text-gray-900">
                      Détails du Résultat
                    </h3>
                    <button
                      onClick={() => setShowResultDetails(false)}
                      className="text-gray-400 hover:text-gray-600"
                    >
                      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </div>
                  
                  {loadingDetails ? (
                    <div className="text-center py-8">
                      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                      <p className="mt-2 text-gray-600">Chargement des détails...</p>
                    </div>
                  ) : resultDetails ? (
                    <div className="space-y-4">
                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700">Étudiant</label>
                          <p className="mt-1 text-sm text-gray-900">{resultDetails.student_name || selectedResult?.student?.username || 'Non spécifié'}</p>
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700">Quiz</label>
                          <p className="mt-1 text-sm text-gray-900">{resultDetails.quiz_title || selectedResult?.quiz?.title || 'Non spécifié'}</p>
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700">Score</label>
                          <p className="mt-1 text-sm text-gray-900">
                            {resultDetails.score || selectedResult?.score || 0}/{resultDetails.max_score || selectedResult?.max_score || 0} ({resultDetails.percentage || selectedResult?.percentage || 0}%)
                          </p>
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700">Statut</label>
                          <p className="mt-1 text-sm text-gray-900">
                            {resultDetails.is_completed || selectedResult?.is_completed ? 'Complété' : 'En cours'}
                          </p>
                        </div>
                      </div>
                      
                      {/* Section des réponses détaillées */}
                      <div className="mt-6">
                        <h4 className="text-lg font-medium text-gray-900 mb-4">Réponses détaillées de l'étudiant</h4>
                        
                        {resultDetails.answers && resultDetails.answers.length > 0 ? (
                          <div className="space-y-4">
                            {resultDetails.answers.map((answer: any, index: number) => (
                              <div key={index} className="border border-gray-200 rounded-lg p-4 bg-gray-50">
                                <div className="flex items-start justify-between mb-3">
                                  <h5 className="font-medium text-gray-900">
                                    Question {index + 1}
                                  </h5>
                                  <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                                    answer.is_correct ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                                  }`}>
                                    {answer.is_correct ? 'Correct' : 'Incorrect'}
                                  </span>
                                </div>
                                
                                <div className="space-y-3">
                                  {/* Question */}
                                  <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Question:</label>
                                    <p className="text-sm text-gray-900 bg-white p-2 rounded border">
                                      {answer.question_text || `Question ${index + 1}`}
                                    </p>
                                  </div>
                                  
                                  {/* Réponse de l'étudiant */}
                                  <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Réponse de l'étudiant:</label>
                                    <div className={`p-2 rounded border ${
                                      answer.is_correct ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'
                                    }`}>
                                      <span className={`text-sm font-medium ${
                                        answer.is_correct ? 'text-green-800' : 'text-red-800'
                                      }`}>
                                        {answer.student_answer || 'Aucune réponse'}
                                      </span>
                                    </div>
                                  </div>
                                  
                                  {/* Réponse correcte (si incorrect) */}
                                  {!answer.is_correct && answer.correct_answer && (
                                    <div>
                                      <label className="block text-sm font-medium text-gray-700 mb-1">Réponse correcte:</label>
                                      <div className="p-2 rounded border bg-green-50 border-green-200">
                                        <span className="text-sm font-medium text-green-800">
                                          {answer.correct_answer}
                                        </span>
                                      </div>
                                    </div>
                                  )}
                                  
                                  {/* Points gagnés */}
                                  <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Points:</label>
                                    <span className="text-sm text-gray-900">
                                      {answer.points_earned || 0} point(s)
                                    </span>
                                  </div>
                                </div>
                              </div>
                            ))}
                          </div>
                        ) : (
                          <div className="text-center py-8">
                            <div className="text-gray-400 mb-2">
                              <svg className="mx-auto h-12 w-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                              </svg>
                            </div>
                            <h3 className="text-sm font-medium text-gray-900">Aucune réponse détaillée disponible</h3>
                            <p className="mt-1 text-sm text-gray-500">
                              Les réponses détaillées ne sont pas encore disponibles pour ce résultat.
                            </p>
                          </div>
                        )}
                      </div>
                      
                      {/* Informations supplémentaires */}
                      <div className="mt-6 pt-4 border-t border-gray-200">
                        <h4 className="text-sm font-medium text-gray-700 mb-2">Informations supplémentaires</h4>
                        <div className="grid grid-cols-2 gap-4 text-sm">
                          <div>
                            <span className="text-gray-500">Complété le:</span>
                            <span className="ml-2 text-gray-900">
                              {resultDetails.completed_at || selectedResult?.completed_at ? 
                                formatDate(resultDetails.completed_at || selectedResult?.completed_at) : 
                                'Non spécifié'
                              }
                            </span>
                          </div>
                          <div>
                            <span className="text-gray-500">Temps passé:</span>
                            <span className="ml-2 text-gray-900">
                              {resultDetails.time_spent || 'Non spécifié'}
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                  ) : (
                    <div className="text-center py-8">
                      <div className="text-gray-400 mb-2">
                        <svg className="mx-auto h-12 w-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                      </div>
                      <h3 className="text-sm font-medium text-gray-900">Aucun détail disponible</h3>
                      <p className="mt-1 text-sm text-gray-500">
                        Les détails de ce résultat ne sont pas encore disponibles.
                      </p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
} 