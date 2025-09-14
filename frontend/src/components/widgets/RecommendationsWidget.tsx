'use client';

import React from 'react';
import { Card } from '../Card';
import { Lightbulb, BookOpen, Play, Target, ArrowRight } from 'lucide-react';

interface Recommendation {
  type: string;
  id: number;
  title: string;
  name?: string;
}

interface RecommendationsWidgetProps {
  recommendations: Recommendation[];
  className?: string;
}

export default function RecommendationsWidget({ recommendations, className = '' }: RecommendationsWidgetProps) {
  const getRecommendationIcon = (type: string) => {
    switch (type) {
      case 'content':
        return <BookOpen className="text-blue-600" size={20} />;
      case 'learning_path':
        return <Play className="text-green-600" size={20} />;
      case 'quiz':
        return <Target className="text-purple-600" size={20} />;
      default:
        return <Lightbulb className="text-yellow-600" size={20} />;
    }
  };

  const getRecommendationColor = (type: string) => {
    switch (type) {
      case 'content':
        return 'from-blue-50 to-blue-100 border-blue-200';
      case 'learning_path':
        return 'from-green-50 to-green-100 border-green-200';
      case 'quiz':
        return 'from-purple-50 to-purple-100 border-purple-200';
      default:
        return 'from-yellow-50 to-yellow-100 border-yellow-200';
    }
  };

  const getRecommendationTextColor = (type: string) => {
    switch (type) {
      case 'content':
        return 'text-blue-700';
      case 'learning_path':
        return 'text-green-700';
      case 'quiz':
        return 'text-purple-700';
      default:
        return 'text-yellow-700';
    }
  };

  const getRecommendationTypeLabel = (type: string) => {
    switch (type) {
      case 'content':
        return 'Contenu';
      case 'learning_path':
        return 'Parcours';
      case 'quiz':
        return 'Quiz';
      default:
        return 'Recommandation';
    }
  };

  return (
    <Card title="Recommandations Personnalisées" icon={<Lightbulb />} className={`p-8 shadow-lg rounded-2xl ${className}`}>
      <div className="space-y-8">
        {/* En-tête avec statistiques */}
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-xl font-bold text-gray-800">
              {recommendations.length} recommandation{recommendations.length > 1 ? 's' : ''} pour toi
            </h3>
            <p className="text-base text-gray-600">
              Basées sur tes performances récentes
            </p>
          </div>
          <div className="w-14 h-14 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-full flex items-center justify-center shadow-md">
            <Lightbulb className="text-white" size={28} />
          </div>
        </div>

        {/* Liste des recommandations */}
        <div className="space-y-6 max-h-96 overflow-y-auto">
          {recommendations.length > 0 ? (
            recommendations.map((rec, index) => (
              <div
                key={`${rec.type}-${rec.id}`}
                className={`p-5 rounded-xl border-2 bg-gradient-to-r ${getRecommendationColor(rec.type)} transition-all duration-300 hover:scale-105 hover:shadow-lg group cursor-pointer shadow-md`}
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <div className="flex items-start gap-5">
                  {/* Icône */}
                  <div className="w-14 h-14 bg-white rounded-xl flex items-center justify-center shadow-md group-hover:shadow-lg transition-shadow">
                    {getRecommendationIcon(rec.type)}
                  </div>

                  {/* Contenu */}
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <span className={`px-2 py-1 rounded-full text-xs font-bold bg-white ${getRecommendationTextColor(rec.type)}`}>
                        {getRecommendationTypeLabel(rec.type)}
                      </span>
                      <span className="text-xs text-gray-500">#{rec.id}</span>
                    </div>
                    
                    <h4 className="font-bold text-lg text-gray-800 mb-1 group-hover:text-gray-900 transition-colors">
                      {rec.title || rec.name || 'Contenu recommandé'}
                    </h4>
                    
                    <p className="text-base text-gray-600 mb-3">
                      {rec.type === 'content' && 'Contenu éducatif adapté à ton niveau'}
                      {rec.type === 'learning_path' && "Parcours d'apprentissage personnalisé"}
                      {rec.type === 'quiz' && 'Quiz pour tester tes connaissances'}
                    </p>

                    {/* Actions */}
                    <div className="flex items-center gap-4">
                      <button className="flex items-center gap-2 px-4 py-2 bg-white rounded-xl text-base font-semibold text-gray-700 hover:bg-gray-50 transition-colors shadow-sm">
                        <BookOpen size={16} />
                        Voir le contenu
                        <ArrowRight size={16} />
                      </button>
                      
                      <button className="flex items-center gap-2 px-4 py-2 bg-white/80 rounded-xl text-base font-semibold text-gray-600 hover:bg-white transition-colors shadow-sm">
                        <Target size={16} />
                        Commencer
                      </button>
                    </div>
                  </div>

                  {/* Indicateur de priorité */}
                  <div className="flex flex-col items-center gap-2">
                    <div className="w-4 h-4 bg-green-500 rounded-full animate-pulse"></div>
                    <span className="text-xs text-gray-500 font-medium">Priorité</span>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="flex flex-col items-center justify-center py-12">
              <Lightbulb className="w-14 h-14 text-yellow-200 mb-4" />
              <h4 className="text-lg font-semibold text-gray-600 mb-2">Aucune recommandation pour le moment</h4>
              <p className="text-base text-gray-400 text-center">
                Complète quelques quiz pour recevoir des recommandations personnalisées
              </p>
            </div>
          )}
        </div>

        {/* Section d'actions rapides */}
        {recommendations.length > 0 && (
          <div className="p-5 bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl border border-blue-200 shadow-md">
            <div className="flex items-center gap-4 mb-3">
              <div className="w-10 h-10 bg-blue-100 rounded-xl flex items-center justify-center">
                <Target className="text-blue-600" size={20} />
              </div>
              <div>
                <h5 className="font-bold text-blue-800 text-base">Actions rapides</h5>
                <p className="text-sm text-blue-700">Commence par ce qui t'intéresse le plus</p>
              </div>
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <button className="flex items-center gap-2 p-4 bg-white rounded-xl text-base font-semibold text-gray-700 hover:bg-blue-50 transition-colors shadow-sm">
                <BookOpen size={18} />
                Voir tout le contenu
              </button>
              <button className="flex items-center gap-2 p-4 bg-white rounded-xl text-base font-semibold text-gray-700 hover:bg-blue-50 transition-colors shadow-sm">
                <Play size={18} />
                Parcours recommandés
              </button>
            </div>
          </div>
        )}

        {/* Statistiques des recommandations */}
        <div className="grid grid-cols-3 gap-6">
          <div className="text-center p-4 bg-gray-50 rounded-xl shadow-md">
            <div className="text-xl font-bold text-gray-700">
              {recommendations.filter(r => r.type === 'content').length}
            </div>
            <div className="text-sm text-gray-500">Contenus</div>
          </div>
          <div className="text-center p-4 bg-gray-50 rounded-xl shadow-md">
            <div className="text-xl font-bold text-gray-700">
              {recommendations.filter(r => r.type === 'learning_path').length}
            </div>
            <div className="text-sm text-gray-500">Parcours</div>
          </div>
          <div className="text-center p-4 bg-gray-50 rounded-xl shadow-md">
            <div className="text-xl font-bold text-gray-700">
              {recommendations.filter(r => r.type === 'quiz').length}
            </div>
            <div className="text-sm text-gray-500">Quiz</div>
          </div>
        </div>
      </div>
    </Card>
  );
} 