import React, { useState } from 'react';
import { Copy, Check, Download, Share2 } from 'lucide-react';
import { useStore } from '../store/useStore';

const Share: React.FC = () => {
  const { user } = useStore();
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="max-w-4xl mx-auto flex flex-col md:flex-row gap-12 items-center justify-center min-h-[60vh]">
        {/* The Card Preview */}
        <div className="relative group">
            <div className="absolute -inset-1 bg-gradient-to-r from-spotify to-violet rounded-[2rem] blur opacity-25 group-hover:opacity-75 transition duration-1000 group-hover:duration-200"></div>
            <div className="relative w-[320px] h-[500px] bg-black rounded-[1.8rem] overflow-hidden border border-white/10 flex flex-col shadow-2xl">
                {/* Card Content */}
                <div className="h-2/3 bg-cover bg-center relative" style={{ backgroundImage: `url(${user?.avatarUrl || 'https://picsum.photos/400/600'})` }}>
                    <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent"></div>
                    <div className="absolute bottom-4 left-6">
                        <h2 className="text-3xl font-bold text-white tracking-tighter">{user?.displayName}</h2>
                        <p className="text-spotify font-medium">Top 1% Listener</p>
                    </div>
                </div>
                <div className="flex-1 bg-offblack p-6 flex flex-col justify-between">
                    <div className="flex justify-between items-center border-b border-white/10 pb-4">
                        <div>
                            <span className="block text-xs text-graphite uppercase">Top Genre</span>
                            <span className="text-white font-semibold">Indie Pop</span>
                        </div>
                        <div className="text-right">
                             <span className="block text-xs text-graphite uppercase">Streak</span>
                            <span className="text-white font-semibold">14 Days</span>
                        </div>
                    </div>
                    <div className="flex items-center justify-between text-xs text-graphite mt-2">
                        <span>wrapmyspotify.com</span>
                        <div className="w-6 h-6 bg-spotify rounded-full flex items-center justify-center text-black font-bold text-[10px]">W</div>
                    </div>
                </div>
            </div>
        </div>

        {/* Controls */}
        <div className="flex flex-col gap-6 w-full max-w-xs">
            <div className="text-center md:text-left">
                <h2 className="text-2xl font-bold text-white mb-2">Share your wrap</h2>
                <p className="text-graphite text-sm">Export your professional music profile card.</p>
            </div>
            
            <button 
                onClick={handleCopy}
                className="w-full py-3 px-4 bg-white text-black font-semibold rounded-xl flex items-center justify-center gap-2 hover:bg-gray-200 transition-colors"
            >
                {copied ? <Check size={18} /> : <Copy size={18} />}
                {copied ? 'Link Copied!' : 'Copy Link'}
            </button>

            <div className="grid grid-cols-2 gap-4">
                <button className="py-3 px-4 bg-offblack border border-white/10 text-white font-medium rounded-xl flex items-center justify-center gap-2 hover:bg-white/5 transition-colors">
                    <Download size={18} /> Save
                </button>
                 <button className="py-3 px-4 bg-offblack border border-white/10 text-white font-medium rounded-xl flex items-center justify-center gap-2 hover:bg-white/5 transition-colors">
                    <Share2 size={18} /> Social
                </button>
            </div>
        </div>
    </div>
  );
};

export default Share;