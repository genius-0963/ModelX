"use client";

import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const mockFitnessData = [
  { generation: 1, bestFitness: 0.82, avgFitness: 0.75 },
  { generation: 2, bestFitness: 0.84, avgFitness: 0.77 },
  { generation: 3, bestFitness: 0.85, avgFitness: 0.79 },
  { generation: 4, bestFitness: 0.88, avgFitness: 0.81 },
  { generation: 5, bestFitness: 0.89, avgFitness: 0.83 },
  { generation: 6, bestFitness: 0.91, avgFitness: 0.85 },
  { generation: 7, bestFitness: 0.93, avgFitness: 0.87 },
  { generation: 8, bestFitness: 0.94, avgFitness: 0.88 },
];

export default function EvolutionDashboard() {
  const [currentGen] = useState(8);
  const [populationSize] = useState(50);
  const [bestFitness] = useState(0.94);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Evolution Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
          <h2 className="text-gray-500 text-sm font-medium">Current Generation</h2>
          <div className="mt-2 text-3xl font-bold text-gray-900">{currentGen}</div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
          <h2 className="text-gray-500 text-sm font-medium">Population Size</h2>
          <div className="mt-2 text-3xl font-bold text-gray-900">{populationSize}</div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
          <h2 className="text-gray-500 text-sm font-medium">Best Fitness</h2>
          <div className="mt-2 text-3xl font-bold text-green-600">{bestFitness.toFixed(2)}</div>
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
        <h2 className="text-lg font-semibold mb-4">Fitness Trend (Generations)</h2>
        <div className="h-80 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={mockFitnessData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="generation" />
              <YAxis domain={[0, 1]} />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="bestFitness" stroke="#10b981" name="Best Fitness" strokeWidth={2} />
              <Line type="monotone" dataKey="avgFitness" stroke="#3b82f6" name="Avg Fitness" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
