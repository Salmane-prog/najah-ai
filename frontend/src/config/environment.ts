/**
 * Configuration de l'environnement pour le système IA français
 */

export const ENV_CONFIG = {
  // API OpenAI
  OPENAI_API_KEY: process.env.OPENAI_API_KEY || '',
  AI_ENABLED: process.env.NEXT_PUBLIC_AI_ENABLED === 'true',
  AI_MODEL: process.env.NEXT_PUBLIC_AI_MODEL || 'gpt-3.5-turbo',
  AI_MAX_TOKENS: parseInt(process.env.NEXT_PUBLIC_AI_MAX_TOKENS || '2000'),

  // URL de l'API backend
  API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',

  // Configuration de fallback
  FALLBACK_ENABLED: process.env.NEXT_PUBLIC_FALLBACK_ENABLED !== 'false',
  LOCAL_QUESTIONS_ENABLED: process.env.NEXT_PUBLIC_LOCAL_QUESTIONS_ENABLED !== 'false',

  // Configuration de validation
  VALIDATION_STRICT: process.env.NEXT_PUBLIC_VALIDATION_STRICT !== 'false',
  MIN_QUALITY_SCORE: parseInt(process.env.NEXT_PUBLIC_MIN_QUALITY_SCORE || '7'),

  // Configuration de performance
  MAX_GENERATION_TIME: parseInt(process.env.NEXT_PUBLIC_MAX_GENERATION_TIME || '30'),
  CACHE_ENABLED: process.env.NEXT_PUBLIC_CACHE_ENABLED !== 'false',

  // Configuration de débogage
  DEBUG_MODE: process.env.NEXT_PUBLIC_DEBUG_MODE === 'true',
  LOG_LEVEL: process.env.NEXT_PUBLIC_LOG_LEVEL || 'info',

  // Configuration de sécurité
  AUTH_REQUIRED: process.env.NEXT_PUBLIC_AUTH_REQUIRED !== 'false',
  RATE_LIMIT_ENABLED: process.env.NEXT_PUBLIC_RATE_LIMIT_ENABLED !== 'false'
};

// Vérification de la configuration
export const validateEnvironment = () => {
  const errors: string[] = [];

  if (!ENV_CONFIG.API_URL) {
    errors.push('NEXT_PUBLIC_API_URL est requis');
  }

  if (ENV_CONFIG.AI_ENABLED && !ENV_CONFIG.OPENAI_API_KEY) {
    errors.push('OPENAI_API_KEY est requis quand l\'IA est activée');
  }

  if (ENV_CONFIG.MIN_QUALITY_SCORE < 1 || ENV_CONFIG.MIN_QUALITY_SCORE > 10) {
    errors.push('MIN_QUALITY_SCORE doit être entre 1 et 10');
  }

  if (ENV_CONFIG.MAX_GENERATION_TIME < 5 || ENV_CONFIG.MAX_GENERATION_TIME > 120) {
    errors.push('MAX_GENERATION_TIME doit être entre 5 et 120 secondes');
  }

  return {
    isValid: errors.length === 0,
    errors
  };
};

// Configuration par défaut pour le développement
export const DEFAULT_CONFIG = {
  questionCount: 10,
  maxQuestions: 50,
  minQuestions: 5,
  defaultDifficulty: 5,
  defaultLevel: "Débutant (1-3)",
  defaultTopics: ["Articles", "Conjugaison", "Vocabulaire"],
  defaultLearningObjectives: [
    "Reconnaître les articles définis et indéfinis",
    "Conjuguer les verbes être et avoir au présent",
    "Comprendre le vocabulaire de base"
  ]
};

// Configuration des niveaux de difficulté
export const DIFFICULTY_LEVELS = {
  TRES_FACILE: 1,
  FACILE: 2,
  MOYEN: 5,
  DIFFICILE: 8,
  TRES_DIFFICILE: 10
};

// Configuration des types de questions
export const QUESTION_TYPES = {
  MULTIPLE_CHOICE: 'multiple_choice',
  TRUE_FALSE: 'true_false',
  FILL_BLANK: 'fill_blank',
  MATCHING: 'matching'
};

// Configuration des thèmes français
export const FRENCH_THEMES = {
  GRAMMAIRE: 'Grammaire',
  CONJUGAISON: 'Conjugaison',
  VOCABULAIRE: 'Vocabulaire',
  SYNTAXE: 'Syntaxe',
  COMPREHENSION: 'Compréhension',
  EXPRESSION: 'Expression'
};

// Configuration des objectifs d'apprentissage
export const LEARNING_OBJECTIVES = {
  RECONNAITRE: 'Reconnaître',
  COMPRENDRE: 'Comprendre',
  APPLIQUER: 'Appliquer',
  ANALYSER: 'Analyser',
  EVALUER: 'Évaluer',
  CREER: 'Créer'
};

// Messages de configuration
export const CONFIG_MESSAGES = {
  AI_AVAILABLE: '🤖 IA disponible et configurée',
  AI_UNAVAILABLE: '🔄 IA non disponible, utilisation du fallback local',
  CONFIG_VALID: '✅ Configuration valide',
  CONFIG_INVALID: '❌ Configuration invalide',
  FALLBACK_ACTIVE: '🔄 Mode fallback activé',
  VALIDATION_STRICT: '🔍 Validation stricte activée',
  CACHE_ENABLED: '💾 Cache activé',
  DEBUG_MODE: '🐛 Mode débogage activé'
};

export default ENV_CONFIG;


















