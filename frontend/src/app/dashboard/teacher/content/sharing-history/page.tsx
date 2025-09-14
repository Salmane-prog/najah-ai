'use client';

import React, { useState, useEffect } from 'react';
import Sidebar from '../../../../components/Sidebar';
import { useAuth  } from '../../../../hooks/useAuth';
import { 
  BookOpen, Search, Filter, Share2, Eye, Download, Users, 
  Calendar, Clock, CheckCircle, XCircle, Edit, Trash2, BarChart3 
} from 'lucide-react';

interface ContentSharing {
  id: number;
  content_id: number;
  shared_by: number;
  shared_at: string;
  is_active: boolean;
  target_type: string;
  target_ids: number[];
  allow_download: boolean;
  allow_view: boolean;
  expiration_date?: string;
  notify_students: boolean;
  custom_message?: string;
  view_count: number;
  download_count: number;
  student_count: number;
  content_title: string;
  content_subject: string;
  content_type: string;
  teacher_name: string;
}

interface ContentAccess {
  id: number;
  content_id: number;
  student_id: number;
  sharing_id: number;
  first_accessed?: string;
  last_accessed?: string;
  access_count: number;
  can_view: boolean;
  can_download: boolean;
  student_name: string;
  student_email: string;
  content_title: string;
}

interface SharingStats {
  total_sharings: number;
  active_sharings: number;
  total_views: number;
  total_downloads: number;
  total_students_reached: number;
  sharings_this_week: number;
  sharings_this_month: number;
  views_this_week: number;
  downloads_this_week: number;
}

export default function SharingHistory() {
  const { user, token } = useAuth();
  const [sharings, setSharings] = useState<ContentSharing[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [filterType, setFilterType] = useState<string>('all');
  const [sortBy, setSortBy] = useState<'shared_at' | 'content_title' | 'student_count' | 'view_count'>('shared_at');
  const [stats, setStats] = useState<SharingStats | null>(null);
  const [selectedSharing, setSelectedSharing] = useState<ContentSharing | null>(null);
  const [showAccessModal, setShowAccessModal] = useState(false);
  const [accesses, setAccesses] = useState<ContentAccess[]>([]);
  const [loadingAccesses, setLoadingAccesses] = useState(false);

  useEffect(() => {
    if (token) {
      fetchSharings();
      fetchStats();
    }
  }, [token]);

  const fetchSharings = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/content-sharing/?active_only=false`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setSharings(data);
      } else {
        setError('Erreur lors du chargement des partages');
      }
    } catch (err) {
      setError('Erreur de connexion');
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/content-sharing/stats`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setStats(data);
      }
    } catch (err) {
      console.error('Erreur lors du chargement des statistiques:', err);
    }
  };

  const fetchAccesses = async (sharingId: number) => {
    try {
      setLoadingAccesses(true);
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/content-sharing/accesses/${sharingId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setAccesses(data);
      }
    } catch (err) {
      console.error('Erreur lors du chargement des accès:', err);
    } finally {
      setLoadingAccesses(false);
    }
  };

  const handleViewAccesses = (sharing: ContentSharing) => {
    setSelectedSharing(sharing);
    setShowAccessModal(true);
    fetchAccesses(sharing.id);
  };

  const updateSharing = async (sharingId: number, updates: any) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/content-sharing/${sharingId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(updates)
      });
      
      if (response.ok) {
        fetchSharings();
        fetchStats();
      }
    } catch (err) {
      console.error('Erreur lors de la mise à jour:', err);
    }
  };

  const deleteSharing = async (sharingId: number) => {
    if (!confirm('Êtes-vous sûr de vouloir supprimer ce partage ?')) return;

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/content-sharing/${sharingId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        fetchSharings();
        fetchStats();
      }
    } catch (err) {
      console.error('Erreur lors de la suppression:', err);
    }
  };

  const getTargetTypeLabel = (type: string) => {
    switch (type) {
      case 'class': return 'Classes';
      case 'student': return 'Étudiants';
      case 'all_students': return 'Tous les étudiants';
      default: return type;
    }
  };

  const getStatusIcon = (sharing: ContentSharing) => {
    if (!sharing.is_active) return <XCircle className="text-red-500" size={16} />;
    if (sharing.expiration_date && new Date(sharing.expiration_date) < new Date()) {
      return <Clock className="text-orange-500" size={16} />;
    }
    return <CheckCircle className="text-green-500" size={16} />;
  };

  const getStatusText = (sharing: ContentSharing) => {
    if (!sharing.is_active) return 'Inactif';
    if (sharing.expiration_date && new Date(sharing.expiration_date) < new Date()) {
      return 'Expiré';
    }
    return 'Actif';
  };

  const filteredAndSortedSharings = sharings
    .filter(sharing => {
      const matchesSearch = sharing.content_title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          sharing.content_subject.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesStatus = filterStatus === 'all' || 
                           (filterStatus === 'active' && sharing.is_active) ||
                           (filterStatus === 'inactive' && !sharing.is_active);
      const matchesType = filterType === 'all' || sharing.target_type === filterType;
      
      return matchesSearch && matchesStatus && matchesType;
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'shared_at':
          return new Date(b.shared_at).getTime() - new Date(a.shared_at).getTime();
        case 'content_title':
          return a.content_title.localeCompare(b.content_title);
        case 'student_count':
          return b.student_count - a.student_count;
        case 'view_count':
          return b.view_count - a.view_count;
        default:
          return 0;
      }
    });

  if (loading) {
    return (
      <div className="flex min-h-screen bg-gray-50">
        <Sidebar userType="teacher" />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-blue-600 animate-pulse text-xl font-bold">Chargement de l'historique...</div>
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
            <h1 className="text-3xl font-bold text-gray-800 mb-2">Historique des Partages</h1>
            <p className="text-gray-600">Suivez et gérez vos partages de contenu</p>
          </div>

          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-800">{error}</p>
            </div>
          )}

          {/* Statistiques */}
          {stats && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
              <div className="bg-white p-4 rounded-lg shadow-sm border">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                    <Share2 className="text-blue-600" size={20} />
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Total partages</p>
                    <p className="text-2xl font-bold text-gray-800">{stats.total_sharings}</p>
                  </div>
                </div>
              </div>

              <div className="bg-white p-4 rounded-lg shadow-sm border">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                    <CheckCircle className="text-green-600" size={20} />
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Partages actifs</p>
                    <p className="text-2xl font-bold text-gray-800">{stats.active_sharings}</p>
                  </div>
                </div>
              </div>

              <div className="bg-white p-4 rounded-lg shadow-sm border">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                    <Eye className="text-purple-600" size={20} />
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Total vues</p>
                    <p className="text-2xl font-bold text-gray-800">{stats.total_views}</p>
                  </div>
                </div>
              </div>

              <div className="bg-white p-4 rounded-lg shadow-sm border">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center">
                    <Users className="text-orange-600" size={20} />
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Étudiants touchés</p>
                    <p className="text-2xl font-bold text-gray-800">{stats.total_students_reached}</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Filtres et recherche */}
          <div className="mb-6 flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center gap-4">
              <div className="relative">
                <Search className="absolute left-3 top-2.5 text-gray-400" size={16} />
                <input
                  type="text"
                  placeholder="Rechercher des partages..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div className="flex items-center gap-2">
                <Filter className="text-gray-600" size={16} />
                <select
                  value={filterStatus}
                  onChange={(e) => setFilterStatus(e.target.value)}
                  className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="all">Tous les statuts</option>
                  <option value="active">Actifs</option>
                  <option value="inactive">Inactifs</option>
                </select>
              </div>

              <div className="flex items-center gap-2">
                <select
                  value={filterType}
                  onChange={(e) => setFilterType(e.target.value)}
                  className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="all">Tous les types</option>
                  <option value="class">Classes</option>
                  <option value="student">Étudiants</option>
                  <option value="all_students">Tous les étudiants</option>
                </select>
              </div>

              <div className="flex items-center gap-2">
                <span className="text-sm text-gray-600">Trier par:</span>
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value as any)}
                  className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="shared_at">Date de partage</option>
                  <option value="content_title">Titre du contenu</option>
                  <option value="student_count">Nombre d'étudiants</option>
                  <option value="view_count">Nombre de vues</option>
                </select>
              </div>
            </div>
          </div>

          {/* Liste des partages */}
          <div className="space-y-4">
            {filteredAndSortedSharings.map((sharing) => (
              <div key={sharing.id} className="bg-white rounded-xl shadow-sm border p-6">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                      <BookOpen className="text-blue-600" size={20} />
                    </div>
                    <div>
                      <h3 className="font-bold text-gray-800 text-lg">{sharing.content_title}</h3>
                      <p className="text-gray-600">{sharing.content_subject} • {sharing.content_type}</p>
                      <div className="flex items-center gap-4 mt-2 text-sm text-gray-500">
                        <span>Partagé le {new Date(sharing.shared_at).toLocaleDateString('fr-FR')}</span>
                        <span>•</span>
                        <span>{getTargetTypeLabel(sharing.target_type)}</span>
                        <span>•</span>
                        <span>{sharing.student_count} étudiants</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-2">
                    {getStatusIcon(sharing)}
                    <span className="text-sm font-medium">{getStatusText(sharing)}</span>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
                  <div className="text-center">
                    <p className="text-2xl font-bold text-blue-600">{sharing.view_count}</p>
                    <p className="text-sm text-gray-600">Vues</p>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-bold text-green-600">{sharing.download_count}</p>
                    <p className="text-sm text-gray-600">Téléchargements</p>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-bold text-purple-600">{sharing.student_count}</p>
                    <p className="text-sm text-gray-600">Étudiants</p>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-bold text-orange-600">
                      {sharing.expiration_date ? new Date(sharing.expiration_date).toLocaleDateString('fr-FR') : '∞'}
                    </p>
                    <p className="text-sm text-gray-600">Expire le</p>
                  </div>
                </div>

                {sharing.custom_message && (
                  <div className="mb-4 p-3 bg-gray-50 rounded-lg">
                    <p className="text-sm text-gray-700 italic">"{sharing.custom_message}"</p>
                  </div>
                )}

                <div className="flex items-center justify-between pt-4 border-t border-gray-200">
                  <div className="flex items-center gap-2 text-sm text-gray-600">
                    <span>Permissions:</span>
                    {sharing.allow_view && <span className="px-2 py-1 bg-green-100 text-green-800 rounded-full text-xs">Vue</span>}
                    {sharing.allow_download && <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs">Téléchargement</span>}
                  </div>
                  
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleViewAccesses(sharing)}
                      className="px-3 py-2 text-blue-600 hover:text-blue-800 border border-blue-300 rounded-lg hover:bg-blue-50 text-sm"
                    >
                      <Eye size={16} className="inline mr-1" />
                      Voir les accès
                    </button>
                    
                    <button
                      onClick={() => updateSharing(sharing.id, { is_active: !sharing.is_active })}
                      className="px-3 py-2 text-gray-600 hover:text-gray-800 border border-gray-300 rounded-lg hover:bg-gray-50 text-sm"
                    >
                      <Edit size={16} className="inline mr-1" />
                      {sharing.is_active ? 'Désactiver' : 'Activer'}
                    </button>
                    
                    <button
                      onClick={() => deleteSharing(sharing.id)}
                      className="px-3 py-2 text-red-600 hover:text-red-800 border border-red-300 rounded-lg hover:bg-red-50 text-sm"
                    >
                      <Trash2 size={16} className="inline mr-1" />
                      Supprimer
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {filteredAndSortedSharings.length === 0 && (
            <div className="text-center py-12">
              <Share2 className="mx-auto text-gray-400 mb-4" size={48} />
              <p className="text-gray-600">Aucun partage trouvé</p>
              <p className="text-sm text-gray-500">Commencez à partager du contenu pour voir l'historique</p>
            </div>
          )}
        </div>
      </div>

      {/* Modal des accès */}
      {showAccessModal && selectedSharing && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-6 w-full max-w-4xl max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-bold text-gray-800">
                Accès au contenu : {selectedSharing.content_title}
              </h3>
              <button
                onClick={() => setShowAccessModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                ✕
              </button>
            </div>

            {loadingAccesses ? (
              <div className="text-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                <p className="text-gray-600 mt-2">Chargement des accès...</p>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-5 gap-4 p-4 bg-gray-50 rounded-lg font-medium text-gray-700">
                  <div>Étudiant</div>
                  <div>Email</div>
                  <div>Premier accès</div>
                  <div>Dernier accès</div>
                  <div>Nombre d'accès</div>
                </div>
                
                {accesses.map((access) => (
                  <div key={access.id} className="grid grid-cols-1 md:grid-cols-5 gap-4 p-4 border border-gray-200 rounded-lg">
                    <div className="font-medium">{access.student_name}</div>
                    <div className="text-gray-600">{access.student_email}</div>
                    <div className="text-gray-600">
                      {access.first_accessed ? new Date(access.first_accessed).toLocaleDateString('fr-FR') : 'Jamais'}
                    </div>
                    <div className="text-gray-600">
                      {access.last_accessed ? new Date(access.last_accessed).toLocaleDateString('fr-FR') : 'Jamais'}
                    </div>
                    <div className="text-gray-600">{access.access_count}</div>
                  </div>
                ))}
                
                {accesses.length === 0 && (
                  <div className="text-center py-8 text-gray-500">
                    Aucun accès enregistré pour ce partage
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}



