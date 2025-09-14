"use client";

import React, { useState, useEffect } from 'react';
import { ScoreCalculator } from '../../utils/scoreCalculator';
import { CheckCircle, AlertCircle, TrendingUp } from 'lucide-react';

interface ScoreCorrectionWidgetProps {
  className?: string;
  quizResults?: any[];
}

export default function ScoreCorrectionWidget({ className = "", quizResults = [] }: ScoreCorrectionWidgetProps) {
  const [corrections, setCorrections] = useState<any[]>([]);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    if (quizResults.length > 0) {
      const correctionsList = quizResults.map((quiz, index) => {
        const oldScore = quiz.score || 0;
        const maxScore = quiz.max_score || 1;
        const oldPercentage = Math.round((oldScore / maxScore) * 100);
        const newPercentage = ScoreCalculator.calculatePercentage(oldScore, maxScore);
        
        return {
          id: index,
          quizName: quiz.quiz_name || `Quiz ${index + 1}`,
          oldScore: oldPercentage,
          newScore: newPercentage,
          isCorrected: oldPercentage !== newPercentage,
          difference: newPercentage - oldPercentage
        };
      });

      setCorrections(correctionsList);
      setIsVisible(true);
    }
  }, [quizResults]);

  const totalCorrections = corrections.filter(c => c.isCorrected).length;
  const averageCorrection = corrections.length > 0 
    ? corrections.reduce((sum, c) => sum + Math.abs(c.difference), 0) / corrections.length 
    : 0;

  return (
    <div className={`bg-white rounded-lg shadow-sm p-6 ${className}`}>
      <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
        🔧 Corrections de Scores
        {totalCorrections > 0 && (
          <span className="bg-red-100 text-red-800 text-xs font-medium px-2 py-1 rounded-full">
            {totalCorrections} correction{totalCorrections > 1 ? 's' : ''}
          </span>
        )}
      </h3>
      
      {isVisible && (
        <div className="space-y-4 animate-fade-in">
          {/* Résumé des corrections */}
          <div className="grid grid-cols-2 gap-4">
            <div className="p-3 bg-blue-50 rounded-lg">
              <p className="text-sm text-blue-600 font-medium">Corrections</p>
              <p className="text-2xl font-bold text-blue-700">{totalCorrections}</p>
            </div>
            <div className="p-3 bg-green-50 rounded-lg">
              <p className="text-sm text-green-600 font-medium">Moyenne Correction</p>
              <p className="text-2xl font-bold text-green-700">{Math.round(averageCorrection)}%</p>
            </div>
          </div>

          {/* Liste des corrections */}
          <div className="space-y-3 max-h-96 overflow-y-auto">
            {corrections.map((correction) => (
              <div 
                key={correction.id} 
                className={`p-3 rounded-lg border ${
                  correction.isCorrected 
                    ? 'bg-red-50 border-red-200' 
                    : 'bg-green-50 border-green-200'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-800">{correction.quizName}</p>
                    <div className="flex items-center gap-2 mt-1">
                      {correction.isCorrected ? (
                        <>
                          <AlertCircle className="text-red-600" size={16} />
                          <span className="text-xs text-red-600">Corrigé</span>
                        </>
                      ) : (
                        <>
                          <CheckCircle className="text-green-600" size={16} />
                          <span className="text-xs text-green-600">Correct</span>
                        </>
                      )}
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="flex items-center gap-2">
                      <span className={`text-sm font-medium ${
                        correction.isCorrected ? 'text-red-600' : 'text-green-600'
                      }`}>
                        {correction.oldScore}%
                      </span>
                      <TrendingUp className="text-gray-400" size={16} />
                      <span className="text-sm font-bold text-gray-800">
                        {correction.newScore}%
                      </span>
                    </div>
                    {correction.isCorrected && (
                      <p className="text-xs text-red-600 mt-1">
                        {correction.difference > 0 ? '+' : ''}{correction.difference}%
                      </p>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Message de statut */}
          <div className={`p-3 rounded-lg ${
            totalCorrections > 0 
              ? 'bg-yellow-50 border border-yellow-200' 
              : 'bg-green-50 border border-green-200'
          }`}>
            <p className="text-sm font-medium text-gray-800">
              {totalCorrections > 0 
                ? `✅ ${totalCorrections} score${totalCorrections > 1 ? 's' : ''} corrigé${totalCorrections > 1 ? 's' : ''} avec le nouveau ScoreCalculator`
                : '✅ Tous les scores sont corrects !'
              }
            </p>
          </div>
        </div>
      )}

      {!isVisible && (
        <div className="flex items-center justify-center py-8">
          <div className="text-gray-500 text-sm">Chargement des corrections...</div>
        </div>
      )}
    </div>
  );
} 