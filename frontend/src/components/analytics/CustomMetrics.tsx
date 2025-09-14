'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Switch } from '@/components/ui/switch';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { 
  BarChart3, 
  TrendingUp, 
  TrendingDown, 
  Users, 
  Target, 
  Calendar,
  Plus,
  Trash2,
  Settings,
  PieChart,
  LineChart,
  Activity,
  Star,
  Clock,
  Award
} from 'lucide-react';

interface ClassParticipation {
  classId: number;
  className: string;
  totalStudents: number;
  activeStudents: number;
  participationRate: number;
  averageScore: number;
  trend: 'up' | 'down' | 'stable';
}

interface DifficultyPerformance {
  level: number;
  levelName: string;
  totalTests: number;
  averageScore: number;
  completionRate: number;
  timeSpent: number;
  studentCount: number;
}

interface SeasonalTrend {
  period: string;
  averageScore: number;
  testCount: number;
  studentEngagement: number;
  notes: string[];
}

interface CustomMetric {
  id: string;
  name: string;
  description: string;
  type: 'participation' | 'difficulty' | 'seasonal' | 'custom';
  formula: string;
  isActive: boolean;
  lastCalculated: string;
  value: number;
  unit: string;
}

interface CustomMetricsProps {
  className?: string;
}

export default function CustomMetrics({ className }: CustomMetricsProps) {
  const [activeTab, setActiveTab] = useState<'participation' | 'difficulty' | 'seasonal' | 'custom'>('participation');
  const [selectedClass, setSelectedClass] = useState<string>('all');
  const [selectedDifficulty, setSelectedDifficulty] = useState<string>('all');
  const [selectedPeriod, setSelectedPeriod] = useState<string>('all');
  const [showNewMetricForm, setShowNewMetricForm] = useState(false);

  // Données simulées
  const [classParticipation] = useState<ClassParticipation[]>([
    {
      classId: 1,
      className: "Classe 6ème A",
      totalStudents: 25,
      activeStudents: 22,
      participationRate: 88,
      averageScore: 78.5,
      trend: 'up'
    },
    {
      classId: 2,
      className: "Classe 6ème B",
      totalStudents: 23,
      activeStudents: 20,
      participationRate: 87,
      averageScore: 75.2,
      trend: 'stable'
    },
    {
      classId: 3,
      className: "Classe 5ème A",
      totalStudents: 28,
      activeStudents: 24,
      participationRate: 85.7,
      averageScore: 72.8,
      trend: 'down'
    }
  ]);

  const [difficultyPerformance] = useState<DifficultyPerformance[]>([
    {
      level: 1,
      levelName: "Débutant",
      totalTests: 45,
      averageScore: 85.2,
      completionRate: 92.3,
      timeSpent: 18,
      studentCount: 28
    },
    {
      level: 2,
      levelName: "Intermédiaire Bas",
      totalTests: 52,
      averageScore: 78.9,
      completionRate: 88.7,
      timeSpent: 25,
      studentCount: 32
    },
    {
      level: 3,
      levelName: "Intermédiaire",
      totalTests: 48,
      averageScore: 72.4,
      completionRate: 84.2,
      timeSpent: 32,
      studentCount: 30
    },
    {
      level: 4,
      levelName: "Intermédiaire Haut",
      totalTests: 38,
      averageScore: 68.7,
      completionRate: 79.8,
      timeSpent: 38,
      studentCount: 25
    },
    {
      level: 5,
      levelName: "Avancé",
      totalTests: 35,
      averageScore: 63.2,
      completionRate: 75.4,
      timeSpent: 45,
      studentCount: 22
    }
  ]);

  const [seasonalTrends] = useState<SeasonalTrend[]>([
    {
      period: "Lundi",
      averageScore: 78.5,
      testCount: 15,
      studentEngagement: 85.2,
      notes: ["Meilleur jour de la semaine", "Tests plus faciles programmés"]
    },
    {
      period: "Mardi",
      averageScore: 76.8,
      testCount: 18,
      studentEngagement: 82.1,
      notes: ["Engagement stable", "Tests de niveau moyen"]
    },
    {
      period: "Mercredi",
      averageScore: 74.2,
      testCount: 12,
      studentEngagement: 78.9,
      notes: ["Journée plus courte", "Moins d'activité"]
    },
    {
      period: "Jeudi",
      averageScore: 75.9,
      testCount: 20,
      studentEngagement: 80.3,
      notes: ["Récupération après mercredi", "Tests variés"]
    },
    {
      period: "Vendredi",
      averageScore: 72.1,
      testCount: 16,
      studentEngagement: 75.6,
      notes: ["Fatigue de fin de semaine", "Tests plus difficiles"]
    }
  ]);

  const [customMetrics, setCustomMetrics] = useState<CustomMetric[]>([
    {
      id: '1',
      name: 'Indice de Progression Global',
      description: 'Moyenne pondérée des scores par niveau de difficulté',
      type: 'custom',
      formula: 'Σ(score × niveau) / Σ(niveau)',
      isActive: true,
      lastCalculated: '2025-01-19 17:45:00',
      value: 76.8,
      unit: 'points'
    },
    {
      id: '2',
      name: 'Taux d\'Engagement Qualitatif',
      description: 'Score moyen × Taux de participation × Temps moyen',
      type: 'custom',
      formula: 'score_moyen × participation × (temps/60)',
      isActive: true,
      lastCalculated: '2025-01-19 17:45:00',
      value: 68.4,
      unit: '%'
    }
  ]);

  const [newMetric, setNewMetric] = useState({
    name: '',
    description: '',
    type: 'custom' as const,
    formula: '',
    unit: ''
  });

  const getTrendIcon = (trend: 'up' | 'down' | 'stable') => {
    switch (trend) {
      case 'up':
        return <TrendingUp className="w-4 h-4 text-green-500" />;
      case 'down':
        return <TrendingDown className="w-4 h-4 text-red-500" />;
      default:
        return <Activity className="w-4 h-4 text-blue-500" />;
    }
  };

  const getTrendColor = (trend: 'up' | 'down' | 'stable') => {
    switch (trend) {
      case 'up':
        return 'text-green-600';
      case 'down':
        return 'text-red-600';
      default:
        return 'text-blue-600';
    }
  };

  const getDifficultyColor = (level: number) => {
    if (level <= 2) return 'bg-green-100 text-green-800';
    if (level <= 3) return 'bg-yellow-100 text-yellow-800';
    if (level <= 4) return 'bg-orange-100 text-orange-800';
    return 'bg-red-100 text-red-800';
  };

  const handleCreateMetric = () => {
    if (newMetric.name && newMetric.formula) {
      const metric: CustomMetric = {
        id: Date.now().toString(),
        ...newMetric,
        isActive: true,
        lastCalculated: new Date().toISOString(),
        value: Math.random() * 100
      };
      setCustomMetrics([...customMetrics, metric]);
      setNewMetric({
        name: '',
        description: '',
        type: 'custom',
        formula: '',
        unit: ''
      });
      setShowNewMetricForm(false);
    }
  };

  const handleDeleteMetric = (metricId: string) => {
    setCustomMetrics(customMetrics.filter(metric => metric.id !== metricId));
  };

  const handleToggleMetric = (metricId: string) => {
    setCustomMetrics(customMetrics.map(metric => 
      metric.id === metricId ? { ...metric, isActive: !metric.isActive } : metric
    ));
  };

  return (
    <div className={`space-y-6 ${className}`}>
      {/* En-tête avec onglets */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <BarChart3 className="w-6 h-6 text-blue-600" />
          <h2 className="text-2xl font-bold text-gray-900">Métriques Personnalisées</h2>
        </div>
        <div className="flex space-x-2">
          <Button
            variant={activeTab === 'participation' ? 'default' : 'outline'}
            onClick={() => setActiveTab('participation')}
            className="flex items-center space-x-2"
          >
            <Users className="w-4 h-4" />
            <span>Participation</span>
          </Button>
          <Button
            variant={activeTab === 'difficulty' ? 'default' : 'outline'}
            onClick={() => setActiveTab('difficulty')}
            className="flex items-center space-x-2"
          >
            <Target className="w-4 h-4" />
            <span>Difficulté</span>
          </Button>
          <Button
            variant={activeTab === 'seasonal' ? 'default' : 'outline'}
            onClick={() => setActiveTab('seasonal')}
            className="flex items-center space-x-2"
          >
            <Calendar className="w-4 h-4" />
            <span>Saisonnier</span>
          </Button>
          <Button
            variant={activeTab === 'custom' ? 'default' : 'outline'}
            onClick={() => setActiveTab('custom')}
            className="flex items-center space-x-2"
          >
            <Plus className="w-4 h-4" />
            <span>Personnalisées</span>
          </Button>
        </div>
      </div>

      {/* Contenu des onglets */}
      {activeTab === 'participation' && (
        <div className="space-y-6">
          {/* Filtres */}
          <div className="flex space-x-4">
            <Select value={selectedClass} onValueChange={setSelectedClass}>
              <SelectTrigger className="w-48">
                <SelectValue placeholder="Sélectionner une classe" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Toutes les classes</SelectItem>
                {classParticipation.map((cls) => (
                  <SelectItem key={cls.classId} value={cls.classId.toString()}>
                    {cls.className}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Métriques de participation par classe */}
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {classParticipation
              .filter(cls => selectedClass === 'all' || cls.classId.toString() === selectedClass)
              .map((cls) => (
                <Card key={cls.classId} className="hover:shadow-lg transition-shadow">
                  <CardHeader className="pb-3">
                    <CardTitle className="flex items-center justify-between text-lg">
                      <span>{cls.className}</span>
                      {getTrendIcon(cls.trend)}
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    {/* Taux de participation */}
                    <div className="space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">Participation</span>
                        <span className="font-semibold">{cls.participationRate}%</span>
                      </div>
                      <Progress value={cls.participationRate} className="h-2" />
                      <div className="text-xs text-gray-500">
                        {cls.activeStudents} / {cls.totalStudents} étudiants actifs
                      </div>
                    </div>

                    {/* Score moyen */}
                    <div className="space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">Score moyen</span>
                        <span className={`font-semibold ${getTrendColor(cls.trend)}`}>
                          {cls.averageScore}%
                        </span>
                      </div>
                    </div>

                    {/* Statistiques */}
                    <div className="grid grid-cols-2 gap-4 pt-2">
                      <div className="text-center">
                        <div className="text-2xl font-bold text-blue-600">{cls.totalStudents}</div>
                        <div className="text-xs text-gray-600">Total</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-green-600">{cls.activeStudents}</div>
                        <div className="text-xs text-gray-600">Actifs</div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
          </div>
        </div>
      )}

      {activeTab === 'difficulty' && (
        <div className="space-y-6">
          {/* Filtres */}
          <div className="flex space-x-4">
            <Select value={selectedDifficulty} onValueChange={setSelectedDifficulty}>
              <SelectTrigger className="w-48">
                <SelectValue placeholder="Niveau de difficulté" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Tous les niveaux</SelectItem>
                {difficultyPerformance.map((diff) => (
                  <SelectItem key={diff.level} value={diff.level.toString()}>
                    Niveau {diff.level} - {diff.levelName}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Performance par niveau de difficulté */}
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {difficultyPerformance
              .filter(diff => selectedDifficulty === 'all' || diff.level.toString() === selectedDifficulty)
              .map((diff) => (
                <Card key={diff.level} className="hover:shadow-lg transition-shadow">
                  <CardHeader className="pb-3">
                    <CardTitle className="flex items-center justify-between text-lg">
                      <span>Niveau {diff.level}</span>
                      <Badge className={getDifficultyColor(diff.level)}>
                        {diff.levelName}
                      </Badge>
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    {/* Score moyen */}
                    <div className="space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">Score moyen</span>
                        <span className="font-semibold">{diff.averageScore}%</span>
                      </div>
                      <Progress value={diff.averageScore} className="h-2" />
                    </div>

                    {/* Taux de completion */}
                    <div className="space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">Taux de completion</span>
                        <span className="font-semibold">{diff.completionRate}%</span>
                      </div>
                      <Progress value={diff.completionRate} className="h-2" />
                    </div>

                    {/* Statistiques */}
                    <div className="grid grid-cols-2 gap-4 pt-2">
                      <div className="text-center">
                        <div className="text-2xl font-bold text-blue-600">{diff.totalTests}</div>
                        <div className="text-xs text-gray-600">Tests</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-green-600">{diff.studentCount}</div>
                        <div className="text-xs text-gray-600">Étudiants</div>
                      </div>
                    </div>

                    {/* Temps moyen */}
                    <div className="text-center pt-2">
                      <div className="text-lg font-semibold text-purple-600">{diff.timeSpent} min</div>
                      <div className="text-xs text-gray-600">Temps moyen</div>
                    </div>
                  </CardContent>
                </Card>
              ))}
          </div>
        </div>
      )}

      {activeTab === 'seasonal' && (
        <div className="space-y-6">
          {/* Filtres */}
          <div className="flex space-x-4">
            <Select value={selectedPeriod} onValueChange={setSelectedPeriod}>
              <SelectTrigger className="w-48">
                <SelectValue placeholder="Période" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Toutes les périodes</SelectItem>
                {seasonalTrends.map((trend) => (
                  <SelectItem key={trend.period} value={trend.period}>
                    {trend.period}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Tendances saisonnières */}
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {seasonalTrends
              .filter(trend => selectedPeriod === 'all' || trend.period === selectedPeriod)
              .map((trend) => (
                <Card key={trend.period} className="hover:shadow-lg transition-shadow">
                  <CardHeader className="pb-3">
                    <CardTitle className="flex items-center justify-between text-lg">
                      <span>{trend.period}</span>
                      <Calendar className="w-5 h-5 text-blue-500" />
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    {/* Score moyen */}
                    <div className="space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">Score moyen</span>
                        <span className="font-semibold">{trend.averageScore}%</span>
                      </div>
                      <Progress value={trend.averageScore} className="h-2" />
                    </div>

                    {/* Engagement */}
                    <div className="space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">Engagement</span>
                        <span className="font-semibold">{trend.studentEngagement}%</span>
                      </div>
                      <Progress value={trend.studentEngagement} className="h-2" />
                    </div>

                    {/* Statistiques */}
                    <div className="grid grid-cols-2 gap-4 pt-2">
                      <div className="text-center">
                        <div className="text-2xl font-bold text-blue-600">{trend.testCount}</div>
                        <div className="text-xs text-gray-600">Tests</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-green-600">{trend.studentEngagement}%</div>
                        <div className="text-xs text-gray-600">Engagement</div>
                      </div>
                    </div>

                    {/* Notes */}
                    <div className="space-y-2">
                      <h4 className="text-sm font-medium text-gray-700">Observations</h4>
                      <ul className="space-y-1">
                        {trend.notes.map((note, index) => (
                          <li key={index} className="text-xs text-gray-600 flex items-start space-x-2">
                            <Star className="w-3 h-3 text-yellow-500 mt-0.5 flex-shrink-0" />
                            <span>{note}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </CardContent>
                </Card>
              ))}
          </div>
        </div>
      )}

      {activeTab === 'custom' && (
        <div className="space-y-6">
          {/* Filtres et actions */}
          <div className="flex justify-between items-center">
            <div className="text-sm text-gray-600">
              {customMetrics.filter(m => m.isActive).length} métriques actives sur {customMetrics.length}
            </div>
            <Button
              onClick={() => setShowNewMetricForm(!showNewMetricForm)}
              className="bg-blue-600 hover:bg-blue-700"
            >
              <Plus className="w-4 h-4 mr-2" />
              Nouvelle Métrique
            </Button>
          </div>

          {/* Formulaire nouvelle métrique */}
          {showNewMetricForm && (
            <Card className="border-blue-200 bg-blue-50">
              <CardHeader>
                <CardTitle className="text-blue-800">Nouvelle Métrique Personnalisée</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="metricName">Nom de la métrique</Label>
                    <Input
                      id="metricName"
                      value={newMetric.name}
                      onChange={(e) => setNewMetric({...newMetric, name: e.target.value})}
                      placeholder="Ex: Indice de progression"
                    />
                  </div>
                  <div>
                    <Label htmlFor="metricDescription">Description</Label>
                    <Input
                      id="metricDescription"
                      value={newMetric.description}
                      onChange={(e) => setNewMetric({...newMetric, description: e.target.value})}
                      placeholder="Description de la métrique"
                    />
                  </div>
                  <div>
                    <Label htmlFor="metricFormula">Formule de calcul</Label>
                    <Input
                      id="metricFormula"
                      value={newMetric.formula}
                      onChange={(e) => setNewMetric({...newMetric, formula: e.target.value})}
                      placeholder="Ex: score × participation"
                    />
                  </div>
                  <div>
                    <Label htmlFor="metricUnit">Unité</Label>
                    <Input
                      id="metricUnit"
                      value={newMetric.unit}
                      onChange={(e) => setNewMetric({...newMetric, unit: e.target.value})}
                      placeholder="Ex: points, %, etc."
                    />
                  </div>
                </div>
                <div className="flex space-x-2">
                  <Button onClick={handleCreateMetric} className="bg-blue-600 hover:bg-blue-700">
                    Créer la Métrique
                  </Button>
                  <Button variant="outline" onClick={() => setShowNewMetricForm(false)}>
                    Annuler
                  </Button>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Liste des métriques personnalisées */}
          <div className="grid gap-6 md:grid-cols-2">
            {customMetrics.map((metric) => (
              <Card key={metric.id} className="hover:shadow-lg transition-shadow">
                <CardHeader className="pb-3">
                  <CardTitle className="flex items-center justify-between text-lg">
                    <span>{metric.name}</span>
                    <div className="flex items-center space-x-2">
                      <Switch
                        checked={metric.isActive}
                        onCheckedChange={() => handleToggleMetric(metric.id)}
                      />
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleDeleteMetric(metric.id)}
                        className="text-red-600 hover:text-red-700"
                      >
                        <Trash2 className="w-4 h-4" />
                      </Button>
                    </div>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <p className="text-sm text-gray-600">{metric.description}</p>
                  
                  {/* Formule */}
                  <div className="bg-gray-50 p-3 rounded-lg">
                    <div className="text-sm font-medium text-gray-700 mb-1">Formule</div>
                    <code className="text-sm text-blue-600">{metric.formula}</code>
                  </div>

                  {/* Valeur actuelle */}
                  <div className="text-center">
                    <div className="text-3xl font-bold text-green-600">{metric.value.toFixed(1)}</div>
                    <div className="text-sm text-gray-600">{metric.unit}</div>
                  </div>

                  {/* Métadonnées */}
                  <div className="text-xs text-gray-500 space-y-1">
                    <div>Dernière mise à jour: {metric.lastCalculated}</div>
                    <div>Type: {metric.type}</div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}














