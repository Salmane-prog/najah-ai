'use client';

import React, { useState, useEffect } from 'react';
import { X, Calendar, BookOpen, Target, Clock, Bell, Plus } from 'lucide-react';
import { organizationAPI } from '../api/student/organization';

interface CalendarEventFormProps {
  isOpen: boolean;
  onClose: () => void;
  onEventCreated: () => void;
  selectedDate?: Date;
}

interface EventFormData {
  title: string;
  description: string;
  event_type: 'homework' | 'study_session' | 'goal' | 'reminder';
  start_date: string;
  end_date: string;
  location: string;
  color: string;
  priority: 'low' | 'medium' | 'high';
  all_day: boolean;
}

export default function CalendarEventForm({ 
  isOpen, 
  onClose, 
  onEventCreated, 
  selectedDate 
}: CalendarEventFormProps) {
  const [formData, setFormData] = useState<EventFormData>({
    title: '',
    description: '',
    event_type: 'reminder',
    start_date: selectedDate ? selectedDate.toISOString().slice(0, 16) : new Date().toISOString().slice(0, 16),
    end_date: selectedDate ? selectedDate.toISOString().slice(0, 16) : new Date().toISOString().slice(0, 16),
    location: '',
    color: '#3B82F6',
    priority: 'medium',
    all_day: false
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Mettre à jour la date si selectedDate change
  useEffect(() => {
    if (selectedDate) {
      setFormData(prev => ({
        ...prev,
        start_date: selectedDate.toISOString().slice(0, 16),
        end_date: selectedDate.toISOString().slice(0, 16)
      }));
    }
  }, [selectedDate]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    
    if (type === 'checkbox') {
      const checked = (e.target as HTMLInputElement).checked;
      setFormData(prev => ({ ...prev, [name]: checked }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Créer l'événement dans le calendrier
      await organizationAPI.createCalendarEvent({
        title: formData.title,
        description: formData.description,
        event_type: formData.event_type,
        start_date: new Date(formData.start_date).toISOString(),
        end_date: formData.end_date ? new Date(formData.end_date).toISOString() : undefined,
        location: formData.location || undefined,
        color: formData.color,
        priority: formData.priority,
        all_day: formData.all_day
      });

      // Créer l'élément correspondant selon le type
      switch (formData.event_type) {
        case 'homework':
          // Pour les devoirs, on peut créer un devoir local
          console.log('Devoir créé localement');
          break;
        case 'study_session':
          // Créer une session d'étude
          await organizationAPI.createStudySession({
            title: formData.title,
            description: formData.description,
            subject: formData.location || 'Général',
            start_time: new Date(formData.start_date).toISOString(),
            end_time: formData.end_date ? new Date(formData.end_date).toISOString() : undefined,
            duration: formData.end_date && formData.start_date 
              ? Math.round((new Date(formData.end_date).getTime() - new Date(formData.start_date).getTime()) / (1000 * 60))
              : 60
          });
          break;
        case 'goal':
          // Créer un objectif d'apprentissage
          await organizationAPI.createLearningGoal({
            title: formData.title,
            description: formData.description,
            target_date: formData.end_date ? new Date(formData.end_date).toISOString() : undefined,
            priority: formData.priority,
            category: formData.location || 'Général'
          });
          break;
        case 'reminder':
          // Créer un rappel
          await organizationAPI.createReminder({
            title: formData.title,
            description: formData.description,
            reminder_time: new Date(formData.start_date).toISOString(),
            is_active: true
          });
          break;
      }

      onEventCreated();
      onClose();
      
      // Réinitialiser le formulaire
      setFormData({
        title: '',
        description: '',
        event_type: 'reminder',
        start_date: new Date().toISOString().slice(0, 16),
        end_date: new Date().toISOString().slice(0, 16),
        location: '',
        color: '#3B82F6',
        priority: 'medium',
        all_day: false
      });

    } catch (error) {
      console.error('Erreur lors de la création:', error);
      setError('Erreur lors de la création de l\'événement');
    } finally {
      setLoading(false);
    }
  };

  const getEventTypeIcon = (type: string) => {
    switch (type) {
      case 'homework': return <BookOpen className="w-5 h-5" />;
      case 'study_session': return <Clock className="w-5 h-5" />;
      case 'goal': return <Target className="w-5 h-5" />;
      case 'reminder': return <Bell className="w-5 h-5" />;
      default: return <Calendar className="w-5 h-5" />;
    }
  };

  const getEventTypeLabel = (type: string) => {
    switch (type) {
      case 'homework': return 'Devoir';
      case 'study_session': return 'Session d\'étude';
      case 'goal': return 'Objectif';
      case 'reminder': return 'Rappel';
      default: return 'Événement';
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-2xl mx-4 max-h-[90vh] overflow-y-auto">
        {/* En-tête */}
        <div className="flex items-center justify-between p-6 border-b">
          <div className="flex items-center space-x-3">
            <Calendar className="w-6 h-6 text-blue-600" />
            <h2 className="text-xl font-semibold text-gray-900">
              Ajouter un événement
            </h2>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Formulaire */}
        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {/* Type d'événement */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Type d'événement
            </label>
            <div className="grid grid-cols-2 gap-3">
              {(['homework', 'study_session', 'goal', 'reminder'] as const).map((type) => (
                <button
                  key={type}
                  type="button"
                  onClick={() => setFormData(prev => ({ ...prev, event_type: type }))}
                  className={`
                    flex items-center space-x-2 p-3 rounded-lg border-2 transition-all
                    ${formData.event_type === type 
                      ? 'border-blue-500 bg-blue-50 text-blue-700' 
                      : 'border-gray-200 hover:border-gray-300'
                    }
                  `}
                >
                  {getEventTypeIcon(type)}
                  <span className="font-medium">{getEventTypeLabel(type)}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Titre */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Titre *
            </label>
            <input
              type="text"
              name="title"
              value={formData.title}
              onChange={handleInputChange}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Titre de l'événement"
            />
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Description
            </label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Description de l'événement"
            />
          </div>

          {/* Dates */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Date et heure de début *
              </label>
              <input
                type="datetime-local"
                name="start_date"
                value={formData.start_date}
                onChange={handleInputChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Date et heure de fin
              </label>
              <input
                type="datetime-local"
                name="end_date"
                value={formData.end_date}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          {/* Options supplémentaires */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Couleur
              </label>
              <input
                type="color"
                name="color"
                value={formData.color}
                onChange={handleInputChange}
                className="w-full h-10 border border-gray-300 rounded-lg cursor-pointer"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Priorité
              </label>
              <select
                name="priority"
                value={formData.priority}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="low">Basse</option>
                <option value="medium">Moyenne</option>
                <option value="high">Haute</option>
              </select>
            </div>
            <div className="flex items-center space-x-2 pt-8">
              <input
                type="checkbox"
                name="all_day"
                checked={formData.all_day}
                onChange={handleInputChange}
                className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
              />
              <label className="text-sm font-medium text-gray-700">
                Toute la journée
              </label>
            </div>
          </div>

          {/* Localisation */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Localisation / Matière
            </label>
            <input
              type="text"
              name="location"
              value={formData.location}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder={formData.event_type === 'homework' ? 'Matière (ex: Mathématiques)' : 'Localisation'}
            />
          </div>

          {/* Message d'erreur */}
          {error && (
            <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-700">
              {error}
            </div>
          )}

          {/* Boutons d'action */}
          <div className="flex items-center justify-end space-x-3 pt-4 border-t">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
            >
              Annuler
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  <span>Création...</span>
                </>
              ) : (
                <>
                  <Plus className="w-4 h-4" />
                  <span>Créer l'événement</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
