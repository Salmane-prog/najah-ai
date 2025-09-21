'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { 
  User,
  Brain, 
  Target,
  TrendingUp,
  Clock,
  BookOpen,
  Award,
  Lightbulb,
  AlertCircle,
  BarChart3,
  Zap,
  CheckCircle,
  XCircle,
  RefreshCw,
  Star,
  ChevronRight,
  Calendar,
  Activity
} from 'lucide-react';

interface FrenchProfile {
  learning_style: string;
  french_level: string;
  preferred_pace: string;
  strengths: string[];
  weaknesses: string[];
  cognitive_profile: {
    final_score: number;
    difficulty_breakdown: any;
    test_id: number;
  };
  created_at: string;
  updated_at: string;
}

interface FrenchLearningProfileAdvancedProps {
  studentId: number;
  profileData?: FrenchProfile | null;
  onRefresh: () => void;
  token: string;
}

const FrenchLearningProfileAdvanced: React.FC<FrenchLearningProfileAdvancedProps> = ({
  studentId,
  profileData,
  onRefresh,
  token
}) => {
  const [profile, setProfile] = useState<FrenchProfile | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [recommendations, setRecommendations] = useState<any[]>([]);

  const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  const OPTIMIZED_API_PATH = '/api/v1/french-optimized';

  useEffect(() => {
    if (profileData) {
      setProfile(profileData);
      generateRecommendations(profileData);
    } else {
      loadProfile();
    }
  }, [profileData, studentId]);

  const loadProfile = async () => {
    try {
      setIsLoading(true);
      setError(null);

      console.log('👤 Chargement du profil avancé pour l\'étudiant:', studentId);

      const response = await fetch(`${API_BASE}${OPTIMIZED_API_PATH}/student/${studentId}/profile`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`Erreur ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      console.log('✅ Profil avancé récupéré:', data);

      if (data.success && data.profile) {
        setProfile(data.profile);
        generateRecommendations(data.profile);
      } else {
        setProfile(null);
      }

    } catch (error) {
      console.error('❌ Erreur chargement profil avancé:', error);
      setError(`Erreur lors du chargement: ${error instanceof Error ? error.message : 'Erreur inconnue'}`);
    } finally {
      setIsLoading(false);
    }
  };

  const generateRecommendations = (profileData: FrenchProfile) => {
    const recs = [];

    // Recommandations basées sur le niveau
    const level = profileData.french_level;
    if (level === 'A1' || level === 'A2') {
      recs.push({
        title: 'Renforcement des Bases',
        description: 'Concentrez-vous sur la grammaire fondamentale et le vocabulaire de base',
        priority: 'high',
        icon: BookOpen,
        color: 'blue',
        estimatedTime: '15-30 min/jour'
      });
    } else if (level === 'B1' || level === 'B2') {
      recs.push({
        title: 'Perfectionnement Intermédiaire',
        description: 'Travaillez sur les structures complexes et l\'expression écrite',
        priority: 'medium',
        icon: TrendingUp,
        color: 'green',
        estimatedTime: '20-40 min/jour'
      });
    } else {
      recs.push({
        title: 'Maintien du Niveau Avancé',
        description: 'Pratiquez régulièrement avec des textes littéraires et journalistiques',
        priority: 'low',
        icon: Star,
        color: 'purple',
        estimatedTime: '30-45 min/jour'
      });
    }

    // Recommandations basées sur le style d'apprentissage
    const style = profileData.learning_style;
    if (style === 'visual') {
      recs.push({
        title: 'Apprentissage Visuel',
        description: 'Utilisez des cartes mentales, diagrammes et supports visuels',
        priority: 'medium',
        icon: BarChart3,
        color: 'yellow',
        estimatedTime: '10-20 min/jour'
      });
    } else if (style === 'auditory') {
      recs.push({
        title: 'Apprentissage Auditif',
        description: 'Écoutez des podcasts français et pratiquez la prononciation',
        priority: 'medium',
        icon: Activity,
        color: 'orange',
        estimatedTime: '15-25 min/jour'
      });
    } else {
      recs.push({
        title: 'Apprentissage Kinesthésique',
        description: 'Pratiquez avec des exercices interactifs et des jeux de rôle',
        priority: 'medium',
        icon: Zap,
        color: 'red',
        estimatedTime: '20-30 min/jour'
      });
    }

    // Recommandations basées sur les faiblesses
    if (profileData.weaknesses && profileData.weaknesses.length > 0) {
      recs.push({
        title: 'Zones d\'Amélioration',
        description: `Travaillez spécifiquement sur: ${profileData.weaknesses.join(', ')}`,
        priority: 'high',
        icon: Target,
        color: 'red',
        estimatedTime: '15-30 min/jour'
      });
    }

    // Recommandation générale
    recs.push({
      title: 'Pratique Quotidienne',
      description: 'Maintenez une routine d\'apprentissage régulière pour des progrès constants',
      priority: 'low',
      icon: Calendar,
      color: 'gray',
      estimatedTime: '5-10 min/jour'
    });

    setRecommendations(recs);
  };

  const getLevelColor = (level: string) => {
    switch (level) {
      case 'A1': return 'bg-blue-100 text-blue-800';
      case 'A2': return 'bg-green-100 text-green-800';
      case 'B1': return 'bg-yellow-100 text-yellow-800';
      case 'B2': return 'bg-orange-100 text-orange-800';
      case 'C1': return 'bg-red-100 text-red-800';
      case 'C2': return 'bg-purple-100 text-purple-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getLevelDescription = (level: string) => {
    switch (level) {
      case 'A1': return 'Débutant - Notions de base';
      case 'A2': return 'Débutant avancé - Conversations simples';
      case 'B1': return 'Intermédiaire - Situations courantes';
      case 'B2': return 'Intermédiaire avancé - Sujets complexes';
      case 'C1': return 'Avancé - Nuances et subtilités';
      case 'C2': return 'Expert - Maîtrise quasi-native';
      default: return 'Niveau à déterminer';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'text-red-600';
      case 'medium': return 'text-yellow-600';
      case 'low': return 'text-green-600';
      default: return 'text-gray-600';
    }
  };

  const getRecommendationColor = (color: string) => {
    switch (color) {
      case 'blue': return 'bg-blue-50 border-blue-200';
      case 'green': return 'bg-green-50 border-green-200';
      case 'yellow': return 'bg-yellow-50 border-yellow-200';
      case 'orange': return 'bg-orange-50 border-orange-200';
      case 'red': return 'bg-red-50 border-red-200';
      case 'purple': return 'bg-purple-50 border-purple-200';
      default: return 'bg-gray-50 border-gray-200';
    }
  };

  if (isLoading) {
    return (
      <Card className="w-full">
        <CardContent className="flex items-center justify-center py-12">
          <div className="text-center">
            <RefreshCw className="h-12 w-12 animate-spin mx-auto mb-4 text-blue-600" />
            <p className="text-lg font-medium text-gray-900">Chargement du profil avancé...</p>
            <p className="text-gray-600">Analyse de vos données d'apprentissage</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className="w-full">
        <CardContent className="flex items-center justify-center py-12">
          <div className="text-center">
            <AlertCircle className="h-12 w-12 text-red-600 mx-auto mb-4" />
            <p className="text-lg font-medium text-red-900">Erreur de chargement</p>
            <p className="text-gray-600 mb-4">{error}</p>
            <Button onClick={() => { setError(null); loadProfile(); }} variant="outline">
              Réessayer
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!profile) {
    return (
      <Card className="w-full">
        <CardContent className="flex items-center justify-center py-12">
          <div className="text-center">
            <User className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <p className="text-lg font-medium text-gray-900">Aucun profil disponible</p>
            <p className="text-gray-600 mb-4">Passez d'abord le test d'évaluation pour générer votre profil</p>
            <Button onClick={onRefresh} variant="outline">
              <RefreshCw className="h-4 w-4 mr-2" />
              Actualiser
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      {/* En-tête du profil */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="text-2xl flex items-center gap-3">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-100 to-purple-100 rounded-lg flex items-center justify-center">
                <Brain className="h-6 w-6 text-blue-600" />
              </div>
              Profil d'Apprentissage Français IA
            </CardTitle>
            <Button onClick={onRefresh} variant="outline" size="sm">
              <RefreshCw className="h-4 w-4 mr-2" />
              Actualiser
            </Button>
          </div>
          <p className="text-gray-600">
            Profil généré le {new Date(profile.created_at).toLocaleDateString('fr-FR')}
            {profile.updated_at !== profile.created_at && 
              ` • Mis à jour le ${new Date(profile.updated_at).toLocaleDateString('fr-FR')}`
            }
          </p>
        </CardHeader>
      </Card>

      {/* Métriques principales */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <Target className="h-6 w-6 text-blue-600" />
              </div>
              <div>
                <p className="text-sm font-medium text-gray-700">Niveau Français</p>
                <div className="flex items-center gap-2 mt-1">
                  <Badge className={getLevelColor(profile.french_level)}>
                    {profile.french_level}
                  </Badge>
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  {getLevelDescription(profile.french_level)}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                <Brain className="h-6 w-6 text-green-600" />
              </div>
              <div>
                <p className="text-sm font-medium text-gray-700">Style d'Apprentissage</p>
                <p className="text-lg font-semibold text-gray-900 capitalize mt-1">
                  {profile.learning_style}
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  Mode d'apprentissage préféré
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                <Clock className="h-6 w-6 text-purple-600" />
              </div>
              <div>
                <p className="text-sm font-medium text-gray-700">Rythme Préféré</p>
                <p className="text-lg font-semibold text-gray-900 capitalize mt-1">
                  {profile.preferred_pace}
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  Vitesse d'apprentissage optimale
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Analyse détaillée */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Forces */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <CheckCircle className="h-5 w-5 text-green-600" />
              Points Forts
            </CardTitle>
          </CardHeader>
          <CardContent>
            {profile.strengths && profile.strengths.length > 0 ? (
              <div className="space-y-3">
                {profile.strengths.map((strength, index) => (
                  <div key={index} className="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
                    <Star className="h-4 w-4 text-green-600" />
                    <span className="text-green-800 font-medium">{strength}</span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 italic">Continuez votre apprentissage pour identifier vos forces</p>
            )}
          </CardContent>
        </Card>

        {/* Zones d'amélioration */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <Target className="h-5 w-5 text-orange-600" />
              Zones d'Amélioration
            </CardTitle>
          </CardHeader>
          <CardContent>
            {profile.weaknesses && profile.weaknesses.length > 0 ? (
              <div className="space-y-3">
                {profile.weaknesses.map((weakness, index) => (
                  <div key={index} className="flex items-center gap-3 p-3 bg-orange-50 rounded-lg">
                    <TrendingUp className="h-4 w-4 text-orange-600" />
                    <span className="text-orange-800 font-medium">{weakness}</span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 italic">Excellent ! Aucune faiblesse majeure identifiée</p>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Données cognitives */}
      {profile.cognitive_profile && (
        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <BarChart3 className="h-5 w-5 text-purple-600" />
              Analyse Cognitive Détaillée
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-blue-50 rounded-lg p-4">
                <p className="text-sm font-medium text-blue-700">Score Final</p>
                <p className="text-2xl font-bold text-blue-900">
                  {Math.round(profile.cognitive_profile.final_score)}%
                </p>
              </div>
              <div className="bg-green-50 rounded-lg p-4">
                <p className="text-sm font-medium text-green-700">Questions Réussies</p>
                <p className="text-2xl font-bold text-green-900">
                  {Math.round((profile.cognitive_profile.final_score / 100) * 20)}/20
                </p>
              </div>
              <div className="bg-purple-50 rounded-lg p-4">
                <p className="text-sm font-medium text-purple-700">Test ID</p>
                <p className="text-2xl font-bold text-purple-900">
                  #{profile.cognitive_profile.test_id}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Recommandations IA */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <Lightbulb className="h-5 w-5 text-yellow-600" />
            Recommandations Personnalisées IA
          </CardTitle>
          <p className="text-sm text-gray-600">
            Suggestions d'apprentissage basées sur votre profil et vos performances
          </p>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {recommendations.map((rec, index) => {
              const IconComponent = rec.icon;
              return (
                <div key={index} className={`border rounded-lg p-4 ${getRecommendationColor(rec.color)}`}>
                  <div className="flex items-start gap-3">
                    <div className="w-8 h-8 bg-white rounded-lg flex items-center justify-center flex-shrink-0">
                      <IconComponent className="h-4 w-4 text-gray-700" />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center justify-between">
                        <h4 className="font-semibold text-gray-900">{rec.title}</h4>
                        <Badge className={`text-xs ${getPriorityColor(rec.priority)}`} variant="outline">
                          {rec.priority === 'high' ? 'Priorité haute' : 
                           rec.priority === 'medium' ? 'Priorité moyenne' : 'Priorité basse'}
                        </Badge>
                      </div>
                      <p className="text-gray-700 mt-1">{rec.description}</p>
                      <div className="flex items-center gap-4 mt-2">
                        <span className="text-xs text-gray-500 flex items-center gap-1">
                          <Clock className="h-3 w-3" />
                          {rec.estimatedTime}
                        </span>
                        <ChevronRight className="h-4 w-4 text-gray-400" />
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default FrenchLearningProfileAdvanced;














