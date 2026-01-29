import React, { useEffect, useState } from 'react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { fetchOverviewData } from '../services/api';
import { Flame, Music, Disc, Activity } from 'lucide-react';

// Reusable Stat Card
const StatCard: React.FC<{ 
  title: string; 
  value: string | number; 
  subtext?: string;
  icon: React.ReactNode; 
  color?: string;
  image?: string;
}> = ({ title, value, subtext, icon, color = "text-spotify", image }) => (
  <div className="bg-offblack/50 border border-white/5 rounded-2xl p-6 backdrop-blur-sm hover:border-white/10 transition-all group overflow-hidden relative">
    {image && (
        <div className="absolute right-0 top-0 bottom-0 w-24 opacity-20 mask-image-gradient group-hover:opacity-40 transition-opacity">
            <img src={image} alt="bg" className="h-full w-full object-cover" />
            <div className="absolute inset-0 bg-gradient-to-r from-offblack via-offblack/80 to-transparent"></div>
        </div>
    )}
    <div className="flex items-start justify-between relative z-10">
      <div>
        <p className="text-xs uppercase tracking-wider text-graphite mb-1">{title}</p>
        <h3 className="text-2xl lg:text-3xl font-bold text-white mb-1">{value}</h3>
        {subtext && <p className="text-xs text-spotify">{subtext}</p>}
      </div>
      <div className={`p-3 rounded-xl bg-white/5 ${color}`}>
        {icon}
      </div>
    </div>
  </div>
);

const Overview: React.FC = () => {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    fetchOverviewData().then(setData);
  }, []);

  if (!data) return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 animate-pulse">
        {[1,2,3,4].map(i => <div key={i} className="h-40 bg-white/5 rounded-2xl" />)}
    </div>
  );

  return (
    <div className="space-y-8">
      {/* Top Stats Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard 
            title="Top Artist" 
            value={data.topArtist.name} 
            icon={<Music size={24} />} 
            image={data.topArtist.image}
        />
        <StatCard 
            title="Current Streak" 
            value={`${data.streak} Days`} 
            subtext="🔥 Personal Best!"
            icon={<Flame size={24} />} 
            color="text-orange-500"
        />
        <StatCard 
            title="Top Genre" 
            value={data.topGenre} 
            icon={<Disc size={24} />} 
            color="text-violet"
        />
         <StatCard 
            title="Top Track" 
            value={data.topTrack.name} 
            icon={<Activity size={24} />} 
            image={data.topTrack.image}
        />
      </div>

      {/* Main Chart Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 bg-offblack/50 border border-white/5 rounded-3xl p-6 backdrop-blur-sm">
            <div className="flex items-center justify-between mb-8">
                <div>
                    <h3 className="text-lg font-semibold text-white">Listening Activity</h3>
                    <p className="text-sm text-graphite">Minutes listened over the last 7 days</p>
                </div>
                <select className="bg-white/5 border border-white/10 rounded-lg px-3 py-1 text-xs text-mist focus:outline-none focus:border-spotify">
                    <option>Last 7 Days</option>
                    <option>Last 30 Days</option>
                </select>
            </div>
            <div className="h-[300px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={data.listeningHistory}>
                        <defs>
                            <linearGradient id="colorMin" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#1DB954" stopOpacity={0.3}/>
                                <stop offset="95%" stopColor="#1DB954" stopOpacity={0}/>
                            </linearGradient>
                        </defs>
                        <XAxis 
                            dataKey="day" 
                            axisLine={false} 
                            tickLine={false} 
                            tick={{fill: '#A0A0A0', fontSize: 12}}
                            dy={10}
                        />
                        <YAxis 
                            hide 
                        />
                        <Tooltip 
                            contentStyle={{ backgroundColor: '#121212', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }}
                            itemStyle={{ color: '#fff' }}
                        />
                        <Area 
                            type="monotone" 
                            dataKey="minutes" 
                            stroke="#1DB954" 
                            strokeWidth={3}
                            fillOpacity={1} 
                            fill="url(#colorMin)" 
                        />
                    </AreaChart>
                </ResponsiveContainer>
            </div>
        </div>

        {/* Profile/Identity Card */}
        <div className="bg-gradient-to-br from-violet/20 to-offblack border border-white/5 rounded-3xl p-8 flex flex-col items-center justify-center text-center relative overflow-hidden">
             <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-violet to-spotify"></div>
             <div className="text-4xl mb-4">🌙</div>
             <h3 className="text-2xl font-bold text-white mb-2">Night Owl</h3>
             <p className="text-graphite text-sm mb-6">42% of your listening happens after 9PM.</p>
             <button className="text-xs font-semibold uppercase tracking-widest text-white border border-white/20 px-6 py-2 rounded-full hover:bg-white hover:text-black transition-colors">
                 Share This
             </button>
        </div>
      </div>
      
      {/* Simple Lists */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="bg-offblack/30 border border-white/5 rounded-2xl p-6">
                <h4 className="text-white font-semibold mb-4">Top 5 Artists</h4>
                <ul className="space-y-4">
                    {[1, 2, 3, 4, 5].map((item) => (
                        <li key={item} className="flex items-center gap-4">
                            <span className="text-graphite font-mono text-sm">0{item}</span>
                            <div className="w-10 h-10 bg-white/10 rounded-full"></div>
                            <div className="flex-1 h-3 bg-white/5 rounded w-full animate-pulse"></div>
                        </li>
                    ))}
                </ul>
            </div>
            <div className="bg-offblack/30 border border-white/5 rounded-2xl p-6">
                <h4 className="text-white font-semibold mb-4">Top 5 Genres</h4>
                <ul className="space-y-4">
                    {[1, 2, 3, 4, 5].map((item) => (
                        <li key={item} className="flex items-center gap-4">
                            <span className="text-graphite font-mono text-sm">0{item}</span>
                            <div className="w-10 h-10 bg-white/10 rounded-lg"></div>
                            <div className="flex-1 h-3 bg-white/5 rounded w-full animate-pulse"></div>
                        </li>
                    ))}
                </ul>
            </div>
      </div>
    </div>
  );
};

export default Overview;