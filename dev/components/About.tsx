import React, { useState } from 'react';
import confetti from 'canvas-confetti';

const About: React.FC = () => {
  const [clicks, setClicks] = useState(0);

  const handleVersionClick = () => {
    const newCount = clicks + 1;
    setClicks(newCount);
    if (newCount === 5) {
      confetti({
        particleCount: 150,
        spread: 70,
        origin: { y: 0.6 },
        colors: ['#1DB954', '#BB86FC', '#FFFFFF']
      });
      setClicks(0);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] text-center max-w-2xl mx-auto space-y-12">
        <div>
            <h1 className="text-4xl font-bold text-white mb-4">WrapMySpotify</h1>
            <p className="text-lg text-graphite leading-relaxed">
                The radical, minimalist CRM for music professionals. 
                We believe your data should look as good as it sounds.
            </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 w-full">
            <div className="p-6 border border-white/5 rounded-2xl bg-offblack/30">
                <h3 className="text-white font-semibold mb-2">Privacy First</h3>
                <p className="text-sm text-graphite">Your data never leaves your browser until you choose to sync. We respect the sanctity of your listening habits.</p>
            </div>
            <div className="p-6 border border-white/5 rounded-2xl bg-offblack/30">
                <h3 className="text-white font-semibold mb-2">Open Architecture</h3>
                <p className="text-sm text-graphite">Built for Python backends. Extendable, scalable, and ready for the future of music tech.</p>
            </div>
        </div>

        <div className="pt-12 border-t border-white/5 w-full">
            <p className="text-sm text-graphite mb-4">
                Made with <span className="text-red-500">♥</span> for Music
            </p>
            <button 
                onClick={handleVersionClick}
                className="text-xs font-mono text-white/20 hover:text-white/50 transition-colors select-none"
            >
                v1.0.0 (The Glass Symphony)
            </button>
        </div>
    </div>
  );
};

export default About;