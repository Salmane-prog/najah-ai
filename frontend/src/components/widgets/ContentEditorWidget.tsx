"use client";

import React, { useState, useEffect } from 'react';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface Content {
  id?: number;
  title: string;
  description: string;
  content_type: string;
  subject: string;
  difficulty: string;
  category_id?: number;
}

interface Category {
  id: number;
  name: string;
  description: string;
}

interface ContentEditorProps {
  content?: Content;
  onSave: () => void;
  onCancel: () => void;
}

export default function ContentEditorWidget({ content, onSave, onCancel }: ContentEditorProps) {
  const [formData, setFormData] = useState<Content>({
    title: content?.title || '',
    description: content?.description || '',
    content_type: content?.content_type || 'quiz',
    subject: content?.subject || '',
    difficulty: content?.difficulty || 'easy',
    category_id: content?.category_id
  });
  
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchCategories();
  }, []);

  const fetchCategories = async () => {
    try {
      const token = typeof window !== "undefined" ? localStorage.getItem("najah_token") : null;
      const headers: Record<string, string> = {};
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(`${API_BASE_URL}/api/v1/categories/`, { headers });
      if (response.ok) {
        const data = await response.json();
        setCategories(Array.isArray(data) ? data : []);
      }
    } catch (err) {
      console.error('Erreur lors du chargement des catégories:', err);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const token = typeof window !== "undefined" ? localStorage.getItem("najah_token") : null;
      const headers: Record<string, string> = {
        'Content-Type': 'application/json'
      };
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const url = content?.id 
        ? `${API_BASE_URL}/api/v1/contents/${content.id}`
        : `${API_BASE_URL}/api/v1/contents/`;
      
      const method = content?.id ? 'PUT' : 'POST';

      const response = await fetch(url, {
        method,
        headers,
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        throw new Error('Erreur lors de la sauvegarde du contenu');
      }

      onSave();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur inconnue');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl shadow-2xl p-8 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-800">
            {content?.id ? 'Modifier le contenu' : 'Nouveau contenu'}
          </h2>
          <button
            onClick={onCancel}
            className="text-gray-400 hover:text-gray-600 text-2xl font-bold"
          >
            ×
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Titre */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Titre *
            </label>
            <input
              type="text"
              name="title"
              value={formData.title}
              onChange={handleChange}
              required
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Titre du contenu"
            />
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Description *
            </label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              required
              rows={3}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Description du contenu"
            />
          </div>

          {/* Type de contenu */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Type de contenu *
            </label>
            <select
              name="content_type"
              value={formData.content_type}
              onChange={handleChange}
              required
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="quiz">Quiz</option>
              <option value="cours">Cours</option>
              <option value="exercice">Exercice</option>
              <option value="video">Vidéo</option>
            </select>
          </div>

          {/* Matière */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Matière *
            </label>
            <input
              type="text"
              name="subject"
              value={formData.subject}
              onChange={handleChange}
              required
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Ex: Littérature, Mathématiques, Sciences"
            />
          </div>

          {/* Difficulté */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Niveau de difficulté *
            </label>
            <select
              name="difficulty"
              value={formData.difficulty}
              onChange={handleChange}
              required
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="easy">Facile</option>
              <option value="medium">Moyen</option>
              <option value="hard">Difficile</option>
            </select>
          </div>

          {/* Catégorie */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Catégorie
            </label>
            <select
              name="category_id"
              value={formData.category_id || ''}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Sélectionner une catégorie</option>
              {categories.map(category => (
                <option key={category.id} value={category.id}>
                  {category.name}
                </option>
              ))}
            </select>
          </div>

          {/* Messages d'erreur */}
          {error && (
            <div className="text-red-600 text-sm bg-red-50 p-3 rounded-lg">
              {error}
            </div>
          )}

          {/* Boutons */}
          <div className="flex justify-end space-x-4 pt-4">
            <button
              type="button"
              onClick={onCancel}
              disabled={loading}
              className="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition disabled:opacity-50"
            >
              Annuler
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
            >
              {loading ? 'Sauvegarde...' : (content?.id ? 'Modifier' : 'Créer')}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
} 