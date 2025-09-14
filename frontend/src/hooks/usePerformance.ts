import { useState, useEffect, useCallback } from 'react';

interface PerformanceMetrics {
  loadTime: number;
  memoryUsage: number;
  cpuUsage: number;
  networkSpeed: number;
  cacheHitRate: number;
  offlineCapability: boolean;
}

interface PerformanceOptimizations {
  enableLazyLoading: boolean;
  enableImageOptimization: boolean;
  enableCodeSplitting: boolean;
  enableServiceWorker: boolean;
  enableCompression: boolean;
}

export function usePerformance() {
  const [metrics, setMetrics] = useState<PerformanceMetrics>({
    loadTime: 0,
    memoryUsage: 0,
    cpuUsage: 0,
    networkSpeed: 0,
    cacheHitRate: 0,
    offlineCapability: false
  });

  const [optimizations, setOptimizations] = useState<PerformanceOptimizations>({
    enableLazyLoading: true,
    enableImageOptimization: true,
    enableCodeSplitting: true,
    enableServiceWorker: true,
    enableCompression: true
  });

  const [isOptimizing, setIsOptimizing] = useState(false);

  // Mesurer les performances de base
  const measurePerformance = useCallback(() => {
    if (typeof window !== 'undefined' && 'performance' in window) {
      const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
      const loadTime = navigation.loadEventEnd - navigation.loadEventStart;
      
      // Simuler d'autres métriques (dans un vrai système, utiliser des APIs spécifiques)
      const memoryUsage = (performance as any).memory?.usedJSHeapSize / 1024 / 1024 || 0;
      const cpuUsage = Math.random() * 100; // Simulation
      const networkSpeed = navigator.connection?.effectiveType === '4g' ? 100 : 50; // Simulation
      
      setMetrics({
        loadTime,
        memoryUsage: Math.round(memoryUsage * 100) / 100,
        cpuUsage: Math.round(cpuUsage * 100) / 100,
        networkSpeed,
        cacheHitRate: Math.random() * 100, // Simulation
        offlineCapability: 'serviceWorker' in navigator
      });
    }
  }, []);

  // Optimiser les images
  const optimizeImages = useCallback(async () => {
    if (!optimizations.enableImageOptimization) return;

    try {
      const images = document.querySelectorAll('img');
      images.forEach((img) => {
        // Ajouter lazy loading
        if (!img.loading) {
          img.loading = 'lazy';
        }
        
        // Optimiser la taille si possible
        if (img.width > 800) {
          img.style.maxWidth = '100%';
          img.style.height = 'auto';
        }
      });
    } catch (error) {
      console.error('Erreur lors de l\'optimisation des images:', error);
    }
  }, [optimizations.enableImageOptimization]);

  // Optimiser le cache
  const optimizeCache = useCallback(async () => {
    if (!optimizations.enableServiceWorker) return;

    try {
      if ('caches' in window) {
        const cacheNames = await caches.keys();
        const cacheToKeep = ['najah-ai-v1'];
        
        // Nettoyer les anciens caches
        for (const cacheName of cacheNames) {
          if (!cacheToKeep.includes(cacheName)) {
            await caches.delete(cacheName);
          }
        }
      }
    } catch (error) {
      console.error('Erreur lors de l\'optimisation du cache:', error);
    }
  }, [optimizations.enableServiceWorker]);

  // Optimiser la mémoire
  const optimizeMemory = useCallback(() => {
    try {
      // Forcer le garbage collection si disponible
      if ('gc' in window) {
        (window as any).gc();
      }
      
      // Nettoyer les event listeners non utilisés
      // (dans un vrai système, maintenir une liste des listeners)
    } catch (error) {
      console.error('Erreur lors de l\'optimisation mémoire:', error);
    }
  }, []);

  // Optimisation complète
  const performOptimization = useCallback(async () => {
    setIsOptimizing(true);
    
    try {
      await Promise.all([
        optimizeImages(),
        optimizeCache(),
        optimizeMemory()
      ]);
      
      // Remesurer les performances après optimisation
      setTimeout(() => {
        measurePerformance();
        setIsOptimizing(false);
      }, 1000);
      
    } catch (error) {
      console.error('Erreur lors de l\'optimisation:', error);
      setIsOptimizing(false);
    }
  }, [optimizeImages, optimizeCache, optimizeMemory, measurePerformance]);

  // Précharger les ressources importantes
  const preloadResources = useCallback(() => {
    try {
      const criticalResources = [
        '/dashboard/student',
        '/dashboard/teacher',
        '/api/v1/auth/me'
      ];
      
      criticalResources.forEach(resource => {
        const link = document.createElement('link');
        link.rel = 'prefetch';
        link.href = resource;
        document.head.appendChild(link);
      });
    } catch (error) {
      console.error('Erreur lors du préchargement:', error);
    }
  }, []);

  // Surveiller les performances en temps réel
  useEffect(() => {
    const measureInterval = setInterval(measurePerformance, 30000); // Toutes les 30 secondes
    
    return () => clearInterval(measureInterval);
  }, [measurePerformance]);

  // Mesurer les performances au chargement initial
  useEffect(() => {
    measurePerformance();
    preloadResources();
  }, [measurePerformance, preloadResources]);

  // Optimisations automatiques basées sur les métriques
  useEffect(() => {
    if (metrics.memoryUsage > 100) { // Plus de 100MB
      optimizeMemory();
    }
    
    if (metrics.loadTime > 3000) { // Plus de 3 secondes
      performOptimization();
    }
  }, [metrics, optimizeMemory, performOptimization]);

  return {
    metrics,
    optimizations,
    isOptimizing,
    measurePerformance,
    performOptimization,
    setOptimizations,
    optimizeImages,
    optimizeCache,
    optimizeMemory,
    preloadResources
  };
} 