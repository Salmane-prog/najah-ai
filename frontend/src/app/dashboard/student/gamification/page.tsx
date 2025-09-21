'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Trophy, 
  Star, 
  TrendingUp, 
  Target, 
  Award, 
  Zap, 
  Crown, 
  ChartBar,
  Download,
  Share2,
  Settings
} from 'lucide-react';
import { GamificationService, Badge as BadgeType, Achievement } from '@/services/gamificationService';
import { ComparisonService, ProgressComparison } from '@/services/comparisonService';
import { RemediationService } from '@/services/remediationService';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  RadialLinearScale,
  Filler,
} from 'chart.js';
import { Line, Radar } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  RadialLinearScale,
  Filler
);

export default function GamificationPage() {
  const { user, token } = useAuth();
  const [badges, setBadges] = useState<BadgeType[]>([]);
  const [badgeProgress, setBadgeProgress] = useState<any[]>([]);
  const [achievements, setAchievements] = useState<Achievement[]>([]);
  const [gamificationLevel, setGamificationLevel] = useState<any>(null);
  const [comparisons, setComparisons] = useState<ProgressComparison[]>([]);
  const [remediationResults, setRemediationResults] = useState<any[]>([]);
  const [progress, setProgress] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    if (user && token) {
      loadGamificationData();
    }
  }, [user, token]);

  const loadGamificationData = async () => {
    try {
      setLoading(true);
      
      // Charger les données de remédiation
      const [results, progressData] = await Promise.all([
        RemediationService.getRemediationResults(token, user!.id),
        RemediationService.getRemediationProgress(token, user!.id)
      ]);
      
      setRemediationResults(results);
      setProgress(progressData);

      // Charger les badges
      const [studentBadges, availableBadges] = await Promise.all([
        GamificationService.getStudentBadges(token, user!.id),
        GamificationService.getAvailableBadges(token, user!.id)
      ]);
      
      setBadges(studentBadges);
      
      // Calculer le progrès des badges
      const calculatedProgress = GamificationService.calculateBadgeProgress(
        studentBadges,
        results,
        progressData
      );
      setBadgeProgress(calculatedProgress);

      // Générer les achievements
      const generatedAchievements = GamificationService.generateAchievements(results, progressData);
      setAchievements(generatedAchievements);

      // Calculer le niveau de gamification
      const level = GamificationService.calculateGamificationLevel(
        studentBadges,
        generatedAchievements,
        results.length
      );
      setGamificationLevel(level);

      // Charger les comparaisons
      const comparisonData = await ComparisonService.getProgressComparison(token, user!.id);
      setComparisons(comparisonData);

    } catch (error) {
      console.error('❌ Erreur chargement données gamification:', error);
    } finally {
      setLoading(false);
    }
  };

  const exportData = () => {
    if (comparisons.length === 0) return;
    
    const csvContent = ComparisonService.exportComparisonToCSV(comparisons);
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `progression_remediation_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
  };

  const shareProgress = () => {
    if (navigator.share) {
      navigator.share({
        title: 'Mon Progrès de Remédiation',
        text: `J'ai obtenu ${badges.length} badges et ${achievements.length} achievements !`,
        url: window.location.href
      });
    } else {
      // Fallback pour les navigateurs qui ne supportent pas l'API Web Share
      navigator.clipboard.writeText(
        `Mon Progrès de Remédiation: ${badges.length} badges, ${achievements.length} achievements !`
      );
      alert('Progrès copié dans le presse-papiers !');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-7xl mx-auto">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p>Chargement de votre profil de gamification...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 flex items-center space-x-3">
                <Trophy className="w-8 h-8 text-yellow-600" />
                <span>Gamification & Récompenses</span>
              </h1>
              <p className="text-gray-600 mt-2">
                Suivez vos progrès, débloquez des badges et atteignez de nouveaux niveaux !
              </p>
            </div>
            <div className="flex space-x-3">
              <Button onClick={exportData} variant="outline">
                <Download className="w-4 h-4 mr-2" />
                Exporter
              </Button>
              <Button onClick={shareProgress} variant="outline">
                <Share2 className="w-4 h-4 mr-2" />
                Partager
              </Button>
              <Button variant="outline">
                <Settings className="w-4 h-4 mr-2" />
                Paramètres
              </Button>
            </div>
          </div>
        </div>

        {/* Niveau de Gamification */}
        {gamificationLevel && (
          <Card className="mb-8 bg-gradient-to-r from-blue-500 to-purple-600 text-white">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-2xl font-bold mb-2">
                    Niveau {gamificationLevel.level} - {gamificationLevel.title}
                  </h2>
                  <p className="text-blue-100 mb-4">
                    {gamificationLevel.totalPoints} points totaux
                  </p>
                  <div className="w-64">
                    <Progress 
                      value={gamificationLevel.progress} 
                      className="h-3 bg-blue-400"
                    />
                    <p className="text-sm text-blue-100 mt-2">
                      {gamificationLevel.progress}/100 vers le niveau {gamificationLevel.nextLevel}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-6xl font-bold text-yellow-300">
                    {gamificationLevel.level}
                  </div>
                  <p className="text-blue-100">Niveau actuel</p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="overview">Vue d'ensemble</TabsTrigger>
            <TabsTrigger value="badges">Badges</TabsTrigger>
            <TabsTrigger value="achievements">Achievements</TabsTrigger>
            <TabsTrigger value="analytics">Analytics</TabsTrigger>
          </TabsList>

          {/* Vue d'ensemble */}
          <TabsContent value="overview" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Statistiques rapides */}
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-600">
                    Badges Obtenus
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{badges.length}</div>
                  <p className="text-xs text-gray-500 mt-1">
                    sur {badgeProgress.length} disponibles
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-600">
                    Achievements
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{achievements.length}</div>
                  <p className="text-xs text-gray-500 mt-1">
                    débloqués
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-600">
                    Exercices Complétés
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{remediationResults.length}</div>
                  <p className="text-xs text-gray-500 mt-1">
                    en remédiation
                  </p>
                </CardContent>
              </Card>
            </div>

            {/* Progrès récent */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <TrendingUp className="w-5 h-5 text-green-600" />
                  <span>Progrès Récent</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                {comparisons.length > 0 ? (
                  <div className="space-y-4">
                    {comparisons.slice(0, 3).map((comparison, index) => (
                      <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div>
                          <h4 className="font-medium">{comparison.topic}</h4>
                          <p className="text-sm text-gray-600">
                            Niveau {comparison.before.current_level} → {comparison.after.current_level}
                          </p>
                        </div>
                        <Badge variant={comparison.improvement_percentage > 0 ? "default" : "secondary"}>
                          {comparison.improvement_percentage > 0 ? '+' : ''}
                          {comparison.improvement_percentage.toFixed(1)}%
                        </Badge>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500 text-center py-8">
                    Aucun progrès récent à afficher
                  </p>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Badges */}
          <TabsContent value="badges" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Award className="w-5 h-5 text-yellow-600" />
                  <span>Mes Badges</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {badgeProgress.map((badge, index) => (
                    <div
                      key={index}
                      className={`p-4 rounded-lg border-2 transition-all ${
                        badge.is_earned
                          ? 'border-yellow-500 bg-yellow-50'
                          : 'border-gray-200 bg-gray-50'
                      }`}
                    >
                      <div className="text-center">
                        <div className="text-4xl mb-2">{badge.icon}</div>
                        <h3 className="font-semibold mb-1">{badge.name}</h3>
                        <p className="text-sm text-gray-600 mb-3">{badge.description}</p>
                        
                        {badge.is_earned ? (
                          <Badge variant="default" className="bg-yellow-600">
                            <Star className="w-3 h-3 mr-1" />
                            Obtenu
                          </Badge>
                        ) : (
                          <div className="space-y-2">
                            <div className="text-xs text-gray-500">{badge.condition}</div>
                            <Progress 
                              value={(badge.progress / badge.max_progress) * 100} 
                              className="h-2"
                            />
                            <div className="text-xs text-gray-500">
                              {badge.progress}/{badge.max_progress}
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Achievements */}
          <TabsContent value="achievements" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Target className="w-5 h-5 text-purple-600" />
                  <span>Mes Achievements</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {achievements.map((achievement, index) => (
                    <div
                      key={index}
                      className={`p-4 rounded-lg border-2 transition-all ${
                        achievement.is_unlocked
                          ? 'border-purple-500 bg-purple-50'
                          : 'border-gray-200 bg-gray-50'
                      }`}
                    >
                      <div className="text-center">
                        <div className="text-4xl mb-2">{achievement.icon}</div>
                        <h3 className="font-semibold mb-1">{achievement.title}</h3>
                        <p className="text-sm text-gray-600 mb-3">{achievement.description}</p>
                        
                        <div className="space-y-2">
                          <div className="flex items-center justify-center space-x-2">
                            <Zap className="w-4 h-4 text-yellow-600" />
                            <span className="text-sm font-medium">
                              {achievement.reward_points} points
                            </span>
                          </div>
                          
                          <Progress 
                            value={(achievement.progress / achievement.max_progress) * 100} 
                            className="h-2"
                          />
                          <div className="text-xs text-gray-500">
                            {achievement.progress}/{achievement.max_progress}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Analytics */}
          <TabsContent value="analytics" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Graphique de comparaison avant/après */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <ChartBar className="w-5 h-5 text-blue-600" />
                    <span>Comparaison Avant/Après</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  {comparisons.length > 0 ? (
                    <div className="h-64">
                      <Line
                        data={{
                          labels: comparisons.map(c => c.topic),
                          datasets: [
                            {
                              label: 'Avant',
                              data: comparisons.map(c => c.before.current_level),
                              borderColor: '#EF4444',
                              backgroundColor: '#EF444420',
                              tension: 0.1
                            },
                            {
                              label: 'Après',
                              data: comparisons.map(c => c.after.current_level),
                              borderColor: '#10B981',
                              backgroundColor: '#10B98120',
                              tension: 0.1
                            }
                          ]
                        }}
                        options={{
                          responsive: true,
                          maintainAspectRatio: false,
                          plugins: {
                            legend: {
                              position: 'top' as const,
                            },
                            title: {
                              display: true,
                              text: 'Évolution des Niveaux par Domaine'
                            }
                          }
                        }}
                      />
                    </div>
                  ) : (
                    <p className="text-gray-500 text-center py-8">
                      Aucune donnée de comparaison disponible
                    </p>
                  )}
                </CardContent>
              </Card>

              {/* Graphique radar des améliorations */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Crown className="w-5 h-5 text-purple-600" />
                    <span>Taux d'Amélioration</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  {comparisons.length > 0 ? (
                    <div className="h-64">
                      <Radar
                        data={{
                          labels: comparisons.map(c => c.topic),
                          datasets: [
                            {
                              label: 'Taux d\'Amélioration (%)',
                              data: comparisons.map(c => c.improvement_percentage),
                              borderColor: '#8B5CF6',
                              backgroundColor: '#8B5CF620',
                              tension: 0.1
                            }
                          ]
                        }}
                        options={{
                          responsive: true,
                          maintainAspectRatio: false,
                          plugins: {
                            legend: {
                              position: 'top' as const,
                            },
                            title: {
                              display: true,
                              text: 'Performance par Domaine'
                            }
                          },
                          scales: {
                            r: {
                              beginAtZero: true,
                              max: Math.max(...comparisons.map(c => c.improvement_percentage), 20)
                            }
                          }
                        }}
                      />
                    </div>
                  ) : (
                    <p className="text-gray-500 text-center py-8">
                      Aucune donnée d'amélioration disponible
                    </p>
                  )}
                </CardContent>
              </Card>
            </div>

            {/* Statistiques détaillées */}
            <Card>
              <CardHeader>
                <CardTitle>Statistiques Détaillées</CardTitle>
              </CardHeader>
              <CardContent>
                {comparisons.length > 0 ? (
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div className="text-center p-4 bg-blue-50 rounded-lg">
                      <div className="text-2xl font-bold text-blue-600">
                        {comparisons.reduce((sum, c) => sum + c.improvement_percentage, 0).toFixed(1)}%
                      </div>
                      <p className="text-sm text-blue-600">Amélioration Totale</p>
                    </div>
                    
                    <div className="text-center p-4 bg-green-50 rounded-lg">
                      <div className="text-2xl font-bold text-green-600">
                        {(comparisons.reduce((sum, c) => sum + c.improvement_percentage, 0) / comparisons.length).toFixed(1)}%
                      </div>
                      <p className="text-sm text-green-600">Amélioration Moyenne</p>
                    </div>
                    
                    <div className="text-center p-4 bg-yellow-50 rounded-lg">
                      <div className="text-2xl font-bold text-yellow-600">
                        {comparisons.filter(c => c.improvement_percentage > 0).length}
                      </div>
                      <p className="text-sm text-yellow-600">Domaines Améliorés</p>
                    </div>
                    
                    <div className="text-center p-4 bg-purple-50 rounded-lg">
                      <div className="text-2xl font-bold text-purple-600">
                        {comparisons.length}
                      </div>
                      <p className="text-sm text-purple-600">Domaines Suivis</p>
                    </div>
                  </div>
                ) : (
                  <p className="text-gray-500 text-center py-8">
                    Aucune statistique disponible
                  </p>
                )}
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}











