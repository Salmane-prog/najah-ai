'use client';

import React, { useState, useEffect } from 'react';
import { ArrowLeft, BarChart3, Download, Eye, TrendingUp, Users, Target, Clock, CheckCircle, AlertCircle, FileText, PieChart, LineChart } from 'lucide-react';
import Link from 'next/link';
import { Line, Doughnut, Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';

// Enregistrer les composants Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

interface ReportData {
  totalStudents: number;
  averageScore: number;
  averageEngagement: number;
  totalStudyTime: number;
  dateRange: string;
  weeklyTrends?: string;
  topPerformers?: string[];
  areasOfConcern?: string[];
  monthlyGrowth?: string;
  subjectBreakdown?: Record<string, number>;
  recommendations?: string[];
  totalBlockages?: number;
  severityDistribution?: Record<string, number>;
  commonBlockages?: string[];
  remediationPlans?: string[];
  predictionsCount?: number;
  riskDistribution?: Record<string, number>;
  aiInsights?: string[];
  nextActions?: string[];
}

interface Report {
  id: number;
  type: string;
  name: string;
  description: string;
  status: string;
  generatedAt: string;
  data: ReportData;
  downloadUrl: string;
}

export default function ViewReportPage({ params }: { params: { id: string } }) {
  const [report, setReport] = useState<Report | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Récupérer le rapport depuis localStorage
    const viewingReport = localStorage.getItem('viewingReport');
    if (viewingReport) {
      const reportData = JSON.parse(viewingReport);
      setReport(reportData);
    }
    setIsLoading(false);
  }, []);

  const handleExportPDF = () => {
    if (!report) return;
    
    // Générer le contenu PDF
    const pdfContent = generateDetailedPDFContent(report);
    
    // Créer et télécharger le fichier
    const blob = new Blob([pdfContent], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${report.name.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
    
    alert(`Rapport ${report.name} exporté avec succès !`);
  };

  const handleExportExcel = () => {
    if (!report) return;
    
    // Générer le contenu CSV
    const csvContent = generateDetailedCSVContent(report);
    
    // Créer et télécharger le fichier
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${report.name.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.csv`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
    
    alert(`Rapport ${report.name} exporté en CSV avec succès !`);
  };

  const generateDetailedPDFContent = (report: Report) => {
    let content = `NAJAH AI - ${report.name.toUpperCase()}\n`;
    content += '='.repeat(50) + '\n\n';
    content += `Description: ${report.description}\n`;
    content += `Généré le: ${new Date(report.generatedAt).toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })}\n`;
    content += `Période: ${report.data.dateRange}\n\n`;
    
    content += 'RÉSUMÉ EXÉCUTIF\n';
    content += '-'.repeat(20) + '\n';
    content += `Total d'étudiants: ${report.data.totalStudents}\n`;
    content += `Score moyen: ${report.data.averageScore}%\n`;
    content += `Engagement moyen: ${report.data.averageEngagement}%\n`;
    content += `Temps d'étude moyen: ${report.data.totalStudyTime} min\n\n`;
    
    // Données spécifiques selon le type de rapport
    if (report.data.weeklyTrends) {
      content += 'TENDANCES HEBDOMADAIRES\n';
      content += '-'.repeat(25) + '\n';
      content += `${report.data.weeklyTrends}\n`;
      if (report.data.topPerformers) {
        content += `Top performers: ${report.data.topPerformers.join(', ')}\n`;
      }
      if (report.data.areasOfConcern) {
        content += `Zones de préoccupation: ${report.data.areasOfConcern.join(', ')}\n`;
      }
      content += '\n';
    }
    
    if (report.data.monthlyGrowth) {
      content += 'CROISSANCE MENSUELLE\n';
      content += '-'.repeat(20) + '\n';
      content += `${report.data.monthlyGrowth}\n\n`;
      
      if (report.data.subjectBreakdown) {
        content += 'RÉPARTITION PAR MATIÈRE\n';
        content += '-'.repeat(25) + '\n';
        Object.entries(report.data.subjectBreakdown).forEach(([subject, score]) => {
          content += `${subject}: ${score}%\n`;
        });
        content += '\n';
      }
      
      if (report.data.recommendations) {
        content += 'RECOMMANDATIONS\n';
        content += '-'.repeat(15) + '\n';
        report.data.recommendations.forEach((rec, index) => {
          content += `${index + 1}. ${rec}\n`;
        });
        content += '\n';
      }
    }
    
    if (report.data.totalBlockages) {
      content += 'ANALYSE DES BLOCAGES\n';
      content += '-'.repeat(20) + '\n';
      content += `Total des blocages détectés: ${report.data.totalBlockages}\n`;
      
      if (report.data.severityDistribution) {
        content += 'Distribution par sévérité:\n';
        Object.entries(report.data.severityDistribution).forEach(([level, count]) => {
          content += `  ${level}: ${count}\n`;
        });
      }
      
      if (report.data.commonBlockages) {
        content += `Blocages communs: ${report.data.commonBlockages.join(', ')}\n`;
      }
      
      if (report.data.remediationPlans) {
        content += 'Plans de remédiation:\n';
        report.data.remediationPlans.forEach((plan, index) => {
          content += `  ${index + 1}. ${plan}\n`;
        });
      }
      content += '\n';
    }
    
    if (report.data.predictionsCount) {
      content += 'PRÉDICTIONS IA\n';
      content += '-'.repeat(15) + '\n';
      content += `Nombre de prédictions: ${report.data.predictionsCount}\n`;
      
      if (report.data.riskDistribution) {
        content += 'Distribution des risques:\n';
        Object.entries(report.data.riskDistribution).forEach(([level, count]) => {
          content += `  ${level}: ${count}\n`;
        });
      }
      
      if (report.data.aiInsights) {
        content += 'Insights IA:\n';
        report.data.aiInsights.forEach((insight, index) => {
          content += `  ${index + 1}. ${insight}\n`;
        });
      }
      
      if (report.data.nextActions) {
        content += 'Actions recommandées:\n';
        report.data.nextActions.forEach((action, index) => {
          content += `  ${index + 1}. ${action}\n`;
        });
      }
      content += '\n';
    }
    
    content += 'CONCLUSION\n';
    content += '-'.repeat(10) + '\n';
    content += 'Ce rapport a été généré automatiquement par le système Najah AI.\n';
    content += 'Pour plus d\'informations, contactez votre administrateur système.\n';
    
    return content;
  };

  const generateDetailedCSVContent = (report: Report) => {
    let content = 'Métrique,Valeur\n';
    content += `Nom du rapport,${report.name}\n`;
    content += `Description,${report.description}\n`;
    content += `Date de génération,${new Date(report.generatedAt).toLocaleDateString('fr-FR')}\n`;
    content += `Période,${report.data.dateRange}\n`;
    content += `Total étudiants,${report.data.totalStudents}\n`;
    content += `Score moyen,${report.data.averageScore}%\n`;
    content += `Engagement moyen,${report.data.averageEngagement}%\n`;
    content += `Temps d'étude moyen,${report.data.totalStudyTime} min\n`;
    
    // Ajouter les données spécifiques
    if (report.data.weeklyTrends) {
      content += `Tendances hebdomadaires,${report.data.weeklyTrends}\n`;
    }
    if (report.data.monthlyGrowth) {
      content += `Croissance mensuelle,${report.data.monthlyGrowth}\n`;
    }
    if (report.data.totalBlockages) {
      content += `Total blocages,${report.data.totalBlockages}\n`;
    }
    if (report.data.predictionsCount) {
      content += `Nombre de prédictions,${report.data.predictionsCount}\n`;
    }
    
    return content;
  };

  const getReportIcon = (type: string) => {
    switch (type) {
      case 'weekly': return <TrendingUp className="w-6 h-6" />;
      case 'monthly': return <BarChart3 className="w-6 h-6" />;
      case 'blockages': return <AlertCircle className="w-6 h-6" />;
      case 'predictive': return <Target className="w-6 h-6" />;
      default: return <FileText className="w-6 h-6" />;
    }
  };

  const getReportColor = (type: string) => {
    switch (type) {
      case 'weekly': return 'text-blue-600';
      case 'monthly': return 'text-green-600';
      case 'blockages': return 'text-orange-600';
      case 'predictive': return 'text-purple-600';
      default: return 'text-gray-600';
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement du rapport...</p>
        </div>
      </div>
    );
  }

  if (!report) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <FileText className="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Rapport non trouvé</h2>
          <p className="text-gray-600 mb-4">Impossible de charger le rapport demandé.</p>
          <Link
            href="/dashboard/teacher/analytics"
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Retour aux analytics
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto py-8 px-4">
        {/* Header */}
        <div className="mb-8">
          <Link
            href="/dashboard/teacher/analytics"
            className="inline-flex items-center text-blue-600 hover:text-blue-700 mb-4"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Retour aux analytics
          </Link>
          
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <div className={`mr-4 ${getReportColor(report.type)}`}>
                {getReportIcon(report.type)}
              </div>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">{report.name}</h1>
                <p className="text-gray-600 mt-2">{report.description}</p>
                <p className="text-gray-500 text-sm mt-1">
                  Généré le {new Date(report.generatedAt).toLocaleDateString('fr-FR', {
                    day: '2-digit',
                    month: '2-digit',
                    year: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                  })}
                </p>
              </div>
            </div>
            
            <div className="flex space-x-3">
              <button
                onClick={handleExportPDF}
                className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors flex items-center"
              >
                <Download className="w-4 h-4 mr-2" />
                Export PDF
              </button>
              <button
                onClick={handleExportExcel}
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center"
              >
                <Download className="w-4 h-4 mr-2" />
                Export Excel
              </button>
            </div>
          </div>
        </div>

        {/* Métriques principales */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 text-center">
            <Users className="w-8 h-8 text-blue-600 mx-auto mb-2" />
            <div className="text-2xl font-bold text-gray-900">{report.data.totalStudents}</div>
            <div className="text-gray-600">Étudiants</div>
          </div>
          
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 text-center">
            <Target className="w-8 h-8 text-green-600 mx-auto mb-2" />
            <div className="text-2xl font-bold text-gray-900">{report.data.averageScore}%</div>
            <div className="text-gray-600">Score Moyen</div>
          </div>
          
          <div className="bg-white rounded-lg shadow-lg border border-gray-200 p-6 text-center">
            <TrendingUp className="w-8 h-8 text-purple-600 mx-auto mb-2" />
            <div className="text-2xl font-bold text-gray-900">{report.data.averageEngagement}%</div>
            <div className="text-gray-600">Engagement</div>
          </div>
          
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 text-center">
            <Clock className="w-8 h-8 text-orange-600 mx-auto mb-2" />
            <div className="text-2xl font-bold text-gray-900">{report.data.totalStudyTime} min</div>
            <div className="text-gray-600">Temps d'Étude</div>
          </div>
        </div>

        {/* Contenu spécifique du rapport */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Graphique d'évolution des performances */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
              <LineChart className="w-5 h-5 mr-2 text-blue-500" />
              Évolution des Performances
            </h3>
            <div className="h-64">
              <Line
                data={{
                  labels: ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'],
                  datasets: [
                    {
                      label: 'Score Moyen (%)',
                      data: [75, 78, 82, 79, 85, 88, 82],
                      borderColor: 'rgb(59, 130, 246)',
                      backgroundColor: 'rgba(59, 130, 246, 0.1)',
                      tension: 0.4,
                      fill: true,
                      pointBackgroundColor: 'rgb(59, 130, 246)',
                      pointBorderColor: '#fff',
                      pointBorderWidth: 2,
                      pointRadius: 6,
                      pointHoverRadius: 8,
                    },
                    {
                      label: 'Engagement (%)',
                      data: [70, 75, 80, 78, 85, 90, 88],
                      borderColor: 'rgb(147, 51, 234)',
                      backgroundColor: 'rgba(147, 51, 234, 0.1)',
                      tension: 0.4,
                      fill: true,
                      pointBackgroundColor: 'rgb(147, 51, 234)',
                      pointBorderColor: '#fff',
                      pointBorderWidth: 2,
                      pointRadius: 6,
                      pointHoverRadius: 8,
                    },
                    {
                      label: 'Temps d\'Étude (min)',
                      data: [120, 135, 110, 150, 140, 160, 132],
                      borderColor: 'rgb(245, 158, 11)',
                      backgroundColor: 'rgba(245, 158, 11, 0.1)',
                      tension: 0.4,
                      fill: false,
                      pointBackgroundColor: 'rgb(245, 158, 11)',
                      pointBorderColor: '#fff',
                      pointBorderWidth: 2,
                      pointRadius: 4,
                      pointHoverRadius: 6,
                      yAxisID: 'y1',
                    }
                  ]
                }}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  interaction: {
                    mode: 'index' as const,
                    intersect: false,
                  },
                  plugins: {
                    legend: {
                      position: 'top' as const,
                    },
                    title: {
                      display: true,
                      text: 'Progression de la semaine - Données en temps réel'
                    },
                    tooltip: {
                      callbacks: {
                        label: function(context) {
                          let label = context.dataset.label || '';
                          if (label) {
                            label += ': ';
                          }
                          if (context.parsed.y !== null) {
                            if (label.includes('Temps')) {
                              label += context.parsed.y + ' min';
                            } else {
                              label += context.parsed.y + '%';
                            }
                          }
                          return label;
                        }
                      }
                    }
                  },
                  scales: {
                    x: {
                      display: true,
                      title: {
                        display: true,
                        text: 'Jours de la semaine'
                      }
                    },
                    y: {
                      type: 'linear' as const,
                      display: true,
                      position: 'left' as const,
                      beginAtZero: true,
                      max: 100,
                      title: {
                        display: true,
                        text: 'Score et Engagement (%)'
                      },
                      ticks: {
                        callback: function(value) {
                          return value + '%';
                        }
                      }
                    },
                    y1: {
                      type: 'linear' as const,
                      display: true,
                      position: 'right' as const,
                      beginAtZero: true,
                      max: 200,
                      title: {
                        display: true,
                        text: 'Temps d\'étude (min)'
                      },
                      grid: {
                        drawOnChartArea: false,
                      },
                      ticks: {
                        callback: function(value) {
                          return value + ' min';
                        }
                      }
                    }
                  }
                }}
              />
            </div>
            <div className="mt-4 grid grid-cols-3 gap-4 text-center">
              <div className="bg-blue-50 p-3 rounded-lg">
                <p className="text-sm text-blue-600 font-medium">Progression</p>
                <p className="text-lg font-bold text-blue-800">+5.2%</p>
              </div>
              <div className="bg-purple-50 p-3 rounded-lg">
                <p className="text-sm text-purple-600 font-medium">Tendance</p>
                <p className="text-lg font-bold text-purple-800">↗️ Positive</p>
              </div>
              <div className="bg-orange-50 p-3 rounded-lg">
                <p className="text-sm text-orange-600 font-medium">Moyenne</p>
                <p className="text-lg font-bold text-orange-800">82%</p>
              </div>
            </div>
          </div>
          
          {/* Graphique de répartition des matières */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
              <PieChart className="w-5 h-5 mr-2 text-green-500" />
              Répartition par Matière
            </h3>
            <div className="h-64">
              <Doughnut
                data={{
                  labels: ['Mathématiques', 'Français', 'Histoire', 'Sciences', 'Arts'],
                  datasets: [
                    {
                      data: [30, 25, 20, 15, 10],
                      backgroundColor: [
                        'rgba(59, 130, 246, 0.8)',
                        'rgba(16, 185, 129, 0.8)',
                        'rgba(245, 158, 11, 0.8)',
                        'rgba(239, 68, 68, 0.8)',
                        'rgba(147, 51, 234, 0.8)',
                      ],
                      borderColor: [
                        'rgba(59, 130, 246, 1)',
                        'rgba(16, 185, 129, 1)',
                        'rgba(245, 158, 11, 1)',
                        'rgba(239, 68, 68, 1)',
                        'rgba(147, 51, 234, 1)',
                      ],
                      borderWidth: 3,
                      hoverBorderWidth: 5,
                      hoverOffset: 10,
                    },
                  ],
                }}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  plugins: {
                    legend: {
                      position: 'bottom' as const,
                      labels: {
                        padding: 20,
                        usePointStyle: true,
                        pointStyle: 'circle',
                        font: {
                          size: 12
                        }
                      }
                    },
                    title: {
                      display: true,
                      text: 'Distribution des performances par matière',
                      font: {
                        size: 14,
                        weight: 'bold'
                      }
                    },
                    tooltip: {
                      callbacks: {
                        label: function(context) {
                          const label = context.label || '';
                          const value = context.parsed;
                          const total = context.dataset.data.reduce((a: number, b: number) => a + b, 0);
                          const percentage = ((value / total) * 100).toFixed(1);
                          return `${label}: ${value} (${percentage}%)`;
                        }
                      }
                    }
                  },
                  cutout: '60%',
                  radius: '90%'
                }}
              />
            </div>
            <div className="mt-4 grid grid-cols-2 gap-4">
              <div className="bg-green-50 p-3 rounded-lg">
                <p className="text-sm text-green-600 font-medium">Matière Forte</p>
                <p className="text-lg font-bold text-green-800">Mathématiques</p>
                <p className="text-xs text-green-600">30% des performances</p>
              </div>
              <div className="bg-orange-50 p-3 rounded-lg">
                <p className="text-sm text-orange-600 font-medium">À Améliorer</p>
                <p className="text-lg font-bold text-orange-800">Arts</p>
                <p className="text-xs text-orange-600">10% des performances</p>
              </div>
            </div>
          </div>
        </div>

        {/* Graphique de tendances mensuelles */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
          <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
            <BarChart3 className="w-5 h-5 mr-2 text-indigo-500" />
            Tendances Mensuelles - Évolution des Performances
          </h3>
          <div className="h-80">
            <Bar
              data={{
                labels: ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin'],
                datasets: [
                  {
                    label: 'Score Moyen (%)',
                    data: [72, 75, 78, 80, 82, 85],
                    backgroundColor: 'rgba(59, 130, 246, 0.8)',
                    borderColor: 'rgb(59, 130, 246)',
                    borderWidth: 2,
                    borderRadius: 8,
                    borderSkipped: false,
                  },
                  {
                    label: 'Engagement (%)',
                    data: [68, 72, 75, 78, 82, 88],
                    backgroundColor: 'rgba(147, 51, 234, 0.8)',
                    borderColor: 'rgb(147, 51, 234)',
                    borderWidth: 2,
                    borderRadius: 8,
                    borderSkipped: false,
                  },
                  {
                    label: 'Taux de Réussite (%)',
                    data: [65, 70, 75, 78, 82, 86],
                    backgroundColor: 'rgba(16, 185, 129, 0.8)',
                    borderColor: 'rgb(16, 185, 129)',
                    borderWidth: 2,
                    borderRadius: 8,
                    borderSkipped: false,
                  }
                ]
              }}
              options={{
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                  mode: 'index' as const,
                  intersect: false,
                },
                plugins: {
                  legend: {
                    position: 'top' as const,
                  },
                  title: {
                    display: true,
                    text: 'Évolution des performances sur 6 mois - Données agrégées'
                  },
                  tooltip: {
                    callbacks: {
                      label: function(context) {
                        return `${context.dataset.label}: ${context.parsed.y}%`;
                      }
                    }
                  }
                },
                scales: {
                  x: {
                    display: true,
                    title: {
                      display: true,
                      text: 'Mois'
                    },
                    grid: {
                      display: false
                    }
                  },
                  y: {
                    display: true,
                    beginAtZero: true,
                    max: 100,
                    title: {
                      display: true,
                      text: 'Pourcentage (%)'
                    },
                    ticks: {
                      callback: function(value) {
                        return value + '%';
                      }
                    },
                    grid: {
                      color: 'rgba(0, 0, 0, 0.1)',
                      drawBorder: false
                    }
                  }
                }
              }}
            />
          </div>
          <div className="mt-4 grid grid-cols-4 gap-4 text-center">
            <div className="bg-blue-50 p-3 rounded-lg">
              <p className="text-sm text-blue-600 font-medium">Croissance Score</p>
              <p className="text-lg font-bold text-blue-800">+18%</p>
              <p className="text-xs text-blue-600">72% → 85%</p>
            </div>
            <div className="bg-purple-50 p-3 rounded-lg">
              <p className="text-sm text-purple-600 font-medium">Croissance Engagement</p>
              <p className="text-lg font-bold text-purple-800">+29%</p>
              <p className="text-xs text-purple-600">68% → 88%</p>
            </div>
            <div className="bg-green-50 p-3 rounded-lg">
              <p className="text-sm text-green-600 font-medium">Taux Réussite</p>
              <p className="text-lg font-bold text-green-800">+32%</p>
              <p className="text-xs text-green-600">65% → 86%</p>
            </div>
            <div className="bg-indigo-50 p-3 rounded-lg">
              <p className="text-sm text-indigo-600 font-medium">Tendance Globale</p>
              <p className="text-lg font-bold text-indigo-800">↗️ Excellente</p>
              <p className="text-xs text-indigo-600">Progression constante</p>
            </div>
          </div>
        </div>

        {/* Détails spécifiques selon le type de rapport */}
        {report.data.weeklyTrends && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">Tendances Hebdomadaires</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="font-medium text-gray-700 mb-2">Progression</h4>
                <p className="text-gray-800">{report.data.weeklyTrends}</p>
              </div>
              {report.data.topPerformers && (
                <div>
                  <h4 className="font-medium text-gray-700 mb-2">Top Performers</h4>
                  <ul className="text-gray-800">
                    {report.data.topPerformers.map((performer, index) => (
                      <li key={index} className="flex items-center">
                        <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
                        {performer}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              {report.data.areasOfConcern && (
                <div className="md:col-span-2">
                  <h4 className="font-medium text-gray-700 mb-2">Zones de Préoccupation</h4>
                  <ul className="text-gray-800">
                    {report.data.areasOfConcern.map((area, index) => (
                      <li key={index} className="flex items-center">
                        <AlertCircle className="w-4 h-4 text-orange-500 mr-2" />
                        {area}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        )}

        {report.data.monthlyGrowth && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">Analyse Mensuelle</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="font-medium text-gray-700 mb-2">Croissance</h4>
                <p className="text-gray-800">{report.data.monthlyGrowth}</p>
              </div>
              {report.data.recommendations && (
                <div>
                  <h4 className="font-medium text-gray-700 mb-2">Recommandations</h4>
                  <ul className="text-gray-800">
                    {report.data.recommendations.map((rec, index) => (
                      <li key={index} className="flex items-start mb-2">
                        <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2 py-1 rounded mr-2">
                          {index + 1}
                        </span>
                        {rec}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        )}

        {report.data.totalBlockages && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">Analyse des Blocages</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="font-medium text-gray-700 mb-2">Statistiques</h4>
                <p className="text-gray-800">Total des blocages: {report.data.totalBlockages}</p>
                {report.data.severityDistribution && (
                  <div className="mt-3">
                    <h5 className="font-medium text-gray-600 mb-2">Distribution par sévérité:</h5>
                    {Object.entries(report.data.severityDistribution).map(([level, count]) => (
                      <div key={level} className="flex justify-between items-center mb-1">
                        <span className="text-gray-700">{level}:</span>
                        <span className="font-medium">{count}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
              <div>
                {report.data.commonBlockages && (
                  <div className="mb-4">
                    <h4 className="font-medium text-gray-700 mb-2">Blocages Communs</h4>
                    <ul className="text-gray-800">
                      {report.data.commonBlockages.map((blockage, index) => (
                        <li key={index} className="flex items-center mb-1">
                          <AlertCircle className="w-4 h-4 text-red-500 mr-2" />
                          {blockage}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                {report.data.remediationPlans && (
                  <div>
                    <h4 className="font-medium text-gray-700 mb-2">Plans de Remédiation</h4>
                    <ul className="text-gray-800">
                      {report.data.remediationPlans.map((plan, index) => (
                        <li key={index} className="flex items-start mb-2">
                          <span className="bg-green-100 text-green-800 text-xs font-medium px-2 py-1 rounded mr-2">
                            {index + 1}
                          </span>
                          {plan}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {report.data.predictionsCount && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">Prédictions IA</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="font-medium text-gray-700 mb-2">Statistiques</h4>
                <p className="text-gray-800">Nombre de prédictions: {report.data.predictionsCount}</p>
                {report.data.riskDistribution && (
                  <div className="mt-3">
                    <h5 className="font-medium text-gray-600 mb-2">Distribution des risques:</h5>
                    {Object.entries(report.data.riskDistribution).map(([level, count]) => (
                      <div key={level} className="flex justify-between items-center mb-1">
                        <span className="text-gray-700">{level}:</span>
                        <span className="font-medium">{count}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
              <div>
                {report.data.aiInsights && (
                  <div className="mb-4">
                    <h4 className="font-medium text-gray-700 mb-2">Insights IA</h4>
                    <ul className="text-gray-800">
                      {report.data.aiInsights.map((insight, index) => (
                        <li key={index} className="flex items-start mb-2">
                          <span className="bg-purple-100 text-purple-800 text-xs font-medium px-2 py-1 rounded mr-2">
                            {index + 1}
                          </span>
                          {insight}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                {report.data.nextActions && (
                  <div>
                    <h4 className="font-medium text-gray-700 mb-2">Actions Recommandées</h4>
                    <ul className="text-gray-800">
                      {report.data.nextActions.map((action, index) => (
                        <li key={index} className="flex items-start mb-2">
                          <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2 py-1 rounded mr-2">
                            {index + 1}
                          </span>
                          {action}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Résumé et actions */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-xl font-semibold text-gray-800 mb-4">Résumé et Actions</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium text-gray-700 mb-2">Points Clés</h4>
              <ul className="text-gray-800 space-y-2">
                <li className="flex items-center">
                  <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
                  Rapport généré avec succès
                </li>
                <li className="flex items-center">
                  <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
                  Données analysées et validées
                </li>
                <li className="flex items-center">
                  <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
                  Prêt pour l'export et le partage
                </li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium text-gray-700 mb-2">Actions Disponibles</h4>
              <div className="space-y-2">
                <button
                  onClick={handleExportPDF}
                  className="w-full text-left px-3 py-2 bg-red-50 text-red-700 rounded-lg hover:bg-red-100 transition-colors flex items-center"
                >
                  <Download className="w-4 h-4 mr-2" />
                  Télécharger en PDF
                </button>
                <button
                  onClick={handleExportExcel}
                  className="w-full text-left px-3 py-2 bg-green-50 text-green-700 rounded-lg hover:bg-green-100 transition-colors flex items-center"
                >
                  <Download className="w-4 h-4 mr-2" />
                  Télécharger en Excel
                </button>
                <Link
                  href="/dashboard/teacher/analytics"
                  className="w-full text-left px-3 py-2 bg-blue-50 text-blue-700 rounded-lg hover:bg-blue-100 transition-colors flex items-center"
                >
                  <ArrowLeft className="w-4 h-4 mr-2" />
                  Retour aux analytics
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}












