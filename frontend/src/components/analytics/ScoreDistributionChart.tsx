'use client';

import React from 'react';

interface ScoreDistributionData {
  range: string;
  count: number;
  percentage: number;
  color: string;
}

interface ScoreDistributionChartProps {
  data: ScoreDistributionData[];
  title?: string;
}

export default function ScoreDistributionChart({ data, title = "Distribution des Scores" }: ScoreDistributionChartProps) {
  console.log('📊 ScoreDistributionChart - Données reçues:', data);
  
  if (!data || data.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <div className="w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
          <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        </div>
        <p className="text-lg font-medium">Aucune donnée disponible</p>
        <p className="text-sm">Les données de distribution des scores apparaîtront ici</p>
      </div>
    );
  }

  const chartData = data.map((item, index) => ({
    name: item.range,
    count: item.count,
    percentage: item.percentage,
    color: item.color,
    index
  }));

  return (
    <div className="w-full h-64">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">{title}</h3>
      
      {/* Graphique en barres CSS */}
      <div className="h-48 flex items-end justify-center space-x-8 px-4">
        {chartData.map((item, index) => (
          <div key={index} className="flex flex-col items-center min-w-0">
            <div 
              className="w-16 rounded-t-lg transition-all duration-300 hover:opacity-80 shadow-sm"
              style={{ 
                height: `${Math.max(20, (item.count / Math.max(...chartData.map(d => d.count))) * 120)}px`,
                backgroundColor: item.color 
              }}
            ></div>
            <div className="mt-3 text-sm font-semibold text-gray-700">{item.range}</div>
            <div className="text-sm font-bold text-gray-900">{item.count}</div>
            <div className="text-xs text-gray-500 mt-1">{item.percentage}%</div>
          </div>
        ))}
      </div>
    </div>
  );
}
