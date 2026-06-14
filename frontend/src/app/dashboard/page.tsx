"use client";

import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Activity, CheckCircle, Target, Zap } from 'lucide-react';

const knowledgeGrowthData = [
  { name: 'Week 1', score: 40 },
  { name: 'Week 2', score: 55 },
  { name: 'Week 3', score: 68 },
  { name: 'Week 4', score: 85 },
  { name: 'Week 5', score: 110 },
  { name: 'Week 6', score: 145 },
];

const StatCard = ({ title, value, icon: Icon, description }: any) => (
  <div className="bg-white dark:bg-slate-800 p-6 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700">
    <div className="flex items-center justify-between">
      <div>
        <p className="text-sm font-medium text-slate-500 dark:text-slate-400">{title}</p>
        <p className="text-2xl font-bold text-slate-900 dark:text-white mt-2">{value}</p>
      </div>
      <div className="p-3 bg-blue-50 dark:bg-blue-900/30 rounded-lg">
        <Icon className="w-6 h-6 text-blue-600 dark:text-blue-400" />
      </div>
    </div>
    <div className="mt-4 text-sm text-slate-600 dark:text-slate-300">
      {description}
    </div>
  </div>
);

export default function DashboardPage() {
  return (
    <div className="p-8 max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900 dark:text-white">Agent Dashboard</h1>
        <p className="text-slate-500 dark:text-slate-400 mt-2">Overview of autonomous performance and learning metrics.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard title="Active Goals" value="12" icon={Target} description="3 high priority" />
        <StatCard title="Completed Goals" value="1,284" icon={CheckCircle} description="+24 this week" />
        <StatCard title="Autonomy Score" value="94.2%" icon={Activity} description="Requires human input 5.8% of time" />
        <StatCard title="Learning Velocity" value="8.4x" icon={Zap} description="Concepts mastered per day" />
      </div>

      <div className="bg-white dark:bg-slate-800 p-6 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700">
        <h2 className="text-xl font-semibold text-slate-900 dark:text-white mb-6">Knowledge Growth Over Time</h2>
        <div className="h-80 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={knowledgeGrowthData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" className="stroke-slate-200 dark:stroke-slate-700" />
              <XAxis dataKey="name" className="text-slate-600 dark:text-slate-400" />
              <YAxis className="text-slate-600 dark:text-slate-400" />
              <Tooltip 
                contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px', color: '#fff' }}
              />
              <Line 
                type="monotone" 
                dataKey="score" 
                stroke="#3b82f6" 
                strokeWidth={3}
                dot={{ r: 4, strokeWidth: 2 }}
                activeDot={{ r: 8 }} 
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
