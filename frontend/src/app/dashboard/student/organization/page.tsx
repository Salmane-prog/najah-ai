'use client';

import '../../../../styles/no-hover-effects.css';

import React, { useState, useEffect, useCallback } from 'react';
import Sidebar from '../../../../components/Sidebar';
import { useAuth  } from '../../../../hooks/useAuth';
import { organizationAPI, StudySession, Reminder, LearningGoal, Milestone, CalendarEvent } from '../../../../api/student/organization';
// import { homeworkAPI, Homework } from '../../../../api/student/homework';
import { studySessionAPI, StudySession as StudySessionType } from '../../../../api/student/study-sessions';
import { learningGoalsAPI, LearningGoal as LearningGoalType } from '../../../../api/student/learning-goals';
import OrganizationAnalytics from '../../../../components/OrganizationAnalytics';
// import { HomeworkWidget } from '../../../../components/widgets';
import CreateStudySessionModal from '../../../../components/modals/CreateStudySessionModal';
import LearningGoalModal from '../../../../components/modals/LearningGoalModal';
import { 
  Calendar, 
  Clock, 
  BookOpen, 
  Target, 
  CheckCircle, 
  AlertCircle, 
  Star,
  Edit3,
  Trash2,
  Bell,
  BellOff,
  TrendingUp,
  Calendar as CalendarIcon,
  Clock as ClockIcon,
  Book as BookIcon,
  Target as TargetIcon,
  CheckSquare,
  Square,
  Filter,
  Search,
  MoreVertical,
  ArrowLeft,
  ArrowRight,
  Plus
} from 'lucide-react';
import ProfessionalTaskWidget from '../../../../components/widgets/ProfessionalTaskWidget';



export default function OrganizationPage() {
  const { user, token } = useAuth();
  const [homeworks, setHomeworks] = useState<any[]>([]);
  // const [studentHomeworks, setStudentHomeworks] = useState<Homework[]>([]);
  const [studySessions, setStudySessions] = useState<StudySession[]>([]);
  const [reminders, setReminders] = useState<Reminder[]>([]);
  const [learningGoals, setLearningGoals] = useState<LearningGoal[]>([]);
  const [calendarEvents, setCalendarEvents] = useState<CalendarEvent[]>([]);
  const [selectedTab, setSelectedTab] = useState<'calendar' | 'homework' | 'study' | 'goals' | 'reminders'>('calendar');
  const [selectedDate, setSelectedDate] = useState(new Date(2025, 0, 1)); // Janvier 2025 pour voir les devoirs récents
  const [currentMonth, setCurrentMonth] = useState(new Date(2025, 0, 1)); // Mois actuel affiché
  const [calendarView, setCalendarView] = useState<'month' | 'week' | 'day'>('month');
  const [studySessionSort, setStudySessionSort] = useState<'recent' | 'oldest' | 'duration'>('recent');
  const [learningGoalSort, setLearningGoalSort] = useState<'recent' | 'oldest' | 'progress'>('recent');
  const [showStudySessionModal, setShowStudySessionModal] = useState(false);
  const [showLearningGoalModal, setShowLearningGoalModal] = useState(false);



  const [loading, setLoading] = useState(true);

  // Fonctions de chargement des données
  const loadStudySessions = async () => {
    if (!user) {
      setStudySessions(mockStudySessions);
      return;
    }
    
    // Vérifier si le token est valide avant de faire l'appel API
    if (!token) {
      console.warn('Aucun token disponible, utilisation des données mockées');
      setStudySessions(mockStudySessions);
      return;
    }
    
    try {
      const sessions = await studySessionAPI.getStudySessions(user.id);
      setStudySessions(sessions);
      console.log('Sessions d\'étude chargées:', sessions.length);
    } catch (error) {
      console.error('Erreur lors du chargement des sessions d\'étude:', error);
      // En cas d'erreur 401, rediriger vers la page de connexion ou utiliser les données mockées
      if (error instanceof Error && error.message.includes('401')) {
        console.warn('Token expiré, utilisation des données mockées');
        setStudySessions(mockStudySessions);
      } else {
        setStudySessions(mockStudySessions);
      }
    }
  };

  const loadLearningGoals = async () => {
    if (!user) {
      setLearningGoals(mockLearningGoals);
      return;
    }
    
    // Vérifier si le token est valide avant de faire l'appel API
    if (!token) {
      console.warn('Aucun token disponible, utilisation des données mockées');
      setLearningGoals(mockLearningGoals);
      return;
    }
    
    try {
      const goals = await learningGoalsAPI.getLearningGoals(user.id);
      setLearningGoals(goals);
      console.log('Objectifs chargés:', goals.length);
    } catch (error) {
      console.error('Erreur lors du chargement des objectifs:', error);
      // En cas d'erreur 401, utiliser les données mockées
      if (error instanceof Error && error.message.includes('401')) {
        console.warn('Token expiré, utilisation des données mockées');
        setLearningGoals(mockLearningGoals);
      } else {
        setLearningGoals(mockLearningGoals);
      }
    }
  };

  // Charger les devoirs assignés à l'étudiant
  const loadStudentAssignments = async () => {
    if (!user) {
      setHomeworks([]);
      return;
    }
    
    // Vérifier si le token est valide avant de faire l'appel API
    if (!token) {
      console.warn('Aucun token disponible, pas de devoirs chargés');
      setHomeworks([]);
      return;
    }
    
    try {
      // Utiliser l'endpoint des devoirs assignés
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/assignments/homework/assigned/${user.id}`, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        const assignments = await response.json();
        console.log('Devoirs assignés chargés:', assignments.length);
        
        // Convertir les assignations en format Homework avec toutes les informations
        const studentHomeworks = assignments.map((assignment: any) => ({
          id: assignment.id,
          title: assignment.title,
          description: assignment.description,
          subject: assignment.subject,
          due_date: assignment.due_date,
          priority: assignment.priority,
          status: assignment.status || 'pending',
          estimated_time: assignment.estimated_time,
          tags: [],
          attachments: assignment.attachment ? [assignment.attachment.name] : [],
          // Ajouter les informations des fichiers et soumissions
          attachment: assignment.attachment || null,
          submission: assignment.submission || null
        }));
        
        setHomeworks(studentHomeworks);
      } else {
        // Gérer les erreurs 401 spécifiquement
        if (response.status === 401) {
          console.warn('Token expiré, pas de devoirs chargés');
        } else {
          console.error('Erreur lors du chargement des devoirs assignés:', response.status);
        }
        setHomeworks([]);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des devoirs assignés:', error);
      setHomeworks([]);
    }
  };

  // Fonction pour vérifier et rafraîchir le token si nécessaire
  const checkAndRefreshToken = async () => {
    if (!token) return false;
    
    try {
      // Vérifier si le token est expiré en le décodant
      const payload = JSON.parse(atob(token.split('.')[1]));
      const now = Date.now() / 1000;
      
      if (payload.exp < now) {
        console.warn('Token expiré, redirection vers la page de connexion');
        // Ici vous pourriez rediriger vers la page de connexion
        // router.push('/login');
        return false;
      }
      
      return true;
    } catch (error) {
      console.error('Erreur lors de la vérification du token:', error);
      return false;
    }
  };

  // Charger les données au montage du composant
  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      
      // Vérifier le token avant de charger les données
      const isTokenValid = await checkAndRefreshToken();
      
      if (!isTokenValid) {
        console.warn('Token invalide, utilisation des données mockées');
        setStudySessions(mockStudySessions);
        setLearningGoals(mockLearningGoals);
        setHomeworks([]);
        setLoading(false);
        return;
      }
      
      try {
        await Promise.all([
          loadStudySessions(),
          loadLearningGoals(),
          loadStudentAssignments() // Charger les devoirs assignés
        ]);
      } catch (error) {
        console.error('Erreur lors du chargement des données:', error);
      } finally {
        setLoading(false);
      }
    };

    if (user) {
      loadData();
    } else {
      setLoading(false);
    }
  }, [user, token]);

  // Supprimer les données mockées

  const mockStudySessions: StudySession[] = [
    {
      id: 1,
      title: 'Révision mathématiques',
      subject: 'Mathématiques',
      start_time: '2024-01-16T14:00:00Z',
      end_time: '2024-01-16T16:00:00Z',
      duration: 120,
      goals: ['Réviser les équations', 'Faire les exercices'],
      completed: true,
      notes: 'Bien progressé sur les équations du second degré'
    },
    {
      id: 2,
      title: 'Lecture littérature',
      subject: 'Français',
      start_time: '2024-01-17T10:00:00Z',
      end_time: '2024-01-17T11:30:00Z',
      duration: 90,
      goals: ['Lire le chapitre 5', 'Prendre des notes'],
      completed: false
    }
  ];

  const mockReminders: Reminder[] = [
    {
      id: 1,
      title: 'Rendre le devoir de maths',
      message: 'N\'oubliez pas de rendre votre devoir de mathématiques',
      due_date: '2024-01-20T23:59:00Z',
      priority: 'high',
      is_active: true,
      repeat: 'none'
    },
    {
      id: 2,
      title: 'Révision quotidienne',
      message: '30 minutes de révision chaque jour',
      due_date: '2024-01-16T20:00:00Z',
      priority: 'medium',
      is_active: true,
      repeat: 'daily'
    }
  ];

  const mockLearningGoals: LearningGoal[] = [
    {
      id: 1,
      title: 'Maîtriser les équations du second degré',
      description: 'Être capable de résoudre toutes les équations du second degré',
      subject: 'Mathématiques',
      target_date: '2024-02-01T00:00:00Z',
      progress: 75,
      status: 'in_progress',
      milestones: [
        { id: 1, title: 'Comprendre la formule du discriminant', completed: true, due_date: '2024-01-10T00:00:00Z' },
        { id: 2, title: 'Résoudre 10 exercices', completed: true, due_date: '2024-01-15T00:00:00Z' },
        { id: 3, title: 'Passer le test final', completed: false, due_date: '2024-01-25T00:00:00Z' }
      ]
    },
    {
      id: 2,
      title: 'Améliorer l\'expression écrite',
      description: 'Écrire des textes plus fluides et structurés',
      subject: 'Français',
      target_date: '2024-03-01T00:00:00Z',
      progress: 40,
      status: 'in_progress',
      milestones: [
        { id: 4, title: 'Lire 5 livres', completed: true, due_date: '2024-01-20T00:00:00Z' },
        { id: 5, title: 'Écrire 3 dissertations', completed: false, due_date: '2024-02-15T00:00:00Z' },
        { id: 6, title: 'Améliorer la grammaire', completed: false, due_date: '2024-02-28T00:00:00Z' }
      ]
    }
  ];

  const mockCalendarEvents: CalendarEvent[] = [
    {
      id: 1,
      title: 'Cours de mathématiques',
      description: 'Équations du second degré',
      event_type: 'course',
      start_time: '2024-01-16T09:00:00Z',
      end_time: '2024-01-16T10:30:00Z',
      location: 'Salle 101',
      subject: 'Mathématiques',
      color: '#3B82F6',
      is_recurring: true,
      recurrence_pattern: { frequency: 'weekly', interval: 1 },
      class_name: 'Terminale S'
    },
    {
      id: 2,
      title: 'Devoir de français',
      description: 'Dissertation sur la liberté',
      event_type: 'exam',
      start_time: '2024-01-18T14:00:00Z',
      end_time: '2024-01-18T16:00:00Z',
      location: 'Salle 102',
      subject: 'Français',
      color: '#EF4444',
      is_recurring: false,
      recurrence_pattern: null,
      class_name: 'Terminale S'
    }
  ];

  // Supprimer complètement l'ancien système qui écrase les données
  // const loadData = useCallback(async () => { ... }, []);
  // useEffect(() => { if (user) { loadData(); } }, [user]);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatTime = (minutes: number) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return hours > 0 ? `${hours}h${mins > 0 ? mins : ''}` : `${mins}min`;
  };

  // Fonction pour obtenir les devoirs d'une date spécifique
  const getHomeworksForDate = (date: Date) => {
    const filtered = homeworks.filter(homework => {
      const dueDate = new Date(homework.due_date);
      return dueDate.toDateString() === date.toDateString();
    });
    console.log(`Devoirs pour ${date.toDateString()}:`, filtered);
    return filtered;
  };

  // Fonction pour obtenir la couleur de priorité
  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'bg-red-100 text-red-700';
      case 'medium': return 'bg-yellow-100 text-yellow-700';
      case 'low': return 'bg-green-100 text-green-700';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'text-green-600 bg-green-100';
      case 'in_progress': return 'text-blue-600 bg-blue-100';
      case 'pending': return 'text-gray-600 bg-gray-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const handleHomeworkStatus = async (homeworkId: number, newStatus: string) => {
    try {
      await organizationAPI.updateHomeworkStatus(homeworkId, newStatus);
      // Mettre à jour l'état local après le changement
      setHomeworks(prev => prev.map(hw => 
        hw.id === homeworkId ? { ...hw, status: newStatus as any } : hw
      ));
    } catch (error) {
      console.error('Error updating homework status:', error);
    }
  };

  const handleStudySessionComplete = async (sessionId: number) => {
    try {
      await studySessionAPI.completeStudySession(sessionId);
      // Mettre à jour l'état local après le changement
      setStudySessions(prev => prev.map(session => 
        session.id === sessionId ? { ...session, completed: !session.completed } : session
      ));
    } catch (error) {
      console.error('Error toggling study session:', error);
    }
  };













  const handleMilestoneComplete = async (goalId: number, milestoneId: number) => {
    try {
      await organizationAPI.toggleMilestoneComplete(goalId, milestoneId);
      // Mettre à jour l'état local après le changement
      setLearningGoals(prev => prev.map(goal => {
        if (goal.id === goalId) {
          const updatedMilestones = goal.milestones.map(milestone => 
            milestone.id === milestoneId ? { ...milestone, completed: !milestone.completed } : milestone
          );
          const completedCount = updatedMilestones.filter(m => m.completed).length;
          const progress = Math.round((completedCount / updatedMilestones.length) * 100);
          return { ...goal, milestones: updatedMilestones, progress };
        }
        return goal;
      }));
    } catch (error) {
      console.error('Error toggling milestone:', error);
    }
  };

  const handleReminderToggle = async (reminderId: number) => {
    try {
      await organizationAPI.toggleReminder(reminderId);
      // Mettre à jour l'état local après le changement
      setReminders(prev => prev.map(reminder => 
        reminder.id === reminderId ? { ...reminder, is_active: !reminder.is_active } : reminder
      ));
    } catch (error) {
      console.error('Error toggling reminder:', error);
    }
  };

  // Fonctions de navigation du calendrier
  const goToPreviousPeriod = () => {
    const newDate = new Date(currentMonth);
    if (calendarView === 'month') {
      newDate.setMonth(newDate.getMonth() - 1);
    } else if (calendarView === 'week') {
      newDate.setDate(newDate.getDate() - 7);
    } else if (calendarView === 'day') {
      newDate.setDate(newDate.getDate() - 1);
    }
    setCurrentMonth(newDate);
  };

  const goToNextPeriod = () => {
    const newDate = new Date(currentMonth);
    if (calendarView === 'month') {
      newDate.setMonth(newDate.getMonth() + 1);
    } else if (calendarView === 'week') {
      newDate.setDate(newDate.getDate() + 7);
    } else if (calendarView === 'day') {
      newDate.setDate(newDate.getDate() + 1);
    }
    setCurrentMonth(newDate);
  };

  const formatPeriodDisplay = (date: Date) => {
    switch (calendarView) {
      case 'month':
        return date.toLocaleDateString('fr-FR', { month: 'long', year: 'numeric' });
      case 'week':
        const startOfWeek = new Date(date);
        startOfWeek.setDate(date.getDate() - date.getDay());
        const endOfWeek = new Date(startOfWeek);
        endOfWeek.setDate(startOfWeek.getDate() + 6);
        return `${startOfWeek.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short' })} - ${endOfWeek.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short', year: 'numeric' })}`;
      case 'day':
        return date.toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
      default:
        return date.toLocaleDateString('fr-FR');
    }
  };

  // Fonction de tri pour les sessions d'étude
  const getSortedStudySessions = () => {
    const sorted = [...studySessions];
    switch (studySessionSort) {
      case 'recent':
        return sorted.sort((a, b) => new Date(b.start_time).getTime() - new Date(a.start_time).getTime());
      case 'oldest':
        return sorted.sort((a, b) => new Date(a.start_time).getTime() - new Date(b.start_time).getTime());
      case 'duration':
        return sorted.sort((a, b) => b.duration - a.duration);
      default:
        return sorted;
    }
  };

  // Fonction de tri pour les objectifs d'apprentissage
  const getSortedLearningGoals = () => {
    const sorted = [...learningGoals];
    switch (learningGoalSort) {
      case 'recent':
        return sorted.sort((a, b) => new Date(b.created_at || b.target_date).getTime() - new Date(a.created_at || a.target_date).getTime());
      case 'oldest':
        return sorted.sort((a, b) => new Date(a.created_at || a.target_date).getTime() - new Date(b.created_at || b.target_date).getTime());
      case 'progress':
        return sorted.sort((a, b) => b.progress - a.progress);
      default:
        return sorted;
    }
  };

  const getDaysInMonth = (date: Date) => {
    const year = date.getFullYear();
    const month = date.getMonth();
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const daysInMonth = lastDay.getDate();
    const firstDayOfWeek = firstDay.getDay();
    
    // Ajuster pour que lundi = 0, dimanche = 6
    const adjustedFirstDay = firstDayOfWeek === 0 ? 6 : firstDayOfWeek - 1;
    
    return { daysInMonth, adjustedFirstDay };
  };

  // Fonctions pour les vues calendrier
  const getWeekDays = (date: Date) => {
    const startOfWeek = new Date(date);
    const day = date.getDay();
    const diff = date.getDate() - day + (day === 0 ? -6 : 1); // Ajuster pour lundi
    startOfWeek.setDate(diff);
    
    const weekDays = [];
    for (let i = 0; i < 7; i++) {
      const day = new Date(startOfWeek);
      day.setDate(startOfWeek.getDate() + i);
      weekDays.push(day);
    }
    return weekDays;
  };

  const getSessionsForDate = (date: Date) => {
    return studySessions.filter(session => {
      const sessionDate = new Date(session.start_time);
      return sessionDate.toDateString() === date.toDateString();
    });
  };

  const renderCalendarView = () => {
    switch (calendarView) {
      case 'month':
        return renderMonthView();
      case 'week':
        return renderWeekView();
      case 'day':
        return renderDayView();
      default:
        return renderMonthView();
    }
  };

  const renderMonthView = () => (
    <div className="grid grid-cols-7 gap-1">
      {['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'].map(day => (
        <div key={day} className="p-3 text-center font-medium text-gray-500 text-sm">
          {day}
        </div>
      ))}
      
      {/* Jours vides avant le premier jour du mois */}
      {Array.from({ length: getDaysInMonth(currentMonth).adjustedFirstDay }, (_, i) => (
        <div key={`empty-${i}`} className="p-3 border border-gray-200 min-h-[80px] bg-gray-50"></div>
      ))}
      
      {/* Jours du mois */}
      {Array.from({ length: getDaysInMonth(currentMonth).daysInMonth }, (_, i) => {
        const day = i + 1;
        const currentDate = new Date(currentMonth.getFullYear(), currentMonth.getMonth(), day);
        const dayHomeworks = getHomeworksForDate(currentDate);
        const daySessions = getSessionsForDate(currentDate);
        
        return (
          <div key={day} className="p-3 border border-gray-200 min-h-[80px] relative">
            <span className="text-sm font-medium">{day}</span>
            {/* Devoirs pour ce jour */}
            {dayHomeworks.length > 0 && (
              <div className="mt-1 space-y-1">
                {dayHomeworks.map((homework, index) => (
                  <div 
                    key={`hw-${homework.id}-${index}`} 
                    className={`text-xs p-1 rounded ${getPriorityColor(homework.priority)}`}
                    title={`${homework.title} - ${homework.subject}`}
                  >
                    {homework.title.length > 15 
                      ? homework.title.substring(0, 15) + '...' 
                      : homework.title
                    }
                  </div>
                ))}
              </div>
            )}
            {/* Sessions d'étude pour ce jour */}
            {daySessions.length > 0 && (
              <div className="mt-1 space-y-1">
                {daySessions.map((session, index) => (
                  <div 
                    key={`ss-${session.id}-${index}`} 
                    className="text-xs p-1 rounded bg-blue-100 text-blue-700"
                    title={`${session.title} - ${session.subject}`}
                  >
                    {session.title.length > 15 
                      ? session.title.substring(0, 15) + '...' 
                      : session.title
                    }
                  </div>
                ))}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );

  const renderWeekView = () => {
    const weekDays = getWeekDays(currentMonth);
    
    return (
      <div className="grid grid-cols-8 gap-1">
        {/* En-tête avec les jours */}
        <div className="p-3 text-center font-medium text-gray-500 text-sm">
          Heure
        </div>
        {weekDays.map((day, index) => (
          <div key={index} className="p-3 text-center font-medium text-gray-500 text-sm">
            {day.toLocaleDateString('fr-FR', { weekday: 'short', day: '2-digit' })}
          </div>
        ))}
        
        {/* Heures de la journée */}
        {Array.from({ length: 24 }, (_, hour) => (
          <React.Fragment key={hour}>
            <div className="p-2 text-xs text-gray-500 border-r">
              {hour}:00
            </div>
            {weekDays.map((day, dayIndex) => {
              const currentDate = new Date(day);
              currentDate.setHours(hour);
              const dayHomeworks = getHomeworksForDate(currentDate);
              const daySessions = getSessionsForDate(currentDate);
              
              return (
                <div key={`${dayIndex}-${hour}`} className="p-1 border border-gray-200 min-h-[40px] text-xs">
                  {dayHomeworks.map((homework, index) => (
                    <div 
                      key={`hw-${homework.id}-${index}`} 
                      className={`p-1 rounded mb-1 ${getPriorityColor(homework.priority)}`}
                      title={homework.title}
                    >
                      {homework.title.substring(0, 10)}...
                    </div>
                  ))}
                  {daySessions.map((session, index) => (
                    <div 
                      key={`ss-${session.id}-${index}`} 
                      className="p-1 rounded mb-1 bg-blue-100 text-blue-700"
                      title={session.title}
                    >
                      {session.title.substring(0, 10)}...
                    </div>
                  ))}
                </div>
              );
            })}
          </React.Fragment>
        ))}
      </div>
    );
  };

  const renderDayView = () => {
    const currentDate = new Date(currentMonth);
    const dayHomeworks = getHomeworksForDate(currentDate);
    const daySessions = getSessionsForDate(currentDate);
    
    // Trier les événements par heure
    const allEvents = [
      ...dayHomeworks.map(hw => ({ ...hw, type: 'homework', time: new Date(hw.due_date) })),
      ...daySessions.map(ss => ({ ...ss, type: 'session', time: new Date(ss.start_time) }))
    ].sort((a, b) => a.time.getTime() - b.time.getTime());
    
    return (
      <div className="space-y-4">
        <div className="text-lg font-semibold text-gray-900 mb-4">
          {currentDate.toLocaleDateString('fr-FR', { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
          })}
        </div>
        
        {/* Devoirs du jour */}
        {dayHomeworks.length > 0 && (
          <div className="bg-white rounded-lg p-4 border">
            <h3 className="font-semibold text-gray-900 mb-3">Devoirs</h3>
            <div className="space-y-2">
              {dayHomeworks.map((homework, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                  <div>
                    <div className="font-medium">{homework.title}</div>
                    <div className="text-sm text-gray-600">{homework.subject}</div>
                  </div>
                  <span className={`px-2 py-1 rounded text-xs ${getPriorityColor(homework.priority)}`}>
                    {homework.priority}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {/* Sessions d'étude du jour */}
        {daySessions.length > 0 && (
          <div className="bg-white rounded-lg p-4 border">
            <h3 className="font-semibold text-gray-900 mb-3">Sessions d'étude</h3>
            <div className="space-y-2">
              {daySessions.map((session, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-blue-50 rounded">
                  <div>
                    <div className="font-medium">{session.title}</div>
                    <div className="text-sm text-gray-600">{session.subject}</div>
                  </div>
                  <span className="px-2 py-1 rounded text-xs bg-blue-100 text-blue-700">
                    {session.duration} min
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {allEvents.length === 0 && (
          <div className="text-center text-gray-500 py-8">
            Aucun événement prévu pour {currentDate.toLocaleDateString('fr-FR', { 
              weekday: 'long', 
              day: 'numeric', 
              month: 'long', 
              year: 'numeric' 
            })}
          </div>
        )}
        
        {/* Timeline des événements */}
        {allEvents.length > 0 && (
          <div className="bg-white rounded-lg p-4 border">
            <h3 className="font-semibold text-gray-900 mb-3">Planning de la journée</h3>
            <div className="space-y-3">
              {allEvents.map((event, index) => (
                <div key={`${event.type}-${event.id}-${index}`} className="flex items-center space-x-3 p-3 bg-gray-50 rounded">
                  <div className="flex-shrink-0">
                    <div className="w-3 h-3 rounded-full bg-blue-500"></div>
                  </div>
                  <div className="flex-1">
                    <div className="font-medium">{event.title}</div>
                    <div className="text-sm text-gray-600">{event.subject}</div>
                    <div className="text-xs text-gray-500">
                      {event.time.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}
                    </div>
                  </div>
                  <span className={`px-2 py-1 rounded text-xs ${
                    event.type === 'homework' 
                      ? getPriorityColor(event.priority)
                      : 'bg-blue-100 text-blue-700'
                  }`}>
                    {event.type === 'homework' ? 'Devoir' : 'Session'}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    );
  };

  if (loading) {
    return (
      <div className="flex min-h-screen bg-bg-secondary">
        <Sidebar />
        <div className="flex-1 ml-56 p-8 pb-32">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-200 rounded w-1/4 mb-6"></div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="h-48 bg-gray-200 rounded-lg"></div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-bg-secondary">
      <Sidebar />
      <div className="flex-1 ml-56 p-8 pb-32">
        {/* Header */}
        <div className="mb-8 animate-slide-in-up">
          <div>
            <h1 className="text-3xl font-bold text-primary mb-2">Organisation Personnelle</h1>
            <p className="text-secondary">Gérez votre calendrier, devoirs et objectifs d'apprentissage</p>
          </div>
        </div>

        {/* Tabs */}
        <div className="card-unified mb-8 animate-fade-in-scale">
          <div className="card-unified-body">
            <div className="flex border-b border-gray-200">
              {[
                { id: 'calendar', label: 'Calendrier', icon: CalendarIcon },
                { id: 'homework', label: 'Devoirs', icon: BookIcon },
                { id: 'study', label: 'Sessions d\'étude', icon: ClockIcon },
                { id: 'goals', label: 'Objectifs', icon: TargetIcon },
                { id: 'reminders', label: 'Rappels', icon: Bell }
              ].map(tab => (
                <button
                  key={tab.id}
                  onClick={() => setSelectedTab(tab.id as any)}
                  className={`flex items-center space-x-2 px-6 py-4 font-medium transition-colors ${
                    selectedTab === tab.id
                      ? 'text-primary border-b-2 border-primary'
                      : 'text-muted hover:text-primary'
                  }`}
                >
                  <tab.icon size={20} />
                  <span>{tab.label}</span>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Analytics Dashboard */}
        <div className="mb-8 animate-fade-in-scale">
          <OrganizationAnalytics />
        </div>

        {/* Content */}
        <div className="space-y-8">
          {selectedTab === 'calendar' && (
            <div className="card-unified animate-fade-in-scale">
              <div className="card-unified-body">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-xl font-semibold text-primary">Calendrier Scolaire</h2>
                <div className="flex items-center space-x-4">
                  {/* Boutons de vue */}
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => setCalendarView('month')}
                      className={`px-3 py-1 rounded text-sm font-medium transition-colors ${
                        calendarView === 'month' 
                          ? 'btn-unified btn-unified-primary' 
                          : 'bg-gray-100 text-muted hover:bg-gray-200'
                      }`}
                    >
                      Mois
                    </button>
                    <button
                      onClick={() => setCalendarView('week')}
                      className={`px-3 py-1 rounded text-sm font-medium transition-colors ${
                        calendarView === 'week' 
                          ? 'btn-unified btn-unified-primary' 
                          : 'bg-gray-100 text-muted hover:bg-gray-200'
                      }`}
                    >
                      Semaine
                    </button>
                    <button
                      onClick={() => setCalendarView('day')}
                      className={`px-3 py-1 rounded text-sm font-medium transition-colors ${
                        calendarView === 'day' 
                          ? 'btn-unified btn-unified-primary' 
                          : 'bg-gray-100 text-muted hover:bg-gray-200'
                      }`}
                    >
                      Jour
                    </button>
                  </div>
                  
                  {/* Navigation de la période */}
                  <div className="flex items-center space-x-2">
                    <button 
                      onClick={goToPreviousPeriod}
                      className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                    >
                      <ArrowLeft size={20} />
                    </button>
                    <span className="font-medium min-w-[200px] text-center text-sm">
                      {formatPeriodDisplay(currentMonth)}
                    </span>
                    <button 
                      onClick={goToNextPeriod}
                      className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                    >
                      <ArrowRight size={20} />
                    </button>
                  </div>
                  

                </div>
              </div>
              
                {/* Calendar Content */}
                {renderCalendarView()}
              </div>
            </div>
          )}

          {selectedTab === 'homework' && (
            <div className="space-y-6 animate-fade-in-scale">
              {/* Utiliser le composant EnhancedHomeworkWidget avec tous les boutons d'action */}
              <ProfessionalTaskWidget 
                homeworks={homeworks}
                onHomeworkUpdate={(updatedHomework) => {
                  // Mettre à jour la liste des devoirs
                  setHomeworks(prev => 
                    prev.map(hw => 
                      hw.id === updatedHomework.id ? updatedHomework : hw
                    )
                  );
                }}
              />
            </div>
          )}

          {selectedTab === 'study' && (
            <div className="space-y-6 animate-fade-in-scale">
              {/* Header */}
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-semibold text-primary">Mes Sessions d'Étude</h2>
                <div className="flex items-center space-x-2">
                  <select 
                    className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    value={studySessionSort}
                    onChange={(e) => setStudySessionSort(e.target.value as 'recent' | 'oldest' | 'duration')}
                  >
                    <option value="recent">Plus récent</option>
                    <option value="oldest">Plus ancien</option>
                    <option value="duration">Durée</option>
                  </select>
                  <button
                    onClick={() => setShowStudySessionModal(true)}
                    className="btn-unified btn-unified-primary flex items-center space-x-2"
                  >
                    <Plus size={16} />
                    <span>Nouvelle Session</span>
                  </button>
                </div>
              </div>
              
              <div className="max-h-96 overflow-y-auto space-y-6">
                {getSortedStudySessions().map(session => (
                  <div key={session.id} className="card-unified animate-fade-in-scale">
                    <div className="card-unified-body">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-3">
                          <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">
                            {session.subject}
                          </span>
                          {session.completed && (
                            <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm">
                              Terminé
                            </span>
                          )}
                        </div>
                        <h3 className="text-lg font-semibold text-primary mb-2">{session.title}</h3>
                        <div className="flex items-center space-x-4 text-sm text-muted mb-3">
                          <div className="flex items-center">
                            <Calendar size={16} className="mr-1" />
                            {formatDate(session.start_time)}
                          </div>
                          <div className="flex items-center">
                            <Clock size={16} className="mr-1" />
                            Durée : {formatTime(session.duration)}
                          </div>
                        </div>
                        <div className="mb-3">
                          <h4 className="font-medium text-primary mb-2">Objectifs :</h4>
                          <ul className="space-y-1">
                            {session.goals.map((goal, index) => (
                              <li key={index} className="flex items-center text-sm text-secondary">
                                <CheckCircle size={16} className="mr-2 text-green-500" />
                                {goal}
                              </li>
                            ))}
                          </ul>
                        </div>
                        {session.notes && (
                          <div className="p-3 bg-gray-50 rounded-lg">
                            <p className="text-sm text-secondary">{session.notes}</p>
                          </div>
                        )}
                      </div>
                      <div className="flex items-center space-x-2 ml-4">
                        <button
                          onClick={() => handleStudySessionComplete(session.id)}
                          className={`p-2 rounded-lg ${
                            session.completed 
                              ? 'text-green-600 bg-green-50' 
                              : 'text-gray-500 hover:text-green-600 hover:bg-gray-100'
                          }`}
                        >
                          <CheckCircle size={20} />
                        </button>
                        <button className="p-2 text-gray-500 hover:text-blue-600 rounded-lg hover:bg-gray-100">
                          <Edit3 size={16} />
                        </button>
                      </div>
                    </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {selectedTab === 'goals' && (
            <div className="space-y-6 animate-fade-in-scale">
              {/* Header */}
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-semibold text-primary">Mes Objectifs d'Apprentissage</h2>
                <div className="flex items-center space-x-2">
                  <select 
                    className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    value={learningGoalSort}
                    onChange={(e) => setLearningGoalSort(e.target.value as 'recent' | 'oldest' | 'progress')}
                  >
                    <option value="recent">Plus récent</option>
                    <option value="oldest">Plus ancien</option>
                    <option value="progress">Progression</option>
                  </select>
                  <button
                    onClick={() => setShowLearningGoalModal(true)}
                    className="btn-unified btn-unified-primary flex items-center space-x-2"
                  >
                    <Plus size={16} />
                    <span>Nouvel Objectif</span>
                  </button>
                </div>
              </div>
              
              <div className="max-h-96 overflow-y-auto space-y-6">
                {/* Debug: Afficher le nombre d'objectifs */}
                <div className="text-sm text-muted mb-2">
                  Total des objectifs : {getSortedLearningGoals().length}
                </div>
                {getSortedLearningGoals().map(goal => (
                  <div key={goal.id} className="card-unified animate-fade-in-scale">
                    <div className="card-unified-body">
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-3">
                          <span className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm">
                            {goal.subject}
                          </span>
                          <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(goal.status)}`}>
                            {goal.status === 'completed' ? 'Terminé' :
                             goal.status === 'in_progress' ? 'En cours' : 'Non commencé'}
                          </span>
                        </div>
                        <h3 className="text-lg font-semibold text-primary mb-2">{goal.title}</h3>
                        <p className="text-secondary mb-3">{goal.description}</p>
                        <div className="flex items-center space-x-4 text-sm text-muted">
                          <div className="flex items-center">
                            <Calendar size={16} className="mr-1" />
                            Objectif : {formatDate(goal.target_date)}
                          </div>
                          <div className="flex items-center">
                            <Target size={16} className="mr-1" />
                            Progression : {goal.progress}%
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    {/* Progress Bar */}
                    <div className="mb-4">
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${goal.progress}%` }}
                        ></div>
                      </div>
                    </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {selectedTab === 'reminders' && (
            <div className="space-y-6 animate-fade-in-scale">
              {/* Header */}
              <div>
                <h2 className="text-xl font-semibold text-primary">Mes Rappels</h2>
              </div>
              
              {reminders.map(reminder => (
                <div key={reminder.id} className="card-unified animate-fade-in-scale">
                  <div className="card-unified-body">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-3">
                        <span className={`px-3 py-1 rounded-full text-sm font-medium ${getPriorityColor(reminder.priority)}`}>
                          {reminder.priority === 'high' ? 'Priorité haute' : 
                           reminder.priority === 'medium' ? 'Priorité moyenne' : 'Priorité basse'}
                        </span>
                        <div className="flex items-center">
                          {reminder.is_active ? (
                            <Bell className="text-green-500" size={16} />
                          ) : (
                            <BellOff className="text-gray-400" size={16} />
                          )}
                          <span className={`ml-1 text-sm ${reminder.is_active ? 'text-green-600' : 'text-gray-500'}`}>
                            {reminder.is_active ? 'Actif' : 'Inactif'}
                          </span>
                        </div>
                        <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded-full text-xs">
                          {reminder.repeat === 'none' ? 'Une fois' :
                           reminder.repeat === 'daily' ? 'Quotidien' :
                           reminder.repeat === 'weekly' ? 'Hebdomadaire' : 'Mensuel'}
                        </span>
                      </div>
                      <h3 className="text-lg font-semibold text-primary mb-2">{reminder.title}</h3>
                      <p className="text-secondary mb-3">{reminder.message}</p>
                      <div className="flex items-center space-x-4 text-sm text-muted">
                        <div className="flex items-center">
                          <Calendar size={16} className="mr-1" />
                          Échéance : {formatDate(reminder.due_date)}
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2 ml-4">
                      <button
                        onClick={() => handleReminderToggle(reminder.id)}
                        className={`p-2 rounded-lg ${
                          reminder.is_active 
                            ? 'text-green-600 bg-green-50' 
                            : 'text-gray-500 hover:text-green-600 hover:bg-gray-100'
                        }`}
                      >
                        {reminder.is_active ? <Bell size={16} /> : <BellOff size={16} />}
                      </button>
                      <button className="p-2 text-gray-500 hover:text-blue-600 rounded-lg hover:bg-gray-100">
                        <Edit3 size={16} />
                      </button>
                      <button className="p-2 text-gray-500 hover:text-red-600 rounded-lg hover:bg-gray-100">
                        <Trash2 size={16} />
                      </button>
                    </div>
                  </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Modales */}
      {showStudySessionModal && (
        <CreateStudySessionModal
          isOpen={showStudySessionModal}
          onClose={() => setShowStudySessionModal(false)}
          onSuccess={async () => {
            setShowStudySessionModal(false);
            // Recharger les sessions d'étude immédiatement
            await loadStudySessions();
          }}
        />
      )}

      {showLearningGoalModal && (
        <LearningGoalModal
          isOpen={showLearningGoalModal}
          onClose={() => setShowLearningGoalModal(false)}
          onSuccess={async () => {
            setShowLearningGoalModal(false);
            // Recharger les objectifs d'apprentissage immédiatement
            await loadLearningGoals();
          }}
        />
      )}
    </div>
  );
} 