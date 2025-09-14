'use client';

import React, { useState, useEffect } from 'react';
import { X } from 'lucide-react';
import { organizationAPI } from '../../api/student/organization';

interface LearningGoalModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
  goal?: any | null; // Si fourni, c'est pour modifier, sinon pour créer
}

interface LearningGoalData {
  title: string;
  description: string;
  subject: string;
  target_date: string;
}

export default function LearningGoalModal({ isOpen, onClose, onSuccess, goal }: LearningGoalModalProps) {
  const [formData, setFormData] = useState<LearningGoalData>({
    title: '',
    description: '',
    subject: '',
    target_date: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const subjects = [
    'Mathématiques', 'Français', 'Histoire', 'Géographie', 
    'Sciences', 'Physique', 'Chimie', 'Biologie', 
    'Anglais', 'Espagnol', 'Allemand', 'Philosophie',
    'Économie', 'Informatique', 'Art', 'Musique', 'Sport'
  ];

  // Initialiser le formulaire avec les données de l'objectif si on modifie
  useEffect(() => {
    if (goal) {
      setFormData({
        title: goal.title,
        description: goal.description,
        subject: goal.subject,
        target_date: goal.target_date ? goal.target_date.slice(0, 16) : '' // Format datetime-local
      });
    } else {
      setFormData({
        title: '',
        description: '',
        subject: '',
        target_date: ''
      });
    }
    setError(null);
  }, [goal, isOpen]);

  const handleInputChange = (field: keyof LearningGoalData, value: any) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      if (goal) {
        // Modification
        const updateData = {
          title: formData.title,
          description: formData.description,
          subject: formData.subject,
          target_date: formData.target_date || undefined
        };
        await organizationAPI.updateLearningGoal(goal.id, updateData);
      } else {
        // Création
        await organizationAPI.createLearningGoal(formData);
      }
      
      onSuccess();
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur lors de la sauvegarde de l\'objectif');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-semibold text-gray-900">
            {goal ? 'Modifier l\'Objectif' : 'Nouvel Objectif d\'Apprentissage'}
          </h2>
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
              Titre de l'objectif *
            </label>
            <input
              type="text"
              value={formData.title}
              onChange={(e) => handleInputChange('title', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Ex: Maîtriser les équations du second degré"
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
              placeholder="Décrivez votre objectif d'apprentissage..."
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

          {/* Date cible */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Date cible (optionnel)
            </label>
            <input
              type="datetime-local"
              value={formData.target_date}
              onChange={(e) => handleInputChange('target_date', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
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
              {loading ? 'Sauvegarde...' : (goal ? 'Modifier' : 'Créer')}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
} 