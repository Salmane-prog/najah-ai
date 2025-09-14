"use client";

import React, { useState, useEffect } from 'react';
import { BarChart3, TrendingUp, BookOpen, Calendar, Award } from 'lucide-react';
import { useAuth  } from '../../hooks/useAuth';

interface AnalyticsData {
  quizPerformance: {
    labels: string[];
    datasets: {
      label: string;
      data: number[];
      backgroundColor: string[];
      borderColor: string[];
    }[];
  };
  subjectProgress: {
    subject: string;
    progress: number;
    quizzes: number;
    averageScore: number;
  }[];
  weeklyActivity: {
    date: string;
    quizzes: number;
    timeSpent: number;
    points: number;
  }[];
  learningStreak: {
    current: number;
    best: number;
    history: number[];
  };
}

export default function InteractiveAnalytics() {
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState('performance');
  const { token } = useAuth();

  useEffect(() => {
    const fetchAnalyticsData = async () => {
      if (!token) return;
      
      try {
        setLoading(true);
        setError(null);

        // Récupérer les données analytics depuis l'API
        const [performanceRes, subjectsRes, activityRes, streakRes] = await Promise.all([
          fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/analytics/quiz-performance`, {
            headers: { 'Authorization': `Bearer ${token}` }
          }).catch(() => ({ ok: false, json: () => ({ labels: [], datasets: [] }) })),
          
          fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/analytics/subject-progress`, {
            headers: { 'Authorization': `Bearer ${token}` }
          }).catch(() => ({ ok: false, json: () => [] })),
          
          fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/analytics/weekly-activity`, {
            headers: { 'Authorization': `Bearer ${token}` }
          }).catch(() => ({ ok: false, json: () => [] })),
          
          fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/gamification/learning-streak`, {
            headers: { 'Authorization': `Bearer ${token}` }
          }).catch(() => ({ ok: false, json: () => ({ current: 0, best: 0, history: [] }) }))
        ]);

        const performance = await performanceRes.json();
        const subjects = await subjectsRes.json();
        const activity = await activityRes.json();
        const streak = await streakRes.json();

        setData({
          quizPerformance: performance,
          subjectProgress: subjects,
          weeklyActivity: activity,
          learningStreak: streak
        });
      } catch (err: any) {
        setError(err.message || 'Erreur lors du chargement des analytics');
      } finally {
        setLoading(false);
      }
    };

    fetchAnalyticsData();
  }, [token]);

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-sm p-6">
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 rounded w-1/3 mb-4"></div>
          <div className="space-y-3">
            <div className="h-4 bg-gray-200 rounded"></div>
            <div className="h-4 bg-gray-200 rounded w-5/6"></div>
            <div className="h-4 bg-gray-200 rounded w-4/6"></div>
          </div>
        </div>
      </div>
    );
  }

  if (!data) return null;

  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      {/* Header avec onglets */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-gray-800 flex items-center">
          <BarChart3 className="w-5 h-5 mr-2 text-blue-600" />
          Analytics Interactives
        </h2>
        
        <div className="flex space-x-1 bg-gray-100 rounded-lg p-1">
          {[
            { id: 'performance', label: 'Performance', icon: TrendingUp },
            { id: 'subjects', label: 'Matières', icon: BookOpen },
            { id: 'activity', label: 'Activité', icon: Calendar },
            { id: 'streak', label: 'Série', icon: Award }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center px-3 py-1 rounded-md text-sm font-medium transition-colors ${
                activeTab === tab.id
                  ? 'bg-white text-blue-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              <tab.icon className="w-4 h-4 mr-1" />
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Contenu des onglets */}
      <div className="space-y-6">
        {activeTab === 'performance' && (
          <div className="space-y-4">
            <h3 className="text-lg font-medium text-gray-800">Performance Hebdomadaire</h3>
            <div className="h-64 bg-gray-50 rounded-lg p-4">
              <div className="flex items-end justify-between h-full space-x-2">
                {data.quizPerformance.datasets[0].data.map((value, index) => (
                  <div key={index} className="flex flex-col items-center">
                    <div className="text-xs text-gray-500 mb-1">
                      {data.quizPerformance.labels[index]}
                    </div>
                    <div 
                      className="w-8 bg-blue-500 rounded-t transition-all duration-300 hover:bg-blue-600"
                      style={{ height: `${(value / 100) * 200}px` }}
                    ></div>
                    <div className="text-xs text-gray-600 mt-1">{value}%</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'subjects' && (
          <div className="space-y-4">
            <h3 className="text-lg font-medium text-gray-800">Progression par Matière</h3>
            <div className="space-y-3">
              {data.subjectProgress.map((subject, index) => (
                <div key={subject.subject} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                      <BookOpen className="w-5 h-5 text-blue-600" />
                    </div>
                    <div>
                      <h4 className="font-medium text-gray-800">{subject.subject}</h4>
                      <p className="text-sm text-gray-500">{subject.quizzes} quiz complétés</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-lg font-semibold text-gray-800">{subject.averageScore}%</div>
                    <div className="text-sm text-gray-500">Score moyen</div>
                  </div>
                  <div className="w-24">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs text-gray-500">Progression</span>
                      <span className="text-xs font-medium text-gray-700">{subject.progress}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-blue-500 h-2 rounded-full transition-all duration-500"
                        style={{ width: `${subject.progress}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'activity' && (
          <div className="space-y-4">
            <h3 className="text-lg font-medium text-gray-800">Activité Hebdomadaire</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-blue-50 rounded-lg p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-blue-600">Quiz Complétés</p>
                    <p className="text-2xl font-bold text-blue-800">
                      {data.weeklyActivity.reduce((sum, day) => sum + day.quizzes, 0)}
                    </p>
                  </div>
                  <Award className="w-8 h-8 text-blue-600" />
                </div>
              </div>
              
              <div className="bg-green-50 rounded-lg p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-green-600">Temps Total</p>
                    <p className="text-2xl font-bold text-green-800">
                      {data.weeklyActivity.reduce((sum, day) => sum + day.timeSpent, 0)} min
                    </p>
                  </div>
                  <Calendar className="w-8 h-8 text-green-600" />
                </div>
              </div>
              
              <div className="bg-purple-50 rounded-lg p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-purple-600">Points Gagnés</p>
                    <p className="text-2xl font-bold text-purple-800">
                      {data.weeklyActivity.reduce((sum, day) => sum + day.points, 0)}
                    </p>
                  </div>
                  <Award className="w-8 h-8 text-purple-600" />
                </div>
              </div>
            </div>
            
            <div className="bg-gray-50 rounded-lg p-4">
              <h4 className="font-medium text-gray-800 mb-3">Activité Quotidienne</h4>
              <div className="flex items-end justify-between space-x-2">
                {data.weeklyActivity.map((day, index) => (
                  <div key={index} className="flex flex-col items-center">
                    <div className="text-xs text-gray-500 mb-1">{day.date}</div>
                    <div className="w-6 bg-blue-500 rounded-t transition-all duration-300 hover:bg-blue-600"
                         style={{ height: `${Math.max(day.quizzes * 20, 4)}px` }}></div>
                    <div className="text-xs text-gray-600 mt-1">{day.quizzes}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'streak' && (
          <div className="space-y-4">
            <h3 className="text-lg font-medium text-gray-800">Série d'Apprentissage</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg p-6 text-white">
                <div className="text-center">
                  <div className="text-4xl font-bold mb-2">{data.learningStreak.current}</div>
                  <div className="text-sm opacity-90">Jours consécutifs actuels</div>
                </div>
              </div>
              
              <div className="bg-gray-50 rounded-lg p-6">
                <div className="text-center">
                  <div className="text-4xl font-bold text-gray-800 mb-2">{data.learningStreak.best}</div>
                  <div className="text-sm text-gray-600">Meilleure série</div>
                </div>
              </div>
            </div>
            
            <div className="bg-gray-50 rounded-lg p-4">
              <h4 className="font-medium text-gray-800 mb-3">Historique des 14 derniers jours</h4>
              <div className="flex space-x-1">
                {data.learningStreak.history.map((day, index) => (
                  <div
                    key={index}
                    className={`w-6 h-6 rounded-sm ${
                      day === 1 ? 'bg-green-500' : 'bg-gray-300'
                    }`}
                    title={`Jour ${index + 1}: ${day === 1 ? 'Activité' : 'Aucune activité'}`}
                  ></div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
} 