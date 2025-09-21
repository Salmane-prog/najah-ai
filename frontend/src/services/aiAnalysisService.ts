import { 
  TestResponse, 
  CompetencyAnalysis, 
  AIAnalysisResult,
  AdaptiveQuestion 
} from '../types/adaptiveEvaluation';

class AIAnalysisService {
  private readonly API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  // ============================================================================
  // ANALYSE DES COMPÉTENCES AVEC IA
  // ============================================================================

  async analyzeCompetencies(
    responses: TestResponse[],
    questions: AdaptiveQuestion[],
    studentId: number,
    testId: number
  ): Promise<AIAnalysisResult> {
    try {
      // Analyser les réponses pour identifier les patterns
      const responseAnalysis = this.analyzeResponsePatterns(responses, questions);
      
      // Calculer les niveaux de compétence
      const competencyLevels = this.calculateCompetencyLevels(responses, questions);
      
      // Générer des recommandations personnalisées
      const recommendations = this.generatePersonalizedRecommendations(
        competencyLevels,
        responseAnalysis
      );
      
      // Ajuster la difficulté pour les prochaines questions
      const difficultyAdjustment = this.calculateDifficultyAdjustment(
        competencyLevels,
        responseAnalysis
      );
      
      // Suggérer la prochaine question
      const nextQuestionSuggestion = this.suggestNextQuestion(
        questions,
        responses,
        competencyLevels
      );

      return {
        competencies: competencyLevels,
        learning_recommendations: recommendations,
        difficulty_adjustment: difficultyAdjustment,
        next_question_suggestion: nextQuestionSuggestion
      };
    } catch (error) {
      console.error('Erreur lors de l\'analyse IA:', error);
      throw error;
    }
  }

  // ============================================================================
  // ANALYSE DES PATTERNS DE RÉPONSES
  // ============================================================================

  private analyzeResponsePatterns(
    responses: TestResponse[], 
    questions: AdaptiveQuestion[]
  ) {
    const patterns = {
      responseTime: {
        fast: 0,    // < 30 secondes
        medium: 0,  // 30-60 secondes
        slow: 0     // > 60 secondes
      },
      difficultyProgression: {
        improving: 0,
        stable: 0,
        declining: 0
      },
      subjectStrengths: new Map<string, number>(),
      subjectWeaknesses: new Map<string, number>()
    };

    // Analyser les temps de réponse
    responses.forEach(response => {
      if (response.response_time < 30) patterns.responseTime.fast++;
      else if (response.response_time < 60) patterns.responseTime.medium++;
      else patterns.responseTime.slow++;
    });

    // Analyser la progression de difficulté
    let previousDifficulty = 0;
    let improvementCount = 0;
    let declineCount = 0;

    responses.forEach((response, index) => {
      const question = questions.find(q => q.id === response.question_id);
      if (question) {
        if (index > 0) {
          if (question.difficulty_level > previousDifficulty) {
            improvementCount++;
          } else if (question.difficulty_level < previousDifficulty) {
            declineCount++;
          }
        }
        previousDifficulty = question.difficulty_level;
      }
    });

    patterns.difficultyProgression.improving = improvementCount;
    patterns.difficultyProgression.declining = declineCount;
    patterns.difficultyProgression.stable = responses.length - improvementCount - declineCount;

    return patterns;
  }

  // ============================================================================
  // CALCUL DES NIVEAUX DE COMPÉTENCE
  // ============================================================================

  private calculateCompetencyLevels(
    responses: TestResponse[], 
    questions: AdaptiveQuestion[]
  ): CompetencyAnalysis[] {
    const competencyMap = new Map<string, {
      correct: number;
      total: number;
      totalTime: number;
      difficultyLevels: number[];
    }>();

    // Grouper les réponses par objectif d'apprentissage
    responses.forEach(response => {
      const question = questions.find(q => q.id === response.question_id);
      if (question && question.learning_objective) {
        const objective = question.learning_objective;
        const current = competencyMap.get(objective) || {
          correct: 0,
          total: 0,
          totalTime: 0,
          difficultyLevels: []
        };

        current.total++;
        current.totalTime += response.response_time;
        current.difficultyLevels.push(question.difficulty_level);

        if (this.isCorrectAnswer(response.answer, question)) {
          current.correct++;
        }

        competencyMap.set(objective, current);
      }
    });

    // Calculer les niveaux de compétence
    const competencies: CompetencyAnalysis[] = [];
    
    competencyMap.forEach((data, objective) => {
      const accuracy = (data.correct / data.total) * 100;
      const avgTime = data.totalTime / data.total;
      const avgDifficulty = data.difficultyLevels.reduce((a, b) => a + b, 0) / data.difficultyLevels.length;
      
      // Algorithme de calcul du niveau de compétence
      let competencyLevel = this.calculateCompetencyScore(accuracy, avgTime, avgDifficulty);
      let confidenceScore = this.calculateConfidenceScore(data.total, accuracy);
      
      // Générer des recommandations spécifiques
      const recommendations = this.generateCompetencyRecommendations(
        objective,
        competencyLevel,
        accuracy,
        avgTime
      );

      competencies.push({
        id: Date.now() + Math.random(), // ID temporaire
        attempt_id: 0, // Sera défini par l'appelant
        student_id: 0, // Sera défini par l'appelant
        test_id: 0,    // Sera défini par l'appelant
        competency_name: objective,
        competency_level: competencyLevel,
        confidence_score: confidenceScore,
        ai_recommendations: recommendations,
        analyzed_at: new Date().toISOString()
      });
    });

    return competencies;
  }

  private calculateCompetencyScore(accuracy: number, avgTime: number, avgDifficulty: number): number {
    // Score de base basé sur la précision
    let score = accuracy;
    
    // Bonus/malus pour le temps de réponse
    if (avgTime < 30) score += 10;      // Réponses rapides = bonus
    else if (avgTime > 90) score -= 15; // Réponses lentes = malus
    
    // Bonus/malus pour la difficulté
    if (avgDifficulty > 7) score += 15; // Questions difficiles réussies = bonus
    else if (avgDifficulty < 3) score -= 10; // Questions faciles échouées = malus
    
    // Limiter le score entre 0 et 100
    return Math.max(0, Math.min(100, score));
  }

  private calculateConfidenceScore(totalQuestions: number, accuracy: number): number {
    // Plus il y a de questions, plus la confiance est élevée
    const questionConfidence = Math.min(100, (totalQuestions / 5) * 20);
    
    // La précision influence aussi la confiance
    const accuracyConfidence = accuracy;
    
    // Moyenne pondérée
    return Math.round((questionConfidence * 0.3) + (accuracyConfidence * 0.7));
  }

  // ============================================================================
  // GÉNÉRATION DE RECOMMANDATIONS PERSONNALISÉES
  // ============================================================================

  private generatePersonalizedRecommendations(
    competencies: CompetencyAnalysis[],
    patterns: any
  ): string[] {
    const recommendations: string[] = [];
    
    // Recommandations basées sur les compétences
    competencies.forEach(competency => {
      if (competency.competency_level < 40) {
        recommendations.push(
          `${competency.competency_name} : Niveau faible détecté. Recommandation : révision complète des bases avec des exercices progressifs.`
        );
      } else if (competency.competency_level < 70) {
        recommendations.push(
          `${competency.competency_name} : Niveau intermédiaire. Recommandation : pratique ciblée sur les points faibles identifiés.`
        );
      } else {
        recommendations.push(
          `${competency.competency_name} : Niveau élevé. Recommandation : consolidation et défi avec des exercices avancés.`
        );
      }
    });

    // Recommandations basées sur les patterns
    if (patterns.responseTime.slow > patterns.responseTime.fast) {
      recommendations.push(
        "Temps de réponse élevé détecté. Recommandation : exercices de rapidité et gestion du stress."
      );
    }

    if (patterns.difficultyProgression.declining > patterns.difficultyProgression.improving) {
      recommendations.push(
        "Progression en difficulté en baisse. Recommandation : révision des concepts précédents avant d'augmenter la difficulté."
      );
    }

    return recommendations;
  }

  // ============================================================================
  // CALCUL D'AJUSTEMENT DE DIFFICULTÉ
  // ============================================================================

  private calculateDifficultyAdjustment(
    competencies: CompetencyAnalysis[],
    patterns: any
  ): number {
    const avgCompetency = competencies.reduce((sum, c) => sum + c.competency_level, 0) / competencies.length;
    
    let adjustment = 0;
    
    // Ajustement basé sur le niveau de compétence moyen
    if (avgCompetency > 80) {
      adjustment = 2; // Augmenter la difficulté
    } else if (avgCompetency < 40) {
      adjustment = -2; // Diminuer la difficulté
    } else if (avgCompetency < 60) {
      adjustment = -1; // Légèrement diminuer
    } else {
      adjustment = 1; // Légèrement augmenter
    }
    
    // Ajustement basé sur les patterns
    if (patterns.difficultyProgression.improving > patterns.difficultyProgression.declining) {
      adjustment += 1; // L'étudiant progresse bien
    } else if (patterns.difficultyProgression.declining > patterns.difficultyProgression.improving) {
      adjustment -= 1; // L'étudiant a des difficultés
    }
    
    // Limiter l'ajustement entre -3 et +3
    return Math.max(-3, Math.min(3, adjustment));
  }

  // ============================================================================
  // SUGGESTION DE LA PROCHAINE QUESTION
  // ============================================================================

  private suggestNextQuestion(
    questions: AdaptiveQuestion[],
    responses: TestResponse[],
    competencies: CompetencyAnalysis[]
  ): number {
    const answeredQuestionIds = responses.map(r => r.question_id);
    const unansweredQuestions = questions.filter(q => !answeredQuestionIds.includes(q.id));
    
    if (unansweredQuestions.length === 0) return -1; // Toutes les questions ont été répondues
    
    // Calculer le niveau de difficulté optimal
    const avgCompetency = competencies.reduce((sum, c) => sum + c.competency_level, 0) / competencies.length;
    const targetDifficulty = Math.max(1, Math.min(10, Math.round(avgCompetency / 10)));
    
    // Trouver la question la plus proche du niveau cible
    let bestQuestion = unansweredQuestions[0];
    let bestScore = Math.abs(bestQuestion.difficulty_level - targetDifficulty);
    
    unansweredQuestions.forEach(question => {
      const score = Math.abs(question.difficulty_level - targetDifficulty);
      if (score < bestScore) {
        bestScore = score;
        bestQuestion = question;
      }
    });
    
    return bestQuestion.id;
  }

  // ============================================================================
  // UTILITAIRES
  // ============================================================================

  private isCorrectAnswer(studentAnswer: string, question: AdaptiveQuestion): boolean {
    // Normaliser les réponses pour la comparaison
    const normalizedStudent = studentAnswer.toLowerCase().trim();
    const normalizedCorrect = question.correct_answer.toLowerCase().trim();
    
    return normalizedStudent === normalizedCorrect;
  }

  // ============================================================================
  // ANALYSE AVANCÉE AVEC MACHINE LEARNING (SIMULATION)
  // ============================================================================

  async performAdvancedAnalysis(
    studentId: number,
    testHistory: any[]
  ): Promise<{
    learningStyle: string;
    optimalStudyTime: string;
    recommendedBreaks: number;
    predictedPerformance: number;
  }> {
    // Simulation d'analyse ML avancée
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          learningStyle: this.determineLearningStyle(testHistory),
          optimalStudyTime: this.calculateOptimalStudyTime(testHistory),
          recommendedBreaks: this.calculateRecommendedBreaks(testHistory),
          predictedPerformance: this.predictPerformance(testHistory)
        });
      }, 2000);
    });
  }

  private determineLearningStyle(testHistory: any[]): string {
    const styles = ['visuel', 'auditif', 'kinesthésique', 'lecture-écriture'];
    return styles[Math.floor(Math.random() * styles.length)];
  }

  private calculateOptimalStudyTime(testHistory: any[]): string {
    const times = ['30 minutes', '45 minutes', '1 heure', '1h30'];
    return times[Math.floor(Math.random() * times.length)];
  }

  private calculateRecommendedBreaks(testHistory: any[]): number {
    return Math.floor(Math.random() * 3) + 1; // 1-3 pauses
  }

  private predictPerformance(testHistory: any[]): number {
    return Math.floor(Math.random() * 40) + 60; // 60-100%
  }
}

export const aiAnalysisService = new AIAnalysisService();




















