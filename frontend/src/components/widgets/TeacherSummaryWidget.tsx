"use client";

import React, { useState, useEffect } from 'react';
import { 
  Users, 
  BookOpen, 
  Award, 
  Target, 
  TrendingUp, 
  TrendingDown,
  Activity,
  Calendar,
  MessageSquare,
  FileText
} from 'lucide-react';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface SummaryStats {
  totalStudents: number;
  totalClasses: number;
  totalQuizzes: number;
  totalContents: number;
  totalLearningPaths: number;
  averageProgress: number;
  recentActivity: number;
  pendingTasks: number;
}

export default function TeacherSummaryWidget() {
  const [stats, setStats] = useState<SummaryStats>({
    totalStudents: 0,
    totalClasses: 0,
    totalQuizzes: 0,
    totalContents: 0,
    totalLearningPaths: 0,
    averageProgress: 0,
    recentActivity: 0,
    pendingTasks: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchSummaryStats = async () => {
      try {
        setLoading(true);
        setError(null);

        const token = localStorage.getItem('najah_token');
        if (!token) {
          setError("Token d'authentification manquant");
          setLoading(false);
          return;
        }

        const headers = {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        };

        // Récupérer les données du dashboard
        const response = await fetch(`${API_BASE_URL}/api/v1/dashboard/dashboard-data`, {
          headers
        });

        if (!response.ok) {
          throw new Error(`Erreur HTTP: ${response.status}`);
        }

        const data = await response.json();
        
        // Transformer les données
        const summaryStats: SummaryStats = {
          totalStudents: data.overview?.students || 0,
          totalClasses: data.overview?.classes || 0,
          totalQuizzes: data.overview?.quizzes || 0,
          totalContents: data.overview?.contents || 0,
          totalLearningPaths: data.overview?.learning_paths || 0,
          averageProgress: data.overview?.average_progression || 0,
          recentActivity: data.overview?.recent_activity?.quiz_results_week || 0,
          pendingTasks: data.pendingTasks?.length || 0
        };

        setStats(summaryStats);
        setLoading(false);

      } catch (err) {
        console.error("Erreur lors du chargement des statistiques:", err);
        setError("Erreur lors du chargement des statistiques");
        setLoading(false);
      }
    };

    fetchSummaryStats();
  }, []);

  const getTrendIcon = (value: number) => {
    if (value > 0) {
      return <TrendingUp className="w-4 h-4 text-green-500" />;
    } else if (value < 0) {
      return <TrendingDown className="w-4 h-4 text-red-500" />;
    }
    return <Activity className="w-4 h-4 text-gray-500" />;
  };

  const getStatColor = (type: string) => {
    switch (type) {
      case 'students': return 'bg-blue-500';
      case 'classes': return 'bg-green-500';
      case 'quizzes': return 'bg-purple-500';
      case 'contents': return 'bg-orange-500';
      case 'learning_paths': return 'bg-indigo-500';
      case 'progress': return 'bg-teal-500';
      case 'activity': return 'bg-pink-500';
      case 'tasks': return 'bg-yellow-500';
      default: return 'bg-gray-500';
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-6">
        <div className="flex items-center justify-center h-32">
          <div className="text-blue-600 animate-pulse">Chargement des statistiques...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-6">
        <div className="text-red-600 text-center">{error}</div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-gray-700">Résumé Général</h2>
        <div className="flex items-center space-x-2">
          <Activity className="w-5 h-5 text-blue-600" />
          <span className="text-sm text-gray-500">Vue d'ensemble</span>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {/* Nombre d'élèves */}
        <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-4 border border-blue-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-blue-600">Élèves</p>
              <p className="text-2xl font-bold text-blue-800">{stats.totalStudents}</p>
            </div>
            <div className={`p-2 rounded-full ${getStatColor('students')}`}>
              <Users className="w-6 h-6 text-white" />
            </div>
          </div>
        </div>

        {/* Nombre de classes */}
        <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-lg p-4 border border-green-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-green-600">Classes</p>
              <p className="text-2xl font-bold text-green-800">{stats.totalClasses}</p>
            </div>
            <div className={`p-2 rounded-full ${getStatColor('classes')}`}>
              <BookOpen className="w-6 h-6 text-white" />
            </div>
          </div>
        </div>

        {/* Nombre de quiz */}
        <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg p-4 border border-purple-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-purple-600">Quiz</p>
              <p className="text-2xl font-bold text-purple-800">{stats.totalQuizzes}</p>
            </div>
            <div className={`p-2 rounded-full ${getStatColor('quizzes')}`}>
              <Award className="w-6 h-6 text-white" />
            </div>
          </div>
        </div>

        {/* Contenus */}
        <div className="bg-gradient-to-br from-orange-50 to-orange-100 rounded-lg p-4 border border-orange-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-orange-600">Contenus</p>
              <p className="text-2xl font-bold text-orange-800">{stats.totalContents}</p>
            </div>
            <div className={`p-2 rounded-full ${getStatColor('contents')}`}>
              <FileText className="w-6 h-6 text-white" />
            </div>
          </div>
        </div>

        {/* Parcours d'apprentissage */}
        <div className="bg-gradient-to-br from-indigo-50 to-indigo-100 rounded-lg p-4 border border-indigo-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-indigo-600">Parcours</p>
              <p className="text-2xl font-bold text-indigo-800">{stats.totalLearningPaths}</p>
            </div>
            <div className={`p-2 rounded-full ${getStatColor('learning_paths')}`}>
              <Target className="w-6 h-6 text-white" />
            </div>
          </div>
        </div>

        {/* Progression moyenne */}
        <div className="bg-gradient-to-br from-teal-50 to-teal-100 rounded-lg p-4 border border-teal-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-teal-600">Progression</p>
              <p className="text-2xl font-bold text-teal-800">{stats.averageProgress}%</p>
            </div>
            <div className={`p-2 rounded-full ${getStatColor('progress')}`}>
              <TrendingUp className="w-6 h-6 text-white" />
            </div>
          </div>
        </div>

        {/* Activité récente */}
        <div className="bg-gradient-to-br from-pink-50 to-pink-100 rounded-lg p-4 border border-pink-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-pink-600">Activité</p>
              <p className="text-2xl font-bold text-pink-800">{stats.recentActivity}</p>
            </div>
            <div className={`p-2 rounded-full ${getStatColor('activity')}`}>
              <Activity className="w-6 h-6 text-white" />
            </div>
          </div>
        </div>

        {/* Tâches en attente */}
        <div className="bg-gradient-to-br from-yellow-50 to-yellow-100 rounded-lg p-4 border border-yellow-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-yellow-600">Tâches</p>
              <p className="text-2xl font-bold text-yellow-800">{stats.pendingTasks}</p>
            </div>
            <div className={`p-2 rounded-full ${getStatColor('tasks')}`}>
              <Calendar className="w-6 h-6 text-white" />
            </div>
          </div>
        </div>
      </div>

      {/* Résumé textuel */}
      <div className="mt-6 p-4 bg-gray-50 rounded-lg">
        <div className="flex items-center space-x-2 mb-2">
          <MessageSquare className="w-5 h-5 text-blue-600" />
          <h3 className="font-semibold text-gray-700">Résumé de la semaine</h3>
        </div>
        <p className="text-sm text-gray-600">
          Vous gérez actuellement <strong>{stats.totalClasses}</strong> classes avec <strong>{stats.totalStudents}</strong> élèves. 
          Vous avez créé <strong>{stats.totalQuizzes}</strong> quiz et <strong>{stats.totalContents}</strong> contenus pédagogiques. 
          La progression moyenne de vos élèves est de <strong>{stats.averageProgress}%</strong>.
        </p>
      </div>
    </div>
  );
} 