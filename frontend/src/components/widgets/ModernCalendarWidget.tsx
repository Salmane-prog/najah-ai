'use client';

import React, { useState, useEffect } from 'react';
import { Calendar, Clock, MapPin, BookOpen, Target, AlertCircle, ChevronLeft, ChevronRight, Plus, Filter } from 'lucide-react';

interface CalendarEvent {
  id: number;
  title: string;
  type: 'quiz' | 'homework' | 'exam' | 'course' | 'reminder' | 'deadline';
  start_time: string;
  end_time?: string;
  description?: string;
  subject?: string;
  location?: string;
  priority?: 'low' | 'medium' | 'high';
  completed?: boolean;
}

interface ModernCalendarWidgetProps {
  className?: string;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function ModernCalendarWidget({ className = '' }: ModernCalendarWidgetProps) {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [events, setEvents] = useState<CalendarEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedDate, setSelectedDate] = useState<Date | null>(null);
  const [selectedEvent, setSelectedEvent] = useState<CalendarEvent | null>(null);
  const [view, setView] = useState<'month' | 'week'>('month');
  const [filter, setFilter] = useState<string>('all');

  useEffect(() => {
    loadCalendarData();
  }, [currentDate]);

  const loadCalendarData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const token = localStorage.getItem('najah_token');
      const user = localStorage.getItem('najah_user');
      
      if (!token || !user) {
        setError('Authentification requise');
        setLoading(false);
        return;
      }
      
      const userData = JSON.parse(user);
      
      // Charger les événements du calendrier depuis les différents endpoints
      const startDate = new Date(currentDate);
      startDate.setDate(startDate.getDate() - 15);
      const endDate = new Date(currentDate);
      endDate.setDate(endDate.getDate() + 45);

      // Récupérer les événements depuis les différents endpoints
      const [assessmentsRes, learningPathsRes, quizzesRes, homeworksRes] = await Promise.all([
        fetch(`${API_BASE_URL}/api/v1/assessments/student/${userData.id}/pending`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).catch(() => ({ ok: false, json: () => [] })),
        
        fetch(`${API_BASE_URL}/api/v1/learning_paths/student/${userData.id}/active`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).catch(() => ({ ok: false, json: () => [] })),
        
        fetch(`${API_BASE_URL}/api/v1/quizzes/assigned/${userData.id}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).catch(() => ({ ok: false, json: () => [] })),
        
        fetch(`${API_BASE_URL}/api/v1/assignments/student/${userData.id}/assigned`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).catch(() => ({ ok: false, json: () => [] }))
      ]);

      // Combiner tous les événements
      let allEvents: any[] = [];
      
      if (assessmentsRes.ok) {
        const assessments = await assessmentsRes.json();
        // Assurez-vous que 'assessments' est un tableau avant d'appeler .map()
        if (Array.isArray(assessments)) {
          allEvents = allEvents.concat(assessments.map((assessment: any) => ({
            id: assessment.id,
            title: assessment.title,
            event_type: 'exam',
            start_time: assessment.created_at,
            end_time: new Date(new Date(assessment.created_at).getTime() + assessment.duration_minutes * 60000).toISOString(),
            description: assessment.description,
            subject: assessment.subject,
            priority: 'high'
          })));
        } else {
          console.warn("Assessments data is not an array:", assessments);
        }
      }
      
      if (learningPathsRes.ok) {
        const learningPaths = await learningPathsRes.json();
        // Assurez-vous que 'learningPaths' est un tableau avant d'appeler .map()
        if (Array.isArray(learningPaths)) {
          allEvents = allEvents.concat(learningPaths.map((path: any) => ({
            id: path.id,
            title: `Parcours: ${path.title}`,
            event_type: 'course',
            start_time: path.started_at || path.created_at,
            end_time: new Date(new Date(path.started_at || path.created_at).getTime() + path.estimated_duration_hours * 3600000).toISOString(),
            description: path.description,
            subject: path.subject,
            priority: 'medium'
          })));
        } else {
          console.warn("Learning paths data is not an array:", learningPaths);
        }
      }
      
      if (quizzesRes.ok) {
        const quizzes = await quizzesRes.json();
        // Assurez-vous que 'quizzes' est un tableau avant d'appeler .map()
        if (Array.isArray(quizzes)) {
          allEvents = allEvents.concat(quizzes.map((quiz: any) => ({
            id: quiz.id,
            title: `Quiz: ${quiz.title}`,
            event_type: 'quiz',
            start_time: quiz.assigned_at,
            end_time: quiz.due_date,
            description: quiz.description,
            subject: quiz.subject,
            priority: 'medium'
          })));
        } else {
          console.warn("Quizzes data is not an array:", quizzes);
        }
      }
      
      if (homeworksRes.ok) {
        const homeworks = await homeworksRes.json();
        console.log('📚 Devoirs bruts reçus:', homeworks);
        
        // Assurez-vous que 'homeworks' est un tableau avant d'appeler .map()
        if (Array.isArray(homeworks)) {
          const transformedHomeworks = homeworks.map((homework: any) => ({
            id: homework.id,
            title: `Devoir: ${homework.title}`,
            event_type: 'homework',
            start_time: homework.due_date, // Utiliser due_date comme date principale
            end_time: homework.due_date,
            description: homework.description,
            subject: homework.subject,
            priority: homework.priority || 'medium'
          }));
          
          console.log('🔄 Devoirs transformés:', transformedHomeworks);
          allEvents = allEvents.concat(transformedHomeworks);
        } else {
          console.warn("Homeworks data is not an array:", homeworks);
        }
      }

      // Filtrer les événements dans la période - Améliorer la logique
      const filteredEvents = allEvents.filter(event => {
        // Pour les devoirs, utiliser due_date, pour les autres start_time
        const eventDate = event.event_type === 'homework' 
          ? new Date(event.end_time || event.start_time)
          : new Date(event.start_time);
        
        // Vérifier que la date est valide
        if (isNaN(eventDate.getTime())) {
          console.warn('Date invalide pour l\'événement:', event);
          return false;
        }
        
        return eventDate >= startDate && eventDate <= endDate;
      });

      // Transformer les données pour correspondre à l'interface
      const transformedEvents = filteredEvents.map((event: any) => ({
        id: event.id,
        title: event.title || 'Événement sans titre',
        type: event.event_type || 'reminder',
        start_time: event.start_time,
        end_time: event.end_time,
        description: event.description || '',
        subject: event.subject || 'Général',
        location: event.location || 'Non spécifié',
        priority: event.priority || 'medium',
        completed: false
      }));
      
      setEvents(transformedEvents);
      
      console.log('📅 Événements chargés:', {
        total: transformedEvents.length,
        assessments: allEvents.filter(e => e.event_type === 'exam').length,
        learningPaths: allEvents.filter(e => e.event_type === 'course').length,
        quizzes: allEvents.filter(e => e.event_type === 'quiz').length,
        homeworks: allEvents.filter(e => e.event_type === 'homework').length,
        events: transformedEvents
      });
      
      if (transformedEvents.length === 0) {
        console.log('Aucun événement trouvé pour cette période');
      }
    } catch (err) {
      console.error('Erreur lors du chargement des événements:', err);
      
      if (err.message?.includes('401')) {
        setError('Session expirée. Veuillez vous reconnecter.');
      } else if (err.message?.includes('403')) {
        setError('Accès refusé au calendrier.');
      } else if (err.message?.includes('404')) {
        setError('Calendrier non trouvé.');
      } else {
        setError('Erreur lors du chargement des événements');
      }
    } finally {
      setLoading(false);
    }
  };

  const getDaysInMonth = (date: Date) => {
    const year = date.getFullYear();
    const month = date.getMonth();
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const daysInMonth = lastDay.getDate();
    const startingDay = firstDay.getDay();
    
    const days = [];
    
    // Ajouter les jours du mois précédent
    for (let i = startingDay - 1; i >= 0; i--) {
      const prevDate = new Date(year, month, -i);
      days.push({ date: prevDate, isCurrentMonth: false });
    }
    
    // Ajouter les jours du mois actuel
    for (let i = 1; i <= daysInMonth; i++) {
      const currentDate = new Date(year, month, i);
      days.push({ date: currentDate, isCurrentMonth: true });
    }
    
    // Ajouter les jours du mois suivant pour compléter la grille
    const remainingDays = 42 - days.length; // 6 semaines * 7 jours
    for (let i = 1; i <= remainingDays; i++) {
      const nextDate = new Date(year, month + 1, i);
      days.push({ date: nextDate, isCurrentMonth: false });
    }
    
    return days;
  };

  const getEventsForDate = (date: Date) => {
    const dateStr = date.toISOString().split('T')[0];
    return events.filter(event => {
      let eventDate: Date;
      
      // Pour les devoirs, utiliser end_time (due_date), pour les autres start_time
      if (event.type === 'homework') {
        eventDate = new Date(event.end_time || event.start_time);
      } else {
        eventDate = new Date(event.start_time);
      }
      
      // Vérifier que la date est valide
      if (isNaN(eventDate.getTime())) {
        return false;
      }
      
      return eventDate.toISOString().split('T')[0] === dateStr;
    });
  };

  const getEventTypeColor = (type: string) => {
    switch (type) {
      case 'quiz': return 'bg-blue-500';
      case 'homework': return 'bg-yellow-500';
      case 'exam': return 'bg-red-500';
      case 'course': return 'bg-green-500';
      case 'reminder': return 'bg-purple-500';
      case 'deadline': return 'bg-orange-500';
      default: return 'bg-gray-500';
    }
  };

  const getEventTypeIcon = (type: string) => {
    switch (type) {
      case 'quiz': return <BookOpen className="w-3 h-3" />;
      case 'homework': return <Target className="w-3 h-3" />;
      case 'exam': return <AlertCircle className="w-3 h-3" />;
      case 'course': return <BookOpen className="w-3 h-3" />;
      case 'reminder': return <Clock className="w-3 h-3" />;
      case 'deadline': return <AlertCircle className="w-3 h-3" />;
      default: return <Calendar className="w-3 h-3" />;
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'border-l-4 border-l-red-500';
      case 'medium': return 'border-l-4 border-l-yellow-500';
      case 'low': return 'border-l-4 border-l-green-500';
      default: return '';
    }
  };

  const formatTime = (dateString: string) => {
    return new Date(dateString).toLocaleTimeString('fr-FR', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const formatDate = (date: Date) => {
    return date.toLocaleDateString('fr-FR', {
      weekday: 'short',
      day: 'numeric',
      month: 'short',
    });
  };

  const isToday = (date: Date) => {
    const today = new Date();
    return date.toDateString() === today.toDateString();
  };

  const isSelected = (date: Date) => {
    return selectedDate && date.toDateString() === selectedDate.toDateString();
  };

  const handleDateClick = (date: Date) => {
    setSelectedDate(date);
    const dayEvents = getEventsForDate(date);
    if (dayEvents.length > 0) {
      setSelectedEvent(dayEvents[0]);
    }
  };

  const navigateMonth = (direction: 'prev' | 'next') => {
    const newDate = new Date(currentDate);
    if (direction === 'prev') {
      newDate.setMonth(newDate.getMonth() - 1);
    } else {
      newDate.setMonth(newDate.getMonth() + 1);
    }
    setCurrentDate(newDate);
  };

  const filteredEvents = events.filter(event => {
    if (filter === 'all') return true;
    return event.type === filter;
  });

  const days = getDaysInMonth(currentDate);

  return (
    <div className={`bg-white rounded-xl shadow-lg p-6 card-enhanced hover-lift-enhanced ${className}`}>
      {/* En-tête du calendrier */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-gray-800 flex items-center gap-2">
          <Calendar className="w-6 h-6 text-blue-600" />
          Calendrier
        </h2>
        <div className="flex items-center gap-3">
          {/* Filtres */}
          <div className="flex gap-1">
            <button
              onClick={() => setFilter('all')}
              className={`px-2 py-1 rounded text-xs font-medium transition-colors ${
                filter === 'all' 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              Tous
            </button>
            <button
              onClick={() => setFilter('quiz')}
              className={`px-2 py-1 rounded text-xs font-medium transition-colors ${
                filter === 'quiz' 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              Quiz
            </button>
            <button
              onClick={() => setFilter('homework')}
              className={`px-2 py-1 rounded text-xs font-medium transition-colors ${
                filter === 'homework' 
                  ? 'bg-yellow-600 text-white' 
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              Devoirs
            </button>
            <button
              onClick={() => setFilter('exam')}
              className={`px-2 py-1 rounded text-xs font-medium transition-colors ${
                filter === 'exam' 
                  ? 'bg-red-600 text-white' 
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              Examens
            </button>
          </div>
          
          {/* Navigation */}
          <div className="flex items-center gap-2">
            <button
              onClick={() => navigateMonth('prev')}
              className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <span className="text-sm font-medium text-gray-700 min-w-[120px] text-center">
              {currentDate.toLocaleDateString('fr-FR', { month: 'long', year: 'numeric' })}
            </span>
            <button
              onClick={() => navigateMonth('next')}
              className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
          {error}
        </div>
      )}

      {/* Grille du calendrier */}
      <div className="grid grid-cols-7 gap-1 mb-6">
        {/* En-têtes des jours */}
        {['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam'].map((day) => (
          <div key={day} className="p-2 text-center text-sm font-medium text-gray-500">
            {day}
          </div>
        ))}
        
        {/* Jours du calendrier */}
        {days.map((day, index) => {
          const dayEvents = getEventsForDate(day.date);
          const hasEvents = dayEvents.length > 0;
          
          return (
            <div
              key={index}
              onClick={() => handleDateClick(day.date)}
              className={`
                min-h-[80px] p-2 border rounded-lg cursor-pointer transition-all duration-200 hover:bg-gray-50
                ${day.isCurrentMonth ? 'bg-white' : 'bg-gray-50'}
                ${isToday(day.date) ? 'border-blue-500 bg-blue-50' : 'border-gray-200'}
                ${isSelected(day.date) ? 'border-purple-500 bg-purple-50' : ''}
                ${!day.isCurrentMonth ? 'text-gray-400' : 'text-gray-700'}
              `}
            >
              <div className="text-sm font-medium mb-1">
                {day.date.getDate()}
              </div>
              
              {/* Événements du jour */}
              <div className="space-y-1">
                {dayEvents.slice(0, 2).map((event) => (
                  <div
                    key={event.id}
                    onClick={(e) => {
                      e.stopPropagation();
                      setSelectedEvent(event);
                    }}
                    className={`
                      p-1 rounded text-xs text-white cursor-pointer hover:opacity-80 transition-opacity
                      ${getEventTypeColor(event.type)}
                    `}
                    title={event.title}
                  >
                    <div className="flex items-center gap-1">
                      {getEventTypeIcon(event.type)}
                      <span className="truncate">{event.title}</span>
                    </div>
                  </div>
                ))}
                
                {dayEvents.length > 2 && (
                  <div className="text-xs text-gray-500 text-center">
                    +{dayEvents.length - 2} autres
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Événements du jour sélectionné */}
      {selectedDate && (
        <div className="mt-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">
            Événements du {selectedDate.toLocaleDateString('fr-FR', { 
              weekday: 'long', 
              day: 'numeric', 
              month: 'long' 
            })}
          </h3>
          
          <div className="space-y-3">
            {loading ? (
              <div className="text-center py-8">
                <div className="text-blue-600 animate-pulse">Chargement des événements...</div>
              </div>
            ) : error ? (
              <div className="text-center py-8">
                <div className="text-red-600 mb-4">
                  <p className="font-semibold">Erreur de chargement</p>
                  <p className="text-sm">{error}</p>
                </div>
                <button 
                  onClick={loadCalendarData}
                  className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                >
                  Réessayer
                </button>
              </div>
            ) : events.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <Calendar className="w-12 h-12 mx-auto mb-3 text-gray-300" />
                <p className="font-medium mb-2">Aucun événement programmé</p>
                <p className="text-sm">Ce jour est libre pour vos études personnelles</p>
              </div>
            ) : getEventsForDate(selectedDate).length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <Calendar className="w-12 h-12 mx-auto mb-3 text-gray-300" />
                <p className="font-medium mb-2">Aucun événement ce jour</p>
                <p className="text-sm">Profitez-en pour avancer sur vos projets</p>
              </div>
            ) : (
              getEventsForDate(selectedDate).map((event) => (
                <div
                  key={event.id}
                  className={`p-4 bg-white rounded-lg border border-gray-200 hover:border-gray-300 transition-colors cursor-pointer ${getPriorityColor(event.priority)}`}
                  onClick={() => setSelectedEvent(event)}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <span className={`w-3 h-3 rounded-full ${getEventTypeColor(event.type)}`}></span>
                        <h4 className="font-medium text-gray-800">{event.title}</h4>
                        {event.completed && (
                          <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">
                            Terminé
                          </span>
                        )}
                      </div>
                      
                      {event.description && (
                        <p className="text-sm text-gray-600 mb-2">{event.description}</p>
                      )}
                      
                      <div className="flex items-center gap-4 text-sm text-gray-500">
                        <span className="flex items-center gap-1">
                          <Clock className="w-4 h-4" />
                          {formatTime(event.start_time)}
                        </span>
                        {event.subject && (
                          <span className="flex items-center gap-1">
                            <BookOpen className="w-4 h-4" />
                            {event.subject}
                          </span>
                        )}
                        {event.location && (
                          <span className="flex items-center gap-1">
                            <MapPin className="w-4 h-4" />
                            {event.location}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {/* Modal de détail d'événement */}
      {selectedEvent && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-bold text-gray-800">Détails de l'événement</h3>
              <button
                onClick={() => setSelectedEvent(null)}
                className="text-gray-500 hover:text-gray-700"
              >
                ✕
              </button>
            </div>
            
            <div className="space-y-4">
              <div className="flex items-center gap-2">
                <span className={`w-4 h-4 rounded-full ${getEventTypeColor(selectedEvent.type)}`}></span>
                <h4 className="font-semibold text-gray-800">{selectedEvent.title}</h4>
              </div>
              
              {selectedEvent.description && (
                <p className="text-gray-600">{selectedEvent.description}</p>
              )}
              
              <div className="space-y-2 text-sm">
                <div className="flex items-center gap-2">
                  <Clock className="w-4 h-4 text-gray-500" />
                  <span>Début: {formatTime(selectedEvent.start_time)}</span>
                </div>
                
                {selectedEvent.end_time && (
                  <div className="flex items-center gap-2">
                    <Clock className="w-4 h-4 text-gray-500" />
                    <span>Fin: {formatTime(selectedEvent.end_time)}</span>
                  </div>
                )}
                
                {selectedEvent.subject && (
                  <div className="flex items-center gap-2">
                    <BookOpen className="w-4 h-4 text-gray-500" />
                    <span>Matière: {selectedEvent.subject}</span>
                  </div>
                )}
                
                {selectedEvent.location && (
                  <div className="flex items-center gap-2">
                    <MapPin className="w-4 h-4 text-gray-500" />
                    <span>Lieu: {selectedEvent.location}</span>
                  </div>
                )}
                
                {selectedEvent.priority && (
                  <div className="flex items-center gap-2">
                    <AlertCircle className="w-4 h-4 text-gray-500" />
                    <span>Priorité: {selectedEvent.priority}</span>
                  </div>
                )}
              </div>
            </div>
            
            <div className="mt-6 flex justify-end">
              <button
                onClick={() => setSelectedEvent(null)}
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

