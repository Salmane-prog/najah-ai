'use client';

import React, { useState } from 'react';
import { X, Plus, Minus } from 'lucide-react';
import { organizationAPI } from '../../api/student/organization';

interface CreateStudySessionModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

interface StudySessionData {
  title: string;
  description: string;
  subject: string;
  start_time: string;
  end_time: string;
  duration: number;
  goals: string[];
  notes: string;
}

export default function CreateStudySessionModal({ isOpen, onClose, onSuccess }: CreateStudySessionModalProps) {
  const [formData, setFormData] = useState<StudySessionData>({
    title: '',
    description: '',
    subject: '',
    start_time: '',
    end_time: '',
    duration: 60,
    goals: [''],
    notes: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const subjects = [
    'Mathématiques', 'Français', 'Histoire', 'Géographie', 
    'Sciences', 'Physique', 'Chimie', 'Biologie', 
    'Anglais', 'Espagnol', 'Allemand', 'Philosophie',
    'Économie', 'Informatique', 'Art', 'Musique', 'Sport'
  ];

  const handleInputChange = (field: keyof StudySessionData, value: any) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleGoalChange = (index: number, value: string) => {
    const newGoals = [...formData.goals];
    newGoals[index] = value;
    setFormData(prev => ({
      ...prev,
      goals: newGoals
    }));
  };

  const addGoal = () => {
    setFormData(prev => ({
      ...prev,
      goals: [...prev.goals, '']
    }));
  };

  const removeGoal = (index: number) => {
    if (formData.goals.length > 1) {
      const newGoals = formData.goals.filter((_, i) => i !== index);
      setFormData(prev => ({
        ...prev,
        goals: newGoals
      }));
    }
  };

  const calculateDuration = () => {
    if (formData.start_time && formData.end_time) {
      const start = new Date(formData.start_time);
      const end = new Date(formData.end_time);
      const diffMs = end.getTime() - start.getTime();
      const diffMinutes = Math.round(diffMs / (1000 * 60));
      return Math.max(0, diffMinutes);
    }
    return 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Calculer la durée automatiquement
      const duration = calculateDuration();
      
      const sessionData = {
        ...formData,
        duration,
        goals: formData.goals.filter(goal => goal.trim() !== '')
      };

      await organizationAPI.createStudySession(sessionData);
      onSuccess();
      onClose();
      
      // Reset form
      setFormData({
        title: '',
        description: '',
        subject: '',
        start_time: '',
        end_time: '',
        duration: 60,
        goals: [''],
        notes: ''
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur lors de la création de la session');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-semibold text-gray-900">Nouvelle Session d'Étude</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
          >
            <X size={24} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}

          {/* Titre */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Titre de la session *
            </label>
            <input
              type="text"
              value={formData.title}
              onChange={(e) => handleInputChange('title', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Ex: Révision mathématiques"
              required
            />
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Description
            </label>
            <textarea
              value={formData.description}
              onChange={(e) => handleInputChange('description', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={3}
              placeholder="Décrivez ce que vous allez étudier..."
            />
          </div>

          {/* Matière */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Matière *
            </label>
            <select
              value={formData.subject}
              onChange={(e) => handleInputChange('subject', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            >
              <option value="">Sélectionner une matière</option>
              {subjects.map(subject => (
                <option key={subject} value={subject}>{subject}</option>
              ))}
            </select>
          </div>

          {/* Date et heure */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Heure de début *
              </label>
              <input
                type="datetime-local"
                value={formData.start_time}
                onChange={(e) => handleInputChange('start_time', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Heure de fin *
              </label>
              <input
                type="datetime-local"
                value={formData.end_time}
                onChange={(e) => handleInputChange('end_time', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
          </div>

          {/* Durée calculée */}
          {formData.start_time && formData.end_time && (
            <div className="bg-blue-50 border border-blue-200 text-blue-700 px-4 py-3 rounded">
              Durée calculée : {calculateDuration()} minutes
            </div>
          )}

          {/* Objectifs */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Objectifs d'apprentissage
            </label>
            {formData.goals.map((goal, index) => (
              <div key={index} className="flex items-center space-x-2 mb-2">
                <input
                  type="text"
                  value={goal}
                  onChange={(e) => handleGoalChange(index, e.target.value)}
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder={`Objectif ${index + 1}`}
                />
                <button
                  type="button"
                  onClick={() => removeGoal(index)}
                  className="p-2 text-red-500 hover:text-red-700"
                  disabled={formData.goals.length === 1}
                >
                  <Minus size={16} />
                </button>
              </div>
            ))}
            <button
              type="button"
              onClick={addGoal}
              className="flex items-center space-x-2 text-blue-600 hover:text-blue-700"
            >
              <Plus size={16} />
              <span>Ajouter un objectif</span>
            </button>
          </div>

          {/* Notes */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Notes (optionnel)
            </label>
            <textarea
              value={formData.notes}
              onChange={(e) => handleInputChange('notes', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={3}
              placeholder="Notes supplémentaires..."
            />
          </div>

          {/* Boutons */}
          <div className="flex justify-end space-x-4 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md transition-colors"
            >
              Annuler
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 transition-colors"
            >
              {loading ? 'Création...' : 'Créer la session'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
} 