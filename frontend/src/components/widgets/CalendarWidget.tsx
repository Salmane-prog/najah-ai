'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Calendar, Clock, MapPin, Plus, ChevronLeft, ChevronRight } from 'lucide-react';
import { calendarAPI, CalendarEvent, StudySession } from '@/api/student/calendar';
import { useAuth  } from '@/hooks/useAuth';

interface CalendarWidgetProps {
  className?: string;
}

export default function CalendarWidget({ className }: CalendarWidgetProps) {
  const { user } = useAuth();
  const [events, setEvents] = useState<CalendarEvent[]>([]);
  const [studySessions, setStudySessions] = useState<StudySession[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentDate, setCurrentDate] = useState(new Date());
  const [selectedView, setSelectedView] = useState<'week' | 'month'>('week');

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
          endDate.toISOString()
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
      <Card className={className}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Calendar className="w-5 h-5" />
            Calendrier
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="animate-pulse space-y-4">
            {[1, 2, 3, 4, 5, 6, 7].map((i) => (
              <div key={i} className="flex items-center space-x-4">
                <div className="w-16 h-4 bg-gray-200 rounded"></div>
                <div className="flex-1 space-y-2">
                  <div className="h-3 bg-gray-200 rounded w-3/4"></div>
                  <div className="h-3 bg-gray-200 rounded w-1/2"></div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Calendar className="w-5 h-5" />
            Calendrier
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center text-red-500">
            <Calendar className="w-8 h-8 mx-auto mb-2" />
            <p>{error}</p>
            <Button onClick={loadCalendarData} className="mt-2">
              Réessayer
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  const weekDays = getWeekDays();

  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <Calendar className="w-5 h-5" />
            Calendrier
          </CardTitle>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => navigateWeek('prev')}
            >
              <ChevronLeft className="w-4 h-4" />
            </Button>
            <span className="text-sm font-medium">
              {formatDate(weekDays[0])} - {formatDate(weekDays[6])}
            </span>
            <Button
              variant="outline"
              size="sm"
              onClick={() => navigateWeek('next')}
            >
              <ChevronRight className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-2 max-h-96 overflow-y-auto">
          {weekDays.map((day) => {
            const dayEvents = getEventsForDate(day);
            const daySessions = getSessionsForDate(day);
            const isToday = day.toDateString() === new Date().toDateString();

            return (
              <div
                key={day.toISOString()}
                className={`border rounded-lg p-3 ${
                  isToday ? 'border-blue-300 bg-blue-50' : 'border-gray-200'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <h3 className={`font-semibold text-sm ${
                    isToday ? 'text-blue-600' : 'text-gray-900'
                  }`}>
                    {formatDate(day)}
                  </h3>
                  <span className="text-xs text-gray-500">
                    {dayEvents.length + daySessions.length} événement(s)
                  </span>
                </div>

                <div className="space-y-1">
                  {dayEvents.map((event) => (
                    <div key={event.id} className="flex items-center gap-2 p-2 bg-white rounded border">
                      <div className={`w-2 h-2 rounded-full ${
                        event.color ? `bg-[${event.color}]` : 'bg-blue-500'
                      }`}></div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-gray-900 truncate">
                          {event.title}
                        </p>
                        <div className="flex items-center gap-2 text-xs text-gray-500">
                          <Clock className="w-3 h-3" />
                          <span>{formatTime(event.start_time)}</span>
                          {event.location && (
                            <>
                              <MapPin className="w-3 h-3" />
                              <span>{event.location}</span>
                            </>
                          )}
                        </div>
                      </div>
                      <Badge className={getEventTypeColor(event.event_type)}>
                        {event.event_type}
                      </Badge>
                    </div>
                  ))}

                  {daySessions.map((session) => (
                    <div key={session.id} className="flex items-center gap-2 p-2 bg-green-50 rounded border">
                      <div className="w-2 h-2 rounded-full bg-green-500"></div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-gray-900 truncate">
                          {session.title}
                        </p>
                        <div className="flex items-center gap-2 text-xs text-gray-500">
                          <Clock className="w-3 h-3" />
                          <span>{formatTime(session.start_time)}</span>
                          {session.duration && (
                            <span>({session.duration} min)</span>
                          )}
                        </div>
                      </div>
                      <Badge className="bg-green-100 text-green-800">
                        Session
                      </Badge>
                    </div>
                  ))}

                  {dayEvents.length === 0 && daySessions.length === 0 && (
                    <div className="text-center text-gray-400 py-2">
                      <p className="text-xs">Aucun événement</p>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}