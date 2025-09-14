'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/hooks/useAuthSimple';
import { ArrowLeft, CheckCircle, XCircle, Brain, Shuffle } from 'lucide-react';
import { useRouter } from 'next/navigation';

interface MatchingPageProps {
  params: {
    topic: string;
  };
}

export default function MatchingPage({ params }: MatchingPageProps) {
  const { user, token } = useAuth();
  const router = useRouter();
  const { topic } = React.use(params);
  
  // Exercices de matching prédéfinis
  const [exercise] = useState(() => {
    switch (topic) {
      case 'vocabulary':
        return {
          id: 'vocab_matching_001',
          type: 'matching',
          question: 'Associez les mots de famille avec leurs définitions',
          explanation: 'Faites correspondre chaque mot de famille à sa définition correcte.',
          difficulty: 'facile',
          topic: 'Vocabulaire',
          estimated_time: 4,
          pairs: [
            ['père', 'Parent masculin'],
            ['mère', 'Parent féminin'],
            ['frère', 'Enfant masculin de mêmes parents'],
            ['sœur', 'Enfant féminin de mêmes parents'],
            ['grand-père', 'Père du père ou de la mère'],
            ['grand-mère', 'Mère du père ou de la mère']
          ]
        };
        
      case 'grammar':
        return {
          id: 'grammar_matching_001',
          type: 'matching',
          question: 'Associez les mots avec leurs catégories grammaticales',
          explanation: 'Faites correspondre chaque mot à sa catégorie grammaticale.',
          difficulty: 'facile',
          topic: 'Grammaire',
          estimated_time: 4,
          pairs: [
            ['maison', 'Nom commun'],
            ['grand', 'Adjectif'],
            ['manger', 'Verbe'],
            ['rapidement', 'Adverbe'],
            ['le', 'Article défini'],
            ['mon', 'Déterminant possessif']
          ]
        };
        
      case 'conjugation':
        return {
          id: 'conj_matching_001',
          type: 'matching',
          question: 'Associez les verbes avec leurs conjugaisons',
          explanation: 'Faites correspondre chaque verbe à sa conjugaison correcte.',
          difficulty: 'facile',
          topic: 'Conjugaison',
          estimated_time: 4,
          pairs: [
            ['je mange', '1ère personne du singulier'],
            ['tu manges', '2ème personne du singulier'],
            ['il mange', '3ème personne du singulier'],
            ['nous mangeons', '1ère personne du pluriel'],
            ['vous mangez', '2ème personne du pluriel'],
            ['ils mangent', '3ème personne du pluriel']
          ]
        };
        
      default:
        return {
          id: 'general_matching_001',
          type: 'matching',
          question: 'Associez les éléments avec leurs correspondances',
          explanation: 'Faites correspondre chaque élément à sa correspondance correcte.',
          difficulty: 'facile',
          topic: 'Général',
          estimated_time: 4,
          pairs: [
            ['chat', 'Animal domestique qui miaule'],
            ['livre', 'Objet avec des pages à lire'],
            ['voiture', 'Moyen de transport à 4 roues'],
            ['arbre', 'Plante avec un tronc et des feuilles'],
            ['soleil', 'Étoile qui éclaire la Terre'],
            ['eau', 'Liquide transparent et incolore']
          ]
        };
    }
  });

  // Séparer les paires en items gauche et droite
  const [leftItems] = useState(() => exercise.pairs.map(pair => pair[0]));
  const [rightItems] = useState(() => {
    const right = exercise.pairs.map(pair => pair[1]);
    return [...right].sort(() => Math.random() - 0.5); // Mélanger
  });

  const [selectedLeft, setSelectedLeft] = useState<string | null>(null);
  const [selectedRight, setSelectedRight] = useState<string | null>(null);
  const [matches, setMatches] = useState<Map<string, string>>(new Map());
  const [score, setScore] = useState(0);
  const [completed, setCompleted] = useState(false);

  console.log('🎯 [MATCHING PAGE] Exercice chargé:', exercise);
  console.log('📝 [MATCHING PAGE] Items gauche:', leftItems);
  console.log('📝 [MATCHING PAGE] Items droite:', rightItems);

  const handleLeftItemClick = (item: string) => {
    if (completed) return;
    setSelectedLeft(selectedLeft === item ? null : item);
  };

  const handleRightItemClick = (item: string) => {
    if (completed || !selectedLeft) return;
    
    // Vérifier si la correspondance est correcte
    const correctMatch = exercise.pairs.find(pair => pair[0] === selectedLeft);
    const isCorrect = correctMatch && correctMatch[1] === item;
    
    if (isCorrect) {
      // Ajouter la correspondance correcte
      setMatches(prev => new Map(prev.set(selectedLeft, item)));
      setScore(score + 1);
      
      // Vérifier si l'exercice est terminé
      if (matches.size + 1 === leftItems.length) {
        setCompleted(true);
      }
    }
    
    setSelectedLeft(null);
  };

  const isMatched = (item: string) => {
    return Array.from(matches.values()).includes(item);
  };

  const getMatchedPair = (item: string) => {
    for (const [left, right] of matches.entries()) {
      if (right === item) return left;
    }
    return null;
  };

  const getTopicIcon = (topic: string) => {
    switch (topic) {
      case 'vocabulary': return <Brain className="w-6 h-6 text-green-500" />;
      case 'grammar': return <Brain className="w-6 h-6 text-blue-500" />;
      case 'conjugation': return <Brain className="w-6 h-6 text-purple-500" />;
      default: return <Brain className="w-6 h-6 text-gray-500" />;
    }
  };

  const getTopicTitle = (topic: string) => {
    switch (topic) {
      case 'vocabulary': return 'Vocabulaire';
      case 'grammar': return 'Grammaire';
      case 'conjugation': return 'Conjugaison';
      default: return 'Général';
    }
  };

  const progress = (matches.size / leftItems.length) * 100;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <button
              onClick={() => router.back()}
              className="flex items-center gap-2 text-gray-600 hover:text-gray-800 transition-colors"
            >
              <ArrowLeft className="w-5 h-5" />
              Retour
            </button>
            
            <div className="text-center">
              <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-3 justify-center">
                {getTopicIcon(topic)}
                Quiz de Remédiation - {getTopicTitle(topic)} Française
              </h1>
            </div>
            
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 text-gray-600">
                <Brain className="w-4 h-4" />
                <span>4:50</span>
              </div>
              <div className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                Score: {score}/{leftItems.length}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="max-w-6xl mx-auto px-4 py-4">
        <div className="mb-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-gray-600">
              Question {leftItems.length} sur {leftItems.length}
            </span>
            <span className="text-sm font-medium text-gray-900">
              {Math.round(progress)}%
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
            <div 
              className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full transition-all duration-300"
              style={{ width: `${Math.min(progress, 100)}%` }}
            ></div>
          </div>
        </div>
      </div>

      {/* Exercise Instructions */}
      <div className="max-w-6xl mx-auto px-4 py-4">
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <h2 className="font-semibold text-blue-900 mb-2">Instructions :</h2>
          <p className="text-blue-800">{exercise.question}</p>
        </div>
      </div>

      {/* Matching Exercise */}
      <div className="max-w-6xl mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-900 text-center mb-4">
              Cliquez sur un élément à gauche ({leftItems.length} éléments)
            </h3>
            {leftItems.map((item, index) => (
              <div
                key={index}
                onClick={() => handleLeftItemClick(item)}
                className={`p-4 border-2 rounded-lg cursor-pointer transition-all ${
                  selectedLeft === item
                    ? 'border-green-500 bg-green-50'
                    : matches.has(item)
                    ? 'border-green-500 bg-green-100 cursor-default'
                    : 'border-gray-200 hover:border-gray-300 bg-white'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-gray-900 font-medium">{item}</span>
                  {matches.has(item) && (
                    <CheckCircle className="w-5 h-5 text-green-500" />
                  )}
                </div>
              </div>
            ))}
          </div>

          {/* Right Column */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-900 text-center mb-4">
              Puis cliquez sur sa correspondance à droite ({rightItems.length} éléments)
            </h3>
            {rightItems.map((item, index) => (
              <div
                key={index}
                onClick={() => handleRightItemClick(item)}
                className={`p-4 border-2 rounded-lg cursor-pointer transition-all ${
                  isMatched(item)
                    ? 'border-green-500 bg-green-100 cursor-default'
                    : selectedLeft && !isMatched(item)
                    ? 'border-blue-300 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300 bg-white'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-gray-900 font-medium">{item}</span>
                  {isMatched(item) && (
                    <CheckCircle className="w-5 h-5 text-green-500" />
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Matches Display */}
      {matches.size > 0 && (
        <div className="max-w-6xl mx-auto px-4 py-6">
          <div className="bg-green-50 border border-green-200 rounded-lg p-6">
            <h3 className="font-semibold text-green-900 mb-4 text-center">
              Correspondances trouvées ({matches.size}/{leftItems.length})
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {Array.from(matches.entries()).map(([left, right], index) => (
                <div key={index} className="bg-white p-3 rounded-lg border border-green-200">
                  <div className="flex items-center justify-between">
                    <span className="font-medium text-gray-900">{left}</span>
                    <span className="text-gray-500 mx-2">→</span>
                    <span className="text-gray-700">{right}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Completion Message */}
      {completed && (
        <div className="max-w-6xl mx-auto px-4 py-6">
          <div className="bg-gradient-to-r from-green-50 to-blue-50 rounded-lg border border-green-200 p-8 text-center">
            <h3 className="text-3xl font-bold text-green-800 mb-4">
              🎉 Exercice Terminé !
            </h3>
            <div className="text-2xl font-bold text-green-600 mb-4">
              Score: {score}/{leftItems.length}
            </div>
            <p className="text-green-700 mb-6 text-lg">
              {score === leftItems.length ? 'Parfait ! Toutes les correspondances sont correctes !' :
               score >= leftItems.length * 0.8 ? 'Excellent travail !' :
               score >= leftItems.length * 0.6 ? 'Bon travail ! Continuez à vous entraîner.' :
               'Continuez à vous entraîner pour améliorer vos compétences.'}
            </p>
            
            {exercise.explanation && (
              <div className="bg-white p-4 rounded-lg border border-green-200 mb-6 text-left">
                <h4 className="font-semibold text-green-900 mb-2">Explication :</h4>
                <p className="text-green-800">{exercise.explanation}</p>
              </div>
            )}
            
            <div className="flex gap-4 justify-center">
              <button
                onClick={() => window.location.reload()}
                className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors flex items-center gap-2"
              >
                <Shuffle className="w-4 h-4" />
                Recommencer
              </button>
              <button
                onClick={() => router.push('/dashboard/student/remediation')}
                className="px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium transition-colors"
              >
                Retour à la Remédiation
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
