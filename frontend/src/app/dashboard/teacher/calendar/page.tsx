'use client';

import React, { useState, useEffect } from 'react';
import Sidebar from '../../../../components/Sidebar';
import { useAuth  } from '../../../../hooks/useAuth';
import { 
  Calendar, 
  Plus, 
  Clock, 
  MapPin, 
  Users, 
  BookOpen, 
  AlertCircle,
  Edit,
  Trash2,
  Filter,
  Search
} from 'lucide-react';

interface CalendarEvent {
  id: number;
  title: string;
  description: string;
  event_type: 'course' | 'exam' | 'meeting' | 'reminder';
  start_time: string;
  end_time: string;
  location: string;
  subject: string;
  color: string;
  is_recurring: boolean;
  recurrence_pattern: any;
  class_name: string;
}

interface Class {
  id: number;
  name: string;
  subject: string;
}

export default function TeacherCalendar() {
  const { user, token } = useAuth();
  const [events, setEvents] = useState<CalendarEvent[]>([]);
  const [classes, setClasses] = useState<Class[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [selectedEvent, setSelectedEvent] = useState<CalendarEvent | null>(null);
  const [filterType, setFilterType] = useState<string>('all');
  const [filterClass, setFilterClass] = useState<string>('all');

  // Formulaire de création/édition
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    event_type: 'course',
    start_time: '',
    end_time: '',
    location: '',
    subject: '',
    class_id: '',
    color: '#3B82F6',
    is_recurring: false,
    recurrence_pattern: null
  });

  useEffect(() => {
    if (token) {
      fetchEvents();
      fetchClasses();
    }
  }, [token, selectedDate, filterType, filterClass]);

  const fetchEvents = async () => {
    try {
      setLoading(true);
      const startDate = selectedDate.toISOString().split('T')[0];
      const endDate = new Date(selectedDate.getTime() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
      
      let url = `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/calendar/events?start_date=${startDate}&end_date=${endDate}`;
      
      if (filterType !== 'all') {
        url += `&event_type=${filterType}`;
      }
      if (filterClass !== 'all') {
        url += `&class_id=${filterClass}`;
      }

      const response = await fetch(url, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setEvents(data);
      } else {
        setError('Erreur lors du chargement des événements');
      }
    } catch (err) {
      setError('Erreur de connexion');
    } finally {
      setLoading(false);
    }
  };

  const fetchClasses = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/classes/`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setClasses(data);
      }
    } catch (err) {
      console.error('Erreur lors du chargement des classes:', err);
    }
  };

  const createEvent = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/calendar/events`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          ...formData,
          class_id: formData.class_id ? parseInt(formData.class_id) : null
        })
      });

      if (response.ok) {
        setShowCreateModal(false);
        setFormData({
          title: '',
          description: '',
          event_type: 'course',
          start_time: '',
          end_time: '',
          location: '',
          subject: '',
          class_id: '',
          color: '#3B82F6',
          is_recurring: false,
          recurrence_pattern: null
        });
        fetchEvents();
      } else {
        setError('Erreur lors de la création de l\'événement');
      }
    } catch (err) {
      setError('Erreur de connexion');
    }
  };

  const updateEvent = async () => {
    if (!selectedEvent) return;

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/calendar/events/${selectedEvent.id}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          ...formData,
          class_id: formData.class_id ? parseInt(formData.class_id) : null
        })
      });

      if (response.ok) {
        setShowEditModal(false);
        setSelectedEvent(null);
        fetchEvents();
      } else {
        setError('Erreur lors de la mise à jour de l\'événement');
      }
    } catch (err) {
      setError('Erreur de connexion');
    }
  };

  const deleteEvent = async (eventId: number) => {
    if (!confirm('Êtes-vous sûr de vouloir supprimer cet événement ?')) return;

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/calendar/events/${eventId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        fetchEvents();
      } else {
        setError('Erreur lors de la suppression de l\'événement');
      }
    } catch (err) {
      setError('Erreur de connexion');
    }
  };

  const handleEdit = (event: CalendarEvent) => {
    setSelectedEvent(event);
    setFormData({
      title: event.title,
      description: event.description,
      event_type: event.event_type,
      start_time: event.start_time,
      end_time: event.end_time,
      location: event.location || '',
      subject: event.subject || '',
      class_id: event.class_name || '',
      color: event.color,
      is_recurring: event.is_recurring,
      recurrence_pattern: event.recurrence_pattern
    });
    setShowEditModal(true);
  };

  const getEventIcon = (eventType: string) => {
    switch (eventType) {
      case 'course': return <BookOpen size={16} />;
      case 'exam': return <AlertCircle size={16} />;
      case 'meeting': return <Users size={16} />;
      case 'reminder': return <Clock size={16} />;
      default: return <Calendar size={16} />;
    }
  };

  const getEventTypeColor = (eventType: string) => {
    switch (eventType) {
      case 'course': return 'bg-blue-100 text-blue-800';
      case 'exam': return 'bg-red-100 text-red-800';
      case 'meeting': return 'bg-green-100 text-green-800';
      case 'reminder': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="flex min-h-screen bg-gray-50">
        <Sidebar userType="teacher" />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-blue-600 animate-pulse text-xl font-bold">Chargement du calendrier...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar userType="teacher" />
      <div className="flex-1 overflow-auto pl-0 md:pl-56">
        <div className="p-6">
          {/* Header */}
          <div className="mb-6 flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-800 mb-2">Calendrier</h1>
              <p className="text-gray-600">Gérez votre planning et vos événements</p>
            </div>
            <button
              onClick={() => setShowCreateModal(true)}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
            >
              <Plus size={16} />
              Nouvel événement
            </button>
          </div>

          {/* Filtres */}
          <div className="mb-6 flex gap-4">
            <div className="flex items-center gap-2">
              <Filter size={16} />
              <select
                value={filterType}
                onChange={(e) => setFilterType(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="all">Tous les types</option>
                <option value="course">Cours</option>
                <option value="exam">Examen</option>
                <option value="meeting">Réunion</option>
                <option value="reminder">Rappel</option>
              </select>
            </div>
            <div className="flex items-center gap-2">
              <Users size={16} />
              <select
                value={filterClass}
                onChange={(e) => setFilterClass(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="all">Toutes les classes</option>
                {classes.map((cls) => (
                  <option key={cls.id} value={cls.id}>{cls.name}</option>
                ))}
              </select>
            </div>
          </div>

          {/* Calendrier */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {events.map((event) => (
                <div
                  key={event.id}
                  className="border rounded-lg p-4 hover:shadow-md transition"
                  style={{ borderLeftColor: event.color, borderLeftWidth: '4px' }}
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center gap-2">
                      {getEventIcon(event.event_type)}
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getEventTypeColor(event.event_type)}`}>
                        {event.event_type}
                      </span>
                    </div>
                    <div className="flex gap-1">
                      <button
                        onClick={() => handleEdit(event)}
                        className="p-1 text-gray-400 hover:text-blue-600"
                      >
                        <Edit size={14} />
                      </button>
                      <button
                        onClick={() => deleteEvent(event.id)}
                        className="p-1 text-gray-400 hover:text-red-600"
                      >
                        <Trash2 size={14} />
                      </button>
                    </div>
                  </div>
                  
                  <h3 className="font-semibold text-gray-800 mb-2">{event.title}</h3>
                  {event.description && (
                    <p className="text-sm text-gray-600 mb-2">{event.description}</p>
                  )}
                  
                  <div className="space-y-1 text-sm text-gray-500">
                    <div className="flex items-center gap-2">
                      <Clock size={14} />
                      <span>
                        {new Date(event.start_time).toLocaleDateString()} {new Date(event.start_time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                      </span>
                    </div>
                    {event.location && (
                      <div className="flex items-center gap-2">
                        <MapPin size={14} />
                        <span>{event.location}</span>
                      </div>
                    )}
                    {event.subject && (
                      <div className="flex items-center gap-2">
                        <BookOpen size={14} />
                        <span>{event.subject}</span>
                      </div>
                    )}
                    {event.class_name && (
                      <div className="flex items-center gap-2">
                        <Users size={14} />
                        <span>{event.class_name}</span>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>

            {events.length === 0 && (
              <div className="text-center py-12">
                <Calendar className="mx-auto text-gray-400 mb-4" size={48} />
                <p className="text-gray-600">Aucun événement trouvé</p>
                <p className="text-sm text-gray-500">Créez votre premier événement pour commencer</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Modal de création */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-bold mb-4">Nouvel événement</h2>
            <form onSubmit={(e) => { e.preventDefault(); createEvent(); }}>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Titre</label>
                  <input
                    type="text"
                    value={formData.title}
                    onChange={(e) => setFormData({...formData, title: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                  <textarea
                    value={formData.description}
                    onChange={(e) => setFormData({...formData, description: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    rows={3}
                  />
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Type</label>
                    <select
                      value={formData.event_type}
                      onChange={(e) => setFormData({...formData, event_type: e.target.value as any})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="course">Cours</option>
                      <option value="exam">Examen</option>
                      <option value="meeting">Réunion</option>
                      <option value="reminder">Rappel</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Classe</label>
                    <select
                      value={formData.class_id}
                      onChange={(e) => setFormData({...formData, class_id: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="">Aucune classe</option>
                      {classes.map((cls) => (
                        <option key={cls.id} value={cls.id}>{cls.name}</option>
                      ))}
                    </select>
                  </div>
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Début</label>
                    <input
                      type="datetime-local"
                      value={formData.start_time}
                      onChange={(e) => setFormData({...formData, start_time: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Fin</label>
                    <input
                      type="datetime-local"
                      value={formData.end_time}
                      onChange={(e) => setFormData({...formData, end_time: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    />
                  </div>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Lieu</label>
                  <input
                    type="text"
                    value={formData.location}
                    onChange={(e) => setFormData({...formData, location: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Matière</label>
                  <input
                    type="text"
                    value={formData.subject}
                    onChange={(e) => setFormData({...formData, subject: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
              
              <div className="flex gap-3 mt-6">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50"
                >
                  Annuler
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  Créer
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal d'édition */}
      {showEditModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-bold mb-4">Modifier l'événement</h2>
            <form onSubmit={(e) => { e.preventDefault(); updateEvent(); }}>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Titre</label>
                  <input
                    type="text"
                    value={formData.title}
                    onChange={(e) => setFormData({...formData, title: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                  <textarea
                    value={formData.description}
                    onChange={(e) => setFormData({...formData, description: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    rows={3}
                  />
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Type</label>
                    <select
                      value={formData.event_type}
                      onChange={(e) => setFormData({...formData, event_type: e.target.value as any})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="course">Cours</option>
                      <option value="exam">Examen</option>
                      <option value="meeting">Réunion</option>
                      <option value="reminder">Rappel</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Classe</label>
                    <select
                      value={formData.class_id}
                      onChange={(e) => setFormData({...formData, class_id: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="">Aucune classe</option>
                      {classes.map((cls) => (
                        <option key={cls.id} value={cls.id}>{cls.name}</option>
                      ))}
                    </select>
                  </div>
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Début</label>
                    <input
                      type="datetime-local"
                      value={formData.start_time}
                      onChange={(e) => setFormData({...formData, start_time: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Fin</label>
                    <input
                      type="datetime-local"
                      value={formData.end_time}
                      onChange={(e) => setFormData({...formData, end_time: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    />
                  </div>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Lieu</label>
                  <input
                    type="text"
                    value={formData.location}
                    onChange={(e) => setFormData({...formData, location: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Matière</label>
                  <input
                    type="text"
                    value={formData.subject}
                    onChange={(e) => setFormData({...formData, subject: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
              
              <div className="flex gap-3 mt-6">
                <button
                  type="button"
                  onClick={() => setShowEditModal(false)}
                  className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50"
                >
                  Annuler
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  Mettre à jour
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
} 