'use client';

import React, { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { ArrowLeft, BookOpen, CheckCircle, Clock, Target, Lightbulb } from 'lucide-react';

interface ReadingContent {
  title: string;
  content: string[];
  keyPoints: string[];
  exercises: string[];
  estimatedTime: number;
}

export default function RemediationReadingPage() {
  const { topic } = useParams();
  const router = useRouter();
  const { user, token } = useAuth();
  
  const [currentSection, setCurrentSection] = useState(0);
  const [readingProgress, setReadingProgress] = useState(0);
  const [completedSections, setCompletedSections] = useState<number[]>([]);
  const [timeSpent, setTimeSpent] = useState(0);
  const [readingCompleted, setReadingCompleted] = useState(false);

  const [readingContent, setReadingContent] = useState<ReadingContent | null>(null);

  useEffect(() => {
    if (topic) {
      generateReadingContent(topic as string);
    }
  }, [topic]);

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeSpent(prev => prev + 1);
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const generateReadingContent = (topic: string) => {
    const contentMap: { [key: string]: ReadingContent } = {
      'fondamentaux': {
        title: "Les Fondamentaux de la Grammaire Française",
        content: [
          "La grammaire française est l'ensemble des règles qui régissent la structure et l'organisation de la langue française. Elle comprend plusieurs éléments essentiels que tout apprenant doit maîtriser.",
          "Les noms sont des mots qui désignent des personnes, des animaux, des choses ou des idées. Ils peuvent être masculins ou féminins, singuliers ou pluriels. Par exemple : 'table' (féminin singulier), 'livres' (masculin pluriel).",
          "Les articles accompagnent les noms et indiquent leur genre et leur nombre. Il existe trois types d'articles : définis (le, la, les), indéfinis (un, une, des) et partitifs (du, de la, des).",
          "Les adjectifs qualifient les noms et s'accordent en genre et en nombre avec eux. Par exemple : 'une belle table' (féminin singulier), 'de beaux livres' (masculin pluriel)."
        ],
        keyPoints: [
          "Les noms ont un genre (masculin/féminin) et un nombre (singulier/pluriel)",
          "Les articles s'accordent avec les noms",
          "Les adjectifs s'accordent en genre et en nombre",
          "La structure de base est : Article + Adjectif + Nom"
        ],
        exercises: [
          "Identifiez le genre et le nombre des noms dans une phrase",
          "Choisissez le bon article selon le contexte",
          "Accordez les adjectifs avec les noms",
          "Construisez des phrases avec la structure correcte"
        ],
        estimatedTime: 15
      },
      'conjugaison': {
        title: "Maîtriser la Conjugaison Française",
        content: [
          "La conjugaison est l'art de faire varier les verbes selon la personne, le temps et le mode. En français, elle peut sembler complexe mais suit des règles logiques.",
          "Les verbes du premier groupe (en -er) sont les plus réguliers. Au présent, ils suivent le modèle : je parle, tu parles, il/elle parle, nous parlons, vous parlez, ils/elles parlent.",
          "Les verbes du deuxième groupe (en -ir) comme 'finir' se conjuguent : je finis, tu finis, il/elle finit, nous finissons, vous finissez, ils/elles finissent.",
          "Les verbes du troisième groupe sont irréguliers et doivent être appris individuellement. Parmi les plus courants : être, avoir, faire, dire, venir, aller."
        ],
        keyPoints: [
          "Trois groupes de verbes avec des règles différentes",
          "Le premier groupe (-er) est le plus régulier",
          "Le deuxième groupe (-ir) suit un modèle spécifique",
          "Le troisième groupe contient les verbes irréguliers"
        ],
        exercises: [
          "Conjuguez des verbes du premier groupe au présent",
          "Identifiez le groupe d'un verbe",
          "Conjuguez des verbes irréguliers courants",
          "Pratiquez la conjugaison dans des phrases"
        ],
        estimatedTime: 20
      },
      'vocabulaire': {
        title: "Enrichir son Vocabulaire Français",
        content: [
          "Le vocabulaire est l'ensemble des mots d'une langue. En français, il est particulièrement riche et permet d'exprimer des nuances subtiles.",
          "Les synonymes sont des mots de sens proche. Par exemple : 'rapide', 'vite', 'prompt', 'accéléré' expriment tous l'idée de vitesse mais avec des nuances différentes.",
          "Les antonymes sont des mots de sens opposé. 'Grand' s'oppose à 'petit', 'chaud' à 'froid', 'jour' à 'nuit'. Connaître les antonymes aide à comprendre le sens des mots.",
          "Un champ lexical regroupe des mots qui appartiennent au même domaine. Par exemple, le champ lexical de 'cuisine' comprend : cuisiner, mijoter, rôtir, assaisonner, déguster, etc."
        ],
        keyPoints: [
          "Les synonymes expriment des nuances différentes",
          "Les antonymes aident à comprendre le sens",
          "Les champs lexicaux organisent le vocabulaire",
          "Le contexte aide à choisir le bon mot"
        ],
        exercises: [
          "Trouvez des synonymes pour enrichir vos phrases",
          "Identifiez les antonymes de mots donnés",
          "Construisez des champs lexicaux",
          "Utilisez le vocabulaire dans des contextes variés"
        ],
        estimatedTime: 15
      }
    };

    setReadingContent(contentMap[topic.toLowerCase()] || contentMap['fondamentaux']);
  };

  const handleSectionComplete = async () => {
    if (!completedSections.includes(currentSection)) {
      setCompletedSections(prev => [...prev, currentSection]);
    }
    
    const newProgress = ((completedSections.length + 1) / (readingContent?.content.length || 1)) * 100;
    setReadingProgress(newProgress);

    if (currentSection < (readingContent?.content.length || 1) - 1) {
      setCurrentSection(prev => prev + 1);
    } else {
      setReadingCompleted(true);
      
      // Sauvegarder le résultat de lecture
      if (user && token && readingContent) {
        try {
          const { RemediationService } = await import('@/services/remediationService');
          
          const result = {
            student_id: user.id,
            topic: topic as string,
            exercise_type: 'reading' as const,
            score: completedSections.length + 1,
            max_score: readingContent.content.length,
            percentage: 100, // Lecture complète
            time_spent: timeSpent,
            weak_areas_improved: [topic as string],
          };
          
          await RemediationService.saveRemediationResult(token, result);
          console.log('✅ [READING] Résultat de lecture sauvegardé:', result);
          
          // Mettre à jour l'analyse des lacunes
          await RemediationService.updateGapAnalysis(token, user.id, 'Français');
          console.log('✅ [READING] Analyse des lacunes mise à jour');
          
        } catch (error) {
          console.error('❌ [READING] Erreur sauvegarde résultat:', error);
        }
      }
    }
  };

  const handlePreviousSection = () => {
    if (currentSection > 0) {
      setCurrentSection(prev => prev - 1);
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  if (!readingContent) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-4xl mx-auto">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p>Chargement du contenu de lecture...</p>
          </div>
        </div>
      </div>
    );
  }

  if (readingCompleted) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-4xl mx-auto">
          <Card className="mb-6">
            <CardHeader className="text-center">
              <CardTitle className="text-2xl text-green-600">
                Lecture Terminée ! 📚✨
              </CardTitle>
            </CardHeader>
            <CardContent className="text-center space-y-4">
              <div className="text-4xl font-bold text-blue-600">
                {completedSections.length}/{readingContent.content.length}
              </div>
              <div className="text-xl text-gray-600">
                Sections complétées
              </div>
              <Progress value={100} className="w-full max-w-md mx-auto" />
              
              <div className="text-gray-600">
                <p>Temps passé : {formatTime(timeSpent)}</p>
                <p>Temps estimé : {readingContent.estimatedTime} min</p>
              </div>

              <div className="mt-6 p-4 bg-blue-50 rounded-lg text-left">
                <h3 className="font-semibold text-blue-800 mb-2">Points Clés à Retenir :</h3>
                <ul className="space-y-1 text-blue-700">
                  {readingContent.keyPoints.map((point, index) => (
                    <li key={index} className="flex items-start space-x-2">
                      <CheckCircle className="w-4 h-4 text-blue-600 mt-0.5 flex-shrink-0" />
                      <span>{point}</span>
                    </li>
                  ))}
                </ul>
              </div>
              
              <div className="flex justify-center space-x-4 mt-6">
                <Button 
                  onClick={() => router.push('/dashboard/student/remediation')}
                  variant="outline"
                >
                  <ArrowLeft className="w-4 h-4 mr-2" />
                  Retour au Plan
                </Button>
                <Button 
                  onClick={() => window.location.reload()}
                  className="bg-blue-600 hover:bg-blue-700"
                >
                  Relire
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  const currentContent = readingContent.content[currentSection];
  const isSectionCompleted = completedSections.includes(currentSection);

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <Button 
            variant="outline" 
            onClick={() => router.push('/dashboard/student/remediation')}
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Retour
          </Button>
          
          <div className="text-center">
            <h1 className="text-2xl font-bold text-gray-900">
              {readingContent.title}
            </h1>
            <p className="text-gray-600">Section {currentSection + 1} sur {readingContent.content.length}</p>
          </div>

          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <Clock className="w-4 h-4 text-blue-500" />
              <span className="font-mono text-lg">{formatTime(timeSpent)}</span>
            </div>
            <Badge variant="secondary">
              {readingContent.estimatedTime} min estimées
            </Badge>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="mb-6">
          <Progress value={readingProgress} className="w-full" />
          <div className="flex justify-between text-sm text-gray-600 mt-1">
            <span>Progression de lecture</span>
            <span>{Math.round(readingProgress)}%</span>
          </div>
        </div>

        {/* Reading Content */}
        <Card className="mb-6">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="text-xl flex items-center space-x-2">
                <BookOpen className="w-5 h-5 text-blue-600" />
                <span>Section {currentSection + 1}</span>
              </CardTitle>
              <Badge variant={isSectionCompleted ? 'default' : 'secondary'}>
                {isSectionCompleted ? 'Terminée' : 'En cours'}
              </Badge>
            </div>
          </CardHeader>
          
          <CardContent className="space-y-6">
            {/* Content */}
            <div className="prose max-w-none">
              <p className="text-lg leading-relaxed text-gray-700">
                {currentContent}
              </p>
            </div>

            {/* Key Points Preview */}
            <div className="p-4 bg-yellow-50 rounded-lg border border-yellow-200">
              <div className="flex items-center space-x-2 mb-3">
                <Lightbulb className="w-5 h-5 text-yellow-600" />
                <h3 className="font-semibold text-yellow-800">Point Clé de cette Section :</h3>
              </div>
              <p className="text-yellow-700">
                {readingContent.keyPoints[currentSection]}
              </p>
            </div>

            {/* Exercise Preview */}
            <div className="p-4 bg-green-50 rounded-lg border border-green-200">
              <div className="flex items-center space-x-2 mb-3">
                <Target className="w-5 h-5 text-green-600" />
                <h3 className="font-semibold text-green-800">Exercice Associé :</h3>
              </div>
              <p className="text-green-700">
                {readingContent.exercises[currentSection]}
              </p>
            </div>

            {/* Navigation */}
            <div className="flex justify-between items-center pt-4 border-t">
              <Button 
                onClick={handlePreviousSection}
                disabled={currentSection === 0}
                variant="outline"
              >
                Section Précédente
              </Button>

              <Button 
                onClick={handleSectionComplete}
                className="bg-blue-600 hover:bg-blue-700"
              >
                {currentSection < readingContent.content.length - 1 ? 'Section Suivante' : 'Terminer la Lecture'}
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
