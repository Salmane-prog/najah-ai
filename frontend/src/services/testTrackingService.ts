import { TestPerformance, StudentPerformance } from '@/types/analytics';

interface TestAttempt {
  id: string;
  testId: number;
  studentId: number;
  studentName: string;
  startTime: Date;
  endTime?: Date;
  score?: number;
  questionsAnswered: number;
  totalQuestions: number;
  timeSpent: number;
  status: 'in_progress' | 'completed' | 'abandoned';
}

interface TestSession {
  testId: number;
  testTitle: string;
  activeStudents: number;
  averageTimeSpent: number;
  completionRate: number;
  lastActivity: Date;
}

class TestTrackingService {
  private baseUrl = 'http://localhost:8000/api/v1';
  private activeSessions = new Map<number, TestSession>();
  private testAttempts = new Map<string, TestAttempt>();
  private listeners: Array<(data: any) => void> = [];

  // Démarrer un test pour un étudiant
  async startTest(testId: number, studentId: number, studentName: string): Promise<string> {
    const attemptId = `attempt_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    const attempt: TestAttempt = {
      id: attemptId,
      testId,
      studentId,
      studentName,
      startTime: new Date(),
      questionsAnswered: 0,
      totalQuestions: 0,
      timeSpent: 0,
      status: 'in_progress'
    };

    this.testAttempts.set(attemptId, attempt);
    
    // Mettre à jour la session active
    this.updateActiveSession(testId, studentName);
    
    // Envoyer au backend
    await this.sendTestStartToBackend(attempt);
    
    console.log(`🚀 Test démarré: ${studentName} - Test ID: ${testId}`);
    return attemptId;
  }

  // Mettre à jour le progrès d'un test
  async updateProgress(attemptId: string, questionsAnswered: number, totalQuestions: number): Promise<void> {
    const attempt = this.testAttempts.get(attemptId);
    if (!attempt) {
      throw new Error('Tentative de test non trouvée');
    }

    attempt.questionsAnswered = questionsAnswered;
    attempt.totalQuestions = totalQuestions;
    attempt.timeSpent = Date.now() - attempt.startTime.getTime();

    // Mettre à jour la session active
    this.updateActiveSession(attempt.testId, attempt.studentName);

    // Envoyer au backend
    await this.sendProgressToBackend(attempt);
    
    console.log(`📊 Progrès mis à jour: ${attempt.studentName} - ${questionsAnswered}/${totalQuestions}`);
  }

  // Terminer un test
  async completeTest(attemptId: string, score: number): Promise<void> {
    const attempt = this.testAttempts.get(attemptId);
    if (!attempt) {
      throw new Error('Tentative de test non trouvée');
    }

    attempt.endTime = new Date();
    attempt.score = score;
    attempt.status = 'completed';
    attempt.timeSpent = attempt.endTime.getTime() - attempt.startTime.getTime();

    // Mettre à jour la session active
    this.updateActiveSession(attempt.testId, attempt.studentName);

    // Envoyer au backend
    await this.sendTestCompletionToBackend(attempt);
    
    console.log(`✅ Test terminé: ${attempt.studentName} - Score: ${score}%`);
    
    // Notifier les listeners
    this.notifyListeners({
      type: 'test_completed',
      data: attempt
    });
  }

  // Abandonner un test
  async abandonTest(attemptId: string): Promise<void> {
    const attempt = this.testAttempts.get(attemptId);
    if (!attempt) {
      throw new Error('Tentative de test non trouvée');
    }

    attempt.endTime = new Date();
    attempt.status = 'abandoned';
    attempt.timeSpent = attempt.endTime.getTime() - attempt.startTime.getTime();

    // Envoyer au backend
    await this.sendTestAbandonToBackend(attempt);
    
    console.log(`❌ Test abandonné: ${attempt.studentName}`);
  }

  // Obtenir les sessions actives
  getActiveSessions(): TestSession[] {
    return Array.from(this.activeSessions.values());
  }

  // Obtenir les tentatives de test
  getTestAttempts(): TestAttempt[] {
    return Array.from(this.testAttempts.values());
  }

  // Obtenir les statistiques en temps réel
  getRealTimeStats(): {
    totalActiveTests: number;
    totalStudents: number;
    averageCompletionRate: number;
    recentCompletions: TestAttempt[];
  } {
    const activeTests = this.activeSessions.size;
    const totalStudents = Array.from(this.activeSessions.values())
      .reduce((sum, session) => sum + session.activeStudents, 0);
    
    const completedTests = Array.from(this.testAttempts.values())
      .filter(attempt => attempt.status === 'completed');
    
    const averageCompletionRate = completedTests.length > 0 
      ? (completedTests.length / this.testAttempts.size) * 100 
      : 0;

    const recentCompletions = completedTests
      .sort((a, b) => (b.endTime?.getTime() || 0) - (a.endTime?.getTime() || 0))
      .slice(0, 5);

    return {
      totalActiveTests: activeTests,
      totalStudents,
      averageCompletionRate,
      recentCompletions
    };
  }

  // S'abonner aux mises à jour
  subscribe(listener: (data: any) => void): () => void {
    this.listeners.push(listener);
    
    return () => {
      const index = this.listeners.indexOf(listener);
      if (index > -1) {
        this.listeners.splice(index, 1);
      }
    };
  }

  // Mettre à jour une session active
  private updateActiveSession(testId: number, studentName: string): void {
    const existingSession = this.activeSessions.get(testId);
    
    if (existingSession) {
      existingSession.activeStudents = Math.max(existingSession.activeStudents, 1);
      existingSession.lastActivity = new Date();
    } else {
      this.activeSessions.set(testId, {
        testId,
        testTitle: `Test ${testId}`,
        activeStudents: 1,
        averageTimeSpent: 0,
        completionRate: 0,
        lastActivity: new Date()
      });
    }
  }

  // Notifier les listeners
  private notifyListeners(data: any): void {
    this.listeners.forEach(listener => {
      try {
        listener(data);
      } catch (error) {
        console.error('❌ Erreur dans un listener:', error);
      }
    });
  }

  // Envoyer le démarrage du test au backend
  private async sendTestStartToBackend(attempt: TestAttempt): Promise<void> {
    try {
      const token = localStorage.getItem('najah_token');
      if (!token) return;

      await fetch(`${this.baseUrl}/test-tracking/start`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          attempt_id: attempt.id,
          test_id: attempt.testId,
          student_id: attempt.studentId,
          student_name: attempt.studentName,
          start_time: attempt.startTime.toISOString()
        }),
      });
    } catch (error) {
      console.error('❌ Erreur lors de l\'envoi du démarrage au backend:', error);
    }
  }

  // Envoyer le progrès au backend
  private async sendProgressToBackend(attempt: TestAttempt): Promise<void> {
    try {
      const token = localStorage.getItem('najah_token');
      if (!token) return;

      await fetch(`${this.baseUrl}/test-tracking/progress`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          attempt_id: attempt.id,
          questions_answered: attempt.questionsAnswered,
          total_questions: attempt.totalQuestions,
          time_spent: attempt.timeSpent
        }),
      });
    } catch (error) {
      console.error('❌ Erreur lors de l\'envoi du progrès au backend:', error);
    }
  }

  // Envoyer la completion au backend
  private async sendTestCompletionToBackend(attempt: TestAttempt): Promise<void> {
    try {
      const token = localStorage.getItem('najah_token');
      if (!token) return;

      await fetch(`${this.baseUrl}/test-tracking/complete`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          attempt_id: attempt.id,
          score: attempt.score,
          end_time: attempt.endTime?.toISOString(),
          time_spent: attempt.timeSpent,
          questions_answered: attempt.questionsAnswered,
          total_questions: attempt.totalQuestions
        }),
      });
    } catch (error) {
      console.error('❌ Erreur lors de l\'envoi de la completion au backend:', error);
    }
  }

  // Envoyer l'abandon au backend
  private async sendTestAbandonToBackend(attempt: TestAttempt): Promise<void> {
    try {
      const token = localStorage.getItem('najah_token');
      if (!token) return;

      await fetch(`${this.baseUrl}/test-tracking/abandon`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          attempt_id: attempt.id,
          end_time: attempt.endTime?.toISOString(),
          time_spent: attempt.timeSpent,
          questions_answered: attempt.questionsAnswered,
          total_questions: attempt.totalQuestions
        }),
      });
    } catch (error) {
      console.error('❌ Erreur lors de l\'envoi de l\'abandon au backend:', error);
    }
  }
}

export const testTrackingService = new TestTrackingService();


















