'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  BarChart3, 
  TrendingUp, 
  Users, 
  Target, 
  Settings, 
  Bell,
  Activity,
  RefreshCw,
  Download,
  Share2,
  Eye,
  EyeOff
} from 'lucide-react';
import RealTimeAnalytics from './RealTimeAnalytics';
import AnalyticsDashboard from './AnalyticsDashboard';
import MetricsCustomizer from './MetricsCustomizer';
import SmartAlerts from './SmartAlerts';
import StudentTestSimulator from './StudentTestSimulator';
import AIPredictions from './analytics/AIPredictions';
import IntelligentAlertsAdvanced from './analytics/IntelligentAlertsAdvanced';
import CustomMetrics from './analytics/CustomMetrics';

interface DashboardConfig {
  showRealTime: boolean;
  showCustomization: boolean;
  showAlerts: boolean;
  showSimulator: boolean;
  autoRefresh: boolean;
  refreshInterval: number;
  compactMode: boolean;
}

export default function AdvancedAnalyticsDashboard() {
  const [activeTab, setActiveTab] = useState('overview');
  const [config, setConfig] = useState<DashboardConfig>({
    showRealTime: true,
    showCustomization: true,
    showAlerts: true,
    showSimulator: true,
    autoRefresh: true,
    refreshInterval: 30,
    compactMode: false
  });
  const [lastRefresh, setLastRefresh] = useState(new Date());
  const [isRefreshing, setIsRefreshing] = useState(false);

  useEffect(() => {
    // Charger la configuration depuis localStorage
    const savedConfig = localStorage.getItem('najah_advanced_dashboard_config');
    if (savedConfig) {
      try {
        const parsed = JSON.parse(savedConfig);
        setConfig(prev => ({ ...prev, ...parsed }));
      } catch (error) {
        console.error('Erreur lors du chargement de la configuration:', error);
      }
    }
  }, []);

  useEffect(() => {
    // Sauvegarder la configuration dans localStorage
    localStorage.setItem('najah_advanced_dashboard_config', JSON.stringify(config));
  }, [config]);

  const handleRefresh = async () => {
    setIsRefreshing(true);
    try {
      // Simuler un rafraîchissement
      await new Promise(resolve => setTimeout(resolve, 1000));
      setLastRefresh(new Date());
    } finally {
      setIsRefreshing(false);
    }
  };

  const toggleFeature = (feature: keyof DashboardConfig) => {
    setConfig(prev => ({ ...prev, [feature]: !prev[feature] }));
  };

  const exportDashboard = () => {
    const data = {
      timestamp: new Date().toISOString(),
      config,
      lastRefresh: lastRefresh.toISOString()
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `najah-dashboard-${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const shareDashboard = () => {
    if (navigator.share) {
      navigator.share({
        title: 'Tableau de Bord Najah AI',
        text: 'Consultez les analytics en temps réel de notre plateforme d\'éducation',
        url: window.location.href
      });
    } else {
      // Fallback pour les navigateurs qui ne supportent pas l'API Share
      navigator.clipboard.writeText(window.location.href);
      alert('Lien copié dans le presse-papiers !');
    }
  };

  return (
    <div className="space-y-6">
      {/* En-tête du tableau de bord */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2 text-2xl">
                <BarChart3 className="w-8 h-8 text-blue-600" />
                Tableau de Bord Analytics Avancé
              </CardTitle>
              <p className="text-gray-600 mt-1">
                Surveillance complète des performances et analytics en temps réel
              </p>
            </div>
            <div className="flex items-center gap-2">
              <Button
                onClick={handleRefresh}
                disabled={isRefreshing}
                variant="outline"
                className="flex items-center gap-2"
              >
                <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} />
                Rafraîchir
              </Button>
              <Button
                onClick={exportDashboard}
                variant="outline"
                className="flex items-center gap-2"
              >
                <Download className="w-4 h-4" />
                Exporter
              </Button>
              <Button
                onClick={shareDashboard}
                variant="outline"
                className="flex items-center gap-2"
              >
                <Share2 className="w-4 h-4" />
                Partager
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Badge variant="outline" className="flex items-center gap-1">
                <Activity className="w-3 h-3" />
                Dernière mise à jour: {lastRefresh.toLocaleTimeString()}
              </Badge>
              <Badge variant="outline" className="flex items-center gap-1">
                <Target className="w-3 h-3" />
                Mode: {config.compactMode ? 'Compact' : 'Standard'}
              </Badge>
            </div>
            <div className="flex items-center gap-2">
              <Button
                onClick={() => toggleFeature('compactMode')}
                variant="outline"
                size="sm"
                className="flex items-center gap-2"
              >
                {config.compactMode ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                {config.compactMode ? 'Standard' : 'Compact'}
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Configuration rapide */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Settings className="w-5 h-5 text-gray-600" />
            Configuration Rapide
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="flex items-center space-x-2">
              <Button
                onClick={() => toggleFeature('showRealTime')}
                variant={config.showRealTime ? 'default' : 'outline'}
                size="sm"
                className="w-full"
              >
                <Activity className="w-4 h-4 mr-1" />
                Temps Réel
              </Button>
            </div>
            <div className="flex items-center space-x-2">
              <Button
                onClick={() => toggleFeature('showCustomization')}
                variant={config.showCustomization ? 'default' : 'outline'}
                size="sm"
                className="w-full"
              >
                <Settings className="w-4 h-4 mr-1" />
                Personnalisation
              </Button>
            </div>
            <div className="flex items-center space-x-2">
              <Button
                onClick={() => toggleFeature('showAlerts')}
                variant={config.showAlerts ? 'default' : 'outline'}
                size="sm"
                className="w-full"
              >
                <Bell className="w-4 h-4 mr-1" />
                Alertes
              </Button>
            </div>
            <div className="flex items-center space-x-2">
              <Button
                onClick={() => toggleFeature('showSimulator')}
                variant={config.showSimulator ? 'default' : 'outline'}
                size="sm"
                className="w-full"
              >
                <Users className="w-4 h-4 mr-1" />
                Simulateur
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Onglets principaux */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-8">
          <TabsTrigger value="overview">Vue d'ensemble</TabsTrigger>
          <TabsTrigger value="realtime">Temps Réel</TabsTrigger>
          <TabsTrigger value="customization">Personnalisation</TabsTrigger>
          <TabsTrigger value="alerts">Alertes</TabsTrigger>
          <TabsTrigger value="predictions">Prédictions IA</TabsTrigger>
          <TabsTrigger value="intelligent-alerts">Alertes Intelligentes</TabsTrigger>
          <TabsTrigger value="custom-metrics">Métriques Perso</TabsTrigger>
          <TabsTrigger value="simulator">Simulateur</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-6">
          <AnalyticsDashboard />
        </TabsContent>

        <TabsContent value="realtime" className="space-y-6">
          {config.showRealTime ? (
            <RealTimeAnalytics />
          ) : (
            <Card>
              <CardContent className="text-center py-8">
                <Activity className="w-12 h-12 mx-auto mb-2 text-gray-400" />
                <p className="text-gray-500">Module Temps Réel désactivé</p>
                <Button
                  onClick={() => toggleFeature('showRealTime')}
                  className="mt-2"
                >
                  Activer
                </Button>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="customization" className="space-y-6">
          {config.showCustomization ? (
            <MetricsCustomizer />
          ) : (
            <Card>
              <CardContent className="text-center py-8">
                <Settings className="w-12 h-12 mx-auto mb-2 text-gray-400" />
                <p className="text-gray-500">Module Personnalisation désactivé</p>
                <Button
                  onClick={() => toggleFeature('showCustomization')}
                  className="mt-2"
                >
                  Activer
                </Button>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="alerts" className="space-y-6">
          {config.showAlerts ? (
            <SmartAlerts />
          ) : (
            <Card>
              <CardContent className="text-center py-8">
                <Bell className="w-12 h-12 mx-auto mb-2 text-gray-400" />
                <p className="text-gray-500">Module Alertes désactivé</p>
                <Button
                  onClick={() => toggleFeature('showAlerts')}
                  className="mt-2"
                >
                  Activer
                </Button>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="predictions" className="space-y-6">
          <AIPredictions />
        </TabsContent>

        <TabsContent value="intelligent-alerts" className="space-y-6">
          <IntelligentAlertsAdvanced />
        </TabsContent>

        <TabsContent value="custom-metrics" className="space-y-6">
          <CustomMetrics />
        </TabsContent>

        <TabsContent value="simulator" className="space-y-6">
          {config.showSimulator ? (
            <StudentTestSimulator />
          ) : (
            <Card>
              <CardContent className="text-center py-8">
                <Users className="w-12 h-12 mx-auto mb-2 text-gray-400" />
                <p className="text-gray-500">Module Simulateur désactivé</p>
                <Button
                  onClick={() => toggleFeature('showSimulator')}
                  className="mt-2"
                >
                  Activer
                </Button>
              </CardContent>
            </Card>
          )}
        </TabsContent>
      </Tabs>

      {/* Pied de page avec statistiques */}
      <Card>
        <CardContent className="py-4">
          <div className="flex items-center justify-between text-sm text-gray-500">
            <div className="flex items-center gap-4">
              <span>Modules actifs: {
                [config.showRealTime, config.showCustomization, config.showAlerts, config.showSimulator]
                  .filter(Boolean).length
              }/4</span>
              <span>Mode: {config.compactMode ? 'Compact' : 'Standard'}</span>
              <span>Auto-refresh: {config.autoRefresh ? 'Activé' : 'Désactivé'}</span>
            </div>
            <div className="flex items-center gap-2">
              <TrendingUp className="w-4 h-4" />
              <span>Performance optimale</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

