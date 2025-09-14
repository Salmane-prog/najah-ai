import { useState, useEffect, useCallback } from 'react';
import { useAuth } from './useAuth';

interface BadgeAwardResult {
  student_id: number;
  current_level: number;
  total_points: number;
  total_tests: number;
  test_breakdown: {
    quiz: number;
    adaptive: number;
    remediation: number;
    assessment: number;
  };
  badges_awarded: string[];
  message: string;
}

export function useAutoBadges() {
  const { user, token } = useAuth();
  const [isChecking, setIsChecking] = useState(false);
  const [lastCheckResult, setLastCheckResult] = useState<BadgeAwardResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const checkAndAwardBadges = useCallback(async () => {
    if (!user?.id || !token) {
      setError('Utilisateur non authentifié');
      return null;
    }

    setIsChecking(true);
    setError(null);

    try {
      const response = await fetch(`http://localhost:8000/api/v1/analytics/test/student/${user.id}/check-badges`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }

      const result: BadgeAwardResult = await response.json();
      setLastCheckResult(result);

      // Si des badges ont été attribués, afficher une notification
      if (result.badges_awarded.length > 0) {
        console.log(`🎉 ${result.badges_awarded.length} nouveau(x) badge(s) attribué(s) !`);
        
        // Optionnel : Afficher une notification toast
        if (typeof window !== 'undefined' && 'Notification' in window) {
          if (Notification.permission === 'granted') {
            new Notification('Nouveaux badges !', {
              body: `${result.badges_awarded.length} badge(s) attribué(s) automatiquement !`,
              icon: '/badges/notification-icon.png'
            });
          }
        }
      }

      return result;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erreur inconnue';
      setError(errorMessage);
      console.error('❌ Erreur lors de la vérification des badges:', err);
      return null;
    } finally {
      setIsChecking(false);
    }
  }, [user?.id, token]);

  // Vérifier automatiquement les badges au chargement et après certaines actions
  useEffect(() => {
    if (user?.id && token) {
      // Vérifier les badges au chargement initial
      checkAndAwardBadges();
    }
  }, [user?.id, token, checkAndAwardBadges]);

  // Fonction pour forcer la vérification (appelée après un quiz, test, etc.)
  const forceCheck = useCallback(() => {
    return checkAndAwardBadges();
  }, [checkAndAwardBadges]);

  return {
    checkAndAwardBadges,
    forceCheck,
    isChecking,
    lastCheckResult,
    error,
    hasNewBadges: lastCheckResult?.badges_awarded.length > 0,
    newBadgesCount: lastCheckResult?.badges_awarded.length || 0,
    currentLevel: lastCheckResult?.current_level || 0,
    totalPoints: lastCheckResult?.total_points || 0,
    totalTests: lastCheckResult?.total_tests || 0,
  };
}
