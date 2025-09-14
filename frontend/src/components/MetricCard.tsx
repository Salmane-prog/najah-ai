import React from 'react';
import { LucideIcon } from 'lucide-react';

interface MetricCardProps {
  title: string;
  value: string | number;
  change?: string;
  trend?: 'up' | 'down' | 'neutral';
  icon?: LucideIcon;
  priority?: 1 | 2 | 3 | 4;
  className?: string;
  onClick?: () => void;
  loading?: boolean;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  change,
  trend = 'neutral',
  icon: Icon,
  priority = 2,
  className = '',
  onClick,
  loading = false
}) => {
  const priorityClasses = {
    1: 'priority-1',
    2: 'priority-2', 
    3: 'priority-3',
    4: 'priority-4'
  };

  const trendColors = {
    up: 'text-green-600',
    down: 'text-red-600',
    neutral: 'text-gray-600'
  };

  const trendIcons = {
    up: '↗',
    down: '↘',
    neutral: '→'
  };

  if (loading) {
    return (
      <div className={`dashboard-card ${className} animate-pulse`}>
        <div className="flex items-center justify-between">
          <div className="h-4 bg-gray-200 rounded w-1/2"></div>
          <div className="h-4 bg-gray-200 rounded w-1/4"></div>
        </div>
        <div className="h-8 bg-gray-200 rounded mt-2"></div>
      </div>
    );
  }

  return (
    <div 
      className={`dashboard-card hover-lift smooth-transition ${className} ${onClick ? 'cursor-pointer' : ''}`}
      onClick={onClick}
      role={onClick ? 'button' : undefined}
      tabIndex={onClick ? 0 : undefined}
      onKeyDown={onClick ? (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          onClick();
        }
      } : undefined}
    >
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          {Icon && <Icon size={20} className="text-gray-500" />}
          <h3 className={`${priorityClasses[priority]} font-medium`}>
            {title}
          </h3>
        </div>
        {change && (
          <div className={`text-sm font-medium ${trendColors[trend]}`}>
            <span className="sr-only">
              {trend === 'up' ? 'Augmentation' : trend === 'down' ? 'Diminution' : 'Stable'}: 
            </span>
            {trendIcons[trend]} {change}
          </div>
        )}
      </div>
      
      <div className="metric-value">
        <span className="sr-only">Valeur: </span>
        {value}
      </div>
      
      {onClick && (
        <div className="mt-2 text-xs text-gray-500">
          Cliquez pour plus de détails
        </div>
      )}
    </div>
  );
};

export default MetricCard; 