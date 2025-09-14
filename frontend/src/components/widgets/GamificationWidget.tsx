"use client";

import React from 'react';
import { Trophy, Star, Target, Award, TrendingUp, Zap } from 'lucide-react';
import { useStudentDashboard } from '../../hooks/useStudentDashboard';

export const GamificationWidget: React.FC<{ className?: string }> = ({ 
  className = '' 
}) => {
  const { gamification, loading } = useStudentDashboard();

  if (loading) {
    return (
      <div className={`space-y-6 ${className}`}>
        <div className="animate-pulse space-y-4">
          <div className="h-6 bg-gray-200 rounded w-1/3"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="h-20 bg-gray-200 rounded"></div>
            <div className="h-20 bg-gray-200 rounded"></div>
          </div>
        </div>
      </div>
    );
  }

  if (!gamification) {
    return (
      <div className={`space-y-6 ${className}`}>
        <p className="text-gray-500 text-center">Données de gamification non disponibles</p>
      </div>
    );
  }

  const { points, achievements, challenges, leaderboard, level } = gamification;

  return (
    <div className={`space-y-6 ${className}`}>
      <div className="flex items-center gap-2 mb-4">
        <Trophy className="text-yellow-500" size={24} />
        <h3 className="text-xl font-bold text-gray-800">Gamification</h3>
      </div>

      {/* Points et Niveau - Maintenant synchronisés */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
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

        <div className="bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg p-4 text-white">
          <div className="flex items-center gap-2 mb-2">
            <Target className="text-white" size={20} />
            <span className="font-bold">Niveau {level?.level || 1}</span>
          </div>
          <div className="text-3xl font-bold">{level?.current_xp || 0} XP</div>
          <div className="text-sm opacity-90">
            {level?.xp_to_next_level || 0} XP pour le niveau suivant
          </div>
        </div>
      </div>

      {/* Barre de progression XP - Maintenant synchronisée */}
      {level && (
        <div className="bg-gray-100 rounded-lg p-4">
          <div className="flex justify-between text-sm mb-2">
            <span className="font-medium text-gray-700">
              Progression vers le niveau {level.level + 1}
            </span>
            <span className="text-gray-500">
              {level.current_xp} / {level.xp_to_next_level} XP
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
            <div 
              className="bg-gradient-to-r from-blue-500 to-purple-600 h-3 rounded-full transition-all duration-1000 ease-out"
              style={{ 
                width: `${level.progress_percentage || 0}%` 
              }}
            ></div>
          </div>
          <div className="text-xs text-gray-500 mt-1 text-center">
            {(level.progress_percentage || 0).toFixed(1)}% complété
          </div>
        </div>
      )}

      {/* Achievements et Challenges */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-3">
            <Award className="text-green-500" size={20} />
            <span className="font-semibold">Achievements</span>
          </div>
          <div className="text-2xl font-bold text-green-600">
            {achievements?.unlocked_count || 0} / {achievements?.total_achievements || 0}
          </div>
          <div className="text-sm text-gray-600">
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

        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-3">
            <Zap className="text-orange-500" size={20} />
            <span className="font-semibold">Challenges</span>
          </div>
          <div className="text-2xl font-bold text-orange-600">
            {challenges?.completed_count || 0} / {challenges?.total_challenges || 0}
          </div>
          <div className="text-sm text-gray-600">
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

      {/* Leaderboard */}
      {leaderboard && leaderboard.leaderboard && leaderboard.leaderboard.length > 0 && (
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-3">
            <TrendingUp className="text-blue-500" size={20} />
            <span className="font-semibold">Classement</span>
          </div>
          <div className="space-y-2 max-h-96 overflow-y-auto">
            {leaderboard.leaderboard.slice(0, 5).map((entry: any, index: number) => (
              <div key={entry.user_id} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                <div className="flex items-center gap-3">
                  <div className="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center text-xs font-bold">
                    {index + 1}
                  </div>
                  <span className="text-sm font-medium">{entry.username}</span>
                </div>
                <div className="text-sm text-gray-600">
                  {entry.total_points} pts
                </div>
              </div>
            ))}
            {leaderboard.user_rank && (
              <div className="mt-3 p-2 bg-blue-50 rounded border border-blue-200">
                <div className="text-sm text-blue-700">
                  Votre rang : #{leaderboard.user_rank}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Indicateur de synchronisation */}
      <div className="bg-green-50 border border-green-200 rounded-lg p-3">
        <div className="flex items-center gap-2 text-green-700">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-sm font-medium">Données synchronisées avec le système unifié</span>
        </div>
      </div>
    </div>
  );
}; 