'use client';

import React, { useState, useEffect } from 'react';
import { Card } from '../Card';
import { FileText, Download, BarChart3, TrendingUp, Users, Target } from 'lucide-react';
import { apiClient } from '../../utils/api';

interface Report {
  id: string;
  title: string;
  type: 'class_performance' | 'student_progress' | 'quiz_analytics' | 'content_usage';
  description: string;
  lastGenerated: string;
  status: 'ready' | 'generating' | 'error';
}

interface TeacherReportsWidgetProps {
  className?: string;
}

export default function TeacherReportsWidget({ className = '' }: TeacherReportsWidgetProps) {
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [generatingReport, setGeneratingReport] = useState<string | null>(null);

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    setLoading(true);
    try {
      const response = await apiClient.get('/api/v1/reports/teacher');
      setReports(response.data.reports || []);
    } catch (error) {
      console.error('Erreur lors du chargement des rapports:', error);
      setError(error instanceof Error ? error.message : 'Erreur inconnue');
    } finally {
      setLoading(false);
    }
  };

  const generateReport = async (reportType: string) => {
    try {
      setGeneratingReport(reportType);
      
      await apiClient.post('/api/v1/reports/generate', { type: reportType });

      // Simuler le temps de génération
      setTimeout(() => {
        setGeneratingReport(null);
        fetchReports(); // Rafraîchir la liste
      }, 2000);

    } catch (err) {
      console.error('Erreur lors de la génération du rapport:', err);
      setGeneratingReport(null);
    }
  };

  const downloadReport = async (reportId: string, format: 'pdf' | 'csv' = 'pdf') => {
    try {
      const token = localStorage.getItem('najah_token');
      const headers: Record<string, string> = {};
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(`${API_BASE_URL}/api/v1/reports/${reportId}/download?format=${format}`, { headers });
      
      if (!response.ok) {
        throw new Error('Erreur lors du téléchargement');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `rapport_${reportId}.${format}`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);

    } catch (err) {
      console.error('Erreur lors du téléchargement:', err);
      alert('Erreur lors du téléchargement du rapport');
    }
  };

  const getReportIcon = (type: string) => {
    switch (type) {
      case 'class_performance': return <BarChart3 className="text-blue-600" size={20} />;
      case 'student_progress': return <TrendingUp className="text-green-600" size={20} />;
      case 'quiz_analytics': return <Target className="text-purple-600" size={20} />;
      case 'content_usage': return <Users className="text-orange-600" size={20} />;
      default: return <FileText className="text-gray-600" size={20} />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'ready': return 'text-green-600 bg-green-50';
      case 'generating': return 'text-yellow-600 bg-yellow-50';
      case 'error': return 'text-red-600 bg-red-50';
      default: return 'text-gray-600 bg-gray-50';
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('fr-FR', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <Card title="Rapports et Analytics" icon={<FileText />} className={`p-8 shadow-lg rounded-2xl ${className}`}>
      <div className="space-y-6">
                 {/* Actions rapides */}
         <div className="grid grid-cols-2 gap-4">
           <button
             onClick={() => generateReport('class_performance')}
             disabled={generatingReport === 'class_performance'}
             className="p-3 bg-blue-50 rounded-lg hover:bg-blue-100 transition disabled:opacity-50"
           >
             <BarChart3 className="text-blue-600 mx-auto mb-1" size={20} />
             <div className="text-xs font-medium text-blue-700">Performance</div>
             {generatingReport === 'class_performance' && (
               <div className="text-xs text-blue-600">...</div>
             )}
           </button>

           <button
             onClick={() => generateReport('student_progress')}
             disabled={generatingReport === 'student_progress'}
             className="p-3 bg-green-50 rounded-lg hover:bg-green-100 transition disabled:opacity-50"
           >
             <TrendingUp className="text-green-600 mx-auto mb-1" size={20} />
             <div className="text-xs font-medium text-green-700">Progression</div>
             {generatingReport === 'student_progress' && (
               <div className="text-xs text-green-600">...</div>
             )}
           </button>
         </div>

        {/* Liste des rapports */}
        <div>
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Rapports disponibles</h3>
          
          {loading ? (
            <div className="text-blue-600 font-semibold">Chargement des rapports...</div>
          ) : error ? (
            <div className="text-red-600 font-semibold">{error}</div>
          ) : reports.length === 0 ? (
            <div className="text-gray-500 italic">Aucun rapport disponible</div>
          ) : (
            <div className="space-y-4">
              {reports.map((report, index) => (
                <div key={report.id || `report-${index}`} className="p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-start justify-between">
                    <div className="flex items-start gap-3 flex-1">
                      {getReportIcon(report.type)}
                      <div className="flex-1">
                        <h4 className="font-semibold text-gray-800 mb-1">{report.title}</h4>
                        <p className="text-sm text-gray-600 mb-2">{report.description}</p>
                        <div className="flex items-center gap-4 text-xs text-gray-500">
                          <span>Généré le: {formatDate(report.lastGenerated)}</span>
                          <span className={`px-2 py-1 rounded-full font-medium ${getStatusColor(report.status)}`}>
                            {report.status === 'ready' ? 'Prêt' : 
                             report.status === 'generating' ? 'Génération...' : 'Erreur'}
                          </span>
                        </div>
                      </div>
                    </div>
                    
                    {report.status === 'ready' && (
                      <div className="flex gap-2">
                        <button
                          onClick={() => downloadReport(report.id, 'pdf')}
                          className="px-3 py-1 bg-blue-600 text-white rounded text-sm font-medium hover:bg-blue-700 transition"
                        >
                          <Download size={14} className="inline mr-1" />
                          PDF
                        </button>
                        <button
                          onClick={() => downloadReport(report.id, 'csv')}
                          className="px-3 py-1 bg-green-600 text-white rounded text-sm font-medium hover:bg-green-700 transition"
                        >
                          <Download size={14} className="inline mr-1" />
                          CSV
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Statistiques rapides */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-4 border-t">
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600">{reports.length}</div>
            <div className="text-sm text-gray-600">Rapports disponibles</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600">
              {reports.filter(r => r.status === 'ready').length}
            </div>
            <div className="text-sm text-gray-600">Prêts à télécharger</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-purple-600">
              {reports.filter(r => r.type === 'class_performance').length}
            </div>
            <div className="text-sm text-gray-600">Rapports de classe</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-orange-600">
              {reports.filter(r => r.type === 'student_progress').length}
            </div>
            <div className="text-sm text-gray-600">Rapports élèves</div>
          </div>
        </div>
      </div>
    </Card>
  );
} 