"use client";

import React from 'react';
import { ScoreCalculator } from '../../utils/scoreCalculator';

interface DebugWidgetProps {
  className?: string;
  quizResults?: any[];
}

export default function DebugWidget({ className = "", quizResults = [] }: DebugWidgetProps) {
  const debugData = quizResults.map((quiz, index) => {
    const rawScore = quiz.score || 0;
    const maxScore = quiz.max_score || 1;
    const oldCalculation = Math.round((rawScore / maxScore) * 100);
    const newCalculation = ScoreCalculator.calculatePercentage(rawScore, maxScore);
    
    return {
      id: index,
      quizName: quiz.quiz_name || `Quiz ${index + 1}`,
      rawScore,
      maxScore,
      oldCalculation,
      newCalculation,
      isProblematic: oldCalculation > 100 || oldCalculation < 0,
      difference: newCalculation - oldCalculation
    };
  });

  const problematicQuizzes = debugData.filter(q => q.isProblematic);
  const totalProblems = problematicQuizzes.length;

  return (
    <div className={`bg-white rounded-lg shadow-sm p-6 ${className}`}>
      <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
        🐛 Debug - Analyse des Scores
        {totalProblems > 0 && (
          <span className="bg-red-100 text-red-800 text-xs font-medium px-2 py-1 rounded-full">
            {totalProblems} problème{totalProblems > 1 ? 's' : ''}
          </span>
        )}
      </h3>
      
      <div className="space-y-4">
        {/* Résumé */}
        <div className="grid grid-cols-2 gap-4">
          <div className="p-3 bg-blue-50 rounded-lg">
            <p className="text-sm text-blue-600 font-medium">Total Quiz</p>
            <p className="text-2xl font-bold text-blue-700">{debugData.length}</p>
          </div>
          <div className="p-3 bg-red-50 rounded-lg">
            <p className="text-sm text-red-600 font-medium">Problèmes</p>
            <p className="text-2xl font-bold text-red-700">{totalProblems}</p>
          </div>
        </div>

        {/* Détails des problèmes */}
        {problematicQuizzes.length > 0 && (
          <div className="space-y-3">
            <h4 className="font-semibold text-red-700">Quiz Problématiques :</h4>
            {problematicQuizzes.map((quiz) => (
              <div key={quiz.id} className="p-3 bg-red-50 border border-red-200 rounded-lg">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-800">{quiz.quizName}</p>
                    <p className="text-xs text-gray-600">
                      Score brut: {quiz.rawScore}/{quiz.maxScore}
                    </p>
                  </div>
                  <div className="text-right">
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-medium text-red-600">
                        {quiz.oldCalculation}%
                      </span>
                      <span className="text-gray-400">→</span>
                      <span className="text-sm font-bold text-green-600">
                        {quiz.newCalculation}%
                      </span>
                    </div>
                    <p className="text-xs text-red-600 mt-1">
                      Différence: {quiz.difference > 0 ? '+' : ''}{quiz.difference}%
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Tous les quiz */}
        <div className="space-y-2">
          <h4 className="font-semibold text-gray-700">Tous les Quiz :</h4>
          <div className="max-h-40 overflow-y-auto space-y-1">
            {debugData.map((quiz) => (
              <div key={quiz.id} className={`p-2 rounded text-xs ${
                quiz.isProblematic ? 'bg-red-50 border border-red-200' : 'bg-gray-50'
              }`}>
                <div className="flex items-center justify-between">
                  <span className="font-medium">{quiz.quizName}</span>
                  <div className="flex items-center gap-2">
                    <span className={quiz.isProblematic ? 'text-red-600' : 'text-gray-600'}>
                      {quiz.oldCalculation}%
                    </span>
                    <span className="text-gray-400">→</span>
                    <span className="font-bold text-green-600">
                      {quiz.newCalculation}%
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recommandations */}
        <div className="p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
          <p className="text-sm font-medium text-yellow-800">
            {totalProblems > 0 
              ? `⚠️ ${totalProblems} quiz avec des scores incorrects détectés. Utilisez ScoreCalculator pour corriger.`
              : '✅ Tous les scores semblent corrects !'
            }
          </p>
        </div>
      </div>
    </div>
  );
} 