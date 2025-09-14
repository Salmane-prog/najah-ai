"use client";

import React, { useState, useEffect } from 'react';
import { useAuth  } from '../../hooks/useAuth';
import { StudentTheme, StudentComponents } from '../design-system/StudentTheme';
import { 
  Trophy, 
  TrendingUp, 
  BookOpen, 
  Target, 
  Award, 
  Clock, 
  CheckCircle,
  Play,
  BarChart3,
  MessageCircle,
  Bell,
  Star,
  Zap
} from 'lucide-react';

interface DashboardStats {
  totalQuizzes: number;
  completedQuizzes: number;
  averageScore: number;
  currentStreak: number;
  totalPoints: number;
  level: number;
  xpToNextLevel: number;
  currentXp: number;
  rank: string;
}

interface QuickAction {
  id: string;
  title: string;
  description: string;
  icon: React.ReactNode;
  href: string;
  color: string;
  badge?: string;
}

export default function EnhancedStudentDashboard() {
  const { user, token } = useAuth();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');

  // Actions rapides
  const quickActions: QuickAction[] = [
    {
      id: 'quiz',
      title: 'Commencer un Quiz',
      description: 'Testez vos connaissances',
      icon: <Target className="w-6 h-6" />,
      href: '/dashboard/student/mes-quiz',
      color: 'bg-blue-500',
      badge: 'Nouveau'
    },
    {
      id: 'assessment',
      title: 'Évaluation Initiale',
      description: 'Déterminez votre niveau',
      icon: <BarChart3 className="w-6 h-6" />,
      href: '/dashboard/student/assessment',
      color: 'bg-green-500'
    },
    {
      id: 'learning-path',
      title: 'Parcours d\'Apprentissage',
      description: 'Suivez votre progression',
      icon: <BookOpen className="w-6 h-6" />,
      href: '/dashboard/student/learning-path',
      color: 'bg-purple-500'
    },
    {
      id: 'messages',
      title: 'Messages',
      description: 'Communiquez avec vos professeurs',
      icon: <MessageCircle className="w-6 h-6" />,
      href: '/dashboard/messages',
      color: 'bg-orange-500'
    }
  ];

  useEffect(() => {
    if (user && token) {
      fetchDashboardData();
    }
  }, [user, token]);

  const fetchDashboardData = async () => {
    if (!token) return;
    
    try {
      setLoading(true);
      
      // Récupérer les données réelles depuis l'API
      const [statsRes, streakRes, gamificationRes] = await Promise.all([
        fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/student_performance/my-performance`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).catch(() => ({ ok: false, json: () => ({ total_quizzes: 0, average_score: 0 }) })),
        
        fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/gamification/learning-streak`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).catch(() => ({ ok: false, json: () => ({ current: 0 }) })),
        
        fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/gamification/user-progress`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).catch(() => ({ ok: false, json: () => ({ totalPoints: 0, level: 1, xpToNextLevel: 1000, currentXp: 0, rank: 'Débutant' }) }))
      ]);

      const statsData = await statsRes.json();
      const streakData = await streakRes.json();
      const gamificationData = await gamificationRes.json();
      
      setStats({
        totalQuizzes: statsData.total_quizzes || 0,
        completedQuizzes: statsData.total_quizzes || 0,
        averageScore: statsData.average_score || 0,
        currentStreak: streakData.current || 0,
        totalPoints: gamificationData.totalPoints || 0,
        level: gamificationData.level || 1,
        xpToNextLevel: gamificationData.xpToNextLevel || 1000,
        currentXp: gamificationData.currentXp || 0,
        rank: gamificationData.rank || 'Débutant'
      });
    } catch (error) {
      console.error('Erreur lors du chargement des données:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement de votre espace...</p>
        </div>
      </div>
    );
  }

  const progressToNextLevel = stats ? (stats.currentXp / stats.xpToNextLevel) * 100 : 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header avec animation */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                  <BookOpen className="w-5 h-5 text-white" />
                </div>
                <span className="text-xl font-bold text-gray-900">Najah AI</span>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <button className="relative p-2 text-gray-400 hover:text-gray-600 transition-colors">
                <Bell className="w-6 h-6" />
                <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full"></span>
              </button>
              
              <div className="flex items-center space-x-3">
                <div className="text-right">
                  <p className="text-sm font-medium text-gray-900">{user?.name || 'Étudiant'}</p>
                  <p className="text-xs text-gray-500">{stats?.rank || 'Étudiant'}</p>
                </div>
                <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                  <span className="text-white font-semibold text-sm">
                    {user?.name?.charAt(0) || 'E'}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                Bonjour, {user?.name || 'Étudiant'} ! 👋
              </h1>
              <p className="text-gray-600">Prêt à continuer votre apprentissage ?</p>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">{stats?.level || 1}</div>
                <div className="text-sm text-gray-500">Niveau</div>
              </div>
              <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center shadow-lg">
                <Trophy className="w-8 h-8 text-white" />
              </div>
            </div>
          </div>
        </div>

        {/* XP Progress Bar */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700">
              Progression vers le niveau {(stats?.level || 1) + 1}
            </span>
            <span className="text-sm text-gray-500">
              {stats?.currentXp || 0} / {stats?.xpToNextLevel || 1000} XP
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
            <div 
              className="bg-gradient-to-r from-blue-500 to-purple-600 h-3 rounded-full transition-all duration-1000 ease-out"
              style={{ width: `${progressToNextLevel}%` }}
            ></div>
          </div>
        </div>

        {/* Quick Actions Grid */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
            <Zap className="w-5 h-5 mr-2 text-yellow-500" />
            Actions Rapides
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {quickActions.map((action) => (
              <div
                key={action.id}
                className={`${StudentComponents.Card.interactive} p-6 group hover:scale-105 transition-all duration-200`}
              >
                <div className="flex items-start justify-between mb-4">
                  <div className={`${action.color} p-3 rounded-lg text-white`}>
                    {action.icon}
                  </div>
                  {action.badge && (
                    <span className="bg-red-500 text-white text-xs px-2 py-1 rounded-full">
                      {action.badge}
                    </span>
                  )}
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">{action.title}</h3>
                <p className="text-sm text-gray-600 mb-4">{action.description}</p>
                <a
                  href={action.href}
                  className="inline-flex items-center text-blue-600 hover:text-blue-700 font-medium text-sm group-hover:translate-x-1 transition-transform"
                >
                  Commencer
                  <Play className="w-4 h-4 ml-1" />
                </a>
              </div>
            ))}
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className={`${StudentComponents.Card.base} p-6`}>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Quiz Complétés</p>
                <p className="text-2xl font-bold text-gray-900">{stats?.completedQuizzes || 0}</p>
              </div>
              <CheckCircle className="w-8 h-8 text-green-500" />
            </div>
          </div>

          <div className={`${StudentComponents.Card.base} p-6`}>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Score Moyen</p>
                <p className="text-2xl font-bold text-gray-900">{stats?.averageScore || 0}%</p>
              </div>
              <TrendingUp className="w-8 h-8 text-blue-500" />
            </div>
          </div>

          <div className={`${StudentComponents.Card.base} p-6`}>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Série Actuelle</p>
                <p className="text-2xl font-bold text-gray-900">{stats?.currentStreak || 0} jours</p>
              </div>
              <Star className="w-8 h-8 text-yellow-500" />
            </div>
          </div>

          <div className={`${StudentComponents.Card.base} p-6`}>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Points Totaux</p>
                <p className="text-2xl font-bold text-gray-900">{stats?.totalPoints || 0}</p>
              </div>
              <Award className="w-8 h-8 text-purple-500" />
            </div>
          </div>
        </div>

        {/* Recent Activity */}
        <div className={`${StudentComponents.Card.base} p-6`}>
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Activité Récente</h2>
          <div className="space-y-4">
            {[
              { action: 'Quiz "Antigone" complété', score: 92, time: 'Il y a 2h' },
              { action: 'Évaluation initiale terminée', score: 85, time: 'Il y a 1j' },
              { action: 'Badge "Premier Quiz" obtenu', score: null, time: 'Il y a 2j' },
            ].map((activity, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                    <CheckCircle className="w-4 h-4 text-blue-600" />
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">{activity.action}</p>
                    <p className="text-sm text-gray-500">{activity.time}</p>
                  </div>
                </div>
                {activity.score && (
                  <span className="text-sm font-medium text-green-600">
                    {activity.score}%
                  </span>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
} 