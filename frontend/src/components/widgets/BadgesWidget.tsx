'use client';

import React, { useState, useEffect } from 'react';
import { Card } from '../Card';
import { Award, Trophy, Star, Target, RefreshCw } from 'lucide-react';
import { Dialog } from '@headlessui/react';
import { useAutoBadges } from '../../hooks/useAutoBadges';

interface Badge {
  id: number;
  user_id: number;
  badge_id: number;
  progression: number;
  awarded_at: string;
  badge?: {
    name: string;
    description: string;
    image_url?: string;
  };
}

interface BadgesWidgetProps {
  badges: Badge[];
  className?: string;
}

export default function BadgesWidget({ badges, className = '' }: BadgesWidgetProps) {
  // Hook pour les badges automatiques
  const { 
    hasNewBadges, 
    newBadgesCount, 
    currentLevel, 
    totalPoints, 
    totalTests,
    forceCheck: forceCheckBadges,
    isChecking 
  } = useAutoBadges();

  // État local pour les badges combinés
  const [combinedBadges, setCombinedBadges] = useState<Badge[]>([]);
  const [isRefreshing, setIsRefreshing] = useState(false);

  // Combiner les badges existants avec les nouveaux badges automatiques
  useEffect(() => {
    // Filtrer les badges valides
    const validBadges = badges.filter(b => b && typeof b.progression === 'number' && !isNaN(b.progression));
    
    // Si on a des badges automatiques, les ajouter
    if (hasNewBadges && newBadgesCount > 0) {
      // Créer des badges virtuels pour les nouveaux badges automatiques
      const autoBadges: Badge[] = Array.from({ length: newBadgesCount }, (_, index) => ({
        id: 1000 + index, // ID virtuel
        user_id: 0,
        badge_id: 0,
        progression: 1.0, // Badge obtenu
        awarded_at: new Date().toISOString(),
        badge: {
          name: `Nouveau Badge ${index + 1}`,
          description: 'Badge attribué automatiquement !',
          image_url: '/badges/auto-badge.png'
        }
      }));
      
      setCombinedBadges([...validBadges, ...autoBadges]);
    } else {
      setCombinedBadges(validBadges);
    }
  }, [badges, hasNewBadges, newBadgesCount]);

  // Amélioration du calcul de la progression avec gestion des valeurs null/undefined
  const validBadges = combinedBadges.filter(b => b && typeof b.progression === 'number' && !isNaN(b.progression));
  const unlockedBadges = validBadges.filter(b => b.progression >= 1);
  const inProgressBadges = validBadges.filter(b => b.progression < 1 && b.progression > 0);
  
  // Calcul de la progression globale basé sur les badges valides
  const totalProgress = validBadges.length > 0
    ? validBadges.reduce((acc, b) => acc + (Math.min(b.progression, 1) / validBadges.length) * 100, 0)
    : 0;

  // Fonction pour forcer la vérification des badges
  const handleRefreshBadges = async () => {
    setIsRefreshing(true);
    try {
      await forceCheckBadges();
    } finally {
      setIsRefreshing(false);
    }
  };

  const [selectedBadge, setSelectedBadge] = React.useState<Badge | null>(null);
  const [isModalOpen, setIsModalOpen] = React.useState(false);

  const handleBadgeClick = (badge: Badge) => {
    setSelectedBadge(badge);
    setIsModalOpen(true);
  };
  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedBadge(null);
  };

  const getBadgeIcon = (badgeName: string) => {
    const name = badgeName.toLowerCase();
    if (name.includes('trophy') || name.includes('champion')) return <Trophy className="text-yellow-600" size={20} />;
    if (name.includes('star') || name.includes('excellent')) return <Star className="text-yellow-500" size={20} />;
    if (name.includes('target') || name.includes('goal')) return <Target className="text-blue-600" size={20} />;
    return <Award className="text-purple-600" size={20} />;
  };

  const getProgressColor = (progression: number) => {
    if (progression >= 1) return 'bg-green-500';
    if (progression >= 0.7) return 'bg-blue-500';
    if (progression >= 0.4) return 'bg-yellow-500';
    return 'bg-gray-300';
  };

  return (
    <Card title="Badges & Réalisations" icon={<Award />} className={`p-8 shadow-lg rounded-2xl ${className}`}>
      <div className="space-y-8">
        {/* En-tête avec bouton de rafraîchissement */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Award className="text-purple-600" size={20} />
            <span className="text-sm text-purple-600 font-medium">
              Système automatique activé
            </span>
          </div>
          <button
            onClick={handleRefreshBadges}
            disabled={isRefreshing || isChecking}
            className="flex items-center gap-2 px-3 py-2 bg-purple-100 hover:bg-purple-200 text-purple-700 rounded-lg transition-colors disabled:opacity-50"
          >
            <RefreshCw className={`${isRefreshing || isChecking ? 'animate-spin' : ''}`} size={16} />
            <span className="text-sm font-medium">
              {isRefreshing || isChecking ? 'Vérification...' : 'Vérifier badges'}
            </span>
          </button>
        </div>

        {/* Statistiques des badges automatiques */}
        <div className="grid grid-cols-3 gap-6">
          <div className="text-center p-6 bg-yellow-50 rounded-xl shadow-md">
            <div className="text-3xl font-extrabold text-yellow-600 drop-shadow-sm">
              {currentLevel > 0 ? 
                // Calculer le nombre de badges obtenus basé sur les critères
                (currentLevel >= 1 ? 1 : 0) + 
                (currentLevel >= 5 ? 1 : 0) + 
                (currentLevel >= 10 ? 1 : 0) + 
                (currentLevel >= 15 ? 1 : 0) + 
                (currentLevel >= 20 ? 1 : 0) +
                (totalTests >= 1 ? 1 : 0) + 
                (totalTests >= 10 ? 1 : 0) + 
                (totalTests >= 50 ? 1 : 0) + 
                (totalTests >= 100 ? 1 : 0) + 
                (totalTests >= 500 ? 1 : 0) +
                (totalPoints >= 100 ? 1 : 0) + 
                (totalPoints >= 1000 ? 1 : 0) + 
                (totalPoints >= 5000 ? 1 : 0) + 
                (totalPoints >= 10000 ? 1 : 0) + 
                (totalPoints >= 50000 ? 1 : 0) +
                (totalTests >= 5 ? 1 : 0) + // Quiz Master
                (totalTests >= 3 ? 1 : 0)   // Test Adaptatif Expert
                : 0
              }
            </div>
            <div className="text-base font-medium text-gray-700">Badges obtenus</div>
            {newBadgesCount > 0 && (
              <div className="text-xs text-green-600 font-medium mt-1">
                +{newBadgesCount} nouveau(x)
              </div>
            )}
          </div>
          <div className="text-center p-6 bg-blue-50 rounded-xl shadow-md">
            <div className="text-3xl font-extrabold text-blue-600 drop-shadow-sm">
              {currentLevel > 0 ? 
                // Calculer le nombre de badges en cours
                Math.max(0, 20 - currentLevel) + // Niveaux restants
                Math.max(0, 500 - totalTests) + // Tests restants (approximatif)
                Math.max(0, 100000 - totalPoints) // Points restants (approximatif)
                : 0
              }
            </div>
            <div className="text-base font-medium text-gray-700">En cours</div>
          </div>
          <div className="text-center p-6 bg-purple-50 rounded-xl shadow-md">
            <div className="text-3xl font-extrabold text-purple-700 drop-shadow-sm">
              {currentLevel > 0 ? 
                // Calculer la progression globale
                Math.min(100, Math.round((currentLevel / 20) * 100))
                : 0
              }%
            </div>
            <div className="text-base font-medium text-gray-700">Progression</div>
          </div>
        </div>

        {/* Informations sur le système automatique */}
        {currentLevel > 0 && (
          <div className="bg-gradient-to-r from-green-50 to-blue-50 p-4 rounded-xl border border-green-200">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-sm font-medium text-green-700">
                  Système de badges automatiques actif
                </span>
              </div>
              <div className="text-right">
                <div className="text-lg font-bold text-green-700">Niveau {currentLevel}</div>
                <div className="text-xs text-green-600">{totalPoints} points • {totalTests} tests</div>
              </div>
            </div>
          </div>
        )}

        {/* Barre de progression globale */}
        <div className="space-y-2">
          <div className="flex justify-between text-base font-semibold">
            <span className="text-gray-700">Progression globale</span>
            <span className="font-bold text-purple-700">
              {currentLevel > 0 ? Math.min(100, Math.round((currentLevel / 20) * 100)) : 0}%
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-4">
            <div 
              className="bg-gradient-to-r from-yellow-400 to-orange-500 h-4 rounded-full transition-all duration-1000 ease-out shadow-md"
              style={{ 
                width: currentLevel > 0 ? `${Math.min(100, Math.round((currentLevel / 20) * 100))}%` : '0%' 
              }}
            ></div>
          </div>
        </div>

        {/* Liste des badges automatiques */}
        <div className="space-y-4 max-h-96 overflow-y-auto">
          <h4 className="font-bold text-lg text-gray-800 mb-2">Mes badges</h4>
          
          {/* Affichage des badges automatiques */}
          {currentLevel > 0 && totalTests > 0 ? (
            <div className="space-y-6">
              {/* Badges de niveau */}
              <div className="space-y-3">
                <h6 className="text-sm font-semibold text-gray-600 uppercase tracking-wide flex items-center gap-2">
                  <Trophy className="w-4 h-4" /> Badges de Niveau
                </h6>
                <div className="grid grid-cols-1 gap-3">
                  {[1, 5, 10, 15, 20].map((level) => (
                    <div 
                      key={`level-${level}`}
                      className={`p-4 rounded-lg border-2 transition-all duration-300 ${
                        currentLevel >= level 
                          ? 'bg-gradient-to-r from-green-50 to-blue-50 border-green-200 shadow-md' 
                          : 'bg-gray-50 border-gray-200 opacity-50'
                      }`}
                    >
                      <div className="flex items-center gap-4">
                        <div className={`w-12 h-12 rounded-full flex items-center justify-center ${
                          currentLevel >= level 
                            ? 'bg-gradient-to-br from-green-400 to-blue-500 text-white' 
                            : 'bg-gray-200 text-gray-400'
                        }`}>
                          {currentLevel >= level ? (
                            <Trophy size={24} />
                          ) : (
                            <Award size={24} />
                          )}
                        </div>
                        <div className="flex-1">
                          <h6 className={`font-bold ${
                            currentLevel >= level ? 'text-green-800' : 'text-gray-600'
                          }`}>
                            {level === 1 && 'Débutant'}
                            {level === 5 && 'Apprenti'}
                            {level === 10 && 'Élève Confirmé'}
                            {level === 15 && 'Expert'}
                            {level === 20 && 'Maître'}
                          </h6>
                          <p className="text-sm text-gray-600">
                            Niveau {level} atteint
                          </p>
                        </div>
                        {currentLevel >= level && (
                          <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full font-semibold">
                            ✅ Obtenu
                          </span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Badges de tests */}
              <div className="space-y-3">
                <h6 className="text-sm font-semibold text-gray-600 uppercase tracking-wide flex items-center gap-2">
                  <Target className="w-4 h-4" /> Badges de Tests
                </h6>
                <div className="grid grid-cols-1 gap-3">
                  {[1, 10, 50, 100, 500].map((count) => (
                    <div 
                      key={`test-${count}`}
                      className={`p-4 rounded-lg border-2 transition-all duration-300 ${
                        totalTests >= count 
                          ? 'bg-gradient-to-r from-blue-50 to-purple-50 border-blue-200 shadow-md' 
                          : 'bg-gray-50 border-gray-200 opacity-50'
                      }`}
                    >
                      <div className="flex items-center gap-4">
                        <div className={`w-12 h-12 rounded-full flex items-center justify-center ${
                          totalTests >= count 
                            ? 'bg-gradient-to-br from-blue-400 to-purple-500 text-white' 
                            : 'bg-gray-200 text-gray-400'
                        }`}>
                          {totalTests >= count ? (
                            <Star size={24} />
                          ) : (
                            <Target size={24} />
                          )}
                        </div>
                        <div className="flex-1">
                          <h6 className={`font-bold ${
                            totalTests >= count ? 'text-blue-800' : 'text-gray-600'
                          }`}>
                            {count === 1 && 'Premier Pas'}
                            {count === 10 && 'Débutant Actif'}
                            {count === 50 && 'Étudiant Régulier'}
                            {count === 100 && 'Étudiant Assidu'}
                            {count === 500 && 'Étudiant Expert'}
                          </h6>
                          <p className="text-sm text-gray-600">
                            {count} test{count > 1 ? 's' : ''} complété{count > 1 ? 's' : ''}
                          </p>
                        </div>
                        {totalTests >= count && (
                          <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full font-semibold">
                            ✅ Obtenu
                          </span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Badges de points */}
              <div className="space-y-3">
                <h6 className="text-sm font-semibold text-gray-600 uppercase tracking-wide flex items-center gap-2">
                  <Star className="w-4 h-4" /> Badges de Points
                </h6>
                <div className="grid grid-cols-1 gap-3">
                  {[100, 1000, 5000, 10000, 50000].map((points) => (
                    <div 
                      key={`points-${points}`}
                      className={`p-4 rounded-lg border-2 transition-all duration-300 ${
                        totalPoints >= points 
                          ? 'bg-gradient-to-r from-yellow-50 to-orange-50 border-yellow-200 shadow-md' 
                          : 'bg-gray-50 border-gray-200 opacity-50'
                      }`}
                    >
                      <div className="flex items-center gap-4">
                        <div className={`w-12 h-12 rounded-full flex items-center justify-center ${
                          totalPoints >= points 
                            ? 'bg-gradient-to-br from-yellow-400 to-orange-500 text-white' 
                            : 'bg-gray-200 text-gray-400'
                        }`}>
                          {totalPoints >= points ? (
                            <Star size={24} />
                          ) : (
                            <Target size={24} />
                          )}
                        </div>
                        <div className="flex-1">
                          <h6 className={`font-bold ${
                            totalPoints >= points ? 'text-yellow-800' : 'text-gray-600'
                          }`}>
                            {points === 100 && 'Premiers Points'}
                            {points === 1000 && 'Élève Motivé'}
                            {points === 5000 && 'Élève Déterminé'}
                            {points === 10000 && 'Élève Exceptionnel'}
                            {points === 50000 && 'Légende'}
                          </h6>
                          <p className="text-sm text-gray-600">
                            {points.toLocaleString()} points accumulés
                          </p>
                        </div>
                        {totalPoints >= points && (
                          <span className="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs rounded-full font-semibold">
                            ✅ Obtenu
                          </span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center py-12">
              <Trophy className="w-16 h-16 text-yellow-200 mb-4" />
              <p className="text-lg font-semibold text-gray-600 mb-2">Aucun badge disponible</p>
              <p className="text-base text-gray-400">Participe à des quiz pour débloquer tes premiers badges !</p>
            </div>
          )}
        </div>

        {/* Message d'encouragement */}
        {inProgressBadges.length > 0 && (
          <div className="p-5 bg-blue-50 rounded-xl border border-blue-200 shadow-md">
            <div className="flex items-center gap-3">
              <Target className="text-blue-600" size={20} />
              <p className="text-base text-blue-800 font-semibold">
                Continue tes efforts ! Tu as {inProgressBadges.length} badge{inProgressBadges.length > 1 ? 's' : ''} en cours d'obtention.
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Modale de détail du badge */}
      <Dialog open={isModalOpen} onClose={closeModal} className="fixed z-50 inset-0 overflow-y-auto">
        <div className="flex items-center justify-center min-h-screen px-4">
          <Dialog.Overlay className="fixed inset-0 bg-black bg-opacity-30" />
          <div className="relative bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full z-10">
            {selectedBadge && (
              <>
                <div className="flex flex-col items-center mb-4">
                  <Award className="w-16 h-16 text-yellow-400 mb-2" />
                  <h2 className="text-2xl font-bold text-gray-800 mb-1">{selectedBadge.badge?.name || 'Badge'}</h2>
                  <p className="text-gray-600 text-center mb-2">{selectedBadge.badge?.description || 'Description du badge'}</p>
                  {selectedBadge.awarded_at && (
                    <p className="text-sm text-green-600 mb-2">Obtenu le {new Date(selectedBadge.awarded_at).toLocaleDateString('fr-FR')}</p>
                  )}
                  {selectedBadge.badge?.image_url && (
                    <img src={selectedBadge.badge.image_url} alt="Badge" className="w-20 h-20 object-contain rounded-xl border mb-2" />
                  )}
                </div>
                <div className="flex justify-end">
                  <button onClick={closeModal} className="px-4 py-2 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 transition">Fermer</button>
                </div>
              </>
            )}
          </div>
        </div>
      </Dialog>
    </Card>
  );
} 