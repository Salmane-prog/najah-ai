'use client';

import React, { useState, useEffect } from 'react';
import Sidebar from '../../../../components/Sidebar';
import { useAuth  } from '../../../../hooks/useAuth';
import { assignmentsAPI, TeacherTargetsResponse, TeacherTarget } from '../../../../api/teacher/assignments';
import { getTeacherDashboardData } from '../../../../services/teacherDashboardService';
import { getTeacherClassesWithFallback } from '../../../../services/teacherClassesService';
import { getTeacherQuizzesWithFallback } from '../../../../services/quizService';
import { getUserMessagesWithFallback } from '../../../../services/messagingService';
import { 
  Plus, 
  BookOpen, 
  Calendar, 
  Clock, 
  AlertTriangle, 
  CheckCircle, 
  XCircle,
  Edit,
  Trash2,
  Filter,
  Search,
  Target,
  Users,
  BarChart3,
  User,
  UserCheck,
  FileText,
  Upload,
  Download,
  Eye,
  MoreHorizontal,
  RefreshCw,
  Info
} from 'lucide-react';

interface Homework {
  id: number;
  title: string;
  description: string;
  subject: string;
  class_id: number;
  assigned_by: number;
  assigned_to: number; // ID de l'étudiant
  due_date: string;
  status: string;
  priority: string;
  estimated_time?: number;
  created_at: string;
  attachment?: {
    name: string;
    size: number;
    url: string;
    type: string;
    filename?: string; // Nom du fichier sur le serveur
  } | null;
}

interface LearningGoal {
  id: number;
  title: string;
  description: string;
  subject: string;
  target_date: string;
  progress: number;
  status: string;
  created_at: string;
  student_id?: number;
  student_name?: string;
}

export default function TeacherAssignmentsPage() {
  const { user, token } = useAuth();
  const [activeTab, setActiveTab] = useState<'homework' | 'goals'>('homework');
  const [homeworks, setHomeworks] = useState<Homework[]>([]);
  const [learningGoals, setLearningGoals] = useState<LearningGoal[]>([]);
  const [teacherTargets, setTeacherTargets] = useState<TeacherTargetsResponse>({
    classes: [],
    students: [],
    total_students: 0
  });
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showGoalModal, setShowGoalModal] = useState(false);
  const [showViewModal, setShowViewModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [selectedHomework, setSelectedHomework] = useState<Homework | null>(null);
  const [selectedClass, setSelectedClass] = useState<number | null>(null);
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [assignmentType, setAssignmentType] = useState<'class' | 'student'>('class');
  const [selectedStudents, setSelectedStudents] = useState<number[]>([]);
  
  // New enhanced states
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState<'due_date' | 'priority' | 'created_at' | 'title'>('due_date');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [selectedAssignments, setSelectedAssignments] = useState<number[]>([]);

  // États pour les formulaires
  const [homeworkForm, setHomeworkForm] = useState({
    title: '',
    description: '',
    subject: '',
    class_id: 0,
    student_ids: [] as number[],
    due_date: '',
    priority: 'medium',
    estimated_time: '',
    attachment: null as File | null
  });

  const [goalForm, setGoalForm] = useState({
    title: '',
    description: '',
    subject: '',
    class_id: 0,
    student_ids: [] as number[],
    target_date: ''
  });

  useEffect(() => {
    if (token) {
      fetchData();
    }
  }, [token]);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      console.log('🔄 Chargement des données...');
      console.log('Token:', token ? 'Présent' : 'Absent');
      
      // Récupérer les données réelles du dashboard
      console.log('📊 Récupération des données du dashboard...');
      try {
        const dashboardData = await getTeacherDashboardData(token || '');
        console.log('Dashboard data récupéré:', dashboardData);
        
        // Utiliser les données réelles pour les statistiques
        if (dashboardData.overview) {
          console.log('Overview récupéré:', dashboardData.overview);
        }
        
        if (dashboardData.class_metrics) {
          console.log('Métriques des classes récupérées:', dashboardData.class_metrics);
        }
      } catch (dashboardError) {
        console.log('⚠️ Erreur dashboard, utilisation des données de fallback:', dashboardError);
      }
      
      // Récupérer les cibles disponibles pour l'enseignant (classes et étudiants)
      console.log('📚 Récupération des cibles...');
      const targetsData = await assignmentsAPI.getTeacherTargets();
      console.log('Cibles récupérées:', targetsData);
      setTeacherTargets(targetsData);

      // Récupérer les devoirs existants
      console.log('📝 Récupération des devoirs...');
      const assignmentsData = await assignmentsAPI.getTeacherAssignments();
      console.log('Devoirs récupérés:', assignmentsData);
      console.log('Détail du premier devoir:', assignmentsData[0]);
      console.log('Champ attachment du premier devoir:', assignmentsData[0]?.attachment);
      
      // Convertir les assignations en format Homework
      const existingHomeworks: Homework[] = assignmentsData.map(assignment => ({
        id: assignment.id,
        title: assignment.title,
        description: assignment.description,
        subject: assignment.subject,
        class_id: assignment.assignment_type === 'class' ? assignment.target_ids[0] || 0 : 0,
        assigned_by: assignment.created_by,
        assigned_to: assignment.assignment_type === 'student' ? assignment.target_ids[0] || 0 : 0,
        due_date: assignment.due_date || new Date().toISOString(),
        status: assignment.status || 'pending',
        priority: assignment.priority,
        estimated_time: assignment.estimated_time,
        created_at: assignment.created_at,
        attachment: assignment.attachment
      }));
      
      setHomeworks(existingHomeworks);
      
      console.log('🎯 Récupération des objectifs...');
      setLearningGoals([]);

    } catch (error) {
      console.error('Erreur lors du chargement des données:', error);
      setError('Erreur lors du chargement des données. Veuillez réessayer.');
    } finally {
      setLoading(false);
    }
  };

  // Enhanced utility functions
  const formatDate = (dateString: string, includeTime: boolean = false) => {
    try {
      const date = new Date(dateString);
      if (isNaN(date.getTime())) return 'Date invalide';
      
      if (includeTime) {
        return date.toLocaleString('fr-FR', {
          day: '2-digit',
          month: '2-digit',
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        });
      }
      
      return date.toLocaleDateString('fr-FR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      });
    } catch {
      return 'Date invalide';
    }
  };

  const getTimeUntilDue = (dueDate: string) => {
    try {
      const due = new Date(dueDate);
      const now = new Date();
      const diff = due.getTime() - now.getTime();
      
      if (diff < 0) return 'En retard';
      
      const days = Math.floor(diff / (1000 * 60 * 60 * 24));
      const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      
      if (days > 0) return `${days} jour(s) restant(s)`;
      if (hours > 0) return `${hours} heure(s) restante(s)`;
      return 'Moins d\'une heure';
    } catch {
      return 'Date invalide';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return <CheckCircle className="w-4 h-4 text-green-600" />;
      case 'in_progress': return <BarChart3 className="w-4 h-4 text-blue-600" />;
      case 'pending': return <Clock className="w-4 h-4 text-yellow-600" />;
      case 'overdue': return <AlertTriangle className="w-4 h-4 text-red-600" />;
      default: return <Info className="w-4 h-4 text-gray-600" />;
    }
  };

  const getPriorityIcon = (priority: string) => {
    switch (priority) {
      case 'high': return <AlertTriangle className="w-4 h-4 text-red-600" />;
      case 'medium': return <Clock className="w-4 h-4 text-yellow-600" />;
      case 'low': return <CheckCircle className="w-4 h-4 text-green-600" />;
      default: return <Info className="w-4 h-4 text-gray-600" />;
    }
  };

  const showSuccessMessage = (message: string) => {
    setSuccessMessage(message);
    setTimeout(() => setSuccessMessage(null), 5000);
  };

  const showErrorMessage = (message: string) => {
    setError(message);
    setTimeout(() => setError(null), 5000);
  };

  const handleRefresh = async () => {
    setIsRefreshing(true);
    await fetchData();
    setIsRefreshing(false);
  };

  const handleCreateHomework = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      // Vérifier que le token est présent
      if (!token) {
        showErrorMessage('Erreur d\'authentification. Veuillez vous reconnecter.');
        return;
      }
      
      console.log('🔑 Token présent:', token ? 'Oui' : 'Non');
      console.log('👤 Utilisateur connecté:', user);
      
      // Préparer les données de base
      const requestData = {
        title: homeworkForm.title,
        description: homeworkForm.description,
        subject: homeworkForm.subject,
        assignment_type: assignmentType,
        target_ids: assignmentType === 'class' ? [homeworkForm.class_id] : selectedStudents,
        due_date: homeworkForm.due_date ? new Date(homeworkForm.due_date).toISOString() : undefined,
        priority: homeworkForm.priority as 'low' | 'medium' | 'high',
        estimated_time: homeworkForm.estimated_time ? parseInt(homeworkForm.estimated_time) : undefined
      };

      console.log('📝 Données à envoyer:', requestData);
      
      // Créer d'abord le devoir
      const result = await assignmentsAPI.createAssignment(requestData);

      if (result) {
        // Si un fichier est attaché, l'uploader
        if (homeworkForm.attachment) {
          try {
            const formData = new FormData();
            formData.append('file', homeworkForm.attachment);
            
            const uploadResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/assignments/upload-file?assignment_id=${result.id}`, {
              method: 'POST',
              headers: {
                'Authorization': `Bearer ${token}`
              },
              body: formData
            });
            
            if (uploadResponse.ok) {
              const uploadResult = await uploadResponse.json();
              console.log('✅ Fichier uploadé avec succès:', uploadResult);
              
              // Mettre à jour le champ attachment avec les données du fichier uploadé
              const serverFilename = uploadResult.file_metadata.url.split('/').pop();
              result.attachment = {
                name: uploadResult.file_metadata.name,
                size: uploadResult.file_metadata.size,
                type: uploadResult.file_metadata.type,
                url: uploadResult.file_metadata.url,
                filename: serverFilename
              };
            } else {
              console.error('❌ Erreur lors de l\'upload du fichier:', uploadResponse.status);
              showErrorMessage('Devoir créé mais erreur lors de l\'upload du fichier');
            }
          } catch (uploadError) {
            console.error('❌ Erreur lors de l\'upload du fichier:', uploadError);
            showErrorMessage('Devoir créé mais erreur lors de l\'upload du fichier');
          }
        }
        
        // Créer un objet Homework à partir du résultat
        const newHomework: Homework = {
          id: result.id,
          title: result.title,
          description: result.description,
          subject: result.subject,
          class_id: assignmentType === 'class' ? homeworkForm.class_id : 0,
          assigned_by: result.created_by,
          assigned_to: assignmentType === 'class' ? 0 : (selectedStudents[0] || 0),
          due_date: result.due_date || homeworkForm.due_date,
          status: 'pending',
          priority: result.priority,
          estimated_time: result.estimated_time,
          created_at: result.created_at,
          attachment: result.attachment
        };

        // Ajouter le nouveau devoir à la liste
        setHomeworks(prev => [newHomework, ...prev]);

        showSuccessMessage('Devoir créé avec succès !');
        setShowCreateModal(false);
        setHomeworkForm({
          title: '',
          description: '',
          subject: '',
          class_id: 0,
          student_ids: [],
          due_date: '',
          priority: 'medium',
          estimated_time: '',
          attachment: null
        });
        setSelectedStudents([]);
        setAssignmentType('class');
      } else {
        showErrorMessage('Erreur lors de la création du devoir');
      }
    } catch (error) {
      console.error('Erreur lors de la création du devoir:', error);
      showErrorMessage('Erreur lors de la création du devoir');
    }
  };

  const handleCreateGoal = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      const requestData: any = {
        title: goalForm.title,
        description: goalForm.description,
        subject: goalForm.subject,
        target_date: new Date(goalForm.target_date).toISOString(),
      };

      if (assignmentType === 'class') {
        requestData.class_id = goalForm.class_id;
      } else {
        requestData.student_ids = selectedStudents;
      }

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/teacher-assignments/learning-goals`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
      });

      if (response.ok) {
        showSuccessMessage('Objectif créé avec succès !');
        setShowGoalModal(false);
        setGoalForm({
          title: '',
          description: '',
          subject: '',
          class_id: 0,
          student_ids: [],
          target_date: ''
        });
        setSelectedStudents([]);
        setAssignmentType('class');
        fetchData();
      } else {
        const error = await response.json();
        showErrorMessage(`Erreur: ${error.detail}`);
      }
    } catch (error) {
      console.error('Erreur lors de la création de l\'objectif:', error);
      showErrorMessage('Erreur lors de la création de l\'objectif');
    }
  };

  const handleStudentToggle = (studentId: number) => {
    setSelectedStudents(prev => 
      prev.includes(studentId) 
        ? prev.filter(id => id !== studentId)
        : [...prev, studentId]
    );
  };

  // Fonctions pour la gestion des devoirs
  const handleViewHomework = (homework: Homework) => {
    setSelectedHomework(homework);
    setShowViewModal(true);
  };

  const handleEditHomework = (homework: Homework) => {
    setSelectedHomework(homework);
    setHomeworkForm({
      title: homework.title,
      description: homework.description,
      subject: homework.subject,
      class_id: homework.class_id,
      student_ids: homework.assigned_to > 0 ? [homework.assigned_to] : [],
      due_date: homework.due_date,
      priority: homework.priority,
      estimated_time: homework.estimated_time?.toString() || '',
      attachment: null
    });
    setAssignmentType(homework.class_id > 0 ? 'class' : 'student');
    setSelectedStudents(homework.assigned_to > 0 ? [homework.assigned_to] : []);
    setShowEditModal(true);
  };

  const handleUpdateHomework = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!selectedHomework) return;
    
    try {
      const requestData = {
        title: homeworkForm.title,
        description: homeworkForm.description,
        subject: homeworkForm.subject,
        assignment_type: assignmentType,
        target_ids: assignmentType === 'class' ? [homeworkForm.class_id] : selectedStudents,
        due_date: homeworkForm.due_date ? new Date(homeworkForm.due_date).toISOString() : undefined,
        priority: homeworkForm.priority as 'low' | 'medium' | 'high',
        estimated_time: homeworkForm.estimated_time ? parseInt(homeworkForm.estimated_time) : undefined
      };

      const result = await assignmentsAPI.updateAssignment(selectedHomework.id, requestData);

      if (result) {
        // Mettre à jour le devoir dans la liste
        setHomeworks(prev => prev.map(hw => 
          hw.id === selectedHomework.id 
            ? {
                ...hw,
                title: result.title,
                description: result.description,
                subject: result.subject,
                class_id: assignmentType === 'class' ? homeworkForm.class_id : 0,
                assigned_to: assignmentType === 'student' ? (selectedStudents[0] || 0) : 0,
                due_date: result.due_date || homeworkForm.due_date,
                priority: result.priority,
                estimated_time: result.estimated_time
              }
            : hw
        ));

        showSuccessMessage('Devoir modifié avec succès !');
        setShowEditModal(false);
        setSelectedHomework(null);
        setHomeworkForm({
          title: '',
          description: '',
          subject: '',
          class_id: 0,
          student_ids: [],
          due_date: '',
          priority: 'medium',
          estimated_time: '',
          attachment: null
        });
        setSelectedStudents([]);
        setAssignmentType('class');
      } else {
        showErrorMessage('Erreur lors de la modification du devoir');
      }
    } catch (error) {
      console.error('Erreur lors de la modification du devoir:', error);
      showErrorMessage('Erreur lors de la modification du devoir');
    }
  };

  const handleDeleteHomework = async (homeworkId: number) => {
    if (!confirm('Êtes-vous sûr de vouloir supprimer ce devoir ?')) return;
    
    try {
      const success = await assignmentsAPI.deleteAssignment(homeworkId);
      
      if (success) {
        // Supprimer le devoir de la liste
        setHomeworks(prev => prev.filter(hw => hw.id !== homeworkId));
        showSuccessMessage('Devoir supprimé avec succès !');
      } else {
        showErrorMessage('Erreur lors de la suppression du devoir');
      }
    } catch (error) {
      console.error('Erreur lors de la suppression du devoir:', error);
      showErrorMessage('Erreur lors de la suppression du devoir');
    }
  };

  const getStudentName = (studentId: number) => {
    if (studentId === 0) {
      return "Classe entière";
    }
    const student = teacherTargets.students.find(s => s.id === studentId);
    return student ? student.name : `Étudiant ${studentId}`;
  };

  const getAssignmentTarget = (homework: Homework) => {
    if (homework.class_id > 0) {
      const classGroup = teacherTargets.classes.find(c => c.id === homework.class_id);
      return classGroup ? `${classGroup.name} (${classGroup.student_count} étudiants)` : `Classe ${homework.class_id}`;
    } else if (homework.assigned_to > 0) {
      return getStudentName(homework.assigned_to);
    }
    return "Cible non définie";
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'text-red-600 bg-red-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      case 'low': return 'text-green-600 bg-green-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'text-green-600 bg-green-100';
      case 'in_progress': return 'text-blue-600 bg-blue-100';
      case 'pending': return 'text-yellow-600 bg-yellow-100';
      case 'overdue': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const filteredHomeworks = homeworks.filter(homework => {
    if (selectedClass && homework.class_id !== selectedClass) return false;
    if (filterStatus !== 'all' && homework.status !== filterStatus) return false;
    
    // Enhanced search functionality
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      const matchesTitle = homework.title.toLowerCase().includes(query);
      const matchesDescription = homework.description.toLowerCase().includes(query);
      const matchesSubject = homework.subject.toLowerCase().includes(query);
      const matchesTarget = getAssignmentTarget(homework).toLowerCase().includes(query);
      
      if (!matchesTitle && !matchesDescription && !matchesSubject && !matchesTarget) {
        return false;
      }
    }
    
    return true;
  });

  // Enhanced sorting
  const sortedHomeworks = [...filteredHomeworks].sort((a, b) => {
    let aValue: string | number, bValue: string | number;
    
    switch (sortBy) {
      case 'due_date':
        aValue = new Date(a.due_date).getTime();
        bValue = new Date(b.due_date).getTime();
        break;
      case 'priority':
        const priorityOrder = { high: 3, medium: 2, low: 1 };
        aValue = priorityOrder[a.priority as keyof typeof priorityOrder] || 0;
        bValue = priorityOrder[b.priority as keyof typeof priorityOrder] || 0;
        break;
      case 'created_at':
        aValue = new Date(a.created_at).getTime();
        bValue = new Date(b.created_at).getTime();
        break;
      case 'title':
        aValue = a.title.toLowerCase();
        bValue = b.title.toLowerCase();
        break;
      default:
        return 0;
    }
    
    if (sortOrder === 'asc') {
      return aValue > bValue ? 1 : -1;
    } else {
      return aValue < bValue ? 1 : -1;
    }
  });

  // Log pour déboguer
  console.log('📊 État des données:');
  console.log('  - Classes:', teacherTargets.classes.length);
  console.log('  - Étudiants:', teacherTargets.students.length);
  console.log('  - Total étudiants:', teacherTargets.total_students);
  console.log('  - Devoirs:', homeworks.length);
  console.log('  - Objectifs:', learningGoals.length);
  console.log('  - Devoirs filtrés:', filteredHomeworks.length);

  if (loading) {
    return (
      <div className="flex min-h-screen bg-gray-50">
        <Sidebar />
        <div className="flex-1 ml-56 p-8 pb-32">
          <div className="flex items-center justify-center h-64">
            <div className="text-blue-600 animate-pulse">Chargement...</div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 ml-56 p-8 pb-32">
        {/* Custom CSS for text truncation */}
        <style jsx>{`
          .line-clamp-2 {
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
          }
        `}</style>
        
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Assignations</h1>
          <p className="text-gray-600 mt-2">Gérez les devoirs et objectifs d'apprentissage</p>
        </div>

        {/* Tabs */}
        <div className="mb-6">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              <button
                onClick={() => setActiveTab('homework')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'homework'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <BookOpen className="inline w-4 h-4 mr-2" />
                Devoirs
              </button>
              <button
                onClick={() => setActiveTab('goals')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'goals'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <Target className="inline w-4 h-4 mr-2" />
                Objectifs d'Apprentissage
              </button>
            </nav>
          </div>
        </div>

        {/* Filtres */}
        <div className="mb-6 flex flex-wrap gap-4 items-center">
          {/* Enhanced Search Bar */}
          <div className="flex-1 min-w-64">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="text"
                placeholder="Rechercher dans les devoirs..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>

          {/* Enhanced Sorting */}
          <div className="flex items-center space-x-2">
            <label className="text-sm font-medium text-gray-700">Trier par:</label>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as 'due_date' | 'priority' | 'created_at' | 'title')}
              className="border border-gray-300 rounded-md px-3 py-2 text-sm"
            >
              <option value="due_date">Date limite</option>
              <option value="priority">Priorité</option>
              <option value="created_at">Date de création</option>
              <option value="title">Titre</option>
            </select>
            <button
              onClick={() => setSortOrder(prev => prev === 'asc' ? 'desc' : 'asc')}
              className="p-2 border border-gray-300 rounded-md hover:bg-gray-50"
              title={sortOrder === 'asc' ? 'Ordre décroissant' : 'Ordre croissant'}
            >
              {sortOrder === 'asc' ? '↑' : '↓'}
            </button>
          </div>

          {/* Refresh Button */}
          <button
            onClick={handleRefresh}
            disabled={isRefreshing}
            className="p-2 border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50"
            title="Actualiser"
          >
            <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} />
          </button>

          <div className="flex items-center space-x-2">
            <Filter className="w-4 h-4 text-gray-500" />
            <select
              value={selectedClass || ''}
              onChange={(e) => setSelectedClass(e.target.value ? parseInt(e.target.value) : null)}
              className="border border-gray-300 rounded-md px-3 py-2 text-sm"
            >
              <option value="">Toutes les classes</option>
              {teacherTargets.classes.map((classGroup) => (
                <option key={classGroup.id} value={classGroup.id}>
                  {classGroup.name} ({classGroup.student_count} étudiants)
                </option>
              ))}
            </select>
          </div>

          {activeTab === 'homework' && (
            <div className="flex items-center space-x-2">
              <select
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
                className="border border-gray-300 rounded-md px-3 py-2 text-sm"
              >
                <option value="all">Tous les statuts</option>
                <option value="pending">En attente</option>
                <option value="in_progress">En cours</option>
                <option value="completed">Terminé</option>
                <option value="overdue">En retard</option>
              </select>
            </div>
          )}

          <button
            onClick={() => activeTab === 'homework' ? setShowCreateModal(true) : setShowGoalModal(true)}
            className="ml-auto bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 flex items-center"
          >
            <Plus className="w-4 h-4 mr-2" />
            Nouveau {activeTab === 'homework' ? 'Devoir' : 'Objectif'}
          </button>
        </div>

        {/* Enhanced Status Messages */}
        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-md">
            <div className="flex items-center">
              <AlertTriangle className="w-5 h-5 text-red-400 mr-2" />
              <span className="text-red-800">{error}</span>
            </div>
          </div>
        )}

        {successMessage && (
          <div className="mb-4 p-4 bg-green-50 border border-green-200 rounded-md">
            <div className="flex items-center">
              <CheckCircle className="w-5 h-5 text-green-400 mr-2" />
              <span className="text-green-800">{successMessage}</span>
            </div>
          </div>
        )}

        {/* Summary Statistics */}
        {activeTab === 'homework' && (
          <div className="mb-6 grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
              <div className="flex items-center">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <BookOpen className="w-6 h-6 text-blue-600" />
                </div>
                <div className="ml-3">
                  <p className="text-sm font-medium text-gray-600">Total Devoirs</p>
                  <p className="text-2xl font-bold text-gray-900">{homeworks.length}</p>
                </div>
              </div>
            </div>
            
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
              <div className="flex items-center">
                <div className="p-2 bg-yellow-100 rounded-lg">
                  <Clock className="w-6 h-6 text-yellow-600" />
                </div>
                <div className="ml-3">
                  <p className="text-sm font-medium text-gray-600">En Attente</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {homeworks.filter(h => h.status === 'pending').length}
                  </p>
                </div>
              </div>
            </div>
            
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
              <div className="flex items-center">
                <div className="p-2 bg-red-100 rounded-lg">
                  <AlertTriangle className="w-6 h-6 text-red-600" />
                </div>
                <div className="ml-3">
                  <p className="text-sm font-medium text-gray-600">En Retard</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {homeworks.filter(h => h.status === 'overdue').length}
                  </p>
                </div>
              </div>
            </div>
            
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
              <div className="flex items-center">
                <div className="p-2 bg-green-100 rounded-lg">
                  <CheckCircle className="w-6 h-6 text-green-600" />
                </div>
                <div className="ml-3">
                  <p className="text-sm font-medium text-gray-600">Terminés</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {homeworks.filter(h => h.status === 'completed').length}
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Contenu */}
        {activeTab === 'homework' ? (
          <div className="grid gap-6">
            {sortedHomeworks.length === 0 ? (
              <div className="text-center py-12">
                <BookOpen className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">Aucun devoir trouvé</h3>
                <p className="text-gray-500">
                  {searchQuery || selectedClass || filterStatus !== 'all' 
                    ? 'Aucun devoir ne correspond à vos critères de recherche.'
                    : 'Commencez par créer votre premier devoir !'
                  }
                </p>
              </div>
            ) : (
              sortedHomeworks.map((homework) => (
                <div key={homework.id} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      {/* Header with enhanced status and priority */}
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex-1">
                          <h3 className="text-lg font-semibold text-gray-900 mb-1">{homework.title}</h3>
                          <p className="text-gray-600 text-sm line-clamp-2">{homework.description}</p>
                        </div>
                        <div className="flex items-center space-x-2 ml-4">
                          <div className="flex items-center space-x-1">
                            {getPriorityIcon(homework.priority)}
                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(homework.priority)}`}>
                              {homework.priority === 'high' ? 'Élevée' : homework.priority === 'medium' ? 'Moyenne' : 'Faible'}
                            </span>
                          </div>
                          <div className="flex items-center space-x-1">
                            {getStatusIcon(homework.status)}
                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(homework.status)}`}>
                              {homework.status === 'completed' ? 'Terminé' : 
                               homework.status === 'in_progress' ? 'En cours' : 
                               homework.status === 'overdue' ? 'En retard' : 'En attente'}
                            </span>
                          </div>
                        </div>
                      </div>

                      {/* Enhanced metadata grid */}
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-gray-600 mb-4">
                        <div className="flex items-center space-x-2">
                          <BookOpen className="w-4 h-4 text-gray-400" />
                          <span className="font-medium">{homework.subject}</span>
                        </div>
                        <div className="flex items-center space-x-2">
                          <Calendar className="w-4 h-4 text-gray-400" />
                          <div>
                            <div className="font-medium">{formatDate(homework.due_date)}</div>
                            <div className="text-xs text-gray-500">{getTimeUntilDue(homework.due_date)}</div>
                          </div>
                        </div>
                        <div className="flex items-center space-x-2">
                          <Users className="w-4 h-4 text-gray-400" />
                          <span className="font-medium">{getAssignmentTarget(homework)}</span>
                        </div>
                        {homework.estimated_time && (
                          <div className="flex items-center space-x-2">
                            <Clock className="w-4 h-4 text-gray-400" />
                            <span className="font-medium">{homework.estimated_time} min</span>
                          </div>
                        )}
                      </div>

                      {/* File attachment preview */}
                      {homework.attachment && (
                        <div className="bg-gray-50 rounded-lg p-3 mb-4">
                          <div className="flex items-center space-x-3">
                            <FileText className="w-5 h-5 text-blue-500" />
                            <div className="flex-1 min-w-0">
                              <p className="text-sm font-medium text-gray-900 truncate">{homework.attachment.name}</p>
                              <p className="text-xs text-gray-500">
                                {(homework.attachment.size / 1024 / 1024).toFixed(2)} MB
                              </p>
                            </div>
                            <div className="flex space-x-2">
                              <button
                                onClick={() => handleViewHomework(homework)}
                                className="p-1 text-gray-400 hover:text-blue-600"
                                title="Visualiser"
                              >
                                <Eye className="w-4 h-4" />
                              </button>
                              <a
                                href={`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/uploads/assignments/${homework.attachment.url.split('/').pop()}`}
                                download={homework.attachment.name}
                                className="p-1 text-gray-400 hover:text-green-600"
                                title="Télécharger"
                              >
                                <Download className="w-4 h-4" />
                              </a>
                            </div>
                          </div>
                        </div>
                      )}

                      {/* Creation info */}
                      <div className="text-xs text-gray-500">
                        Créé le {formatDate(homework.created_at, true)}
                      </div>
                    </div>

                    {/* Action buttons */}
                    <div className="flex items-center space-x-1 ml-4">
                      <button 
                        onClick={() => handleViewHomework(homework)}
                        className="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-md transition-colors"
                        title="Consulter"
                      >
                        <Eye className="w-4 h-4" />
                      </button>
                      <button 
                        onClick={() => handleEditHomework(homework)}
                        className="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-md transition-colors"
                        title="Modifier"
                      >
                        <Edit className="w-4 h-4" />
                      </button>
                      <button 
                        onClick={() => handleDeleteHomework(homework.id)}
                        className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-md transition-colors"
                        title="Supprimer"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        ) : (
          <div className="grid gap-6">
            {learningGoals.map((goal) => (
              <div key={goal.id} className="bg-white rounded-lg shadow p-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <h3 className="text-lg font-semibold text-gray-900">{goal.title}</h3>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(goal.status)}`}>
                        {goal.status}
                      </span>
                    </div>
                    <p className="text-gray-600 mb-3">{goal.description}</p>
                    <div className="flex items-center space-x-4 text-sm text-gray-500 mb-3">
                      <div className="flex items-center">
                        <BookOpen className="w-4 h-4 mr-1" />
                        {goal.subject}
                      </div>
                      <div className="flex items-center">
                        <Calendar className="w-4 h-4 mr-1" />
                        {new Date(goal.target_date).toLocaleDateString()}
                      </div>
                      <div className="flex items-center">
                        <BarChart3 className="w-4 h-4 mr-1" />
                        {goal.progress}% complété
                      </div>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-blue-600 h-2 rounded-full" 
                        style={{ width: `${goal.progress}%` }}
                      ></div>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <button className="p-2 text-gray-400 hover:text-blue-600">
                      <Edit className="w-4 h-4" />
                    </button>
                    <button className="p-2 text-gray-400 hover:text-red-600">
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Modal Création Devoir */}
        {showCreateModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
              <h2 className="text-xl font-bold mb-4">Nouveau Devoir</h2>
              <form onSubmit={handleCreateHomework}>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Titre</label>
                    <input
                      type="text"
                      value={homeworkForm.title}
                      onChange={(e) => setHomeworkForm({...homeworkForm, title: e.target.value})}
                      className="w-full border border-gray-300 rounded-md px-3 py-2"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                    <textarea
                      value={homeworkForm.description}
                      onChange={(e) => setHomeworkForm({...homeworkForm, description: e.target.value})}
                      className="w-full border border-gray-300 rounded-md px-3 py-2"
                      rows={3}
                      required
                    />
                  </div>
                  
                  {/* Zone d'upload de fichier */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Fichier du devoir</label>
                    <div 
                      className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-400 transition-colors"
                      onDragOver={(e) => {
                        e.preventDefault();
                        e.currentTarget.classList.add('border-blue-400', 'bg-blue-50');
                      }}
                      onDragLeave={(e) => {
                        e.currentTarget.classList.remove('border-blue-400', 'bg-blue-50');
                      }}
                      onDrop={(e) => {
                        e.preventDefault();
                        e.currentTarget.classList.remove('border-blue-400', 'bg-blue-50');
                        const files = e.dataTransfer.files;
                        if (files.length > 0) {
                          const file = files[0];
                          if (file.size <= 10 * 1024 * 1024) { // 10 MB max
                            setHomeworkForm({...homeworkForm, attachment: file});
                          } else {
                            alert('Fichier trop volumineux. Taille maximum : 10 MB');
                          }
                        }
                      }}
                    >
                      {homeworkForm.attachment ? (
                        <div className="space-y-2">
                          <div className="flex items-center justify-center space-x-2">
                            <FileText className="w-8 h-8 text-blue-500" />
                            <span className="text-sm font-medium text-gray-700">{homeworkForm.attachment.name}</span>
                          </div>
                          <div className="flex items-center justify-center space-x-2">
                            <button
                              type="button"
                              onClick={() => setHomeworkForm({...homeworkForm, attachment: null})}
                              className="text-red-500 hover:text-red-700 text-sm"
                            >
                              Supprimer
                            </button>
                            <span className="text-gray-500 text-xs">
                              {(homeworkForm.attachment.size / 1024 / 1024).toFixed(2)} MB
                            </span>
                          </div>
                        </div>
                      ) : (
                        <div className="space-y-4">
                          <div className="flex flex-col items-center space-y-2">
                            <Upload className="w-12 h-12 text-gray-400" />
                            <div className="text-sm text-gray-600">
                              <label htmlFor="file-upload" className="cursor-pointer">
                                <span className="text-blue-600 hover:text-blue-500 font-medium">
                                  Cliquez pour sélectionner
                                </span>
                                {' '}ou glissez-déposez votre fichier ici
                              </label>
                            </div>
                            <p className="text-xs text-gray-500">
                              PDF, DOC, DOCX, TXT jusqu'à 10 MB
                            </p>
                          </div>
                          <input
                            id="file-upload"
                            type="file"
                            accept=".pdf,.doc,.docx,.txt"
                            onChange={(e) => {
                              const file = e.target.files?.[0];
                              if (file && file.size <= 10 * 1024 * 1024) { // 10 MB max
                                setHomeworkForm({...homeworkForm, attachment: file});
                              } else if (file) {
                                alert('Fichier trop volumineux. Taille maximum : 10 MB');
                              }
                            }}
                            className="hidden"
                          />
                        </div>
                      )}
                    </div>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Matière</label>
                    <input
                      type="text"
                      value={homeworkForm.subject}
                      onChange={(e) => setHomeworkForm({...homeworkForm, subject: e.target.value})}
                      className="w-full border border-gray-300 rounded-md px-3 py-2"
                      required
                    />
                  </div>
                  
                  {/* Type d'assignation */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Type d'assignation</label>
                    <div className="flex space-x-4">
                      <label className="flex items-center">
                        <input
                          type="radio"
                          value="class"
                          checked={assignmentType === 'class'}
                          onChange={(e) => setAssignmentType(e.target.value as 'class' | 'student')}
                          className="mr-2"
                        />
                        <Users className="w-4 h-4 mr-1" />
                        Par classe
                      </label>
                      <label className="flex items-center">
                        <input
                          type="radio"
                          value="student"
                          checked={assignmentType === 'student'}
                          onChange={(e) => setAssignmentType(e.target.value as 'class' | 'student')}
                          className="mr-2"
                        />
                        <UserCheck className="w-4 h-4 mr-1" />
                        Étudiants spécifiques
                      </label>
                    </div>
                  </div>

                  {assignmentType === 'class' ? (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Classe</label>
                      <select
                        value={homeworkForm.class_id}
                        onChange={(e) => setHomeworkForm({...homeworkForm, class_id: parseInt(e.target.value)})}
                        className="w-full border border-gray-300 rounded-md px-3 py-2"
                        required
                      >
                        <option value={0}>Sélectionner une classe</option>
                        {teacherTargets.classes.map((classGroup) => (
                          <option key={classGroup.id} value={classGroup.id}>
                            {classGroup.name} ({classGroup.student_count} étudiants)
                          </option>
                        ))}
                      </select>
                    </div>
                  ) : (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Sélectionner les étudiants</label>
                      <div className="border border-gray-300 rounded-md p-3 max-h-40 overflow-y-auto">
                        {teacherTargets.students.map((student) => (
                          <label key={student.id} className="flex items-center py-1">
                            <input
                              type="checkbox"
                              checked={selectedStudents.includes(student.id)}
                              onChange={() => handleStudentToggle(student.id)}
                              className="mr-2"
                            />
                            {student.name} ({student.email})
                          </label>
                        ))}
                      </div>
                      {selectedStudents.length > 0 && (
                        <p className="text-sm text-gray-600 mt-1">
                          {selectedStudents.length} étudiant(s) sélectionné(s)
                        </p>
                      )}
                    </div>
                  )}

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Date limite</label>
                    <input
                      type="datetime-local"
                      value={homeworkForm.due_date}
                      onChange={(e) => setHomeworkForm({...homeworkForm, due_date: e.target.value})}
                      className="w-full border border-gray-300 rounded-md px-3 py-2"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Priorité</label>
                    <select
                      value={homeworkForm.priority}
                      onChange={(e) => setHomeworkForm({...homeworkForm, priority: e.target.value})}
                      className="w-full border border-gray-300 rounded-md px-3 py-2"
                    >
                      <option value="low">Faible</option>
                      <option value="medium">Moyenne</option>
                      <option value="high">Élevée</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Temps estimé (minutes)</label>
                    <input
                      type="number"
                      value={homeworkForm.estimated_time}
                      onChange={(e) => setHomeworkForm({...homeworkForm, estimated_time: e.target.value})}
                      className="w-full border border-gray-300 rounded-md px-3 py-2"
                      placeholder="Optionnel"
                    />
                  </div>
                </div>
                <div className="flex justify-end space-x-3 mt-6">
                  <button
                    type="button"
                    onClick={() => setShowCreateModal(false)}
                    className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
                  >
                    Annuler
                  </button>
                  <button
                    type="submit"
                    className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                    disabled={assignmentType === 'student' && selectedStudents.length === 0}
                  >
                    Créer
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Modal Consultation Devoir */}
        {showViewModal && selectedHomework && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold">Détails du Devoir</h2>
                <button
                  onClick={() => setShowViewModal(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <XCircle className="w-6 h-6" />
                </button>
              </div>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Titre</label>
                  <p className="text-gray-900 font-medium">{selectedHomework.title}</p>
                </div>
                
                                 <div>
                   <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                   <p className="text-gray-900">{selectedHomework.description}</p>
                 </div>
                 
                 {/* Affichage du fichier du devoir */}
                 <div>
                   <label className="block text-sm font-medium text-gray-700 mb-1">Fichier du devoir</label>
                   {selectedHomework.attachment && selectedHomework.attachment.name ? (
                     <div className="border border-gray-200 rounded-lg p-4 bg-gray-50">
                       <div className="flex items-center space-x-3">
                         <FileText className="w-8 h-8 text-blue-500" />
                         <div className="flex-1">
                           <p className="text-sm font-medium text-gray-900">{selectedHomework.attachment.name}</p>
                           <p className="text-xs text-gray-500">
                             {(selectedHomework.attachment.size / 1024 / 1024).toFixed(2)} MB
                           </p>
                         </div>
                         <div className="flex space-x-2">
                                                       <button
                              onClick={() => {
                                // Extraire le nom du fichier depuis l'URL
                                const urlParts = selectedHomework.attachment!.url.split('/');
                                const serverFilename = urlParts[urlParts.length - 1];
                                const fileUrl = `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/uploads/assignments/${serverFilename}`;
                                console.log('🔗 URL du fichier:', fileUrl);
                                console.log('📄 Nom du fichier sur le serveur:', serverFilename);
                                window.open(fileUrl, '_blank');
                              }}
                              className="px-3 py-1 bg-blue-600 text-white text-xs rounded hover:bg-blue-700 transition-colors"
                              title="Visualiser le fichier"
                            >
                              Visualiser
                            </button>
                            <a
                              href={`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/uploads/assignments/${selectedHomework.attachment!.url.split('/').pop()}`}
                              download={selectedHomework.attachment!.name}
                              className="px-3 py-1 bg-green-600 text-white text-xs rounded hover:bg-green-700 transition-colors"
                              title="Télécharger le fichier"
                            >
                              Télécharger
                            </a>
                         </div>
                       </div>
                     </div>
                   ) : (
                     <div className="border border-gray-200 rounded-lg p-4 bg-gray-50">
                       <div className="text-center text-gray-500">
                         <FileText className="w-8 h-8 mx-auto mb-2 text-gray-400" />
                         <p className="text-sm">Aucun fichier attaché à ce devoir</p>
                       </div>
                     </div>
                   )}
                 </div>
                 
                 <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Matière</label>
                    <p className="text-gray-900">{selectedHomework.subject}</p>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Date limite</label>
                    <p className="text-gray-900">{new Date(selectedHomework.due_date).toLocaleDateString()}</p>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Priorité</label>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(selectedHomework.priority)}`}>
                      {selectedHomework.priority}
                    </span>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Statut</label>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(selectedHomework.status)}`}>
                      {selectedHomework.status}
                    </span>
                  </div>
                  
                  {selectedHomework.estimated_time && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Temps estimé</label>
                      <p className="text-gray-900">{selectedHomework.estimated_time} minutes</p>
                    </div>
                  )}
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Cible</label>
                    <p className="text-gray-900">{getAssignmentTarget(selectedHomework)}</p>
                  </div>
                </div>
              </div>
              
              <div className="flex justify-end space-x-3 mt-6">
                <button
                  onClick={() => {
                    setShowViewModal(false);
                    handleEditHomework(selectedHomework);
                  }}
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                >
                  Modifier
                </button>
                <button
                  onClick={() => setShowViewModal(false)}
                  className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
                >
                  Fermer
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Modal Modification Devoir */}
        {showEditModal && selectedHomework && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold">Modifier le Devoir</h2>
                <button
                  onClick={() => setShowEditModal(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <XCircle className="w-6 h-6" />
                </button>
              </div>
              
              <form onSubmit={handleUpdateHomework}>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Titre</label>
                    <input
                      type="text"
                      value={homeworkForm.title}
                      onChange={(e) => setHomeworkForm({...homeworkForm, title: e.target.value})}
                      className="w-full border border-gray-300 rounded-md px-3 py-2"
                      required
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                    <textarea
                      value={homeworkForm.description}
                      onChange={(e) => setHomeworkForm({...homeworkForm, description: e.target.value})}
                      className="w-full border border-gray-300 rounded-md px-3 py-2"
                      rows={3}
                      required
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Matière</label>
                    <input
                      type="text"
                      value={homeworkForm.subject}
                      onChange={(e) => setHomeworkForm({...homeworkForm, subject: e.target.value})}
                      className="w-full border border-gray-300 rounded-md px-3 py-2"
                      required
                    />
                  </div>
                  
                  {/* Type d'assignation */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Type d'assignation</label>
                    <div className="flex space-x-4">
                      <label className="flex items-center">
                        <input
                          type="radio"
                          value="class"
                          checked={assignmentType === 'class'}
                          onChange={(e) => setAssignmentType(e.target.value as 'class' | 'student')}
                          className="mr-2"
                        />
                        <Users className="w-4 h-4 mr-1" />
                        Par classe
                      </label>
                      <label className="flex items-center">
                        <input
                          type="radio"
                          value="student"
                          checked={assignmentType === 'student'}
                          onChange={(e) => setAssignmentType(e.target.value as 'class' | 'student')}
                          className="mr-2"
                        />
                        <UserCheck className="w-4 h-4 mr-1" />
                        Étudiants spécifiques
                      </label>
                    </div>
                  </div>

                  {assignmentType === 'class' ? (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Classe</label>
                      <select
                        value={homeworkForm.class_id}
                        onChange={(e) => setHomeworkForm({...homeworkForm, class_id: parseInt(e.target.value)})}
                        className="w-full border border-gray-300 rounded-md px-3 py-2"
                        required
                      >
                        <option value={0}>Sélectionner une classe</option>
                        {teacherTargets.classes.map((classGroup) => (
                          <option key={classGroup.id} value={classGroup.id}>
                            {classGroup.name} ({classGroup.student_count} étudiants)
                          </option>
                        ))}
                      </select>
                    </div>
                  ) : (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Sélectionner les étudiants</label>
                      <div className="border border-gray-300 rounded-md p-3 max-h-40 overflow-y-auto">
                        {teacherTargets.students.map((student) => (
                          <label key={student.id} className="flex items-center py-1">
                            <input
                              type="checkbox"
                              checked={selectedStudents.includes(student.id)}
                              onChange={() => handleStudentToggle(student.id)}
                              className="mr-2"
                            />
                            {student.name} ({student.email})
                          </label>
                        ))}
                      </div>
                      {selectedStudents.length > 0 && (
                        <p className="text-sm text-gray-600 mt-1">
                          {selectedStudents.length} étudiant(s) sélectionné(s)
                        </p>
                      )}
                    </div>
                  )}

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Date limite</label>
                    <input
                      type="datetime-local"
                      value={homeworkForm.due_date}
                      onChange={(e) => setHomeworkForm({...homeworkForm, due_date: e.target.value})}
                      className="w-full border border-gray-300 rounded-md px-3 py-2"
                      required
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Priorité</label>
                    <select
                      value={homeworkForm.priority}
                      onChange={(e) => setHomeworkForm({...homeworkForm, priority: e.target.value})}
                      className="w-full border border-gray-300 rounded-md px-3 py-2"
                    >
                      <option value="low">Faible</option>
                      <option value="medium">Moyenne</option>
                      <option value="high">Élevée</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Temps estimé (minutes)</label>
                    <input
                      type="number"
                      value={homeworkForm.estimated_time}
                      onChange={(e) => setHomeworkForm({...homeworkForm, estimated_time: e.target.value})}
                      className="w-full border border-gray-300 rounded-md px-3 py-2"
                      placeholder="Optionnel"
                    />
                  </div>
                </div>
                
                <div className="flex justify-end space-x-3 mt-6">
                  <button
                    type="button"
                    onClick={() => setShowEditModal(false)}
                    className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
                  >
                    Annuler
                  </button>
                  <button
                    type="submit"
                    className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                    disabled={assignmentType === 'student' && selectedStudents.length === 0}
                  >
                    Mettre à jour
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Modal Création Objectif */}
        {showGoalModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
              <h2 className="text-xl font-bold mb-4">Nouvel Objectif d'Apprentissage</h2>
              <form onSubmit={handleCreateGoal}>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Titre</label>
                    <input
                      type="text"
                      value={goalForm.title}
                      onChange={(e) => setGoalForm({...goalForm, title: e.target.value})}
                      className="w-full border border-gray-300 rounded-md px-3 py-2"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                    <textarea
                      value={goalForm.description}
                      onChange={(e) => setGoalForm({...goalForm, description: e.target.value})}
                      className="w-full border border-gray-300 rounded-md px-3 py-2"
                      rows={3}
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Matière</label>
                    <input
                      type="text"
                      value={goalForm.subject}
                      onChange={(e) => setGoalForm({...goalForm, subject: e.target.value})}
                      className="w-full border border-gray-300 rounded-md px-3 py-2"
                      required
                    />
                  </div>
                  
                  {/* Type d'assignation */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Type d'assignation</label>
                    <div className="flex space-x-4">
                      <label className="flex items-center">
                        <input
                          type="radio"
                          value="class"
                          checked={assignmentType === 'class'}
                          onChange={(e) => setAssignmentType(e.target.value as 'class' | 'student')}
                          className="mr-2"
                        />
                        <Users className="w-4 h-4 mr-1" />
                        Par classe
                      </label>
                      <label className="flex items-center">
                        <input
                          type="radio"
                          value="student"
                          checked={assignmentType === 'student'}
                          onChange={(e) => setAssignmentType(e.target.value as 'class' | 'student')}
                          className="mr-2"
                        />
                        <UserCheck className="w-4 h-4 mr-1" />
                        Étudiants spécifiques
                      </label>
                    </div>
                  </div>

                  {assignmentType === 'class' ? (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Classe</label>
                      <select
                        value={goalForm.class_id}
                        onChange={(e) => setGoalForm({...goalForm, class_id: parseInt(e.target.value)})}
                        className="w-full border border-gray-300 rounded-md px-3 py-2"
                        required
                      >
                        <option value={0}>Sélectionner une classe</option>
                        {teacherTargets.classes.map((classGroup) => (
                          <option key={classGroup.id} value={classGroup.id}>
                            {classGroup.name} ({classGroup.student_count} étudiants)
                          </option>
                        ))}
                      </select>
                    </div>
                  ) : (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Sélectionner les étudiants</label>
                      <div className="border border-gray-300 rounded-md p-3 max-h-40 overflow-y-auto">
                        {teacherTargets.students.map((student) => (
                          <label key={student.id} className="flex items-center py-1">
                            <input
                              type="checkbox"
                              checked={selectedStudents.includes(student.id)}
                              onChange={() => handleStudentToggle(student.id)}
                              className="mr-2"
                            />
                            {student.name} ({student.email})
                          </label>
                        ))}
                      </div>
                      {selectedStudents.length > 0 && (
                        <p className="text-sm text-gray-600 mt-1">
                          {selectedStudents.length} étudiant(s) sélectionné(s)
                        </p>
                      )}
                    </div>
                  )}

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Date cible</label>
                    <input
                      type="datetime-local"
                      value={goalForm.target_date}
                      onChange={(e) => setGoalForm({...goalForm, target_date: e.target.value})}
                      className="w-full border border-gray-300 rounded-md px-3 py-2"
                      required
                    />
                  </div>
                </div>
                <div className="flex justify-end space-x-3 mt-6">
                  <button
                    type="button"
                    onClick={() => setShowGoalModal(false)}
                    className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
                  >
                    Annuler
                  </button>
                  <button
                    type="submit"
                    className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                    disabled={assignmentType === 'student' && selectedStudents.length === 0}
                  >
                    Créer
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  );
} 