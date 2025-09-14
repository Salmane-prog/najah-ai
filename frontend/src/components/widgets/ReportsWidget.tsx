'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { FileText, TrendingUp, BarChart3, Download, Calendar, Target } from 'lucide-react';
import { reportsAPI, DetailedReport, SubjectProgressReport, AnalyticsReport } from '@/api/student/reports';
import { useAuth  } from '@/hooks/useAuth';

interface ReportsWidgetProps {
  className?: string;
}

export default function ReportsWidget({ className }: ReportsWidgetProps) {
  const { user } = useAuth();
  const [detailedReports, setDetailedReports] = useState<DetailedReport[]>([]);
  const [subjectReports, setSubjectReports] = useState<SubjectProgressReport[]>([]);
  const [analyticsReports, setAnalyticsReports] = useState<AnalyticsReport[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedTab, setSelectedTab] = useState<'detailed' | 'subjects' | 'analytics'>('detailed');

  useEffect(() => {
    loadReportsData();
  }, []);

  const loadReportsData = async () => {
    try {
      setLoading(true);
      const [detailedData, subjectsData, analyticsData] = await Promise.all([
        reportsAPI.getDetailedReports(),
        reportsAPI.getSubjectProgressReports(),
        reportsAPI.getAnalyticsReports()
      ]);

      setDetailedReports(detailedData.reports || []);
      setSubjectReports(subjectsData.reports || []);
      setAnalyticsReports(analyticsData.reports || []);
    } catch (err) {
      setError('Erreur lors du chargement des rapports');
      console.error('Erreur:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleExportReport = async (reportId: number, format: string = 'pdf') => {
    try {
      const exportData = await reportsAPI.exportReport(reportId, format);
      // Ici vous pouvez gérer le téléchargement du fichier
      console.log('Rapport exporté:', exportData);
    } catch (err) {
      console.error('Erreur lors de l\'export du rapport:', err);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
    });
  };

  const getReportTypeColor = (type: string) => {
    switch (type) {
      case 'performance':
        return 'bg-blue-100 text-blue-800';
      case 'progress':
        return 'bg-green-100 text-green-800';
      case 'analytics':
        return 'bg-purple-100 text-purple-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getProgressColor = (percentage: number) => {
    if (percentage >= 80) return 'bg-green-100 text-green-800';
    if (percentage >= 60) return 'bg-yellow-100 text-yellow-800';
    return 'bg-red-100 text-red-800';
  };

  if (loading) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <FileText className="w-5 h-5" />
            Rapports
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="animate-pulse space-y-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="flex items-center space-x-4">
                <div className="w-4 h-4 bg-gray-200 rounded"></div>
                <div className="flex-1 space-y-2">
                  <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                  <div className="h-3 bg-gray-200 rounded w-1/2"></div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <FileText className="w-5 h-5" />
            Rapports
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center text-red-500">
            <FileText className="w-8 h-8 mx-auto mb-2" />
            <p>{error}</p>
            <Button onClick={loadReportsData} className="mt-2">
              Réessayer
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <FileText className="w-5 h-5" />
            Rapports
          </CardTitle>
          <div className="flex gap-2">
            <Button
              variant={selectedTab === 'detailed' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setSelectedTab('detailed')}
            >
              Détaillés
            </Button>
            <Button
              variant={selectedTab === 'subjects' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setSelectedTab('subjects')}
            >
              Matières
            </Button>
            <Button
              variant={selectedTab === 'analytics' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setSelectedTab('analytics')}
            >
              Analytics
            </Button>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-4 max-h-96 overflow-y-auto">
          {selectedTab === 'detailed' && (
            <>
              {detailedReports.length === 0 ? (
                <div className="text-center text-gray-500 py-8">
                  <FileText className="w-12 h-12 mx-auto mb-2 opacity-50" />
                  <p>Aucun rapport détaillé disponible</p>
                </div>
              ) : (
                detailedReports.map((report) => (
                  <div key={report.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <h3 className="font-semibold text-gray-900">{report.title}</h3>
                          <Badge className={getReportTypeColor(report.report_type)}>
                            {report.report_type}
                          </Badge>
                        </div>
                        <p className="text-sm text-gray-600 mb-2">{report.description}</p>
                        <div className="flex items-center gap-4 text-sm text-gray-500">
                          <div className="flex items-center gap-1">
                            <Calendar className="w-4 h-4" />
                            <span>{formatDate(report.period_start)} - {formatDate(report.period_end)}</span>
                          </div>
                          {report.is_exported && (
                            <div className="flex items-center gap-1">
                              <Download className="w-4 h-4" />
                              <span>Exporté le {formatDate(report.exported_at!)}</span>
                            </div>
                          )}
                        </div>
                      </div>
                      <div className="flex flex-col gap-2 ml-4">
                        <Button
                          size="sm"
                          onClick={() => handleExportReport(report.id, 'pdf')}
                        >
                          <Download className="w-4 h-4 mr-1" />
                          Exporter
                        </Button>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </>
          )}

          {selectedTab === 'subjects' && (
            <>
              {subjectReports.length === 0 ? (
                <div className="text-center text-gray-500 py-8">
                  <Target className="w-12 h-12 mx-auto mb-2 opacity-50" />
                  <p>Aucun rapport de matière disponible</p>
                </div>
              ) : (
                subjectReports.map((report) => (
                  <div key={report.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <h3 className="font-semibold text-gray-900">{report.subject}</h3>
                          <Badge className={getProgressColor(report.percentage)}>
                            {Math.round(report.percentage)}%
                          </Badge>
                        </div>
                        <div className="flex items-center gap-4 text-sm text-gray-500 mb-2">
                          <div className="flex items-center gap-1">
                            <TrendingUp className="w-4 h-4" />
                            <span>Score: {report.total_score}/{report.max_score}</span>
                          </div>
                          {report.improvement_rate && (
                            <div className="flex items-center gap-1">
                              <BarChart3 className="w-4 h-4" />
                              <span>Amélioration: {Math.round(report.improvement_rate * 100)}%</span>
                            </div>
                          )}
                        </div>
                        <div className="flex items-center gap-4 text-sm text-gray-500">
                          <div className="flex items-center gap-1">
                            <Calendar className="w-4 h-4" />
                            <span>{formatDate(report.period_start)} - {formatDate(report.period_end)}</span>
                          </div>
                        </div>
                      </div>
                      <div className="flex flex-col gap-2 ml-4">
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleExportReport(report.id, 'pdf')}
                        >
                          <Download className="w-4 h-4 mr-1" />
                          Exporter
                        </Button>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </>
          )}

          {selectedTab === 'analytics' && (
            <>
              {analyticsReports.length === 0 ? (
                <div className="text-center text-gray-500 py-8">
                  <BarChart3 className="w-12 h-12 mx-auto mb-2 opacity-50" />
                  <p>Aucun rapport d'analytics disponible</p>
                </div>
              ) : (
                analyticsReports.map((report) => (
                  <div key={report.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <h3 className="font-semibold text-gray-900">
                            Analytics {report.analytics_type}
                          </h3>
                          <Badge className="bg-purple-100 text-purple-800">
                            Analytics
                          </Badge>
                        </div>
                        {report.insights && (
                          <p className="text-sm text-gray-600 mb-2">{report.insights}</p>
                        )}
                        <div className="flex items-center gap-4 text-sm text-gray-500">
                          <div className="flex items-center gap-1">
                            <Calendar className="w-4 h-4" />
                            <span>{formatDate(report.period_start)} - {formatDate(report.period_end)}</span>
                          </div>
                        </div>
                      </div>
                      <div className="flex flex-col gap-2 ml-4">
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleExportReport(report.id, 'pdf')}
                        >
                          <Download className="w-4 h-4 mr-1" />
                          Exporter
                        </Button>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
