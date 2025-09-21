// ============================================================================
// EXPORT DE TOUS LES SERVICES
// ============================================================================

// Services principaux - exports spécifiques pour éviter les conflits
export { 
  teacherDashboardService, 
  getTeacherDashboardData, 
  getTeacherAnalytics, 
  getTeacherStudents, 
  getTeacherQuizzes 
} from './teacherDashboardService';

export { 
  aiAnalyticsService, 
  getAIAnalyticsData, 
  getLearningAnalytics, 
  getAIPredictions, 
  getBlockageDetections, 
  getLearningPatterns, 
  getAIRecommendations 
} from './aiAnalyticsService';

// Services secondaires - exports par défaut uniquement
export { default as adaptiveAlgorithmService } from './adaptiveAlgorithmService';
export { default as aiModelsService } from './aiModelsService';
export { default as cognitiveDiagnosticService } from './cognitiveDiagnosticService';
export { default as adaptiveLearningService } from './adaptiveLearningService';
export { default as analyticsService } from './analyticsService';
export { default as adaptiveEvaluationService } from './adaptiveEvaluationService';
export { default as frenchAIService } from './frenchAIService';
export { default as studentDashboardService } from './studentDashboardService';
export { default as teacherClassesService } from './teacherClassesService';
export { default as quizService } from './quizService';
export { default as messagingService } from './messagingService';
export { default as calendarService } from './calendarService';
export { default as realAIModelsService } from './realAIModelsService';
export { default as realDataCollectionService } from './realDataCollectionService';
export { default as realTrainingSessionsService } from './realTrainingSessionsService';
export { default as unifiedAIService } from './unifiedAIService';

// ============================================================================
// RÉSUMÉ DES SERVICES DISPONIBLES
// ============================================================================

/*
🎯 SERVICES PRINCIPAUX (DASHBOARD)

1. teacherDashboardService - Dashboard professeur avec vraies données
2. studentDashboardService - Dashboard étudiant avec vraies données
3. aiAnalyticsService - Analytics IA avec vraies données

🎯 SERVICES SPÉCIALISÉS

4. teacherClassesService - Classes et étudiants du professeur
5. quizService - Quiz et évaluations
6. messagingService - Messages et notifications
7. calendarService - Calendrier et emploi du temps

🎯 SERVICES IA ET ADAPTATIFS (MAINTENANT AVEC VRAIES DONNÉES)

8. adaptiveAlgorithmService - Algorithme d'apprentissage adaptatif
9. adaptiveLearningService - Apprentissage adaptatif
10. adaptiveEvaluationService - Évaluation adaptative
11. aiModelsService - Modèles IA (ancien service)
12. cognitiveDiagnosticService - Diagnostic cognitif
13. analyticsService - Analytics générales

🎯 NOUVEAUX SERVICES IA POUR LES VRAIES DONNÉES

14. realAIModelsService - Vrais modèles IA et sessions d'entraînement
15. realDataCollectionService - Vraies métriques de collecte de données
16. realTrainingSessionsService - Vraies sessions d'entraînement IA

🎯 FONCTIONNALITÉS

✅ TOUTES les fonctionnalités consomment maintenant les vraies données
✅ Fallback automatique vers les données mockées en cas d'erreur
✅ Logs détaillés pour le debugging
✅ Gestion d'erreurs robuste
✅ Types TypeScript complets

🎯 ENDPOINTS CONNECTÉS

✅ /api/v1/teacher-dashboard/ - Dashboard professeur
✅ /api/v1/ai-analytics/ - Analytics IA
✅ /api/v1/student_analytics/ - Analytics étudiant
✅ /api/v1/quiz_assignments/ - Assignations de quiz
✅ /api/v1/quiz_results/ - Résultats de quiz
✅ /api/v1/class_groups/ - Classes et étudiants
✅ /api/v1/messages/ - Messages
✅ /api/v1/notifications/ - Notifications
✅ /api/v1/calendar/ - Calendrier
✅ /api/v1/schedule/ - Emploi du temps

🎯 NOUVEAUX ENDPOINTS IA CONNECTÉS

✅ /api/v1/ai_models/ - Modèles IA réels
✅ /api/v1/ai_models/training-sessions/ - Sessions d'entraînement
✅ /api/v1/ai_models/predictions/ - Prédictions des modèles
✅ /api/v1/ai_models/performance/ - Performance des modèles
✅ /api/v1/data_collection/metrics/ - Métriques de collecte
✅ /api/v1/data_collection/sources/ - Sources de données
✅ /api/v1/data_collection/activities/ - Activités de collecte
✅ /api/v1/training_sessions/ - Sessions d'entraînement
✅ /api/v1/training_sessions/jobs/ - Jobs d'entraînement
✅ /api/v1/training_sessions/metrics/ - Métriques d'entraînement

🎯 FLUX DE DONNÉES RÉEL

✅ Professeur crée quiz → Étudiant le voit
✅ Étudiant passe quiz → Professeur voit les résultats
✅ Analytics IA basées sur les vraies performances
✅ Messages et notifications en temps réel
✅ Calendrier synchronisé entre prof et étudiants
*/
