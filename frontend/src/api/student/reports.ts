import { apiClient } from '../apiClient';

export interface DetailedReport {
  id: number;
  user_id: number;
  report_type: string;
  title: string;
  description?: string;
  period_start: string;
  period_end: string;
  data: any;
  insights?: string;
  recommendations?: any;
  is_exported: boolean;
  exported_at?: string;
  created_at: string;
}

export interface SubjectProgressReport {
  id: number;
  user_id: number;
  subject: string;
  period_start: string;
  period_end: string;
  total_score: number;
  max_score: number;
  percentage: number;
  improvement_rate?: number;
  topics_covered?: any;
  strengths?: any;
  weaknesses?: any;
  recommendations?: any;
  created_at: string;
}

export interface AnalyticsReport {
  id: number;
  user_id: number;
  analytics_type: string;
  period_start: string;
  period_end: string;
  metrics: any;
  trends?: any;
  insights?: string;
  recommendations?: any;
  created_at: string;
}

export interface ReportExport {
  id: number;
  report_id: number;
  export_format: string;
  file_url?: string;
  file_size?: number;
  exported_at: string;
  status: string;
}

export interface CreateDetailedReportData {
  report_type: string;
  title: string;
  description?: string;
  period_start: string;
  period_end: string;
}

export interface CreateSubjectProgressReportData {
  subject: string;
  period_start: string;
  period_end: string;
}

export interface CreateAnalyticsReportData {
  analytics_type: string;
  period_start: string;
  period_end: string;
}

class ReportsAPI {
  // Rapports détaillés
  async getDetailedReports(report_type?: string, limit?: number): Promise<DetailedReport[]> {
    const params = new URLSearchParams();
    if (report_type) params.append('report_type', report_type);
    if (limit) params.append('limit', limit.toString());
    
    return this.request(`/api/v1/reports/detailed?${params.toString()}`);
  }

  async getDetailedReport(reportId: number): Promise<DetailedReport> {
    return this.request(`/api/v1/reports/detailed/${reportId}`);
  }

  async createDetailedReport(data: CreateDetailedReportData): Promise<DetailedReport> {
    return this.request('/api/v1/reports/detailed', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Rapports de progression par matière
  async getSubjectProgressReports(subject?: string, limit?: number): Promise<SubjectProgressReport[]> {
    const params = new URLSearchParams();
    if (subject) params.append('subject', subject);
    if (limit) params.append('limit', limit.toString());
    
    return this.request(`/api/v1/reports/subject-progress?${params.toString()}`);
  }

  async createSubjectProgressReport(data: CreateSubjectProgressReportData): Promise<SubjectProgressReport> {
    return this.request('/api/v1/reports/subject-progress', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Rapports d'analytics
  async getAnalyticsReports(analytics_type?: string, limit?: number): Promise<AnalyticsReport[]> {
    const params = new URLSearchParams();
    if (analytics_type) params.append('analytics_type', analytics_type);
    if (limit) params.append('limit', limit.toString());
    
    return this.request(`/api/v1/reports/analytics?${params.toString()}`);
  }

  async createAnalyticsReport(data: CreateAnalyticsReportData): Promise<AnalyticsReport> {
    return this.request('/api/v1/reports/analytics', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Export de rapports
  async exportReport(reportId: number, export_format?: string): Promise<ReportExport> {
    const params = new URLSearchParams();
    if (export_format) params.append('export_format', export_format);
    
    return this.request(`/api/v1/reports/${reportId}/export?${params.toString()}`, {
      method: 'POST',
    });
  }

  private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const response = await apiClient.request<T>(endpoint, options);
    return response.data;
  }
}

export const reportsAPI = new ReportsAPI();
