"use client";
import React, { useState, useEffect, useRef } from 'react';
import { useAuth  } from '../../../../hooks/useAuth';
import { Card } from '../../../../components/Card';
import Button from '../../../../components/Button';
import { 
  Upload, 
  FileText, 
  Video, 
  Image, 
  Music, 
  Download, 
  Eye, 
  Trash2, 
  Folder,
  Search,
  Filter,
  Grid,
  List,
  Calendar,
  User,
  HardDrive,
  Share2,
  Star,
  Bookmark,
  MoreVertical
} from 'lucide-react';

interface ContentItem {
  id: number;
  title: string;
  description: string;
  file_type: 'pdf' | 'video' | 'image' | 'audio' | 'document' | 'presentation';
  file_size: string;
  file_url: string;
  thumbnail_url?: string;
  uploaded_by: string;
  uploaded_at: string;
  category: string;
  tags: string[];
  is_favorite: boolean;
  is_bookmarked: boolean;
  download_count: number;
  view_count: number;
  duration?: number; // pour les vidéos
  pages?: number; // pour les PDFs
}

interface Category {
  id: number;
  name: string;
  icon: string;
  count: number;
}

const ContentPage: React.FC = () => {
  const { user, token } = useAuth();
  const [contentItems, setContentItems] = useState<ContentItem[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [uploading, setUploading] = useState(false);
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const fetchContent = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/v1/content/student/${user?.id}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.ok) {
          const data = await response.json();
          setContentItems(data.content || []);
          setCategories(data.categories || []);
        }
      } catch (error) {
        console.error('Erreur lors du chargement du contenu:', error);
      } finally {
        setLoading(false);
      }
    };

    if (user && token) {
      fetchContent();
    }
  }, [user, token]);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(event.target.files || []);
    setSelectedFiles(files);
  };

  const handleUpload = async () => {
    if (selectedFiles.length === 0) return;

    setUploading(true);
    const formData = new FormData();
    selectedFiles.forEach(file => {
      formData.append('files', file);
    });

    try {
      const response = await fetch('http://localhost:8000/api/v1/content/upload', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData
      });

      if (response.ok) {
        const uploadedContent = await response.json();
        setContentItems(prev => [...prev, ...uploadedContent.content]);
        setSelectedFiles([]);
        setShowUploadModal(false);
      }
    } catch (error) {
      console.error('Erreur lors de l\'upload:', error);
    } finally {
      setUploading(false);
    }
  };

  const handleDownload = async (contentId: number, fileName: string) => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/content/${contentId}/download`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = fileName;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      }
    } catch (error) {
      console.error('Erreur lors du téléchargement:', error);
    }
  };

  const handleFavorite = async (contentId: number) => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/content/${contentId}/favorite`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (response.ok) {
        setContentItems(prev => prev.map(item => 
          item.id === contentId ? { ...item, is_favorite: !item.is_favorite } : item
        ));
      }
    } catch (error) {
      console.error('Erreur lors de la mise en favori:', error);
    }
  };

  const handleBookmark = async (contentId: number) => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/content/${contentId}/bookmark`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (response.ok) {
        setContentItems(prev => prev.map(item => 
          item.id === contentId ? { ...item, is_bookmarked: !item.is_bookmarked } : item
        ));
      }
    } catch (error) {
      console.error('Erreur lors du bookmark:', error);
    }
  };

  const handleDelete = async (contentId: number) => {
    if (!confirm('Êtes-vous sûr de vouloir supprimer ce contenu ?')) return;

    try {
      const response = await fetch(`http://localhost:8000/api/v1/content/${contentId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (response.ok) {
        setContentItems(prev => prev.filter(item => item.id !== contentId));
      }
    } catch (error) {
      console.error('Erreur lors de la suppression:', error);
    }
  };

  const getFileIcon = (fileType: string) => {
    switch (fileType) {
      case 'pdf': return <FileText className="w-6 h-6 text-red-500" />;
      case 'video': return <Video className="w-6 h-6 text-blue-500" />;
      case 'image': return <Image className="w-6 h-6 text-green-500" />;
      case 'audio': return <Music className="w-6 h-6 text-purple-500" />;
      case 'document': return <FileText className="w-6 h-6 text-gray-500" />;
      case 'presentation': return <FileText className="w-6 h-6 text-orange-500" />;
      default: return <FileText className="w-6 h-6 text-gray-500" />;
    }
  };

  const getFileTypeColor = (fileType: string) => {
    switch (fileType) {
      case 'pdf': return 'bg-red-100 text-red-800';
      case 'video': return 'bg-blue-100 text-blue-800';
      case 'image': return 'bg-green-100 text-green-800';
      case 'audio': return 'bg-purple-100 text-purple-800';
      case 'document': return 'bg-gray-100 text-gray-800';
      case 'presentation': return 'bg-orange-100 text-orange-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const formatFileSize = (size: string) => {
    const bytes = parseInt(size);
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('fr-FR', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const filteredContent = contentItems.filter(item => {
    const matchesSearch = item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         item.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         item.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()));
    
    const matchesCategory = selectedCategory === 'all' || item.category === selectedCategory;
    
    return matchesSearch && matchesCategory;
  });

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-blue-600 animate-pulse text-xl font-bold">
          Chargement du contenu...
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Contenu</h1>
          <p className="text-gray-600">Gérez et organisez vos documents et ressources</p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card>
            <div className="p-6 text-center">
              <FileText className="w-8 h-8 text-blue-500 mx-auto mb-2" />
              <div className="text-2xl font-bold text-gray-900">{contentItems.length}</div>
              <div className="text-sm text-gray-500">Fichiers totaux</div>
            </div>
          </Card>
          <Card>
            <div className="p-6 text-center">
              <HardDrive className="w-8 h-8 text-green-500 mx-auto mb-2" />
              <div className="text-2xl font-bold text-gray-900">
                {contentItems.reduce((acc, item) => acc + parseInt(item.file_size), 0)} MB
              </div>
              <div className="text-sm text-gray-500">Espace utilisé</div>
            </div>
          </Card>
          <Card>
            <div className="p-6 text-center">
              <Download className="w-8 h-8 text-purple-500 mx-auto mb-2" />
              <div className="text-2xl font-bold text-gray-900">
                {contentItems.reduce((acc, item) => acc + item.download_count, 0)}
              </div>
              <div className="text-sm text-gray-500">Téléchargements</div>
            </div>
          </Card>
          <Card>
            <div className="p-6 text-center">
              <Eye className="w-8 h-8 text-orange-500 mx-auto mb-2" />
              <div className="text-2xl font-bold text-gray-900">
                {contentItems.reduce((acc, item) => acc + item.view_count, 0)}
              </div>
              <div className="text-sm text-gray-500">Vues totales</div>
            </div>
          </Card>
        </div>

        {/* Controls */}
        <div className="flex flex-col sm:flex-row gap-4 mb-6">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Rechercher du contenu..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
          <div className="flex gap-2">
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="all">Toutes les catégories</option>
              {categories.map(category => (
                <option key={category.id} value={category.name}>
                  {category.name} ({category.count})
                </option>
              ))}
            </select>
            <Button
              onClick={() => setViewMode(viewMode === 'grid' ? 'list' : 'grid')}
              variant="outline"
              size="sm"
            >
              {viewMode === 'grid' ? <List className="w-4 h-4" /> : <Grid className="w-4 h-4" />}
            </Button>
            <Button
              onClick={() => setShowUploadModal(true)}
              className="bg-blue-500 hover:bg-blue-600"
            >
              <Upload className="w-4 h-4 mr-2" />
              Upload
            </Button>
          </div>
        </div>

        {/* Content Grid/List */}
        {viewMode === 'grid' ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filteredContent.map((item) => (
              <Card key={item.id} className="hover:shadow-lg transition-shadow">
                <div className="p-4">
                  {/* Thumbnail */}
                  <div className="relative h-32 bg-gray-100 rounded-lg mb-4 flex items-center justify-center">
                    {item.thumbnail_url ? (
                      <img
                        src={item.thumbnail_url}
                        alt={item.title}
                        className="w-full h-full object-cover rounded-lg"
                      />
                    ) : (
                      getFileIcon(item.file_type)
                    )}
                    <div className="absolute top-2 right-2 flex space-x-1">
                      {item.is_favorite && (
                        <Star className="w-4 h-4 text-yellow-400 fill-current" />
                      )}
                      {item.is_bookmarked && (
                        <Bookmark className="w-4 h-4 text-blue-500 fill-current" />
                      )}
                    </div>
                  </div>

                  {/* Content Info */}
                  <div className="mb-4">
                    <h3 className="font-semibold text-gray-900 mb-1 truncate">{item.title}</h3>
                    <p className="text-sm text-gray-600 line-clamp-2 mb-2">{item.description}</p>
                    
                    <div className="flex items-center justify-between text-xs text-gray-500 mb-2">
                      <span>{formatFileSize(item.file_size)}</span>
                      <span>{item.download_count} téléchargements</span>
                    </div>

                    <div className="flex items-center justify-between">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getFileTypeColor(item.file_type)}`}>
                        {item.file_type.toUpperCase()}
                      </span>
                      <span className="text-xs text-gray-500">{formatDate(item.uploaded_at)}</span>
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="flex items-center justify-between">
                    <div className="flex space-x-2">
                      <button
                        onClick={() => handleDownload(item.id, item.title)}
                        className="p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                        title="Télécharger"
                      >
                        <Download className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => window.open(item.file_url, '_blank')}
                        className="p-2 text-gray-600 hover:text-green-600 hover:bg-green-50 rounded-lg transition-colors"
                        title="Voir"
                      >
                        <Eye className="w-4 h-4" />
                      </button>
                    </div>
                    <div className="flex space-x-2">
                      <button
                        onClick={() => handleFavorite(item.id)}
                        className={`p-2 rounded-lg transition-colors ${
                          item.is_favorite
                            ? 'text-yellow-600 bg-yellow-50'
                            : 'text-gray-600 hover:text-yellow-600 hover:bg-yellow-50'
                        }`}
                        title="Favori"
                      >
                        <Star className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleBookmark(item.id)}
                        className={`p-2 rounded-lg transition-colors ${
                          item.is_bookmarked
                            ? 'text-blue-600 bg-blue-50'
                            : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50'
                        }`}
                        title="Bookmark"
                      >
                        <Bookmark className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleDelete(item.id)}
                        className="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                        title="Supprimer"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        ) : (
          <div className="space-y-4">
            {filteredContent.map((item) => (
              <Card key={item.id}>
                <div className="p-4">
                  <div className="flex items-center space-x-4">
                    <div className="flex-shrink-0">
                      {getFileIcon(item.file_type)}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between">
                        <h3 className="font-semibold text-gray-900 truncate">{item.title}</h3>
                        <div className="flex items-center space-x-2">
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getFileTypeColor(item.file_type)}`}>
                            {item.file_type.toUpperCase()}
                          </span>
                          {item.is_favorite && <Star className="w-4 h-4 text-yellow-400 fill-current" />}
                          {item.is_bookmarked && <Bookmark className="w-4 h-4 text-blue-500 fill-current" />}
                        </div>
                      </div>
                      <p className="text-sm text-gray-600 mt-1">{item.description}</p>
                      <div className="flex items-center space-x-4 mt-2 text-xs text-gray-500">
                        <span>{formatFileSize(item.file_size)}</span>
                        <span>{item.download_count} téléchargements</span>
                        <span>{item.view_count} vues</span>
                        <span>{formatDate(item.uploaded_at)}</span>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <button
                        onClick={() => handleDownload(item.id, item.title)}
                        className="p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                      >
                        <Download className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => window.open(item.file_url, '_blank')}
                        className="p-2 text-gray-600 hover:text-green-600 hover:bg-green-50 rounded-lg transition-colors"
                      >
                        <Eye className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleFavorite(item.id)}
                        className={`p-2 rounded-lg transition-colors ${
                          item.is_favorite
                            ? 'text-yellow-600 bg-yellow-50'
                            : 'text-gray-600 hover:text-yellow-600 hover:bg-yellow-50'
                        }`}
                      >
                        <Star className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleBookmark(item.id)}
                        className={`p-2 rounded-lg transition-colors ${
                          item.is_bookmarked
                            ? 'text-blue-600 bg-blue-50'
                            : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50'
                        }`}
                      >
                        <Bookmark className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleDelete(item.id)}
                        className="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}

        {filteredContent.length === 0 && (
          <div className="text-center py-12">
            <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-600 mb-2">Aucun contenu trouvé</h3>
            <p className="text-gray-500">Essayez de modifier vos filtres ou uploader du nouveau contenu</p>
          </div>
        )}
      </div>

      {/* Upload Modal */}
      {showUploadModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Upload de fichiers</h3>
            
            <div className="mb-4">
              <input
                ref={fileInputRef}
                type="file"
                multiple
                onChange={handleFileSelect}
                className="w-full"
              />
            </div>

            {selectedFiles.length > 0 && (
              <div className="mb-4">
                <h4 className="font-medium text-gray-900 mb-2">Fichiers sélectionnés:</h4>
                <div className="space-y-2">
                  {selectedFiles.map((file, index) => (
                    <div key={index} className="text-sm text-gray-600">
                      {file.name} ({(file.size / 1024 / 1024).toFixed(2)} MB)
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="flex justify-end space-x-3">
              <Button
                onClick={() => {
                  setShowUploadModal(false);
                  setSelectedFiles([]);
                }}
                variant="outline"
              >
                Annuler
              </Button>
              <Button
                onClick={handleUpload}
                disabled={selectedFiles.length === 0 || uploading}
                className="bg-blue-500 hover:bg-blue-600"
              >
                {uploading ? 'Upload en cours...' : 'Upload'}
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ContentPage; 