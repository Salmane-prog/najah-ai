// Types pour les analytics en temps réel

export interface StudentPerformance {
  id: number;
  name: string;
  email: string;
  testsCompleted: number;
  averageScore: number;
  progressPercentage: number;
  lastTestDate: string;
  improvementTrend: 'up' | 'down' | 'stable';
}

export interface TestPerformance {
  id: number;
  title: string;
  subject: string;
  participants: number;
  averageScore: number;
  completionRate: number;
  difficultyLevel: number;
  timeSpent: number;
  successRate: number;
  lastAttemptDate: string;
}

export interface WeeklyProgress {
  week: string;
  averageScore: number;
  testsCompleted: number;
  studentsActive: number;
  improvementRate: number;
}

export interface MonthlyStats {
  month: string;
  testsCreated: number;
  testsCompleted: number;
  newStudents: number;
  averagePerformance: number;
}

export interface RealTimeAnalytics {
  currentActiveTests: number;
  studentsOnline: number;
  testsInProgress: number;
  recentCompletions: TestCompletion[];
  systemHealth: SystemHealth;
}

export interface TestCompletion {
  testId: number;
  testTitle: string;
  studentName: string;
  score: number;
  completionTime: string;
  duration: number;
}

export interface SystemHealth {
  backendStatus: 'online' | 'offline' | 'degraded';
  databaseStatus: 'healthy' | 'slow' | 'error';
  lastUpdate: string;
  activeConnections: number;
}

export interface PerformanceMetrics {
  overallAverageScore: number;
  totalTestsCompleted: number;
  totalStudents: number;
  completionRate: number;
  difficultTestsPercentage: number;
  topPerformingTests: TestPerformance[];
  topPerformingStudents: StudentPerformance[];
  weeklyProgress: WeeklyProgress[];
  monthlyStats: MonthlyStats[];
}















