'use client';

import React, { useState, useEffect } from 'react';
import { Calendar as CalendarIcon, Plus, Edit3, Trash2, Clock, MapPin, BookOpen, Target, Bell } from 'lucide-react';
import { organizationAPI, CalendarEvent, Homework } from '../api/student/organization';
import CalendarEventForm from './CalendarEventForm';

interface CalendarProps {
  onEventClick?: (event: CalendarEvent) => void;
  onAddEvent?: () => void;
}

export default function Calendar({ onEventClick, onAddEvent }: CalendarProps) {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [events, setEvents] = useState<CalendarEvent[]>([]);
  const [homeworks, setHomeworks] = useState<Homework[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedDate, setSelectedDate] = useState<Date | null>(null);
  const [showEventForm, setShowEventForm] = useState(false);
  const [formSelectedDate, setFormSelectedDate] = useState<Date | null>(null);

  // Générer le calendrier pour le mois actuel
  const generateCalendarDays = () => {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const startDate = new Date(firstDay);
    startDate.setDate(startDate.getDate() - firstDay.getDay());
    
    const days = [];
    const current = new Date(startDate);
    
    while (current <= lastDay || current.getDay() !== 0) {
      days.push(new Date(current));
      current.setDate(current.getDate() + 1);
    }
    
    return days;
  };

  // Charger les événements du calendrier et les devoirs
  useEffect(() => {
    const loadEvents = async () => {
      try {
        setLoading(true);
        const startDate = new Date(currentDate.getFullYear(), currentDate.getFullYear(), 1);
        const endDate = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0);
        
        // Charger les événements du calendrier
        const calendarEvents = await organizationAPI.getCalendarEvents(
          startDate.toISOString(),
          endDate.toISOString()
        );
        setEvents(calendarEvents);
        
        // Charger les devoirs
        const homeworksData = await organizationAPI.getHomeworks();
        setHomeworks(homeworksData);
      } catch (error) {
        console.error('Erreur lors du chargement des événements:', error);
        setEvents([]);
        setHomeworks([]);
      } finally {
        setLoading(false);
      }
    };

    loadEvents();
  }, [currentDate]);

  // Obtenir les événements pour une date donnée
  const getEventsForDate = (date: Date) => {
    return events.filter(event => {
      const eventDate = new Date(event.start_date);
      return eventDate.toDateString() === date.toDateString();
    });
  };

  // Obtenir les devoirs pour une date donnée
  const getHomeworksForDate = (date: Date) => {
    return homeworks.filter(homework => {
      const homeworkDate = new Date(homework.due_date);
      return homeworkDate.toDateString() === date.toDateString();
    });
  };

  // Transformer les devoirs en événements de calendrier
  const transformHomeworksToEvents = (homeworks: Homework[]) => {
    return homeworks.map(homework => ({
      id: homework.id,
      title: homework.title,
      description: homework.description,
      event_type: 'homework',
      start_date: homework.due_date,
      end_date: homework.due_date,
      color: getHomeworkColor(homework.priority),
      priority: homework.priority
    }));
  };

  // Obtenir la couleur selon la priorité du devoir
  const getHomeworkColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'bg-red-100 text-red-800 border-red-200';
      case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low': return 'bg-green-100 text-green-800 border-green-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  // Navigation dans le calendrier
  const goToPreviousMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, 1));
  };

  const goToNextMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 1));
  };

  const goToToday = () => {
    setCurrentDate(new Date());
  };

  // Formater la date
  const formatDate = (date: Date) => {
    return date.toLocaleDateString('fr-FR', { 
      month: 'long', 
      year: 'numeric' 
    });
  };

  // Formater le jour
  const formatDay = (date: Date) => {
    return date.getDate();
  };

  // Vérifier si c'est aujourd'hui
  const isToday = (date: Date) => {
    const today = new Date();
    return date.toDateString() === today.toDateString();
  };

  // Vérifier si c'est le mois actuel
  const isCurrentMonth = (date: Date) => {
    return date.getMonth() === currentDate.getMonth();
  };

  // Obtenir la couleur de l'événement
  const getEventColor = (eventType: string) => {
    const colors = {
      homework: 'bg-red-100 text-red-800 border-red-200',
      study_session: 'bg-blue-100 text-blue-800 border-blue-200',
      reminder: 'bg-yellow-100 text-yellow-800 border-yellow-200',
      goal: 'bg-green-100 text-green-800 border-green-200',
      exam: 'bg-purple-100 text-purple-800 border-purple-200',
      meeting: 'bg-indigo-100 text-indigo-800 border-indigo-200'
    };
    return colors[eventType as keyof typeof colors] || colors.reminder;
  };

  // Obtenir l'icône de l'événement
  const getEventIcon = (eventType: string) => {
    switch (eventType) {
      case 'homework': return <BookOpen className="w-3 h-3" />;
      case 'study_session': return <Clock className="w-3 h-3" />;
      case 'goal': return <Target className="w-3 h-3" />;
      case 'reminder': return <Bell className="w-3 h-3" />;
      default: return <CalendarIcon className="w-3 h-3" />;
    }
  };

  // Obtenir le label de l'événement
  const getEventLabel = (eventType: string) => {
    switch (eventType) {
      case 'homework': return 'Devoir';
      case 'study_session': return 'Session';
      case 'goal': return 'Objectif';
      case 'reminder': return 'Rappel';
      default: return 'Événement';
    }
  };

  const calendarDays = generateCalendarDays();

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      {/* En-tête du calendrier */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-4">
          <CalendarIcon className="h-6 w-6 text-blue-600" />
          <h2 className="text-xl font-semibold text-gray-900">
            {formatDate(currentDate)}
          </h2>
        </div>
        
        <div className="flex items-center space-x-2">
          <button
            onClick={goToPreviousMonth}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          
          <button
            onClick={goToToday}
            className="px-4 py-2 text-sm font-medium text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
          >
            Aujourd'hui
          </button>
          
          <button
            onClick={goToNextMonth}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </button>
          
          <button
            onClick={() => {
              setFormSelectedDate(null);
              setShowEventForm(true);
            }}
            className="ml-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center space-x-2"
          >
            <Plus className="w-4 h-4" />
            <span>Ajouter</span>
          </button>
        </div>
      </div>

      {/* Jours de la semaine */}
      <div className="grid grid-cols-7 gap-1 mb-2">
        {['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam'].map(day => (
          <div key={day} className="text-center text-sm font-medium text-gray-500 py-2">
            {day}
          </div>
        ))}
      </div>

      {/* Grille du calendrier */}
      <div className="grid grid-cols-7 gap-1">
        {calendarDays.map((date, index) => {
          const dayEvents = getEventsForDate(date);
          const dayHomeworks = getHomeworksForDate(date);
          const isCurrentMonthDay = isCurrentMonth(date);
          const isTodayDate = isToday(date);
          
          return (
            <div
              key={index}
              className={`
                min-h-[100px] p-2 border border-gray-200 relative
                ${isCurrentMonthDay ? 'bg-white' : 'bg-gray-50'}
                ${isTodayDate ? 'ring-2 ring-blue-500' : ''}
                hover:bg-gray-50 transition-colors cursor-pointer
              `}
              onClick={() => {
                setSelectedDate(date);
                setFormSelectedDate(date);
              }}
            >
              {/* Numéro du jour */}
              <div className={`
                text-sm font-medium mb-1
                ${isCurrentMonthDay ? 'text-gray-900' : 'text-gray-400'}
                ${isTodayDate ? 'text-blue-600 font-bold' : ''}
              `}>
                {formatDay(date)}
              </div>

              {/* Événements du jour */}
              <div className="space-y-1">
                {/* Afficher d'abord les devoirs */}
                {dayHomeworks.slice(0, 3).map((homework, homeworkIndex) => (
                  <div
                    key={`homework-${homeworkIndex}`}
                    className={`
                      text-xs p-1 rounded border truncate cursor-pointer flex items-center space-x-1
                      ${getHomeworkColor(homework.priority)}
                      hover:opacity-80 transition-opacity
                    `}
                    onClick={(e) => {
                      e.stopPropagation();
                      // Ici vous pouvez ajouter une action pour afficher les détails du devoir
                      console.log('Devoir cliqué:', homework);
                    }}
                    title={`Devoir: ${homework.title} - Priorité: ${homework.priority}`}
                  >
                    <BookOpen className="w-3 h-3" />
                    <span className="truncate">{homework.title}</span>
                  </div>
                ))}
                
                {/* Puis afficher les autres événements */}
                {dayEvents.slice(0, 2).map((event, eventIndex) => (
                  <div
                    key={`event-${eventIndex}`}
                    className={`
                      text-xs p-1 rounded border truncate cursor-pointer flex items-center space-x-1
                      ${getEventColor(event.event_type)}
                      hover:opacity-80 transition-opacity
                    `}
                    onClick={(e) => {
                      e.stopPropagation();
                      onEventClick?.(event);
                    }}
                    title={`${getEventLabel(event.event_type)}: ${event.title}`}
                  >
                    {getEventIcon(event.event_type)}
                    <span className="truncate">{event.title}</span>
                  </div>
                ))}
                
                {/* Afficher le total des événements */}
                {(dayHomeworks.length + dayEvents.length) > 5 && (
                  <div className="text-xs text-gray-500 text-center">
                    +{(dayHomeworks.length + dayEvents.length) - 5} autres
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Événements du jour sélectionné */}
      {selectedDate && (
        <div className="mt-6 p-4 bg-gray-50 rounded-lg">
          <h3 className="text-lg font-medium text-gray-900 mb-3">
            Événements du {selectedDate.toLocaleDateString('fr-FR', { 
              weekday: 'long', 
              year: 'numeric', 
              month: 'long', 
              day: 'numeric' 
            })}
          </h3>
          
          {getEventsForDate(selectedDate).length === 0 && getHomeworksForDate(selectedDate).length === 0 ? (
            <p className="text-gray-500">Aucun événement pour cette date</p>
          ) : (
            <div className="space-y-3">
              {/* Afficher d'abord les devoirs */}
              {getHomeworksForDate(selectedDate).map((homework, index) => (
                <div
                  key={`homework-${index}`}
                  className={`
                    p-3 rounded-lg border-l-4 cursor-pointer
                    ${getHomeworkColor(homework.priority)}
                    hover:shadow-md transition-shadow
                  `}
                  onClick={() => {
                    // Ici vous pouvez ajouter une action pour afficher les détails du devoir
                    console.log('Devoir sélectionné:', homework);
                  }}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <BookOpen className="w-4 h-4" />
                      <span className="font-medium">{homework.title}</span>
                    </div>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      homework.priority === 'high' ? 'bg-red-100 text-red-800' :
                      homework.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-green-100 text-green-800'
                    }`}>
                      {homework.priority === 'high' ? 'Élevée' : 
                       homework.priority === 'medium' ? 'Moyenne' : 'Faible'}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mt-1">{homework.description}</p>
                  <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
                    <span>Matière: {homework.subject}</span>
                    <span>Temps estimé: {homework.estimated_time} min</span>
                  </div>
                </div>
              ))}
              
              {/* Puis afficher les autres événements */}
              {getEventsForDate(selectedDate).map((event, index) => (
                <div
                  key={`event-${index}`}
                  className={`
                    p-3 rounded-lg border-l-4 cursor-pointer
                    ${getEventColor(event.event_type).replace('bg-', 'bg-').replace('text-', 'text-')}
                    hover:shadow-md transition-shadow
                  `}
                  onClick={() => onEventClick?.(event)}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-1">
                        {getEventIcon(event.event_type)}
                        <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">
                          {getEventLabel(event.event_type)}
                        </span>
                      </div>
                      <h4 className="font-medium text-gray-900">{event.title}</h4>
                      {event.description && (
                        <p className="text-sm text-gray-600 mt-1">{event.description}</p>
                      )}
                      <div className="flex items-center space-x-4 mt-2 text-sm text-gray-500">
                        <div className="flex items-center space-x-1">
                          <Clock className="w-4 h-4" />
                          <span>
                            {new Date(event.start_date).toLocaleTimeString('fr-FR', { 
                              hour: '2-digit', 
                              minute: '2-digit' 
                            })}
                          </span>
                        </div>
                        {event.location && (
                          <div className="flex items-center space-x-1">
                            <MapPin className="w-4 h-4" />
                            <span>{event.location}</span>
                          </div>
                        )}
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-2">
                      <button className="p-1 hover:bg-white hover:bg-opacity-50 rounded">
                        <Edit3 className="w-4 h-4" />
                      </button>
                      <button className="p-1 hover:bg-white hover:bg-opacity-50 rounded">
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Formulaire d'ajout d'événement */}
      <CalendarEventForm
        isOpen={showEventForm}
        onClose={() => setShowEventForm(false)}
        onEventCreated={() => {
          // Recharger les événements
          const loadEvents = async () => {
            try {
              const startDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
              const endDate = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0);
              
              const calendarEvents = await organizationAPI.getCalendarEvents(
                startDate.toISOString(),
                endDate.toISOString()
              );
              setEvents(calendarEvents);
            } catch (error) {
              console.error('Erreur lors du rechargement des événements:', error);
            }
          };
          loadEvents();
        }}
        selectedDate={formSelectedDate}
      />
    </div>
  );
}
