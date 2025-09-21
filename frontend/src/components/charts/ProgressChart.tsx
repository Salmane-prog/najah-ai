'use client';

import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import { Line, Bar, Doughnut } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

interface ProgressChartProps {
  type: 'line' | 'bar' | 'doughnut';
  data: any;
  options?: any;
  title?: string;
  className?: string;
}

export const ProgressChart: React.FC<ProgressChartProps> = ({
  type,
  data,
  options,
  title,
  className = ''
}) => {
  const renderChart = () => {
    switch (type) {
      case 'line':
        return <Line data={data} options={options} />;
      case 'bar':
        return <Bar data={data} options={options} />;
      case 'doughnut':
        return <Doughnut data={data} options={options} />;
      default:
        return <Line data={data} options={options} />;
    }
  };

  return (
    <div className={`bg-white rounded-lg shadow-md p-6 ${className}`}>
      {title && (
        <h3 className="text-lg font-semibold text-gray-800 mb-4 text-center">
          {title}
        </h3>
      )}
      <div className="w-full h-64">
        {renderChart()}
      </div>
    </div>
  );
};

// Composants spécialisés pour différents types de graphiques
export const TrendChart: React.FC<{
  data: { labels: string[]; scores: number[]; dates: string[] };
  title?: string;
}> = ({ data, title }) => {
  const chartData = {
    labels: data.labels,
    datasets: [
      {
        label: 'Score Global',
        data: data.scores,
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.4,
        fill: true,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: false,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        ticks: {
          callback: function(value: any) {
            return value + '%';
          },
        },
      },
    },
  };

  return (
    <ProgressChart
      type="line"
      data={chartData}
      options={options}
      title={title || 'Évolution des Scores'}
      className="mb-6"
    />
  );
};

export const WeakAreasChart: React.FC<{
  weakAreas: Array<{ topic: string; success_rate: number }>;
  title?: string;
}> = ({ weakAreas, title }) => {
  const chartData = {
    labels: weakAreas.map(area => area.topic),
    datasets: [
      {
        label: 'Taux de Réussite',
        data: weakAreas.map(area => area.success_rate),
        backgroundColor: [
          'rgba(239, 68, 68, 0.8)',   // Rouge pour les scores très faibles
          'rgba(245, 158, 11, 0.8)',  // Orange pour les scores faibles
          'rgba(34, 197, 94, 0.8)',   // Vert pour les scores moyens
        ],
        borderColor: [
          'rgb(239, 68, 68)',
          'rgb(245, 158, 11)',
          'rgb(34, 197, 94)',
        ],
        borderWidth: 2,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      tooltip: {
        callbacks: {
          label: function(context: any) {
            return `${context.label}: ${context.parsed.y.toFixed(1)}%`;
          },
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        ticks: {
          callback: function(value: any) {
            return value + '%';
          },
        },
      },
    },
  };

  return (
    <ProgressChart
      type="bar"
      data={chartData}
      options={options}
      title={title || 'Analyse des Domaines Faibles'}
      className="mb-6"
    />
  );
};

export const CompetencyChart: React.FC<{
  competencies: Array<{ name: string; level: number; maxLevel: number }>;
  title?: string;
}> = ({ competencies, title }) => {
  const chartData = {
    labels: competencies.map(comp => comp.name),
    datasets: [
      {
        label: 'Niveau Actuel',
        data: competencies.map(comp => (comp.level / comp.maxLevel) * 100),
        backgroundColor: 'rgba(59, 130, 246, 0.8)',
        borderColor: 'rgb(59, 130, 246)',
        borderWidth: 2,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      tooltip: {
        callbacks: {
          label: function(context: any) {
            const comp = competencies[context.dataIndex];
            return `${comp.name}: Niveau ${comp.level}/${comp.maxLevel}`;
          },
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        ticks: {
          callback: function(value: any) {
            return value + '%';
          },
        },
      },
    },
  };

  return (
    <ProgressChart
      type="bar"
      data={chartData}
      options={options}
      title={title || 'Niveaux de Compétence'}
      className="mb-6"
    />
  );
};











