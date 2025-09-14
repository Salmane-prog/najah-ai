'use client';

import React from 'react';
import SimpleIcon, { SimpleIconWithBackground, SimpleCardIcon } from '../ui/SimpleIcon';

interface UnifiedStatsWidgetProps {
  className?: string;
  loading?: boolean;
  isRealData?: boolean;
  stats?: {
    quizzesCompleted?: number;
    averageScore?: number;
    consecutiveDays?: number;
    badgesEarned?: number;
    totalPoints?: number;
    challengesCompleted?: number;
    totalQuizzes?: number;
    bestScore?: number;
  };
}

export default function UnifiedStatsWidget({ className = '', loading = false, isRealData = false, stats = {} }: UnifiedStatsWidgetProps) {
  const {
    quizzesCompleted = 0,
    averageScore = 0,
    consecutiveDays = 0,
    badgesEarned = 0,
    totalPoints = 0,
    challengesCompleted = 0,
    totalQuizzes = 0,
    bestScore = 0
  } = stats;

  // 🔧 CORRECTION : Utiliser le même système de calcul que les badges (500 points par niveau)
  // Au lieu de 1000 XP par niveau pour éviter l'incohérence
  const calculateLevel = (points: number): number => {
    return Math.floor(points / 500) + 1;
  };
  
  const currentLevel = calculateLevel(totalPoints);
  const xpInCurrentLevel = totalPoints % 500;
  const xpToNextLevel = 500;
  const progressPercentage = Math.min((xpInCurrentLevel / xpToNextLevel) * 100, 100);
  
  // Déterminer le rang basé sur le niveau
  const getRank = (level: number): string => {
    if (level <= 2) return 'Débutant';
    if (level <= 5) return 'Intermédiaire';
    if (level <= 10) return 'Avancé';
    return 'Expert';
  };

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Indicateur de données réelles */}
      {isRealData && (
        <div className="flex items-center justify-center gap-2 p-3 bg-green-50 border border-green-200 rounded-lg">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-green-600 font-medium text-sm">
            Données unifiées en temps réel (Quiz adaptatifs + Remédiation + Quiz assignés)
          </span>
        </div>
      )}

      {/* Indicateur de chargement */}
      {loading && (
        <div className="flex items-center justify-center gap-2 p-3 bg-blue-50 border border-blue-200 rounded-lg">
          <div className="w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
          <span className="text-blue-600 font-medium text-sm">
            Chargement des métriques unifiées...
          </span>
        </div>
      )}

      {/* Statistiques principales */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="card-stat card-stat-primary">
          <div className="card-stat-icon">
            <SimpleIcon name="check" size="lg" color="white" />
          </div>
          <div className="card-stat-value">{quizzesCompleted}</div>
          <div className="card-stat-label">Quiz Complétés</div>
        </div>

        <div className="card-stat card-stat-info">
          <div className="card-stat-icon">
            <SimpleIcon name="arrow-up" size="lg" color="white" />
          </div>
          <div className="card-stat-value">{averageScore.toFixed(1)}%</div>
          <div className="card-stat-label">Score Moyen</div>
        </div>

        <div className="card-stat card-stat-warning">
          <div className="card-stat-icon">
            <SimpleIcon name="star" size="lg" color="white" />
          </div>
          <div className="card-stat-value">{consecutiveDays}</div>
          <div className="card-stat-label">Jours Consécutifs</div>
        </div>

        <div className="card-stat card-stat-secondary">
          <div className="card-stat-icon">
            <SimpleIcon name="heart" size="lg" color="white" />
          </div>
          <div className="card-stat-value">{badgesEarned}</div>
          <div className="card-stat-label">Badges Obtenus</div>
        </div>
      </div>

      {/* Barre de progression */}
      <div className="card-unified">
        <div className="card-unified-body">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <SimpleIconWithBackground name="star" backgroundType="warning" size="lg" />
              <div>
                <h3 className="text-lg font-semibold text-primary">Niveau {currentLevel} {getRank(currentLevel)}</h3>
                <p className="text-sm text-secondary">{xpInCurrentLevel}/{xpToNextLevel} XP</p>
              </div>
            </div>
            <div className="text-right">
              <div className="text-2xl font-bold text-success">Progression {progressPercentage.toFixed(1)}%</div>
              <p className="text-sm text-muted">Vers le niveau {currentLevel + 1}</p>
            </div>
          </div>
          
          <div className="progress-unified progress-unified-large">
            <div 
              className="progress-unified-bar" 
              style={{ width: `${progressPercentage}%` }}
            ></div>
          </div>
          
          <div className="flex justify-between mt-2 text-sm text-muted">
            <span>Niveau {currentLevel}</span>
            <span>Niveau {currentLevel + 1}</span>
          </div>
        </div>
      </div>

      {/* Statistiques détaillées */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="card-unified">
          <div className="card-unified-header">
            <div className="flex items-center gap-3">
              <SimpleIconWithBackground name="star" backgroundType="warning" size="lg" />
              <h3 className="text-lg font-semibold">Points & Achievements</h3>
            </div>
          </div>
          <div className="card-unified-body">
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-muted">Points Totaux:</span>
                <span className="font-semibold text-primary">{totalPoints}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-muted">Points Achievements:</span>
                <span className="font-semibold text-success">+{badgesEarned * 50}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-muted">Points Challenges:</span>
                <span className="font-semibold text-warning">+{challengesCompleted * 25}</span>
              </div>
            </div>
          </div>
        </div>

        <div className="card-unified">
          <div className="card-unified-header">
            <div className="flex items-center gap-3">
              <SimpleIconWithBackground name="grid" backgroundType="info" size="lg" />
              <h3 className="text-lg font-semibold">Challenges & Activité</h3>
            </div>
          </div>
          <div className="card-unified-body">
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-muted">Challenges Complétés:</span>
                <span className="font-semibold text-warning">{challengesCompleted}/5</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-muted">Quiz Total:</span>
                <span className="font-semibold text-info">{totalQuizzes}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-muted">Meilleur Score:</span>
                <span className="font-semibold text-success">{bestScore.toFixed(1)}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Message de synchronisation */}
      <div className="alert-unified alert-unified-success">
        <SimpleIcon name="check" size="md" color="success" />
        <div>
          <p className="font-medium">Toutes les statistiques sont synchronisées et cohérentes</p>
          <p className="text-sm text-success-600">Vos données sont mises à jour en temps réel</p>
        </div>
      </div>
    </div>
  );
}
