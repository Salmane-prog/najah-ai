'use client';

import React from 'react';

interface LearningTrendData {
  week: string;
  performance: number;
  engagement: number;
  completion: number;
  difficulty: number;
}

interface LearningTrendsChartProps {
  data: LearningTrendData[];
  title?: string;
}

export default function LearningTrendsChart({ data, title = "Tendances d'Apprentissage" }: LearningTrendsChartProps) {
  console.log('📈 LearningTrendsChart - Données reçues:', data);
  
  if (!data || data.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <div className="w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
          <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        </div>
        <p className="text-lg font-medium">Aucune donnée disponible</p>
        <p className="text-sm">Les tendances d'apprentissage apparaîtront ici</p>
      </div>
    );
  }

  const chartData = data.map((item, index) => ({
    name: item.week,
    performance: item.performance,
    engagement: item.engagement,
    completion: item.completion,
    difficulty: item.difficulty,
    index
  }));

  return (
    <div className="w-full h-64">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">{title}</h3>
      
      {/* Légende */}
      <div className="flex justify-center space-x-6 mb-4">
        <div className="flex items-center">
          <div className="w-3 h-3 rounded-full bg-blue-500 mr-2"></div>
          <span className="text-xs text-gray-600">Performance</span>
        </div>
        <div className="flex items-center">
          <div className="w-3 h-3 rounded-full bg-purple-500 mr-2"></div>
          <span className="text-xs text-gray-600">Engagement</span>
        </div>
        <div className="flex items-center">
          <div className="w-3 h-3 rounded-full bg-green-500 mr-2"></div>
          <span className="text-xs text-gray-600">Complétion</span>
        </div>
      </div>
      
      {/* Graphique en barres CSS */}
      <div className="h-40 relative">
        {/* Grille de fond */}
        <div className="absolute inset-0 flex flex-col justify-between">
          {[0, 25, 50, 75, 100].map((value) => (
            <div key={value} className="border-t border-gray-200 flex justify-between">
              <span className="text-xs text-gray-400 -mt-2 font-medium">{value}%</span>
            </div>
          ))}
        </div>
        
        {/* Barres empilées par semaine */}
        <div className="absolute inset-0 flex items-end justify-center space-x-4 px-4 pb-8">
          {chartData.map((item, index) => (
            <div key={index} className="flex flex-col items-center min-w-0">
              <div className="flex flex-col items-center w-8 h-32 justify-end space-y-1">
                {/* Barre Performance */}
                <div 
                  className="w-full rounded-t-sm shadow-sm"
                  style={{ 
                    height: `${Math.max(4, (item.performance / 100) * 60)}px`,
                    backgroundColor: '#3b82f6'
                  }}
                ></div>
                {/* Barre Engagement */}
                <div 
                  className="w-full rounded-t-sm shadow-sm"
                  style={{ 
                    height: `${Math.max(4, (item.engagement / 100) * 60)}px`,
                    backgroundColor: '#8b5cf6'
                  }}
                ></div>
                {/* Barre Complétion */}
                <div 
                  className="w-full rounded-t-sm shadow-sm"
                  style={{ 
                    height: `${Math.max(4, (item.completion / 100) * 60)}px`,
                    backgroundColor: '#10b981'
                  }}
                ></div>
              </div>
              <div className="mt-3 text-xs font-semibold text-gray-700">{item.name}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
