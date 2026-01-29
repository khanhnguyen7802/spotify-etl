import { create } from 'zustand';
import { User, AppRoute } from '../types';

interface AppState {
  user: User | null;
  isAuthenticated: boolean;
  currentRoute: AppRoute;
  darkMode: boolean;
  
  // Actions
  login: (user: User) => void;
  logout: () => void;
  setRoute: (route: AppRoute) => void;
  toggleDarkMode: () => void;
}

export const useStore = create<AppState>((set) => ({
  user: null,
  isAuthenticated: false,
  currentRoute: AppRoute.LOGIN,
  darkMode: true,

  login: (user) => set({ user, isAuthenticated: true, currentRoute: AppRoute.OVERVIEW }),
  logout: () => set({ user: null, isAuthenticated: false, currentRoute: AppRoute.LOGIN }),
  setRoute: (route) => set({ currentRoute: route }),
  toggleDarkMode: () => set((state) => ({ darkMode: !state.darkMode })),
}));