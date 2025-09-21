'use client';

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { TrendingUp, TrendingDown, Minus, Target, Clock, BookOpen } from 'lucide-react';

interface QuickStatsCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  trend?: 'up' | 'down' | 'stable';
  trendValue?: string;
  progress?: number;
  icon?: React.ReactNode;
  variant?: 'default' | 'success' | 'warning' | 'danger';
}

export const QuickStatsCard: React.FC<QuickStatsCardProps> = ({
  title,
  value,
  subtitle,
  trend,
  trendValue,
  progress,
  icon,
  variant = 'default'
}) => {
  const getTrendIcon = () => {
    switch (trend) {
      case 'up':
        return <TrendingUp className="w-4 h-4 text-green-500" />;
      case 'down':
        return <TrendingDown className="w-4 h-4 text-red-500" />;
      case 'stable':
        return <Minus className="w-4 h-4 text-gray-500" />;
      default:
        return null;
    }
  };

  const getTrendColor = () => {
    switch (trend) {
      case 'up':
        return 'text-green-600';
      case 'down':
        return 'text-red-600';
      case 'stable':
        return 'text-gray-600';
      default:
        return 'text-gray-600';
    }
  };

  const getVariantStyles = () => {
    switch (variant) {
      case 'success':
        return 'border-green-200 bg-green-50';
      case 'warning':
        return 'border-yellow-200 bg-yellow-50';
      case 'danger':
        return 'border-red-200 bg-red-50';
      default:
        return 'border-gray-200 bg-white';
    }
  };

  return (
    <Card className={`${getVariantStyles()} transition-all duration-200 hover:shadow-md`}>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium text-gray-700">{title}</CardTitle>
        {icon && <div className="text-gray-400">{icon}</div>}
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold text-gray-900">{value}</div>
        
        {subtitle && (
          <p className="text-xs text-gray-500 mt-1">{subtitle}</p>
        )}
        
        {trend && trendValue && (
          <div className="flex items-center space-x-2 mt-2">
            {getTrendIcon()}
            <span className={`text-xs font-medium ${getTrendColor()}`}>
              {trendValue}
            </span>
          </div>
        )}
        
        {progress !== undefined && (
          <div className="mt-3">
            <Progress value={progress} className="h-2" />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>0%</span>
              <span>{progress}%</span>
              <span>100%</span>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

// Composants spécialisés
export const ScoreCard: React.FC<{
  score: number;
  maxScore: number;
  title?: string;
  trend?: 'up' | 'down' | 'stable';
}> = ({ score, maxScore, title = 'Score', trend }) => {
  const percentage = Math.round((score / maxScore) * 100);
  const trendValue = trend === 'up' ? 'En amélioration' : trend === 'down' ? 'En baisse' : 'Stable';
  
  return (
    <QuickStatsCard
      title={title}
      value={`${score}/${maxScore}`}
      subtitle={`${percentage}% de réussite`}
      trend={trend}
      trendValue={trendValue}
      progress={percentage}
      icon={<Target className="w-4 h-4" />}
      variant={percentage >= 80 ? 'success' : percentage >= 60 ? 'warning' : 'danger'}
    />
  );
};

export const TimeCard: React.FC<{
  minutes: number;
  title?: string;
}> = ({ minutes, title = 'Temps d\'étude' }) => {
  const hours = Math.floor(minutes / 60);
  const remainingMinutes = minutes % 60;
  const displayValue = hours > 0 ? `${hours}h ${remainingMinutes}m` : `${minutes}m`;
  
  return (
    <QuickStatsCard
      title={title}
      value={displayValue}
      subtitle="Cette semaine"
      icon={<Clock className="w-4 h-4" />}
    />
  );
};

export const QuizCard: React.FC<{
  completed: number;
  total: number;
  title?: string;
}> = ({ completed, total, title = 'Quiz complétés' }) => {
  const percentage = Math.round((completed / total) * 100);
  
  return (
    <QuickStatsCard
      title={title}
      value={`${completed}/${total}`}
      subtitle={`${percentage}% terminés`}
      progress={percentage}
      icon={<BookOpen className="w-4 h-4" />}
      variant={percentage >= 80 ? 'success' : percentage >= 50 ? 'warning' : 'danger'}
    />
  );
};











