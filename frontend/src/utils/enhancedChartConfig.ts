// Configuration améliorée pour les graphiques Chart.js
export const EnhancedChartConfig = {
  // Palette de couleurs unifiée et harmonieuse
  colors: {
    primary: ['#3B82F6', '#2563EB', '#1D4ED8'],
    secondary: ['#8B5CF6', '#7C3AED', '#6D28D9'],
    success: ['#10B981', '#059669', '#047857'],
    warning: ['#F59E0B', '#D97706', '#B45309'],
    danger: ['#EF4444', '#DC2626', '#B91C1C'],
    info: ['#0EA5E9', '#0284C7', '#0369A1'],
    neutral: ['#737373', '#525252', '#404040']
  },

  // Styles de graphiques améliorés
  elements: {
    line: {
      tension: 0.4,
      borderWidth: 3,
      fill: true,
      backgroundColor: 'rgba(59, 130, 246, 0.1)',
      borderColor: '#3B82F6'
    },
    point: {
      radius: 6,
      hoverRadius: 8,
      backgroundColor: '#3B82F6',
      borderColor: '#ffffff',
      borderWidth: 2,
      hoverBorderWidth: 3
    },
    bar: {
      backgroundColor: 'rgba(59, 130, 246, 0.8)',
      borderColor: '#3B82F6',
      borderWidth: 1,
      borderRadius: 4,
      hoverBackgroundColor: 'rgba(59, 130, 246, 1)'
    }
  },

  // Animations plus fluides
  animation: {
    duration: 2000,
    easing: 'easeInOutQuart'
  },

  // Options communes pour tous les graphiques
  common: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: {
          font: {
            family: 'Inter, -apple-system, BlinkMacSystemFont, sans-serif',
            size: 12,
            weight: '600'
          },
          padding: 20,
          usePointStyle: true,
          pointStyle: 'circle'
        }
      },
      tooltip: {
        backgroundColor: 'rgba(17, 24, 39, 0.95)',
        titleColor: '#ffffff',
        bodyColor: '#e5e7eb',
        borderColor: '#374151',
        borderWidth: 1,
        cornerRadius: 8,
        displayColors: true,
        padding: 12,
        titleFont: {
          size: 14,
          weight: '600'
        },
        bodyFont: {
          size: 13
        }
      }
    }
  },

  // Configuration spécifique pour les graphiques en ligne
  line: {
    scales: {
      x: {
        grid: {
          color: 'rgba(156, 163, 175, 0.1)',
          lineWidth: 1
        },
        ticks: {
          color: '#6B7280',
          font: {
            size: 11
          }
        }
      },
      y: {
        grid: {
          color: 'rgba(156, 163, 175, 0.1)',
          lineWidth: 1
        },
        ticks: {
          color: '#6B7280',
          font: {
            size: 11
          }
        }
      }
    }
  },

  // Configuration pour les graphiques en barres
  bar: {
    scales: {
      x: {
        grid: {
          display: false
        },
        ticks: {
          color: '#6B7280',
          font: {
            size: 11
          }
        }
      },
      y: {
        grid: {
          color: 'rgba(156, 163, 175, 0.1)',
          lineWidth: 1
        },
        ticks: {
          color: '#6B7280',
          font: {
            size: 11
          }
        }
      }
    }
  },

  // Configuration pour les graphiques circulaires
  doughnut: {
    cutout: '65%',
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          padding: 20,
          usePointStyle: true,
          pointStyle: 'circle'
        }
      }
    }
  },

  // Méthode getConfig pour créer la configuration des graphiques
  getConfig: (chartType: string, data: any) => {
    const baseConfig = {
      type: chartType === 'performance' || chartType === 'progression' ? 'line' : 'bar',
      data: {
        labels: data?.labels || [],
        datasets: data?.datasets || []
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: 'top' as const
          },
          tooltip: {
            enabled: true
          }
        },
        scales: {
          x: {
            display: true,
            grid: {
              display: false
            }
          },
          y: {
            display: true,
            grid: {
              color: 'rgba(156, 163, 175, 0.1)'
            },
            beginAtZero: true
          }
        }
      }
    };

    // Configuration spécifique selon le type de graphique
    if (chartType === 'performance' || chartType === 'progression') {
      baseConfig.type = 'line';
      baseConfig.data.datasets = baseConfig.data.datasets.map((dataset: any) => ({
        ...dataset,
        borderColor: '#3B82F6',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.4,
        fill: true
      }));
    } else if (chartType === 'matieres') {
      baseConfig.type = 'bar';
      baseConfig.data.datasets = baseConfig.data.datasets.map((dataset: any) => ({
        ...dataset,
        backgroundColor: '#8B5CF6',
        borderRadius: 4
      }));
    } else if (chartType === 'gamification') {
      baseConfig.type = 'doughnut';
      baseConfig.options.plugins.legend.position = 'bottom';
    }

    return baseConfig;
  }
};

// Fonction pour créer des graphiques avec configuration améliorée
export const createEnhancedChart = (ctx: CanvasRenderingContext2D, config: any) => {
  return {
    ...config,
    options: {
      ...EnhancedChartConfig.common,
      ...config.options,
      animation: {
        ...EnhancedChartConfig.animation,
        ...config.options?.animation
      }
    }
  };
};
