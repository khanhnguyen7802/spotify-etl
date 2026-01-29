export interface User {
  id: string;
  displayName: string;
  email: string;
  avatarUrl?: string;
  tier: 'free' | 'premium';
}

export interface PipelineStats {
  status: 'running' | 'idle' | 'failed';
  currentStage: 'bronze' | 'silver' | 'gold' | 'complete';
  bronze: { rows: number; timestamp: string };
  silver: { rows: number; timestamp: string };
  gold: { kpis: number; timestamp: string };
}

export interface LogEntry {
  id: string;
  timestamp: string;
  level: 'INFO' | 'SUCCESS' | 'WARNING' | 'ERROR';
  message: string;
}

export interface KPI {
  label: string;
  value: string | number;
  change?: number; // percentage
  trend?: 'up' | 'down' | 'neutral';
  icon?: React.ReactNode;
}

export enum AppRoute {
  LOGIN = 'login',
  OVERVIEW = 'overview',
  PIPELINES = 'pipelines',
  ANALYSIS = 'analysis',
  SHARE = 'share',
  ABOUT = 'about',
}