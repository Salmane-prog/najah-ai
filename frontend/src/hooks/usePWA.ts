import { useState, useEffect } from 'react';

interface PWAState {
  isInstalled: boolean;
  isOnline: boolean;
  isStandalone: boolean;
  canInstall: boolean;
  installPrompt: any;
}

export function usePWA() {
  const [pwaState, setPwaState] = useState<PWAState>({
    isInstalled: false,
    isOnline: navigator.onLine,
    isStandalone: window.matchMedia('(display-mode: standalone)').matches,
    canInstall: false,
    installPrompt: null
  });

  useEffect(() => {
    // Vérifier si l'app est installée
    const checkInstallation = () => {
      const isInstalled = window.matchMedia('(display-mode: standalone)').matches ||
                         (window.navigator as any).standalone === true;
      
      setPwaState(prev => ({ ...prev, isInstalled }));
    };

    // Gérer la connectivité
    const handleOnline = () => setPwaState(prev => ({ ...prev, isOnline: true }));
    const handleOffline = () => setPwaState(prev => ({ ...prev, isOnline: false }));

    // Gérer l'installation
    const handleBeforeInstallPrompt = (e: Event) => {
      e.preventDefault();
      setPwaState(prev => ({ 
        ...prev, 
        canInstall: true, 
        installPrompt: e 
      }));
    };

    // Gérer l'installation terminée
    const handleAppInstalled = () => {
      setPwaState(prev => ({ 
        ...prev, 
        isInstalled: true, 
        canInstall: false, 
        installPrompt: null 
      }));
    };

    // Écouter les événements
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    window.addEventListener('appinstalled', handleAppInstalled);

    // Vérifier l'installation initiale
    checkInstallation();

    // Enregistrer le service worker
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/sw.js')
        .then((registration) => {
          console.log('Service Worker enregistré:', registration);
        })
        .catch((error) => {
          console.error('Erreur d\'enregistrement du Service Worker:', error);
        });
    }

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
      window.removeEventListener('appinstalled', handleAppInstalled);
    };
  }, []);

  // Fonction pour installer l'app
  const installApp = async () => {
    if (pwaState.installPrompt) {
      const result = await pwaState.installPrompt.prompt();
      console.log('Résultat de l\'installation:', result);
      
      if (result.outcome === 'accepted') {
        setPwaState(prev => ({ 
          ...prev, 
          isInstalled: true, 
          canInstall: false, 
          installPrompt: null 
        }));
      }
    }
  };

  // Fonction pour demander les permissions de notification
  const requestNotificationPermission = async () => {
    if ('Notification' in window) {
      const permission = await Notification.requestPermission();
      return permission === 'granted';
    }
    return false;
  };

  // Fonction pour envoyer une notification
  const sendNotification = (title: string, options?: NotificationOptions) => {
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification(title, {
        icon: '/icon-192x192.png',
        badge: '/icon-192x192.png',
        ...options
      });
    }
  };

  // Fonction pour synchroniser les données
  const syncData = async () => {
    if ('serviceWorker' in navigator && 'sync' in window.ServiceWorkerRegistration.prototype) {
      const registration = await navigator.serviceWorker.ready;
      await registration.sync.register('background-sync');
    }
  };

  return {
    ...pwaState,
    installApp,
    requestNotificationPermission,
    sendNotification,
    syncData
  };
} 