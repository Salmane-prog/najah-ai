'use client';

import React, { useState, useEffect } from 'react';
import { useAuth  } from '../../../../hooks/useAuth';
import { Card } from '../../../../components/Card';
import Button from '../../../../components/Button';
import Sidebar from '../../../../components/Sidebar';
import ProgressChart from '../../../../components/analytics/ProgressChart';
import SubjectDistributionChart from '../../../../components/analytics/SubjectDistributionChart';
import DifficultyPerformanceChart from '../../../../components/analytics/DifficultyPerformanceChart';
import EngagementTrendChart from '../../../../components/analytics/EngagementTrendChart';
import ScoreDistributionChart from '../../../../components/analytics/ScoreDistributionChart';
import LearningTrendsChart from '../../../../components/analytics/LearningTrendsChart';
import AIPredictions from '../../../../components/analytics/AIPredictions';
import { realAnalyticsService } from '../../../../services/realAnalyticsService';
import { 
  BarChart3, 
  TrendingUp, 
  Users, 
  BookOpen, 
  Target,
  Calendar,
  Download,
  Eye,
  Filter,
  RefreshCw,
  PieChart,
  LineChart,
  Activity,
  Award,
  Clock,
  CheckCircle,
  AlertCircle
} from 'lucide-react';

interface LearningAnalytics {
  id: number;
  student_id: number;
  student_name: string;
  date: string;
  total_study_time: number;
  subjects_studied: string[];
  quizzes_taken: number;
  quizzes_passed: number;
  average_score: number;
  engagement_score: number;
}

interface PredictiveInsight {
  id: number;
  student_id: number;
  student_name: string;
  prediction_type: string;
  predicted_value: number;
  confidence: number;
  recommendation: string;
  risk_level: 'low' | 'medium' | 'high';
}

interface BlockageDetection {
  id: number;
  student_id: number;
  student_name: string;
  subject: string;
  topic: string;
  blockage_type: string;
  severity_level: number;
  description: string;
  detected_at: string;
}

export default function AnalyticsPage() {
  const { user, token } = useAuth();
  const [activeTab, setActiveTab] = useState('overview');
  const [analytics, setAnalytics] = useState<LearningAnalytics[]>([]);
  const [predictions, setPredictions] = useState<any>({ students: [] });
  const [blockages, setBlockages] = useState<BlockageDetection[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [dateRange, setDateRange] = useState('week');
  
  // États pour les données des graphiques
  const [weeklyProgressData, setWeeklyProgressData] = useState<any[]>([]);
  const [monthlyStatsData, setMonthlyStatsData] = useState<any[]>([]);
  const [difficultyPerformanceData, setDifficultyPerformanceData] = useState<any[]>([]);
  const [engagementTrendsData, setEngagementTrendsData] = useState<any[]>([]);
  const [scoreDistributionData, setScoreDistributionData] = useState<any[]>([]);
  const [learningTrendsData, setLearningTrendsData] = useState<any[]>([]);
  
  // États pour les modals
  const [showDetailsModal, setShowDetailsModal] = useState(false);
  const [selectedStudent, setSelectedStudent] = useState<PredictiveInsight | null>(null);
  const [showBlockageModal, setShowBlockageModal] = useState(false);
  const [selectedBlockage, setSelectedBlockage] = useState<BlockageDetection | null>(null);

  // Mock data pour la démonstration
  useEffect(() => {
    // Charger les données des graphiques depuis le backend
    const loadGraphData = async () => {
      try {
        if (token) {
          console.log('🚀 Chargement des données des graphiques...');
          
          // Utiliser les services pour récupérer les données
          const [weeklyData, monthlyData, difficultyData, engagementData, scoreData, learningData] = await Promise.all([
            realAnalyticsService.getWeeklyProgress(),
            realAnalyticsService.getMonthlyStats(),
            realAnalyticsService.getDifficultyPerformance(),
            realAnalyticsService.getEngagementTrends(),
            realAnalyticsService.getScoreDistribution(),
            realAnalyticsService.getLearningTrends()
          ]);

          console.log('📈 Données hebdomadaires reçues:', weeklyData);
          console.log('📊 Données mensuelles reçues:', monthlyData);
          console.log('🎯 Données de difficulté reçues:', difficultyData);
          console.log('📈 Données d\'engagement reçues:', engagementData);
          console.log('📊 Données de distribution reçues:', scoreData);
          console.log('📈 Données d\'apprentissage reçues:', learningData);
          
          // S'assurer que les données sont des tableaux
          setWeeklyProgressData(Array.isArray(weeklyData) ? weeklyData : []);
          setMonthlyStatsData(Array.isArray(monthlyData) ? monthlyData : []);
          setDifficultyPerformanceData(Array.isArray(difficultyData) ? difficultyData : []);
          setEngagementTrendsData(Array.isArray(engagementData) ? engagementData : []);
          setScoreDistributionData(Array.isArray(scoreData) ? scoreData : []);
          setLearningTrendsData(Array.isArray(learningData) ? learningData : []);
        }
      } catch (error) {
        console.error('❌ Erreur lors du chargement des données des graphiques:', error);
        // En cas d'erreur, initialiser avec des tableaux vides
        setWeeklyProgressData([]);
        setMonthlyStatsData([]);
        setDifficultyPerformanceData([]);
        setEngagementTrendsData([]);
        setScoreDistributionData([]);
        setLearningTrendsData([]);
      }
    };

    loadGraphData();

    // Charger les VRAIES données analytics depuis le backend
    const loadRealAnalytics = async () => {
      try {
        console.log('🚀 Chargement des VRAIES données analytics...');
        const realAnalytics = await realAnalyticsService.getDetailedAnalytics();
        console.log('✅ Analytics réelles reçues:', realAnalytics);
        setAnalytics(realAnalytics);
      } catch (error) {
        console.error('❌ Erreur lors du chargement des analytics:', error);
        // Fallback vers des données par défaut en cas d'erreur
        setAnalytics([]);
      }
    };

    // Charger les VRAIES prédictions IA depuis le backend
    const loadRealPredictions = async () => {
      try {
        console.log('🚀 Chargement des VRAIES prédictions IA...');
        const realPredictions = await realAnalyticsService.getAIPredictions();
        console.log('✅ Prédictions réelles reçues:', realPredictions);
        
        // Transformer les données pour le composant AIPredictions
        const transformedPredictions = {
          students: realPredictions.map((pred: any) => ({
            id: pred.student_id,
            name: pred.student_name,
            currentScore: pred.avg_score ?? 0,
            predictedScore: pred.predicted_value ?? 0,
            trend: pred.risk_level === 'low' ? 'up' : pred.risk_level === 'high' ? 'down' : 'stable',
            confidence: (pred.confidence ?? 0) * 100, // Convertir en pourcentage
            recommendations: [pred.recommendation ?? 'Aucune recommandation']
          }))
        };
        
        console.log('🔄 Prédictions transformées:', transformedPredictions);
        setPredictions(transformedPredictions);
      } catch (error) {
        console.error('❌ Erreur lors du chargement des prédictions:', error);
        // Fallback vers des données par défaut en cas d'erreur
        setPredictions({ students: [] });
      }
    };

    loadRealAnalytics();
    loadRealPredictions();

    // Charger les VRAIS blocages depuis le backend
    const loadBlockages = async () => {
      try {
        console.log('🚀 Chargement des VRAIS blocages depuis le backend...');
        const realBlockages = await realAnalyticsService.getLearningBlockages();
        console.log('✅ Blocages réels reçus:', realBlockages);
        
        // Convertir les données du backend au format du composant
        const convertedBlockages = realBlockages.map((blockage, index) => ({
          id: index + 1,
          student_id: blockage.studentId,
          student_name: blockage.studentName,
          subject: blockage.subject,
          topic: blockage.topic,
          blockage_type: blockage.tags[2] || 'conceptuel', // 3ème tag = type de blocage
          severity_level: blockage.level,
          description: blockage.difficulty,
          detected_at: blockage.date
        }));
        
        setBlockages(convertedBlockages);
        console.log('🎯 Blocages convertis:', convertedBlockages);
        
      } catch (error) {
        console.error('❌ Erreur lors du chargement des blocages:', error);
        // Fallback vers des données par défaut en cas d'erreur
        setBlockages([
          {
            id: 1,
            student_id: 1,
            student_name: "Erreur de chargement",
            subject: "Données non disponibles",
            topic: "Veuillez réessayer",
            blockage_type: "erreur",
            severity_level: 1,
            description: "Impossible de charger les blocages depuis le serveur",
            detected_at: "N/A"
          }
        ]);
      }
    };
    
    loadBlockages();
  }, []);

  const getRiskLevelColor = (level: string) => {
    switch (level) {
      case 'low': return 'text-green-600 bg-green-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      case 'high': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getSeverityColor = (level: number) => {
    if (level <= 2) return 'text-green-600 bg-green-100';
    if (level <= 3) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  // Nouvelle fonction pour ouvrir la modal
  const handleViewDetails = (prediction: PredictiveInsight) => {
    setSelectedStudent(prediction);
    setShowDetailsModal(true);
  };

  // Fonction pour ouvrir la modal de blocage
  const handleViewBlockageDetails = (blockage: BlockageDetection) => {
    setSelectedBlockage(blockage);
    setShowBlockageModal(true);
  };

  const [generatedReports, setGeneratedReports] = useState<any[]>([]);
  const [isGeneratingReport, setIsGeneratingReport] = useState<string | null>(null);

  const handleExportReport = (type: string) => {
    if (type === 'pdf' || type === 'excel') {
      // Export des rapports générés
      const availableReports = generatedReports.filter(report => report.status === 'completed');
      if (availableReports.length === 0) {
        alert('Aucun rapport disponible pour l\'export. Veuillez d\'abord générer des rapports.');
        return;
      }
      
      if (type === 'pdf') {
        handleExportToPDF(availableReports);
      } else {
        handleExportToExcel(availableReports);
      }
    } else {
      // Génération de nouveaux rapports
      generateReport(type);
    }
  };

  const generateReport = async (reportType: string) => {
    setIsGeneratingReport(reportType);
    
    try {
      // Simulation de la génération du rapport
      await new Promise(resolve => setTimeout(resolve, 2000 + Math.random() * 3000));
      
      const newReport = {
        id: Date.now(),
        type: reportType,
        name: getReportName(reportType),
        description: getReportDescription(reportType),
        status: 'completed',
        generatedAt: new Date().toISOString(),
        data: generateReportData(reportType),
        downloadUrl: `#report-${Date.now()}`
      };
      
      setGeneratedReports(prev => [newReport, ...prev]);
      
      // Notification de succès
      alert(`Rapport ${getReportName(reportType)} généré avec succès !`);
      
    } catch (error) {
      alert(`Erreur lors de la génération du rapport ${getReportName(reportType)}`);
    } finally {
      setIsGeneratingReport(null);
    }
  };

  const getReportName = (type: string) => {
    switch (type) {
      case 'weekly': return 'Rapport Hebdomadaire';
      case 'monthly': return 'Rapport Mensuel';
      case 'blockages': return 'Rapport de Blocages';
      case 'predictive': return 'Rapport Prédictif';
      default: return 'Rapport';
    }
  };

  const getReportDescription = (type: string) => {
    switch (type) {
      case 'weekly': return 'Résumé des performances de la semaine';
      case 'monthly': return 'Analyse complète du mois';
      case 'blockages': return 'Détection et recommandations';
      case 'predictive': return 'Analyses et prédictions IA';
      default: return 'Rapport généré';
    }
  };

  const generateReportData = (type: string) => {
    const baseData = {
      totalStudents: analytics.length,
      averageScore: Math.round(analytics.reduce((sum, a) => sum + a.average_score, 0) / analytics.length),
      averageEngagement: Math.round(analytics.reduce((sum, a) => sum + a.engagement_score, 0) / analytics.length),
      totalStudyTime: Math.round(analytics.reduce((sum, a) => sum + a.total_study_time, 0) / analytics.length),
      dateRange: dateRange
    };

    switch (type) {
      case 'weekly':
        return {
          ...baseData,
          weeklyTrends: 'Progression positive de 5.2%',
          topPerformers: analytics.slice(0, 3).map(a => a.student_name),
          areasOfConcern: ['Mathématiques - Équations', 'Français - Conjugaison']
        };
      case 'monthly':
        return {
          ...baseData,
          monthlyGrowth: 'Amélioration de 12.8%',
          subjectBreakdown: {
            'Mathématiques': 78.5,
            'Français': 82.3,
            'Sciences': 85.1,
            'Histoire': 79.8
          },
          recommendations: [
            'Renforcer les exercices d\'algèbre',
            'Développer la compréhension en lecture',
            'Encourager les projets scientifiques'
          ]
        };
      case 'blockages':
        return {
          ...baseData,
          totalBlockages: blockages.length,
          severityDistribution: {
            'Faible': blockages.filter(b => b.severity_level <= 2).length,
            'Moyen': blockages.filter(b => b.severity_level === 3).length,
            'Élevé': blockages.filter(b => b.severity_level >= 4).length
          },
          commonBlockages: ['Équations du second degré', 'Conjugaison des verbes'],
          remediationPlans: [
            'Séances de soutien en petits groupes',
            'Exercices d\'entraînement personnalisés',
            'Tutorat par les pairs'
          ]
        };
      case 'predictive':
        return {
          ...baseData,
          predictionsCount: predictions.length,
          riskDistribution: {
            'Faible': predictions.filter(p => p.risk_level === 'low').length,
            'Moyen': predictions.filter(p => p.risk_level === 'medium').length,
            'Élevé': predictions.filter(p => p.risk_level === 'high').length
          },
          aiInsights: [
            'Tendance positive pour 70% des étudiants',
            'Risque de décrochage identifié pour 2 étudiants',
            'Opportunités d\'amélioration en mathématiques'
          ],
          nextActions: [
            'Surveiller les étudiants à risque',
            'Planifier des interventions ciblées',
            'Adapter le contenu pédagogique'
          ]
        };
      default:
        return baseData;
    }
  };

  const handleExportToPDF = (reports: any[]) => {
    // Génération d'un PDF simulé
    const reportNames = reports.map(r => r.name).join(', ');
    
    // Créer le contenu du PDF
    const pdfContent = generatePDFContent(reports);
    
    // Créer et télécharger le fichier
    const blob = new Blob([pdfContent], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `rapports_analytics_${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
    
    alert(`Export PDF simulé réussi pour: ${reportNames}\n\nFichier téléchargé: rapports_analytics_${new Date().toISOString().split('T')[0]}.txt`);
  };

  const handleExportToExcel = (reports: any[]) => {
    // Génération d'un Excel simulé
    const reportNames = reports.map(r => r.name).join(', ');
    
    // Créer le contenu CSV (format Excel)
    const csvContent = generateCSVContent(reports);
    
    // Créer et télécharger le fichier
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `rapports_analytics_${new Date().toISOString().split('T')[0]}.csv`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
    
    alert(`Export Excel simulé réussi pour: ${reportNames}\n\nFichier téléchargé: rapports_analytics_${new Date().toISOString().split('T')[0]}.csv`);
  };

  const generatePDFContent = (reports: any[]) => {
    let content = 'NAJAH AI - RAPPORTS ANALYTICS\n';
    content += '=====================================\n\n';
    content += `Date de génération: ${new Date().toLocaleDateString('fr-FR')}\n`;
    content += `Nombre de rapports: ${reports.length}\n\n`;
    
    reports.forEach((report, index) => {
      content += `${index + 1}. ${report.name}\n`;
      content += `   Description: ${report.description}\n`;
      content += `   Généré le: ${new Date(report.generatedAt).toLocaleDateString('fr-FR')}\n`;
      content += `   Données:\n`;
      
      if (report.data) {
        Object.entries(report.data).forEach(([key, value]) => {
          if (typeof value === 'object') {
            content += `     ${key}:\n`;
            Object.entries(value).forEach(([subKey, subValue]) => {
              content += `       ${subKey}: ${subValue}\n`;
            });
          } else {
            content += `     ${key}: ${value}\n`;
          }
        });
      }
      content += '\n';
    });
    
    return content;
  };

  const generateCSVContent = (reports: any[]) => {
    let content = 'Nom,Description,Date de génération,Étudiants,Score moyen,Engagement,Temps d\'étude\n';
    
    reports.forEach(report => {
      const row = [
        report.name,
        report.description,
        new Date(report.generatedAt).toLocaleDateString('fr-FR'),
        report.data?.totalStudents || 'N/A',
        report.data?.averageScore ? `${report.data.averageScore}%` : 'N/A',
        report.data?.averageEngagement ? `${report.data.averageEngagement}%` : 'N/A',
        report.data?.totalStudyTime ? `${report.data.totalStudyTime} min` : 'N/A'
      ];
      content += row.map(field => `"${field}"`).join(',') + '\n';
    });
    
    return content;
  };

  const handleViewReport = (report: any) => {
    // Stocker le rapport à visualiser dans localStorage
    localStorage.setItem('viewingReport', JSON.stringify(report));
    // Ouvrir la page de visualisation dans un nouvel onglet
    window.open(`/dashboard/teacher/analytics/view-report/${report.id}`, '_blank');
  };

  const handleRefreshData = async () => {
    setIsLoading(true);
    try {
      console.log('🔄 Rafraîchissement des données...');
      
      // Recharger toutes les données
      await Promise.all([
        loadRealAnalytics(),
        loadRealPredictions(),
        loadBlockages(),
        loadGraphData()
      ]);
      
      console.log('✅ Données rafraîchies avec succès');
    } catch (error) {
      console.error('❌ Erreur lors du rafraîchissement:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 ml-56 p-8 overflow-y-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2 flex items-center">
            <BarChart3 className="mr-3 text-blue-600" size={32} />
            Analytics & Reporting
          </h1>
          <p className="text-gray-600">
            Tableaux de bord avancés, analyses prédictives et détection des blocages d'apprentissage
          </p>
        </div>

        {/* Contrôles */}
        <div className="flex justify-between items-center mb-6">
          <div className="flex space-x-4">
            <select
              value={dateRange}
              onChange={(e) => setDateRange(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="week">Cette semaine</option>
              <option value="month">Ce mois</option>
              <option value="quarter">Ce trimestre</option>
              <option value="year">Cette année</option>
            </select>
            
            <Button
              onClick={handleRefreshData}
              disabled={isLoading}
              className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-md flex items-center"
            >
              <RefreshCw className={`w-4 h-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
              Actualiser
            </Button>
          </div>

          <div className="flex space-x-2">
            <Button
              onClick={() => handleExportReport('pdf')}
              disabled={generatedReports.filter(r => r.status === 'completed').length === 0}
              className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Download className="w-4 h-4 mr-2" />
              Export PDF
              {generatedReports.filter(r => r.status === 'completed').length > 0 && (
                <span className="ml-2 bg-red-700 text-white text-xs px-2 py-1 rounded-full">
                  {generatedReports.filter(r => r.status === 'completed').length}
                </span>
              )}
            </Button>
            <Button
              onClick={() => handleExportReport('excel')}
              disabled={generatedReports.filter(r => r.status === 'completed').length === 0}
              className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Download className="w-4 h-4 mr-2" />
              Export Excel
              {generatedReports.filter(r => r.status === 'completed').length > 0 && (
                <span className="ml-2 bg-green-700 text-white text-xs px-2 py-1 rounded-full">
                  {generatedReports.filter(r => r.status === 'completed').length}
                </span>
              )}
            </Button>
          </div>
        </div>

        {/* Onglets */}
        <div className="mb-6">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              <button
                onClick={() => setActiveTab('overview')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'overview'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Vue d'ensemble
              </button>
              <button
                onClick={() => setActiveTab('predictions')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'predictions'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Prédictions IA
              </button>
              <button
                onClick={() => setActiveTab('blockages')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'blockages'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Détection de Blocages
              </button>
              <button
                onClick={() => setActiveTab('reports')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'reports'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Rapports
              </button>
            </nav>
          </div>
        </div>

        {/* Contenu des onglets */}
        {activeTab === 'overview' && (
          <div>
            <h2 className="text-2xl font-semibold text-gray-800 mb-6">Vue d'ensemble de la Classe</h2>
            
            {/* Métriques principales */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
              <Card className="p-6 text-center">
                <div className="text-3xl font-bold text-blue-600 mb-2">
                  {analytics.length}
                </div>
                <div className="text-gray-600">Étudiants Actifs</div>
              </Card>
              
              <Card className="p-6 text-center">
                <div className="text-3xl font-bold text-green-600 mb-2">
                  {analytics.length > 0 ? Math.round(analytics.reduce((sum, a) => sum + a.average_score, 0) / analytics.length) : 0}%
                </div>
                <div className="text-gray-600">Score Moyen</div>
              </Card>
              
              <Card className="p-6 text-center">
                <div className="text-3xl font-bold text-purple-600 mb-2">
                  {analytics.length > 0 ? Math.round(analytics.reduce((sum, a) => sum + a.engagement_score, 0) / analytics.length) : 0}%
                </div>
                <div className="text-gray-600">Engagement Moyen</div>
              </Card>
              
              <Card className="p-6 text-center">
                <div className="text-3xl font-bold text-orange-600 mb-2">
                  {analytics.length > 0 ? Math.round(analytics.reduce((sum, a) => sum + a.total_study_time, 0) / analytics.length) : 0} min
                </div>
                <div className="text-gray-600">Temps d'Étude Moyen</div>
              </Card>
            </div>

            {/* Graphiques */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
              <Card className="p-6">
                <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
                  <TrendingUp className="w-5 h-5 mr-2 text-blue-500" />
                  Progression des Scores
                </h3>
                <ProgressChart 
                  data={weeklyProgressData} 
                  title="Progression des Scores"
                  type="line"
                />
              </Card>
              
              <Card className="p-6">
                <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
                  <PieChart className="w-5 h-5 mr-2 text-green-500" />
                  Répartition par Matière
                </h3>
                <SubjectDistributionChart 
                  data={monthlyStatsData} 
                />
              </Card>
            </div>

            {/* Nouveaux graphiques supplémentaires */}
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-8 mb-8">
              <Card className="p-6 min-h-[400px]">
                <h3 className="text-xl font-semibold text-gray-800 mb-6 flex items-center">
                  <BarChart3 className="w-5 h-5 mr-2 text-orange-500" />
                  Performance par Difficulté
                </h3>
                <div className="h-80">
                  <DifficultyPerformanceChart 
                    data={difficultyPerformanceData} 
                    title="Performance par Difficulté"
                  />
                </div>
              </Card>
              
              <Card className="p-6 min-h-[400px]">
                <h3 className="text-xl font-semibold text-gray-800 mb-6 flex items-center">
                  <Activity className="w-5 h-5 mr-2 text-purple-500" />
                  Tendance d'Engagement
                </h3>
                <div className="h-80">
                  <EngagementTrendChart 
                    data={engagementTrendsData} 
                    title="Tendance d'Engagement"
                  />
                </div>
              </Card>
            </div>

            {/* Deuxième ligne de graphiques */}
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-8 mb-8">
              <Card className="p-6 min-h-[400px]">
                <h3 className="text-xl font-semibold text-gray-800 mb-6 flex items-center">
                  <Target className="w-5 h-5 mr-2 text-red-500" />
                  Distribution des Scores
                </h3>
                <div className="h-80">
                  <ScoreDistributionChart 
                    data={scoreDistributionData} 
                    title="Distribution des Scores"
                  />
                </div>
              </Card>
              
              <Card className="p-6 min-h-[400px]">
                <h3 className="text-xl font-semibold text-gray-800 mb-6 flex items-center">
                  <TrendingUp className="w-5 h-5 mr-2 text-indigo-500" />
                  Tendances d'Apprentissage
                </h3>
                <div className="h-80">
                  <LearningTrendsChart 
                    data={learningTrendsData} 
                    title="Tendances d'Apprentissage"
                  />
                </div>
              </Card>
            </div>

            {/* Tableau des performances */}
            <Card className="p-6">
              <h3 className="text-xl font-semibold text-gray-800 mb-4">Performances Détaillées</h3>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Étudiant
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Temps d'Étude
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Quiz Passés
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Score Moyen
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Engagement
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {analytics.length > 0 ? (
                      analytics.map((student) => (
                        <tr key={student.id}>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm font-medium text-gray-900">{student.student_name}</div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm text-gray-900">{student.total_study_time} min</div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm text-gray-900">{student.quizzes_passed}/{student.quizzes_taken}</div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm text-gray-900">{student.average_score}%</div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm text-gray-900">{student.engagement_score}%</div>
                          </td>
                        </tr>
                      ))
                    ) : (
                      <tr>
                        <td colSpan={5} className="px-6 py-8 text-center text-gray-500">
                          <div className="flex flex-col items-center">
                            <div className="w-16 h-16 mb-4 bg-gray-100 rounded-full flex items-center justify-center">
                              <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
                              </svg>
                            </div>
                            <p className="text-lg font-medium">Aucune donnée disponible</p>
                            <p className="text-sm">Les performances des étudiants apparaîtront ici</p>
                          </div>
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </Card>
          </div>
        )}

        {activeTab === 'predictions' && (
          <div>
            <AIPredictions />
          </div>
        )}

        {activeTab === 'blockages' && (
          <div>
            <h2 className="text-2xl font-semibold text-gray-800 mb-6">Détection de Blocages</h2>
            
            <div className="grid gap-6">
              {blockages.map((blockage) => (
                <Card key={blockage.id} className="p-6">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center mb-2">
                        <h3 className="text-xl font-semibold text-gray-800 mr-3">
                          {blockage.student_name}
                        </h3>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSeverityColor(blockage.severity_level)}`}>
                          Niveau {blockage.severity_level}/5
                        </span>
                      </div>
                      
                      <div className="mb-3">
                        <p className="text-gray-600 font-medium">{blockage.subject} - {blockage.topic}</p>
                        <p className="text-gray-800">{blockage.description}</p>
                      </div>
                      
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                        <div className="flex items-center">
                          <BookOpen className="w-4 h-4 mr-2 text-blue-500" />
                          <span className="text-gray-600">{blockage.subject}</span>
                        </div>
                        <div className="flex items-center">
                          <Target className="w-4 h-4 mr-2 text-green-500" />
                          <span className="text-gray-600">{blockage.topic}</span>
                        </div>
                        <div className="flex items-center">
                          <AlertCircle className="w-4 h-4 mr-2 text-orange-500" />
                          <span className="text-gray-600">{blockage.blockage_type}</span>
                        </div>
                        <div className="flex items-center">
                          <Clock className="w-4 h-4 mr-2 text-purple-500" />
                          <span className="text-gray-600">{blockage.detected_at}</span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex space-x-2 ml-4">
                      <Button
                        onClick={() => handleViewBlockageDetails(blockage)}
                        className="bg-blue-600 hover:bg-blue-700 text-white p-2 rounded-md"
                        title="Voir les détails du blocage"
                      >
                        <Eye className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'reports' && (
          <div>
            <h2 className="text-2xl font-semibold text-gray-800 mb-6">Rapports Automatisés</h2>
            
            <div className="grid gap-6">
              {/* Rapports Disponibles */}
              <Card className="p-6">
                <h3 className="text-xl font-semibold text-gray-800 mb-4">Rapports Disponibles</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="border border-gray-200 rounded-lg p-4">
                    <h4 className="font-medium text-gray-800 mb-2">Rapport Hebdomadaire</h4>
                    <p className="text-gray-600 text-sm mb-3">Résumé des performances de la semaine</p>
                    <Button
                      onClick={() => handleExportReport('weekly')}
                      disabled={isGeneratingReport === 'weekly'}
                      className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm disabled:opacity-50"
                    >
                      {isGeneratingReport === 'weekly' ? (
                        <>
                          <RefreshCw className="w-4 h-4 mr-1 animate-spin" />
                          Génération...
                        </>
                      ) : (
                        'Générer'
                      )}
                    </Button>
                  </div>
                  
                  <div className="border border-gray-200 rounded-lg p-4">
                    <h4 className="font-medium text-gray-800 mb-2">Rapport Mensuel</h4>
                    <p className="text-gray-600 text-sm mb-3">Analyse complète du mois</p>
                    <Button
                      onClick={() => handleExportReport('monthly')}
                      disabled={isGeneratingReport === 'monthly'}
                      className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm disabled:opacity-50"
                    >
                      {isGeneratingReport === 'monthly' ? (
                        <>
                          <RefreshCw className="w-4 h-4 mr-1 animate-spin" />
                          Génération...
                        </>
                      ) : (
                        'Générer'
                      )}
                    </Button>
                  </div>
                  
                  <div className="border border-gray-200 rounded-lg p-4">
                    <h4 className="font-medium text-gray-800 mb-2">Rapport de Blocages</h4>
                    <p className="text-gray-600 text-sm mb-3">Détection et recommandations</p>
                    <Button
                      onClick={() => handleExportReport('blockages')}
                      disabled={isGeneratingReport === 'blockages'}
                      className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm disabled:opacity-50"
                    >
                      {isGeneratingReport === 'blockages' ? (
                        <>
                          <RefreshCw className="w-4 h-4 mr-1 animate-spin" />
                          Génération...
                        </>
                      ) : (
                        'Générer'
                      )}
                    </Button>
                  </div>
                  
                  <div className="border border-gray-200 rounded-lg p-4">
                    <h4 className="font-medium text-gray-800 mb-2">Rapport Prédictif</h4>
                    <p className="text-gray-600 text-sm mb-3">Analyses et prédictions IA</p>
                    <Button
                      onClick={() => handleExportReport('predictive')}
                      disabled={isGeneratingReport === 'predictive'}
                      className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm disabled:opacity-50"
                    >
                      {isGeneratingReport === 'predictive' ? (
                        <>
                          <RefreshCw className="w-4 h-4 mr-1 animate-spin" />
                          Génération...
                        </>
                      ) : (
                        'Générer'
                      )}
                    </Button>
                  </div>
                </div>
              </Card>

              {/* Rapports Générés */}
              {generatedReports.length > 0 && (
                <Card className="p-6">
                  <h3 className="text-xl font-semibold text-gray-800 mb-4">Rapports Générés</h3>
                  <div className="space-y-4">
                    {generatedReports.map((report) => (
                      <div key={report.id} className="border border-gray-200 rounded-lg p-4">
                        <div className="flex justify-between items-start">
                          <div className="flex-1">
                            <div className="flex items-center mb-2">
                              <h4 className="font-medium text-gray-800 mr-3">{report.name}</h4>
                              <span className="px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                {report.status === 'completed' ? 'Terminé' : 'En cours'}
                              </span>
                            </div>
                            <p className="text-gray-600 text-sm mb-2">{report.description}</p>
                            <p className="text-gray-500 text-xs">
                              Généré le {new Date(report.generatedAt).toLocaleDateString('fr-FR', {
                                day: '2-digit',
                                month: '2-digit',
                                year: 'numeric',
                                hour: '2-digit',
                                minute: '2-digit'
                              })}
                            </p>
                          </div>
                          <div className="flex space-x-2">
                            <Button
                              onClick={() => handleViewReport(report)}
                              className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm"
                              title="Visualiser le rapport"
                            >
                              <Eye className="w-4 h-4 mr-1" />
                              Voir
                            </Button>
                            <Button
                              onClick={() => handleExportReport('pdf')}
                              className="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded text-sm"
                              title="Télécharger en PDF"
                            >
                              <Download className="w-4 h-4 mr-1" />
                              PDF
                            </Button>
                            <Button
                              onClick={() => handleExportReport('excel')}
                              className="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded text-sm"
                              title="Télécharger en Excel"
                            >
                              <Download className="w-4 h-4 mr-1" />
                              Excel
                            </Button>
                          </div>
                        </div>
                        
                        {/* Aperçu des données du rapport */}
                        {report.data && (
                          <div className="mt-4 p-3 bg-gray-50 rounded-lg">
                            <h5 className="font-medium text-gray-700 mb-2">Aperçu des données :</h5>
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
                              {report.data.totalStudents && (
                                <div>
                                  <span className="text-gray-600">Étudiants :</span>
                                  <span className="font-medium ml-1">{report.data.totalStudents}</span>
                                </div>
                              )}
                              {report.data.averageScore && (
                                <div>
                                  <span className="text-gray-600">Score moyen :</span>
                                  <span className="font-medium ml-1">{report.data.averageScore}%</span>
                                </div>
                              )}
                              {report.data.averageEngagement && (
                                <div>
                                  <span className="text-gray-600">Engagement :</span>
                                  <span className="font-medium ml-1">{report.data.averageEngagement}%</span>
                                </div>
                              )}
                              {report.data.totalStudyTime && (
                                <div>
                                  <span className="text-gray-600">Temps d'étude :</span>
                                  <span className="font-medium ml-1">{report.data.totalStudyTime} min</span>
                                </div>
                              )}
                            </div>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </Card>
              )}

              {/* Message d'information */}
              {generatedReports.length === 0 && (
                <Card className="p-6">
                  <div className="text-center py-8">
                    <BarChart3 className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 mb-2">Aucun rapport généré</h3>
                    <p className="text-gray-500">
                      Utilisez les boutons ci-dessus pour générer vos premiers rapports d'analytics.
                    </p>
                  </div>
                </Card>
              )}
            </div>
          </div>
        )}
      </div>

        {/* Modal de détails de l'étudiant */}
        {showDetailsModal && selectedStudent && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 w-full max-w-4xl max-h-[90vh] overflow-y-auto">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-900">
                  Détails de l'Étudiant : {selectedStudent.student_name}
                </h2>
                <button
                  onClick={() => setShowDetailsModal(false)}
                  className="text-gray-400 hover:text-gray-600 text-2xl"
                >
                  ×
                </button>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Informations de prédiction */}
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-gray-800 border-b pb-2">
                    Prédiction IA
                  </h3>
                  
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="font-medium text-gray-600">Type de Prédiction:</span>
                      <span className="text-gray-800">{selectedStudent.prediction_type}</span>
                    </div>
                    
                    <div className="flex justify-between">
                      <span className="font-medium text-gray-600">Valeur Prédite:</span>
                      <span className="text-blue-600 font-bold">{selectedStudent.predicted_value}</span>
                    </div>
                    
                    <div className="flex justify-between">
                      <span className="font-medium text-gray-600">Niveau de Confiance:</span>
                      <span className="text-green-600 font-bold">{(selectedStudent.confidence * 100).toFixed(1)}%</span>
                    </div>
                    
                    <div className="flex justify-between">
                      <span className="font-medium text-gray-600">Niveau de Risque:</span>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getRiskLevelColor(selectedStudent.risk_level)}`}>
                        {selectedStudent.risk_level}
                      </span>
                    </div>
                  </div>

                  <div className="mt-4 p-4 bg-blue-50 rounded-lg">
                    <h4 className="font-medium text-blue-800 mb-2">Recommandation IA:</h4>
                    <p className="text-blue-700">{selectedStudent.recommendation}</p>
                  </div>
                </div>

                {/* Informations de l'étudiant */}
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-gray-800 border-b pb-2">
                    Profil de l'Étudiant
                  </h3>
                  
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="font-medium text-gray-600">ID Étudiant:</span>
                      <span className="text-gray-800">{selectedStudent.student_id}</span>
                    </div>
                    
                    <div className="flex justify-between">
                      <span className="font-medium text-gray-600">Nom Complet:</span>
                      <span className="text-gray-800">{selectedStudent.student_name}</span>
                    </div>
                    
                    <div className="flex justify-between">
                      <span className="font-medium text-gray-600">Statut:</span>
                      <span className="text-green-600 font-medium">Actif</span>
                    </div>
                  </div>

                  {/* Actions recommandées */}
                  <div className="mt-4 p-4 bg-green-50 rounded-lg">
                    <h4 className="font-medium text-green-800 mb-2">Actions Recommandées:</h4>
                    <ul className="text-green-700 space-y-1 text-sm">
                      {selectedStudent.risk_level === 'low' && (
                        <>
                          <li>• Maintenir le niveau actuel</li>
                          <li>• Continuer le suivi régulier</li>
                          <li>• Encourager les bonnes pratiques</li>
                        </>
                      )}
                      {selectedStudent.risk_level === 'medium' && (
                        <>
                          <li>• Augmenter la surveillance</li>
                          <li>• Proposer un soutien supplémentaire</li>
                          <li>• Planifier des entretiens réguliers</li>
                        </>
                      )}
                      {selectedStudent.risk_level === 'high' && (
                        <>
                          <li>• Intervention immédiate requise</li>
                          <li>• Soutien personnalisé intensif</li>
                          <li>• Contact avec les parents</li>
                        </>
                      )}
                    </ul>
                  </div>
                </div>
              </div>

              {/* Boutons d'action */}
              <div className="flex justify-end space-x-3 mt-6 pt-4 border-t border-gray-200">
                <button
                  onClick={() => setShowDetailsModal(false)}
                  className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Fermer
                </button>
                <button
                  onClick={() => {
                    // TODO: Implémenter l'action de suivi
                    alert('Fonctionnalité de suivi à implémenter');
                  }}
                  className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Planifier un Suivi
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Modal de détails du blocage */}
        {showBlockageModal && selectedBlockage && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 w-full max-w-4xl max-h-[90vh] overflow-y-auto">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-900">
                  Détails du Blocage : {selectedBlockage.student_name}
                </h2>
                <button
                  onClick={() => setShowBlockageModal(false)}
                  className="text-gray-400 hover:text-gray-600 text-2xl"
                >
                  ×
                </button>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Informations de blocage */}
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-gray-800 border-b pb-2">
                    Détails du Blocage
                  </h3>
                  
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="font-medium text-gray-600">Étudiant:</span>
                      <span className="text-gray-800">{selectedBlockage.student_name}</span>
                    </div>
                    
                    <div className="flex justify-between">
                      <span className="font-medium text-gray-600">Matière:</span>
                      <span className="text-gray-800">{selectedBlockage.subject}</span>
                    </div>
                    
                    <div className="flex justify-between">
                      <span className="font-medium text-gray-600">Sujet:</span>
                      <span className="text-gray-800">{selectedBlockage.topic}</span>
                    </div>
                    
                    <div className="flex justify-between">
                      <span className="font-medium text-gray-600">Type de Blocage:</span>
                      <span className="text-gray-800">{selectedBlockage.blockage_type}</span>
                    </div>
                    
                    <div className="flex justify-between">
                      <span className="font-medium text-gray-600">Niveau de Gravité:</span>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSeverityColor(selectedBlockage.severity_level)}`}>
                        {selectedBlockage.severity_level}/5
                      </span>
                    </div>
                  </div>

                  <div className="mt-4 p-4 bg-red-50 rounded-lg">
                    <h4 className="font-medium text-red-800 mb-2">Description:</h4>
                    <p className="text-red-700">{selectedBlockage.description}</p>
                  </div>
                </div>

                {/* Actions recommandées */}
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-gray-800 border-b pb-2">
                    Plan de Remédiation
                  </h3>
                  
                  <div className="space-y-3">
                    <div className="flex items-center">
                      <CheckCircle className="w-5 h-5 mr-2 text-green-600" />
                      <span className="text-gray-800">• Surveiller l'assiduité de l'étudiant.</span>
                    </div>
                    <div className="flex items-center">
                      <CheckCircle className="w-5 h-5 mr-2 text-green-600" />
                      <span className="text-gray-800">• Proposer des exercices de révision spécifiques.</span>
                    </div>
                    <div className="flex items-center">
                      <CheckCircle className="w-5 h-5 mr-2 text-green-600" />
                      <span className="text-gray-800">• Organiser des séances de soutien individuelle.</span>
                    </div>
                    <div className="flex items-center">
                      <CheckCircle className="w-5 h-5 mr-2 text-green-600" />
                      <span className="text-gray-800">• Encourager l'autonomie et la résolution de problèmes.</span>
                    </div>
                    <div className="flex items-center">
                      <CheckCircle className="w-5 h-5 mr-2 text-green-600" />
                      <span className="text-gray-800">• Planifier des entretiens réguliers avec l'étudiant.</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Boutons d'action */}
              <div className="flex justify-end space-x-3 mt-6 pt-4 border-t border-gray-200">
                <button
                  onClick={() => setShowBlockageModal(false)}
                  className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Fermer
                </button>
                <button
                  onClick={() => {
                    // TODO: Implémenter l'action de suivi
                    alert('Fonctionnalité de suivi à implémenter');
                  }}
                  className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Planifier un Suivi
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  }
