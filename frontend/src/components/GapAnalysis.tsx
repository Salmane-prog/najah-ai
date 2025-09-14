import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Search, AlertTriangle, Target, TrendingDown, BookOpen, Lightbulb } from 'lucide-react';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface DashboardData {
  students: Array<{id: number, name: string}>;
  analysis_types: Array<{id: string, name: string}>;
  subjects: Array<{id: string, name: string}>;
  gap_score: number;
  total_students: number;
  total_quizzes: number;
}

const GapAnalysis: React.FC = () => {
  console.log('🚀 GapAnalysis component is rendering!');
  
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [selectedStudent, setSelectedStudent] = useState<string>('');
  const [selectedAnalysisType, setSelectedAnalysisType] = useState<string>('');
  const [selectedSubject, setSelectedSubject] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<any>(null);

  useEffect(() => {
    console.log('GapAnalysis component mounted');
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      console.log('🔍 [FRONTEND] Début de récupération des données...');
      setLoading(true);
      setError(null);

      const response = await fetch(`${API_BASE_URL}/api/v1/gap_analysis/dashboard-data`, {
        headers: {
          'Content-Type': 'application/json'
        }
      });

      console.log('🔍 [FRONTEND] Response status:', response.status);
      console.log('🔍 [FRONTEND] Response ok:', response.ok);

      if (!response.ok) {
        throw new Error(`Erreur ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      console.log('🔍 [FRONTEND] Gap Analysis Data reçu:', data); // Debug
      console.log('🔍 [FRONTEND] Students:', data.students); // Debug
      console.log('🔍 [FRONTEND] Analysis Types:', data.analysis_types); // Debug
      console.log('🔍 [FRONTEND] Subjects:', data.subjects); // Debug
      console.log('🔍 [FRONTEND] DashboardData state before:', dashboardData);
      setDashboardData(data);
      console.log('🔍 [FRONTEND] DashboardData state after set:', data);
      
      // Pré-sélectionner le premier étudiant et type d'analyse
      if (data.students && data.students.length > 0) {
        console.log('🔍 [FRONTEND] Setting selected student:', data.students[0].id.toString());
        setSelectedStudent(data.students[0].id.toString());
      }
      if (data.analysis_types && data.analysis_types.length > 0) {
        console.log('🔍 [FRONTEND] Setting selected analysis type:', data.analysis_types[0].id);
        setSelectedAnalysisType(data.analysis_types[0].id);
      }
      if (data.subjects && data.subjects.length > 0) {
        console.log('🔍 [FRONTEND] Setting selected subject:', data.subjects[0].id);
        setSelectedSubject(data.subjects[0].id);
      }
      
    } catch (err) {
      console.error('❌ [FRONTEND] Erreur gap analysis:', err);
      setError('Erreur lors du chargement des données');
    } finally {
      setLoading(false);
    }
  };

  const getGapSeverity = (score: number) => {
    if (score >= 80) return { color: 'text-green-600', bg: 'bg-green-100', label: 'Faible' };
    if (score >= 60) return { color: 'text-yellow-600', bg: 'bg-yellow-100', label: 'Modéré' };
    return { color: 'text-red-600', bg: 'bg-red-100', label: 'Élevé' };
  };

  const handleAnalyzeGaps = async () => {
    try {
      console.log('🔍 [FRONTEND] Début de l\'analyse des lacunes...');
      console.log('🔍 [FRONTEND] Paramètres:', { selectedAnalysisType, selectedStudent, selectedSubject });
      
      setAnalyzing(true);
      setError(null);

      // Construire l'URL selon le type d'analyse
      let url = '';
      if (selectedAnalysisType === 'student' && selectedStudent) {
        url = `${API_BASE_URL}/api/v1/gap_analysis/student/${selectedStudent}/gaps`;
      } else if (selectedAnalysisType === 'subject' && selectedSubject) {
        url = `${API_BASE_URL}/api/v1/gap_analysis/subject/${encodeURIComponent(selectedSubject)}/gaps-test`;
      } else if (selectedAnalysisType === 'class' && selectedStudent) {
        url = `${API_BASE_URL}/api/v1/gap_analysis/class/${selectedStudent}/gaps`;
      } else if (selectedAnalysisType === 'performance') {
        url = `${API_BASE_URL}/api/v1/gap_analysis/performance/analysis`;
      } else if (selectedAnalysisType === 'comprehensive') {
        url = `${API_BASE_URL}/api/v1/gap_analysis/comprehensive/analysis`;
      } else if (selectedAnalysisType === 'temporal') {
        url = `${API_BASE_URL}/api/v1/gap_analysis/temporal/analysis`;
      } else {
        // Analyse générale
        url = `${API_BASE_URL}/api/v1/gap_analysis/dashboard-data`;
      }

      console.log('🔍 [FRONTEND] URL d\'analyse:', url);

      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error('❌ [FRONTEND] Erreur HTTP:', response.status, errorText);
        throw new Error(`Erreur ${response.status}: ${response.statusText}`);
      }

      const result = await response.json();
      console.log('🔍 [FRONTEND] Résultat de l\'analyse:', result);
      
      setAnalysisResult(result);
      
      // Mettre à jour le score global si disponible
      if (result.gap_score !== undefined) {
        setDashboardData(prev => prev ? { ...prev, gap_score: result.gap_score } : null);
      }

    } catch (err) {
      console.error('❌ [FRONTEND] Erreur lors de l\'analyse:', err);
      setError(err instanceof Error ? err.message : 'Erreur lors de l\'analyse des lacunes');
    } finally {
      setAnalyzing(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertTriangle className="h-4 w-4" />
        <AlertDescription>{error}</AlertDescription>
      </Alert>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Analyse des Lacunes</h2>
        <Badge variant="outline" className="text-sm">
          <Search className="h-4 w-4 mr-1" />
          Diagnostic IA
        </Badge>
      </div>

      {/* Contrôles */}
      <Card>
        <CardHeader>
          <CardTitle>Paramètres d'Analyse</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex gap-4">
            <div className="flex-1">
              <label className="text-sm font-medium">Type d'Analyse</label>
              <select 
                value={selectedAnalysisType} 
                onChange={(e) => setSelectedAnalysisType(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Sélectionner un type d'analyse</option>
                {dashboardData?.analysis_types && dashboardData.analysis_types.length > 0 ? (
                  dashboardData.analysis_types.map(type => (
                    <option key={type.id} value={type.id}>{type.name}</option>
                  ))
                ) : (
                  <option value="no-data" disabled>Aucune donnée disponible</option>
                )}
              </select>
              {console.log('🔍 [FRONTEND] Rendering analysis types dropdown with:', dashboardData?.analysis_types)}
            </div>

            {/* Afficher le dropdown Étudiant seulement pour les analyses par étudiant */}
            {(selectedAnalysisType === 'student' || selectedAnalysisType === 'class' || selectedAnalysisType === '') && (
              <div className="flex-1">
                <label className="text-sm font-medium">Étudiant</label>
                <select 
                  value={selectedStudent} 
                  onChange={(e) => setSelectedStudent(e.target.value)}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Sélectionner un étudiant</option>
                  {dashboardData?.students && dashboardData.students.length > 0 ? (
                    dashboardData.students.map(student => (
                      <option key={student.id} value={student.id.toString()}>{student.name}</option>
                    ))
                  ) : (
                    <option value="no-data" disabled>Aucun étudiant disponible</option>
                  )}
                </select>
                {console.log('🔍 [FRONTEND] Rendering students dropdown with:', dashboardData?.students)}
              </div>
            )}

            {/* Afficher le dropdown Matière seulement pour les analyses par matière */}
            {(selectedAnalysisType === 'subject' || selectedAnalysisType === '') && (
              <div className="flex-1">
                <label className="text-sm font-medium">Matière</label>
                <select 
                  value={selectedSubject} 
                  onChange={(e) => setSelectedSubject(e.target.value)}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Sélectionner une matière</option>
                  {dashboardData?.subjects && dashboardData.subjects.length > 0 ? (
                    dashboardData.subjects.map(subject => (
                      <option key={subject.id} value={subject.id}>
                        {subject.name}
                      </option>
                    ))
                  ) : (
                    <>
                      <option value="math">Mathématiques</option>
                      <option value="french">Français</option>
                      <option value="science">Sciences</option>
                      <option value="history">Histoire</option>
                    </>
                  )}
                </select>
                {console.log('🔍 [FRONTEND] Rendering subjects dropdown with:', dashboardData?.subjects)}
              </div>
            )}
          </div>

          <Button 
            onClick={handleAnalyzeGaps} 
            disabled={analyzing || !selectedAnalysisType}
            className="w-full"
          >
            {analyzing ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Analyse en cours...
              </>
            ) : (
              <>
                <Search className="h-4 w-4 mr-2" />
                Analyser les Lacunes
              </>
            )}
          </Button>
        </CardContent>
      </Card>

      {/* Résultats de l'analyse */}
      {dashboardData && (
        <div className="space-y-6">
          {/* Score global */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Target className="h-5 w-5 text-blue-500" />
                Score Global des Lacunes
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">Score de lacunes</span>
                  <Badge variant={getGapSeverity(dashboardData.gap_score).bg as any}>
                    {dashboardData.gap_score}%
                  </Badge>
                </div>
                <Progress value={dashboardData.gap_score} className="h-2" />
                <p className="text-xs text-muted-foreground">
                  Plus le score est élevé, plus les lacunes sont importantes
                </p>
              </div>
            </CardContent>
          </Card>

          {/* Résultats détaillés de l'analyse */}
          {analysisResult && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Search className="h-5 w-5 text-green-500" />
                  Résultats de l'Analyse
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {analysisResult.gaps && analysisResult.gaps.length > 0 ? (
                    <div className="space-y-2">
                      <h4 className="font-semibold text-gray-700">Lacunes identifiées :</h4>
                      {analysisResult.gaps.map((gap: any, index: number) => (
                        <div key={index} className="p-3 bg-red-50 border border-red-200 rounded-lg">
                          <div className="flex items-center gap-2">
                            <AlertTriangle className="h-4 w-4 text-red-500" />
                            <span className="text-sm font-medium">{gap.subject || gap.quiz_title}</span>
                          </div>
                          <p className="text-xs text-gray-600 mt-1">
                            Score: {gap.average_score || gap.score || 'N/A'}% - {gap.suggestion}
                          </p>
                        </div>
                      ))}
                    </div>
                  ) : analysisResult.problematic_subjects && analysisResult.problematic_subjects.length > 0 ? (
                    <div className="space-y-2">
                      <h4 className="font-semibold text-gray-700">Matières problématiques :</h4>
                      {analysisResult.problematic_subjects.map((subject: any, index: number) => (
                        <div key={index} className="p-3 bg-orange-50 border border-orange-200 rounded-lg">
                          <div className="flex items-center gap-2">
                            <AlertTriangle className="h-4 w-4 text-orange-500" />
                            <span className="text-sm font-medium">{subject.subject}</span>
                          </div>
                          <p className="text-xs text-gray-600 mt-1">
                            Score moyen: {subject.average_score}% - {subject.suggestion}
                          </p>
                        </div>
                      ))}
                    </div>
                  ) : analysisResult.common_gaps && analysisResult.common_gaps.length > 0 ? (
                    <div className="space-y-2">
                      <h4 className="font-semibold text-gray-700">Lacunes communes :</h4>
                      {analysisResult.common_gaps.map((gap: any, index: number) => (
                        <div key={index} className="p-3 bg-purple-50 border border-purple-200 rounded-lg">
                          <div className="flex items-center gap-2">
                            <AlertTriangle className="h-4 w-4 text-purple-500" />
                            <span className="text-sm font-medium">{gap.subject}</span>
                          </div>
                          <p className="text-xs text-gray-600 mt-1">
                            Score moyen: {gap.average_score}% - {gap.suggestion}
                          </p>
                        </div>
                      ))}
                    </div>
                  ) : analysisResult.subject_analysis && Object.keys(analysisResult.subject_analysis).length > 0 ? (
                    <div className="space-y-2">
                      <h4 className="font-semibold text-gray-700">Analyse par matière :</h4>
                      {Object.entries(analysisResult.subject_analysis).map(([subject, data]: [string, any], index: number) => (
                        <div key={index} className="p-3 bg-blue-50 border border-blue-200 rounded-lg">
                          <div className="flex items-center justify-between">
                            <span className="text-sm font-medium">{subject}</span>
                            <span className="text-sm font-semibold">{data.average_score}%</span>
                          </div>
                          <p className="text-xs text-gray-600 mt-1">
                            {data.total_quizzes} quiz - Score moyen: {data.average_score}%
                          </p>
                        </div>
                      ))}
                    </div>
                  ) : analysisResult.temporal_analysis && Object.keys(analysisResult.temporal_analysis).length > 0 ? (
                    <div className="space-y-4">
                      <h4 className="font-semibold text-gray-700">Analyse Temporelle :</h4>
                      
                      {/* Tendances hebdomadaires */}
                      {analysisResult.temporal_analysis.weekly_trends && Object.keys(analysisResult.temporal_analysis.weekly_trends).length > 0 && (
                        <div className="space-y-2">
                          <h5 className="text-sm font-medium text-gray-600">Tendances Hebdomadaires :</h5>
                          {Object.entries(analysisResult.temporal_analysis.weekly_trends).slice(-3).map(([week, data]: [string, any], index: number) => (
                            <div key={index} className="p-2 bg-green-50 border border-green-200 rounded">
                              <div className="flex items-center justify-between">
                                <span className="text-xs">Semaine {week.split('-W')[1]}</span>
                                <span className="text-xs font-semibold">{data.average_score}%</span>
                              </div>
                              <p className="text-xs text-gray-500">Amélioration: {data.improvement_rate}%</p>
                            </div>
                          ))}
                        </div>
                      )}
                      
                      {/* Patterns saisonniers */}
                      {analysisResult.temporal_analysis.seasonal_patterns && Object.keys(analysisResult.temporal_analysis.seasonal_patterns).length > 0 && (
                        <div className="space-y-2">
                          <h5 className="text-sm font-medium text-gray-600">Patterns Saisonniers :</h5>
                          {Object.entries(analysisResult.temporal_analysis.seasonal_patterns).map(([season, data]: [string, any], index: number) => (
                            <div key={index} className="p-2 bg-purple-50 border border-purple-200 rounded">
                              <div className="flex items-center justify-between">
                                <span className="text-xs">{season}</span>
                                <span className="text-xs font-semibold">{data.average_score}%</span>
                              </div>
                              <p className="text-xs text-gray-500">Niveau: {data.performance_level}</p>
                            </div>
                          ))}
                        </div>
                      )}
                      
                      {/* Périodes de régression */}
                      {analysisResult.temporal_analysis.regression_periods && analysisResult.temporal_analysis.regression_periods.length > 0 && (
                        <div className="space-y-2">
                          <h5 className="text-sm font-medium text-gray-600">Périodes de Régression :</h5>
                          {analysisResult.temporal_analysis.regression_periods.map((regression: any, index: number) => (
                            <div key={index} className="p-2 bg-red-50 border border-red-200 rounded">
                              <div className="flex items-center justify-between">
                                <span className="text-xs">Période {regression.period}</span>
                                <span className="text-xs font-semibold text-red-600">-{regression.decline_percentage}%</span>
                              </div>
                              <p className="text-xs text-gray-500">Sévérité: {regression.severity}</p>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  ) : (
                    <div className="text-center py-4">
                      <div className="text-green-500 mb-2">✅</div>
                      <p className="text-sm text-gray-600">Aucune lacune critique identifiée</p>
                    </div>
                  )}

                  {analysisResult.recommendations && analysisResult.recommendations.length > 0 && (
                    <div className="space-y-2">
                      <h4 className="font-semibold text-gray-700">Recommandations :</h4>
                      {analysisResult.recommendations.map((rec: string, index: number) => (
                        <div key={index} className="p-3 bg-blue-50 border border-blue-200 rounded-lg">
                          <div className="flex items-center gap-2">
                            <Lightbulb className="h-4 w-4 text-blue-500" />
                            <span className="text-sm">{rec}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Métriques de performance */}
                  {analysisResult.performance_metrics && (
                    <div className="space-y-2">
                      <h4 className="font-semibold text-gray-700">Métriques de Performance :</h4>
                      <div className="grid grid-cols-2 gap-4">
                        <div className="p-3 bg-gray-50 border border-gray-200 rounded-lg">
                          <div className="text-xs text-gray-500">Score moyen</div>
                          <div className="text-lg font-semibold">{analysisResult.average_score || 'N/A'}%</div>
                        </div>
                        <div className="p-3 bg-gray-50 border border-gray-200 rounded-lg">
                          <div className="text-xs text-gray-500">Étudiants analysés</div>
                          <div className="text-lg font-semibold">{analysisResult.performance_metrics.total_students || 'N/A'}</div>
                        </div>
                        <div className="p-3 bg-gray-50 border border-gray-200 rounded-lg">
                          <div className="text-xs text-gray-500">Matières</div>
                          <div className="text-lg font-semibold">{analysisResult.performance_metrics.total_subjects || 'N/A'}</div>
                        </div>
                        <div className="p-3 bg-gray-50 border border-gray-200 rounded-lg">
                          <div className="text-xs text-gray-500">Tendance</div>
                          <div className="text-lg font-semibold capitalize">{analysisResult.performance_metrics.performance_trend || 'N/A'}</div>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Métriques de l'analyse complète */}
                  {analysisResult.comprehensive_metrics && (
                    <div className="space-y-2">
                      <h4 className="font-semibold text-gray-700">Métriques de l'Analyse Complète :</h4>
                      <div className="grid grid-cols-2 gap-4">
                        <div className="p-3 bg-gray-50 border border-gray-200 rounded-lg">
                          <div className="text-xs text-gray-500">Score global</div>
                          <div className="text-lg font-semibold">{analysisResult.overall_gap_score || 'N/A'}%</div>
                        </div>
                        <div className="p-3 bg-gray-50 border border-gray-200 rounded-lg">
                          <div className="text-xs text-gray-500">Étudiants analysés</div>
                          <div className="text-lg font-semibold">{analysisResult.comprehensive_metrics.total_students || 'N/A'}</div>
                        </div>
                        <div className="p-3 bg-gray-50 border border-gray-200 rounded-lg">
                          <div className="text-xs text-gray-500">Matières</div>
                          <div className="text-lg font-semibold">{analysisResult.comprehensive_metrics.total_subjects || 'N/A'}</div>
                        </div>
                        <div className="p-3 bg-gray-50 border border-gray-200 rounded-lg">
                          <div className="text-xs text-gray-500">Lacunes identifiées</div>
                          <div className="text-lg font-semibold">{analysisResult.comprehensive_metrics.total_gaps_identified || 'N/A'}</div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Message d'erreur */}
          {error && (
            <Alert variant="destructive">
              <AlertTriangle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
        </div>
      )}
    </div>
  );
};

export default GapAnalysis; 