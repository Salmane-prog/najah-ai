'use client';

import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

interface SubjectData {
  month: string;
  testsCreated: number;
  testsCompleted: number;
}

interface SubjectDistributionChartProps {
  data: SubjectData[];
}

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4'];

export default function SubjectDistributionChart({ data }: SubjectDistributionChartProps) {
  // Vérifier si data est valide et est un tableau
  if (!data || !Array.isArray(data) || data.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <div className="w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
          <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z" />
          </svg>
        </div>
        <p className="text-lg font-medium">Aucune donnée disponible</p>
        <p className="text-sm">Les statistiques par matière apparaîtront ici</p>
      </div>
    );
  }

  // Transformer les données pour le graphique circulaire
  const chartData = data.map((item, index) => ({
    name: item.month,
    value: item.testsCreated,
    completed: item.testsCompleted,
    color: COLORS[index % COLORS.length]
  }));

  const totalTests = chartData.reduce((sum, item) => sum + item.value, 0);

  return (
    <div className="w-full h-64">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip 
            contentStyle={{
              backgroundColor: 'white',
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
              boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
            }}
            formatter={(value: any, name: any, props: any) => [
              `${value} tests (${((value / totalTests) * 100).toFixed(1)}%)`,
              'Tests Créés'
            ]}
          />
          <Legend 
            verticalAlign="bottom" 
            height={36}
            formatter={(value, entry: any) => (
              <span style={{ color: entry.color }}>
                {value} - {entry.payload.value} tests
              </span>
            )}
          />
        </PieChart>
      </ResponsiveContainer>
      
      {/* Statistiques détaillées */}
      <div className="mt-4 grid grid-cols-2 gap-4 text-sm">
        <div className="text-center">
          <div className="text-lg font-bold text-blue-600">
            {totalTests}
          </div>
          <div className="text-gray-600">Total Tests Créés</div>
        </div>
        <div className="text-center">
          <div className="text-lg font-bold text-green-600">
            {chartData.reduce((sum, item) => sum + item.completed, 0)}
          </div>
          <div className="text-gray-600">Total Tests Complétés</div>
        </div>
      </div>
    </div>
  );
}









