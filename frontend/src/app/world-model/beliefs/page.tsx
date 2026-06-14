"use client";

import React, { useState, useEffect } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";
import { Brain } from "lucide-react";

export default function BeliefsPage() {
  const [mounted, setMounted] = useState(false);
  
  useEffect(() => {
    setMounted(true);
  }, []);

  const beliefEvolutionData = [
    { time: "Day 1", "Memory Leak Hypothesis": 0.2, "Network Latency Hypothesis": 0.4, "Database Lock Hypothesis": 0.3 },
    { time: "Day 2", "Memory Leak Hypothesis": 0.25, "Network Latency Hypothesis": 0.45, "Database Lock Hypothesis": 0.25 },
    { time: "Day 3", "Memory Leak Hypothesis": 0.4, "Network Latency Hypothesis": 0.3, "Database Lock Hypothesis": 0.15 },
    { time: "Day 4", "Memory Leak Hypothesis": 0.65, "Network Latency Hypothesis": 0.2, "Database Lock Hypothesis": 0.1 },
    { time: "Day 5", "Memory Leak Hypothesis": 0.85, "Network Latency Hypothesis": 0.1, "Database Lock Hypothesis": 0.05 },
    { time: "Day 6", "Memory Leak Hypothesis": 0.92, "Network Latency Hypothesis": 0.05, "Database Lock Hypothesis": 0.02 },
    { time: "Day 7", "Memory Leak Hypothesis": 0.95, "Network Latency Hypothesis": 0.03, "Database Lock Hypothesis": 0.01 },
  ];

  const beliefs = [
    { id: "b1", concept: "Memory Leak", probability: 0.95, evidenceCount: 14, status: "strong" },
    { id: "b2", concept: "Network Latency", probability: 0.03, evidenceCount: 5, status: "weak" },
    { id: "b3", concept: "Database Lock", probability: 0.01, evidenceCount: 2, status: "weak" },
    { id: "b4", concept: "Cache Invalidation Issue", probability: 0.65, evidenceCount: 8, status: "moderate" },
  ];

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Bayesian Beliefs</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Evolution of the system's causal beliefs updated via Bayesian inference over time.
        </p>
      </div>

      <div className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 mb-8">
        <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-6">Belief Evolution</h2>
        <div className="h-80 w-full">
          {mounted && (
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={beliefEvolutionData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.3} />
                <XAxis dataKey="time" stroke="#6b7280" />
                <YAxis stroke="#6b7280" domain={[0, 1]} tickFormatter={(val) => `${(val * 100).toFixed(0)}%`} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#1f2937', borderColor: '#374151', color: '#f3f4f6' }}
                  formatter={(value: number) => [`${(value * 100).toFixed(1)}%`, undefined]}
                />
                <Legend />
                <Line type="monotone" dataKey="Memory Leak Hypothesis" stroke="#3b82f6" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 6 }} />
                <Line type="monotone" dataKey="Network Latency Hypothesis" stroke="#ef4444" strokeWidth={2} />
                <Line type="monotone" dataKey="Database Lock Hypothesis" stroke="#10b981" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>

      <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Current Belief Distribution</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {beliefs.map((belief) => (
          <div key={belief.id} className="bg-white dark:bg-gray-800 p-5 rounded-xl border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between mb-3">
              <Brain className={
                belief.status === 'strong' ? 'text-blue-500' :
                belief.status === 'moderate' ? 'text-amber-500' : 'text-gray-400'
              } size={24} />
              <span className="text-2xl font-bold text-gray-900 dark:text-white">
                {(belief.probability * 100).toFixed(0)}%
              </span>
            </div>
            <h3 className="font-medium text-gray-900 dark:text-white mb-1">{belief.concept}</h3>
            <p className="text-sm text-gray-500">Based on {belief.evidenceCount} evidence points</p>
            
            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-1.5 mt-4">
              <div 
                className={`h-1.5 rounded-full ${
                  belief.status === 'strong' ? 'bg-blue-500' :
                  belief.status === 'moderate' ? 'bg-amber-500' : 'bg-gray-400'
                }`}
                style={{ width: `${belief.probability * 100}%` }}
              ></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
