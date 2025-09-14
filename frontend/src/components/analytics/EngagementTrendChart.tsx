'use client';

import React from 'react';

interface EngagementData {
  day: string;
  engagement: number;
  studyTime: number;
  activities: number;
}

interface EngagementTrendChartProps {
  data: EngagementData[];
  title?: string;
}

export default function EngagementTrendChart({ data, title = "Tendance d'Engagement" }: EngagementTrendChartProps) {
  console.log('📈 EngagementTrendChart - Données reçues:', data);
  
  if (!data || data.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <div className="w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
          <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
          </svg>
        </div>
        <p className="text-lg font-medium">Aucune donnée disponible</p>
        <p className="text-sm">Les données d'engagement apparaîtront ici</p>
      </div>
    );
  }

  const chartData = data.map((item, index) => ({
    name: item.day,
    engagement: item.engagement,
    studyTime: item.studyTime,
    activities: item.activities,
    index
  }));

  console.log('📈 EngagementTrendChart - chartData:', chartData);

  return (
    <div className="w-full h-72">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        <div className="flex items-center space-x-4 text-xs text-gray-500">
          <div className="flex items-center">
            <div className="w-2 h-2 bg-blue-600 rounded-full mr-2"></div>
            <span>Engagement</span>
          </div>
          <div className="flex items-center">
            <div className="w-2 h-2 bg-gray-600 rounded-full mr-2"></div>
            <span>Temps d'Étude</span>
          </div>
        </div>
      </div>

      <div className="h-48 relative">
        {/* Grille de fond */}
        <div className="absolute inset-0 flex flex-col justify-between px-2">
          {[0, 25, 50, 75, 100].map((value) => (
            <div key={value} className="border-t border-gray-200 flex justify-between">
              <span className="text-xs text-gray-400 -mt-2 font-medium">{value}%</span>
            </div>
          ))}
        </div>
        
        {/* Graphique en barres empilées */}
        <div className="absolute inset-0 flex items-end justify-center space-x-6 px-6 pb-8">
          {chartData.map((item, index) => (
            <div key={index} className="flex flex-col items-center min-w-0">
              <div className="flex flex-col items-center w-12 h-32 justify-end space-y-1">
                {/* Barre d'engagement */}
                <div 
                  className="w-full rounded-t-md shadow-sm"
                  style={{ 
                    height: `${Math.max(8, (item.engagement / 100) * 80)}px`,
                    backgroundColor: '#2563eb'
                  }}
                ></div>
                {/* Barre de temps d'étude */}
                <div 
                  className="w-full rounded-t-md shadow-sm"
                  style={{ 
                    height: `${Math.max(8, (item.studyTime / 100) * 80)}px`,
                    backgroundColor: '#6b7280'
                  }}
                ></div>
              </div>
              <div className="mt-3 text-xs font-semibold text-gray-700">{item.name}</div>
              <div className="text-xs text-gray-500 mt-1">
                {item.engagement}% / {item.studyTime}%
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
