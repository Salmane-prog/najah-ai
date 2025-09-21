'use client';

import React, { useState, useEffect } from 'react';
import AdvancedAssessmentInterface from './AdvancedAssessmentInterface';

interface AssessmentWrapperProps {
  studentId: number;
  studentName: string;
  onComplete?: (results: any) => void;
  onClose?: () => void;
  mode?: 'evaluation' | 'practice' | 'diagnostic';
}

const AssessmentWrapper: React.FC<AssessmentWrapperProps> = ({
  studentId,
  studentName,
  onComplete,
  onClose,
  mode = 'evaluation'
}) => {
  const [isLoading, setIsLoading] = useState(true);
  const [questions, setQuestions] = useState([]);
  const [assessmentConfig, setAssessmentConfig] = useState({
    subject: 'math',
    difficulty: 5,
    questionCount: 10,
    timeLimit: 30 * 60, // 30 minutes
    adaptive: true
  });

  useEffect(() => {
    loadAssessmentConfiguration();
  }, []);

  const loadAssessmentConfiguration = async () => {
    try {
      setIsLoading(true);
      
      // Charger la configuration depuis l'API
      const response = await fetch(`/api/v1/advanced/questions/extended?subject=${assessmentConfig.subject}&difficulty=${assessmentConfig.difficulty}&limit=${assessmentConfig.questionCount}`);
      
      if (response.ok) {
        const data = await response.json();
        setQuestions(data.questions || []);
      } else {
        console.error('Erreur lors du chargement des questions');
        // Utiliser des questions par défaut
        setQuestions(generateDefaultQuestions());
      }
    } catch (error) {
      console.error('Erreur de connexion:', error);
      setQuestions(generateDefaultQuestions());
    } finally {
      setIsLoading(false);
    }
  };

  const generateDefaultQuestions = () => {
    // Questions par défaut si l'API n'est pas disponible
    return [
      {
        id: 1,
        question_text: "Quel est le résultat de 15 + 27 ?",
        question_type: "multiple_choice",
        subject: "math",
        difficulty: 3,
        options: ["40", "41", "42", "43"],
        correct_answer: "42",
        explanation: "15 + 27 = 42",
        estimated_time: 30,
        cognitive_load: 0.3
      },
      {
        id: 2,
        question_text: "Complétez la phrase : 'Le chat ___ sur le toit.'",
        question_type: "free_text",
        subject: "french",
        difficulty: 4,
        correct_answer: "dort",
        explanation: "Le verbe 'dormir' à la 3ème personne du singulier",
        estimated_time: 45,
        cognitive_load: 0.4
      }
    ];
  };

  const handleAssessmentComplete = async (results: any) => {
    try {
      // Envoyer les résultats à l'API pour analyse cognitive
      const analysisResponse = await fetch('/api/v1/advanced/cognitive/generate-profile', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          student_responses: results.responses
        })
      });

      if (analysisResponse.ok) {
        const cognitiveProfile = await analysisResponse.json();
        console.log('Profil cognitif généré:', cognitiveProfile);
      }

      // Appeler le callback de completion
      if (onComplete) {
        onComplete({
          ...results,
          cognitiveProfile: cognitiveProfile?.cognitive_profile
        });
      }
    } catch (error) {
      console.error('Erreur lors de l\'analyse cognitive:', error);
      
      // Appeler le callback même en cas d'erreur
      if (onComplete) {
        onComplete(results);
      }
    }
  };

  const handleClose = () => {
    if (onClose) {
      onClose();
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-indigo-600 mx-auto mb-4"></div>
          <h2 className="text-xl font-semibold text-gray-700 mb-2">
            Chargement de l'évaluation...
          </h2>
          <p className="text-gray-500">
            Préparation de votre session personnalisée
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="fixed inset-0 z-50 bg-white">
      <AdvancedAssessmentInterface
        studentId={studentId}
        studentName={studentName}
        questions={questions}
        config={assessmentConfig}
        onComplete={handleAssessmentComplete}
        onClose={handleClose}
        mode={mode}
      />
    </div>
  );
};

export default AssessmentWrapper;















