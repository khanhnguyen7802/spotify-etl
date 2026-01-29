import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from 'recharts';

const data = [
  { name: 'Jan', followers: 4000, streams: 2400 },
  { name: 'Feb', followers: 3000, streams: 1398 },
  { name: 'Mar', followers: 2000, streams: 9800 },
  { name: 'Apr', followers: 2780, streams: 3908 },
  { name: 'May', followers: 1890, streams: 4800 },
  { name: 'Jun', followers: 2390, streams: 3800 },
  { name: 'Jul', followers: 3490, streams: 4300 },
];

const Analysis: React.FC = () => {
  return (
    <div className="space-y-8">
        <div className="flex justify-between items-end">
            <div>
                <h1 className="text-3xl font-bold text-white">Audience Growth</h1>
                <p className="text-graphite mt-2">Correlating follower acquisition with stream volume.</p>
            </div>
            <button className="bg-white/10 hover:bg-white/20 px-4 py-2 rounded-lg text-sm transition-colors">Export CSV</button>
        </div>

        <div className="h-[400px] bg-offblack/50 border border-white/5 rounded-3xl p-6">
            <ResponsiveContainer width="100%" height="100%">
                <BarChart data={data}>
                    <XAxis dataKey="name" stroke="#555" tick={{ fill: '#A0A0A0' }} />
                    <YAxis stroke="#555" tick={{ fill: '#A0A0A0' }} />
                    <Tooltip 
                        contentStyle={{ backgroundColor: '#121212', border: '1px solid #333', borderRadius: '8px' }}
                        cursor={{fill: 'rgba(255,255,255,0.05)'}}
                    />
                    <Legend />
                    <Bar dataKey="followers" fill="#BB86FC" radius={[4, 4, 0, 0]} name="New Followers" />
                    <Bar dataKey="streams" fill="#1DB954" radius={[4, 4, 0, 0]} name="Streams (x10)" />
                </BarChart>
            </ResponsiveContainer>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-6 bg-offblack rounded-2xl border border-white/5">
                <h3 className="text-graphite uppercase text-xs tracking-wider mb-2">Conversion Rate</h3>
                <div className="text-2xl text-white font-mono">3.2% <span className="text-green-500 text-sm">↑ 0.4%</span></div>
            </div>
             <div className="p-6 bg-offblack rounded-2xl border border-white/5">
                <h3 className="text-graphite uppercase text-xs tracking-wider mb-2">Avg. Listen Time</h3>
                <div className="text-2xl text-white font-mono">2m 45s</div>
            </div>
             <div className="p-6 bg-offblack rounded-2xl border border-white/5">
                <h3 className="text-graphite uppercase text-xs tracking-wider mb-2">Playlist Adds</h3>
                <div className="text-2xl text-white font-mono">142</div>
            </div>
        </div>
    </div>
  );
};

export default Analysis;