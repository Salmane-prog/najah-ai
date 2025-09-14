'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { 
  User, 
  Brain, 
  Target, 
  TrendingUp, 
  BookOpen, 
  Lightbulb,
  CheckCircle,
  XCircle,
  Loader2,
  RefreshCw,
  Award,
  BarChart3,
  Zap,
  Clock,
  Star
} from 'lucide-react';

interface ProfileData {
  id: number;
  student_id: number;
  learning_style: string;
  french_level: string;
  preferred_pace: string;
  strengths: string;
  weaknesses: string;
  cognitive_profile: string;
  recommendations: string;
  created_at: string;
  updated_at: string;
}

interface FrenchLearningProfileProps {
  studentId: number;
  profileData?: ProfileData | null;
  onRefresh?: () => void;
  token: string;
}

const FrenchLearningProfile: React.FC<FrenchLearningProfileProps> = ({
  studentId,
  profileData,
  onRefresh,
  token
}) => {
  const [profile, setProfile] = useState<ProfileData | null>(profileData || null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  useEffect(() => {
    if (profileData) {
      setProfile(profileData);
    } else {
      loadProfileData();
    }
  }, [profileData, studentId]);

  const loadProfileData = async () => {
    try {
      setIsLoading(true);
      setError(null);

      const response = await fetch(`${API_BASE}/api/v1/french/initial-assessment/student/${studentId}/profile`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`Erreur ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      console.log('✅ Profil chargé:', data);
      setProfile(data);

    } catch (error) {
      console.error('❌ Erreur chargement profil:', error);
      setError(`Erreur lors du chargement: ${error instanceof Error ? error.message : 'Erreur inconnue'}`);
    } finally {
      setIsLoading(false);
    }
  };

  const getLevelColor = (level: string | undefined) => {
    if (!level) return 'bg-gray-100 text-gray-800';
    switch (level.toUpperCase()) {
      case 'A0': return 'bg-gray-100 text-gray-800';
      case 'A1': return 'bg-green-100 text-green-800';
      case 'A2': return 'bg-blue-100 text-blue-800';
      case 'B1': return 'bg-yellow-100 text-yellow-800';
      case 'B2': return 'bg-orange-100 text-orange-800';
      case 'C1': return 'bg-purple-100 text-purple-800';
      case 'C2': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getLevelLabel = (level: string | undefined) => {
    if (!level) return 'Niveau non défini';
    switch (level.toUpperCase()) {
      case 'A0': return 'Débutant Absolu';
      case 'A1': return 'Débutant';
      case 'A2': return 'Débutant Avancé';
      case 'B1': return 'Intermédiaire';
      case 'B2': return 'Intermédiaire Avancé';
      case 'C1': return 'Avancé';
      case 'C2': return 'Expert';
      default: return level;
    }
  };

  const getLearningStyleIcon = (style: string | undefined) => {
    if (!style) return <Brain className="h-5 w-5 text-gray-600" />;
    switch (style.toLowerCase()) {
      case 'visual': return <BarChart3 className="h-5 w-5 text-blue-600" />;
      case 'auditory': return <Zap className="h-5 w-5 text-green-600" />;
      case 'kinesthetic': return <Target className="h-5 w-5 text-purple-600" />;
      default: return <Brain className="h-5 w-5 text-gray-600" />;
    }
  };

  const getLearningStyleLabel = (style: string | undefined) => {
    if (!style) return 'Non défini';
    switch (style.toLowerCase()) {
      case 'visual': return 'Visuel';
      case 'auditory': return 'Auditif';
      case 'kinesthetic': return 'Kinesthésique';
      default: return style;
    }
  };

  const getPaceLabel = (pace: string | undefined) => {
    if (!pace) return 'Non défini';
    switch (pace.toLowerCase()) {
      case 'lent': return 'Lent';
      case 'moyen': return 'Moyen';
      case 'rapide': return 'Rapide';
      default: return pace;
    }
  };

  const parseJsonField = (field: string) => {
    try {
      return JSON.parse(field);
    } catch {
      return [];
    }
  };

  // État de chargement
  if (isLoading) {
    return (
      <Card className="w-full">
        <CardContent className="flex items-center justify-center py-12">
          <div className="text-center">
            <Loader2 className="h-12 w-12 animate-spin mx-auto mb-4 text-blue-600" />
            <p className="text-lg font-medium text-gray-900">Chargement du profil...</p>
            <p className="text-gray-600">Analyse de vos performances en cours</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  // Pas de profil disponible
  if (!profile) {
    return (
      <Card className="w-full">
        <CardContent className="text-center py-12">
          <div className="mx-auto w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
            <User className="h-8 w-8 text-gray-600" />
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">Aucun Profil Disponible</h3>
          <p className="text-gray-600 mb-6">
            Vous devez d'abord compléter l'évaluation française pour générer votre profil personnalisé.
          </p>
          <Button onClick={loadProfileData} variant="outline">
            <RefreshCw className="h-4 w-4 mr-2" />
            Actualiser
          </Button>
        </CardContent>
      </Card>
    );
  }

  // Profil disponible
  const strengths = parseJsonField(profile.strengths);
  const weaknesses = parseJsonField(profile.weaknesses);
  const cognitiveProfile = parseJsonField(profile.cognitive_profile);
  const recommendations = parseJsonField(profile.recommendations);

  return (
    <div className="space-y-6">
      {/* En-tête du profil */}
      <Card>
        <CardHeader className="text-center">
          <div className="mx-auto w-16 h-16 bg-gradient-to-br from-blue-100 to-purple-100 rounded-full flex items-center justify-center mb-4">
            <Award className="h-8 w-8 text-blue-600" />
          </div>
          <CardTitle className="text-2xl text-gray-900">Profil d'Apprentissage Français</CardTitle>
          <p className="text-gray-600">Généré par intelligence artificielle basé sur vos performances</p>
        </CardHeader>
      </Card>

      {/* Informations principales */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Niveau de français */}
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center gap-2 text-lg">
              <Target className="h-5 w-5 text-blue-600" />
              Niveau Actuel
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-center">
              <Badge className={`text-lg px-4 py-2 ${getLevelColor(profile.french_level)}`}>
                {profile.french_level || 'N/A'}
              </Badge>
              <p className="text-sm text-gray-600 mt-2">
                {getLevelLabel(profile.french_level)}
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Style d'apprentissage */}
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center gap-2 text-lg">
              <Brain className="h-5 w-5 text-green-600" />
              Style d'Apprentissage
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-center">
              <div className="flex justify-center mb-2">
                {getLearningStyleIcon(profile.learning_style)}
              </div>
              <p className="font-medium text-gray-900">
                {getLearningStyleLabel(profile.learning_style)}
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Rythme préféré */}
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center gap-2 text-lg">
              <Clock className="h-5 w-5 text-purple-600" />
              Rythme Préféré
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-center">
              <p className="font-medium text-gray-900">
                {getPaceLabel(profile.preferred_pace)}
              </p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Forces et faiblesses */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Forces */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg">
              <CheckCircle className="h-5 w-5 text-green-600" />
              Vos Forces
            </CardTitle>
          </CardHeader>
          <CardContent>
            {strengths.length > 0 ? (
              <div className="space-y-3">
                {strengths.map((strength: any, index: number) => (
                  <div key={index} className="flex items-start gap-3">
                    <div className="w-2 h-2 bg-green-500 rounded-full mt-2 flex-shrink-0"></div>
                    <div>
                      <p className="font-medium text-gray-900">{strength.title || strength}</p>
                      {strength.description && (
                        <p className="text-sm text-gray-600">{strength.description}</p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 text-center py-4">Aucune force identifiée pour le moment</p>
            )}
          </CardContent>
        </Card>

        {/* Faiblesses */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg">
              <XCircle className="h-5 w-5 text-red-600" />
              Points d'Amélioration
            </CardTitle>
          </CardHeader>
          <CardContent>
            {weaknesses.length > 0 ? (
              <div className="space-y-3">
                {weaknesses.map((weakness: any, index: number) => (
                  <div key={index} className="flex items-start gap-3">
                    <div className="w-2 h-2 bg-red-500 rounded-full mt-2 flex-shrink-0"></div>
                    <div>
                      <p className="font-medium text-gray-900">{weakness.title || weakness}</p>
                      {weakness.description && (
                        <p className="text-sm text-gray-600">{weakness.description}</p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 text-center py-4">Aucun point d'amélioration identifié</p>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Profil cognitif détaillé */}
      {cognitiveProfile && Object.keys(cognitiveProfile).length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg">
              <Brain className="h-5 w-5 text-purple-600" />
              Profil Cognitif Détaillé
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Capacités cognitives */}
              {cognitiveProfile.cognitive_abilities && (
                <div>
                  <h4 className="font-medium text-gray-900 mb-3">Capacités Cognitives</h4>
                  <div className="space-y-3">
                    {Object.entries(cognitiveProfile.cognitive_abilities).map(([key, value]: [string, any]) => (
                      <div key={key}>
                        <div className="flex justify-between text-sm mb-1">
                          <span className="text-gray-700">{key}</span>
                          <span className="text-gray-600">{value}%</span>
                        </div>
                        <Progress value={value} className="h-2" />
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Préférences d'apprentissage */}
              {cognitiveProfile.learning_preferences && (
                <div>
                  <h4 className="font-medium text-gray-900 mb-3">Préférences d'Apprentissage</h4>
                  <div className="space-y-2">
                    {Object.entries(cognitiveProfile.learning_preferences).map(([key, value]: [string, any]) => (
                      <div key={key} className="flex items-center justify-between">
                        <span className="text-sm text-gray-700">{key}</span>
                        <Badge variant="outline">{value}</Badge>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Recommandations IA */}
      {recommendations && recommendations.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg">
              <Lightbulb className="h-5 w-5 text-yellow-600" />
              Recommandations Personnalisées
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recommendations.map((rec: any, index: number) => (
                <div key={index} className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-4">
                  <div className="flex items-start gap-3">
                    <div className="w-2 h-2 bg-blue-600 rounded-full mt-2 flex-shrink-0"></div>
                    <div className="flex-1">
                      <h4 className="font-medium text-gray-900 mb-1">{rec.title}</h4>
                      <p className="text-sm text-gray-700 mb-2">{rec.description}</p>
                      {rec.actions && (
                        <div className="space-y-2">
                          <p className="text-xs font-medium text-gray-600">Actions suggérées :</p>
                          <ul className="text-xs text-gray-600 space-y-1">
                            {rec.actions.map((action: string, actionIndex: number) => (
                              <li key={actionIndex} className="flex items-center gap-2">
                                <Star className="h-3 w-3 text-yellow-500" />
                                {action}
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Métadonnées du profil */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Informations du Profil</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div>
              <span className="text-gray-600">Créé le :</span>
              <span className="ml-2 text-gray-900">
                {new Date(profile.created_at).toLocaleDateString('fr-FR')}
              </span>
            </div>
            <div>
              <span className="text-gray-600">Mis à jour le :</span>
              <span className="ml-2 text-gray-900">
                {new Date(profile.updated_at).toLocaleDateString('fr-FR')}
              </span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Actions */}
      <div className="flex justify-center gap-4">
        <Button onClick={loadProfileData} variant="outline">
          <RefreshCw className="h-4 w-4 mr-2" />
          Actualiser le Profil
        </Button>
        {onRefresh && (
          <Button onClick={onRefresh}>
            <BookOpen className="h-4 w-4 mr-2" />
            Retour à l'Évaluation
          </Button>
        )}
      </div>

      {/* Erreur */}
      {error && (
        <Alert variant="destructive">
          <XCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}
    </div>
  );
};

export default FrenchLearningProfile;
