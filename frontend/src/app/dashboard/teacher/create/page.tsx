'use client';

import React, { useState, useEffect } from 'react';
import Sidebar from '../../../../components/Sidebar';
import { useAuth  } from '../../../../hooks/useAuth';
import { Plus, Award, BookOpen, Target, FileText, Video, Image, Upload, Save, X } from 'lucide-react';

interface QuizForm {
  title: string;
  description: string;
  subject: string;
  time_limit: number;
  questions: Array<{
    question_text: string;
    options: string[];
    correct_answer: number;
    points: number;
  }>;
}

interface ContentForm {
  title: string;
  description: string;
  content_type: 'text' | 'video' | 'pdf' | 'image';
  content: string;
  subject: string;
  tags: string[];
  learning_objectives: string[];
}

interface LearningPathForm {
  title: string;
  description: string;
  subject: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  estimated_duration: number;
  contents: number[];
}

export default function TeacherCreate() {
  const { user, token } = useAuth();
  const [activeTab, setActiveTab] = useState<'quiz' | 'content' | 'path'>('quiz');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  // États pour les formulaires
  const [quizForm, setQuizForm] = useState<QuizForm>({
    title: '',
    description: '',
    subject: '',
    time_limit: 30,
    questions: [
      {
        question_text: '',
        options: ['', '', '', ''],
        correct_answer: 0,
        points: 1
      }
    ]
  });

  const [contentForm, setContentForm] = useState<ContentForm>({
    title: '',
    description: '',
    content_type: 'text',
    content: '',
    subject: '',
    tags: [],
    learning_objectives: []
  });

  const [learningPathForm, setLearningPathForm] = useState<LearningPathForm>({
    title: '',
    description: '',
    subject: '',
    difficulty: 'intermediate',
    estimated_duration: 60,
    contents: []
  });

  const [availableContents, setAvailableContents] = useState<Array<{id: number, title: string}>>([]);

  useEffect(() => {
    if (token) {
      fetchAvailableContents();
    }
  }, [token]);

  const fetchAvailableContents = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/contents/`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setAvailableContents(data);
      }
    } catch (err) {
      console.error('Erreur lors du chargement des contenus:', err);
    }
  };

  const addQuestion = () => {
    setQuizForm({
      ...quizForm,
      questions: [
        ...quizForm.questions,
        {
          question_text: '',
          options: ['', '', '', ''],
          correct_answer: 0,
          points: 1
        }
      ]
    });
  };

  const removeQuestion = (index: number) => {
    setQuizForm({
      ...quizForm,
      questions: quizForm.questions.filter((_, i) => i !== index)
    });
  };

  const updateQuestion = (index: number, field: string, value: any) => {
    const updatedQuestions = [...quizForm.questions];
    updatedQuestions[index] = { ...updatedQuestions[index], [field]: value };
    setQuizForm({ ...quizForm, questions: updatedQuestions });
  };

  const updateQuestionOption = (questionIndex: number, optionIndex: number, value: string) => {
    const updatedQuestions = [...quizForm.questions];
    updatedQuestions[questionIndex].options[optionIndex] = value;
    setQuizForm({ ...quizForm, questions: updatedQuestions });
  };

  const createQuiz = async () => {
    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/quizzes/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(quizForm)
      });

      if (response.ok) {
        setSuccess('Quiz créé avec succès !');
        setQuizForm({
          title: '',
          description: '',
          subject: '',
          time_limit: 30,
          questions: [
            {
              question_text: '',
              options: ['', '', '', ''],
              correct_answer: 0,
              points: 1
            }
          ]
        });
      } else {
        setError('Erreur lors de la création du quiz');
      }
    } catch (err) {
      setError('Erreur de connexion');
    } finally {
      setLoading(false);
    }
  };

  const createContent = async () => {
    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/contents/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(contentForm)
      });

      if (response.ok) {
        setSuccess('Contenu créé avec succès !');
        setContentForm({
          title: '',
          description: '',
          content_type: 'text',
          content: '',
          subject: '',
          tags: [],
          learning_objectives: []
        });
      } else {
        setError('Erreur lors de la création du contenu');
      }
    } catch (err) {
      setError('Erreur de connexion');
    } finally {
      setLoading(false);
    }
  };

  const createLearningPath = async () => {
    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/learning-paths/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(learningPathForm)
      });

      if (response.ok) {
        setSuccess('Parcours d\'apprentissage créé avec succès !');
        setLearningPathForm({
          title: '',
          description: '',
          subject: '',
          difficulty: 'intermediate',
          estimated_duration: 60,
          contents: []
        });
      } else {
        setError('Erreur lors de la création du parcours');
      }
    } catch (err) {
      setError('Erreur de connexion');
    } finally {
      setLoading(false);
    }
  };

  const addTag = (tag: string) => {
    if (tag && !contentForm.tags.includes(tag)) {
      setContentForm({
        ...contentForm,
        tags: [...contentForm.tags, tag]
      });
    }
  };

  const removeTag = (tagToRemove: string) => {
    setContentForm({
      ...contentForm,
      tags: contentForm.tags.filter(tag => tag !== tagToRemove)
    });
  };

  const addLearningObjective = (objective: string) => {
    if (objective && !contentForm.learning_objectives.includes(objective)) {
      setContentForm({
        ...contentForm,
        learning_objectives: [...contentForm.learning_objectives, objective]
      });
    }
  };

  const removeLearningObjective = (objectiveToRemove: string) => {
    setContentForm({
      ...contentForm,
      learning_objectives: contentForm.learning_objectives.filter(obj => obj !== objectiveToRemove)
    });
  };

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar userType="teacher" />
      <div className="flex-1 overflow-auto pl-0 md:pl-56">
        <div className="p-6">
          {/* Header */}
          <div className="mb-6">
            <h1 className="text-3xl font-bold text-gray-800 mb-2">Créer</h1>
            <p className="text-gray-600">Créez du contenu pédagogique pour vos élèves</p>
          </div>

          {/* Messages de succès/erreur */}
          {success && (
            <div className="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg">
              <p className="text-green-800">{success}</p>
            </div>
          )}
          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-800">{error}</p>
            </div>
          )}

          {/* Navigation des onglets */}
          <div className="mb-6">
            <div className="flex space-x-1 bg-white rounded-lg p-1 shadow-sm">
              {[
                { id: 'quiz', label: 'Quiz', icon: <Award size={16} /> },
                { id: 'content', label: 'Contenu', icon: <BookOpen size={16} /> },
                { id: 'path', label: 'Parcours', icon: <Target size={16} /> }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`flex items-center gap-2 px-4 py-2 rounded-md font-medium transition ${
                    activeTab === tab.id
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  {tab.icon}
                  {tab.label}
                </button>
              ))}
            </div>
          </div>

          {/* Contenu des onglets */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            {/* Onglet Quiz */}
            {activeTab === 'quiz' && (
              <div className="space-y-6">
                <div className="flex items-center gap-2 mb-4">
                  <Award className="text-blue-600" size={20} />
                  <h2 className="text-lg font-bold text-gray-800">Créer un Quiz</h2>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Titre du quiz</label>
                    <input
                      type="text"
                      value={quizForm.title}
                      onChange={(e) => setQuizForm({ ...quizForm, title: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Ex: Quiz sur la Révolution française"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Matière</label>
                    <input
                      type="text"
                      value={quizForm.subject}
                      onChange={(e) => setQuizForm({ ...quizForm, subject: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Ex: Histoire"
                    />
                  </div>

                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
                    <textarea
                      value={quizForm.description}
                      onChange={(e) => setQuizForm({ ...quizForm, description: e.target.value })}
                      rows={3}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Description du quiz..."
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Temps limite (minutes)</label>
                    <input
                      type="number"
                      value={quizForm.time_limit}
                      onChange={(e) => setQuizForm({ ...quizForm, time_limit: parseInt(e.target.value) })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      min="1"
                    />
                  </div>
                </div>

                {/* Questions */}
                <div className="space-y-6">
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-semibold text-gray-800">Questions</h3>
                    <button
                      onClick={addQuestion}
                      className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
                    >
                      <Plus size={16} />
                      Ajouter une question
                    </button>
                  </div>

                  {quizForm.questions.map((question, questionIndex) => (
                    <div key={questionIndex} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex items-center justify-between mb-4">
                        <h4 className="font-medium text-gray-800">Question {questionIndex + 1}</h4>
                        {quizForm.questions.length > 1 && (
                          <button
                            onClick={() => removeQuestion(questionIndex)}
                            className="text-red-600 hover:text-red-700"
                          >
                            <X size={16} />
                          </button>
                        )}
                      </div>

                      <div className="space-y-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">Question</label>
                          <input
                            type="text"
                            value={question.question_text}
                            onChange={(e) => updateQuestion(questionIndex, 'question_text', e.target.value)}
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="Posez votre question..."
                          />
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          {question.options.map((option, optionIndex) => (
                            <div key={optionIndex}>
                              <label className="block text-sm font-medium text-gray-700 mb-2">
                                Option {optionIndex + 1}
                              </label>
                              <div className="flex items-center gap-2">
                                <input
                                  type="radio"
                                  name={`correct-${questionIndex}`}
                                  checked={question.correct_answer === optionIndex}
                                  onChange={() => updateQuestion(questionIndex, 'correct_answer', optionIndex)}
                                  className="text-blue-600"
                                />
                                <input
                                  type="text"
                                  value={option}
                                  onChange={(e) => updateQuestionOption(questionIndex, optionIndex, e.target.value)}
                                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                                  placeholder={`Option ${optionIndex + 1}`}
                                />
                              </div>
                            </div>
                          ))}
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">Points</label>
                          <input
                            type="number"
                            value={question.points}
                            onChange={(e) => updateQuestion(questionIndex, 'points', parseInt(e.target.value))}
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                            min="1"
                          />
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="flex justify-end">
                  <button
                    onClick={createQuiz}
                    disabled={loading || !quizForm.title || !quizForm.subject}
                    className="flex items-center gap-2 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
                  >
                    <Save size={16} />
                    {loading ? 'Création...' : 'Créer le Quiz'}
                  </button>
                </div>
              </div>
            )}

            {/* Onglet Contenu */}
            {activeTab === 'content' && (
              <div className="space-y-6">
                <div className="flex items-center gap-2 mb-4">
                  <BookOpen className="text-blue-600" size={20} />
                  <h2 className="text-lg font-bold text-gray-800">Créer du Contenu</h2>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Titre</label>
                    <input
                      type="text"
                      value={contentForm.title}
                      onChange={(e) => setContentForm({ ...contentForm, title: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Titre du contenu"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Matière</label>
                    <input
                      type="text"
                      value={contentForm.subject}
                      onChange={(e) => setContentForm({ ...contentForm, subject: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Ex: Mathématiques"
                    />
                  </div>

                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
                    <textarea
                      value={contentForm.description}
                      onChange={(e) => setContentForm({ ...contentForm, description: e.target.value })}
                      rows={3}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Description du contenu..."
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Type de contenu</label>
                    <select
                      value={contentForm.content_type}
                      onChange={(e) => setContentForm({ ...contentForm, content_type: e.target.value as any })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="text">Texte</option>
                      <option value="video">Vidéo</option>
                      <option value="pdf">PDF</option>
                      <option value="image">Image</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Contenu</label>
                  {contentForm.content_type === 'text' ? (
                    <textarea
                      value={contentForm.content}
                      onChange={(e) => setContentForm({ ...contentForm, content: e.target.value })}
                      rows={10}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Votre contenu ici..."
                    />
                  ) : (
                    <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                      <Upload className="mx-auto text-gray-400 mb-4" size={48} />
                      <p className="text-gray-600">Glissez-déposez votre fichier ici ou cliquez pour sélectionner</p>
                      <input
                        type="file"
                        accept={contentForm.content_type === 'video' ? 'video/*' : contentForm.content_type === 'pdf' ? '.pdf' : 'image/*'}
                        className="hidden"
                      />
                    </div>
                  )}
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Tags</label>
                    <div className="space-y-2">
                      <div className="flex gap-2">
                        <input
                          type="text"
                          placeholder="Ajouter un tag..."
                          onKeyPress={(e) => {
                            if (e.key === 'Enter') {
                              e.preventDefault();
                              addTag(e.currentTarget.value);
                              e.currentTarget.value = '';
                            }
                          }}
                          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {contentForm.tags.map((tag, index) => (
                          <span
                            key={index}
                            className="flex items-center gap-1 px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
                          >
                            {tag}
                            <button
                              onClick={() => removeTag(tag)}
                              className="text-blue-600 hover:text-blue-800"
                            >
                              <X size={12} />
                            </button>
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Objectifs d'apprentissage</label>
                    <div className="space-y-2">
                      <div className="flex gap-2">
                        <input
                          type="text"
                          placeholder="Ajouter un objectif..."
                          onKeyPress={(e) => {
                            if (e.key === 'Enter') {
                              e.preventDefault();
                              addLearningObjective(e.currentTarget.value);
                              e.currentTarget.value = '';
                            }
                          }}
                          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                      </div>
                      <div className="space-y-1">
                        {contentForm.learning_objectives.map((objective, index) => (
                          <div
                            key={index}
                            className="flex items-center justify-between p-2 bg-green-50 rounded-lg"
                          >
                            <span className="text-sm text-green-800">{objective}</span>
                            <button
                              onClick={() => removeLearningObjective(objective)}
                              className="text-green-600 hover:text-green-800"
                            >
                              <X size={12} />
                            </button>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>

                <div className="flex justify-end">
                  <button
                    onClick={createContent}
                    disabled={loading || !contentForm.title || !contentForm.content}
                    className="flex items-center gap-2 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
                  >
                    <Save size={16} />
                    {loading ? 'Création...' : 'Créer le Contenu'}
                  </button>
                </div>
              </div>
            )}

            {/* Onglet Parcours */}
            {activeTab === 'path' && (
              <div className="space-y-6">
                <div className="flex items-center gap-2 mb-4">
                  <Target className="text-blue-600" size={20} />
                  <h2 className="text-lg font-bold text-gray-800">Créer un Parcours d'Apprentissage</h2>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Titre du parcours</label>
                    <input
                      type="text"
                      value={learningPathForm.title}
                      onChange={(e) => setLearningPathForm({ ...learningPathForm, title: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Ex: Introduction à l'algèbre"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Matière</label>
                    <input
                      type="text"
                      value={learningPathForm.subject}
                      onChange={(e) => setLearningPathForm({ ...learningPathForm, subject: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Ex: Mathématiques"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Difficulté</label>
                    <select
                      value={learningPathForm.difficulty}
                      onChange={(e) => setLearningPathForm({ ...learningPathForm, difficulty: e.target.value as any })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="beginner">Débutant</option>
                      <option value="intermediate">Intermédiaire</option>
                      <option value="advanced">Avancé</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Durée estimée (minutes)</label>
                    <input
                      type="number"
                      value={learningPathForm.estimated_duration}
                      onChange={(e) => setLearningPathForm({ ...learningPathForm, estimated_duration: parseInt(e.target.value) })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      min="1"
                    />
                  </div>

                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
                    <textarea
                      value={learningPathForm.description}
                      onChange={(e) => setLearningPathForm({ ...learningPathForm, description: e.target.value })}
                      rows={4}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Description du parcours d'apprentissage..."
                    />
                  </div>

                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-2">Contenus à inclure</label>
                    <div className="space-y-2 max-h-48 overflow-y-auto border border-gray-300 rounded-lg p-4">
                      {availableContents.length === 0 ? (
                        <p className="text-gray-500 text-center py-4">Aucun contenu disponible</p>
                      ) : (
                        availableContents.map((content) => (
                          <label key={content.id} className="flex items-center gap-2 p-2 hover:bg-gray-50 rounded">
                            <input
                              type="checkbox"
                              checked={learningPathForm.contents.includes(content.id)}
                              onChange={(e) => {
                                if (e.target.checked) {
                                  setLearningPathForm({
                                    ...learningPathForm,
                                    contents: [...learningPathForm.contents, content.id]
                                  });
                                } else {
                                  setLearningPathForm({
                                    ...learningPathForm,
                                    contents: learningPathForm.contents.filter(id => id !== content.id)
                                  });
                                }
                              }}
                              className="text-blue-600"
                            />
                            <span className="text-sm">{content.title}</span>
                          </label>
                        ))
                      )}
                    </div>
                  </div>
                </div>

                <div className="flex justify-end">
                  <button
                    onClick={createLearningPath}
                    disabled={loading || !learningPathForm.title || !learningPathForm.subject}
                    className="flex items-center gap-2 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
                  >
                    <Save size={16} />
                    {loading ? 'Création...' : 'Créer le Parcours'}
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
} 