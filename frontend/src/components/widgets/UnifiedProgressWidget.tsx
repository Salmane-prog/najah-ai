"use client";

import React from 'react';
import { Trophy, Star, Target, TrendingUp, Award, Zap, CheckCircle } from 'lucide-react';
import { useStudentDashboard } from '../../hooks/useStudentDashboard';

export const UnifiedProgressWidget: React.FC<{ className?: string }> = ({ className = '' }) => {
  const { stats, gamification, loading } = useStudentDashboard();

  if (loading) {
    return (
      <div className={`bg-white rounded-lg shadow-sm p-6 ${className}`}>
        <div className="animate-pulse space-y-4">
          <div className="h-6 bg-gray-200 rounded w-1/3"></div>
          <div className="grid grid-cols-2 gap-4">
            <div className="h-20 bg-gray-200 rounded"></div>
            <div className="h-20 bg-gray-200 rounded"></div>
          </div>
          <div className="h-4 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  if (!stats || !gamification) {
    return (
      <div className={`bg-white rounded-lg shadow-sm p-6 ${className}`}>
        <p className="text-gray-500 text-center">Données non disponibles</p>
      </div>
    );
  }

  const { level, currentXp, xpToNextLevel, rank } = stats;
  const { points, achievements, challenges } = gamification;
  
  // Calcul du pourcentage de progression
  const progressPercentage = Math.min(100, (currentXp / xpToNextLevel) * 100);

  return (
    <div className={`space-y-6 ${className}`}>
      {/* En-tête avec titre et niveau */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Trophy className="text-yellow-500" size={24} />
          <h3 className="text-xl font-bold text-gray-800">Progression Unifiée</h3>
        </div>
        <div className="text-right">
          <p className="text-sm text-gray-600">Niveau {level}</p>
          <p className="text-lg font-bold text-blue-600">{rank}</p>
        </div>
      </div>

      {/* Cartes principales - Points et Niveau */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Carte Points Totaux */}
        <div className="bg-gradient-to-br from-yellow-400 to-orange-500 rounded-lg p-4 text-white">
          <div className="flex items-center gap-2 mb-2">
            <Star className="text-white" size={20} />
            <span className="font-bold">Points Totaux</span>
          </div>
          <div className="text-3xl font-bold">{points?.total_points || 0}</div>
          <div className="text-sm opacity-90">
            +{points?.achievements_points || 0} achievements
            <br />
            +{points?.challenges_points || 0} challenges
          </div>
        </div>

        {/* Carte Niveau */}
        <div className="bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg p-4 text-white">
          <div className="flex items-center gap-2 mb-2">
            <Target className="text-white" size={20} />
            <span className="font-bold">Niveau {level}</span>
          </div>
          <div className="text-3xl font-bold">{currentXp} XP</div>
          <div className="text-sm opacity-90">
            {xpToNextLevel} XP pour le niveau suivant
          </div>
        </div>
      </div>

      {/* Barre de progression XP unifiée */}
      <div className="bg-gray-100 rounded-lg p-4">
        <div className="flex justify-between text-sm mb-2">
          <span className="font-medium text-gray-700">
            Progression vers le niveau {level + 1}
          </span>
          <span className="text-gray-500">
            {currentXp} / {xpToNextLevel} XP
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
          <div 
            className="bg-gradient-to-r from-blue-500 to-purple-600 h-3 rounded-full transition-all duration-1000 ease-out"
            style={{ width: `${progressPercentage}%` }}
          ></div>
        </div>
        <div className="text-xs text-gray-500 mt-1 text-center">
          {progressPercentage.toFixed(1)}% complété
        </div>
      </div>

      {/* Statistiques détaillées */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white border border-gray-200 rounded-lg p-4 text-center">
          <div className="flex items-center justify-center mb-2">
            <CheckCircle className="text-green-500" size={20} />
          </div>
          <div className="text-2xl font-bold text-green-600">
            {stats.completedQuizzes}
          </div>
          <div className="text-sm text-gray-600">Quiz Complétés</div>
        </div>

        <div className="bg-white border border-gray-200 rounded-lg p-4 text-center">
          <div className="flex items-center justify-center mb-2">
            <TrendingUp className="text-blue-500" size={20} />
          </div>
          <div className="text-2xl font-bold text-blue-600">
            {stats.averageScore.toFixed(1)}%
          </div>
          <div className="text-sm text-gray-600">Score Moyen</div>
        </div>

        <div className="bg-white border border-gray-200 rounded-lg p-4 text-center">
          <div className="flex items-center justify-center mb-2">
            <Award className="text-purple-500" size={20} />
          </div>
          <div className="text-2xl font-bold text-purple-600">
            {achievements?.unlocked_count || 0}
          </div>
          <div className="text-sm text-gray-600">Badges Obtenus</div>
        </div>
      </div>

      {/* Achievements et Challenges */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Achievements */}
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-3">
            <Award className="text-green-500" size={20} />
            <span className="font-semibold">Achievements</span>
          </div>
          <div className="text-2xl font-bold text-green-600">
            {achievements?.unlocked_count || 0} / {achievements?.total_achievements || 0}
          </div>
          <div className="text-sm text-gray-600 mt-2">
            {achievements?.achievements?.slice(0, 3).map((achievement: any) => (
              <div key={achievement.id} className="flex items-center gap-2 mt-1">
                <div className={`w-2 h-2 rounded-full ${achievement.unlocked ? 'bg-green-500' : 'bg-gray-300'}`}></div>
                <span className={`text-xs ${achievement.unlocked ? 'text-green-600' : 'text-gray-500'}`}>
                  {achievement.name}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Challenges */}
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-3">
            <Zap className="text-orange-500" size={20} />
            <span className="font-semibold">Challenges</span>
          </div>
          <div className="text-2xl font-bold text-orange-600">
            {challenges?.completed_count || 0} / {challenges?.total_challenges || 0}
          </div>
          <div className="text-sm text-gray-600 mt-2">
            {challenges?.challenges?.slice(0, 3).map((challenge: any) => (
              <div key={challenge.id} className="flex items-center gap-2 mt-1">
                <div className={`w-2 h-2 rounded-full ${challenge.completed ? 'bg-orange-500' : 'bg-gray-300'}`}></div>
                <span className={`text-xs ${challenge.completed ? 'text-orange-600' : 'text-gray-500'}`}>
                  {challenge.name}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Indicateur de synchronisation */}
      <div className="bg-green-50 border border-green-200 rounded-lg p-3">
        <div className="flex items-center gap-2 text-green-700">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-sm font-medium">Données synchronisées en temps réel</span>
        </div>
      </div>
    </div>
  );
};


