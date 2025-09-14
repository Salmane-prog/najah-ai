'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Slider } from '@/components/ui/slider';
import { Badge } from '@/components/ui/badge';
import { 
  Settings, 
  BarChart3, 
  Target, 
  TrendingUp, 
  Users, 
  Clock,
  Save,
  RefreshCw,
  Eye,
  EyeOff
} from 'lucide-react';

interface MetricConfig {
  id: string;
  name: string;
  description: string;
  enabled: boolean;
  weight: number;
  threshold: number;
  alertEnabled: boolean;
  displayType: 'card' | 'chart' | 'gauge' | 'progress';
  refreshInterval: number;
  customFormula?: string;
}

interface CustomMetric {
  id: string;
  name: string;
  description: string;
  formula: string;
  enabled: boolean;
  category: string;
}

export default function MetricsCustomizer() {
  const [metrics, setMetrics] = useState<MetricConfig[]>([
    {
      id: 'overall_score',
      name: 'Score Moyen Global',
      description: 'Score moyen de tous les étudiants sur tous les tests',
      enabled: true,
      weight: 10,
      threshold: 70,
      alertEnabled: true,
      displayType: 'card',
      refreshInterval: 30
    },
    {
      id: 'completion_rate',
      name: 'Taux de Completion',
      description: 'Pourcentage de tests terminés par rapport aux tests créés',
      enabled: true,
      weight: 8,
      threshold: 80,
      alertEnabled: true,
      displayType: 'progress',
      refreshInterval: 60
    },
    {
      id: 'difficult_tests',
      name: 'Tests Difficiles',
      description: 'Pourcentage de tests avec un score moyen inférieur à 60%',
      enabled: true,
      weight: 6,
      threshold: 20,
      alertEnabled: true,
      displayType: 'gauge',
      refreshInterval: 120
    },
    {
      id: 'student_engagement',
      name: 'Engagement des Étudiants',
      description: 'Moyenne des sessions actives et temps passé sur les tests',
      enabled: true,
      weight: 7,
      threshold: 75,
      alertEnabled: false,
      displayType: 'chart',
      refreshInterval: 45
    },
    {
      id: 'improvement_trend',
      name: 'Tendance d\'Amélioration',
      description: 'Évolution des scores sur les 4 dernières semaines',
      enabled: true,
      weight: 9,
      threshold: 5,
      alertEnabled: true,
      displayType: 'chart',
      refreshInterval: 300
    },
    {
      id: 'subject_performance',
      name: 'Performance par Matière',
      description: 'Comparaison des scores moyens entre les différentes matières',
      enabled: false,
      weight: 5,
      threshold: 75,
      alertEnabled: false,
      displayType: 'chart',
      refreshInterval: 600
    }
  ]);

  const [customMetrics, setCustomMetrics] = useState<CustomMetric[]>([]);
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [newCustomMetric, setNewCustomMetric] = useState({
    name: '',
    description: '',
    formula: '',
    category: 'performance'
  });

  const [dashboardLayout, setDashboardLayout] = useState({
    columns: 4,
    autoRefresh: true,
    refreshInterval: 30,
    showAlerts: true,
    compactMode: false
  });

  const updateMetric = (id: string, updates: Partial<MetricConfig>) => {
    setMetrics(prev => prev.map(metric => 
      metric.id === id ? { ...metric, ...updates } : metric
    ));
  };

  const toggleMetric = (id: string) => {
    updateMetric(id, { enabled: !metrics.find(m => m.id === id)?.enabled });
  };

  const addCustomMetric = () => {
    if (!newCustomMetric.name || !newCustomMetric.formula) return;

    const metric: CustomMetric = {
      id: `custom_${Date.now()}`,
      name: newCustomMetric.name,
      description: newCustomMetric.description,
      formula: newCustomMetric.formula,
      enabled: true,
      category: newCustomMetric.category
    };

    setCustomMetrics(prev => [...prev, metric]);
    setNewCustomMetric({ name: '', description: '', formula: '', category: 'performance' });
  };

  const removeCustomMetric = (id: string) => {
    setCustomMetrics(prev => prev.filter(m => m.id !== id));
  };

  const saveConfiguration = () => {
    const config = {
      metrics,
      customMetrics,
      dashboardLayout,
      timestamp: new Date().toISOString()
    };

    localStorage.setItem('najah_analytics_config', JSON.stringify(config));
    alert('Configuration sauvegardée avec succès !');
  };

  const loadConfiguration = () => {
    const saved = localStorage.getItem('najah_analytics_config');
    if (saved) {
      try {
        const config = JSON.parse(saved);
        setMetrics(config.metrics || metrics);
        setCustomMetrics(config.customMetrics || customMetrics);
        setDashboardLayout(config.dashboardLayout || dashboardLayout);
        alert('Configuration chargée avec succès !');
      } catch (error) {
        alert('Erreur lors du chargement de la configuration');
      }
    }
  };

  const resetToDefaults = () => {
    if (confirm('Êtes-vous sûr de vouloir réinitialiser à la configuration par défaut ?')) {
      window.location.reload();
    }
  };

  const getDisplayTypeIcon = (type: string) => {
    switch (type) {
      case 'card': return <BarChart3 className="w-4 h-4" />;
      case 'chart': return <TrendingUp className="w-4 h-4" />;
      case 'gauge': return <Target className="w-4 h-4" />;
      case 'progress': return <Users className="w-4 h-4" />;
      default: return <BarChart3 className="w-4 h-4" />;
    }
  };

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'performance': return 'bg-blue-100 text-blue-800';
      case 'engagement': return 'bg-green-100 text-green-800';
      case 'quality': return 'bg-purple-100 text-purple-800';
      case 'trends': return 'bg-orange-100 text-orange-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Settings className="w-5 h-5 text-blue-600" />
            Personnalisation des Métriques Analytics
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Button onClick={saveConfiguration} className="flex items-center gap-2">
                <Save className="w-4 h-4" />
                Sauvegarder
              </Button>
              <Button onClick={loadConfiguration} variant="outline" className="flex items-center gap-2">
                <RefreshCw className="w-4 h-4" />
                Charger
              </Button>
              <Button onClick={resetToDefaults} variant="outline" className="flex items-center gap-2">
                <RefreshCw className="w-4 h-4" />
                Réinitialiser
              </Button>
            </div>
            <Button
              onClick={() => setShowAdvanced(!showAdvanced)}
              variant="outline"
              className="flex items-center gap-2"
            >
              {showAdvanced ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              {showAdvanced ? 'Masquer Avancé' : 'Afficher Avancé'}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Métriques prédéfinies */}
      <Card>
        <CardHeader>
          <CardTitle>Métriques Prédéfinies</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {metrics.map((metric) => (
            <div key={metric.id} className="border rounded-lg p-4 space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Switch
                    checked={metric.enabled}
                    onCheckedChange={() => toggleMetric(metric.id)}
                  />
                  <div>
                    <h4 className="font-medium">{metric.name}</h4>
                    <p className="text-sm text-gray-600">{metric.description}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  {getDisplayTypeIcon(metric.displayType)}
                  <Badge variant="outline">{metric.displayType}</Badge>
                </div>
              </div>

              {metric.enabled && (
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                  <div>
                    <Label>Poids</Label>
                    <Slider
                      value={[metric.weight]}
                      onValueChange={([value]) => updateMetric(metric.id, { weight: value })}
                      max={10}
                      min={1}
                      step={1}
                      className="w-full"
                    />
                    <span className="text-sm text-gray-500">{metric.weight}/10</span>
                  </div>

                  <div>
                    <Label>Seuil d'alerte</Label>
                    <Input
                      type="number"
                      value={metric.threshold}
                      onChange={(e) => updateMetric(metric.id, { threshold: parseFloat(e.target.value) })}
                      className="w-full"
                    />
                  </div>

                  <div>
                    <Label>Type d'affichage</Label>
                    <Select
                      value={metric.displayType}
                      onValueChange={(value) => updateMetric(metric.id, { displayType: value as any })}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="card">Carte</SelectItem>
                        <SelectItem value="chart">Graphique</SelectItem>
                        <SelectItem value="gauge">Jauge</SelectItem>
                        <SelectItem value="progress">Barre de progression</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <Label>Intervalle de rafraîchissement (sec)</Label>
                    <Input
                      type="number"
                      value={metric.refreshInterval}
                      onChange={(e) => updateMetric(metric.id, { refreshInterval: parseInt(e.target.value) })}
                      className="w-full"
                    />
                  </div>
                </div>
              )}
            </div>
          ))}
        </CardContent>
      </Card>

      {/* Métriques personnalisées */}
      <Card>
        <CardHeader>
          <CardTitle>Métriques Personnalisées</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4 border rounded-lg">
            <div>
              <Label>Nom de la métrique</Label>
              <Input
                value={newCustomMetric.name}
                onChange={(e) => setNewCustomMetric(prev => ({ ...prev, name: e.target.value }))}
                placeholder="Ex: Ratio de réussite par niveau"
              />
            </div>
            <div>
              <Label>Catégorie</Label>
              <Select
                value={newCustomMetric.category}
                onValueChange={(value) => setNewCustomMetric(prev => ({ ...prev, category: value }))}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="performance">Performance</SelectItem>
                  <SelectItem value="engagement">Engagement</SelectItem>
                  <SelectItem value="quality">Qualité</SelectItem>
                  <SelectItem value="trends">Tendances</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="md:col-span-2">
              <Label>Description</Label>
              <Input
                value={newCustomMetric.description}
                onChange={(e) => setNewCustomMetric(prev => ({ ...prev, description: e.target.value }))}
                placeholder="Description de la métrique personnalisée"
              />
            </div>
            <div className="md:col-span-2">
              <Label>Formule de calcul</Label>
              <Input
                value={newCustomMetric.formula}
                onChange={(e) => setNewCustomMetric(prev => ({ ...prev, formula: e.target.value }))}
                placeholder="Ex: (score_moyen * 0.6) + (taux_completion * 0.4)"
              />
              <p className="text-xs text-gray-500 mt-1">
                Utilisez les variables: score_moyen, taux_completion, tests_crees, etc.
              </p>
            </div>
            <div className="md:col-span-2">
              <Button onClick={addCustomMetric} className="w-full">
                Ajouter la Métrique Personnalisée
              </Button>
            </div>
          </div>

          {customMetrics.length > 0 && (
            <div className="space-y-3">
              <h4 className="font-medium">Métriques personnalisées actives</h4>
              {customMetrics.map((metric) => (
                <div key={metric.id} className="flex items-center justify-between p-3 border rounded-lg">
                  <div>
                    <h5 className="font-medium">{metric.name}</h5>
                    <p className="text-sm text-gray-600">{metric.description}</p>
                    <div className="flex items-center gap-2 mt-1">
                      <Badge className={getCategoryColor(metric.category)}>
                        {metric.category}
                      </Badge>
                      <code className="text-xs bg-gray-100 px-2 py-1 rounded">
                        {metric.formula}
                      </code>
                    </div>
                  </div>
                  <Button
                    onClick={() => removeCustomMetric(metric.id)}
                    variant="destructive"
                    size="sm"
                  >
                    Supprimer
                  </Button>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Configuration du tableau de bord */}
      {showAdvanced && (
        <Card>
          <CardHeader>
            <CardTitle>Configuration du Tableau de Bord</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label>Nombre de colonnes</Label>
                <Select
                  value={dashboardLayout.columns.toString()}
                  onValueChange={(value) => setDashboardLayout(prev => ({ ...prev, columns: parseInt(value) }))}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="2">2 colonnes</SelectItem>
                    <SelectItem value="3">3 colonnes</SelectItem>
                    <SelectItem value="4">4 colonnes</SelectItem>
                    <SelectItem value="6">6 colonnes</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label>Intervalle de rafraîchissement automatique (secondes)</Label>
                <Input
                  type="number"
                  value={dashboardLayout.refreshInterval}
                  onChange={(e) => setDashboardLayout(prev => ({ ...prev, refreshInterval: parseInt(e.target.value) }))}
                />
              </div>

              <div className="flex items-center space-x-2">
                <Switch
                  checked={dashboardLayout.autoRefresh}
                  onCheckedChange={(checked) => setDashboardLayout(prev => ({ ...prev, autoRefresh: checked }))}
                />
                <Label>Rafraîchissement automatique</Label>
              </div>

              <div className="flex items-center space-x-2">
                <Switch
                  checked={dashboardLayout.showAlerts}
                  onCheckedChange={(checked) => setDashboardLayout(prev => ({ ...prev, showAlerts: checked }))}
                />
                <Label>Afficher les alertes</Label>
              </div>

              <div className="flex items-center space-x-2">
                <Switch
                  checked={dashboardLayout.compactMode}
                  onCheckedChange={(checked) => setDashboardLayout(prev => ({ ...prev, compactMode: checked }))}
                />
                <Label>Mode compact</Label>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Aperçu de la configuration */}
      <Card>
        <CardHeader>
          <CardTitle>Aperçu de la Configuration</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h4 className="font-medium mb-2">Métriques activées</h4>
              <div className="space-y-1">
                {metrics.filter(m => m.enabled).map(metric => (
                  <div key={metric.id} className="flex items-center justify-between text-sm">
                    <span>{metric.name}</span>
                    <Badge variant="outline">Poids: {metric.weight}</Badge>
                  </div>
                ))}
              </div>
            </div>
            <div>
              <h4 className="font-medium mb-2">Métriques personnalisées</h4>
              <div className="space-y-1">
                {customMetrics.map(metric => (
                  <div key={metric.id} className="flex items-center justify-between text-sm">
                    <span>{metric.name}</span>
                    <Badge className={getCategoryColor(metric.category)}>
                      {metric.category}
                    </Badge>
                  </div>
                ))}
                {customMetrics.length === 0 && (
                  <span className="text-gray-500 text-sm">Aucune métrique personnalisée</span>
                )}
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}















