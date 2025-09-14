// Service pour l'algorithme d'adaptation intelligent des tests
export interface StudentResponse {
  questionId: number;
  selectedAnswer: number;
  correctAnswer: number;
  timeSpent: number;
  difficulty: number;
  isCorrect: boolean;
}

export interface AdaptiveState {
  currentDifficulty: number;
  confidenceLevel: number;
  learningPattern: 'visual' | 'auditory' | 'kinesthetic' | 'mixed';
  strengthAreas: string[];
  weaknessAreas: string[];
  responseHistory: StudentResponse[];
  currentStreak: number;
  totalQuestions: number;
  correctAnswers: number;
}

export interface QuestionRecommendation {
  questionId: number;
  reason: string;
  expectedDifficulty: number;
  learningObjective: string;
  confidence: number;
}

export class AdaptiveAlgorithmEngine {
  private state: AdaptiveState;
  private questions: any[];
  private minDifficulty: number;
  private maxDifficulty: number;

  constructor(questions: any[], difficultyRange: [number, number]) {
    this.questions = questions;
    this.minDifficulty = difficultyRange[0];
    this.maxDifficulty = difficultyRange[1];
    
    this.state = {
      currentDifficulty: (difficultyRange[0] + difficultyRange[1]) / 2,
      confidenceLevel: 0.5,
      learningPattern: 'mixed',
      strengthAreas: [],
      weaknessAreas: [],
      responseHistory: [],
      currentStreak: 0,
      totalQuestions: 0,
      correctAnswers: 0
    };
  }

  // Analyse de la réponse et mise à jour de l'état
  public processResponse(response: StudentResponse): void {
    this.state.responseHistory.push(response);
    this.state.totalQuestions++;
    
    if (response.isCorrect) {
      this.state.correctAnswers++;
      this.state.currentStreak++;
    } else {
      this.state.currentStreak = 0;
    }

    // Mise à jour du niveau de confiance
    this.updateConfidenceLevel(response);
    
    // Analyse du pattern d'apprentissage
    this.analyzeLearningPattern(response);
    
    // Mise à jour des forces et faiblesses
    this.updateStrengthWeaknessAreas(response);
  }

  // Sélection intelligente de la prochaine question
  public selectNextQuestion(): QuestionRecommendation | null {
    const availableQuestions = this.getAvailableQuestions();
    
    if (availableQuestions.length === 0) {
      return null;
    }

    // Calcul de la difficulté cible
    const targetDifficulty = this.calculateTargetDifficulty();
    
    // Filtrage des questions par difficulté cible
    const suitableQuestions = availableQuestions.filter(q => 
      Math.abs(q.difficulty - targetDifficulty) <= 1
    );

    if (suitableQuestions.length === 0) {
      return availableQuestions[0];
    }

    // Sélection basée sur l'objectif d'apprentissage et la difficulté
    const selectedQuestion = this.selectOptimalQuestion(suitableQuestions);
    
    return {
      questionId: selectedQuestion.id,
      reason: this.generateSelectionReason(selectedQuestion),
      expectedDifficulty: selectedQuestion.difficulty,
      learningObjective: selectedQuestion.learningObjective,
      confidence: this.state.confidenceLevel
    };
  }

  // Ajustement de la difficulté en temps réel
  public adjustDifficulty(): number {
    const recentResponses = this.state.responseHistory.slice(-3);
    const recentCorrect = recentResponses.filter(r => r.isCorrect).length;
    
    let adjustment = 0;
    
    if (recentCorrect === 3) {
      // 3 bonnes réponses consécutives → augmenter la difficulté
      adjustment = 0.5;
    } else if (recentCorrect === 0) {
      // 3 mauvaises réponses consécutives → diminuer la difficulté
      adjustment = -0.5;
    } else if (recentCorrect === 1) {
      // 1 bonne réponse sur 3 → légère diminution
      adjustment = -0.2;
    } else if (recentCorrect === 2) {
      // 2 bonnes réponses sur 3 → légère augmentation
      adjustment = 0.2;
    }

    // Ajustement basé sur le streak
    if (this.state.currentStreak >= 5) {
      adjustment += 0.3;
    } else if (this.state.currentStreak <= -3) {
      adjustment -= 0.3;
    }

    // Limiter la difficulté dans la plage autorisée
    this.state.currentDifficulty = Math.max(
      this.minDifficulty,
      Math.min(this.maxDifficulty, this.state.currentDifficulty + adjustment)
    );

    return this.state.currentDifficulty;
  }

  // Analyse prédictive des performances
  public predictPerformance(): {
    expectedScore: number;
    confidence: number;
    recommendations: string[];
  } {
    const accuracy = this.state.correctAnswers / this.state.totalQuestions;
    const recentAccuracy = this.getRecentAccuracy();
    
    // Prédiction basée sur l'historique et la tendance récente
    let expectedScore = accuracy * 100;
    
    if (recentAccuracy > accuracy) {
      expectedScore += 5; // Amélioration récente
    } else if (recentAccuracy < accuracy) {
      expectedScore -= 5; // Dégradation récente
    }

    // Recommandations basées sur l'analyse
    const recommendations = this.generateRecommendations();

    return {
      expectedScore: Math.round(expectedScore),
      confidence: this.state.confidenceLevel,
      recommendations
    };
  }

  // Génération de feedback personnalisé
  public generatePersonalizedFeedback(): {
    message: string;
    suggestions: string[];
    nextSteps: string[];
  } {
    const performance = this.predictPerformance();
    
    let message = '';
    if (performance.expectedScore >= 80) {
      message = "Excellent travail ! Vous maîtrisez bien cette matière.";
    } else if (performance.expectedScore >= 60) {
      message = "Bon travail ! Continuez à vous exercer pour améliorer vos résultats.";
    } else {
      message = "Ne vous découragez pas ! Concentrez-vous sur les points à améliorer.";
    }

    const suggestions = this.generateSuggestions();
    const nextSteps = this.generateNextSteps();

    return { message, suggestions, nextSteps };
  }

  // Méthodes privées pour la logique interne
  private updateConfidenceLevel(response: StudentResponse): void {
    const baseAdjustment = response.isCorrect ? 0.05 : -0.08;
    
    // Ajustement basé sur le temps passé
    const timeAdjustment = this.calculateTimeAdjustment(response.timeSpent);
    
    // Ajustement basé sur la difficulté
    const difficultyAdjustment = this.calculateDifficultyAdjustment(response);
    
    const totalAdjustment = baseAdjustment + timeAdjustment + difficultyAdjustment;
    
    this.state.confidenceLevel = Math.max(0, Math.min(1, 
      this.state.confidenceLevel + totalAdjustment
    ));
  }

  private analyzeLearningPattern(response: StudentResponse): void {
    // Analyse basée sur le temps de réponse et la difficulté
    const responseTime = response.timeSpent;
    const difficulty = response.difficulty;
    
    if (responseTime < 10 && response.isCorrect) {
      // Réponse rapide et correcte → pattern visuel ou auditif
      if (this.state.learningPattern === 'mixed') {
        this.state.learningPattern = Math.random() > 0.5 ? 'visual' : 'auditory';
      }
    } else if (responseTime > 30 && !response.isCorrect) {
      // Réponse lente et incorrecte → pattern kinesthésique
      this.state.learningPattern = 'kinesthetic';
    }
  }

  private updateStrengthWeaknessAreas(response: StudentResponse): void {
    // Mise à jour des forces et faiblesses basée sur les réponses
    // Cette logique peut être étendue selon les besoins
  }

  private getAvailableQuestions(): any[] {
    const answeredIds = this.state.responseHistory.map(r => r.questionId);
    return this.questions.filter(q => !answeredIds.includes(q.id));
  }

  private calculateTargetDifficulty(): number {
    // Calcul de la difficulté cible basé sur l'état actuel
    let target = this.state.currentDifficulty;
    
    // Ajustement basé sur le niveau de confiance
    if (this.state.confidenceLevel > 0.7) {
      target += 0.5;
    } else if (this.state.confidenceLevel < 0.3) {
      target -= 0.5;
    }
    
    // Ajustement basé sur le streak
    if (this.state.currentStreak >= 3) {
      target += 0.3;
    } else if (this.state.currentStreak <= -2) {
      target -= 0.3;
    }
    
    return Math.max(this.minDifficulty, Math.min(this.maxDifficulty, target));
  }

  private selectOptimalQuestion(suitableQuestions: any[]): any {
    // Sélection optimale basée sur plusieurs critères
    let bestQuestion = suitableQuestions[0];
    let bestScore = 0;
    
    for (const question of suitableQuestions) {
      let score = 0;
      
      // Score basé sur la proximité de la difficulté cible
      const difficultyScore = 10 - Math.abs(question.difficulty - this.state.currentDifficulty);
      score += difficultyScore * 0.4;
      
      // Score basé sur l'objectif d'apprentissage
      if (!this.state.strengthAreas.includes(question.learningObjective)) {
        score += 0.3; // Priorité aux objectifs non maîtrisés
      }
      
      // Score basé sur le type de question
      if (question.type === 'multiple_choice') {
        score += 0.2;
      }
      
      if (score > bestScore) {
        bestScore = score;
        bestQuestion = question;
      }
    }
    
    return bestQuestion;
  }

  private generateSelectionReason(question: any): string {
    const reasons = [
      "Question sélectionnée pour renforcer vos compétences",
      "Adaptée à votre niveau actuel de difficulté",
      "Cible un objectif d'apprentissage important",
      "Basée sur votre pattern de réponses récentes",
      "Optimisée pour votre progression"
    ];
    
    return reasons[Math.floor(Math.random() * reasons.length)];
  }

  private getRecentAccuracy(): number {
    const recent = this.state.responseHistory.slice(-5);
    if (recent.length === 0) return 0;
    
    const correct = recent.filter(r => r.isCorrect).length;
    return correct / recent.length;
  }

  private calculateTimeAdjustment(timeSpent: number): number {
    if (timeSpent < 10) return 0.02; // Réponse rapide
    if (timeSpent > 60) return -0.03; // Réponse lente
    return 0; // Temps normal
  }

  private calculateDifficultyAdjustment(response: StudentResponse): number {
    if (response.isCorrect && response.difficulty >= this.state.currentDifficulty) {
      return 0.03; // Bonne réponse à une question difficile
    } else if (!response.isCorrect && response.difficulty <= this.state.currentDifficulty) {
      return -0.05; // Mauvaise réponse à une question facile
    }
    return 0;
  }

  private generateRecommendations(): string[] {
    const recommendations = [];
    
    if (this.state.confidenceLevel < 0.4) {
      recommendations.push("Concentrez-vous sur les bases avant de progresser");
    }
    
    if (this.state.currentStreak < -2) {
      recommendations.push("Prenez votre temps pour analyser chaque question");
    }
    
    if (this.state.learningPattern === 'kinesthetic') {
      recommendations.push("Essayez de visualiser les concepts abstraits");
    }
    
    return recommendations;
  }

  private generateSuggestions(): string[] {
    const suggestions = [];
    
    if (this.state.confidenceLevel < 0.5) {
      suggestions.push("Révisez les concepts de base");
      suggestions.push("Pratiquez avec des exercices simples");
    }
    
    if (this.state.currentStreak > 3) {
      suggestions.push("Continuez à vous challenger");
      suggestions.push("Essayez des questions plus difficiles");
    }
    
    return suggestions;
  }

  private generateNextSteps(): string[] {
    const nextSteps = [];
    
    nextSteps.push("Continuez le test pour affiner l'évaluation");
    
    if (this.state.confidenceLevel > 0.7) {
      nextSteps.push("Préparez-vous pour des défis plus difficiles");
    } else {
      nextSteps.push("Concentrez-vous sur la compréhension des concepts");
    }
    
    return nextSteps;
  }

  // Getters pour accéder à l'état
  public getState(): AdaptiveState {
    return { ...this.state };
  }

  public getCurrentDifficulty(): number {
    return this.state.currentDifficulty;
  }

  public getConfidenceLevel(): number {
    return this.state.confidenceLevel;
  }

  public getProgress(): { total: number; correct: number; percentage: number } {
    return {
      total: this.state.totalQuestions,
      correct: this.state.correctAnswers,
      percentage: this.state.totalQuestions > 0 
        ? Math.round((this.state.correctAnswers / this.state.totalQuestions) * 100)
        : 0
    };
  }
}
























