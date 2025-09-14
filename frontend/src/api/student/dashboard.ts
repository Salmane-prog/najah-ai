// Service d'API réel pour dashboard étudiant
// Appelle les endpoints FastAPI, nécessite le token JWT
import { ScoreCalculator } from '../../utils/scoreCalculator';

export async function fetchStudentDashboard(token: string, userId: number) {
  const API = 'http://localhost:8000/api/v1';
  const headers = { 'Authorization': `Bearer ${token}` };

  try {
    // Appels parallèles avec gestion d'erreurs améliorée
    const [quizResultsRes, analyticsRes, badgesRes, recosRes, learningRes, messagesRes, assignedQuizzesRes] = await Promise.all([
      fetch(`${API}/quiz_results/user/${userId}`, { headers }).catch(() => ({ ok: false, json: () => [] })),
      fetch(`${API}/ai/analytics/`, {
        method: 'POST',
        headers: { ...headers, 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId })
      }).catch(() => ({ ok: false, json: () => ({}) })),
      fetch(`${API}/badges/user/${userId}`, { headers }).catch(() => ({ ok: false, json: () => [] })),
      fetch(`${API}/ai/recommend/`, {
        method: 'POST',
        headers: { ...headers, 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId })
      }).catch(() => ({ ok: false, json: () => ({ recommendations: [] }) })),
      fetch(`${API}/learning_history/?student_id=${userId}`, { headers }).catch(() => ({ ok: false, json: () => [] })),
      fetch(`${API}/messages/user/${userId}`, { headers }).catch(() => ({ ok: false, json: () => [] })),
      fetch(`${API}/quizzes/assigned/?student_id=${userId}`, { headers }).catch(() => ({ ok: false, json: () => [] }))
    ]);

    // Récupération des données avec gestion d'erreurs robuste
    const quizResults = await (quizResultsRes.ok ? quizResultsRes.json() : []);
    const analytics = await (analyticsRes.ok ? analyticsRes.json() : ({}));
    const badges = await (badgesRes.ok ? badgesRes.json() : []);
    const recos = await (recosRes.ok ? recosRes.json() : ({ recommendations: [] }));
    const learningHistory = await (learningRes.ok ? learningRes.json() : []);
    const messages = await (messagesRes.ok ? messagesRes.json() : []);
    const assignedQuizzes = await (assignedQuizzesRes.ok ? assignedQuizzesRes.json() : []);

    // CORRECTION : Utilisation du ScoreCalculator pour des calculs corrects
    const stats = ScoreCalculator.calculateGlobalStats(quizResults);
    
    // Calcul correct de l'XP et progression
    const totalPoints = stats.totalPoints;
    const level = stats.level;
    const currentXp = totalPoints % 1000;
    const xpToNextLevel = 1000;
    const progressToNextLevel = ScoreCalculator.calculateXpProgress(currentXp, xpToNextLevel);

    // Mapping pour le front avec données corrigées
    return {
      stats: {
        totalQuizzes: stats.totalQuizzes,
        completedQuizzes: stats.completedQuizzes,
        averageScore: stats.averageScore, // CORRIGÉ : maintenant entre 0-100%
        currentStreak: 0, // À calculer si dispo
        totalPoints: totalPoints,
        level: level,
        xpToNextLevel: xpToNextLevel,
        currentXp: currentXp,
        rank: stats.rank,
        bestScore: stats.bestScore, // CORRIGÉ : maintenant entre 0-100%
      },
      availableQuizzes: [
        // Quiz assignés (à faire)
        ...(assignedQuizzes || []).map((qa: any) => {
          const quizData = qa.quiz || {};
          const questions = quizData.questions || [];
          
          return {
            id: quizData.id || qa.quiz_id || 0,
            title: quizData.title || 'Quiz sans titre',
            subject: quizData.subject || 'Général',
            level: quizData.level || 'medium',
            estimatedTime: quizData.time_limit || 15,
            questionsCount: questions.length || 0,
            isCompleted: false,
            score: 0,
            created_at: qa.assigned_at || new Date().toISOString(),
            isAssigned: true,
            dueDate: qa.due_date || undefined,
            assignmentId: qa.id || 0
          };
        }),
        // Quiz déjà complétés avec scores corrigés
        ...quizResults.filter(q => q.completed === true || q.completed === 1).map((q: any) => {
          const sanitizedData = ScoreCalculator.sanitizeScoreData(q);
          return {
            id: q.id || 0,
            title: q.title || q.sujet || 'Quiz sans titre',
            subject: q.sujet || 'Général',
            level: q.level || 'medium',
            estimatedTime: q.estimated_time || 15,
            questionsCount: q.questions_count || 0,
            isCompleted: q.completed === 1 || q.completed === true,
            score: sanitizedData.score, // CORRIGÉ
            percentage: sanitizedData.percentage, // CORRIGÉ
            created_at: q.created_at || new Date().toISOString(),
            isAssigned: false
          };
        })
      ],
      assignedQuizzes: (assignedQuizzes || []).map((qa: any) => {
        const quizData = qa.quiz || {};
        const questions = quizData.questions || [];
        
        return {
          id: quizData.id || qa.quiz_id || 0,
          title: quizData.title || 'Quiz sans titre',
          subject: quizData.subject || 'Général',
          level: quizData.level || 'medium',
          estimatedTime: quizData.time_limit || 15,
          questionsCount: questions.length || 0,
          assignedAt: qa.assigned_at || new Date().toISOString(),
          dueDate: qa.due_date || undefined,
          assignmentId: qa.id || 0
        };
      }),
      achievements: badges.map((b: any) => ({
        id: b.id,
        title: b.badge?.name || 'Badge',
        description: b.badge?.description || '',
        icon: b.badge?.icon || '🏆',
        isUnlocked: b.progression >= 1,
        progress: b.progression || 0,
        maxProgress: 1,
      })),
      recommendations: recos.recommendations?.map((r: any) => ({
        id: r.id,
        type: r.type,
        title: r.title || r.name,
        description: r.description || '',
        priority: 'medium',
        reason: '',
      })) || [],
      recentActivity: quizResults.slice(0, 5).map((q: any) => {
        const sanitizedData = ScoreCalculator.sanitizeScoreData(q);
        return {
          id: q.id,
          action: 'QCM complété',
          details: q.sujet,
          score: sanitizedData.percentage, // CORRIGÉ : maintenant entre 0-100%
          date: q.created_at?.split('T')[0],
        };
      }),
      skillRadar: {
        labels: ['Lecture', 'Analyse', 'Mémoire', 'Vocabulaire', 'Synthèse', 'Créativité'],
        data: [80, 70, 85, 60, 75, 90],
      },
      planning: learningHistory,
      messages: messages.slice(-5).reverse(),
      feedback: null, // À implémenter si nécessaire
    };
  } catch (error) {
    console.error('Erreur lors de la récupération des données du dashboard:', error);
    throw new Error('Erreur lors de la récupération des données du dashboard.');
  }
} 