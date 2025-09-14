'use client';

import React from 'react';
import { Calendar, Clock, TrendingUp, Activity, Target, Award } from 'lucide-react';

export default function TemporalAnalyticsWidget() {
  // Données simulées pour les visualisations temporelles
  const hourlyData = Array.from({ length: 24 }, (_, i) => ({
    hour: i,
    activity: Math.floor(Math.random() * 50 + 20),
    performance: Math.floor(Math.random() * 30 + 70)
  }));

  const weeklyPattern = [
    { day: 'Lun', tests: 15, avgScore: 78, engagement: 85 },
    { day: 'Mar', tests: 22, avgScore: 82, engagement: 88 },
    { day: 'Mer', tests: 18, avgScore: 75, engagement: 82 },
    { day: 'Jeu', tests: 25, avgScore: 85, engagement: 90 },
    { day: 'Ven', tests: 20, avgScore: 80, engagement: 87 },
    { day: 'Sam', tests: 12, avgScore: 72, engagement: 75 },
    { day: 'Dim', tests: 8, avgScore: 68, engagement: 70 }
  ];

  const monthlyTrends = [
    { month: 'Jan', growth: 5, challenges: 45, achievements: 120 },
    { month: 'Fév', growth: 8, challenges: 52, achievements: 135 },
    { month: 'Mar', growth: 12, challenges: 58, achievements: 150 },
    { month: 'Avr', growth: 15, challenges: 65, achievements: 168 },
    { month: 'Mai', growth: 18, challenges: 72, achievements: 185 },
    { month: 'Juin', growth: 22, challenges: 80, achievements: 200 }
  ];

  return (
    <div className="space-y-4">
      {/* Titre de la section */}
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-bold text-gray-900">Analytics Temporels</h3>
        <div className="flex items-center space-x-2">
          <Clock className="w-4 h-4 text-blue-600" />
          <span className="text-xs text-blue-600 font-medium">Données temporelles</span>
        </div>
      </div>

      {/* Activité horaire */}
      <div className="bg-white rounded-lg p-4 border border-gray-200 shadow-sm">
        <h4 className="text-base font-semibold text-gray-900 mb-3 flex items-center">
          <Activity className="w-4 h-4 text-green-600 mr-2" />
          Activité Horaire (24h)
        </h4>
        <div className="grid grid-cols-12 gap-1 h-24">
          {hourlyData.map((data, index) => (
            <div key={index} className="flex flex-col items-center justify-end">
              <div 
                className="w-full bg-gradient-to-t from-blue-500 to-blue-600 rounded-t transition-all duration-300 hover:from-blue-600 hover:to-blue-700"
                style={{ height: `${(data.activity / 70) * 100}%` }}
                title={`${data.hour}h: ${data.activity} activités`}
              ></div>
              <span className="text-xs text-gray-500 mt-1">{data.hour}h</span>
            </div>
          ))}
        </div>
        <div className="mt-4 text-center">
          <p className="text-sm text-gray-600">Pic d'activité entre 14h et 16h</p>
        </div>
      </div>

      {/* Patterns hebdomadaires */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="bg-white rounded-lg p-4 border border-gray-200 shadow-sm">
          <h4 className="text-base font-semibold text-gray-900 mb-3 flex items-center">
            <Calendar className="w-4 h-4 text-purple-600 mr-2" />
            Performance Hebdomadaire
          </h4>
          <div className="space-y-3">
            {weeklyPattern.map((day, index) => (
              <div key={index} className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-700 w-12">{day.day}</span>
                <div className="flex-1 mx-4">
                  <div className="flex items-center space-x-2">
                    <div className="flex-1 bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-gradient-to-r from-purple-500 to-purple-600 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${day.engagement}%` }}
                      ></div>
                    </div>
                    <span className="text-xs text-gray-500 w-12">{day.engagement}%</span>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-sm font-semibold text-gray-900">{day.avgScore}%</div>
                  <div className="text-xs text-gray-500">{day.tests} tests</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <TrendingUp className="w-5 h-5 text-orange-600 mr-2" />
            Tendances Mensuelles
          </h3>
          <div className="space-y-4">
            {monthlyTrends.map((month, index) => (
              <div key={index} className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-700 w-12">{month.month}</span>
                <div className="flex-1 mx-4">
                  <div className="flex items-center space-x-4">
                    <div className="flex items-center space-x-2">
                      <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                      <span className="text-xs text-gray-500">+{month.growth}%</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                      <span className="text-xs text-gray-500">{month.challenges}</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="w-3 h-3 bg-purple-500 rounded-full"></div>
                      <span className="text-xs text-gray-500">{month.achievements}</span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Graphique de progression temporelle avancé */}
      <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <Target className="w-5 h-5 text-red-600 mr-2" />
          Progression Temporelle Détaillée
        </h3>
        <div className="grid grid-cols-7 gap-3">
          {Array.from({ length: 7 }, (_, i) => {
            const baseHeight = Math.random() * 40 + 30;
            const performance = Math.floor(Math.random() * 30 + 70);
            const engagement = Math.floor(Math.random() * 20 + 80);
            
            return (
              <div key={i} className="text-center">
                <div className="text-xs text-gray-500 mb-2">J{i + 1}</div>
                <div className="relative w-full bg-gray-200 rounded-t-lg" style={{ height: '80px' }}>
                  {/* Barre de performance */}
                  <div 
                    className="absolute bottom-0 w-full bg-gradient-to-t from-blue-500 to-blue-600 rounded-t transition-all duration-300"
                    style={{ 
                      height: `${baseHeight}%`,
                      opacity: 0.8
                    }}
                  ></div>
                  
                  {/* Barre d'engagement */}
                  <div 
                    className="absolute bottom-0 w-full bg-gradient-to-t from-green-500 to-green-600 rounded-t transition-all duration-300"
                    style={{ 
                      height: `${baseHeight * 0.7}%`,
                      opacity: 0.6
                    }}
                  ></div>
                </div>
                
                <div className="mt-2 space-y-1">
                  <div className="text-xs font-medium text-blue-600">{performance}%</div>
                  <div className="text-xs text-green-600">{engagement}%</div>
                </div>
              </div>
            );
          })}
        </div>
        <div className="mt-4 flex justify-center space-x-6">
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
            <span className="text-xs text-gray-600">Performance</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-green-500 rounded-full"></div>
            <span className="text-xs text-gray-600">Engagement</span>
          </div>
        </div>
      </div>

      {/* Résumé des insights temporels */}
      <div className="bg-gradient-to-r from-indigo-50 to-blue-50 rounded-xl p-6 border border-indigo-200">
        <h3 className="text-lg font-semibold text-indigo-900 mb-4 flex items-center">
          <Award className="w-5 h-5 text-indigo-600 mr-2" />
          Insights Temporels
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-indigo-600">14h-16h</div>
            <div className="text-sm text-indigo-700">Pic d'activité quotidien</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-indigo-600">Jeudi</div>
            <div className="text-sm text-indigo-700">Jour le plus productif</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-indigo-600">+22%</div>
            <div className="text-sm text-indigo-700">Croissance mensuelle</div>
          </div>
        </div>
      </div>
    </div>
  );
}
