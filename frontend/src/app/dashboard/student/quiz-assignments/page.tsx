'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/hooks/useAuthSimple';
import { useRouter } from 'next/navigation';
import { getUnifiedQuizAssignments, getUnifiedCompletedQuizzes, UnifiedQuizAssignment } from '@/services/unifiedQuizService';
import Sidebar from '../../../../components/Sidebar';
import SimpleIcon, { SimpleIconWithBackground } from '../../../../components/ui/SimpleIcon';
import { 
  BookOpen, 
  Clock, 
  CheckCircle, 
  AlertTriangle,
  Search,
  Play,
  Eye,
  Calendar,
  Target,
  TrendingUp
} from 'lucide-react';

interface QuizAssignment {
  id: string; // Maintenant une string unique
  original_id: number; // L'ID original de la base de données
  quiz_id: number;
  quiz_title: string;
  description: string;
  subject: string;
  due_date: string;
  status: string;
  assigned_by: string;
  estimated_duration: number;
  student_status: string;
  score?: number;
  completed_at?: string;
  assigned_at: string;
  quiz_type?: 'normal' | 'adaptive';
}

const StudentQuizAssignmentsPage = () => {
  const { user, token } = useAuth();
  const router = useRouter();
  const [assignments, setAssignments] = useState<QuizAssignment[]>([]);
  const [completedQuizzes, setCompletedQuizzes] = useState<QuizAssignment[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [selectedSubject, setSelectedSubject] = useState('all');

  useEffect(() => {
    if (user && token) {
      console.log('🔥 [DEBUG] Utilisateur chargé, récupération des assignations...');
      fetchAssignments();
    }
  }, [user, token]);

  const fetchAssignments = async () => {
    try {
      if (!user || !token) {
        console.error('Utilisateur non connecté');
        return;
      }
      
      console.log('🔥 [DEBUG] Récupération des assignations unifiées pour l\'étudiant:', user.id);
      
      // Récupérer les assignations ET les quiz terminés
      const [allAssignments, completedQuizzesData] = await Promise.all([
        getUnifiedQuizAssignments(token, user.id),
        getUnifiedCompletedQuizzes(token, user.id)
      ]);
      
      console.log('🔥 [DEBUG] Total des assignations unifiées:', allAssignments.length);
      console.log('🔥 [DEBUG] Total des quiz terminés:', completedQuizzesData.length);
      
      // Vérifier qu'il n'y a pas de doublons
      const ids = allAssignments.map(a => a.id);
      const uniqueIds = new Set(ids);
      if (ids.length !== uniqueIds.size) {
        console.error('❌ [ERROR] Doublons détectés dans les IDs:', ids);
      } else {
        console.log('✅ [SUCCESS] Toutes les clés sont uniques');
      }
      
      setAssignments(allAssignments);
      setCompletedQuizzes(completedQuizzesData);
      
    } catch (error) {
      console.error('Erreur lors du chargement des données:', error);
    } finally {
      setLoading(false);
    }
  };

  const startQuiz = (assignment: QuizAssignment) => {
    console.log('🔥 [DEBUG] Démarrage du quiz:', assignment);
    console.log('🔥 [DEBUG] Quiz ID:', assignment.quiz_id);
    console.log('🔥 [DEBUG] Quiz Type:', assignment.quiz_type);
    console.log('🔥 [DEBUG] Redirection vers:', `/dashboard/student/quiz/${assignment.quiz_id}`);
    
    // Si c'est un test adaptatif et que l'ID n'existe pas, utiliser l'ID 47
    let quizId = assignment.quiz_id;
    if (assignment.quiz_type === 'adaptive' && !quizId) {
      quizId = 47; // ID du test adaptatif de test
      console.log('🔄 [DEBUG] Utilisation de l\'ID de test adaptatif:', quizId);
    }
    
    // Rediriger vers la page du quiz unifié en utilisant quiz_id
    router.push(`/dashboard/student/quiz/${quizId}`);
  };

  const viewQuizDetails = (assignment: QuizAssignment) => {
    console.log('🔥 [DEBUG] Affichage des détails du quiz:', assignment);
    
    // Créer une modal avec les détails complets
    const details = `
📋 DÉTAILS DU QUIZ

🏷️ Titre: ${assignment.quiz_title}
📝 Description: ${assignment.description}
📚 Matière: ${assignment.subject}
⏱️ Durée estimée: ${assignment.estimated_duration} minutes
🎯 Type: ${assignment.quiz_type === 'adaptive' ? 'Test Adaptatif' : 'Quiz Standard'}
📅 Assigné le: ${new Date(assignment.assigned_at).toLocaleDateString()}
${assignment.due_date ? `⏰ Échéance: ${new Date(assignment.due_date).toLocaleDateString()}` : ''}
🆔 ID du quiz: ${assignment.quiz_id}
🆔 ID de l'assignation: ${assignment.original_id}
    `;
    
    alert(details);
  };

  const viewQuizResults = (assignment: QuizAssignment) => {
    console.log('🔥 [DEBUG] Affichage des résultats du quiz:', assignment);
    
    // Trouver le quiz terminé correspondant
    const completedQuiz = completedQuizzes.find(q => q.quiz_id === assignment.quiz_id);
    
    if (completedQuiz) {
      const results = `
🏆 RÉSULTATS DU QUIZ

📋 Quiz: ${assignment.quiz_title}
📚 Matière: ${assignment.subject}
🎯 Type: ${assignment.quiz_type === 'adaptive' ? 'Test Adaptatif' : 'Quiz Standard'}
⏱️ Durée: ${assignment.estimated_duration} minutes

📊 PERFORMANCE:
${assignment.score !== undefined ? `Score: ${assignment.score}/100` : 'Score: Non disponible'}
${assignment.completed_at ? `✅ Terminé le: ${new Date(assignment.completed_at).toLocaleDateString()}` : ''}

💡 CONSEILS:
${assignment.score !== undefined && assignment.score >= 80 ? '🌟 Excellent travail ! Continuez ainsi !' : 
  assignment.score !== undefined && assignment.score >= 60 ? '👍 Bon travail ! Quelques révisions pourraient aider.' : 
  '📚 Continuez à pratiquer ! La persévérance mène au succès.'}
      `;
      
      alert(results);
    } else {
      alert('❌ Aucun résultat trouvé pour ce quiz. Il se peut qu\'il ne soit pas encore terminé.');
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'assigné':
        return <span className="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs font-medium rounded-full">À faire</span>;
      case 'en cours':
        return <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs font-medium rounded-full">En cours</span>;
      case 'fait':
        return <span className="px-2 py-1 bg-green-100 text-green-800 text-xs font-medium rounded-full">Terminé</span>;
      default:
        return <span className="px-2 py-1 bg-gray-100 text-gray-800 text-xs font-medium rounded-full">{status}</span>;
    }
  };

  const getPriorityBadge = (assignment: QuizAssignment) => {
    if (!assignment.due_date) return null;
    
    const dueDate = new Date(assignment.due_date);
    const now = new Date();
    const daysUntilDue = Math.ceil((dueDate.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
    
    if (daysUntilDue < 0) {
      return <span className="px-2 py-1 bg-red-100 text-red-800 text-xs font-medium rounded-full">En retard</span>;
    } else if (daysUntilDue <= 2) {
      return <span className="px-2 py-1 bg-orange-100 text-orange-800 text-xs font-medium rounded-full">Urgent</span>;
    } else if (daysUntilDue <= 7) {
      return <span className="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs font-medium rounded-full">Proche</span>;
    }
    
    return null;
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBadge = (score: number) => {
    if (score >= 80) return <span className="px-2 py-1 bg-green-100 text-green-800 text-xs font-medium rounded-full">Excellent</span>;
    if (score >= 60) return <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs font-medium rounded-full">Bon</span>;
    return <span className="px-2 py-1 bg-red-100 text-red-800 text-xs font-medium rounded-full">À améliorer</span>;
  };

  // Filtrer les assignations selon le statut sélectionné
  const getFilteredAssignments = () => {
    if (filterStatus === 'all') {
      return [...assignments, ...(completedQuizzes || [])];
    } else if (filterStatus === 'fait') {
      return completedQuizzes || [];
    } else {
      return assignments.filter(a => a.student_status === filterStatus);
    }
  };

  const filteredAssignments = getFilteredAssignments().filter(assignment => {
    const matchesSearch = assignment.quiz_title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         assignment.subject.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesSubject = selectedSubject === 'all' || assignment.subject === selectedSubject;
    return matchesSearch && matchesSubject;
  });

  const pendingAssignments = assignments.filter(a => a.student_status === 'assigné');
  const inProgressAssignments = assignments.filter(a => a.student_status === 'en cours');
  const overdueAssignments = assignments.filter(a => {
    if (!a.due_date) return false;
    // Exclure les quiz qui sont dans completedQuizzes
    if (completedQuizzes && completedQuizzes.some(q => q.quiz_id === a.quiz_id)) return false;
    return new Date(a.due_date) < new Date();
  });

  const subjects = Array.from(new Set(assignments.map(a => a.subject)));

  if (!user || !token) {
    return (
      <div className="flex min-h-screen bg-bg-secondary">
        <Sidebar />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-danger text-lg font-bold">Erreur : utilisateur non connecté ou id manquant.</div>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex min-h-screen bg-bg-secondary">
        <Sidebar />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-primary animate-pulse text-xl font-bold">Chargement des quiz assignés...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-bg-secondary">
      <Sidebar />
      <div className="flex-1 overflow-auto pl-0 md:pl-56">
        <div className="p-6">
          {/* Header personnalisé avec thème harmonisé */}
          <div className="mb-8 flex items-center justify-between flex-wrap gap-4 animate-slide-in-up">
            <div className="animate-slide-in-left">
              <h1 className="text-3xl font-bold text-primary mb-2">
                Mes Quiz Assignés <span className="animate-wave inline-block">📚</span>
              </h1>
              <p className="text-secondary">Gérez et suivez vos quiz assignés par vos professeurs</p>
            </div>
            <div className="flex items-center gap-4 animate-slide-in-right">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-100 to-purple-100 rounded-lg flex items-center justify-center">
                <SimpleIcon name="book" className="h-6 w-6 text-blue-600" />
              </div>
            </div>
          </div>

          {/* Widget de statistiques unifiées avec thème harmonisé */}
          <div className="mb-8 animate-scale-in">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="card-unified animate-fade-in-scale animate-delay-200">
                <div className="card-unified-body">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                      <BookOpen className="h-5 w-5 text-blue-600" />
                    </div>
                    <div>
                      <p className="text-sm text-muted">Total Assignés</p>
                      <p className="text-2xl font-bold text-primary">{assignments.length}</p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="card-unified animate-fade-in-scale animate-delay-300">
                <div className="card-unified-body">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-yellow-100 rounded-lg flex items-center justify-center">
                      <Clock className="h-5 w-5 text-yellow-600" />
                    </div>
                    <div>
                      <p className="text-sm text-muted">À Faire</p>
                      <p className="text-2xl font-bold text-primary">{pendingAssignments.length}</p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="card-unified animate-fade-in-scale animate-delay-400">
                <div className="card-unified-body">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                      <Target className="h-5 w-5 text-purple-600" />
                    </div>
                    <div>
                      <p className="text-sm text-muted">En Cours</p>
                      <p className="text-2xl font-bold text-primary">{inProgressAssignments.length}</p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="card-unified animate-fade-in-scale animate-delay-500">
                <div className="card-unified-body">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                      <CheckCircle className="h-5 w-5 text-green-600" />
                    </div>
                    <div>
                      <p className="text-sm text-muted">Terminés</p>
                      <p className="text-2xl font-bold text-primary">{completedQuizzes.length}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Filtres et recherche avec thème harmonisé */}
          <div className="card-unified mb-8 animate-fade-in-scale animate-delay-600">
            <div className="card-unified-body">
              <div className="flex flex-col md:flex-row gap-4">
                <div className="flex-1">
                  <label htmlFor="search" className="block text-sm font-medium text-primary mb-2">Rechercher</label>
                  <div className="relative">
                    <Search className="absolute left-3 top-3 h-4 w-4 text-muted" />
                    <input
                      id="search"
                      placeholder="Rechercher par titre ou matière..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                    />
                  </div>
                </div>

                <div>
                  <label htmlFor="status" className="block text-sm font-medium text-primary mb-2">Statut</label>
                  <select 
                    value={filterStatus} 
                    onChange={(e) => setFilterStatus(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  >
                    <option value="all">Tous</option>
                    <option value="assigné">À faire</option>
                    <option value="en cours">En cours</option>
                    <option value="fait">Terminé</option>
                  </select>
                </div>

                <div>
                  <label htmlFor="subject" className="block text-sm font-medium text-primary mb-2">Matière</label>
                  <select 
                    value={selectedSubject} 
                    onChange={(e) => setSelectedSubject(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  >
                    <option value="all">Toutes matières</option>
                    {subjects.map((subject) => (
                      <option key={subject} value={subject}>{subject}</option>
                    ))}
                  </select>
                </div>
              </div>
            </div>
          </div>

          {/* Alertes pour quiz en retard avec thème harmonisé */}
          {overdueAssignments.length > 0 && (
            <div className="card-unified mb-8 border-red-200 bg-red-50 animate-fade-in-scale animate-delay-700">
              <div className="card-unified-header">
                <h3 className="text-lg font-bold text-red-800 mb-0 flex items-center gap-2">
                  <AlertTriangle className="h-5 w-5" />
                  Quiz en Retard ({overdueAssignments.length})
                </h3>
              </div>
              <div className="card-unified-body">
                <div className="space-y-3">
                  {overdueAssignments.map((assignment) => (
                    <div key={assignment.id} className="flex items-center justify-between p-3 bg-white rounded-lg border border-red-200">
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-1">
                          <span className="font-medium text-red-800">{assignment.quiz_title}</span>
                          <span className="px-2 py-1 bg-red-100 text-red-800 text-xs font-medium rounded-full">En retard</span>
                        </div>
                        <p className="text-sm text-red-700">
                          {assignment.subject} • Échéance: {new Date(assignment.due_date).toLocaleDateString()}
                        </p>
                      </div>
                      <button 
                        className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors text-sm font-medium"
                        onClick={() => startQuiz(assignment)}
                      >
                        Commencer maintenant
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Onglets principaux avec thème harmonisé */}
          <div className="mb-8 animate-fade-in-scale animate-delay-800">
            <div className="flex space-x-1 bg-gray-100 p-1 rounded-lg">
              <button
                onClick={() => setFilterStatus('all')}
                className={`flex-1 flex items-center justify-center gap-2 px-4 py-2 rounded-md transition-all duration-200 ${
                  filterStatus === 'all'
                    ? 'bg-white text-primary shadow-sm'
                    : 'text-muted hover:text-primary'
                }`}
              >
                <BookOpen className="h-4 w-4" />
                Tous ({assignments.length})
              </button>
              <button
                onClick={() => setFilterStatus('assigné')}
                className={`flex-1 flex items-center justify-center gap-2 px-4 py-2 rounded-md transition-all duration-200 ${
                  filterStatus === 'assigné'
                    ? 'bg-white text-primary shadow-sm'
                    : 'text-muted hover:text-primary'
                }`}
              >
                <Clock className="h-4 w-4" />
                À Faire ({pendingAssignments.length})
              </button>
              <button
                onClick={() => setFilterStatus('en cours')}
                className={`flex-1 flex items-center justify-center gap-2 px-4 py-2 rounded-md transition-all duration-200 ${
                  filterStatus === 'en cours'
                    ? 'bg-white text-primary shadow-sm'
                    : 'text-muted hover:text-primary'
                }`}
              >
                <Target className="h-4 w-4" />
                En Cours ({inProgressAssignments.length})
              </button>
              <button
                onClick={() => setFilterStatus('fait')}
                className={`flex-1 flex items-center justify-center gap-2 px-4 py-2 rounded-md transition-all duration-200 ${
                  filterStatus === 'fait'
                    ? 'bg-white text-primary shadow-sm'
                    : 'text-muted hover:text-primary'
                }`}
              >
                <CheckCircle className="h-4 w-4" />
                Terminés ({completedQuizzes.length})
              </button>
            </div>
          </div>

          {/* Liste des assignations avec thème harmonisé */}
          <div className="animate-fade-in-scale animate-delay-900">
            <AssignmentsList 
              assignments={filteredAssignments} 
              getStatusBadge={getStatusBadge}
              getPriorityBadge={getPriorityBadge}
              getScoreColor={getScoreColor}
              getScoreBadge={getScoreBadge}
              startQuiz={startQuiz}
              viewQuizDetails={viewQuizDetails}
              viewQuizResults={viewQuizResults}
              completedQuizzes={completedQuizzes}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

// Composant pour afficher la liste des assignations
const AssignmentsList = ({ 
  assignments, 
  getStatusBadge, 
  getPriorityBadge, 
  getScoreColor, 
  getScoreBadge, 
  startQuiz, 
  viewQuizDetails,
  viewQuizResults,
  completedQuizzes
}: { 
  assignments: QuizAssignment[];
  getStatusBadge: (status: string) => React.ReactNode;
  getPriorityBadge: (assignment: QuizAssignment) => React.ReactNode;
  getScoreColor: (score: number) => string;
  getScoreBadge: (score: number) => React.ReactNode;
  startQuiz: (assignment: QuizAssignment) => void;
  viewQuizDetails: (assignment: QuizAssignment) => void;
  viewQuizResults: (assignment: QuizAssignment) => void;
  completedQuizzes?: QuizAssignment[];
}) => {
  if (assignments.length === 0) {
    return (
      <div className="card-unified">
        <div className="card-unified-body">
          <div className="text-center py-8">
            <BookOpen className="h-12 w-12 text-muted mx-auto mb-4" />
            <p className="text-secondary">Aucun quiz assigné trouvé</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {assignments.map((assignment) => (
        <div key={assignment.id} className="card-unified hover:shadow-md transition-shadow animate-fade-in-scale">
          <div className="card-unified-body">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center space-x-3 mb-3">
                  <h3 className="font-semibold text-xl text-primary">{assignment.quiz_title}</h3>
                  {getStatusBadge(assignment.student_status)}
                  {getPriorityBadge(assignment)}
                  <span className={`px-2 py-1 rounded text-xs ${
                    assignment.quiz_type === 'adaptive' 
                      ? 'bg-purple-100 text-purple-800' 
                      : 'bg-blue-100 text-blue-800'
                  }`}>
                    {assignment.quiz_type === 'adaptive' ? 'Test Adaptatif' : 'Quiz Standard'}
                  </span>
                </div>
                
                <p className="text-secondary mb-4">{assignment.description}</p>
                
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-muted mb-4">
                  <div className="flex items-center space-x-2">
                    <BookOpen className="h-4 w-4" />
                    <span><span className="font-medium">Matière:</span> {assignment.subject}</span>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    <Calendar className="h-4 w-4" />
                    <span><span className="font-medium">Assigné le:</span> {new Date(assignment.assigned_at).toLocaleDateString()}</span>
                  </div>
                  
                  {assignment.due_date && (
                    <div className="flex items-center space-x-2">
                      <Clock className="h-4 w-4" />
                      <span><span className="font-medium">Échéance:</span> {new Date(assignment.due_date).toLocaleDateString()}</span>
                    </div>
                  )}
                  
                  <div className="flex items-center space-x-2">
                    <Target className="h-4 w-4" />
                    <span><span className="font-medium">Durée:</span> {assignment.estimated_duration} min</span>
                  </div>
                </div>

                {/* Afficher le score si disponible OU si c'est un quiz terminé */}
                {(assignment.score !== undefined || (completedQuizzes && completedQuizzes.some(q => q.quiz_id === assignment.quiz_id))) && (
                  <div className="flex items-center space-x-2 mb-3">
                    <TrendingUp className="h-4 w-4" />
                    <span className="font-medium">Score obtenu:</span>
                    {assignment.score !== undefined ? (
                      <>
                        <span className={`font-semibold ${getScoreColor(assignment.score)}`}>
                          {assignment.score}/100
                        </span>
                        {getScoreBadge(assignment.score)}
                      </>
                    ) : (
                      <span className="font-semibold text-green-600">
                        Quiz terminé ✓
                      </span>
                    )}
                  </div>
                )}

                {/* Afficher la date de completion si disponible OU si c'est un quiz terminé */}
                {(assignment.completed_at || (completedQuizzes && completedQuizzes.some(q => q.quiz_id === assignment.quiz_id))) && (
                  <div className="text-sm text-gray-500">
                    {assignment.completed_at ? (
                      <>Terminé le: {new Date(assignment.completed_at).toLocaleDateString()}</>
                    ) : (
                      <>✅ Quiz terminé</>
                    )}
                  </div>
                )}
              </div>

              <div className="flex flex-col space-y-2 ml-4">
                {/* Vérifier si c'est un quiz terminé (dans completedQuizzes) */}
                {completedQuizzes && completedQuizzes.some(q => q.quiz_id === assignment.quiz_id) ? (
                  <button 
                    onClick={() => viewQuizResults(assignment)}
                    className="btn-unified btn-unified-success flex items-center space-x-2"
                  >
                    <TrendingUp className="h-4 w-4" />
                    Voir résultats
                  </button>
                ) : assignment.student_status !== 'fait' ? (
                  <button 
                    onClick={() => startQuiz(assignment)}
                    className={`btn-unified btn-unified-primary flex items-center space-x-2 ${
                      assignment.student_status === 'en cours' 
                        ? 'bg-blue-600 hover:bg-blue-700' 
                        : 'bg-purple-600 hover:bg-purple-700'
                    }`}
                  >
                    <Play className="h-4 w-4" />
                    {assignment.student_status === 'en cours' ? 'Continuer' : 'Commencer'}
                  </button>
                ) : (
                  <button 
                    onClick={() => viewQuizResults(assignment)}
                    className="btn-unified btn-unified-success flex items-center space-x-2"
                  >
                    <TrendingUp className="h-4 w-4" />
                    Voir résultats
                  </button>
                )}
                
                {/* Bouton Voir détails - toujours visible */}
                <button 
                  onClick={() => viewQuizDetails(assignment)}
                  className="btn-unified btn-unified-secondary flex items-center space-x-2"
                >
                  <Eye className="h-4 w-4" />
                  Détails
                </button>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default StudentQuizAssignmentsPage;
