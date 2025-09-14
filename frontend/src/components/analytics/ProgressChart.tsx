'use client';

import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from 'recharts';

interface ProgressData {
  week: string;
  averageScore: number;
  testsCompleted: number;
}

interface ProgressChartProps {
  data: ProgressData[];
  title: string;
  type?: 'line' | 'area';
}

export default function ProgressChart({ data, title, type = 'line' }: ProgressChartProps) {
  console.log('📈 ProgressChart - Données reçues:', data);
  console.log('📈 ProgressChart - Titre:', title);
  console.log('📈 ProgressChart - Type:', type);
  
  if (!data || data.length === 0) {
    console.log('📈 ProgressChart - Aucune donnée, affichage du message de fallback');
    return (
      <div className="text-center py-8 text-gray-500">
        <div className="w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
          <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        </div>
        <p className="text-lg font-medium">Aucune donnée disponible</p>
        <p className="text-sm">Les données de progression apparaîtront ici</p>
      </div>
    );
  }

  console.log('📈 ProgressChart - Données valides, construction du graphique');
  const chartData = data.map((item, index) => ({
    name: item.week,
    score: item.averageScore,
    tests: item.testsCompleted,
    index
  }));

  return (
    <div className="w-full h-64">
      <ResponsiveContainer width="100%" height="100%">
        {type === 'area' ? (
          <AreaChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis 
              dataKey="name" 
              stroke="#666"
              fontSize={12}
              tickLine={false}
              axisLine={false}
            />
            <YAxis 
              stroke="#666"
              fontSize={12}
              tickLine={false}
              axisLine={false}
              domain={[0, 100]}
              tickFormatter={(value) => `${value}%`}
            />
            <Tooltip 
              contentStyle={{
                backgroundColor: 'white',
                border: '1px solid #e5e7eb',
                borderRadius: '8px',
                boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
              }}
              formatter={(value: any, name: any) => [
                `${value}%`, 
                name === 'score' ? 'Score Moyen' : 'Tests Complétés'
              ]}
              labelFormatter={(label) => `Semaine: ${label}`}
            />
            <Area
              type="monotone"
              dataKey="score"
              stroke="#3b82f6"
              strokeWidth={3}
              fill="#3b82f6"
              fillOpacity={0.1}
              name="Score Moyen"
            />
          </AreaChart>
        ) : (
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis 
              dataKey="name" 
              stroke="#666"
              fontSize={12}
              tickLine={false}
              axisLine={false}
            />
            <YAxis 
              stroke="#666"
              fontSize={12}
              tickLine={false}
              axisLine={false}
              domain={[0, 100]}
              tickFormatter={(value) => `${value}%`}
            />
            <Tooltip 
              contentStyle={{
                backgroundColor: 'white',
                border: '1px solid #e5e7eb',
                borderRadius: '8px',
                boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
              }}
              formatter={(value: any, name: any) => [
                `${value}%`, 
                name === 'score' ? 'Score Moyen' : 'Tests Complétés'
              ]}
              labelFormatter={(label) => `Semaine: ${label}`}
            />
            <Line
              type="monotone"
              dataKey="score"
              stroke="#3b82f6"
              strokeWidth={3}
              dot={{ fill: '#3b82f6', strokeWidth: 2, r: 4 }}
              activeDot={{ r: 6, stroke: '#3b82f6', strokeWidth: 2 }}
              name="Score Moyen"
            />
          </LineChart>
        )}
      </ResponsiveContainer>
    </div>
  );
}
