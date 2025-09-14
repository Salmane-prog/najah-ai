'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Users, MessageSquare, FileText, Plus, UserPlus, Calendar } from 'lucide-react';
import { collaborationAPI, StudyGroup, GroupMessage, CollaborationProject } from '@/api/student/collaboration';
import { useAuth  } from '@/hooks/useAuth';

interface CollaborationWidgetProps {
  className?: string;
}

export default function CollaborationWidget({ className }: CollaborationWidgetProps) {
  const { user } = useAuth();
  const [studyGroups, setStudyGroups] = useState<StudyGroup[]>([]);
  const [projects, setProjects] = useState<CollaborationProject[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedTab, setSelectedTab] = useState<'groups' | 'projects'>('groups');

  useEffect(() => {
    loadCollaborationData();
  }, []);

  const loadCollaborationData = async () => {
    try {
      setLoading(true);
      const [groupsData, projectsData] = await Promise.all([
        collaborationAPI.getStudyGroups(),
        collaborationAPI.getCollaborationProjects()
      ]);

      setStudyGroups(groupsData);
      setProjects(projectsData);
    } catch (err) {
      setError('Erreur lors du chargement des données de collaboration');
      console.error('Erreur:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleJoinGroup = async (groupId: number) => {
    try {
      await collaborationAPI.joinStudyGroup(groupId);
      await loadCollaborationData(); // Recharger les données
    } catch (err) {
      console.error('Erreur lors de la jointure du groupe:', err);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
    });
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800';
      case 'completed':
        return 'bg-blue-100 text-blue-800';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Users className="w-5 h-5" />
            Collaboration
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="animate-pulse space-y-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="flex items-center space-x-4">
                <div className="w-4 h-4 bg-gray-200 rounded"></div>
                <div className="flex-1 space-y-2">
                  <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                  <div className="h-3 bg-gray-200 rounded w-1/2"></div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Users className="w-5 h-5" />
            Collaboration
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center text-red-500">
            <Users className="w-8 h-8 mx-auto mb-2" />
            <p>{error}</p>
            <Button onClick={loadCollaborationData} className="mt-2">
              Réessayer
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <Users className="w-5 h-5" />
            Collaboration
          </CardTitle>
          <div className="flex gap-2">
            <Button
              variant={selectedTab === 'groups' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setSelectedTab('groups')}
            >
              Groupes d'étude
            </Button>
            <Button
              variant={selectedTab === 'projects' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setSelectedTab('projects')}
            >
              Projets
            </Button>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-4 max-h-96 overflow-y-auto">
          {selectedTab === 'groups' ? (
            <>
              {studyGroups.length === 0 ? (
                <div className="text-center text-gray-500 py-8">
                  <Users className="w-12 h-12 mx-auto mb-2 opacity-50" />
                  <p>Aucun groupe d'étude disponible</p>
                </div>
              ) : (
                studyGroups.map((group) => (
                  <div key={group.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <h3 className="font-semibold text-gray-900">{group.name}</h3>
                          <Badge className={group.is_public ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'}>
                            {group.is_public ? 'Public' : 'Privé'}
                          </Badge>
                        </div>
                        <p className="text-sm text-gray-600 mb-2">{group.description}</p>
                        <div className="flex items-center gap-4 text-sm text-gray-500">
                          {group.subject && (
                            <div className="flex items-center gap-1">
                              <FileText className="w-4 h-4" />
                              <span>{group.subject}</span>
                            </div>
                          )}
                          <div className="flex items-center gap-1">
                            <Users className="w-4 h-4" />
                            <span>{group.members_count || 0}/{group.max_members} membres</span>
                          </div>
                          <div className="flex items-center gap-1">
                            <Calendar className="w-4 h-4" />
                            <span>Créé le {formatDate(group.created_at)}</span>
                          </div>
                        </div>
                      </div>
                      <Button
                        size="sm"
                        onClick={() => handleJoinGroup(group.id)}
                        className="ml-4"
                      >
                        <UserPlus className="w-4 h-4 mr-1" />
                        Rejoindre
                      </Button>
                    </div>
                  </div>
                ))
              )}
            </>
          ) : (
            <>
              {projects.length === 0 ? (
                <div className="text-center text-gray-500 py-8">
                  <FileText className="w-12 h-12 mx-auto mb-2 opacity-50" />
                  <p>Aucun projet collaboratif disponible</p>
                </div>
              ) : (
                projects.map((project) => (
                  <div key={project.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <h3 className="font-semibold text-gray-900">{project.title}</h3>
                          <Badge className={getStatusColor(project.status)}>
                            {project.status}
                          </Badge>
                        </div>
                        <p className="text-sm text-gray-600 mb-2">{project.description}</p>
                        <div className="flex items-center gap-4 text-sm text-gray-500">
                          {project.subject && (
                            <div className="flex items-center gap-1">
                              <FileText className="w-4 h-4" />
                              <span>{project.subject}</span>
                            </div>
                          )}
                          <div className="flex items-center gap-1">
                            <Users className="w-4 h-4" />
                            <span>{project.members_count || 0} participants</span>
                          </div>
                          {project.due_date && (
                            <div className="flex items-center gap-1">
                              <Calendar className="w-4 h-4" />
                              <span>Échéance: {formatDate(project.due_date)}</span>
                            </div>
                          )}
                        </div>
                      </div>
                      <Button size="sm" variant="outline" className="ml-4">
                        <MessageSquare className="w-4 h-4 mr-1" />
                        Voir
                      </Button>
                    </div>
                  </div>
                ))
              )}
            </>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
