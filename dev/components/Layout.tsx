import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useStore } from '../store/useStore';
import { AppRoute } from '../types';
import { 
  LayoutDashboard, 
  GitCommitHorizontal, 
  BarChart2, 
  Share2, 
  Info, 
  Menu, 
  X, 
  LogOut,
  Sun,
  Moon
} from 'lucide-react';

interface LayoutProps {
  children: React.ReactNode;
}

const NavItem: React.FC<{ 
  icon: React.ReactNode; 
  label: string; 
  active: boolean; 
  onClick: () => void 
}> = ({ icon, label, active, onClick }) => (
  <button
    onClick={onClick}
    className={`w-full flex items-center gap-4 px-6 py-4 transition-all duration-300 relative group
      ${active ? 'text-white bg-white/5' : 'text-graphite hover:text-mist hover:bg-white/5'}`}
  >
    {active && (
      <motion.div
        layoutId="activeTab"
        className="absolute left-0 top-0 bottom-0 w-1 bg-spotify"
      />
    )}
    <span className={`${active ? 'text-spotify' : ''}`}>{icon}</span>
    <span className="font-medium tracking-wide">{label}</span>
  </button>
);

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { currentRoute, setRoute, user, logout, toggleDarkMode, darkMode } = useStore();
  const [isSidebarOpen, setSidebarOpen] = useState(false);

  const navItems = [
    { route: AppRoute.OVERVIEW, label: 'Overview', icon: <LayoutDashboard size={20} /> },
    { route: AppRoute.PIPELINES, label: 'Pipelines', icon: <GitCommitHorizontal size={20} /> },
    { route: AppRoute.ANALYSIS, label: 'Analysis', icon: <BarChart2 size={20} /> },
    { route: AppRoute.SHARE, label: 'Share', icon: <Share2 size={20} /> },
    { route: AppRoute.ABOUT, label: 'About', icon: <Info size={20} /> },
  ];

  return (
    <div className={`min-h-screen flex bg-obsidian text-mist transition-colors duration-500 ${darkMode ? 'dark' : ''}`}>
      {/* Sidebar - Desktop */}
      <aside className="hidden lg:flex flex-col w-64 border-r border-white/5 bg-offblack/50 backdrop-blur-md h-screen sticky top-0 z-20">
        <div className="p-8 flex items-center gap-3">
             <div className="w-8 h-8 rounded-full bg-spotify flex items-center justify-center text-black font-bold text-xs">W</div>
             <span className="font-bold tracking-tight text-xl">WrapMySpotify</span>
        </div>
        <nav className="flex-1 mt-4">
          {navItems.map((item) => (
            <NavItem
              key={item.route}
              icon={item.icon}
              label={item.label}
              active={currentRoute === item.route}
              onClick={() => setRoute(item.route)}
            />
          ))}
        </nav>
        <div className="p-6 border-t border-white/5">
            <div className="flex items-center gap-3 mb-4">
                <img src={user?.avatarUrl} alt="User" className="w-10 h-10 rounded-full border border-white/10" />
                <div className="flex flex-col">
                    <span className="text-sm font-semibold text-white">{user?.displayName}</span>
                    <span className="text-xs text-graphite uppercase">{user?.tier} Plan</span>
                </div>
            </div>
            <button onClick={logout} className="flex items-center gap-2 text-xs text-graphite hover:text-red-400 transition-colors">
                <LogOut size={14} /> Sign Out
            </button>
        </div>
      </aside>

      {/* Mobile Sidebar Overlay */}
      <AnimatePresence>
        {isSidebarOpen && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setSidebarOpen(false)}
              className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 lg:hidden"
            />
            <motion.aside
              initial={{ x: -300 }}
              animate={{ x: 0 }}
              exit={{ x: -300 }}
              transition={{ type: 'spring', damping: 25, stiffness: 200 }}
              className="fixed left-0 top-0 bottom-0 w-64 bg-offblack z-50 border-r border-white/10 lg:hidden flex flex-col"
            >
               <div className="p-6 flex items-center justify-between border-b border-white/5">
                 <span className="font-bold text-lg">Menu</span>
                 <button onClick={() => setSidebarOpen(false)}><X /></button>
               </div>
               <nav className="flex-1 py-4">
                {navItems.map((item) => (
                    <NavItem
                    key={item.route}
                    icon={item.icon}
                    label={item.label}
                    active={currentRoute === item.route}
                    onClick={() => {
                        setRoute(item.route);
                        setSidebarOpen(false);
                    }}
                    />
                ))}
               </nav>
               <div className="p-6">
                 <button onClick={logout} className="flex items-center gap-2 text-sm text-red-400">
                    <LogOut size={16} /> Logout
                 </button>
               </div>
            </motion.aside>
          </>
        )}
      </AnimatePresence>

      {/* Main Content */}
      <main className="flex-1 flex flex-col min-w-0">
        {/* Header */}
        <header className="h-16 border-b border-white/5 flex items-center justify-between px-6 bg-obsidian/80 backdrop-blur-md sticky top-0 z-10">
            <div className="flex items-center gap-4">
                <button 
                  onClick={() => setSidebarOpen(true)} 
                  className="lg:hidden p-2 hover:bg-white/5 rounded-full"
                >
                    <Menu size={20} />
                </button>
                <h2 className="text-lg font-semibold capitalize text-white">
                  {currentRoute}
                </h2>
            </div>
            
            <div className="flex items-center gap-4">
                <button 
                  onClick={toggleDarkMode}
                  className="p-2 rounded-full hover:bg-white/5 text-graphite hover:text-white transition-colors"
                >
                    {darkMode ? <Moon size={20} /> : <Sun size={20} />}
                </button>
                <div className="w-8 h-8 rounded-full overflow-hidden border border-white/10 lg:hidden">
                    <img src={user?.avatarUrl} alt="User" />
                </div>
            </div>
        </header>

        {/* Scrollable Content Area */}
        <div className="flex-1 p-4 lg:p-8 overflow-y-auto">
            <AnimatePresence mode="wait">
                <motion.div
                    key={currentRoute}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    transition={{ duration: 0.3 }}
                    className="max-w-7xl mx-auto w-full"
                >
                    {children}
                </motion.div>
            </AnimatePresence>
        </div>
      </main>
    </div>
  );
};

export default Layout;