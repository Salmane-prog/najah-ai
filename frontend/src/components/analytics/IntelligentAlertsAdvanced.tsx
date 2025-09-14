'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Switch } from '@/components/ui/switch';
import { Badge } from '@/components/ui/badge';
import { 
  Bell, 
  AlertTriangle, 
  CheckCircle, 
  XCircle, 
  Settings, 
  Plus,
  Trash2,
  Eye,
  Clock,
  Zap,
  Shield,
  Activity
} from 'lucide-react';

interface AlertRule {
  id: string;
  name: string;
  description: string;
  metric: string;
  operator: '<' | '>' | '==' | '<=';
  threshold: number;
  severity: 'low' | 'medium' | 'high' | 'critical';
  isActive: boolean;
  triggerCount: number;
  lastTriggered?: string;
}

interface Alert {
  id: string;
  ruleId: string;
  ruleName: string;
  message: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  status: 'active' | 'acknowledged' | 'resolved';
  createdAt: string;
  acknowledgedAt?: string;
  resolvedAt?: string;
  currentValue: number;
  threshold: number;
}

interface IntelligentAlertsAdvancedProps {
  className?: string;
}

export default function IntelligentAlertsAdvanced({ className }: IntelligentAlertsAdvancedProps) {
  const [activeTab, setActiveTab] = useState<'rules' | 'active' | 'history' | 'settings'>('rules');
  const [showNewRuleForm, setShowNewRuleForm] = useState(false);
  const [selectedSeverity, setSelectedSeverity] = useState<string>('all');
  const [selectedStatus, setSelectedStatus] = useState<string>('all');
  const [selectedMetric, setSelectedMetric] = useState<string>('all');
  
  const [rules, setRules] = useState<AlertRule[]>([
    {
      id: '1',
      name: 'Score moyen trop bas',
      description: 'Alerte si le score moyen global descend sous 60%',
      metric: 'overall_average_score',
      operator: '<',
      threshold: 60,
      severity: 'high',
      isActive: true,
      triggerCount: 0
    },
    {
      id: '2',
      name: 'Taux de completion faible',
      description: 'Alerte si moins de 70% des tests sont terminés',
      metric: 'completion_rate',
      operator: '<',
      threshold: 70,
      severity: 'medium',
      isActive: true,
      triggerCount: 0
    },
    {
      id: '3',
      name: 'Tests difficiles en hausse',
      description: 'Alerte si plus de 30% des tests sont considérés difficiles',
      metric: 'difficult_tests_percentage',
      operator: '>',
      threshold: 30,
      severity: 'medium',
      isActive: true,
      triggerCount: 0
    },
    {
      id: '4',
      name: 'Engagement en baisse',
      description: 'Alerte si l\'engagement des étudiants descend sous 50%',
      metric: 'student_engagement',
      operator: '<',
      threshold: 50,
      severity: 'high',
      isActive: true,
      triggerCount: 0
    }
  ]);

  const [activeAlerts, setActiveAlerts] = useState<Alert[]>([
    {
      id: '1',
      ruleId: '1',
      ruleName: 'Score moyen trop bas',
      message: 'Le score moyen global est descendu à 58% (seuil: 60%)',
      severity: 'high',
      status: 'active',
      createdAt: '2025-01-19 17:30:00',
      currentValue: 58,
      threshold: 60
    }
  ]);

  const [alertHistory, setAlertHistory] = useState<Alert[]>([
    {
      id: '2',
      ruleId: '2',
      ruleName: 'Taux de completion faible',
      message: 'Le taux de completion est descendu à 65% (seuil: 70%)',
      severity: 'medium',
      status: 'resolved',
      createdAt: '2025-01-18 14:20:00',
      resolvedAt: '2025-01-19 09:15:00',
      currentValue: 65,
      threshold: 70
    }
  ]);

  const [newRule, setNewRule] = useState({
    name: '',
    description: '',
    metric: '',
    operator: '<' as const,
    threshold: 0,
    severity: 'medium' as const
  });

  const metrics = [
    { value: 'overall_average_score', label: 'Score Moyen Global' },
    { value: 'completion_rate', label: 'Taux de Completion' },
    { value: 'difficult_tests_percentage', label: 'Tests Difficiles (%)' },
    { value: 'student_engagement', label: 'Engagement des Étudiants' },
    { value: 'test_creation_rate', label: 'Taux de Création de Tests' },
    { value: 'average_time_spent', label: 'Temps Moyen par Test' }
  ];

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

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-red-100 text-red-800';
      case 'acknowledged': return 'bg-yellow-100 text-yellow-800';
      case 'resolved': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const handleCreateRule = () => {
    if (newRule.name && newRule.metric && newRule.threshold > 0) {
      const rule: AlertRule = {
        id: Date.now().toString(),
        ...newRule,
        isActive: true,
        triggerCount: 0
      };
      setRules([...rules, rule]);
      setNewRule({
        name: '',
        description: '',
        metric: '',
        operator: '<',
        threshold: 0,
        severity: 'medium'
      });
      setShowNewRuleForm(false);
    }
  };

  const handleDeleteRule = (ruleId: string) => {
    setRules(rules.filter(rule => rule.id !== ruleId));
  };

  const handleToggleRule = (ruleId: string) => {
    setRules(rules.map(rule => 
      rule.id === ruleId ? { ...rule, isActive: !rule.isActive } : rule
    ));
  };

  const handleAcknowledgeAlert = (alertId: string) => {
    setActiveAlerts(activeAlerts.map(alert => 
      alert.id === alertId 
        ? { ...alert, status: 'acknowledged', acknowledgedAt: new Date().toISOString() }
        : alert
    ));
  };

  const handleResolveAlert = (alertId: string) => {
    const alert = activeAlerts.find(a => a.id === alertId);
    if (alert) {
      const resolvedAlert = { ...alert, status: 'resolved', resolvedAt: new Date().toISOString() };
      setAlertHistory([...alertHistory, resolvedAlert]);
      setActiveAlerts(activeAlerts.filter(a => a.id !== alertId));
    }
  };

  const filteredRules = rules.filter(rule => 
    (selectedSeverity === 'all' || rule.severity === selectedSeverity) &&
    (selectedMetric === 'all' || rule.metric === selectedMetric)
  );

  const filteredActiveAlerts = activeAlerts.filter(alert => 
    (selectedSeverity === 'all' || alert.severity === selectedSeverity) &&
    (selectedStatus === 'all' || alert.status === selectedStatus)
  );

  return (
    <div className={`space-y-6 ${className}`}>
      {/* En-tête avec onglets */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Bell className="w-6 h-6 text-blue-600" />
          <h2 className="text-2xl font-bold text-gray-900">Alertes Intelligentes</h2>
        </div>
        <div className="flex space-x-2">
          <Button
            variant={activeTab === 'rules' ? 'default' : 'outline'}
            onClick={() => setActiveTab('rules')}
            className="flex items-center space-x-2"
          >
            <Settings className="w-4 h-4" />
            <span>Règles</span>
          </Button>
          <Button
            variant={activeTab === 'active' ? 'default' : 'outline'}
            onClick={() => setActiveTab('active')}
            className="flex items-center space-x-2"
          >
            <AlertTriangle className="w-4 h-4" />
            <span>Actives ({activeAlerts.length})</span>
          </Button>
          <Button
            variant={activeTab === 'history' ? 'default' : 'outline'}
            onClick={() => setActiveTab('history')}
            className="flex items-center space-x-2"
          >
            <Clock className="w-4 h-4" />
            <span>Historique</span>
          </Button>
          <Button
            variant={activeTab === 'settings' ? 'default' : 'outline'}
            onClick={() => setActiveTab('settings')}
            className="flex items-center space-x-2"
          >
            <Shield className="w-4 h-4" />
            <span>Configuration</span>
          </Button>
        </div>
      </div>

      {/* Résumé des alertes */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="bg-red-50 border-red-200">
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <AlertTriangle className="w-5 h-5 text-red-600" />
              <div>
                <p className="text-sm text-red-600">Alertes Actives</p>
                <p className="text-2xl font-bold text-red-700">{activeAlerts.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card className="bg-yellow-50 border-yellow-200">
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <Eye className="w-5 h-5 text-yellow-600" />
              <div>
                <p className="text-sm text-yellow-600">Reconnues</p>
                <p className="text-2xl font-bold text-yellow-700">
                  {activeAlerts.filter(a => a.status === 'acknowledged').length}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card className="bg-green-50 border-green-200">
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <CheckCircle className="w-5 h-5 text-green-600" />
              <div>
                <p className="text-sm text-green-600">Résolues</p>
                <p className="text-2xl font-bold text-green-700">{alertHistory.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card className="bg-blue-50 border-blue-200">
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <Zap className="w-5 h-5 text-blue-600" />
              <div>
                <p className="text-sm text-blue-600">Règles Actives</p>
                <p className="text-2xl font-bold text-blue-700">
                  {rules.filter(r => r.isActive).length}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Contenu des onglets */}
      {activeTab === 'rules' && (
        <div className="space-y-6">
          {/* Filtres */}
          <div className="flex space-x-4">
            <Select value={selectedSeverity} onValueChange={setSelectedSeverity}>
              <SelectTrigger className="w-32">
                <SelectValue placeholder="Sévérité" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Toutes</SelectItem>
                <SelectItem value="low">Faible</SelectItem>
                <SelectItem value="medium">Moyenne</SelectItem>
                <SelectItem value="high">Élevée</SelectItem>
                <SelectItem value="critical">Critique</SelectItem>
              </SelectContent>
            </Select>
            <Select value={selectedMetric} onValueChange={setSelectedMetric}>
              <SelectTrigger className="w-48">
                <SelectValue placeholder="Métrique" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Toutes les métriques</SelectItem>
                {metrics.map((metric) => (
                  <SelectItem key={metric.value} value={metric.value}>
                    {metric.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Button
              onClick={() => setShowNewRuleForm(!showNewRuleForm)}
              className="ml-auto"
            >
              <Plus className="w-4 h-4 mr-2" />
              Nouvelle Règle
            </Button>
          </div>

          {/* Formulaire nouvelle règle */}
          {showNewRuleForm && (
            <Card className="border-blue-200 bg-blue-50">
              <CardHeader>
                <CardTitle className="text-blue-800">Nouvelle Règle d'Alerte</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="ruleName">Nom de la règle</Label>
                    <Input
                      id="ruleName"
                      value={newRule.name}
                      onChange={(e) => setNewRule({...newRule, name: e.target.value})}
                      placeholder="Ex: Score trop bas"
                    />
                  </div>
                  <div>
                    <Label htmlFor="ruleDescription">Description</Label>
                    <Input
                      id="ruleDescription"
                      value={newRule.description}
                      onChange={(e) => setNewRule({...newRule, description: e.target.value})}
                      placeholder="Description de la règle"
                    />
                  </div>
                  <div>
                    <Label htmlFor="ruleMetric">Métrique</Label>
                    <Select value={newRule.metric} onValueChange={(value) => setNewRule({...newRule, metric: value})}>
                      <SelectTrigger>
                        <SelectValue placeholder="Sélectionner une métrique" />
                      </SelectTrigger>
                      <SelectContent>
                        {metrics.map((metric) => (
                          <SelectItem key={metric.value} value={metric.value}>
                            {metric.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <Label htmlFor="ruleThreshold">Seuil</Label>
                    <Input
                      id="ruleThreshold"
                      type="number"
                      value={newRule.threshold}
                      onChange={(e) => setNewRule({...newRule, threshold: parseFloat(e.target.value)})}
                      placeholder="0"
                    />
                  </div>
                  <div>
                    <Label htmlFor="ruleOperator">Opérateur</Label>
                    <Select value={newRule.operator} onValueChange={(value: any) => setNewRule({...newRule, operator: value})}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="<">&lt; (inférieur à)</SelectItem>
                        <SelectItem value=">">&gt; (supérieur à)</SelectItem>
                        <SelectItem value="==">= (égal à)</SelectItem>
                        <SelectItem value="<=">&lt;= (inférieur ou égal)</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <Label htmlFor="ruleSeverity">Sévérité</Label>
                    <Select value={newRule.severity} onValueChange={(value: any) => setNewRule({...newRule, severity: value})}>
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
                <div className="flex space-x-2">
                  <Button onClick={handleCreateRule} className="bg-blue-600 hover:bg-blue-700">
                    Créer la Règle
                  </Button>
                  <Button variant="outline" onClick={() => setShowNewRuleForm(false)}>
                    Annuler
                  </Button>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Liste des règles */}
          <div className="space-y-4">
            {filteredRules.map((rule) => (
              <Card key={rule.id} className="hover:shadow-md transition-shadow">
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <h3 className="font-semibold text-gray-900">{rule.name}</h3>
                        <Badge className={getSeverityColor(rule.severity)}>
                          {rule.severity}
                        </Badge>
                        <div className="flex items-center space-x-2">
                          <Switch
                            checked={rule.isActive}
                            onCheckedChange={() => handleToggleRule(rule.id)}
                          />
                          <span className="text-sm text-gray-600">
                            {rule.isActive ? 'Active' : 'Inactive'}
                          </span>
                        </div>
                      </div>
                      <p className="text-sm text-gray-600 mb-2">{rule.description}</p>
                      <div className="flex items-center space-x-4 text-sm text-gray-500">
                        <span>Métrique: {metrics.find(m => m.value === rule.metric)?.label}</span>
                        <span>Condition: {rule.metric} {rule.operator} {rule.threshold}</span>
                        <span>Déclenchée: {rule.triggerCount} fois</span>
                        {rule.lastTriggered && (
                          <span>Dernière fois: {rule.lastTriggered}</span>
                        )}
                      </div>
                    </div>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleDeleteRule(rule.id)}
                      className="text-red-600 hover:text-red-700 hover:bg-red-50"
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}

      {activeTab === 'active' && (
        <div className="space-y-6">
          {/* Filtres */}
          <div className="flex space-x-4">
            <Select value={selectedSeverity} onValueChange={setSelectedSeverity}>
              <SelectTrigger className="w-32">
                <SelectValue placeholder="Sévérité" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Toutes</SelectItem>
                <SelectItem value="low">Faible</SelectItem>
                <SelectItem value="medium">Moyenne</SelectItem>
                <SelectItem value="high">Élevée</SelectItem>
                <SelectItem value="critical">Critique</SelectItem>
              </SelectContent>
            </Select>
            <Select value={selectedStatus} onValueChange={setSelectedStatus}>
              <SelectTrigger className="w-32">
                <SelectValue placeholder="Statut" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Tous</SelectItem>
                <SelectItem value="active">Active</SelectItem>
                <SelectItem value="acknowledged">Reconnue</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Alertes actives */}
          <div className="space-y-4">
            {filteredActiveAlerts.length === 0 ? (
              <Card className="text-center py-8">
                <CheckCircle className="w-12 h-12 text-green-500 mx-auto mb-2" />
                <p className="text-gray-600">Aucune alerte active !</p>
              </Card>
            ) : (
              filteredActiveAlerts.map((alert) => (
                <Card key={alert.id} className="border-l-4 border-l-red-500">
                  <CardContent className="p-4">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          {getSeverityIcon(alert.severity)}
                          <h3 className="font-semibold text-gray-900">{alert.ruleName}</h3>
                          <Badge className={getSeverityColor(alert.severity)}>
                            {alert.severity}
                          </Badge>
                          <Badge className={getStatusColor(alert.status)}>
                            {alert.status === 'active' ? 'Active' : 'Reconnue'}
                          </Badge>
                        </div>
                        <p className="text-sm text-gray-600 mb-2">{alert.message}</p>
                        <div className="flex items-center space-x-4 text-sm text-gray-500">
                          <span>Valeur actuelle: {alert.currentValue}</span>
                          <span>Seuil: {alert.threshold}</span>
                          <span>Créée: {alert.createdAt}</span>
                          {alert.acknowledgedAt && (
                            <span>Reconnue: {alert.acknowledgedAt}</span>
                          )}
                        </div>
                      </div>
                      <div className="flex space-x-2">
                        {alert.status === 'active' && (
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleAcknowledgeAlert(alert.id)}
                            className="text-yellow-600 hover:text-yellow-700"
                          >
                            <Eye className="w-4 h-4 mr-1" />
                            Reconnaître
                          </Button>
                        )}
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleResolveAlert(alert.id)}
                          className="text-green-600 hover:text-green-700"
                        >
                          <CheckCircle className="w-4 h-4 mr-1" />
                          Résoudre
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))
            )}
          </div>
        </div>
      )}

      {activeTab === 'history' && (
        <div className="space-y-6">
          {/* Historique des alertes */}
          <div className="space-y-4">
            {alertHistory.length === 0 ? (
              <Card className="text-center py-8">
                <Clock className="w-12 h-12 text-gray-400 mx-auto mb-2" />
                <p className="text-gray-600">Aucun historique d'alerte</p>
              </Card>
            ) : (
              alertHistory.map((alert) => (
                <Card key={alert.id} className="border-l-4 border-l-green-500">
                  <CardContent className="p-4">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          <CheckCircle className="w-4 h-4 text-green-600" />
                          <h3 className="font-semibold text-gray-900">{alert.ruleName}</h3>
                          <Badge className={getSeverityColor(alert.severity)}>
                            {alert.severity}
                          </Badge>
                          <Badge className="bg-green-100 text-green-800">
                            Résolue
                          </Badge>
                        </div>
                        <p className="text-sm text-gray-600 mb-2">{alert.message}</p>
                        <div className="flex items-center space-x-4 text-sm text-gray-500">
                          <span>Valeur: {alert.currentValue}</span>
                          <span>Seuil: {alert.threshold}</span>
                          <span>Créée: {alert.createdAt}</span>
                          <span>Résolue: {alert.resolvedAt}</span>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))
            )}
          </div>
        </div>
      )}

      {activeTab === 'settings' && (
        <div className="space-y-6">
          {/* Configuration générale */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Settings className="w-5 h-5 text-blue-500" />
                <span>Configuration Générale</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="flex items-center justify-between">
                  <Label htmlFor="autoRefresh">Actualisation automatique</Label>
                  <Switch id="autoRefresh" defaultChecked />
                </div>
                <div className="flex items-center justify-between">
                  <Label htmlFor="emailNotifications">Notifications par email</Label>
                  <Switch id="emailNotifications" defaultChecked />
                </div>
                <div className="flex items-center justify-between">
                  <Label htmlFor="pushNotifications">Notifications push</Label>
                  <Switch id="pushNotifications" />
                </div>
                <div className="flex items-center justify-between">
                  <Label htmlFor="soundAlerts">Alertes sonores</Label>
                  <Switch id="soundAlerts" />
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Seuils par défaut */}
          <Card>
            <CardHeader>
              <CardTitle>Seuils d'Alerte par Défaut</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="defaultScoreThreshold">Score moyen minimum (%)</Label>
                  <Input id="defaultScoreThreshold" type="number" defaultValue={60} />
                </div>
                <div>
                  <Label htmlFor="defaultCompletionThreshold">Taux de completion minimum (%)</Label>
                  <Input id="defaultCompletionThreshold" type="number" defaultValue={70} />
                </div>
                <div>
                  <Label htmlFor="defaultEngagementThreshold">Engagement minimum (%)</Label>
                  <Input id="defaultEngagementThreshold" type="number" defaultValue={50} />
                </div>
                <div>
                  <Label htmlFor="defaultDifficultyThreshold">Tests difficiles maximum (%)</Label>
                  <Input id="defaultDifficultyThreshold" type="number" defaultValue={30} />
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Actions de maintenance */}
          <Card>
            <CardHeader>
              <CardTitle>Maintenance et Nettoyage</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Button variant="outline" className="justify-start">
                  <Activity className="w-4 h-4 mr-2" />
                  Archiver les anciennes alertes
                </Button>
                <Button variant="outline" className="justify-start">
                  <Trash2 className="w-4 h-4 mr-2" />
                  Nettoyer l'historique
                </Button>
                <Button variant="outline" className="justify-start">
                  <Zap className="w-4 h-4 mr-2" />
                  Optimiser les performances
                </Button>
                <Button variant="outline" className="justify-start">
                  <Shield className="w-4 h-4 mr-2" />
                  Sauvegarder la configuration
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
