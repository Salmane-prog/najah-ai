import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';

import { Brain, Eye, Ear, Hand, BookOpen, Lightbulb, Target, Users, TrendingUp } from 'lucide-react';
import { apiClient } from '@/api/apiClient';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface CognitiveProfile {
  student_id: number;
  learning_style?: string;
  primary_style_percentage?: number;
  cognitive_strengths?: string[];
  cognitive_weaknesses?: string[];
  confidence_score?: number;
  recommendations?: string[];
}

interface ClassCognitiveAnalysis {
  class_id: number;
  learning_style_distribution?: {
    [style: string]: number;
  };
  dominant_learning_style?: string;
  class_patterns?: string[];
  teaching_recommendations?: string[];
}

const CognitiveDiagnostic: React.FC = () => {
  const [studentProfile, setStudentProfile] = useState<CognitiveProfile | null>(null);
  const [classAnalysis, setClassAnalysis] = useState<ClassCognitiveAnalysis | null>(null);
  const [selectedStudent, setSelectedStudent] = useState<string>('4');
  const [selectedClass, setSelectedClass] = useState<string>('1');
  const [analysisType, setAnalysisType] = useState<'student' | 'class'>('student');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchCognitiveAnalysis();
  }, [analysisType, selectedStudent, selectedClass]);

  const fetchCognitiveAnalysis = async () => {
    try {
      setLoading(true);
      setError(null);

      if (analysisType === 'student') {
        console.log('🔍 [COGNITIVE_DIAGNOSTIC] Analyse du profil étudiant:', selectedStudent);
        const response = await fetch(`${API_BASE_URL}/api/v1/cognitive_diagnostic/student/${selectedStudent}/cognitive-profile-test`);
        
        if (!response.ok) {
          throw new Error(`Erreur ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        console.log('🔍 [COGNITIVE_DIAGNOSTIC] Données reçues:', data);
        setStudentProfile(data);
        setClassAnalysis(null);
      } else {
        console.log('🔍 [COGNITIVE_DIAGNOSTIC] Analyse de classe:', selectedClass);
        const response = await fetch(`${API_BASE_URL}/api/v1/cognitive_diagnostic/class/${selectedClass}/cognitive-analysis`);
        
        if (!response.ok) {
          throw new Error(`Erreur ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        console.log('🔍 [COGNITIVE_DIAGNOSTIC] Données classe reçues:', data);
        setClassAnalysis(data);
        setStudentProfile(null);
      }
    } catch (err) {
      console.error('❌ [COGNITIVE_DIAGNOSTIC] Erreur:', err);
      setError('Erreur lors du chargement de l\'analyse cognitive');
    } finally {
      setLoading(false);
    }
  };

  const getLearningStyleIcon = (style?: string) => {
    if (!style) return <Brain className="h-5 w-5 text-gray-500" />;
    
    switch (style.toLowerCase()) {
      case 'visuel': return <Eye className="h-5 w-5 text-blue-500" />;
      case 'auditif': return <Ear className="h-5 w-5 text-green-500" />;
      case 'kinesthésique': return <Hand className="h-5 w-5 text-purple-500" />;
      case 'lecture/écriture': return <BookOpen className="h-5 w-5 text-orange-500" />;
      default: return <Brain className="h-5 w-5 text-gray-500" />;
    }
  };

  const getLearningStyleColor = (style?: string) => {
    if (!style) return 'bg-gray-100 text-gray-800';
    
    switch (style.toLowerCase()) {
      case 'visuel': return 'bg-blue-100 text-blue-800';
      case 'auditif': return 'bg-green-100 text-green-800';
      case 'kinesthésique': return 'bg-purple-100 text-purple-800';
      case 'lecture/écriture': return 'bg-orange-100 text-orange-800';
      default: return 'bg-gray-100 text-gray-800';
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
        <AlertDescription>{error}</AlertDescription>
      </Alert>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Diagnostic Cognitif</h2>
        <Badge variant="outline" className="text-sm">
          <Brain className="h-4 w-4 mr-1" />
          IA Cognitive
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
                value={analysisType} 
                onChange={(e) => setAnalysisType(e.target.value as 'student' | 'class')}
                className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="student">Profil Étudiant</option>
                <option value="class">Analyse de Classe</option>
              </select>
            </div>

            {analysisType === 'student' && (
              <div className="flex-1">
                <label className="text-sm font-medium">Étudiant</label>
                <select 
                  value={selectedStudent} 
                  onChange={(e) => setSelectedStudent(e.target.value)}
                  className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="4">Salmane EL Hajouji</option>
                  <option value="5">Fatima Alami</option>
                  <option value="6">Omar Benjelloun</option>
                </select>
              </div>
            )}

            {analysisType === 'class' && (
              <div className="flex-1">
                <label className="text-sm font-medium">Classe</label>
                <select 
                  value={selectedClass} 
                  onChange={(e) => setSelectedClass(e.target.value)}
                  className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="1">Classe 1</option>
                  <option value="2">Classe 2</option>
                </select>
              </div>
            )}
          </div>

          <Button onClick={fetchCognitiveAnalysis} className="w-full">
            <Brain className="h-4 w-4 mr-2" />
            Analyser le Profil Cognitif
          </Button>
        </CardContent>
      </Card>

      {/* Profil étudiant */}
      {studentProfile && (
        <div className="space-y-6">
          {/* Style d'apprentissage */}
          {studentProfile.learning_style && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  {getLearningStyleIcon(studentProfile.learning_style)}
                  Style d'Apprentissage Principal
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-semibold">{studentProfile.learning_style}</h3>
                    <Badge className={getLearningStyleColor(studentProfile.learning_style)}>
                      {studentProfile.primary_style_percentage || 0}%
                    </Badge>
                  </div>
                  
                  <Progress value={studentProfile.primary_style_percentage || 0} className="h-2" />
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <h4 className="font-medium mb-2">Caractéristiques du style:</h4>
                      <ul className="text-sm text-muted-foreground space-y-1">
                        {studentProfile.learning_style === 'Visuel' && (
                          <>
                            <li>• Préfère les diagrammes et schémas</li>
                            <li>• Mémorise par l'image</li>
                            <li>• Aime les couleurs et les graphiques</li>
                          </>
                        )}
                        {studentProfile.learning_style === 'Auditif' && (
                          <>
                            <li>• Apprend mieux en écoutant</li>
                            <li>• Aime les discussions</li>
                            <li>• Mémorise par la parole</li>
                          </>
                        )}
                        {studentProfile.learning_style === 'Kinesthésique' && (
                          <>
                            <li>• Apprend par l'action</li>
                            <li>• Préfère les expériences pratiques</li>
                            <li>• Aime manipuler les objets</li>
                          </>
                        )}
                        {studentProfile.learning_style === 'Lecture/Écriture' && (
                          <>
                            <li>• Préfère lire et écrire</li>
                            <li>• Aime prendre des notes</li>
                            <li>• Mémorise par l'écrit</li>
                          </>
                        )}
                      </ul>
                    </div>
                    
                    <div>
                      <h4 className="font-medium mb-2">Niveau de confiance:</h4>
                      <div className="flex items-center gap-2">
                        <Progress value={studentProfile.confidence_score || 0} className="flex-1" />
                        <span className="text-sm font-medium">{studentProfile.confidence_score || 0}%</span>
                      </div>
                      <p className="text-xs text-muted-foreground mt-1">
                        Fiabilité de l'analyse cognitive
                      </p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Forces et faiblesses */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {studentProfile.cognitive_strengths && studentProfile.cognitive_strengths.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <TrendingUp className="h-5 w-5 text-green-500" />
                    Forces Cognitives
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {studentProfile.cognitive_strengths.map((strength, index) => (
                      <div key={index} className="flex items-start gap-2 p-2 bg-green-50 rounded-lg">
                        <Target className="h-4 w-4 mt-0.5 text-green-500" />
                        <span className="text-sm">{strength}</span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}

            {studentProfile.cognitive_weaknesses && studentProfile.cognitive_weaknesses.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Target className="h-5 w-5 text-orange-500" />
                    Zones d'Amélioration
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {studentProfile.cognitive_weaknesses.map((weakness, index) => (
                      <div key={index} className="flex items-start gap-2 p-2 bg-orange-50 rounded-lg">
                        <Lightbulb className="h-4 w-4 mt-0.5 text-orange-500" />
                        <span className="text-sm">{weakness}</span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Recommandations */}
          {studentProfile.recommendations && studentProfile.recommendations.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Lightbulb className="h-5 w-5 text-yellow-500" />
                  Recommandations Personnalisées
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {studentProfile.recommendations.map((rec, index) => (
                    <div key={index} className="flex items-start gap-2 p-3 bg-yellow-50 rounded-lg">
                      <Lightbulb className="h-4 w-4 mt-0.5 text-yellow-500" />
                      <span className="text-sm">{rec}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      )}

      {/* Analyse de classe */}
      {classAnalysis && (
        <div className="space-y-6">
          {/* Distribution des styles */}
          {classAnalysis.learning_style_distribution && Object.keys(classAnalysis.learning_style_distribution).length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Users className="h-5 w-5" />
                  Distribution des Styles d'Apprentissage
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {Object.entries(classAnalysis.learning_style_distribution).map(([style, count]) => (
                    <div key={style} className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        {getLearningStyleIcon(style)}
                        <span className="font-medium">{style}</span>
                      </div>
                      <Badge variant="outline">{count} étudiants</Badge>
                    </div>
                  ))}
                  
                  {classAnalysis.dominant_learning_style && (
                    <div className="mt-4 p-3 bg-blue-50 rounded-lg">
                      <div className="flex items-center gap-2">
                        <Target className="h-4 w-4 text-blue-500" />
                        <span className="font-medium">Style dominant: {classAnalysis.dominant_learning_style}</span>
                      </div>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Patterns de classe */}
          {classAnalysis.class_patterns && classAnalysis.class_patterns.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle>Patterns Cognitifs de la Classe</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {classAnalysis.class_patterns.map((pattern, index) => (
                    <div key={index} className="flex items-start gap-2 p-3 bg-purple-50 rounded-lg">
                      <Brain className="h-4 w-4 mt-0.5 text-purple-500" />
                      <span className="text-sm">{pattern}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Recommandations d'enseignement */}
          {classAnalysis.teaching_recommendations && classAnalysis.teaching_recommendations.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <BookOpen className="h-5 w-5 text-blue-500" />
                  Recommandations d'Enseignement
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {classAnalysis.teaching_recommendations.map((rec, index) => (
                    <div key={index} className="flex items-start gap-2 p-3 bg-blue-50 rounded-lg">
                      <Lightbulb className="h-4 w-4 mt-0.5 text-blue-500" />
                      <span className="text-sm">{rec}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      )}
    </div>
  );
};

export default CognitiveDiagnostic; 