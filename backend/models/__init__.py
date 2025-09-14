# Modèles pour l'évaluation adaptative (doit être avant User)
from .adaptive_evaluation import (
    AdaptiveTest, AdaptiveQuestion, TestAssignment, 
    TestAttempt, QuestionResponse, CompetencyAnalysis, Class, AdaptiveClassStudent
)

# Modèles existants
from .user import User, UserRole
from .quiz import Quiz, Question, QuizResult, QuizAnswer
from .badge import Badge, UserBadge
from .class_group import ClassGroup, ClassStudent
from .content import Content, LearningPathContent
from .learning_path import LearningPath
from .learning_path_step import LearningPathStep
from .student_learning_path import StudentLearningPath
from .learning_history import LearningHistory
from .messages import Message
from .thread import Thread
from .assessment import Assessment, AssessmentQuestion, AssessmentResult
from .homework import AdvancedHomework, AdvancedHomeworkSubmission
from .calendar import CalendarEvent
from .collaboration import StudyGroup, CollaborationProject
from .ai_advanced import AIRecommendation, AITutoringSession
from .reports import DetailedReport, SubjectProgressReport
from .user_activity import UserActivity
from .real_time_activities import RealTimeActivities
from .assignment import Assignment
from .assignment_submission import AssignmentSubmission
from .student_assignment import StudentAssignment
from .content_sharing import ContentSharing, ContentAccess
from .notes import AdvancedNote, AdvancedSubject, AdvancedChapter

# Modèles forum d'entraide
from .forum import ForumCategory, ForumThread, ForumReply

from .french_learning import FrenchLearningProfile, FrenchCompetency, FrenchCompetencyProgress, FrenchLearningPath, FrenchLearningModule, FrenchRecommendation

# Modèles de remédiation
from .remediation import RemediationResult, RemediationBadge, RemediationProgress

# from .analytics import (
#     LearningAnalytics, PredictiveModel, StudentPrediction, LearningPattern,
#     BlockageDetection, TeacherDashboard, ParentDashboard, AutomatedReport, ReportRecipient
# )
# from .ai_models import (
#     AIModel, ModelTrainingSession, AIModelPrediction, ModelDeployment,
#     DataCollection, AILearningPatternAnalysis, ContinuousImprovement
# )