'use client';

import React, { useState, useEffect } from 'react';
import { useAuth  } from '@/hooks/useAuth';
import { calendarAPI, CalendarEvent, StudySession } from '@/api/student/calendar';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { 
  Calendar, 
  Clock, 
  MapPin, 
  Plus, 
  ChevronLeft, 
  ChevronRight,
  Event,
  BookOpen,
  AlertTriangle,
  CheckCircle
} from 'lucide-react';

export default function CalendarPage() {
  const { user } = useAuth();
  const [events, setEvents] = useState<CalendarEvent[]>([]);
  const [studySessions, setStudySessions] = useState<StudySession[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentDate, setCurrentDate] = useState(new Date());
  const [selectedView, setSelectedView] = useState<'week' | 'month'>('week');
  const [selectedEventType, setSelectedEventType] = useState<string>('');
  const [showEventModal, setShowEventModal] = useState(false);
  const [showSessionModal, setShowSessionModal] = useState(false);

  useEffect(() => {
    loadCalendarData();
  }, [currentDate]);

  const loadCalendarData = async () => {
    try {
      setLoading(true);
      const startDate = new Date(currentDate);
      startDate.setDate(startDate.getDate() - 7);
      const endDate = new Date(currentDate);
      endDate.setDate(endDate.getDate() + 7);

      const [eventsData, sessionsData] = await Promise.all([
        calendarAPI.getCalendarEvents(
          startDate.toISOString(),
          endDate.toISOString(),
          selectedEventType
        ),
        calendarAPI.getStudySessions(
          startDate.toISOString(),
          endDate.toISOString()
        )
      ]);

      setEvents(eventsData);
      setStudySessions(sessionsData);
    } catch (err) {
      setError('Erreur lors du chargement du calendrier');
      console.error('Erreur:', err);
    } finally {
      setLoading(false);
    }
  };

  const getEventsForDate = (date: Date) => {
    const dateStr = date.toISOString().split('T')[0];
    return events.filter(event => {
      const eventDate = new Date(event.start_time);
      return eventDate.toISOString().split('T')[0] === dateStr;
    });
  };

  const getSessionsForDate = (date: Date) => {
    const dateStr = date.toISOString().split('T')[0];
    return studySessions.filter(session => {
      const sessionDate = new Date(session.start_time);
      return sessionDate.toISOString().split('T')[0] === dateStr;
    });
  };

  const getEventTypeColor = (eventType: string) => {
    switch (eventType) {
      case 'course':
        return 'bg-blue-100 text-blue-800';
      case 'exam':
        return 'bg-red-100 text-red-800';
      case 'homework':
        return 'bg-yellow-100 text-yellow-800';
      case 'study_session':
        return 'bg-green-100 text-green-800';
      case 'reminder':
        return 'bg-purple-100 text-purple-800';
      default:
        return 'bg-gray-100 text-gray-800';
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

  const getWeekDays = () => {
    const days = [];
    const startOfWeek = new Date(currentDate);
    startOfWeek.setDate(startOfWeek.getDate() - startOfWeek.getDay() + 1);

    for (let i = 0; i < 7; i++) {
      const day = new Date(startOfWeek);
      day.setDate(day.getDate() + i);
      days.push(day);
    }
    return days;
  };

  const navigateWeek = (direction: 'prev' | 'next') => {
    const newDate = new Date(currentDate);
    if (direction === 'prev') {
      newDate.setDate(newDate.getDate() - 7);
    } else {
      newDate.setDate(newDate.getDate() + 7);
    }
    setCurrentDate(newDate);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="max-w-7xl mx-auto">
          <div className="animate-pulse space-y-6">
            {[1, 2, 3, 4, 5, 6, 7].map((i) => (
              <div key={i} className="bg-white rounded-lg p-6">
                <div className="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
                <div className="h-3 bg-gray-200 rounded w-3/4 mb-2"></div>
                <div className="h-3 bg-gray-200 rounded w-1/2"></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-2">
            <Calendar className="w-8 h-8 text-blue-600" />
            Calendrier Avancé
          </h1>
          <p className="text-gray-600 mt-2">
            Gérez vos événements, sessions d'étude et planifiez votre temps
          </p>
        </div>

        {/* Controls */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center gap-4">
              <Button
                variant="outline"
                onClick={() => navigateWeek('prev')}
              >
                <ChevronLeft className="w-4 h-4 mr-2" />
                Semaine précédente
              </Button>
              
              <span className="text-lg font-semibold">
                {formatDate(getWeekDays()[0])} - {formatDate(getWeekDays()[6])}
              </span>
              
              <Button
                variant="outline"
                onClick={() => navigateWeek('next')}
              >
                Semaine suivante
                <ChevronRight className="w-4 h-4 ml-2" />
              </Button>
            </div>

            <div className="flex items-center gap-4">
              <Select value={selectedEventType} onValueChange={setSelectedEventType}>
                <SelectTrigger className="w-48">
                  <SelectValue placeholder="Tous les types" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="">Tous les types</SelectItem>
                  <SelectItem value="course">Cours</SelectItem>
                  <SelectItem value="exam">Examen</SelectItem>
                  <SelectItem value="homework">Devoir</SelectItem>
                  <SelectItem value="study_session">Session d'étude</SelectItem>
                  <SelectItem value="reminder">Rappel</SelectItem>
                </SelectContent>
              </Select>

              <Button onClick={() => setShowEventModal(true)}>
                <Plus className="w-4 h-4 mr-2" />
                Nouvel événement
              </Button>

              <Button onClick={() => setShowSessionModal(true)} variant="outline">
                <BookOpen className="w-4 h-4 mr-2" />
                Nouvelle session
              </Button>
            </div>
          </div>
        </div>

        {/* Calendar Grid */}
        <div className="grid grid-cols-1 md:grid-cols-7 gap-4">
          {getWeekDays().map((day) => {
            const dayEvents = getEventsForDate(day);
            const daySessions = getSessionsForDate(day);
            const isToday = day.toDateString() === new Date().toDateString();

            return (
              <Card key={day.toISOString()} className={`${isToday ? 'border-blue-300 bg-blue-50' : ''}`}>
                <CardHeader className="pb-2">
                  <CardTitle className={`text-sm ${isToday ? 'text-blue-600' : 'text-gray-900'}`}>
                    {formatDate(day)}
                  </CardTitle>
                  <p className="text-xs text-gray-500">
                    {dayEvents.length + daySessions.length} événement(s)
                  </p>
                </CardHeader>
                <CardContent className="pt-0">
                  <div className="space-y-2">
                    {dayEvents.map((event) => (
                      <div key={event.id} className="p-2 bg-white rounded border text-xs">
                        <div className="flex items-center gap-1 mb-1">
                          <div className={`w-2 h-2 rounded-full ${event.color ? `bg-[${event.color}]` : 'bg-blue-500'}`}></div>
                          <span className="font-medium truncate">{event.title}</span>
                        </div>
                        <div className="flex items-center gap-1 text-gray-500">
                          <Clock className="w-3 h-3" />
                          <span>{formatTime(event.start_time)}</span>
                        </div>
                        <Badge className={getEventTypeColor(event.event_type)}>
                          {event.event_type}
                        </Badge>
                      </div>
                    ))}

                    {daySessions.map((session) => (
                      <div key={session.id} className="p-2 bg-green-50 rounded border text-xs">
                        <div className="flex items-center gap-1 mb-1">
                          <div className="w-2 h-2 rounded-full bg-green-500"></div>
                          <span className="font-medium truncate">{session.title}</span>
                        </div>
                        <div className="flex items-center gap-1 text-gray-500">
                          <Clock className="w-3 h-3" />
                          <span>{formatTime(session.start_time)}</span>
                          {session.duration && (
                            <span>({session.duration} min)</span>
                          )}
                        </div>
                        <Badge className="bg-green-100 text-green-800">
                          Session
                        </Badge>
                      </div>
                    ))}

                    {dayEvents.length === 0 && daySessions.length === 0 && (
                      <div className="text-center text-gray-400 py-4">
                        <p className="text-xs">Aucun événement</p>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {/* Event Modal */}
        {showEventModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
            <div className="bg-white rounded-lg p-6 w-full max-w-md mx-4">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold">Nouvel événement</h2>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setShowEventModal(false)}
                >
                  ×
                </Button>
              </div>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Titre
                  </label>
                  <Input placeholder="Titre de l'événement" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Type
                  </label>
                  <Select>
                    <SelectTrigger>
                      <SelectValue placeholder="Sélectionner un type" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="course">Cours</SelectItem>
                      <SelectItem value="exam">Examen</SelectItem>
                      <SelectItem value="homework">Devoir</SelectItem>
                      <SelectItem value="study_session">Session d'étude</SelectItem>
                      <SelectItem value="reminder">Rappel</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Date et heure de début
                  </label>
                  <Input type="datetime-local" />
                </div>
                <div className="flex justify-end gap-2">
                  <Button
                    variant="outline"
                    onClick={() => setShowEventModal(false)}
                  >
                    Annuler
                  </Button>
                  <Button>
                    Créer
                  </Button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Session Modal */}
        {showSessionModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
            <div className="bg-white rounded-lg p-6 w-full max-w-md mx-4">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold">Nouvelle session d'étude</h2>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setShowSessionModal(false)}
                >
                  ×
                </Button>
              </div>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Titre
                  </label>
                  <Input placeholder="Titre de la session" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Matière
                  </label>
                  <Input placeholder="Matière (optionnel)" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Date et heure de début
                  </label>
                  <Input type="datetime-local" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Durée (minutes)
                  </label>
                  <Input type="number" placeholder="60" />
                </div>
                <div className="flex justify-end gap-2">
                  <Button
                    variant="outline"
                    onClick={() => setShowSessionModal(false)}
                  >
                    Annuler
                  </Button>
                  <Button>
                    Créer
                  </Button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
