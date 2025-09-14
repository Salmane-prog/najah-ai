"use client";

import React from 'react';
import { ScoreCalculator } from '../../utils/scoreCalculator';

interface ScoreTestWidgetProps {
  className?: string;
}

export default function ScoreTestWidget({ className = "" }: ScoreTestWidgetProps) {
  // Données de test pour vérifier les calculs
  const testQuizResults = [
    { score: 85, max_score: 100, completed: true },
    { score: 72, max_score: 100, completed: true },
    { score: 90, max_score: 100, completed: true },
    { score: 0, max_score: 100, completed: false },
    { score: 95, max_score: 100, completed: true },
  ];

  const stats = ScoreCalculator.calculateGlobalStats(testQuizResults);
  const averageScore = ScoreCalculator.calculateAverageScore(testQuizResults);
  const xpProgress = ScoreCalculator.calculateXpProgress(150, 200);
  const level = ScoreCalculator.calculateLevel(150);
  const rank = ScoreCalculator.calculateRank(level);

  return (
    <div className={`bg-white rounded-lg shadow-sm p-6 ${className}`}>
      <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
        🧪 Test des Calculs de Scores
      </h3>
      
      <div className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div className="p-3 bg-blue-50 rounded-lg">
            <p className="text-sm text-blue-600 font-medium">Score Moyen</p>
            <p className="text-2xl font-bold text-blue-700">{averageScore}%</p>
          </div>
          <div className="p-3 bg-green-50 rounded-lg">
            <p className="text-sm text-green-600 font-medium">Quiz Complétés</p>
            <p className="text-2xl font-bold text-green-700">{stats.completedQuizzes}/{stats.totalQuizzes}</p>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="p-3 bg-purple-50 rounded-lg">
            <p className="text-sm text-purple-600 font-medium">Niveau</p>
            <p className="text-2xl font-bold text-purple-700">{level}</p>
          </div>
          <div className="p-3 bg-orange-50 rounded-lg">
            <p className="text-sm text-orange-600 font-medium">Rang</p>
            <p className="text-2xl font-bold text-orange-700">{rank}</p>
          </div>
        </div>

        <div className="p-3 bg-gray-50 rounded-lg">
          <p className="text-sm text-gray-600 font-medium">Progression XP</p>
          <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
            <div 
              className="bg-gradient-to-r from-blue-500 to-purple-600 h-2 rounded-full progress-bar-animated"
              style={{ width: `${xpProgress}%` }}
            ></div>
          </div>
          <p className="text-xs text-gray-500 mt-1">{xpProgress}% (150/200 XP)</p>
        </div>

        <div className="p-3 bg-yellow-50 rounded-lg">
          <p className="text-sm text-yellow-600 font-medium">Détails des Calculs</p>
          <div className="text-xs text-gray-600 mt-2 space-y-1">
            <p>• Score 85/100 = {ScoreCalculator.calculatePercentage(85, 100)}%</p>
            <p>• Score 72/100 = {ScoreCalculator.calculatePercentage(72, 100)}%</p>
            <p>• Score 90/100 = {ScoreCalculator.calculatePercentage(90, 100)}%</p>
            <p>• Score 95/100 = {ScoreCalculator.calculatePercentage(95, 100)}%</p>
            <p>• Moyenne: {averageScore}% ✅</p>
          </div>
        </div>
      </div>
    </div>
  );
} 