'use client';

import React from 'react';

interface DifficultyData {
  difficulty: string;
  count: number;
  averageScore: number;
  color: string;
}

interface DifficultyPerformanceChartProps {
  data: DifficultyData[];
  title?: string;
}

export default function DifficultyPerformanceChart({ data, title = "Performance par Difficulté" }: DifficultyPerformanceChartProps) {
  console.log('📊 DifficultyPerformanceChart - Données reçues:', data);
  
  if (!data || data.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <div className="w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
          <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        </div>
        <p className="text-lg font-medium">Aucune donnée disponible</p>
        <p className="text-sm">Les données de performance par difficulté apparaîtront ici</p>
      </div>
    );
  }

  const chartData = data.map((item, index) => ({
    name: item.difficulty,
    count: item.count,
    score: item.averageScore,
    color: item.color,
    index
  }));

  console.log('📊 DifficultyPerformanceChart - chartData:', chartData);

  return (
    <div className="w-full h-72">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        <div className="text-sm text-gray-500">
          {chartData.reduce((sum, item) => sum + item.count, 0)} tests au total
        </div>
      </div>
      
      <div className="grid grid-cols-3 gap-6 mb-6">
        {chartData.map((item, index) => (
          <div key={index} className="text-center p-4 border border-gray-200 rounded-lg bg-white">
            <div className="text-3xl font-bold text-gray-900 mb-1">
              {item.count}
            </div>
            <div className="text-sm text-gray-600 mb-2">Tests</div>
            <div className="text-2xl font-semibold text-gray-800">
              {item.averageScore}%
            </div>
            <div className="text-xs text-gray-500 uppercase tracking-wide">
              {item.difficulty}
            </div>
          </div>
        ))}
      </div>

      <div className="h-48 flex items-end justify-center space-x-12 px-4">
        {chartData.map((item, index) => (
          <div key={index} className="flex flex-col items-center min-w-0">
            <div 
              className="w-20 rounded-t-lg transition-all duration-300 hover:opacity-80 shadow-sm"
              style={{ 
                height: `${Math.max(30, (item.score / 100) * 100)}px`,
                backgroundColor: item.color 
              }}
            ></div>
            <div className="mt-3 text-sm font-semibold text-gray-700">{item.name}</div>
            <div className="text-sm font-bold text-gray-900">{item.score}%</div>
            <div className="text-xs text-gray-500 mt-1">{item.count} tests</div>
          </div>
        ))}
      </div>
    </div>
  );
}
