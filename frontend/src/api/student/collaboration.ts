import { apiClient } from '../apiClient';

export interface StudyGroup {
  id: number;
  name: string;
  description?: string;
  subject?: string;
  max_members: number;
  is_public: boolean;
  created_by: number;
  created_at: string;
  members_count?: number;
}

export interface GroupMessage {
  id: number;
  group_id: number;
  user_id: number;
  content: string;
  message_type: string;
  attachments?: string[];
  created_at: string;
  user_name?: string;
}

export interface GroupResource {
  id: number;
  group_id: number;
  title: string;
  description?: string;
  resource_type: string;
  file_url?: string;
  file_size?: number;
  uploaded_by: number;
  created_at: string;
}

export interface CollaborationProject {
  id: number;
  title: string;
  description?: string;
  subject?: string;
  status: string;
  due_date?: string;
  created_by: number;
  created_at: string;
  members_count?: number;
}

export interface ProjectTask {
  id: number;
  project_id: number;
  title: string;
  description?: string;
  assigned_to?: number;
  status: string;
  priority: string;
  due_date?: string;
  created_by: number;
  created_at: string;
}

export interface CreateStudyGroupData {
  name: string;
  description?: string;
  subject?: string;
  max_members?: number;
  is_public?: boolean;
}

export interface CreateGroupMessageData {
  content: string;
  message_type?: string;
  attachments?: string[];
}

export interface CreateGroupResourceData {
  title: string;
  description?: string;
  resource_type: string;
  file_url?: string;
  file_size?: number;
}

export interface CreateCollaborationProjectData {
  title: string;
  description?: string;
  subject?: string;
  due_date?: string;
}

export interface CreateProjectTaskData {
  title: string;
  description?: string;
  assigned_to?: number;
  priority?: string;
  due_date?: string;
}

class CollaborationAPI {
  // Groupes d'étude
  async getStudyGroups(subject?: string, is_public?: boolean): Promise<StudyGroup[]> {
    const params = new URLSearchParams();
    if (subject) params.append('subject', subject);
    if (is_public !== undefined) params.append('is_public', is_public.toString());
    
    return this.request(`/api/v1/collaboration/study-groups?${params.toString()}`);
  }

  async createStudyGroup(data: CreateStudyGroupData): Promise<StudyGroup> {
    return this.request('/api/v1/collaboration/study-groups', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async joinStudyGroup(groupId: number): Promise<void> {
    return this.request(`/api/v1/collaboration/study-groups/${groupId}/join`, {
      method: 'POST',
    });
  }

  // Messages de groupe
  async getGroupMessages(groupId: number, limit?: number, offset?: number): Promise<GroupMessage[]> {
    const params = new URLSearchParams();
    if (limit) params.append('limit', limit.toString());
    if (offset) params.append('offset', offset.toString());
    
    return this.request(`/api/v1/collaboration/study-groups/${groupId}/messages?${params.toString()}`);
  }

  async createGroupMessage(groupId: number, data: CreateGroupMessageData): Promise<GroupMessage> {
    return this.request(`/api/v1/collaboration/study-groups/${groupId}/messages`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Ressources de groupe
  async getGroupResources(groupId: number): Promise<GroupResource[]> {
    return this.request(`/api/v1/collaboration/study-groups/${groupId}/resources`);
  }

  async createGroupResource(groupId: number, data: CreateGroupResourceData): Promise<GroupResource> {
    return this.request(`/api/v1/collaboration/study-groups/${groupId}/resources`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Projets collaboratifs
  async getCollaborationProjects(status?: string, subject?: string): Promise<CollaborationProject[]> {
    const params = new URLSearchParams();
    if (status) params.append('status', status);
    if (subject) params.append('subject', subject);
    
    return this.request(`/api/v1/collaboration/projects?${params.toString()}`);
  }

  async createCollaborationProject(data: CreateCollaborationProjectData): Promise<CollaborationProject> {
    return this.request('/api/v1/collaboration/projects', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Tâches de projet
  async getProjectTasks(projectId: number, status?: string, assigned_to?: number): Promise<ProjectTask[]> {
    const params = new URLSearchParams();
    if (status) params.append('status', status);
    if (assigned_to) params.append('assigned_to', assigned_to.toString());
    
    return this.request(`/api/v1/collaboration/projects/${projectId}/tasks?${params.toString()}`);
  }

  async createProjectTask(projectId: number, data: CreateProjectTaskData): Promise<ProjectTask> {
    return this.request(`/api/v1/collaboration/projects/${projectId}/tasks`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const response = await apiClient.request<T>(endpoint, options);
    return response.data;
  }
}

export const collaborationAPI = new CollaborationAPI();
