'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { 
  Bell, 
  AlertTriangle, 
  CheckCircle, 
  XCircle, 
  Settings, 
  Zap,
  Clock,
  TrendingUp,
  TrendingDown,
  Users,
  Target,
  BarChart3
} from 'lucide-react';

interface AlertRule {
  id: string;
  name: string;
  description: string;
  metric: string;
  condition: 'above' | 'below' | 'equals' | 'changes_by';
  threshold: number;
  timeWindow: number; // minutes
  severity: 'low' | 'medium' | 'high' | 'critical';
  enabled: boolean;
  actions: string[];
  cooldown: number; // minutes
  lastTriggered?: string;
  triggerCount: number;
}

interface Alert {
  id: string;
  ruleId: string;
  ruleName: string;
  message: string;
  severity: string;
  timestamp: string;
  acknowledged: boolean;
  resolved: boolean;
  data: any;
}

export default function SmartAlerts() {
  const [alertRules, setAlertRules] = useState<AlertRule[]>([
    {
      id: 'rule_1',
      name: 'Score moyen trop bas',
      description: 'Alerte si le score moyen global descend sous 60%',
      metric: 'overall_score',
      condition: 'below',
      threshold: 60,
      timeWindow: 30,
      severity: 'high',
      enabled: true,
      actions: ['email', 'dashboard'],
      cooldown: 60,
      triggerCount: 0
    },
    {
      id: 'rule_2',
      name: 'Taux de completion faible',
      description: 'Alerte si moins de 70% des tests sont terminés',
      metric: 'completion_rate',
      condition: 'below',
      threshold: 70,
      timeWindow: 60,
      severity: 'medium',
      enabled: true,
      actions: ['dashboard'],
      cooldown: 120,
      triggerCount: 0
    },
    {
      id: 'rule_3',
      name: 'Tests difficiles en hausse',
      description: 'Alerte si plus de 30% des tests sont considérés difficiles',
      metric: 'difficult_tests',
      condition: 'above',
      threshold: 30,
      timeWindow: 120,
      severity: 'medium',
      enabled: true,
      actions: ['email', 'dashboard', 'slack'],
      cooldown: 180,
      triggerCount: 0
    },
    {
      id: 'rule_4',
      name: 'Engagement en baisse',
      description: 'Alerte si l\'engagement des étudiants descend sous 50%',
      metric: 'student_engagement',
      condition: 'below',
      threshold: 50,
      timeWindow: 240,
      severity: 'high',
      enabled: false,
      actions: ['email', 'dashboard'],
      cooldown: 300,
      triggerCount: 0
    }
  ]);

  const [activeAlerts, setActiveAlerts] = useState<Alert[]>([]);
  const [showCreateRule, setShowCreateRule] = useState(false);
  const [newRule, setNewRule] = useState({
    name: '',
    description: '',
    metric: 'overall_score',
    condition: 'below' as const,
    threshold: 0,
    timeWindow: 30,
    severity: 'medium' as const,
    actions: ['dashboard'] as string[],
    cooldown: 60
  });

  const [metrics] = useState([
    { id: 'overall_score', name: 'Score Moyen Global', unit: '%' },
    { id: 'completion_rate', name: 'Taux de Completion', unit: '%' },
    { id: 'difficult_tests', name: 'Tests Difficiles', unit: '%' },
    { id: 'student_engagement', name: 'Engagement des Étudiants', unit: '%' },
    { id: 'improvement_trend', name: 'Tendance d\'Amélioration', unit: 'points' },
    { id: 'subject_performance', name: 'Performance par Matière', unit: '%' }
  ]);

  const [filters, setFilters] = useState({
    severity: 'all',
    status: 'all',
    metric: 'all'
  });

  useEffect(() => {
    // Simuler des alertes actives
    const mockAlerts: Alert[] = [
      {
        id: 'alert_1',
        ruleId: 'rule_1',
        ruleName: 'Score moyen trop bas',
        message: 'Le score moyen global est descendu à 58% (seuil: 60%)',
        severity: 'high',
        timestamp: new Date(Date.now() - 15 * 60 * 1000).toISOString(),
        acknowledged: false,
        resolved: false,
        data: { currentValue: 58, threshold: 60, metric: 'overall_score' }
      },
      {
        id: 'alert_2',
        ruleId: 'rule_3',
        ruleName: 'Tests difficiles en hausse',
        message: '35% des tests sont maintenant considérés difficiles (seuil: 30%)',
        severity: 'medium',
        timestamp: new Date(Date.now() - 45 * 60 * 1000).toISOString(),
        acknowledged: true,
        resolved: false,
        data: { currentValue: 35, threshold: 30, metric: 'difficult_tests' }
      }
    ];
    setActiveAlerts(mockAlerts);
  }, []);

  const addAlertRule = () => {
    if (!newRule.name || !newRule.description) return;

    const rule: AlertRule = {
      id: `rule_${Date.now()}`,
      name: newRule.name,
      description: newRule.description,
      metric: newRule.metric,
      condition: newRule.condition,
      threshold: newRule.threshold,
      timeWindow: newRule.timeWindow,
      severity: newRule.severity,
      enabled: true,
      actions: newRule.actions,
      cooldown: newRule.cooldown,
      triggerCount: 0
    };

    setAlertRules(prev => [...prev, rule]);
    setNewRule({
      name: '',
      description: '',
      metric: 'overall_score',
      condition: 'below',
      threshold: 0,
      timeWindow: 30,
      severity: 'medium',
      actions: ['dashboard'],
      cooldown: 60
    });
    setShowCreateRule(false);
  };

  const toggleRule = (id: string) => {
    setAlertRules(prev => prev.map(rule => 
      rule.id === id ? { ...rule, enabled: !rule.enabled } : rule
    ));
  };

  const deleteRule = (id: string) => {
    if (confirm('Êtes-vous sûr de vouloir supprimer cette règle ?')) {
      setAlertRules(prev => prev.filter(rule => rule.id !== id));
    }
  };

  const acknowledgeAlert = (id: string) => {
    setActiveAlerts(prev => prev.map(alert => 
      alert.id === id ? { ...alert, acknowledged: true } : alert
    ));
  };

  const resolveAlert = (id: string) => {
    setActiveAlerts(prev => prev.map(alert => 
      alert.id === id ? { ...alert, resolved: true } : alert
    ));
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'bg-red-100 text-red-800 border-red-200';
      case 'high': return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low': return 'bg-blue-100 text-blue-800 border-blue-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'critical': return <XCircle className="w-4 h-4 text-red-600" />;
      case 'high': return <AlertTriangle className="w-4 h-4 text-orange-600" />;
      case 'medium': return <AlertTriangle className="w-4 h-4 text-yellow-600" />;
      case 'low': return <Bell className="w-4 h-4 text-blue-600" />;
      default: return <Bell className="w-4 h-4 text-gray-600" />;
    }
  };

  const getConditionText = (condition: string, threshold: number) => {
    switch (condition) {
      case 'above': return `> ${threshold}`;
      case 'below': return `< ${threshold}`;
      case 'equals': return `= ${threshold}`;
      case 'changes_by': return `change > ${threshold}`;
      default: return threshold;
    }
  };

  const filteredAlerts = activeAlerts.filter(alert => {
    if (filters.severity !== 'all' && alert.severity !== filters.severity) return false;
    if (filters.status !== 'all') {
      if (filters.status === 'active' && alert.resolved) return false;
      if (filters.status === 'acknowledged' && !alert.acknowledged) return false;
      if (filters.status === 'resolved' && !alert.resolved) return false;
    }
    if (filters.metric !== 'all' && alert.data.metric !== filters.metric) return false;
    return true;
  });

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Bell className="w-5 h-5 text-blue-600" />
            Alertes Intelligentes
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-4">
              <Badge variant="outline" className="flex items-center gap-1">
                <AlertTriangle className="w-3 h-3" />
                {activeAlerts.filter(a => !a.resolved).length} alertes actives
              </Badge>
              <Badge variant="outline" className="flex items-center gap-1">
                <CheckCircle className="w-3 h-3" />
                {activeAlerts.filter(a => a.acknowledged && !a.resolved).length} reconnues
              </Badge>
            </div>
            <Button onClick={() => setShowCreateRule(!showCreateRule)} className="flex items-center gap-2">
              <Zap className="w-4 h-4" />
              Nouvelle Règle
            </Button>
          </div>

          {/* Filtres */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div>
              <Label>Sévérité</Label>
              <Select value={filters.severity} onValueChange={(value) => setFilters(prev => ({ ...prev, severity: value }))}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Toutes</SelectItem>
                  <SelectItem value="critical">Critique</SelectItem>
                  <SelectItem value="high">Élevée</SelectItem>
                  <SelectItem value="medium">Moyenne</SelectItem>
                  <SelectItem value="low">Faible</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>Statut</Label>
              <Select value={filters.status} onValueChange={(value) => setFilters(prev => ({ ...prev, status: value }))}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Tous</SelectItem>
                  <SelectItem value="active">Actives</SelectItem>
                  <SelectItem value="acknowledged">Reconnues</SelectItem>
                  <SelectItem value="resolved">Résolues</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>Métrique</Label>
              <Select value={filters.metric} onValueChange={(value) => setFilters(prev => ({ ...prev, metric: value }))}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Toutes</SelectItem>
                  {metrics.map(metric => (
                    <SelectItem key={metric.id} value={metric.id}>{metric.name}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Création de nouvelle règle */}
      {showCreateRule && (
        <Card>
          <CardHeader>
            <CardTitle>Créer une Nouvelle Règle d'Alerte</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label>Nom de la règle</Label>
                <Input
                  value={newRule.name}
                  onChange={(e) => setNewRule(prev => ({ ...prev, name: e.target.value }))}
                  placeholder="Ex: Score critique"
                />
              </div>
              <div>
                <Label>Métrique surveillée</Label>
                <Select value={newRule.metric} onValueChange={(value) => setNewRule(prev => ({ ...prev, metric: value }))}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {metrics.map(metric => (
                      <SelectItem key={metric.id} value={metric.id}>{metric.name}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label>Condition</Label>
                <Select value={newRule.condition} onValueChange={(value: any) => setNewRule(prev => ({ ...prev, condition: value }))}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="above">Au-dessus de</SelectItem>
                    <SelectItem value="below">En-dessous de</SelectItem>
                    <SelectItem value="equals">Égal à</SelectItem>
                    <SelectItem value="changes_by">Change de plus de</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label>Seuil</Label>
                <Input
                  type="number"
                  value={newRule.threshold}
                  onChange={(e) => setNewRule(prev => ({ ...prev, threshold: parseFloat(e.target.value) }))}
                  placeholder="0"
                />
              </div>
              <div>
                <Label>Fenêtre de temps (minutes)</Label>
                <Input
                  type="number"
                  value={newRule.timeWindow}
                  onChange={(e) => setNewRule(prev => ({ ...prev, timeWindow: parseInt(e.target.value) }))}
                  placeholder="30"
                />
              </div>
              <div>
                <Label>Sévérité</Label>
                <Select value={newRule.severity} onValueChange={(value: any) => setNewRule(prev => ({ ...prev, severity: value }))}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="low">Faible</SelectItem>
                    <SelectItem value="medium">Moyenne</SelectItem>
                    <SelectItem value="high">Élevée</SelectItem>
                    <SelectItem value="critical">Critique</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
            <div className="flex gap-2">
              <Button onClick={addAlertRule} className="flex items-center gap-2">
                <Zap className="w-4 h-4" />
                Créer la Règle
              </Button>
              <Button onClick={() => setShowCreateRule(false)} variant="outline">
                Annuler
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Règles d'alerte */}
      <Card>
        <CardHeader>
          <CardTitle>Règles d'Alerte Configurées</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {alertRules.map((rule) => (
            <div key={rule.id} className="border rounded-lg p-4 space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Switch
                    checked={rule.enabled}
                    onCheckedChange={() => toggleRule(rule.id)}
                  />
                  <div>
                    <h4 className="font-medium">{rule.name}</h4>
                    <p className="text-sm text-gray-600">{rule.description}</p>
                    <div className="flex items-center gap-2 mt-1">
                      <Badge className={getSeverityColor(rule.severity)}>
                        {rule.severity}
                      </Badge>
                      <Badge variant="outline">
                        {metrics.find(m => m.id === rule.metric)?.name}
                      </Badge>
                      <Badge variant="outline">
                        {getConditionText(rule.condition, rule.threshold)}
                      </Badge>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-sm text-gray-500">
                    Déclenchée {rule.triggerCount} fois
                  </span>
                  <Button
                    onClick={() => deleteRule(rule.id)}
                    variant="destructive"
                    size="sm"
                  >
                    Supprimer
                  </Button>
                </div>
              </div>
            </div>
          ))}
        </CardContent>
      </Card>

      {/* Alertes actives */}
      <Card>
        <CardHeader>
          <CardTitle>Alertes Actives</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {filteredAlerts.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <CheckCircle className="w-12 h-12 mx-auto mb-2 text-green-500" />
              <p>Aucune alerte active</p>
            </div>
          ) : (
            filteredAlerts.map((alert) => (
              <div key={alert.id} className={`border rounded-lg p-4 ${alert.resolved ? 'bg-gray-50' : ''}`}>
                <div className="flex items-start justify-between">
                  <div className="flex items-start gap-3">
                    {getSeverityIcon(alert.severity)}
                    <div>
                      <h4 className="font-medium">{alert.ruleName}</h4>
                      <p className="text-sm text-gray-600">{alert.message}</p>
                      <div className="flex items-center gap-2 mt-2">
                        <Badge className={getSeverityColor(alert.severity)}>
                          {alert.severity}
                        </Badge>
                        <Badge variant="outline" className="flex items-center gap-1">
                          <Clock className="w-3 h-3" />
                          {new Date(alert.timestamp).toLocaleString()}
                        </Badge>
                        {alert.acknowledged && (
                          <Badge variant="outline" className="bg-blue-50 text-blue-700">
                            Reconnue
                          </Badge>
                        )}
                        {alert.resolved && (
                          <Badge variant="outline" className="bg-green-50 text-green-700">
                            Résolue
                          </Badge>
                        )}
                      </div>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    {!alert.acknowledged && (
                      <Button
                        onClick={() => acknowledgeAlert(alert.id)}
                        variant="outline"
                        size="sm"
                      >
                        Reconnaître
                      </Button>
                    )}
                    {!alert.resolved && (
                      <Button
                        onClick={() => resolveAlert(alert.id)}
                        variant="outline"
                        size="sm"
                      >
                        Résoudre
                      </Button>
                    )}
                  </div>
                </div>
              </div>
            ))
          )}
        </CardContent>
      </Card>
    </div>
  );
}


















