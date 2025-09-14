'use client';

import React, { useState, useEffect } from 'react';
import Sidebar from '../../../../components/Sidebar';
import { useAuth  } from '../../../../hooks/useAuth';
import NotificationBell from '../../../../components/NotificationBell';
import { 
  fetchUserCorrections, 
  fetchCorrectionStats,
  fetchCorrectionHistory,
  createScoreCorrection,
  updateScoreCorrection,
  deleteScoreCorrection
} from '../../../../api/student/scoreCorrections';
import { Edit, TrendingUp, AlertTriangle, CheckCircle, Clock, BarChart3, Plus, Trash2, Save, X } from 'lucide-react';

export default function CorrectionsPage() {
  const { user, token } = useAuth();
  const userId = user?.id;
  
  const [corrections, setCorrections] = useState<any>(null);
  const [correctionStats, setCorrectionStats] = useState<any>(null);
  const [correctionHistory, setCorrectionHistory] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [selectedSubject, setSelectedSubject] = useState('');
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [editingCorrection, setEditingCorrection] = useState<any>(null);
  const [formData, setFormData] = useState({
    quiz_result_id: '',
    corrected_score: '',
    reason: ''
  });

  useEffect(() => {
    if (!userId) return;
    
    const loadCorrectionData = async () => {
      try {
        const [correctionsRes, statsRes, historyRes] = await Promise.all([
          fetchUserCorrections(userId),
          fetchCorrectionStats(userId),
          fetchCorrectionHistory(userId, selectedSubject || undefined)
        ]);

        setCorrections(correctionsRes);
        setCorrectionStats(statsRes);
        setCorrectionHistory(historyRes);
        setLoading(false);
      } catch (error) {
        console.error('Erreur lors du chargement des corrections:', error);
        setLoading(false);
      }
    };

    loadCorrectionData();
  }, [userId, selectedSubject]);

  const handleCreateCorrection = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!userId) return;

    try {
      await createScoreCorrection(userId, {
        quiz_result_id: parseInt(formData.quiz_result_id),
        corrected_score: parseFloat(formData.corrected_score),
        reason: formData.reason
      });

      // Recharger les données
      const [correctionsRes, statsRes, historyRes] = await Promise.all([
        fetchUserCorrections(userId),
        fetchCorrectionStats(userId),
        fetchCorrectionHistory(userId, selectedSubject || undefined)
      ]);

      setCorrections(correctionsRes);
      setCorrectionStats(statsRes);
      setCorrectionHistory(historyRes);
      
      // Réinitialiser le formulaire
      setFormData({ quiz_result_id: '', corrected_score: '', reason: '' });
      setShowCreateForm(false);
    } catch (error) {
      console.error('Erreur lors de la création de la correction:', error);
    }
  };

  const handleUpdateCorrection = async (correctionId: number, data: any) => {
    if (!userId) return;

    try {
      await updateScoreCorrection(userId, correctionId, data);
      
      // Recharger les données
      const [correctionsRes, statsRes, historyRes] = await Promise.all([
        fetchUserCorrections(userId),
        fetchCorrectionStats(userId),
        fetchCorrectionHistory(userId, selectedSubject || undefined)
      ]);

      setCorrections(correctionsRes);
      setCorrectionStats(statsRes);
      setCorrectionHistory(historyRes);
      setEditingCorrection(null);
    } catch (error) {
      console.error('Erreur lors de la mise à jour de la correction:', error);
    }
  };

  const handleDeleteCorrection = async (correctionId: number) => {
    if (!userId || !confirm('Êtes-vous sûr de vouloir supprimer cette correction ?')) return;

    try {
      await deleteScoreCorrection(userId, correctionId);
      
      // Recharger les données
      const [correctionsRes, statsRes, historyRes] = await Promise.all([
        fetchUserCorrections(userId),
        fetchCorrectionStats(userId),
        fetchCorrectionHistory(userId, selectedSubject || undefined)
      ]);

      setCorrections(correctionsRes);
      setCorrectionStats(statsRes);
      setCorrectionHistory(historyRes);
    } catch (error) {
      console.error('Erreur lors de la suppression de la correction:', error);
    }
  };

  const getCorrectionStatus = (adjustment: number) => {
    if (adjustment > 0) return { icon: <TrendingUp className="text-green-500" size={16} />, color: 'text-green-600', bg: 'bg-green-100' };
    if (adjustment < 0) return { icon: <AlertTriangle className="text-red-500" size={16} />, color: 'text-red-600', bg: 'bg-red-100' };
    return { icon: <CheckCircle className="text-blue-500" size={16} />, color: 'text-blue-600', bg: 'bg-blue-100' };
  };

  const formatAdjustment = (adjustment: number) => {
    const sign = adjustment > 0 ? '+' : '';
    return `${sign}${adjustment.toFixed(1)}%`;
  };

  if (!userId) {
    return (
      <div className="flex min-h-screen bg-gray-50">
        <Sidebar />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-red-600 text-lg font-bold">Erreur : utilisateur non connecté.</div>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex min-h-screen bg-gray-50">
        <Sidebar />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-blue-600 animate-pulse text-xl font-bold">Chargement des corrections...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 overflow-auto pl-0 md:pl-56">
        <div className="p-6">
          {/* Header */}
          <div className="mb-8 flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-3">
                <Edit className="text-blue-600" />
                Corrections de Scores
              </h1>
              <p className="text-gray-600">Gérez et suivez vos corrections de scores</p>
            </div>
            <div className="flex items-center gap-4">
              <NotificationBell />
              <button
                onClick={() => setShowCreateForm(true)}
                className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <Plus className="w-4 h-4" />
                Nouvelle Correction
              </button>
            </div>
          </div>

          {/* Statistiques */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-center gap-2 mb-2">
                <BarChart3 className="text-blue-500" size={16} />
                <span className="font-medium">Total Corrections</span>
              </div>
              <div className="text-2xl font-bold text-blue-600">
                {correctionStats?.total_corrections || 0}
              </div>
              <div className="text-sm text-gray-500">
                Corrections effectuées
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-center gap-2 mb-2">
                <TrendingUp className="text-green-500" size={16} />
                <span className="font-medium">Moyenne Ajustement</span>
              </div>
              <div className="text-2xl font-bold text-green-600">
                {formatAdjustment(correctionStats?.average_correction || 0)}
              </div>
              <div className="text-sm text-gray-500">
                Par correction
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-center gap-2 mb-2">
                <Clock className="text-purple-500" size={16} />
                <span className="font-medium">Dernière Correction</span>
              </div>
              <div className="text-2xl font-bold text-purple-600">
                {correctionHistory?.corrections?.[0] ? 
                  new Date(correctionHistory.corrections[0].created_at).toLocaleDateString() : 
                  'Aucune'
                }
              </div>
              <div className="text-sm text-gray-500">
                Date de la dernière correction
              </div>
            </div>
          </div>

          {/* Filtres et Formulaire */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Filtres et Formulaire */}
            <div className="lg:col-span-1">
              {/* Filtre par sujet */}
              <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
                <h2 className="text-lg font-bold text-gray-800 mb-4">Filtrer par Sujet</h2>
                <select
                  value={selectedSubject}
                  onChange={(e) => setSelectedSubject(e.target.value)}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Tous les sujets</option>
                  {correctionStats?.corrections_by_subject?.map((subject: any) => (
                    <option key={subject.subject} value={subject.subject}>
                      {subject.subject} ({subject.count})
                    </option>
                  ))}
                </select>
              </div>

              {/* Formulaire de création */}
              {showCreateForm && (
                <div className="bg-white rounded-lg shadow-sm p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h2 className="text-lg font-bold text-gray-800">Nouvelle Correction</h2>
                    <button
                      onClick={() => setShowCreateForm(false)}
                      className="text-gray-500 hover:text-gray-700"
                    >
                      <X className="w-5 h-5" />
                    </button>
                  </div>
                  
                  <form onSubmit={handleCreateCorrection} className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        ID du Quiz Result
                      </label>
                      <input
                        type="number"
                        value={formData.quiz_result_id}
                        onChange={(e) => setFormData({...formData, quiz_result_id: e.target.value})}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                        required
                      />
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Score Corrigé (%)
                      </label>
                      <input
                        type="number"
                        step="0.1"
                        min="0"
                        max="100"
                        value={formData.corrected_score}
                        onChange={(e) => setFormData({...formData, corrected_score: e.target.value})}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                        required
                      />
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Raison
                      </label>
                      <textarea
                        value={formData.reason}
                        onChange={(e) => setFormData({...formData, reason: e.target.value})}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                        rows={3}
                        placeholder="Expliquez la raison de cette correction..."
                      />
                    </div>
                    
                    <button
                      type="submit"
                      className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                    >
                      <Save className="w-4 h-4" />
                      Créer la Correction
                    </button>
                  </form>
                </div>
              )}
            </div>

            {/* Historique des corrections */}
            <div className="lg:col-span-2">
              <div className="bg-white rounded-lg shadow-sm p-6">
                <h2 className="text-xl font-bold text-gray-800 mb-4">Historique des Corrections</h2>
                
                <div className="space-y-4">
                  {correctionHistory?.corrections?.length > 0 ? (
                    correctionHistory.corrections.map((correction: any, index: number) => {
                      const status = getCorrectionStatus(correction.adjustment);
                      const isEditing = editingCorrection?.id === correction.id;
                      
                      return (
                        <div key={correction.id} className="border border-gray-200 rounded-lg p-4">
                          {isEditing ? (
                            <div className="space-y-3">
                              <div className="flex items-center justify-between">
                                <h3 className="font-medium text-gray-800">Modifier la correction</h3>
                                <div className="flex gap-2">
                                  <button
                                    onClick={() => handleUpdateCorrection(correction.id, {
                                      corrected_score: editingCorrection.corrected_score,
                                      reason: editingCorrection.reason
                                    })}
                                    className="flex items-center gap-1 px-3 py-1 bg-green-600 text-white rounded text-sm hover:bg-green-700"
                                  >
                                    <Save className="w-3 h-3" />
                                    Sauvegarder
                                  </button>
                                  <button
                                    onClick={() => setEditingCorrection(null)}
                                    className="flex items-center gap-1 px-3 py-1 bg-gray-600 text-white rounded text-sm hover:bg-gray-700"
                                  >
                                    <X className="w-3 h-3" />
                                    Annuler
                                  </button>
                                </div>
                              </div>
                              <div className="grid grid-cols-2 gap-3">
                                <div>
                                  <label className="block text-xs font-medium text-gray-700 mb-1">
                                    Score Corrigé (%)
                                  </label>
                                  <input
                                    type="number"
                                    step="0.1"
                                    value={editingCorrection.corrected_score}
                                    onChange={(e) => setEditingCorrection({
                                      ...editingCorrection,
                                      corrected_score: parseFloat(e.target.value)
                                    })}
                                    className="w-full p-2 border border-gray-300 rounded text-sm"
                                  />
                                </div>
                                <div>
                                  <label className="block text-xs font-medium text-gray-700 mb-1">
                                    Raison
                                  </label>
                                  <input
                                    type="text"
                                    value={editingCorrection.reason}
                                    onChange={(e) => setEditingCorrection({
                                      ...editingCorrection,
                                      reason: e.target.value
                                    })}
                                    className="w-full p-2 border border-gray-300 rounded text-sm"
                                  />
                                </div>
                              </div>
                            </div>
                          ) : (
                            <div className="flex items-start justify-between">
                              <div className="flex items-start gap-3">
                                <div className={`w-8 h-8 rounded-full flex items-center justify-center ${status.bg}`}>
                                  {status.icon}
                                </div>
                                <div className="flex-1">
                                  <div className="flex items-center gap-2 mb-1">
                                    <h3 className="font-medium text-gray-800">{correction.quiz_title}</h3>
                                    <span className="text-xs text-gray-500">({correction.subject})</span>
                                  </div>
                                  <div className="flex items-center gap-4 text-sm text-gray-600 mb-2">
                                    <span>Original: {correction.original_score}%</span>
                                    <span>Corrigé: {correction.corrected_score}%</span>
                                    <span className={`font-medium ${status.color}`}>
                                      {formatAdjustment(correction.adjustment)}
                                    </span>
                                  </div>
                                  {correction.reason && (
                                    <p className="text-sm text-gray-600 mb-2">Raison: {correction.reason}</p>
                                  )}
                                  <p className="text-xs text-gray-500">
                                    {new Date(correction.created_at).toLocaleDateString('fr-FR', {
                                      year: 'numeric',
                                      month: 'long',
                                      day: 'numeric',
                                      hour: '2-digit',
                                      minute: '2-digit'
                                    })}
                                  </p>
                                </div>
                              </div>
                              <div className="flex gap-2">
                                <button
                                  onClick={() => setEditingCorrection({
                                    id: correction.id,
                                    corrected_score: correction.corrected_score,
                                    reason: correction.reason
                                  })}
                                  className="p-2 text-blue-600 hover:bg-blue-50 rounded"
                                >
                                  <Edit className="w-4 h-4" />
                                </button>
                                <button
                                  onClick={() => handleDeleteCorrection(correction.id)}
                                  className="p-2 text-red-600 hover:bg-red-50 rounded"
                                >
                                  <Trash2 className="w-4 h-4" />
                                </button>
                              </div>
                            </div>
                          )}
                        </div>
                      );
                    })
                  ) : (
                    <div className="text-center py-8 text-gray-500">
                      <Edit className="mx-auto mb-2 text-gray-400" size={32} />
                      <p>Aucune correction trouvée</p>
                      <p className="text-sm">Les corrections apparaîtront ici</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 