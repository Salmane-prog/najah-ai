'use client';

import React, { useState, useEffect } from 'react';
import Sidebar from '../../../../components/Sidebar';
import { useAuth  } from '../../../../hooks/useAuth';
import { BookOpen, Search, Filter, Plus, Edit, Trash2, Eye, Download, Share2, FileText, Video, Image, File, User } from 'lucide-react';
import { apiClient } from '../../../../utils/api';

interface Content {
  id: number;
  title: string;
  description: string;
  content_type: 'text' | 'video' | 'pdf' | 'image';
  content: string;
  subject: string;
  tags: string[];
  learning_objectives: string[];
  created_at: string;
  updated_at: string;
  views: number;
  downloads: number;
  is_active: boolean;
  created_by: {
    id: number;
    name: string;
    email: string;
  };
  usage_stats: {
    total_views: number;
    completion_rate: number;
    average_time_spent: number;
    student_count: number;
  };
}

export default function TeacherContent() {
  const { user, token } = useAuth();
  const [contents, setContents] = useState<Content[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState<string>('all');
  const [filterSubject, setFilterSubject] = useState<string>('all');
  const [sortBy, setSortBy] = useState<'title' | 'created' | 'views' | 'type'>('created');
  const [selectedContent, setSelectedContent] = useState<Content | null>(null);
  const [showContentModal, setShowContentModal] = useState(false);
  const [showViewModal, setShowViewModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showShareModal, setShowShareModal] = useState(false);

  useEffect(() => {
    if (token) {
      fetchContents();
    }
  }, [token]);

  const fetchContents = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get('/api/v1/contents/');
      setContents(response.data);
    } catch (err) {
      console.error('Erreur de connexion:', err);
      setError('Erreur de connexion');
    } finally {
      setLoading(false);
    }
  };

  const deleteContent = async (contentId: number) => {
    if (!confirm('Êtes-vous sûr de vouloir supprimer ce contenu ?')) return;

    try {
      await apiClient.delete(`/api/v1/contents/${contentId}`);
      fetchContents();
    } catch (err) {
      setError('Erreur de connexion');
    }
  };

  const handleEdit = (content: Content) => {
    setSelectedContent(content);
    setShowEditModal(true);
    setShowViewModal(false);
  };

  const handleShare = (content: Content) => {
    setSelectedContent(content);
    setShowShareModal(true);
    setShowViewModal(false);
  };

  const getContentIcon = (type: string) => {
    switch (type) {
      case 'text': return <FileText className="text-blue-600" size={20} />;
      case 'video': return <Video className="text-red-600" size={20} />;
      case 'pdf': return <File className="text-orange-600" size={20} />;
      case 'image': return <Image className="text-green-600" size={20} />;
      default: return <FileText className="text-gray-600" size={20} />;
    }
  };

  const getContentTypeLabel = (type: string) => {
    switch (type) {
      case 'text': return 'Texte';
      case 'video': return 'Vidéo';
      case 'pdf': return 'PDF';
      case 'image': return 'Image';
      default: return type;
    }
  };

  const filteredAndSortedContents = contents
    .filter(content => {
          const matchesSearch = (content.title || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
                         (content.description || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
                         (content.subject || '').toLowerCase().includes(searchTerm.toLowerCase());
      const matchesType = filterType === 'all' || content.content_type === filterType;
              const matchesSubject = filterSubject === 'all' || (content.subject || '') === filterSubject;
      return matchesSearch && matchesType && matchesSubject;
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'title':
          return (a.title || '').localeCompare(b.title || '');
        case 'created':
          return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
        case 'views':
          return (b.usage_stats?.total_views ?? 0) - (a.usage_stats?.total_views ?? 0);
        case 'type':
          return (a.content_type || '').localeCompare(b.content_type || '');
        default:
          return 0;
      }
    });

  const handleContentClick = (content: Content) => {
    setSelectedContent(content);
    setShowViewModal(true);
  };

  if (loading) {
    return (
      <div className="flex min-h-screen bg-gray-50">
        <Sidebar userType="teacher" />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-blue-600 animate-pulse text-xl font-bold">Chargement du contenu...</div>
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
          <div className="mb-6">
            <h1 className="text-3xl font-bold text-gray-800 mb-2">Contenu</h1>
            <p className="text-gray-600">Gérez vos ressources pédagogiques</p>
          </div>

          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-800">{error}</p>
            </div>
          )}

                     {/* Actions */}
           <div className="mb-6 flex flex-wrap items-center justify-between gap-4">
             <div className="flex items-center gap-4">
               <div className="relative">
                 <Search className="absolute left-3 top-2.5 text-gray-400" size={16} />
                 <input
                   type="text"
                   placeholder="Rechercher du contenu..."
                   value={searchTerm}
                   onChange={(e) => setSearchTerm(e.target.value)}
                   className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                 />
               </div>
               
               <a
                 href="/dashboard/teacher/content/sharing-history"
                 className="flex items-center gap-2 px-4 py-2 text-blue-600 hover:text-blue-800 border border-blue-300 rounded-lg hover:bg-blue-50"
               >
                 <Share2 size={16} />
                 Historique des partages
               </a>

              <div className="flex items-center gap-2">
                <Filter className="text-gray-600" size={16} />
                <select
                  value={filterType}
                  onChange={(e) => setFilterType(e.target.value)}
                  className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="all">Tous les types</option>
                  <option value="text">Texte</option>
                  <option value="video">Vidéo</option>
                  <option value="pdf">PDF</option>
                  <option value="image">Image</option>
                </select>
              </div>

              <div className="flex items-center gap-2">
                <select
                  value={filterSubject}
                  onChange={(e) => setFilterSubject(e.target.value)}
                  className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="all">Toutes les matières</option>
                  <option value="Français">Français</option>
                  <option value="Mathématiques">Mathématiques</option>
                  <option value="Histoire">Histoire</option>
                  <option value="Sciences">Sciences</option>
                </select>
              </div>

              <div className="flex items-center gap-2">
                <span className="text-sm text-gray-600">Trier par:</span>
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value as any)}
                  className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="created">Date de création</option>
                  <option value="title">Titre</option>
                  <option value="views">Vues</option>
                  <option value="type">Type</option>
                </select>
              </div>
            </div>

            <button
              onClick={() => setShowContentModal(true)}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              <Plus size={16} />
              Nouveau Contenu
            </button>
          </div>

          {/* Liste du contenu */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredAndSortedContents.map((content) => (
              <div
                key={content.id}
                onClick={() => handleContentClick(content)}
                className="bg-white rounded-xl shadow-lg p-6 cursor-pointer hover:shadow-xl transition-shadow"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    {getContentIcon(content.content_type)}
                    <div>
                      <h3 className="font-bold text-gray-800">{content.title || 'Titre non défini'}</h3>
                      <p className="text-sm text-gray-600">{content.subject || 'Matière non définie'}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        // Action de partage
                      }}
                      className="p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg"
                    >
                      <Share2 size={16} />
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        deleteContent(content.id);
                      }}
                      className="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg"
                    >
                      <Trash2 size={16} />
                    </button>
                  </div>
                </div>

                <div className="space-y-3">
                                      <p className="text-sm text-gray-600 line-clamp-2">{content.description || 'Aucune description'}</p>

                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Type</span>
                    <span className="text-sm font-medium text-gray-800">
                      {getContentTypeLabel(content.content_type)}
                    </span>
                  </div>

                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Vues</span>
                    <span className="font-medium text-gray-800">{content.usage_stats?.total_views ?? 0}</span>
                  </div>

                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Complétion</span>
                    <span className="font-medium text-gray-800">{content.usage_stats?.completion_rate ?? 0}%</span>
                  </div>

                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Créé le</span>
                    <span className="text-sm text-gray-600">
                      {new Date(content.created_at).toLocaleDateString('fr-FR')}
                    </span>
                  </div>

                  {/* Tags */}
                  {(content.tags || []).length > 0 && (
                    <div className="pt-3 border-t border-gray-200">
                      <div className="flex flex-wrap gap-1">
                        {(content.tags || []).slice(0, 3).map((tag, index) => (
                          <span
                            key={index}
                            className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs"
                          >
                            {tag}
                          </span>
                        ))}
                        {(content.tags || []).length > 3 && (
                          <span className="text-xs text-gray-500">
                            +{(content.tags || []).length - 3}
                          </span>
                        )}
                      </div>
                    </div>
                  )}

                  {/* Objectifs d'apprentissage */}
                  {(content.learning_objectives || []).length > 0 && (
                    <div className="pt-3 border-t border-gray-200">
                      <h4 className="text-sm font-medium text-gray-700 mb-2">Objectifs</h4>
                      <div className="space-y-1">
                        {(content.learning_objectives || []).slice(0, 2).map((objective, index) => (
                          <p key={index} className="text-xs text-gray-600 truncate">
                            • {objective}
                          </p>
                        ))}
                        {(content.learning_objectives || []).length > 2 && (
                          <p className="text-xs text-gray-500">
                            +{(content.learning_objectives || []).length - 2} autres objectifs
                          </p>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>

          {filteredAndSortedContents.length === 0 && (
            <div className="text-center py-12">
              <BookOpen className="mx-auto text-gray-400 mb-4" size={48} />
              <p className="text-gray-600">Aucun contenu trouvé</p>
              <p className="text-sm text-gray-500">Créez votre premier contenu pour commencer</p>
            </div>
          )}

                     {/* Modal de détails du contenu */}
           {showViewModal && selectedContent && (
            <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
              <div className="bg-white rounded-xl p-6 w-full max-w-4xl max-h-[90vh] overflow-y-auto">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-xl font-bold text-gray-800">Détails du Contenu</h3>
                                     <button
                     onClick={() => setShowViewModal(false)}
                     className="text-gray-400 hover:text-gray-600"
                   >
                     ✕
                   </button>
                </div>

                <div className="space-y-6">
                  {/* En-tête */}
                  <div className="flex items-start gap-4">
                    <div className="w-16 h-16 bg-blue-100 rounded-lg flex items-center justify-center">
                      {getContentIcon(selectedContent.content_type)}
                    </div>
                    <div className="flex-1">
                      <h4 className="text-lg font-bold text-gray-800">{selectedContent.title || 'Titre non défini'}</h4>
                      <p className="text-gray-600">{selectedContent.subject || 'Matière non définie'}</p>
                                              <p className="text-sm text-gray-500">
                          Créé par {selectedContent.created_by?.name || 'Utilisateur inconnu'} le {selectedContent.created_at ? new Date(selectedContent.created_at).toLocaleDateString('fr-FR') : 'Date inconnue'}
                        </p>
                    </div>
                  </div>

                  {/* Statistiques */}
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div className="bg-blue-50 p-4 rounded-lg">
                      <div className="flex items-center gap-2 mb-2">
                        <Eye className="text-blue-600" size={16} />
                        <span className="text-sm font-medium text-blue-800">Vues totales</span>
                      </div>
                      <p className="text-2xl font-bold text-blue-800">
                        {selectedContent.usage_stats?.total_views ?? 0}
                      </p>
                    </div>

                    <div className="bg-green-50 p-4 rounded-lg">
                      <div className="flex items-center gap-2 mb-2">
                        <BookOpen className="text-green-600" size={16} />
                        <span className="text-sm font-medium text-green-800">Taux de complétion</span>
                      </div>
                      <p className="text-2xl font-bold text-green-800">
                        {selectedContent.usage_stats?.completion_rate ?? 0}%
                      </p>
                    </div>

                    <div className="bg-purple-50 p-4 rounded-lg">
                      <div className="flex items-center gap-2 mb-2">
                        <Download className="text-purple-600" size={16} />
                        <span className="text-sm font-medium text-purple-800">Téléchargements</span>
                      </div>
                      <p className="text-2xl font-bold text-purple-800">
                        {selectedContent.downloads ?? 0}
                      </p>
                    </div>

                    <div className="bg-orange-50 p-4 rounded-lg">
                      <div className="flex items-center gap-2 mb-2">
                        <User className="text-orange-600" size={16} />
                        <span className="text-sm font-medium text-orange-800">Élèves</span>
                      </div>
                      <p className="text-2xl font-bold text-orange-800">
                        {selectedContent.usage_stats?.student_count ?? 0}
                      </p>
                    </div>
                  </div>

                  {/* Description */}
                  <div>
                    <h5 className="font-semibold text-gray-800 mb-2">Description</h5>
                    <p className="text-gray-700">{selectedContent.description || 'Aucune description'}</p>
                  </div>

                  {/* Contenu */}
                  <div>
                    <h5 className="font-semibold text-gray-800 mb-2">Contenu</h5>
                    {selectedContent.content_type === 'text' ? (
                      <div className="bg-gray-50 p-4 rounded-lg">
                        <p className="text-gray-700 whitespace-pre-wrap">{selectedContent.content}</p>
                      </div>
                    ) : (
                      <div className="bg-gray-50 p-4 rounded-lg text-center">
                        <p className="text-gray-600">Fichier {getContentTypeLabel(selectedContent.content_type)}</p>
                        <button className="mt-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                          Télécharger
                        </button>
                      </div>
                    )}
                  </div>

                  {/* Tags */}
                  {(selectedContent.tags || []).length > 0 && (
                    <div>
                      <h5 className="font-semibold text-gray-800 mb-2">Tags</h5>
                      <div className="flex flex-wrap gap-2">
                        {(selectedContent.tags || []).map((tag, index) => (
                          <span
                            key={index}
                            className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
                          >
                            {tag}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Objectifs d'apprentissage */}
                  {(selectedContent.learning_objectives || []).length > 0 && (
                    <div>
                      <h5 className="font-semibold text-gray-800 mb-2">Objectifs d'apprentissage</h5>
                      <div className="space-y-2">
                        {(selectedContent.learning_objectives || []).map((objective, index) => (
                          <div key={index} className="flex items-start gap-2">
                            <div className="w-2 h-2 bg-green-500 rounded-full mt-2"></div>
                            <p className="text-gray-700">{objective}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                                     {/* Actions */}
                   <div className="flex justify-end gap-3 pt-4 border-t border-gray-200">
                     <button 
                       onClick={() => handleEdit(selectedContent)}
                       className="px-4 py-2 text-gray-600 hover:text-gray-800 border border-gray-300 rounded-lg hover:bg-gray-50"
                     >
                       Modifier
                     </button>
                     <button 
                       onClick={() => handleShare(selectedContent)}
                       className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                     >
                       Partager
                     </button>
                   </div>
                </div>
              </div>
            </div>
          )}

                     {/* Modal de création de contenu */}
           {showContentModal && !selectedContent && (
             <CreateContentModal
               onClose={() => setShowContentModal(false)}
               onCreated={() => {
                 setShowContentModal(false);
                 fetchContents();
               }}
             />
           )}

           {/* Modal d'édition de contenu */}
           {showEditModal && selectedContent && (
             <EditContentModal
               content={selectedContent}
               onClose={() => setShowEditModal(false)}
               onUpdated={() => {
                 setShowEditModal(false);
                 setSelectedContent(null);
                 fetchContents();
               }}
             />
           )}

           {/* Modal de partage de contenu */}
           {showShareModal && selectedContent && (
             <ShareContentModal
               content={selectedContent}
               onClose={() => setShowShareModal(false)}
               onShared={() => {
                 setShowShareModal(false);
                 setSelectedContent(null);
               }}
             />
           )}
        </div>
      </div>
    </div>
  );
}

// Composant Modal de création de contenu
interface CreateContentModalProps {
  onClose: () => void;
  onCreated: () => void;
}

function CreateContentModal({ onClose, onCreated }: CreateContentModalProps) {
  const [formData, setFormData] = useState({
    title: '',
    subject: '',
    description: '',
    content_type: 'text',
    content: '',
    level: 'middle', // Ajout du champ level manquant
    tags: '',
    learning_objectives: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/contents/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('najah_token')}`
        },
                 body: JSON.stringify({
           title: formData.title,
           subject: formData.subject,
           description: formData.description,
           content_type: formData.content_type,
           content: formData.content,
           level: formData.level,
           tags: formData.tags ? formData.tags.split(',').map(tag => tag.trim()) : [],
           learning_objectives: formData.learning_objectives ? formData.learning_objectives.split(',').map(obj => obj.trim()) : []
         })
      });

      if (response.ok) {
        onCreated();
      } else {
        const errorData = await response.json();
        setError(`Erreur lors de la création: ${errorData.detail || 'Erreur inconnue'}`);
      }
    } catch (err) {
      setError('Erreur de connexion au serveur');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white rounded-xl shadow-2xl p-8 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-800">Créer du Contenu</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 text-2xl font-bold"
          >
            ×
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Titre et Matière */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Titre *
              </label>
              <input
                type="text"
                required
                value={formData.title}
                onChange={(e) => setFormData({...formData, title: e.target.value})}
                placeholder="Titre du contenu"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Matière *
              </label>
              <input
                type="text"
                required
                value={formData.subject}
                onChange={(e) => setFormData({...formData, subject: e.target.value})}
                placeholder="Ex: Mathématiques"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Description
            </label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
              placeholder="Description du contenu..."
              rows={3}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

                     {/* Type de contenu et Niveau */}
           <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
             <div>
               <label className="block text-sm font-medium text-gray-700 mb-2">
                 Type de contenu *
               </label>
               <select
                 required
                 value={formData.content_type}
                 onChange={(e) => setFormData({...formData, content_type: e.target.value})}
                 className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
               >
                 <option value="text">Texte</option>
                 <option value="video">Vidéo</option>
                 <option value="pdf">PDF</option>
                 <option value="image">Image</option>
               </select>
             </div>
             <div>
               <label className="block text-sm font-medium text-gray-700 mb-2">
                 Niveau *
               </label>
               <select
                 required
                 value={formData.level}
                 onChange={(e) => setFormData({...formData, level: e.target.value})}
                 className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
               >
                 <option value="primary">Primaire</option>
                 <option value="middle">Collège</option>
                 <option value="high">Lycée</option>
                 <option value="university">Université</option>
               </select>
             </div>
           </div>

           {/* Contenu - Adaptatif selon le type */}
           <div>
             <label className="block text-sm font-medium text-gray-700 mb-2">
               {formData.content_type === 'text' ? 'Contenu *' : 'Fichier *'}
             </label>
             
             {formData.content_type === 'text' ? (
               // Zone de texte pour le contenu textuel
               <textarea
                 required
                 value={formData.content}
                 onChange={(e) => setFormData({...formData, content: e.target.value})}
                 placeholder="Votre contenu ici..."
                 rows={6}
                 className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
               />
             ) : (
               // Zone de drag & drop pour les fichiers
               <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-400 transition-colors">
                 <div className="space-y-4">
                   <div className="mx-auto w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center">
                     {formData.content_type === 'pdf' && <File className="text-red-500" size={24} />}
                     {formData.content_type === 'video' && <Video className="text-red-500" size={24} />}
                     {formData.content_type === 'image' && <Image className="text-green-500" size={24} />}
                   </div>
                   <div>
                     <p className="text-lg font-medium text-gray-700">
                       Glissez-déposez votre {formData.content_type === 'pdf' ? 'PDF' : formData.content_type === 'video' ? 'vidéo' : 'image'} ici
                     </p>
                     <p className="text-sm text-gray-500 mt-1">
                       ou cliquez pour sélectionner un fichier
                     </p>
                   </div>
                   <input
                     type="file"
                     accept={
                       formData.content_type === 'pdf' ? '.pdf' :
                       formData.content_type === 'video' ? '.mp4,.avi,.mov,.mkv' :
                       '.jpg,.jpeg,.png,.gif'
                     }
                     onChange={(e) => {
                       const file = e.target.files?.[0];
                       if (file) {
                         // Pour l'instant, on stocke le nom du fichier
                         // Plus tard, on pourra implémenter l'upload réel
                         setFormData({...formData, content: file.name});
                       }
                     }}
                     className="hidden"
                     id="file-upload"
                   />
                   <label
                     htmlFor="file-upload"
                     className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 cursor-pointer"
                   >
                     Sélectionner un fichier
                   </label>
                 </div>
               </div>
             )}
           </div>

          {/* Tags et Objectifs */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Tags
              </label>
              <input
                type="text"
                value={formData.tags}
                onChange={(e) => setFormData({...formData, tags: e.target.value})}
                placeholder="Ajouter un tag..."
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <p className="text-xs text-gray-500 mt-1">Séparez les tags par des virgules</p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Objectifs d'apprentissage
              </label>
              <input
                type="text"
                value={formData.learning_objectives}
                onChange={(e) => setFormData({...formData, learning_objectives: e.target.value})}
                placeholder="Ajouter un objectif..."
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <p className="text-xs text-gray-500 mt-1">Séparez les objectifs par des virgules</p>
            </div>
          </div>

          {/* Message d'erreur */}
          {error && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-800">{error}</p>
            </div>
          )}

          {/* Boutons d'action */}
          <div className="flex justify-end gap-3 pt-4 border-t border-gray-200">
            <button
              type="button"
              onClick={onClose}
              className="px-6 py-2 text-gray-600 hover:text-gray-800 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              Annuler
            </button>
            <button
              type="submit"
              disabled={loading}
              className="flex items-center gap-2 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              <FileText size={16} />
              {loading ? 'Création...' : 'Créer le Contenu'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
} 

// Composant Modal d'édition de contenu
interface EditContentModalProps {
  content: Content;
  onClose: () => void;
  onUpdated: () => void;
}

function EditContentModal({ content, onClose, onUpdated }: EditContentModalProps) {
  const [formData, setFormData] = useState({
    title: content.title || '',
    subject: content.subject || '',
    description: content.description || '',
    content_type: content.content_type || 'text',
    content: content.content || '',
    level: 'middle',
    tags: (content.tags || []).join(', '),
    learning_objectives: (content.learning_objectives || []).join(', ')
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/contents/${content.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('najah_token')}`
        },
        body: JSON.stringify({
          title: formData.title,
          subject: formData.subject,
          description: formData.description,
          content_type: formData.content_type,
          content: formData.content,
          level: formData.level,
          tags: formData.tags ? formData.tags.split(',').map(tag => tag.trim()) : [],
          learning_objectives: formData.learning_objectives ? formData.learning_objectives.split(',').map(obj => obj.trim()) : []
        })
      });

      if (response.ok) {
        onUpdated();
      } else {
        const errorData = await response.json();
        setError(`Erreur lors de la modification: ${errorData.detail || 'Erreur inconnue'}`);
      }
    } catch (err) {
      setError('Erreur de connexion au serveur');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white rounded-xl shadow-2xl p-8 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-800">Modifier le Contenu</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 text-2xl font-bold"
          >
            ×
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Titre et Matière */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Titre *
              </label>
              <input
                type="text"
                required
                value={formData.title}
                onChange={(e) => setFormData({...formData, title: e.target.value})}
                placeholder="Titre du contenu"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Matière *
              </label>
              <input
                type="text"
                required
                value={formData.subject}
                onChange={(e) => setFormData({...formData, subject: e.target.value})}
                placeholder="Ex: Mathématiques"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Description
            </label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
              placeholder="Description du contenu..."
              rows={3}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          {/* Type de contenu et Niveau */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Type de contenu *
              </label>
              <select
                required
                value={formData.content_type}
                onChange={(e) => setFormData({...formData, content_type: e.target.value})}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="text">Texte</option>
                <option value="video">Vidéo</option>
                <option value="pdf">PDF</option>
                <option value="image">Image</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Niveau *
              </label>
              <select
                required
                value={formData.level}
                onChange={(e) => setFormData({...formData, level: e.target.value})}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="primary">Primaire</option>
                <option value="middle">Collège</option>
                <option value="high">Lycée</option>
                <option value="university">Université</option>
              </select>
            </div>
          </div>

          {/* Contenu */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {formData.content_type === 'text' ? 'Contenu *' : 'Fichier *'}
            </label>
            
            {formData.content_type === 'text' ? (
              <textarea
                required
                value={formData.content}
                onChange={(e) => setFormData({...formData, content: e.target.value})}
                placeholder="Votre contenu ici..."
                rows={6}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            ) : (
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center">
                <p className="text-gray-600">Fichier actuel: {formData.content}</p>
                <p className="text-sm text-gray-500 mt-1">Modification du fichier non disponible pour l'instant</p>
              </div>
            )}
          </div>

          {/* Tags et Objectifs */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Tags
              </label>
              <input
                type="text"
                value={formData.tags}
                onChange={(e) => setFormData({...formData, tags: e.target.value})}
                placeholder="Ajouter un tag..."
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <p className="text-xs text-gray-500 mt-1">Séparez les tags par des virgules</p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Objectifs d'apprentissage
              </label>
              <input
                type="text"
                value={formData.learning_objectives}
                onChange={(e) => setFormData({...formData, learning_objectives: e.target.value})}
                placeholder="Ajouter un objectif..."
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <p className="text-xs text-gray-500 mt-1">Séparez les objectifs par des virgules</p>
            </div>
          </div>

          {/* Message d'erreur */}
          {error && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-800">{error}</p>
            </div>
          )}

          {/* Boutons d'action */}
          <div className="flex justify-end gap-3 pt-4 border-t border-gray-200">
            <button
              type="button"
              onClick={onClose}
              className="px-6 py-2 text-gray-600 hover:text-gray-800 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              Annuler
            </button>
            <button
              type="submit"
              disabled={loading}
              className="flex items-center gap-2 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              <Edit size={16} />
              {loading ? 'Modification...' : 'Modifier le Contenu'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
} 

// Composant Modal de partage de contenu avancé
interface ShareContentModalProps {
  content: Content;
  onClose: () => void;
  onShared: () => void;
}

function ShareContentModal({ content, onClose, onShared }: ShareContentModalProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  
  // États pour la configuration du partage
  const [targetType, setTargetType] = useState<'class' | 'student' | 'all_students'>('class');
  const [selectedClasses, setSelectedClasses] = useState<number[]>([]);
  const [selectedStudents, setSelectedStudents] = useState<number[]>([]);
  const [allowDownload, setAllowDownload] = useState(true);
  const [allowView, setAllowView] = useState(true);
  const [notifyStudents, setNotifyStudents] = useState(true);
  const [customMessage, setCustomMessage] = useState('');
  const [expirationDate, setExpirationDate] = useState('');
  
  // États pour les cibles disponibles
  const [availableTargets, setAvailableTargets] = useState<{
    classes: Array<{id: number, name: string, student_count: number}>;
    students: Array<{id: number, name: string}>;
    all_students_count: number;
  }>({ classes: [], students: [], all_students_count: 0 });
  
  const [loadingTargets, setLoadingTargets] = useState(true);

  // Charger les cibles disponibles
  useEffect(() => {
    const fetchTargets = async () => {
      try {
        setLoadingTargets(true);
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/content-sharing/targets`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('najah_token')}`
          }
        });
        
        if (response.ok) {
          const data = await response.json();
          setAvailableTargets(data);
        }
      } catch (err) {
        console.error('Erreur lors du chargement des cibles:', err);
      } finally {
        setLoadingTargets(false);
      }
    };
    
    fetchTargets();
  }, []);

  const handleShare = async () => {
    setLoading(true);
    setError(null);

    try {
      // Préparer les données de partage
      const sharingData = {
        content_id: content.id,
        target_type: targetType,
        target_ids: targetType === 'class' ? selectedClasses : 
                   targetType === 'student' ? selectedStudents : [],
        allow_download: allowDownload,
        allow_view: allowView,
        notify_students: notifyStudents,
        custom_message: customMessage || undefined,
        expiration_date: expirationDate ? new Date(expirationDate).toISOString() : undefined
      };

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/content-sharing/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('najah_token')}`
        },
        body: JSON.stringify(sharingData)
      });

      if (response.ok) {
        setSuccess(true);
        setTimeout(() => {
          onShared();
        }, 1500);
      } else {
        const errorData = await response.json();
        setError(`Erreur lors du partage: ${errorData.detail || 'Erreur inconnue'}`);
      }
    } catch (err) {
      setError('Erreur de connexion au serveur');
    } finally {
      setLoading(false);
    }
  };

  const getTargetCount = () => {
    switch (targetType) {
      case 'class':
        return selectedClasses.length;
      case 'student':
        return selectedStudents.length;
      case 'all_students':
        return availableTargets.all_students_count;
      default:
        return 0;
    }
  };

  const getTargetLabel = () => {
    switch (targetType) {
      case 'class':
        return 'classes';
      case 'student':
        return 'étudiants';
      case 'all_students':
        return 'tous les étudiants';
      default:
        return '';
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white rounded-xl shadow-2xl p-8 max-w-4xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-800">Partager le Contenu</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 text-2xl font-bold"
          >
            ×
          </button>
        </div>

        <div className="space-y-6">
          {/* Informations du contenu */}
          <div className="bg-gray-50 p-4 rounded-lg">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <FileText className="text-blue-600" size={20} />
              </div>
              <div>
                <h3 className="font-semibold text-gray-800">{content.title}</h3>
                <p className="text-sm text-gray-600">{content.subject} • {content.content_type}</p>
              </div>
            </div>
          </div>

          {/* Configuration du partage */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Type de cible */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Cibler *
              </label>
              <div className="space-y-3">
                <label className="flex items-center gap-3 cursor-pointer">
                  <input
                    type="radio"
                    name="targetType"
                    value="class"
                    checked={targetType === 'class'}
                    onChange={(e) => setTargetType(e.target.value as any)}
                    className="text-blue-600"
                  />
                  <span>Classes spécifiques</span>
                </label>
                
                <label className="flex items-center gap-3 cursor-pointer">
                  <input
                    type="radio"
                    name="targetType"
                    value="student"
                    checked={targetType === 'student'}
                    onChange={(e) => setTargetType(e.target.value as any)}
                    className="text-blue-600"
                  />
                  <span>Étudiants spécifiques</span>
                </label>
                
                <label className="flex items-center gap-3 cursor-pointer">
                  <input
                    type="radio"
                    name="targetType"
                    value="all_students"
                    checked={targetType === 'all_students'}
                    onChange={(e) => setTargetType(e.target.value as any)}
                    className="text-blue-600"
                  />
                  <span>Tous mes étudiants</span>
                </label>
              </div>
            </div>

            {/* Sélection des cibles */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Sélection ({getTargetCount()} {getTargetLabel()})
              </label>
              
              {loadingTargets ? (
                <div className="text-center py-4">
                  <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600 mx-auto"></div>
                </div>
              ) : (
                <div className="space-y-3">
                  {targetType === 'class' && (
                    <div className="max-h-32 overflow-y-auto space-y-2">
                      {availableTargets.classes.map((classItem) => (
                        <label key={classItem.id} className="flex items-center gap-2 cursor-pointer">
                          <input
                            type="checkbox"
                            checked={selectedClasses.includes(classItem.id)}
                            onChange={(e) => {
                              if (e.target.checked) {
                                setSelectedClasses([...selectedClasses, classItem.id]);
                              } else {
                                setSelectedClasses(selectedClasses.filter(id => id !== classItem.id));
                              }
                            }}
                            className="text-blue-600"
                          />
                          <span className="text-sm">{classItem.name} ({classItem.student_count} étudiants)</span>
                        </label>
                      ))}
                    </div>
                  )}
                  
                  {targetType === 'student' && (
                    <div className="max-h-32 overflow-y-auto space-y-2">
                      {availableTargets.students.map((student) => (
                        <label key={student.id} className="flex items-center gap-2 cursor-pointer">
                          <input
                            type="checkbox"
                            checked={selectedStudents.includes(student.id)}
                            onChange={(e) => {
                              if (e.target.checked) {
                                setSelectedStudents([...selectedStudents, student.id]);
                              } else {
                                setSelectedStudents(selectedStudents.filter(id => id !== student.id));
                              }
                            }}
                            className="text-blue-600"
                          />
                          <span className="text-sm">{student.name}</span>
                        </label>
                      ))}
                    </div>
                  )}
                  
                  {targetType === 'all_students' && (
                    <div className="text-sm text-gray-600 bg-blue-50 p-3 rounded-lg">
                      Le contenu sera partagé avec tous vos {availableTargets.all_students_count} étudiants
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>

          {/* Paramètres de partage */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Permissions
              </label>
              <div className="space-y-3">
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={allowView}
                    onChange={(e) => setAllowView(e.target.checked)}
                    className="text-blue-600"
                  />
                  <span>Autoriser la consultation</span>
                </label>
                
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={allowDownload}
                    onChange={(e) => setAllowDownload(e.target.checked)}
                    className="text-blue-600"
                  />
                  <span>Autoriser le téléchargement</span>
                </label>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Options avancées
              </label>
              <div className="space-y-3">
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={notifyStudents}
                    onChange={(e) => setNotifyStudents(e.target.checked)}
                    className="text-blue-600"
                  />
                  <span>Notifier les étudiants</span>
                </label>
                
                <div>
                  <label className="block text-xs text-gray-600 mb-1">
                    Date d'expiration (optionnel)
                  </label>
                  <input
                    type="datetime-local"
                    value={expirationDate}
                    onChange={(e) => setExpirationDate(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Message personnalisé */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Message personnalisé (optionnel)
            </label>
            <textarea
              value={customMessage}
              onChange={(e) => setCustomMessage(e.target.value)}
              placeholder="Ajoutez un message pour vos étudiants..."
              rows={3}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          {/* Résumé */}
          <div className="bg-blue-50 p-4 rounded-lg">
            <h4 className="font-medium text-blue-800 mb-2">Résumé du partage</h4>
            <div className="text-sm text-blue-700 space-y-1">
              <p>• Contenu : {content.title}</p>
              <p>• Cible : {getTargetCount()} {getTargetLabel()}</p>
              <p>• Permissions : {allowView ? 'Consultation' : ''} {allowView && allowDownload ? '• ' : ''} {allowDownload ? 'Téléchargement' : ''}</p>
              {expirationDate && <p>• Expire le : {new Date(expirationDate).toLocaleDateString('fr-FR')}</p>}
            </div>
          </div>

          {/* Message d'erreur */}
          {error && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-800">{error}</p>
            </div>
          )}

          {/* Message de succès */}
          {success && (
            <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
              <p className="text-green-800">Contenu partagé avec succès !</p>
            </div>
          )}

          {/* Boutons d'action */}
          <div className="flex justify-end gap-3 pt-4 border-t border-gray-200">
            <button
              type="button"
              onClick={onClose}
              className="px-6 py-2 text-gray-600 hover:text-gray-800 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              Annuler
            </button>
            <button
              onClick={handleShare}
              disabled={loading || success || (targetType === 'class' && selectedClasses.length === 0) || (targetType === 'student' && selectedStudents.length === 0)}
              className="flex items-center gap-2 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              <Share2 size={16} />
              {loading ? 'Partage...' : success ? 'Partagé !' : 'Partager le Contenu'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
} 