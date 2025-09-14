import React from 'react';
import { Edit, TrendingUp, AlertTriangle, CheckCircle, Clock, BarChart3 } from 'lucide-react';

interface CorrectionsWidgetProps {
  correctionData?: any;
  className?: string;
}

export const CorrectionsWidget: React.FC<CorrectionsWidgetProps> = ({ 
  correctionData,
  className = '' 
}) => {
  const totalCorrections = correctionData?.total_corrections || 0;
  const averageCorrection = correctionData?.average_correction || 0;
  const correctionsBySubject = correctionData?.corrections_by_subject || [];

  const getCorrectionStatus = (adjustment: number) => {
    if (adjustment > 0) return { icon: <TrendingUp className="text-green-500" size={16} />, color: 'text-green-600', bg: 'bg-green-100' };
    if (adjustment < 0) return { icon: <AlertTriangle className="text-red-500" size={16} />, color: 'text-red-600', bg: 'bg-red-100' };
    return { icon: <CheckCircle className="text-blue-500" size={16} />, color: 'text-blue-600', bg: 'bg-blue-100' };
  };

  const formatAdjustment = (adjustment: number) => {
    const sign = adjustment > 0 ? '+' : '';
    return `${sign}${adjustment.toFixed(1)}%`;
  };

  return (
    <div className={`space-y-6 ${className}`}>
      <div className="flex items-center gap-2 mb-4">
        <Edit className="text-blue-500" size={24} />
        <h3 className="text-xl font-bold text-gray-800">Corrections de Scores</h3>
      </div>

      {/* Statistiques principales */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-2">
            <BarChart3 className="text-blue-500" size={16} />
            <span className="text-sm font-medium">Total Corrections</span>
          </div>
          <div className="text-2xl font-bold text-blue-600">
            {totalCorrections}
          </div>
          <div className="text-xs text-gray-500">
            Corrections effectuées
          </div>
        </div>

        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-2">
            <TrendingUp className="text-green-500" size={16} />
            <span className="text-sm font-medium">Moyenne Ajustement</span>
          </div>
          <div className="text-2xl font-bold text-green-600">
            {formatAdjustment(averageCorrection)}
          </div>
          <div className="text-xs text-gray-500">
            Par correction
          </div>
        </div>
      </div>

      {/* Corrections par sujet */}
      {correctionsBySubject.length > 0 && (
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <h4 className="font-semibold text-gray-800 mb-3">Corrections par Sujet</h4>
          <div className="space-y-3 max-h-96 overflow-y-auto">
            {correctionsBySubject.map((subject: any, index: number) => {
              const status = getCorrectionStatus(subject.average_adjustment);
              
              return (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center ${status.bg}`}>
                      {status.icon}
                    </div>
                    <div>
                      <p className="font-medium text-gray-800">{subject.subject}</p>
                      <p className="text-xs text-gray-500">{subject.count} corrections</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className={`font-bold ${status.color}`}>
                      {formatAdjustment(subject.average_adjustment)}
                    </p>
                    <p className="text-xs text-gray-500">moyenne</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Résumé des corrections */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded-lg p-4">
        <div className="flex items-center gap-2 mb-3">
          <Clock className="text-blue-500" size={16} />
          <span className="font-semibold text-blue-800">Résumé des Corrections</span>
        </div>
        
        {totalCorrections > 0 ? (
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-gray-600">Corrections positives:</span>
              <span className="font-medium text-green-600">
                {correctionsBySubject.filter((s: any) => s.average_adjustment > 0).length} sujets
              </span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-gray-600">Corrections négatives:</span>
              <span className="font-medium text-red-600">
                {correctionsBySubject.filter((s: any) => s.average_adjustment < 0).length} sujets
              </span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-gray-600">Aucune correction:</span>
              <span className="font-medium text-blue-600">
                {correctionsBySubject.filter((s: any) => s.average_adjustment === 0).length} sujets
              </span>
            </div>
          </div>
        ) : (
          <div className="text-center py-4">
            <Edit className="mx-auto mb-2 text-gray-400" size={24} />
            <p className="text-gray-500">Aucune correction effectuée</p>
            <p className="text-sm text-gray-400">Les corrections apparaîtront ici</p>
          </div>
        )}
      </div>

      {/* Conseils pour les corrections */}
      {totalCorrections > 0 && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-2">
            <AlertTriangle className="text-yellow-500" size={16} />
            <span className="font-semibold text-yellow-800">Conseils</span>
          </div>
          <div className="text-sm text-yellow-700 space-y-1">
            <p>• Les corrections positives indiquent une amélioration de vos scores</p>
            <p>• Les corrections négatives suggèrent une révision nécessaire</p>
            <p>• Consultez régulièrement vos corrections pour identifier vos points faibles</p>
          </div>
        </div>
      )}
    </div>
  );
}; 