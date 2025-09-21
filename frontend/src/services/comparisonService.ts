'use client';

import { API_BASE_URL } from '@/config/api';

export interface ProgressComparison {
  topic: string;
  before: {
    current_level: number;
    success_rate: number;
    exercises_completed: number;
    last_updated: string;
  };
  after: {
    current_level: number;
    success_rate: number;
    exercises_completed: number;
    last_updated: string;
  };
  improvement_percentage: number;
  time_to_improve?: number;
}

export interface ComparisonData {
  topic: string;
  dates: string[];
  levels: number[];
  successRates: number[];
  exerciseCounts: number[];
  improvements: number[];
}

export interface ChartData {
  labels: string[];
  datasets: {
    label: string;
    data: number[];
    borderColor: string;
    backgroundColor: string;
    tension: number;
  }[];
}

export interface TrendAnalysis {
  topic: string;
  trend: 'improving' | 'stable' | 'declining';
  improvement_rate: number;
  predicted_completion: string;
  recommendations: string[];
}

export class ComparisonService {
  /**
   * Récupère la comparaison avant/après du progrès
   */
  static async getProgressComparison(
    token: string,
    studentId: number,
    daysBack: number = 30
  ): Promise<ProgressComparison[]> {
    try {
      const response = await fetch(
        `${API_BASE_URL}/api/v1/remediation/comparison/student/${studentId}?days_back=${daysBack}`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error('Erreur lors de la récupération de la comparaison');
      }

      const comparison = await response.json();
      console.log('✅ [COMPARISON] Comparaison récupérée:', comparison);
      return comparison;
    } catch (error) {
      console.error('❌ [COMPARISON] Erreur récupération comparaison:', error);
      return [];
    }
  }

  /**
   * Récupère l'historique détaillé du progrès pour les graphiques
   */
  static async getProgressHistory(
    token: string,
    studentId: number,
    topic: string,
    daysBack: number = 90
  ): Promise<ComparisonData | null> {
    try {
      const response = await fetch(
        `${API_BASE_URL}/api/v1/remediation/results/student/${studentId}?topic=${topic}&limit=1000`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error('Erreur lors de la récupération de l\'historique');
      }

      const results = await response.json();
      
      // Grouper par date et calculer les moyennes
      const groupedByDate: { [key: string]: any[] } = {};
      
      results.forEach((result: any) => {
        const date = new Date(result.completed_at).toISOString().split('T')[0];
        if (!groupedByDate[date]) {
          groupedByDate[date] = [];
        }
        groupedByDate[date].push(result);
      });

      // Trier les dates et calculer les métriques
      const sortedDates = Object.keys(groupedByDate).sort();
      const levels: number[] = [];
      const successRates: number[] = [];
      const exerciseCounts: number[] = [];
      const improvements: number[] = [];

      let previousLevel = 0;
      
      sortedDates.forEach(date => {
        const dayResults = groupedByDate[date];
        const avgSuccessRate = dayResults.reduce((sum, r) => sum + r.percentage, 0) / dayResults.length;
        const currentLevel = Math.floor(avgSuccessRate / 10);
        const improvement = currentLevel - previousLevel;
        
        levels.push(currentLevel);
        successRates.push(avgSuccessRate);
        exerciseCounts.push(dayResults.length);
        improvements.push(improvement);
        
        previousLevel = currentLevel;
      });

      return {
        topic,
        dates: sortedDates,
        levels,
        successRates,
        exerciseCounts,
        improvements
      };
    } catch (error) {
      console.error('❌ [COMPARISON] Erreur récupération historique:', error);
      return null;
    }
  }

  /**
   * Génère les données pour les graphiques de comparaison
   */
  static generateComparisonCharts(
    comparisonData: ComparisonData,
    type: 'levels' | 'success_rates' | 'exercise_counts' | 'improvements'
  ): ChartData {
    const dataMap = {
      levels: comparisonData.levels,
      success_rates: comparisonData.successRates,
      exercise_counts: comparisonData.exerciseCounts,
      improvements: comparisonData.improvements
    };

    const labelMap = {
      levels: 'Niveau',
      success_rates: 'Taux de Réussite (%)',
      exercise_counts: 'Nombre d\'Exercices',
      improvements: 'Amélioration'
    };

    const colorMap = {
      levels: '#3B82F6',
      success_rates: '#10B981',
      exercise_counts: '#F59E0B',
      improvements: '#EF4444'
    };

    return {
      labels: comparisonData.dates.map(date => new Date(date).toLocaleDateString('fr-FR')),
      datasets: [
        {
          label: labelMap[type],
          data: dataMap[type],
          borderColor: colorMap[type],
          backgroundColor: `${colorMap[type]}20`,
          tension: 0.4
        }
      ]
    };
  }

  /**
   * Génère un graphique de comparaison avant/après
   */
  static generateBeforeAfterChart(
    comparisons: ProgressComparison[]
  ): ChartData {
    const topics = comparisons.map(c => c.topic);
    const beforeLevels = comparisons.map(c => c.before.current_level);
    const afterLevels = comparisons.map(c => c.after.current_level);

    return {
      labels: topics,
      datasets: [
        {
          label: 'Avant',
          data: beforeLevels,
          borderColor: '#EF4444',
          backgroundColor: '#EF444420',
          tension: 0.1
        },
        {
          label: 'Après',
          data: afterLevels,
          borderColor: '#10B981',
          backgroundColor: '#10B98120',
          tension: 0.1
        }
      ]
    };
  }

  /**
   * Génère un graphique de progression temporelle
   */
  static generateTimelineChart(
    comparisonData: ComparisonData
  ): ChartData {
    return {
      labels: comparisonData.dates.map(date => new Date(date).toLocaleDateString('fr-FR')),
      datasets: [
        {
          label: 'Niveau',
          data: comparisonData.levels,
          borderColor: '#3B82F6',
          backgroundColor: '#3B82F620',
          tension: 0.4
        },
        {
          label: 'Taux de Réussite (%)',
          data: comparisonData.successRates.map(rate => rate / 10), // Normaliser pour l'affichage
          borderColor: '#10B981',
          backgroundColor: '#10B98120',
          tension: 0.4
        }
      ]
    };
  }

  /**
   * Génère un graphique radar pour comparer les domaines
   */
  static generateRadarChart(
    comparisons: ProgressComparison[]
  ): ChartData {
    const topics = comparisons.map(c => c.topic);
    const improvementRates = comparisons.map(c => c.improvement_percentage);

    return {
      labels: topics,
      datasets: [
        {
          label: 'Taux d\'Amélioration (%)',
          data: improvementRates,
          borderColor: '#8B5CF6',
          backgroundColor: '#8B5CF620',
          tension: 0.1
        }
      ]
    };
  }

  /**
   * Analyse les tendances de progression
   */
  static analyzeTrends(
    comparisonData: ComparisonData
  ): TrendAnalysis {
    const recentLevels = comparisonData.levels.slice(-7); // 7 derniers jours
    const olderLevels = comparisonData.levels.slice(-14, -7); // 7 jours précédents
    
    if (recentLevels.length === 0 || olderLevels.length === 0) {
      return {
        topic: comparisonData.topic,
        trend: 'stable',
        improvement_rate: 0,
        predicted_completion: 'N/A',
        recommendations: ['Continuez à pratiquer régulièrement']
      };
    }

    const recentAvg = recentLevels.reduce((sum, level) => sum + level, 0) / recentLevels.length;
    const olderAvg = olderLevels.reduce((sum, level) => sum + level, 0) / olderLevels.length;
    
    const improvement_rate = recentAvg - olderAvg;
    
    let trend: 'improving' | 'stable' | 'declining';
    if (improvement_rate > 0.5) {
      trend = 'improving';
    } else if (improvement_rate < -0.5) {
      trend = 'declining';
    } else {
      trend = 'stable';
    }

    // Prédire la date de complétion (niveau 7)
    const currentLevel = recentLevels[recentLevels.length - 1];
    const targetLevel = 7;
    const remainingLevels = Math.max(0, targetLevel - currentLevel);
    
    let predicted_completion = 'N/A';
    if (improvement_rate > 0) {
      const daysToComplete = Math.ceil(remainingLevels / improvement_rate);
      const completionDate = new Date();
      completionDate.setDate(completionDate.getDate() + daysToComplete);
      predicted_completion = completionDate.toLocaleDateString('fr-FR');
    }

    // Générer des recommandations
    const recommendations: string[] = [];
    
    if (trend === 'improving') {
      recommendations.push('Excellent ! Continuez sur cette lancée');
      recommendations.push('Augmentez progressivement la difficulté');
    } else if (trend === 'declining') {
      recommendations.push('Revenez aux bases pour consolider');
      recommendations.push('Pratiquez plus régulièrement');
      recommendations.push('Demandez de l\'aide si nécessaire');
    } else {
      recommendations.push('Variez les types d\'exercices');
      recommendations.push('Fixez-vous des objectifs plus précis');
    }

    if (currentLevel < 4) {
      recommendations.push('Concentrez-vous sur les fondamentaux');
    } else if (currentLevel < 6) {
      recommendations.push('Pratiquez les exercices intermédiaires');
    } else {
      recommendations.push('Vous êtes proche de la maîtrise !');
    }

    return {
      topic: comparisonData.topic,
      trend,
      improvement_rate,
      predicted_completion,
      recommendations
    };
  }

  /**
   * Calcule les statistiques de comparaison
   */
  static calculateComparisonStats(
    comparisons: ProgressComparison[]
  ): {
    totalImprovement: number;
    averageImprovement: number;
    bestTopic: string;
    worstTopic: string;
    overallTrend: string;
  } {
    if (comparisons.length === 0) {
      return {
        totalImprovement: 0,
        averageImprovement: 0,
        bestTopic: 'N/A',
        worstTopic: 'N/A',
        overallTrend: 'stable'
      };
    }

    const totalImprovement = comparisons.reduce((sum, c) => sum + c.improvement_percentage, 0);
    const averageImprovement = totalImprovement / comparisons.length;
    
    const bestTopic = comparisons.reduce((best, current) => 
      current.improvement_percentage > best.improvement_percentage ? current : best
    ).topic;
    
    const worstTopic = comparisons.reduce((worst, current) => 
      current.improvement_percentage < worst.improvement_percentage ? worst : current
    ).topic;

    let overallTrend: string;
    if (averageImprovement > 10) {
      overallTrend = 'excellent';
    } else if (averageImprovement > 5) {
      overallTrend = 'bon';
    } else if (averageImprovement > 0) {
      overallTrend = 'stable';
    } else {
      overallTrend = 'à améliorer';
    }

    return {
      totalImprovement,
      averageImprovement,
      bestTopic,
      worstTopic,
      overallTrend
    };
  }

  /**
   * Exporte les données de comparaison en CSV
   */
  static exportComparisonToCSV(
    comparisons: ProgressComparison[]
  ): string {
    const headers = [
      'Domaine',
      'Niveau Avant',
      'Niveau Après',
      'Amélioration (%)',
      'Temps pour Améliorer (s)'
    ];

    const rows = comparisons.map(c => [
      c.topic,
      c.before.current_level,
      c.after.current_level,
      c.improvement_percentage.toFixed(2),
      c.time_to_improve || 'N/A'
    ]);

    const csvContent = [headers, ...rows]
      .map(row => row.map(cell => `"${cell}"`).join(','))
      .join('\n');

    return csvContent;
  }

  /**
   * Génère un rapport de comparaison complet
   */
  static generateComparisonReport(
    comparisons: ProgressComparison[],
    comparisonData: ComparisonData[]
  ): {
    summary: string;
    details: string[];
    charts: ChartData[];
    recommendations: string[];
  } {
    const stats = this.calculateComparisonStats(comparisons);
    
    const summary = `Rapport de Progression - ${new Date().toLocaleDateString('fr-FR')}
    
Tendance Globale: ${stats.overallTrend}
Amélioration Moyenne: ${stats.averageImprovement.toFixed(2)}%
Meilleur Domaine: ${stats.bestTopic}
Domaine à Améliorer: ${stats.worstTopic}`;

    const details = comparisons.map(c => 
      `${c.topic}: Niveau ${c.before.current_level} → ${c.after.current_level} (${c.improvement_percentage > 0 ? '+' : ''}${c.improvement_percentage.toFixed(1)}%)`
    );

    const charts = [
      this.generateBeforeAfterChart(comparisons),
      this.generateRadarChart(comparisons)
    ];

    const recommendations = [
      `Concentrez-vous sur ${stats.worstTopic} pour améliorer votre niveau global`,
      'Maintenez votre progression dans les domaines où vous excellez',
      'Pratiquez régulièrement pour consolider vos acquis',
      'Variez les types d\'exercices pour un apprentissage optimal'
    ];

    return {
      summary,
      details,
      charts,
      recommendations
    };
  }
}











