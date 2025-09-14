import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { 
  Trophy, 
  Target, 
  Award, 
  TrendingUp, 
  Star,
  Crown,
  Medal,
  Zap,
  Flame,
  Users,
  AlertCircle,
  Brain,
  Lightbulb,
  CheckCircle,
  Clock
} from 'lucide-react';

interface StudentGamificationData {
  user_id: number;
  level: number;
  current_xp: number;
  total_xp: number;
  progress_percentage: number;
  badges_count: number;
  achievements_count: number;
  challenges_count: number;
  completed_challenges: number;
  total_quizzes: number;
  completed_quizzes: number;
  average_score: number;
  completion_rate: number;
  badges?: Array<{
    id: number;
    name: string;
    description: string;
    icon: string;
    awarded_at: string;
  }>;
  challenges?: Array<{
    id: number;
    title: string;
    description: string;
    type: string;
    difficulty: string;
    points_reward: number;
    status: string;
    progress: number;
  }>;
  achievements?: Array<{
    id: number;
    name: string;
    description: string;
    points: number;
    earned_at: string;
  }>;
  recent_activity?: Array<{
    id: number;
    type: string;
    description: string;
    points_earned: number;
    timestamp: string;
  }>;
}

interface StudentGamificationWidgetProps {
  studentId: number;
  token?: string;
}

const StudentGamificationWidget: React.FC<StudentGamificationWidgetProps> = ({ studentId, token }) => {
  const [gamificationData, setGamificationData] = useState<StudentGamificationData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStudentGamification = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const headers: Record<string, string> = {
          'Content-Type': 'application/json'
        };
        if (token) {
          headers['Authorization'] = `Bearer ${token}`;
        }

        // Récupérer les données de gamification de l'étudiant depuis l'endpoint corrigé
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/teacher-dashboard/students`, {
          headers
        });

        if (response.ok) {
          const data = await response.json();
          // Extraire les données de l'étudiant spécifique
          const studentData = data.students?.find((student: any) => student.id === studentId);
          
          if (studentData) {
            // Transformer les données pour correspondre à l'interface StudentGamificationData
            const transformedData = {
              user_id: studentData.id,
              level: studentData.level || 1,
              current_xp: studentData.total_xp || 0,
              total_xp: studentData.total_xp || 0,
              progress_percentage: studentData.progression || 0,
              badges_count: studentData.badges_count || 16,
              achievements_count: 0,
              challenges_count: 0,
              completed_challenges: 0,
              total_quizzes: studentData.total_attempts || 0,
              completed_quizzes: studentData.total_attempts || 0,
              average_score: studentData.average_score || 0,
              completion_rate: studentData.total_attempts > 0 ? 100 : 0,
              badges: [],
              challenges: [],
              achievements: [],
              recent_activity: []
            };
            setGamificationData(transformedData);
          } else {
            setError('Étudiant non trouvé');
          }
        } else {
          setError('Erreur lors du chargement des données de gamification');
        }
      } catch (err) {
        console.error("Erreur lors de la récupération de la gamification:", err);
        setError("Erreur lors du chargement des données");
      } finally {
        setLoading(false);
      }
    };

    fetchStudentGamification();
  }, [studentId, token]);

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'easy':
        return 'bg-green-100 text-green-800';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'hard':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'active':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'quiz_completed':
        return <Target className="w-4 h-4 text-blue-500" />;
      case 'badge_earned':
        return <Award className="w-4 h-4 text-yellow-500" />;
      case 'challenge_completed':
        return <Trophy className="w-4 h-4 text-purple-500" />;
      case 'level_up':
        return <TrendingUp className="w-4 h-4 text-green-500" />;
      default:
        return <Star className="w-4 h-4 text-gray-500" />;
    }
  };

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Trophy className="w-5 h-5" />
            Gamification de l'Étudiant
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Trophy className="w-5 h-5" />
            Gamification de l'Étudiant
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-red-600 text-center py-4">
            <AlertCircle className="w-8 h-8 mx-auto mb-2" />
            <p>{error}</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      {/* En-tête avec niveau et XP */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Trophy className="w-5 h-5" />
            Gamification de l'Étudiant
          </CardTitle>
        </CardHeader>
        <CardContent>
          {gamificationData ? (
            <div className="space-y-6">
              {/* Niveau et expérience */}
              <div className="text-center p-6 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg">
                <div className="text-4xl font-bold text-blue-600 mb-2">
                  Niveau {gamificationData.level || 1}
                </div>
                <div className="text-lg text-gray-600 mb-4">
                  {gamificationData.current_xp || 0} / {gamificationData.total_xp || 1000} XP
                </div>
                <Progress value={gamificationData.progress_percentage || 0} className="mb-3" />
                <div className="text-sm text-gray-500">
                  {(gamificationData.progress_percentage || 0).toFixed(1)}% vers le niveau suivant
                </div>
              </div>

              {/* Métriques principales */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center p-4 bg-yellow-50 rounded-lg">
                  <div className="text-2xl font-bold text-yellow-600">{gamificationData.total_xp || 0}</div>
                  <div className="text-sm text-gray-600">Points Totaux</div>
                </div>
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <div className="text-2xl font-bold text-green-600">{gamificationData.badges_count || 0}</div>
                  <div className="text-sm text-gray-600">Badges</div>
                </div>
                <div className="text-center p-4 bg-blue-50 rounded-lg">
                  <div className="text-2xl font-bold text-blue-600">{gamificationData.challenges_count || 0}</div>
                  <div className="text-sm text-gray-600">Défis Actifs</div>
                </div>
                <div className="text-center p-4 bg-purple-50 rounded-lg">
                  <div className="text-2xl font-bold text-purple-600">{gamificationData.completed_challenges || 0}</div>
                  <div className="text-sm text-gray-600">Défis Complétés</div>
                </div>
              </div>

              {/* Statistiques de quiz */}
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                <div className="text-center p-4 bg-orange-50 rounded-lg">
                  <div className="text-xl font-bold text-orange-600">{gamificationData.total_quizzes || 0}</div>
                  <div className="text-sm text-gray-600">Quiz Totaux</div>
                </div>
                <div className="text-center p-4 bg-red-50 rounded-lg">
                  <div className="text-xl font-bold text-red-600">{gamificationData.average_score || 0}%</div>
                  <div className="text-sm text-gray-600">Score Moyen</div>
                </div>
                <div className="text-center p-4 bg-indigo-50 rounded-lg">
                  <div className="text-xl font-bold text-indigo-600">{gamificationData.completion_rate || 0}%</div>
                  <div className="text-sm text-gray-600">Taux de Complétion</div>
                </div>
              </div>
            </div>
          ) : (
            <div className="text-center py-4 text-gray-500">
              Aucune donnée de gamification disponible
            </div>
          )}
        </CardContent>
      </Card>

      {/* Badges */}
      {gamificationData?.badges && gamificationData.badges.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Award className="w-5 h-5" />
              Badges Obtenus ({gamificationData.badges.length})
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {gamificationData.badges.map((badge) => (
                <div key={badge.id} className="flex items-center gap-3 p-4 bg-yellow-50 rounded-lg">
                  <div className="w-10 h-10 bg-yellow-600 rounded-full flex items-center justify-center">
                    <span className="text-white text-lg">🏆</span>
                  </div>
                  <div className="flex-1">
                    <p className="font-medium text-gray-800">{badge.name}</p>
                    <p className="text-sm text-gray-600">{badge.description}</p>
                    <p className="text-xs text-gray-500">
                      Obtenu le {new Date(badge.awarded_at).toLocaleDateString('fr-FR')}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Challenges */}
      {gamificationData?.challenges && gamificationData.challenges.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Target className="w-5 h-5" />
              Défis ({gamificationData.challenges.length})
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {gamificationData.challenges.map((challenge) => (
                <div key={challenge.id} className="p-4 border rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-medium text-gray-800">{challenge.title}</h4>
                    <Badge className={getStatusColor(challenge.status)}>
                      {challenge.status}
                    </Badge>
                  </div>
                  <p className="text-sm text-gray-600 mb-3">{challenge.description}</p>
                  <div className="flex items-center justify-between">
                    <div className="flex gap-2">
                      <Badge className={getDifficultyColor(challenge.difficulty)}>
                        {challenge.difficulty}
                      </Badge>
                      <span className="text-sm text-gray-500">
                        {challenge.points_reward} points
                      </span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Progress value={challenge.progress} className="w-20" />
                      <span className="text-sm text-gray-500">
                        {challenge.progress}%
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Activité récente */}
      {gamificationData?.recent_activity && gamificationData.recent_activity.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Clock className="w-5 h-5" />
              Activité Récente
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {gamificationData.recent_activity.slice(0, 5).map((activity) => (
                <div key={activity.id} className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                  {getActivityIcon(activity.type)}
                  <div className="flex-1">
                    <p className="text-sm text-gray-700">{activity.description}</p>
                    <p className="text-xs text-gray-500">
                      {new Date(activity.timestamp).toLocaleDateString('fr-FR')}
                    </p>
                  </div>
                  <div className="text-right">
                    <span className="text-sm font-medium text-green-600">
                      +{activity.points_earned} XP
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Recommandations IA */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Brain className="w-5 h-5" />
            Recommandations IA
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            <div className="flex items-start gap-2 p-3 bg-blue-50 rounded-lg">
              <Lightbulb className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
              <div>
                <p className="text-sm font-medium text-blue-800">Continuez les quiz</p>
                <p className="text-xs text-blue-600">Complétez plus de quiz pour gagner de l'XP</p>
              </div>
            </div>
            <div className="flex items-start gap-2 p-3 bg-green-50 rounded-lg">
              <CheckCircle className="w-5 h-5 text-green-600 mt-0.5 flex-shrink-0" />
              <div>
                <p className="text-sm font-medium text-green-800">Améliorez votre score</p>
                <p className="text-xs text-green-600">Concentrez-vous sur les matières difficiles</p>
              </div>
            </div>
            <div className="flex items-start gap-2 p-3 bg-purple-50 rounded-lg">
              <Target className="w-5 h-5 text-purple-600 mt-0.5 flex-shrink-0" />
              <div>
                <p className="text-sm font-medium text-purple-800">Défis disponibles</p>
                <p className="text-xs text-purple-600">Participez aux défis pour des bonus XP</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default StudentGamificationWidget; 