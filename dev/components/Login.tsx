import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useStore } from '../store/useStore';
import { getUserProfile } from '../services/api';
import logo from '../assets/logo_icon.png';

const Login: React.FC = () => {
  const login = useStore((state) => state.login);
  const [buttonShake, setButtonShake] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [showError, setShowError] = useState(false);

  // Check if we're returning from Spotify OAuth callback
  useEffect(() => {
    const handleCallback = async () => {
      const urlParams = new URLSearchParams(window.location.search);
      const code = urlParams.get('code');
      const error = urlParams.get('error');

      if (error) { // authentication failed 
        setErrorMessage('Authentication failed. Please try again.');
        setShowError(true);
        setButtonShake(true);

        // Hide error message after 3 seconds (then it will fade out)
        setTimeout(() => setShowError(false), 3000);
        // Keep button shake slightly longer but slower
        setTimeout(() => setButtonShake(false), 1500);

        // Clean up URL
        window.history.replaceState({}, document.title, window.location.pathname);
        return;
      }
      
      // success 
      if (code) {
        setIsLoading(true);
        try {
          // The backend has already handled the code exchange in /callback
          // Now we just need to fetch the user profile
          const user = await getUserProfile();
          login(user);
        } catch (error) {
          console.error('Failed to fetch user profile:', error);
          setErrorMessage('Failed to complete authentication. Please try again.');
          setShowError(true);
          setButtonShake(true);

          // Hide error message after 3 seconds (then it will fade out)
          setTimeout(() => setShowError(false), 3000);
          setTimeout(() => setButtonShake(false), 1500);
        } finally {
          setIsLoading(false);
          
          // Clean up URL
          window.history.replaceState({}, document.title, window.location.pathname);
        }
      }


    };

    handleCallback();
  }, [login]);

  
  const handleLogin = () => {
    setIsLoading(true);
    setErrorMessage(null);
    
    // Redirect to backend login endpoint which will redirect to Spotify
    window.location.href = 'http://127.0.0.1:5000/login';
  };

  return (
    <div className="h-screen w-full flex items-center justify-center bg-obsidian relative overflow-hidden">
      {/* Background Ambient Effect */}
      <motion.div 
        animate={{ rotate: 360 }}
        transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
        className="absolute w-[600px] h-[600px] bg-spotify/20 blur-[120px] rounded-full top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 pointer-events-none"
      />

      <div className="relative z-10 flex flex-col items-center gap-4 max-w-sm w-full">
        {/* Error Message - Above the box */}
        <motion.div
          initial={{ opacity: 0, y: -8 }}
          animate={{ 
            opacity: showError ? 1 : 0,
            y: showError ? 0 : -8
          }}
          transition={{ duration: showError ? 0.15 : 3.5, ease: 'easeOut' }}
          className="w-full px-4 py-2 bg-red-500/10 border border-red-500/50 text-red-400 text-sm text-center rounded-lg"
          style={{ pointerEvents: showError ? 'auto' : 'none' }}
        >
          {errorMessage || 'Connection Interrupted. Try again.'}
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ type: 'spring', stiffness: 100 }}
          className="w-full bg-offblack/80 backdrop-blur-xl border border-white/10 p-12 rounded-3xl shadow-2xl flex flex-col items-center"
        >
        {/* Exposed Logo */}
        <div className="relative h-20 w-20 mb-8 overflow-visible">
            <img
              src={logo}
              alt="Logo"
              className="absolute left-1/2 top-0 -translate-x-1/2 -translate-y-1/4 w-32 h-32 object-contain max-w-none max-h-none"
            />
        </div>
        
        <h1 className="text-3xl font-bold text-mist mb-2 tracking-tight">WrapMySpotify</h1>
        <p className="text-graphite mb-8 text-center text-sm">Orchestrate your music data.</p>

        <motion.button
          onClick={handleLogin}
          disabled={isLoading}
          animate={buttonShake ? { x: [-6, 6, -4, 4, 0] } : { x: 0 }}
            transition={{ duration: 0.9, ease: 'easeInOut' }}
          className={`group relative w-full bg-white text-black font-semibold py-3 px-6 rounded-full flex items-center justify-center gap-3 transition-all hover:scale-[1.02] disabled:opacity-70 disabled:hover:scale-100 ${
            buttonShake 
              ? 'shadow-[0_0_20px_rgba(239,68,68,0.6),0_0_40px_rgba(239,68,68,0.4)]' 
              : 'hover:shadow-[0_0_20px_rgba(29,185,84,0.4)]'
          }`}
        >
          {isLoading ? (
             <span className="flex items-center gap-2">
               <span className="w-2 h-2 bg-black rounded-full animate-bounce" style={{ animationDelay: '0ms' }}/>
               <span className="w-2 h-2 bg-black rounded-full animate-bounce" style={{ animationDelay: '150ms' }}/>
               <span className="w-2 h-2 bg-black rounded-full animate-bounce" style={{ animationDelay: '300ms' }}/>
             </span>
          ) : (
            <>
               {/* Small Spotify Icon */}
               <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" className="text-black">
                <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S16.6 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.4-1.02 15.96 1.74.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.24"/>
               </svg>
               <span>Login with Spotify</span>
            </>
          )}
        </motion.button>
      </motion.div>
      </div>
    </div>
  );
};

export default Login;