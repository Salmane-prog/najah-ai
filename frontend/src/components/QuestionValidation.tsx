import React from 'react';
import { CheckCircle, AlertTriangle, XCircle, Info } from 'lucide-react';

export interface QuestionValidationResult {
  isValid: boolean;
  duplicates: string[];
  qualityScore: number;
  suggestions: string[];
  warnings: string[];
}

interface QuestionValidationProps {
  questions: any[];
  onValidationComplete: (result: QuestionValidationResult) => void;
}

export const QuestionValidation: React.FC<QuestionValidationProps> = ({
  questions,
  onValidationComplete
}) => {
  const [validationResult, setValidationResult] = React.useState<QuestionValidationResult | null>(null);
  const [isValidating, setIsValidating] = React.useState(false);

  React.useEffect(() => {
    if (questions.length > 0) {
      validateQuestions();
    }
  }, [questions]);

  const validateQuestions = () => {
    setIsValidating(true);
    
    // Validation de l'unicité
    const uniquenessCheck = validateUniqueness(questions);
    
    // Validation de la qualité
    const qualityCheck = validateQuality(questions);
    
    // Génération des suggestions
    const suggestions = generateSuggestions(uniquenessCheck, qualityCheck);
    
    // Génération des avertissements
    const warnings = generateWarnings(uniquenessCheck, qualityCheck);
    
    const result: QuestionValidationResult = {
      isValid: uniquenessCheck.isValid && qualityCheck.score >= 7,
      duplicates: uniquenessCheck.duplicates,
      qualityScore: qualityCheck.score,
      suggestions,
      warnings
    };
    
    setValidationResult(result);
    onValidationComplete(result);
    setIsValidating(false);
  };

  const validateUniqueness = (questions: any[]) => {
    const seenQuestions = new Set<string>();
    const duplicates: string[] = [];
    
    for (const question of questions) {
      const questionKey = `${question.question}-${question.topic || 'général'}`;
      if (seenQuestions.has(questionKey)) {
        duplicates.push(questionKey);
      } else {
        seenQuestions.add(questionKey);
      }
    }
    
    return {
      isValid: duplicates.length === 0,
      duplicates,
      uniqueCount: seenQuestions.size,
      totalCount: questions.length
    };
  };

  const validateQuality = (questions: any[]) => {
    let totalScore = 0;
    const maxScore = questions.length * 10;
    
    for (const question of questions) {
      let questionScore = 0;
      
      // Vérifier la longueur de la question
      if (question.question && question.question.length >= 20) questionScore += 2;
      
      // Vérifier les options
      if (question.options && question.options.length === 4) questionScore += 2;
      
      // Vérifier la réponse correcte
      if (question.correctAnswer !== undefined && question.correctAnswer >= 0 && question.correctAnswer < 4) questionScore += 2;
      
      // Vérifier l'explication
      if (question.explanation && question.explanation.length >= 30) questionScore += 2;
      
      // Vérifier la difficulté
      if (question.difficulty && question.difficulty >= 1 && question.difficulty <= 10) questionScore += 1;
      
      // Vérifier l'objectif d'apprentissage
      if (question.learningObjective && question.learningObjective.length > 0) questionScore += 1;
      
      totalScore += questionScore;
    }
    
    return {
      score: Math.round((totalScore / maxScore) * 10),
      totalScore,
      maxScore
    };
  };

  const generateSuggestions = (uniquenessCheck: any, qualityCheck: any): string[] => {
    const suggestions: string[] = [];
    
    if (!uniquenessCheck.isValid) {
      suggestions.push(`Résoudre ${uniquenessCheck.duplicates.length} question(s) en double`);
    }
    
    if (qualityCheck.score < 8) {
      suggestions.push('Améliorer la qualité des questions (longueur, explications)');
    }
    
    if (qualityCheck.score < 6) {
      suggestions.push('Vérifier que toutes les questions ont 4 options valides');
    }
    
    return suggestions;
  };

  const generateWarnings = (uniquenessCheck: any, qualityCheck: any): string[] => {
    const warnings: string[] = [];
    
    if (uniquenessCheck.duplicates.length > 0) {
      warnings.push(`${uniquenessCheck.duplicates.length} question(s) en double détectée(s)`);
    }
    
    if (qualityCheck.score < 5) {
      warnings.push('Qualité des questions insuffisante');
    }
    
    return warnings;
  };

  if (isValidating) {
    return (
      <div className="flex items-center justify-center p-4">
        <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
        <span className="ml-2 text-gray-600">Validation en cours...</span>
      </div>
    );
  }

  if (!validationResult) {
    return null;
  }

  return (
    <div className="bg-white rounded-lg border p-4 space-y-4">
      <div className="flex items-center space-x-2">
        <h3 className="text-lg font-semibold text-gray-900">Validation des Questions</h3>
        {validationResult.isValid ? (
          <CheckCircle className="w-5 h-5 text-green-600" />
        ) : (
          <XCircle className="w-5 h-5 text-red-600" />
        )}
      </div>

      {/* Résumé de validation */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="text-center p-3 bg-gray-50 rounded-lg">
          <div className="text-2xl font-bold text-blue-600">
            {validationResult.qualityScore}/10
          </div>
          <div className="text-sm text-gray-600">Score Qualité</div>
        </div>
        
        <div className="text-center p-3 bg-gray-50 rounded-lg">
          <div className="text-2xl font-bold text-green-600">
            {questions.length - validationResult.duplicates.length}
          </div>
          <div className="text-sm text-gray-600">Questions Uniques</div>
        </div>
        
        <div className="text-center p-3 bg-gray-50 rounded-lg">
          <div className="text-2xl font-bold text-orange-600">
            {validationResult.duplicates.length}
          </div>
          <div className="text-sm text-gray-600">Doublons</div>
        </div>
      </div>

      {/* Statut de validation */}
      <div className={`p-3 rounded-lg ${
        validationResult.isValid 
          ? 'bg-green-50 border border-green-200' 
          : 'bg-red-50 border border-red-200'
      }`}>
        <div className="flex items-center space-x-2">
          {validationResult.isValid ? (
            <CheckCircle className="w-5 h-5 text-green-600" />
          ) : (
            <XCircle className="w-5 h-5 text-red-600" />
          )}
          <span className={`font-medium ${
            validationResult.isValid ? 'text-green-800' : 'text-red-800'
          }`}>
            {validationResult.isValid 
              ? '✅ Validation réussie - Test prêt à être activé' 
              : '❌ Validation échouée - Corrections nécessaires'
            }
          </span>
        </div>
      </div>

      {/* Suggestions d'amélioration */}
      {validationResult.suggestions.length > 0 && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
          <div className="flex items-center space-x-2 mb-2">
            <Info className="w-5 h-5 text-blue-600" />
            <span className="font-medium text-blue-800">Suggestions d'amélioration</span>
          </div>
          <ul className="text-sm text-blue-700 space-y-1">
            {validationResult.suggestions.map((suggestion, index) => (
              <li key={index} className="flex items-start space-x-2">
                <span className="text-blue-500">•</span>
                <span>{suggestion}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Avertissements */}
      {validationResult.warnings.length > 0 && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
          <div className="flex items-center space-x-2 mb-2">
            <AlertTriangle className="w-5 h-5 text-yellow-600" />
            <span className="font-medium text-yellow-800">Avertissements</span>
          </div>
          <ul className="text-sm text-yellow-700 space-y-1">
            {validationResult.warnings.map((warning, index) => (
              <li key={index} className="flex items-start space-x-2">
                <span className="text-yellow-500">⚠</span>
                <span>{warning}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Détails des doublons */}
      {validationResult.duplicates.length > 0 && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-3">
          <div className="flex items-center space-x-2 mb-2">
            <XCircle className="w-5 h-5 text-red-600" />
            <span className="font-medium text-red-800">Questions en double détectées</span>
          </div>
          <div className="text-sm text-red-700">
            {validationResult.duplicates.slice(0, 3).map((duplicate, index) => (
              <div key={index} className="mb-1">
                • {duplicate}
              </div>
            ))}
            {validationResult.duplicates.length > 3 && (
              <div className="text-red-600">
                ... et {validationResult.duplicates.length - 3} autre(s)
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
