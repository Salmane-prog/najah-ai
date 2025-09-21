import React from 'react';
import { Brain, CheckCircle, AlertTriangle, Clock, Target, Zap } from 'lucide-react';

export interface GenerationStatsProps {
  generatedBy: string;
  fallbackUsed: boolean;
  uniquenessValid: boolean;
  questionCount: number;
  generationTime?: number;
  qualityScore?: number;
  topics: string[];
  learningObjectives: string[];
}

export const GenerationStats: React.FC<GenerationStatsProps> = ({
  generatedBy,
  fallbackUsed,
  uniquenessValid,
  questionCount,
  generationTime,
  qualityScore,
  topics,
  learningObjectives
}) => {
  const getStatusColor = (isValid: boolean) => {
    return isValid ? 'text-green-600' : 'text-red-600';
  };

  const getStatusIcon = (isValid: boolean) => {
    return isValid ? CheckCircle : AlertTriangle;
  };

  const getGenerationMethodColor = () => {
    return fallbackUsed ? 'text-yellow-600' : 'text-green-600';
  };

  const getGenerationMethodIcon = () => {
    return fallbackUsed ? AlertTriangle : Brain;
  };

  return (
    <div className="bg-white rounded-lg border p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-xl font-semibold text-gray-900">Statistiques de Génération</h3>
        <div className="flex items-center space-x-2">
          <span className={`px-3 py-1 rounded-full text-sm font-medium ${
            fallbackUsed ? 'bg-yellow-100 text-yellow-800' : 'bg-green-100 text-green-800'
          }`}>
            {fallbackUsed ? '🔄 Mode Local' : '🤖 Mode IA'}
          </span>
        </div>
      </div>

      {/* Métriques principales */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="text-center p-4 bg-blue-50 rounded-lg">
          <div className="flex justify-center mb-2">
            <Brain className="w-6 h-6 text-blue-600" />
          </div>
          <div className="text-2xl font-bold text-blue-600">{generatedBy}</div>
          <div className="text-sm text-blue-600">Générateur</div>
        </div>

        <div className="text-center p-4 bg-green-50 rounded-lg">
          <div className="flex justify-center mb-2">
            <Target className="w-6 h-6 text-green-600" />
          </div>
          <div className="text-2xl font-bold text-green-600">{questionCount}</div>
          <div className="text-sm text-green-600">Questions</div>
        </div>

        <div className="text-center p-4 bg-purple-50 rounded-lg">
          <div className="flex justify-center mb-2">
            <CheckCircle className="w-6 h-6 text-purple-600" />
          </div>
          <div className="text-2xl font-bold text-purple-600">{topics.length}</div>
          <div className="text-sm text-purple-600">Thèmes</div>
        </div>

        <div className="text-center p-4 bg-orange-50 rounded-lg">
          <div className="flex justify-center mb-2">
            <Zap className="w-6 h-6 text-orange-600" />
          </div>
          <div className="text-2xl font-bold text-orange-600">{learningObjectives.length}</div>
          <div className="text-sm text-orange-600">Objectifs</div>
        </div>
      </div>

      {/* Statut de validation */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className={`p-4 rounded-lg border ${
          uniquenessValid ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'
        }`}>
          <div className="flex items-center space-x-2">
            {React.createElement(getStatusIcon(uniquenessValid), { 
              className: `w-5 h-5 ${getStatusColor(uniquenessValid)}` 
            })}
            <span className={`font-medium ${getStatusColor(uniquenessValid)}`}>
              {uniquenessValid ? '✅ Questions Uniques' : '❌ Doublons Détectés'}
            </span>
          </div>
          <p className="text-sm text-gray-600 mt-2">
            {uniquenessValid 
              ? 'Toutes les questions sont uniques et prêtes à l\'utilisation'
              : 'Certaines questions sont en double et nécessitent une révision'
            }
          </p>
        </div>

        <div className={`p-4 rounded-lg border ${
          fallbackUsed ? 'bg-yellow-50 border-yellow-200' : 'bg-green-50 border-green-200'
        }`}>
          <div className="flex items-center space-x-2">
            {React.createElement(getGenerationMethodIcon(), { 
              className: `w-5 h-5 ${getGenerationMethodColor()}` 
            })}
            <span className={`font-medium ${getGenerationMethodColor()}`}>
              {fallbackUsed ? '🔄 Banque Locale' : '🤖 Intelligence Artificielle'}
            </span>
          </div>
          <p className="text-sm text-gray-600 mt-2">
            {fallbackUsed 
              ? 'Questions générées depuis la banque locale étendue'
              : 'Questions générées par l\'IA avec analyse contextuelle'
            }
          </p>
        </div>
      </div>

      {/* Informations détaillées */}
      <div className="space-y-4">
        <div>
          <h4 className="font-medium text-gray-900 mb-2">Thèmes couverts :</h4>
          <div className="flex flex-wrap gap-2">
            {topics.map((topic, index) => (
              <span key={index} className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">
                {topic}
              </span>
            ))}
          </div>
        </div>

        <div>
          <h4 className="font-medium text-gray-900 mb-2">Objectifs d'apprentissage :</h4>
          <div className="space-y-2">
            {learningObjectives.map((objective, index) => (
              <div key={index} className="flex items-start space-x-2">
                <span className="text-blue-500 mt-1">•</span>
                <span className="text-sm text-gray-600">{objective}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Métriques de qualité si disponibles */}
        {(qualityScore !== undefined || generationTime !== undefined) && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4 border-t">
            {qualityScore !== undefined && (
              <div className="text-center p-3 bg-gray-50 rounded-lg">
                <div className="text-lg font-semibold text-gray-900">Score Qualité</div>
                <div className="text-3xl font-bold text-blue-600">{qualityScore}/10</div>
                <div className="text-sm text-gray-500">
                  {qualityScore >= 8 ? 'Excellent' : 
                   qualityScore >= 6 ? 'Bon' : 
                   qualityScore >= 4 ? 'Moyen' : 'À améliorer'}
                </div>
              </div>
            )}

            {generationTime !== undefined && (
              <div className="text-center p-3 bg-gray-50 rounded-lg">
                <div className="flex justify-center mb-2">
                  <Clock className="w-5 h-5 text-gray-600" />
                </div>
                <div className="text-lg font-semibold text-gray-900">Temps de Génération</div>
                <div className="text-2xl font-bold text-gray-600">{generationTime}s</div>
                <div className="text-sm text-gray-500">
                  {generationTime < 5 ? 'Très rapide' : 
                   generationTime < 10 ? 'Rapide' : 
                   generationTime < 20 ? 'Normal' : 'Lent'}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Recommandations */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div className="flex items-center space-x-2 mb-2">
          <Brain className="w-5 h-5 text-blue-600" />
          <span className="font-medium text-blue-800">Recommandations</span>
        </div>
        <div className="text-sm text-blue-700 space-y-1">
          {!uniquenessValid && (
            <div>• Vérifiez et corrigez les questions en double avant d'activer le test</div>
          )}
          {fallbackUsed && (
            <div>• Considérez la configuration de l'IA pour une génération plus avancée</div>
          )}
          {qualityScore !== undefined && qualityScore < 6 && (
            <div>• Améliorez la qualité des questions en ajoutant des explications détaillées</div>
          )}
          <div>• Testez le test avec un petit groupe d'élèves avant l'activation complète</div>
        </div>
      </div>
    </div>
  );
};


















