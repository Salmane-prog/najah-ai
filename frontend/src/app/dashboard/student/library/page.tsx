'use client';

import React, { useState, useEffect } from 'react';
import Sidebar from '../../../../components/Sidebar';
import { useAuth  } from '../../../../hooks/useAuth';
import NotificationBell from '../../../../components/NotificationBell';
import { 
  Search, 
  Filter, 
  BookOpen, 
  Star, 
  Download, 
  Share2, 
  Eye, 
  Clock,
  User,
  Tag,
  Folder,
  Play,
  Pause,
  Volume2,
  FileText,
  Video,
  Image,
  Link,
  Heart,
  Bookmark,
  MoreVertical,
  Plus,
  Grid,
  List,
  SortAsc,
  SortDesc,
  Calendar,
  RefreshCw,
  Share
} from 'lucide-react';

interface Resource {
  id: number;
  title: string;
  description: string;
  type: 'video' | 'document' | 'image' | 'audio' | 'link' | 'interactive';
  subject: string;
  level: string;
  tags: string[];
  author: string;
  created_at: string;
  duration?: number; // en minutes pour les vidéos
  file_size?: string;
  views: number;
  rating: number;
  is_favorite: boolean;
  is_in_collection: boolean;
  collections: string[];
  url: string;
  thumbnail?: string;
  allow_download?: boolean;
}

interface Collection {
  id: number;
  name: string;
  description: string;
  resource_count: number;
  is_public: boolean;
  created_at: string;
  color: string;
}

interface Subject {
  id: number;
  name: string;
  color: string;
  resource_count: number;
}

interface Level {
  id: number;
  name: string;
  color: string;
  resource_count: number;
}

export default function LibraryPage() {
  const { user, token } = useAuth();
  const [resources, setResources] = useState<Resource[]>([]);
  const [collections, setCollections] = useState<Collection[]>([]);
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [levels, setLevels] = useState<Level[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedSubject, setSelectedSubject] = useState<number | null>(null);
  const [selectedLevel, setSelectedLevel] = useState<number | null>(null);
  const [selectedType, setSelectedType] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [sortBy, setSortBy] = useState<'recent' | 'popular' | 'rating' | 'title'>('recent');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  const [selectedResource, setSelectedResource] = useState<Resource | null>(null);
  const [loading, setLoading] = useState(true);
  const [showViewModal, setShowViewModal] = useState(false);
  const [showShareModal, setShowShareModal] = useState(false);

  // Données mockées
  const mockSubjects: Subject[] = [
    { id: 1, name: 'Mathématiques', color: 'bg-blue-500', resource_count: 45 },
    { id: 2, name: 'Sciences', color: 'bg-green-500', resource_count: 32 },
    { id: 3, name: 'Français', color: 'bg-purple-500', resource_count: 28 },
    { id: 4, name: 'Histoire', color: 'bg-orange-500', resource_count: 19 },
    { id: 5, name: 'Anglais', color: 'bg-red-500', resource_count: 23 },
  ];

  const mockLevels: Level[] = [
    { id: 1, name: 'Primaire', color: 'bg-yellow-500', resource_count: 67 },
    { id: 2, name: 'Collège', color: 'bg-blue-500', resource_count: 89 },
    { id: 3, name: 'Lycée', color: 'bg-green-500', resource_count: 76 },
    { id: 4, name: 'Université', color: 'bg-purple-500', resource_count: 45 },
  ];

  const mockCollections: Collection[] = [
    { id: 1, name: 'Mes Favoris', description: 'Ressources que j\'aime', resource_count: 12, is_public: false, created_at: '2024-01-01T00:00:00Z', color: 'bg-yellow-100' },
    { id: 2, name: 'Révision Examens', description: 'Ressources pour réviser', resource_count: 8, is_public: true, created_at: '2024-01-05T00:00:00Z', color: 'bg-blue-100' },
    { id: 3, name: 'Vidéos Tutoriels', description: 'Tutoriels vidéo', resource_count: 15, is_public: true, created_at: '2024-01-10T00:00:00Z', color: 'bg-green-100' },
  ];

  const mockResources: Resource[] = [
    {
      id: 1,
      title: 'Cours complet sur les équations du second degré',
      description: 'Vidéo explicative de 45 minutes couvrant tous les aspects des équations du second degré avec des exemples pratiques.',
      type: 'video',
      subject: 'Mathématiques',
      level: 'Lycée',
      tags: ['équations', 'second degré', 'discriminant', 'maths'],
      author: 'Prof. Martin',
      created_at: '2024-01-15T10:30:00Z',
      duration: 45,
      file_size: '125 MB',
      views: 1250,
      rating: 4.8,
      is_favorite: true,
      is_in_collection: true,
      collections: ['Mes Favoris', 'Révision Examens'],
      url: '/videos/equations-second-degre.mp4',
      thumbnail: '/thumbnails/equations.jpg'
    },
    {
      id: 2,
      title: 'Exercices corrigés - Photosynthèse',
      description: 'Document PDF avec 20 exercices corrigés sur le processus de photosynthèse.',
      type: 'document',
      subject: 'Sciences',
      level: 'Collège',
      tags: ['biologie', 'photosynthèse', 'exercices', 'corrigés'],
      author: 'Prof. Dubois',
      created_at: '2024-01-14T15:45:00Z',
      file_size: '2.3 MB',
      views: 890,
      rating: 4.6,
      is_favorite: false,
      is_in_collection: true,
      collections: ['Révision Examens'],
      url: '/documents/exercices-photosynthese.pdf'
    },
    {
      id: 3,
      title: 'Grammaire française - Les temps verbaux',
      description: 'Cours interactif sur les temps verbaux en français avec exercices pratiques.',
      type: 'interactive',
      subject: 'Français',
      level: 'Lycée',
      tags: ['grammaire', 'temps verbaux', 'français', 'interactif'],
      author: 'Prof. Laurent',
      created_at: '2024-01-13T09:20:00Z',
      duration: 30,
      views: 1560,
      rating: 4.9,
      is_favorite: true,
      is_in_collection: false,
      collections: [],
      url: '/interactive/grammaire-temps-verbaux'
    },
    {
      id: 4,
      title: 'Schéma de la Révolution française',
      description: 'Image interactive du schéma des événements de la Révolution française.',
      type: 'image',
      subject: 'Histoire',
      level: 'Collège',
      tags: ['révolution française', 'histoire', 'schéma', 'interactif'],
      author: 'Prof. Moreau',
      created_at: '2024-01-12T14:10:00Z',
      file_size: '1.8 MB',
      views: 720,
      rating: 4.4,
      is_favorite: false,
      is_in_collection: true,
      collections: ['Mes Favoris'],
      url: '/images/schema-revolution-francaise.jpg',
      thumbnail: '/thumbnails/revolution.jpg'
    },
    {
      id: 5,
      title: 'Podcast - Prononciation anglaise',
      description: 'Audio de 20 minutes sur la prononciation des sons difficiles en anglais.',
      type: 'audio',
      subject: 'Anglais',
      level: 'Lycée',
      tags: ['prononciation', 'anglais', 'audio', 'podcast'],
      author: 'Prof. Wilson',
      created_at: '2024-01-11T11:30:00Z',
      duration: 20,
      file_size: '15 MB',
      views: 430,
      rating: 4.7,
      is_favorite: true,
      is_in_collection: true,
      collections: ['Vidéos Tutoriels'],
      url: '/audio/prononciation-anglaise.mp3'
    },
    {
      id: 6,
      title: 'Lien vers Khan Academy - Algèbre',
      description: 'Ressource externe vers le cours d\'algèbre de Khan Academy.',
      type: 'link',
      subject: 'Mathématiques',
      level: 'Université',
      tags: ['algèbre', 'khan academy', 'externe'],
      author: 'Khan Academy',
      created_at: '2024-01-10T16:20:00Z',
      views: 2100,
      rating: 4.5,
      is_favorite: false,
      is_in_collection: false,
      collections: [],
      url: 'https://www.khanacademy.org/math/algebra'
    }
  ];

  useEffect(() => {
    fetchSharedContents();
    setSubjects(mockSubjects);
    setLevels(mockLevels);
    setCollections(mockCollections);
  }, []);

  const fetchSharedContents = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/v1/content-sharing/my-contents', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const sharedContents = await response.json();
        // Convertir les contenus partagés au format Resource
        const convertedResources: Resource[] = sharedContents.map((content: any) => ({
          id: content.content_id,
          title: content.content_title || 'Sans titre',
          description: content.custom_message || 'Contenu partagé par votre enseignant',
          type: mapContentTypeToResourceType(content.content_type),
          subject: content.content_subject || 'Général',
          level: 'Tous niveaux',
          tags: [content.content_type, content.content_subject].filter(Boolean),
          author: content.teacher_name || 'Enseignant',
          created_at: content.shared_at,
          views: content.view_count || 0,
          rating: 4.5, // Note par défaut
          is_favorite: false,
          is_in_collection: false,
          collections: [],
          url: `/content/${content.content_id}`,
          thumbnail: getThumbnailForType(content.content_type),
          allow_download: content.allow_download
        }));
        
        setResources(convertedResources);
      } else {
        console.error('Erreur lors de la récupération des contenus partagés');
        // En cas d'erreur, utiliser les données mockées
        setResources(mockResources);
      }
    } catch (error) {
      console.error('Erreur de connexion:', error);
      // En cas d'erreur, utiliser les données mockées
      setResources(mockResources);
    } finally {
      setLoading(false);
    }
  };

  const mapContentTypeToResourceType = (contentType: string): Resource['type'] => {
    switch (contentType?.toLowerCase()) {
      case 'video':
        return 'video';
      case 'pdf':
      case 'document':
        return 'document';
      case 'image':
        return 'image';
      case 'audio':
        return 'audio';
      case 'link':
        return 'link';
      default:
        return 'interactive';
    }
  };

  const getThumbnailForType = (contentType: string): string => {
    switch (contentType?.toLowerCase()) {
      case 'video':
        return '/thumbnails/video-default.jpg';
      case 'pdf':
      case 'document':
        return '/thumbnails/document-default.jpg';
      case 'image':
        return '/thumbnails/image-default.jpg';
      case 'audio':
        return '/thumbnails/audio-default.jpg';
      default:
        return '/thumbnails/default.jpg';
    }
  };

  // Fonctions de gestion des actions
  const handleViewContent = async (resource: Resource) => {
    try {
      // Mettre à jour le compteur de vues
      await fetch(`/api/v1/content-sharing/update-access`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content_id: resource.id,
          action: 'view'
        }),
      });
      
      setSelectedResource(resource);
      setShowViewModal(true);
      
      // Rafraîchir la liste pour mettre à jour les compteurs
      fetchSharedContents();
    } catch (error) {
      console.error('Erreur lors de la mise à jour des vues:', error);
      // Afficher quand même la modal même en cas d'erreur
      setSelectedResource(resource);
      setShowViewModal(true);
    }
  };

  const handleDownloadContent = async (resource: Resource) => {
    try {
      // Récupérer les informations de téléchargement
      const response = await fetch(`/api/v1/content-sharing/download/${resource.id}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const downloadInfo = await response.json();
        
        // Si le contenu a une URL de fichier, l'utiliser
        if (downloadInfo.file_url) {
          const link = document.createElement('a');
          link.href = downloadInfo.file_url;
          link.download = downloadInfo.title || resource.title;
          link.click();
        } else if (downloadInfo.content_data) {
          // Si le contenu est stocké directement, créer un blob
          const blob = new Blob([downloadInfo.content_data], { 
            type: getMimeType(downloadInfo.content_type) 
          });
          const url = URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = url;
          link.download = downloadInfo.title || resource.title;
          link.click();
          URL.revokeObjectURL(url);
        }
        
        // Rafraîchir la liste pour mettre à jour les compteurs
        fetchSharedContents();
      } else {
        console.error('Erreur lors du téléchargement:', response.statusText);
      }
    } catch (error) {
      console.error('Erreur lors du téléchargement:', error);
    }
  };

  const getMimeType = (contentType: string): string => {
    switch (contentType?.toLowerCase()) {
      case 'pdf':
        return 'application/pdf';
      case 'image':
        return 'image/jpeg';
      case 'video':
        return 'video/mp4';
      case 'audio':
        return 'audio/mpeg';
      case 'document':
        return 'application/msword';
      default:
        return 'text/plain';
    }
  };

  const handleShareContent = (resource: Resource) => {
    setSelectedResource(resource);
    setShowShareModal(true);
  };

  const closeModals = () => {
    setShowViewModal(false);
    setShowShareModal(false);
    setSelectedResource(null);
  };

  const filteredResources = resources.filter(resource => {
    const matchesSubject = !selectedSubject || resource.subject === subjects.find(s => s.id === selectedSubject)?.name;
    const matchesLevel = !selectedLevel || resource.level === levels.find(l => l.id === selectedLevel)?.name;
    const matchesType = !selectedType || resource.type === selectedType;
    const matchesSearch = !searchTerm || 
      resource.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      resource.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
      resource.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()));
    return matchesSubject && matchesLevel && matchesType && matchesSearch;
  });

  const sortedResources = [...filteredResources].sort((a, b) => {
    let aValue: any, bValue: any;
    
    switch (sortBy) {
      case 'recent':
        aValue = new Date(a.created_at).getTime();
        bValue = new Date(b.created_at).getTime();
        break;
      case 'popular':
        aValue = a.views;
        bValue = b.views;
        break;
      case 'rating':
        aValue = a.rating;
        bValue = b.rating;
        break;
      case 'title':
        aValue = a.title.toLowerCase();
        bValue = b.title.toLowerCase();
        break;
      default:
        return 0;
    }

    if (sortOrder === 'asc') {
      return aValue > bValue ? 1 : -1;
    } else {
      return aValue < bValue ? 1 : -1;
    }
  });

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  };

  const formatDuration = (minutes: number) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return hours > 0 ? `${hours}h${mins > 0 ? mins : ''}` : `${mins}min`;
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'video': return <Video size={16} className="text-red-500" />;
      case 'document': return <FileText size={16} className="text-blue-500" />;
      case 'image': return <Image size={16} className="text-green-500" />;
      case 'audio': return <Volume2 size={16} className="text-purple-500" />;
      case 'link': return <Link size={16} className="text-orange-500" />;
      case 'interactive': return <Play size={16} className="text-indigo-500" />;
      default: return <FileText size={16} className="text-gray-500" />;
    }
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'video': return 'bg-red-100 text-red-700';
      case 'document': return 'bg-blue-100 text-blue-700';
      case 'image': return 'bg-green-100 text-green-700';
      case 'audio': return 'bg-purple-100 text-purple-700';
      case 'link': return 'bg-orange-100 text-orange-700';
      case 'interactive': return 'bg-indigo-100 text-indigo-700';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

  const handleFavorite = (resourceId: number) => {
    setResources(prev => prev.map(resource => 
      resource.id === resourceId ? { ...resource, is_favorite: !resource.is_favorite } : resource
    ));
  };

  const handleCollectionToggle = (resourceId: number) => {
    setResources(prev => prev.map(resource => 
      resource.id === resourceId ? { ...resource, is_in_collection: !resource.is_in_collection } : resource
    ));
  };

  if (loading) {
    return (
      <div className="flex h-screen bg-gray-50">
        <Sidebar />
        <div className="flex-1 ml-56 p-8">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-200 rounded w-1/4 mb-6"></div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="h-48 bg-gray-200 rounded-lg"></div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 ml-56 p-8">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Bibliothèque de Ressources</h1>
            <p className="text-gray-600">Contenus partagés par vos enseignants et ressources d'apprentissage</p>
          </div>
          <div className="flex items-center space-x-4">
            <NotificationBell />
            <button 
              onClick={fetchSharedContents}
              className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg flex items-center space-x-2 transition-colors"
            >
              <RefreshCw size={20} />
              <span>Actualiser</span>
            </button>
            <button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg flex items-center space-x-2 transition-colors">
              <Plus size={20} />
              <span>Nouvelle collection</span>
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar - Filtres */}
          <div className="lg:col-span-1 space-y-6">
            {/* Recherche */}
            <div className="bg-white rounded-xl shadow-sm p-6">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                <input
                  type="text"
                  placeholder="Rechercher des ressources..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>

            {/* Types de ressources */}
            <div className="bg-white rounded-xl shadow-sm p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <Filter size={20} className="mr-2" />
                Types
              </h3>
              <div className="space-y-3">
                <button
                  onClick={() => setSelectedType(null)}
                  className={`w-full text-left px-4 py-3 rounded-lg transition-colors ${
                    selectedType === null 
                      ? 'bg-blue-50 text-blue-700 border border-blue-200' 
                      : 'hover:bg-gray-50'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-medium">Tous les types</span>
                    <span className="text-sm text-gray-500">{resources.length}</span>
                  </div>
                </button>
                {[
                  { type: 'video', label: 'Vidéos', count: resources.filter(r => r.type === 'video').length },
                  { type: 'document', label: 'Documents', count: resources.filter(r => r.type === 'document').length },
                  { type: 'image', label: 'Images', count: resources.filter(r => r.type === 'image').length },
                  { type: 'audio', label: 'Audio', count: resources.filter(r => r.type === 'audio').length },
                  { type: 'interactive', label: 'Interactifs', count: resources.filter(r => r.type === 'interactive').length },
                  { type: 'link', label: 'Liens', count: resources.filter(r => r.type === 'link').length }
                ].map(item => (
                  <button
                    key={item.type}
                    onClick={() => setSelectedType(item.type)}
                    className={`w-full text-left px-4 py-3 rounded-lg transition-colors ${
                      selectedType === item.type 
                        ? 'bg-blue-50 text-blue-700 border border-blue-200' 
                        : 'hover:bg-gray-50'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        {getTypeIcon(item.type)}
                        <span className="font-medium ml-2">{item.label}</span>
                      </div>
                      <span className="text-sm text-gray-500">{item.count}</span>
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* Matières */}
            <div className="bg-white rounded-xl shadow-sm p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <BookOpen size={20} className="mr-2" />
                Matières
              </h3>
              <div className="space-y-3">
                <button
                  onClick={() => setSelectedSubject(null)}
                  className={`w-full text-left px-4 py-3 rounded-lg transition-colors ${
                    selectedSubject === null 
                      ? 'bg-blue-50 text-blue-700 border border-blue-200' 
                      : 'hover:bg-gray-50'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-medium">Toutes les matières</span>
                    <span className="text-sm text-gray-500">{resources.length}</span>
                  </div>
                </button>
                {subjects.map(subject => (
                  <button
                    key={subject.id}
                    onClick={() => setSelectedSubject(subject.id)}
                    className={`w-full text-left px-4 py-3 rounded-lg transition-colors ${
                      selectedSubject === subject.id 
                        ? 'bg-blue-50 text-blue-700 border border-blue-200' 
                        : 'hover:bg-gray-50'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <div className={`w-3 h-3 rounded-full ${subject.color} mr-3`}></div>
                        <span className="font-medium">{subject.name}</span>
                      </div>
                      <span className="text-sm text-gray-500">{subject.resource_count}</span>
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* Niveaux */}
            <div className="bg-white rounded-xl shadow-sm p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <User size={20} className="mr-2" />
                Niveaux
              </h3>
              <div className="space-y-3">
                <button
                  onClick={() => setSelectedLevel(null)}
                  className={`w-full text-left px-4 py-3 rounded-lg transition-colors ${
                    selectedLevel === null 
                      ? 'bg-blue-50 text-blue-700 border border-blue-200' 
                      : 'hover:bg-gray-50'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-medium">Tous les niveaux</span>
                    <span className="text-sm text-gray-500">{resources.length}</span>
                  </div>
                </button>
                {levels.map(level => (
                  <button
                    key={level.id}
                    onClick={() => setSelectedLevel(level.id)}
                    className={`w-full text-left px-4 py-3 rounded-lg transition-colors ${
                      selectedLevel === level.id 
                        ? 'bg-blue-50 text-blue-700 border border-blue-200' 
                        : 'hover:bg-gray-50'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <div className={`w-3 h-3 rounded-full ${level.color} mr-3`}></div>
                        <span className="font-medium">{level.name}</span>
                      </div>
                      <span className="text-sm text-gray-500">{level.resource_count}</span>
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* Collections */}
            <div className="bg-white rounded-xl shadow-sm p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <Folder size={20} className="mr-2" />
                Mes Collections
              </h3>
              <div className="space-y-3">
                {collections.map(collection => (
                  <div key={collection.id} className="p-3 border border-gray-200 rounded-lg">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center">
                        <div className={`w-3 h-3 rounded-full ${collection.color} mr-2`}></div>
                        <span className="font-medium text-sm">{collection.name}</span>
                      </div>
                      <span className="text-xs text-gray-500">{collection.resource_count}</span>
                    </div>
                    <p className="text-xs text-gray-600">{collection.description}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3">
            {/* Controls */}
            <div className="bg-white rounded-xl shadow-sm p-6 mb-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => setViewMode('grid')}
                      className={`p-2 rounded-lg ${
                        viewMode === 'grid' 
                          ? 'bg-blue-100 text-blue-600' 
                          : 'text-gray-500 hover:text-gray-700'
                      }`}
                    >
                      <Grid size={20} />
                    </button>
                    <button
                      onClick={() => setViewMode('list')}
                      className={`p-2 rounded-lg ${
                        viewMode === 'list' 
                          ? 'bg-blue-100 text-blue-600' 
                          : 'text-gray-500 hover:text-gray-700'
                      }`}
                    >
                      <List size={20} />
                    </button>
                  </div>
                  <span className="text-sm text-gray-500">
                    {sortedResources.length} ressource{sortedResources.length > 1 ? 's' : ''}
                  </span>
                </div>
                <div className="flex items-center space-x-2">
                  <select
                    value={sortBy}
                    onChange={(e) => setSortBy(e.target.value as any)}
                    className="px-3 py-2 border border-gray-300 rounded-lg text-sm"
                  >
                    <option value="recent">Plus récent</option>
                    <option value="popular">Plus populaire</option>
                    <option value="rating">Mieux noté</option>
                    <option value="title">Alphabétique</option>
                  </select>
                  <button
                    onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
                    className="p-2 text-gray-500 hover:text-gray-700 rounded-lg hover:bg-gray-100"
                  >
                    {sortOrder === 'asc' ? <SortAsc size={16} /> : <SortDesc size={16} />}
                  </button>
                </div>
              </div>
            </div>

            {/* Resources Grid/List */}
            {viewMode === 'grid' ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {sortedResources.map(resource => (
                  <div key={resource.id} className="bg-white rounded-xl shadow-sm overflow-hidden hover:shadow-md transition-shadow">
                    {/* Thumbnail */}
                    <div className="h-48 bg-gray-200 relative">
                      {resource.thumbnail ? (
                        <img 
                          src={resource.thumbnail} 
                          alt={resource.title}
                          className="w-full h-full object-cover"
                        />
                      ) : (
                        <div className="w-full h-full flex items-center justify-center">
                          {getTypeIcon(resource.type)}
                        </div>
                      )}
                      <div className="absolute top-2 right-2 flex items-center space-x-1">
                        <button
                          onClick={() => handleFavorite(resource.id)}
                          className={`p-1 rounded-full ${
                            resource.is_favorite 
                              ? 'bg-red-500 text-white' 
                              : 'bg-white text-gray-500 hover:text-red-500'
                          }`}
                        >
                          <Heart size={14} />
                        </button>
                        <button
                          onClick={() => handleCollectionToggle(resource.id)}
                          className={`p-1 rounded-full ${
                            resource.is_in_collection 
                              ? 'bg-blue-500 text-white' 
                              : 'bg-white text-gray-500 hover:text-blue-500'
                          }`}
                        >
                          <Bookmark size={14} />
                        </button>
                      </div>
                    </div>

                    {/* Content */}
                    <div className="p-4">
                      <div className="flex items-center space-x-2 mb-2">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getTypeColor(resource.type)}`}>
                          {resource.type === 'video' ? 'Vidéo' :
                           resource.type === 'document' ? 'Document' :
                           resource.type === 'image' ? 'Image' :
                           resource.type === 'audio' ? 'Audio' :
                           resource.type === 'interactive' ? 'Interactif' : 'Lien'}
                        </span>
                        <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded-full text-xs">
                          {resource.subject}
                        </span>
                        <span className="px-2 py-1 bg-green-100 text-green-700 rounded-full text-xs">
                          {resource.level}
                        </span>
                        <span className="px-2 py-1 bg-purple-100 text-purple-700 rounded-full text-xs flex items-center">
                          <Share size={12} className="mr-1" />
                          Partagé
                        </span>
                      </div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">
                        {resource.title}
                      </h3>
                      <p className="text-gray-600 text-sm mb-3 line-clamp-3">
                        {resource.description}
                      </p>
                      <div className="flex items-center justify-between text-xs text-gray-500 mb-3">
                        <div className="flex items-center">
                          <User size={12} className="mr-1" />
                          {resource.author}
                        </div>
                        <div className="flex items-center">
                          <Eye size={12} className="mr-1" />
                          {resource.views}
                        </div>
                        <div className="flex items-center">
                          <Star size={12} className="mr-1" />
                          {resource.rating}
                        </div>
                      </div>
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                          {resource.duration && (
                            <span className="text-xs text-gray-500">
                              {formatDuration(resource.duration)}
                            </span>
                          )}
                          {resource.file_size && (
                            <span className="text-xs text-gray-500">
                              {resource.file_size}
                            </span>
                          )}
                        </div>
                        <div className="flex items-center space-x-1">
                          <button 
                            onClick={() => handleViewContent(resource)}
                            className="p-1 text-gray-500 hover:text-blue-600 transition-colors"
                            title="Consulter le contenu"
                          >
                            <Play size={14} />
                          </button>
                          {resource.allow_download !== false && (
                            <button 
                              onClick={() => handleDownloadContent(resource)}
                              className="p-1 text-gray-500 hover:text-green-600 transition-colors"
                              title="Télécharger le contenu"
                            >
                              <Download size={14} />
                            </button>
                          )}
                          <button 
                            onClick={() => handleShareContent(resource)}
                            className="p-1 text-gray-500 hover:text-purple-600 transition-colors"
                            title="Partager le contenu"
                          >
                            <Share2 size={14} />
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="space-y-4">
                {sortedResources.map(resource => (
                  <div key={resource.id} className="bg-white rounded-xl shadow-sm p-6">
                    <div className="flex items-start space-x-4">
                      <div className="flex-shrink-0">
                        <div className="w-16 h-16 bg-gray-200 rounded-lg flex items-center justify-center">
                          {getTypeIcon(resource.type)}
                        </div>
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          <span className={`px-3 py-1 rounded-full text-sm font-medium ${getTypeColor(resource.type)}`}>
                            {resource.type === 'video' ? 'Vidéo' :
                             resource.type === 'document' ? 'Document' :
                             resource.type === 'image' ? 'Image' :
                             resource.type === 'audio' ? 'Audio' :
                             resource.type === 'interactive' ? 'Interactif' : 'Lien'}
                          </span>
                          <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">
                            {resource.subject}
                          </span>
                          <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm">
                            {resource.level}
                          </span>
                        </div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-2">{resource.title}</h3>
                        <p className="text-gray-600 mb-3">{resource.description}</p>
                        <div className="flex items-center space-x-4 text-sm text-gray-500">
                          <div className="flex items-center">
                            <User size={16} className="mr-1" />
                            {resource.author}
                          </div>
                          <div className="flex items-center">
                            <Calendar size={16} className="mr-1" />
                            {formatDate(resource.created_at)}
                          </div>
                          <div className="flex items-center">
                            <Eye size={16} className="mr-1" />
                            {resource.views} vues
                          </div>
                          <div className="flex items-center">
                            <Star size={16} className="mr-1" />
                            {resource.rating}/5
                          </div>
                          {resource.duration && (
                            <div className="flex items-center">
                              <Clock size={16} className="mr-1" />
                              {formatDuration(resource.duration)}
                            </div>
                          )}
                        </div>
                        {resource.tags.length > 0 && (
                          <div className="flex items-center space-x-2 mt-3">
                            {resource.tags.slice(0, 3).map(tag => (
                              <span key={tag} className="px-2 py-1 bg-gray-100 text-gray-700 rounded-full text-xs">
                                {tag}
                              </span>
                            ))}
                            {resource.tags.length > 3 && (
                              <span className="px-2 py-1 bg-gray-100 text-gray-700 rounded-full text-xs">
                                +{resource.tags.length - 3}
                              </span>
                            )}
                          </div>
                        )}
                      </div>
                      <div className="flex items-center space-x-2">
                        <button
                          onClick={() => handleFavorite(resource.id)}
                          className={`p-2 rounded-lg ${
                            resource.is_favorite 
                              ? 'text-red-500 bg-red-50' 
                              : 'text-gray-500 hover:text-red-500 hover:bg-gray-100'
                          }`}
                        >
                          <Heart size={16} />
                        </button>
                        <button
                          onClick={() => handleCollectionToggle(resource.id)}
                          className={`p-2 rounded-lg ${
                            resource.is_in_collection 
                              ? 'text-blue-500 bg-blue-50' 
                              : 'text-gray-500 hover:text-blue-500 hover:bg-gray-100'
                          }`}
                        >
                          <Bookmark size={16} />
                        </button>
                        <button className="p-2 text-gray-500 hover:text-blue-600 rounded-lg hover:bg-gray-100">
                          <Play size={16} />
                        </button>
                        <button className="p-2 text-gray-500 hover:text-green-600 rounded-lg hover:bg-gray-100">
                          <Download size={16} />
                        </button>
                        <button className="p-2 text-gray-500 hover:text-purple-600 rounded-lg hover:bg-gray-100">
                          <Share2 size={16} />
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {sortedResources.length === 0 && (
              <div className="text-center py-12">
                <BookOpen className="mx-auto text-gray-400 mb-4" size={48} />
                <h3 className="text-lg font-medium text-gray-900 mb-2">Aucune ressource trouvée</h3>
                <p className="text-gray-500">Essayez de modifier vos critères de recherche</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Modal de consultation du contenu */}
      {showViewModal && selectedResource && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-6 max-w-4xl w-full mx-4 max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-start mb-4">
              <h2 className="text-2xl font-bold text-gray-900">{selectedResource.title}</h2>
              <button
                onClick={closeModals}
                className="text-gray-500 hover:text-gray-700 text-xl"
              >
                ×
              </button>
            </div>
            
            <div className="mb-4">
              <div className="flex items-center space-x-2 mb-3">
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${getTypeColor(selectedResource.type)}`}>
                  {selectedResource.type === 'video' ? 'Vidéo' :
                   selectedResource.type === 'document' ? 'Document' :
                   selectedResource.type === 'image' ? 'Image' :
                   selectedResource.type === 'audio' ? 'Audio' :
                   selectedResource.type === 'interactive' ? 'Interactif' : 'Lien'}
                </span>
                <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">
                  {selectedResource.subject}
                </span>
                <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm">
                  {selectedResource.level}
                </span>
                <span className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm flex items-center">
                  <Share size={14} className="mr-1" />
                  Partagé
                </span>
              </div>
              
              <p className="text-gray-600 mb-4">{selectedResource.description}</p>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div className="bg-gray-50 p-4 rounded-lg">
                  <h4 className="font-semibold text-gray-900 mb-2">Informations</h4>
                  <div className="space-y-2 text-sm text-gray-600">
                    <div className="flex justify-between">
                      <span>Auteur:</span>
                      <span>{selectedResource.author}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Date de partage:</span>
                      <span>{formatDate(selectedResource.created_at)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Vues:</span>
                      <span>{selectedResource.views}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Note:</span>
                      <span>{selectedResource.rating}/5</span>
                    </div>
                  </div>
                </div>
                
                <div className="bg-gray-50 p-4 rounded-lg">
                  <h4 className="font-semibold text-gray-900 mb-2">Actions</h4>
                  <div className="space-y-2">
                    <button
                      onClick={() => handleDownloadContent(selectedResource)}
                      className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg transition-colors flex items-center justify-center space-x-2"
                    >
                      <Download size={16} />
                      <span>Télécharger</span>
                    </button>
                    <button
                      onClick={() => handleShareContent(selectedResource)}
                      className="w-full bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded-lg transition-colors flex items-center justify-center space-x-2"
                    >
                      <Share2 size={16} />
                      <span>Partager</span>
                    </button>
                  </div>
                </div>
              </div>
              
              {/* Aperçu du contenu selon le type */}
              <div className="bg-gray-50 p-4 rounded-lg">
                <h4 className="font-semibold text-gray-900 mb-2">Aperçu</h4>
                {selectedResource.type === 'video' && (
                  <div className="text-center py-8">
                    <Video size={48} className="mx-auto text-gray-400 mb-2" />
                    <p className="text-gray-500">Vidéo: {selectedResource.title}</p>
                    <p className="text-sm text-gray-400">Cliquez sur Télécharger pour accéder au contenu</p>
                  </div>
                )}
                {selectedResource.type === 'document' && (
                  <div className="text-center py-8">
                    <FileText size={48} className="mx-auto text-gray-400 mb-2" />
                    <p className="text-gray-500">Document: {selectedResource.title}</p>
                    <p className="text-sm text-gray-400">Cliquez sur Télécharger pour accéder au contenu</p>
                  </div>
                )}
                {selectedResource.type === 'image' && (
                  <div className="text-center py-8">
                    <Image size={48} className="mx-auto text-gray-400 mb-2" />
                    <p className="text-gray-500">Image: {selectedResource.title}</p>
                    <p className="text-sm text-gray-400">Cliquez sur Télécharger pour accéder au contenu</p>
                  </div>
                )}
                {selectedResource.type === 'audio' && (
                  <div className="text-center py-8">
                    <Volume2 size={48} className="mx-auto text-gray-400 mb-2" />
                    <p className="text-gray-500">Audio: {selectedResource.title}</p>
                    <p className="text-sm text-gray-400">Cliquez sur Télécharger pour accéder au contenu</p>
                  </div>
                )}
                {selectedResource.type === 'interactive' && (
                  <div className="text-center py-8">
                    <BookOpen size={48} className="mx-auto text-gray-400 mb-2" />
                    <p className="text-gray-500">Contenu interactif: {selectedResource.title}</p>
                    <p className="text-sm text-gray-400">Cliquez sur Télécharger pour accéder au contenu</p>
                  </div>
                )}
                {selectedResource.type === 'link' && (
                  <div className="text-center py-8">
                    <Link size={48} className="mx-auto text-gray-400 mb-2" />
                    <p className="text-gray-500">Lien: {selectedResource.title}</p>
                    <p className="text-sm text-gray-400">Cliquez sur Télécharger pour accéder au contenu</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Modal de partage */}
      {showShareModal && selectedResource && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-6 max-w-md w-full mx-4">
            <div className="flex justify-between items-start mb-4">
              <h2 className="text-xl font-bold text-gray-900">Partager le contenu</h2>
              <button
                onClick={closeModals}
                className="text-gray-500 hover:text-gray-700 text-xl"
              >
                ×
              </button>
            </div>
            
            <div className="mb-4">
              <p className="text-gray-600 mb-4">
                Partager "{selectedResource.title}" avec d'autres personnes
              </p>
              
              <div className="space-y-3">
                <button className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg transition-colors flex items-center justify-center space-x-2">
                  <Share2 size={16} />
                  <span>Copier le lien</span>
                </button>
                <button className="w-full bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded-lg transition-colors flex items-center justify-center space-x-2">
                  <Download size={16} />
                  <span>Partager le fichier</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
} 