"use client";

import React, { useEffect, useState } from 'react';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface Student {
  id: number;
  name: string;
  email: string;
}

interface QuizStats {
  total_quizzes: number;
  average_score: number;
  best_score: number;
  worst_score: number;
}

interface RecentQuiz {
  quiz_title: string;
  score: number;
  completed_at: string;
}

interface SubjectDifficulty {
  incorrect_answers: number;
  total_questions: number;
  difficulty_rate: number;
}

interface DifficultQuestion {
  question: string;
  quiz: string;
  subject: string;
  incorrect_count: number;
}

interface DailyProgress {
  date: string;
  average_score: number;
  quiz_count: number;
}

interface SubjectProgress {
  subject: string;
  average_score: number;
  quiz_count: number;
}

interface StudentOverview {
  student: Student;
  quiz_stats: QuizStats;
  recent_quizzes: RecentQuiz[];
  badges_count: number;
  learning_paths_count: number;
}

interface StudentDifficulties {
  student: Student;
  subject_difficulties: Record<string, SubjectDifficulty>;
  difficult_questions: DifficultQuestion[];
}

interface ProgressChart {
  student: Student;
  daily_progress: DailyProgress[];
  subject_progress: SubjectProgress[];
}

interface DetailedAnalysis {
  student: Student;
  overview: StudentOverview;
  quiz_history: any[];
  difficulties: StudentDifficulties;
  progress_chart: ProgressChart;
  recommendations: string[];
}

function StudentOverviewCard({ overview }: { overview: StudentOverview }) {
  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-gray-800">{overview.student.name}</h3>
        <span className="text-sm text-gray-500">{overview.student.email}</span>
      </div>
      
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="text-center p-4 bg-blue-50 rounded-lg">
          <div className="text-2xl font-bold text-blue-600">{overview.quiz_stats.total_quizzes}</div>
          <div className="text-sm text-gray-600">Quiz complétés</div>
        </div>
        <div className="text-center p-4 bg-green-50 rounded-lg">
          <div className="text-2xl font-bold text-green-600">{overview.quiz_stats.average_score}%</div>
          <div className="text-sm text-gray-600">Score moyen</div>
        </div>
        <div className="text-center p-4 bg-purple-50 rounded-lg">
          <div className="text-2xl font-bold text-purple-600">{overview.quiz_stats.best_score}%</div>
          <div className="text-sm text-gray-600">Meilleur score</div>
        </div>
        <div className="text-center p-4 bg-yellow-50 rounded-lg">
          <div className="text-2xl font-bold text-yellow-600">{overview.badges_count}</div>
          <div className="text-sm text-gray-600">Badges obtenus</div>
        </div>
      </div>
      
      <div className="space-y-2">
        <h4 className="font-semibold text-gray-700">Quiz récents</h4>
        {overview.recent_quizzes.length > 0 ? (
          <div className="space-y-2">
            {overview.recent_quizzes.map((quiz, index) => (
              <div key={index} className="flex justify-between items-center p-2 bg-gray-50 rounded">
                <span className="text-sm">{quiz.quiz_title}</span>
                <span className={`text-sm font-semibold ${quiz.score >= 70 ? 'text-green-600' : quiz.score >= 50 ? 'text-yellow-600' : 'text-red-600'}`}>
                  {quiz.score}%
                </span>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500 text-sm">Aucun quiz récent</p>
        )}
      </div>
    </div>
  );
}

function DifficultiesCard({ difficulties }: { difficulties: StudentDifficulties }) {
  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h3 className="text-xl font-bold text-gray-800 mb-4">Analyse des difficultés</h3>
      
      <div className="space-y-4">
        <div>
          <h4 className="font-semibold text-gray-700 mb-2">Difficultés par matière</h4>
          {Object.entries(difficulties.subject_difficulties).length > 0 ? (
            <div className="space-y-2">
              {Object.entries(difficulties.subject_difficulties).map(([subject, stats]) => (
                <div key={subject} className="flex justify-between items-center p-3 bg-gray-50 rounded">
                  <span className="font-medium">{subject}</span>
                  <div className="text-right">
                    <div className={`font-semibold ${stats.difficulty_rate > 50 ? 'text-red-600' : stats.difficulty_rate > 30 ? 'text-yellow-600' : 'text-green-600'}`}>
                      {stats.difficulty_rate}%
                    </div>
                    <div className="text-xs text-gray-500">
                      {stats.incorrect_answers}/{stats.total_questions} erreurs
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500 text-sm">Aucune donnée de difficulté disponible</p>
          )}
        </div>
        
        <div>
          <h4 className="font-semibold text-gray-700 mb-2">Questions les plus difficiles</h4>
          {difficulties.difficult_questions.length > 0 ? (
            <div className="space-y-2">
              {difficulties.difficult_questions.slice(0, 3).map((question, index) => (
                <div key={index} className="p-3 bg-red-50 rounded border-l-4 border-red-400">
                  <div className="text-sm font-medium text-gray-800">{question.question}</div>
                  <div className="text-xs text-gray-600 mt-1">
                    Quiz: {question.quiz} | Matière: {question.subject} | Erreurs: {question.incorrect_count}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500 text-sm">Aucune question difficile identifiée</p>
          )}
        </div>
      </div>
    </div>
  );
}

function ProgressChartCard({ progressChart }: { progressChart: ProgressChart }) {
  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h3 className="text-xl font-bold text-gray-800 mb-4">Progression</h3>
      
      <div className="space-y-4">
        <div>
          <h4 className="font-semibold text-gray-700 mb-2">Progression par matière</h4>
          {progressChart.subject_progress.length > 0 ? (
            <div className="space-y-2">
              {progressChart.subject_progress.map((subject, index) => (
                <div key={index} className="flex justify-between items-center p-3 bg-gray-50 rounded">
                  <span className="font-medium">{subject.subject}</span>
                  <div className="text-right">
                    <div className={`font-semibold ${subject.average_score >= 70 ? 'text-green-600' : subject.average_score >= 50 ? 'text-yellow-600' : 'text-red-600'}`}>
                      {subject.average_score}%
                    </div>
                    <div className="text-xs text-gray-500">
                      {subject.quiz_count} quiz
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500 text-sm">Aucune donnée de progression disponible</p>
          )}
        </div>
        
        <div>
          <h4 className="font-semibold text-gray-700 mb-2">Progression quotidienne (30 derniers jours)</h4>
          {progressChart.daily_progress.length > 0 ? (
            <div className="space-y-2 max-h-40 overflow-y-auto">
              {progressChart.daily_progress.map((day, index) => (
                <div key={index} className="flex justify-between items-center p-2 bg-gray-50 rounded">
                  <span className="text-sm">{new Date(day.date).toLocaleDateString()}</span>
                  <div className="text-right">
                    <span className={`text-sm font-semibold ${day.average_score >= 70 ? 'text-green-600' : day.average_score >= 50 ? 'text-yellow-600' : 'text-red-600'}`}>
                      {day.average_score}%
                    </span>
                    <span className="text-xs text-gray-500 ml-2">({day.quiz_count} quiz)</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500 text-sm">Aucune progression quotidienne disponible</p>
          )}
        </div>
      </div>
    </div>
  );
}

function RecommendationsCard({ recommendations }: { recommendations: string[] }) {
  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h3 className="text-xl font-bold text-gray-800 mb-4">Recommandations</h3>
      
      {recommendations.length > 0 ? (
        <div className="space-y-3">
          {recommendations.map((recommendation, index) => (
            <div key={index} className="flex items-start p-3 bg-blue-50 rounded border-l-4 border-blue-400">
              <span className="text-blue-600 mr-2">💡</span>
              <span className="text-sm text-gray-700">{recommendation}</span>
            </div>
          ))}
        </div>
      ) : (
        <p className="text-gray-500 text-sm">Aucune recommandation disponible</p>
      )}
    </div>
  );
}

function StudentDetailModal({ studentId, onClose }: { studentId: number; onClose: () => void }) {
  const [analysis, setAnalysis] = useState<DetailedAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        const token = localStorage.getItem('najah_token');
        const res = await fetch(`${API_BASE_URL}/api/v1/student_performance/students/${studentId}/detailed-analysis`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
          const data = await res.json();
          setAnalysis(data);
        } else {
          setError('Erreur lors du chargement de l\'analyse');
        }
      } catch (error) {
        setError('Erreur de connexion');
      } finally {
        setLoading(false);
      }
    };
    fetchAnalysis();
  }, [studentId]);

  if (loading) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-30">
        <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-4xl w-full relative max-h-[90vh] overflow-y-auto">
          <button type="button" onClick={onClose} className="absolute top-4 right-4 text-gray-400 hover:text-blue-600 text-xl font-bold">×</button>
          <div className="text-center py-8">Chargement de l'analyse...</div>
        </div>
      </div>
    );
  }

  if (error || !analysis) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-30">
        <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-4xl w-full relative max-h-[90vh] overflow-y-auto">
          <button type="button" onClick={onClose} className="absolute top-4 right-4 text-gray-400 hover:text-blue-600 text-xl font-bold">×</button>
          <div className="text-center py-8 text-red-600">{error || 'Erreur inconnue'}</div>
        </div>
      </div>
    );
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-30">
      <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-6xl w-full relative max-h-[90vh] overflow-y-auto">
        <button type="button" onClick={onClose} className="absolute top-4 right-4 text-gray-400 hover:text-blue-600 text-xl font-bold">×</button>
        
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Analyse détaillée - {analysis.student.name}</h2>
          <p className="text-gray-600">{analysis.student.email}</p>
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <StudentOverviewCard overview={analysis.overview} />
          <DifficultiesCard difficulties={analysis.difficulties} />
          <ProgressChartCard progressChart={analysis.progress_chart} />
          <RecommendationsCard recommendations={analysis.recommendations} />
        </div>
      </div>
    </div>
  );
}

export default function StudentPerformanceWidget() {
  const [students, setStudents] = useState<Student[]>([]);
  const [classPerformance, setClassPerformance] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showDetailModal, setShowDetailModal] = useState(false);
  const [selectedStudentId, setSelectedStudentId] = useState<number | null>(null);

  const fetchStudents = async () => {
    try {
      const token = localStorage.getItem('najah_token');
      const res = await fetch(`${API_BASE_URL}/api/v1/users/students-by-role`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setStudents(data);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des élèves:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchClassPerformance = async () => {
    try {
      const token = localStorage.getItem('najah_token');
      // Pour l'exemple, on utilise la classe 1. En réalité, il faudrait récupérer les classes du professeur
      const res = await fetch(`${API_BASE_URL}/api/v1/student_performance/class/1/students-performance`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setClassPerformance(data.students_performance || []);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des performances de classe:', error);
    }
  };

  useEffect(() => {
    fetchStudents();
    fetchClassPerformance();
  }, []);

  if (loading) {
    return <div className="text-center py-8">Chargement des performances...</div>;
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-8">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Suivi des Performances Élèves</h2>
        <button
          onClick={() => {
            fetchClassPerformance();
          }}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition"
        >
          Actualiser
        </button>
      </div>

      {classPerformance.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          Aucune donnée de performance disponible. Les élèves doivent compléter des quiz pour voir leurs performances.
        </div>
      ) : (
        <div className="space-y-4">
          <div className="overflow-x-auto">
            <table className="w-full border-collapse border border-gray-300">
              <thead>
                <tr className="bg-gray-100">
                  <th className="border border-gray-300 px-4 py-2 text-left">Élève</th>
                  <th className="border border-gray-300 px-4 py-2 text-center">Quiz complétés</th>
                  <th className="border border-gray-300 px-4 py-2 text-center">Score moyen</th>
                  <th className="border border-gray-300 px-4 py-2 text-center">Meilleur score</th>
                  <th className="border border-gray-300 px-4 py-2 text-center">Badges</th>
                  <th className="border border-gray-300 px-4 py-2 text-center">Actions</th>
                </tr>
              </thead>
              <tbody>
                {classPerformance.map((studentPerf) => (
                  <tr key={studentPerf.student.id} className="hover:bg-gray-50">
                    <td className="border border-gray-300 px-4 py-2">
                      <div>
                        <div className="font-medium">{studentPerf.student.name}</div>
                        <div className="text-sm text-gray-500">{studentPerf.student.email}</div>
                      </div>
                    </td>
                    <td className="border border-gray-300 px-4 py-2 text-center">
                      {studentPerf.performance.total_quizzes}
                    </td>
                    <td className="border border-gray-300 px-4 py-2 text-center">
                      <span className={`font-semibold ${
                        studentPerf.performance.average_score >= 70 ? 'text-green-600' : 
                        studentPerf.performance.average_score >= 50 ? 'text-yellow-600' : 'text-red-600'
                      }`}>
                        {studentPerf.performance.average_score}%
                      </span>
                    </td>
                    <td className="border border-gray-300 px-4 py-2 text-center">
                      <span className="font-semibold text-blue-600">
                        {studentPerf.performance.best_score}%
                      </span>
                    </td>
                    <td className="border border-gray-300 px-4 py-2 text-center">
                      <span className="font-semibold text-purple-600">
                        {studentPerf.performance.badges_count}
                      </span>
                    </td>
                    <td className="border border-gray-300 px-4 py-2 text-center">
                      <button
                        onClick={() => {
                          setSelectedStudentId(studentPerf.student.id);
                          setShowDetailModal(true);
                        }}
                        className="px-3 py-1 bg-blue-600 text-white rounded text-sm hover:bg-blue-700"
                      >
                        Détails
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {showDetailModal && selectedStudentId && (
        <StudentDetailModal
          studentId={selectedStudentId}
          onClose={() => {
            setShowDetailModal(false);
            setSelectedStudentId(null);
          }}
        />
      )}
    </div>
  );
} 