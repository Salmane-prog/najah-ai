'use client';

import Sidebar from '../../../components/Sidebar';
import { useAuth } from '../../../hooks/useAuth';
import NotificationBell from '../../../components/NotificationBell';
import {
  QuizWidget,
  BadgesWidget,
  AnalyticsWidget,
  RecommendationsWidget,
  MessagesWidget,
  AssignedQuizzesWidget,
  EnhancedQuizWidget,
  ScoreTestWidget,
  ScoreCorrectionWidget,
  AdvancedAnalyticsWidget,
  HomeworkWidget,
  EnhancedHomeworkWidget,
  CalendarWidget,
  ModernCalendarWidget,
  GamificationWidget,
  ActivityWidget,
  CorrectionsWidget,
  LearningGoalsWidget,
  AdvancedAIWidget,
  CollaborationWidget,
  AIAdvancedWidget,
  ReportsWidget,
  UnifiedProgressWidget,
  UnifiedStatsWidget,
  InitialAssessmentWidget,
  LearningPathWidget,
  AIRecommendationsWidget,
  StudentMessagesWidget
} from '../../../components/widgets';
import EnhancedChartsWidget from '../../../components/widgets/EnhancedChartsWidget';
import SimpleIcon, { SimpleIconWithBackground } from '../../../components/ui/SimpleIcon';
import React, { useState, useEffect } from 'react';
import { useStudentDashboard } from '../../../hooks/useStudentDashboard';
import { useAutoBadges } from '../../../hooks/useAutoBadges';
import { ScoreCalculator } from '../../../utils/scoreCalculator';
import { getStudentDashboardDataWithFallback } from '../../../services/studentDashboardService';
import { getStudentQuizzesWithFallback } from '../../../services/quizService';
import { getUserMessagesWithFallback, getUserNotificationsWithFallback } from '../../../services/messagingService';
import { getUserCalendarEventsWithFallback } from '../../../services/calendarService';
import { DashboardMetricsService, DashboardMetrics } from '../../../services/dashboardMetricsService';
import BadgeNotification from '../../../components/widgets/BadgeNotification';

// Composant de feedback pour les quiz
function QuizFeedbackModal({ feedback, onClose }: { feedback: any, onClose: () => void }) {
  return (
    <div className="modal-unified">
      <div className="modal-unified-content max-w-md w-full mx-4">
        <div className="modal-unified-header">
          <h3 className="text-lg font-bold text-primary mb-0">Feedback du Quiz</h3>
        </div>
        <div className="modal-unified-body">
          <div className="space-y-3">
            {feedback.recommendations?.map((reco: any, index: number) => (
              <div key={index} className="flex items-start space-x-3 p-3 bg-primary-50 rounded-lg">
                <div className="icon-status icon-status-online mt-2 flex-shrink-0"></div>
                <div className="flex-1">
                  <p className="text-sm text-primary">{reco.description}</p>
                  <span className="badge-unified badge-unified-primary mt-2">
                    {reco.priority}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
        <div className="modal-unified-footer">
          <button
            onClick={onClose}
            className="btn-unified btn-unified-primary"
          >
            Fermer
          </button>
        </div>
      </div>
    </div>
  );
}

export default function StudentDashboard() {
  const { user, token } = useAuth();
  const [showFeedback, setShowFeedback] = useState(true);
  const [realData, setRealData] = useState<any>(null);
  const [realLoading, setRealLoading] = useState(false);
  const [realError, setRealError] = useState<string | null>(null);
  const [dashboardMetrics, setDashboardMetrics] = useState<DashboardMetrics | null>(null);
  const [metricsLoading, setMetricsLoading] = useState(false);
  
  // Hook pour les badges automatiques
  const { 
    hasNewBadges, 
    newBadgesCount, 
    currentLevel, 
    totalPoints, 
    totalTests,
    forceCheck: forceCheckBadges 
  } = useAutoBadges();
  
  // Utilisation du hook unifié (fallback)
  const { 
    data, 
    loading, 
    error, 
    stats, 
    gamification, 
    quizzes, 
    assignedQuizzes, 
    recentActivity, 
    recommendations, 
    badges,
    activityStats,
    correctionStats,
    messages
  } = useStudentDashboard();

  // Récupération des vraies données
  useEffect(() => {
    const fetchRealData = async () => {
      if (!token || !user?.id) return;
      
      setRealLoading(true);
      setRealError(null);
      
      try {
        
        // Récupérer toutes les données en parallèle
        const [dashboardData, quizData, messagesData, notificationsData, calendarData] = await Promise.all([
          getStudentDashboardDataWithFallback(token, user.id),
          getStudentQuizzesWithFallback(token, user.id),
          getUserMessagesWithFallback(token, user.id),
          getUserNotificationsWithFallback(token, user.id),
          getUserCalendarEventsWithFallback(token, user.id)
        ]);

        const combinedData = {
          ...dashboardData,
          quizzes: quizData.completed_quizzes,
          assignedQuizzes: quizData.assigned_quizzes,
          messages: messagesData,
          notifications: notificationsData,
          calendarEvents: calendarData
        };

        setRealData(combinedData);
        
      } catch (error) {
        setRealError(error instanceof Error ? error.message : 'Erreur inconnue');
      } finally {
        setRealLoading(false);
      }
    };

    fetchRealData();
  }, [token, user?.id]);

  // Récupération des métriques unifiées du dashboard
  useEffect(() => {
    const fetchDashboardMetrics = async () => {
      if (!token || !user?.id) return;
      
      setMetricsLoading(true);
      
      try {
        
        const metrics = await DashboardMetricsService.getDashboardMetrics(token, user.id);
        setDashboardMetrics(metrics);
        
        
      } catch (error) {
        // Ne pas bloquer l'affichage si les métriques échouent
      } finally {
        setMetricsLoading(false);
      }
    };

    fetchDashboardMetrics();
    
    // Rafraîchir les métriques toutes les 30 secondes
    const interval = setInterval(fetchDashboardMetrics, 30000);
    
    // Rafraîchir aussi quand la page redevient visible
    const handleVisibilityChange = () => {
      if (!document.hidden) {
        fetchDashboardMetrics();
      }
    };
    
    document.addEventListener('visibilitychange', handleVisibilityChange);
    
    return () => {
      clearInterval(interval);
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, [token, user?.id]);

  if (!user?.id) {
    return (
      <div className="flex min-h-screen bg-bg-secondary">
        <Sidebar />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-danger text-lg font-bold">Erreur : utilisateur non connecté ou id manquant.</div>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex min-h-screen bg-bg-secondary">
        <Sidebar />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-primary animate-pulse text-xl font-bold">Chargement du dashboard...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex min-h-screen bg-bg-secondary">
        <Sidebar />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-danger text-lg font-bold">{error}</div>
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="flex min-h-screen bg-bg-secondary">
        <div className="flex-1 flex items-center justify-center">
          <div className="text-danger text-lg font-bold">Aucune donnée reçue du backend.</div>
        </div>
      </div>
    );
  }

  // Utiliser les vraies données si disponibles, sinon les données de fallback
  const finalData = realData || data;
  const finalQuizzes = realData?.quizzes || quizzes || [];
  const finalAssignedQuizzes = realData?.assignedQuizzes || assignedQuizzes || [];
  const finalMessages = realData?.messages || messages || [];
  const finalNotifications = realData?.notifications || [];
  const finalCalendarEvents = realData?.calendarEvents || [];

  // Calcul des statistiques avec ScoreCalculator
  const quizResults = finalQuizzes;
  const correctedQuizResults = ScoreCalculator.fixMaxScoreIssue(quizResults);
  const calculatedStats = ScoreCalculator.calculateGlobalStats(correctedQuizResults);

  // Afficher un indicateur si on utilise les vraies données
  const isUsingRealData = !!realData;

  return (
    <div className="flex min-h-screen bg-bg-secondary">
      <Sidebar />
      <div className="flex-1 overflow-auto pl-0 md:pl-56">
        <div className="p-6">
          {/* Affichage du feedback avancé si présent */}
          {data.feedback && showFeedback && (
            <QuizFeedbackModal feedback={data.feedback} onClose={() => setShowFeedback(false)} />
          )}
          
          {/* Header personnalisé avec données unifiées */}
          <div className="mb-8 flex items-center justify-between flex-wrap gap-4 animate-slide-in-up">
            <div className="animate-slide-in-left">
              <h1 className="text-3xl font-bold text-primary mb-2">
                Bonjour, {user?.name || 'Étudiant'} ! <span className="animate-wave inline-block">👋</span>
              </h1>
              <p className="text-secondary">Prêt à apprendre et progresser ?</p>
              
            </div>
            <div className="flex items-center gap-4 animate-slide-in-right">
              <NotificationBell />
              <div className="text-right">
                <p className="text-sm text-muted">
                  Niveau {dashboardMetrics?.currentLevel || stats?.level || 1}
                  {dashboardMetrics && (
                    <span className="ml-2 text-xs text-green-600">
                      ({dashboardMetrics.currentXP}/{dashboardMetrics.nextLevelXP} XP)
                    </span>
                  )}
                </p>
                <p className="text-lg font-bold text-primary">
                  {dashboardMetrics?.levelProgress ? `${Math.round(dashboardMetrics.levelProgress)}%` : (stats?.rank || 'Débutant')}
                </p>
              </div>
              <SimpleIconWithBackground name="star" backgroundType="warning" size="lg" className="hover-lift-enhanced" />
            </div>
          </div>

          {/* Widget de statistiques unifiées */}
          <div className="mb-8 animate-scale-in">
            <UnifiedStatsWidget 
              stats={{
                quizzesCompleted: dashboardMetrics?.quizzesCompleted || stats?.completedQuizzes || 0,
                averageScore: dashboardMetrics?.averageScore || stats?.averageScore || 0,
                consecutiveDays: dashboardMetrics?.consecutiveDays || stats?.currentStreak || 0,
                badgesEarned: dashboardMetrics?.badgesEarned || badges?.length || 0,
                totalPoints: dashboardMetrics?.totalPoints || gamification?.points?.total_points || 0,
                challengesCompleted: dashboardMetrics?.challengesCompleted || gamification?.challenges?.completed_count || 0,
                totalQuizzes: dashboardMetrics?.totalQuizzes || stats?.totalQuizzes || 0,
                bestScore: dashboardMetrics?.bestScore || stats?.bestScore || 0
              }}
              loading={metricsLoading}
              isRealData={!!dashboardMetrics}
            />
          </div>


          {/* Widgets prioritaires - Évaluation Initiale et Parcours d'Apprentissage */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
            {/* Widget Évaluation Initiale */}
            <div className="animate-fade-in-scale animate-delay-200">
              <InitialAssessmentWidget className="h-full" />
            </div>
            
            {/* Widget Parcours d'Apprentissage */}
            <div className="animate-fade-in-scale animate-delay-300">
              <LearningPathWidget className="h-full" />
            </div>
          </div>

          {/* Grille principale des widgets */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
            {/* Colonne gauche */}
            <div className="space-y-8">
              {/* Widget de graphiques améliorés */}
              <div className="animate-fade-in-scale animate-delay-200">
                <EnhancedChartsWidget className="h-full" />
              </div>

              {/* Widget d'activité récente */}
              <div className="card-unified animate-fade-in-scale animate-delay-300">
                <div className="card-unified-header">
                  <h2 className="text-xl font-bold text-primary mb-0">Activité Récente</h2>
                </div>
                <div className="card-unified-body">
                <div className="space-y-4">
                  {recentActivity && recentActivity.length > 0 ? (
                    recentActivity.slice(0, 5).map((activity: any, index: number) => (
                      <div
                        key={activity.id}
                        className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg hover-focus transition-all duration-200"
                        style={{ animationDelay: `${index * 100}ms` }}
                      >
                        <div className="icon-status icon-status-online"></div>
                        <div className="flex-1">
                          <p className="text-sm text-primary">{activity.description}</p>
                          <p className="text-xs text-muted">{activity.timestamp}</p>
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="text-center py-8 text-muted">
                      <p>Aucune activité récente</p>
                      <p className="text-sm">Commencez à étudier pour voir vos activités ici</p>
                    </div>
                  )}
                </div>
                </div>
              </div>

              {/* Widget de quiz assignés amélioré */}
              <div className="animate-fade-in-scale animate-delay-400">
                <EnhancedQuizWidget 
                  className="h-full" 
                  assignedQuizzes={assignedQuizzes}
                />
              </div>
            </div>

            {/* Colonne centrale */}
            <div className="space-y-8">
              {/* Widget de calendrier moderne */}
              <div className="animate-fade-in-scale animate-delay-500">
                <ModernCalendarWidget className="h-full" />
              </div>

              {/* Widget de devoirs amélioré */}
              <div className="animate-fade-in-scale animate-delay-600">
                <EnhancedHomeworkWidget className="h-full" />
              </div>

              {/* Widget de recommandations IA */}
              <div className="animate-fade-in-scale animate-delay-700">
                <AIRecommendationsWidget className="h-full" />
              </div>
            </div>

            {/* Colonne droite */}
            <div className="space-y-8">
              {/* Widget de badges */}
              <div className="card-unified animate-fade-in-scale animate-delay-800">
                <BadgesWidget 
                  badges={badges} 
                  className="h-full"
                />
              </div>

              {/* Widget de corrections */}
              <div className="card-unified animate-fade-in-scale animate-delay-900">
                <CorrectionsWidget 
                  correctionData={correctionStats || {}}
                  className="h-full" 
                />
              </div>

              {/* Widget de messages */}
              <div className="animate-fade-in-scale animate-delay-1000">
                <StudentMessagesWidget className="h-full" />
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Notification des nouveaux badges */}
      <BadgeNotification
        badges={hasNewBadges ? ['Nouveau badge obtenu !'] : []}
        isVisible={hasNewBadges}
        onClose={() => {}} // Géré par le hook
        onDismiss={() => {}} // Géré par le hook
      />
    </div>
  );
} 