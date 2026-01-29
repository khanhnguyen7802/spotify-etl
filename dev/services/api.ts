import { LogEntry, PipelineStats, User } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000';

// Authentication API
export const initiateSpotifyLogin = async (): Promise<string> => {
  // Returns the authorization URL from the backend
  const response = await fetch(`${API_BASE_URL}/login`, {
    method: 'GET',
    credentials: 'include', // Include session cookies
  });
  
  if (!response.ok) {
    throw new Error('Failed to initiate Spotify login');
  }
  
  // Flask will redirect, so we return the URL
  return response.url;
};

export const getUserProfile = async (): Promise<User> => {
  // Fetch user profile from Spotify API via backend
  const response = await fetch(`${API_BASE_URL}/api/me`, {
    method: 'GET',
    credentials: 'include',
  });
  
  if (!response.ok) {
    throw new Error('Failed to fetch user profile');
  }
  
  const data = await response.json();
  
  // Map Spotify user data to our User type
  return {
    id: data.id,
    displayName: data.display_name,
    email: data.email,
    avatarUrl: data.images?.[0]?.url,
    tier: data.product === 'premium' ? 'premium' : 'free',
  };
};

// Mock data generators
export const fetchOverviewData = async () => {
  await new Promise(resolve => setTimeout(resolve, 800)); // Simulate latency
  return {
    streak: 14,
    topGenre: 'Indie Pop',
    topArtist: { name: 'The Weeknd', image: 'https://picsum.photos/200' },
    topTrack: { name: 'Blinding Lights', image: 'https://picsum.photos/200' },
    listeningHistory: [
      { day: 'Mon', minutes: 120 },
      { day: 'Tue', minutes: 200 },
      { day: 'Wed', minutes: 150 },
      { day: 'Thu', minutes: 300 },
      { day: 'Fri', minutes: 280 },
      { day: 'Sat', minutes: 400 },
      { day: 'Sun', minutes: 350 },
    ],
  };
};

export const fetchPipelineStatus = async (): Promise<PipelineStats> => {
  return {
    status: 'running',
    currentStage: 'silver',
    bronze: { rows: 1240, timestamp: new Date(Date.now() - 1000 * 60 * 2).toISOString() },
    silver: { rows: 1228, timestamp: new Date(Date.now() - 1000 * 30).toISOString() },
    gold: { kpis: 0, timestamp: 'PENDING' },
  };
};

export const fetchLogs = async (): Promise<LogEntry[]> => {
  const now = new Date();
  return [
    { id: '1', timestamp: now.toISOString(), level: 'INFO', message: 'Fetching user_top_artists from Spotify API...' },
    { id: '2', timestamp: new Date(now.getTime() + 1000).toISOString(), level: 'INFO', message: 'Received 50 items. Storing to Bronze (S3).' },
    { id: '3', timestamp: new Date(now.getTime() + 2000).toISOString(), level: 'SUCCESS', message: 'Bronze Layer Complete.' },
    { id: '4', timestamp: new Date(now.getTime() + 3000).toISOString(), level: 'INFO', message: 'Starting Silver transformation (Deduplication)...' },
  ];
};