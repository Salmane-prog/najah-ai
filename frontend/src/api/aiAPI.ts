const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface AIQuestionGenerationRequest {
  prompt: string;
  subject: string;
  level: string;
  questionCount: number;
  topics: string[];
  learningObjectives: string[];
}

export interface AIQuestionGenerationResponse {
  success: boolean;
  questions: Array<{
    question: string;
    options: string[];
    correctAnswer: number;
    explanation: string;
    difficulty: number;
    topic: string;
    learningObjective: string;
  }>;
  generatedBy: string;
}

export interface AIStatusResponse {
  success: boolean;
  services: {
    openai: boolean;
    huggingface: boolean;
    local: boolean;
  };
  message: string;
}

class AIAPI {
  private getAuthHeaders(): HeadersInit {
    const token = localStorage.getItem('najah_token') || sessionStorage.getItem('najah_token');
    return {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` })
    };
  }

  async checkStatus(): Promise<AIStatusResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/ai/status`, {
        method: 'GET',
        headers: this.getAuthHeaders()
      });

      if (response.ok) {
        return await response.json();
      } else {
        throw new Error(`Erreur ${response.status}: ${response.statusText}`);
      }
    } catch (error) {
      console.error('❌ Erreur lors de la vérification du statut IA:', error);
      return {
        success: false,
        services: {
          openai: false,
          huggingface: false,
          local: true
        },
        message: 'Services IA non disponibles, utilisation du mode local'
      };
    }
  }

  async generateQuestions(request: AIQuestionGenerationRequest): Promise<AIQuestionGenerationResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/ai/generate-questions`, {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify(request)
      });

      if (response.ok) {
        return await response.json();
      } else {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Erreur ${response.status}: ${response.statusText}`);
      }
    } catch (error) {
      console.error('❌ Erreur lors de la génération de questions IA:', error);
      throw error;
    }
  }

  async testAIService(): Promise<{ success: boolean; message: string }> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/ai/test`, {
        method: 'GET',
        headers: this.getAuthHeaders()
      });

      if (response.ok) {
        const data = await response.json();
        return { success: true, message: data.message || 'Test IA réussi' };
      } else {
        throw new Error(`Erreur ${response.status}: ${response.statusText}`);
      }
    } catch (error) {
      console.error('❌ Erreur lors du test IA:', error);
      return { success: false, message: 'Test IA échoué' };
    }
  }

  async generateFrenchQuestions(
    level: string,
    count: number,
    topics: string[],
    learningObjectives: string[]
  ): Promise<AIQuestionGenerationResponse> {
    const prompt = `
    Génère ${count} questions de français de niveau ${level} sur les thèmes suivants : ${topics.join(', ')}
    
    Objectifs d'apprentissage :
    ${learningObjectives.join('\n')}
    
    Les questions doivent être variées, progressives en difficulté, et couvrir différents aspects de la langue française.
    Chaque question doit avoir 4 options de réponse avec une seule correcte, une explication pédagogique détaillée,
    et être adaptée au niveau spécifié.
    `;

    return this.generateQuestions({
      prompt,
      subject: 'Français',
      level,
      questionCount: count,
      topics,
      learningObjectives
    });
  }

  async analyzeStudentResponse(
    studentAnswer: string,
    correctAnswer: string,
    questionContext: string
  ): Promise<{ success: boolean; analysis: string; suggestions: string[] }> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/ai/analyze-response`, {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({
          student_answer: studentAnswer,
          correct_answer: correctAnswer,
          question_context: questionContext
        })
      });

      if (response.ok) {
        return await response.json();
      } else {
        throw new Error(`Erreur ${response.status}: ${response.statusText}`);
      }
    } catch (error) {
      console.error('❌ Erreur lors de l\'analyse de réponse:', error);
      return {
        success: false,
        analysis: 'Analyse non disponible',
        suggestions: ['Vérifiez votre réponse', 'Consultez la correction']
      };
    }
  }

  async getLearningRecommendations(
    studentId: number,
    subject: string,
    performanceData: any
  ): Promise<{ success: boolean; recommendations: string[]; nextSteps: string[] }> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/ai/recommendations`, {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({
          student_id: studentId,
          subject,
          performance_data: performanceData
        })
      });

      if (response.ok) {
        return await response.json();
      } else {
        throw new Error(`Erreur ${response.status}: ${response.statusText}`);
      }
    } catch (error) {
      console.error('❌ Erreur lors de la récupération des recommandations:', error);
      return {
        success: false,
        recommendations: ['Continuez à pratiquer', 'Révisez les bases'],
        nextSteps: ['Faites des exercices supplémentaires', 'Demandez de l\'aide si nécessaire']
      };
    }
  }
}

export const aiAPI = new AIAPI();
