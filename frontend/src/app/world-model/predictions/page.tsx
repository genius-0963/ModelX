"use client";

import React, { useState } from "react";
import { Target, AlertTriangle, TrendingUp, TrendingDown } from "lucide-react";

export default function PredictionsPage() {
  const [predictions] = useState([
    {
      id: "prd-001",
      target: "System Memory Outage",
      condition: "If concurrent users > 10,000 and cache TTL is 60s",
      probability: 0.88,
      status: "monitoring",
      accuracy: null,
      timeframe: "Next 24 hours"
    },
    {
      id: "prd-002",
      target: "Latency Spike",
      condition: "During daily batch sync (02:00 UTC)",
      probability: 0.95,
      status: "validated",
      accuracy: 0.96,
      timeframe: "Past 7 days"
    },
    {
      id: "prd-003",
      target: "Conversion Drop",
      condition: "If checkout page load > 3s",
      probability: 0.75,
      status: "invalidated",
      accuracy: 0.30,
      timeframe: "Past 30 days"
    }
  ]);

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Predictions</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Model-generated forecasts and their real-world accuracy validation.
        </p>
      </div>

      <div className="grid gap-4">
        {predictions.map((pred) => (
          <div key={pred.id} className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div className="flex-1">
                <div className="flex items-center space-x-3 mb-2">
                  <Target size={18} className="text-blue-500" />
                  <h3 className="text-lg font-bold text-gray-900 dark:text-white">{pred.target}</h3>
                  <span className={`px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    pred.status === 'validated' ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' :
                    pred.status === 'invalidated' ? 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400' :
                    'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400'
                  }`}>
                    {pred.status.toUpperCase()}
                  </span>
                </div>
                <div className="text-gray-600 dark:text-gray-400 text-sm mt-1 bg-gray-50 dark:bg-gray-900/50 p-2 rounded inline-block">
                  <span className="font-medium">Condition:</span> {pred.condition}
                </div>
                <div className="text-sm text-gray-500 mt-2">
                  Timeframe: {pred.timeframe}
                </div>
              </div>
              
              <div className="flex items-center space-x-8">
                <div className="flex flex-col items-center">
                  <span className="text-sm text-gray-500 mb-1">Forecast Prob</span>
                  <div className="text-xl font-bold text-gray-900 dark:text-white">
                    {(pred.probability * 100).toFixed(0)}%
                  </div>
                </div>
                
                <div className="w-px h-12 bg-gray-200 dark:bg-gray-700 hidden md:block"></div>
                
                <div className="flex flex-col items-center min-w-[100px]">
                  <span className="text-sm text-gray-500 mb-1">Historical Accuracy</span>
                  {pred.accuracy !== null ? (
                    <div className={`flex items-center space-x-1 text-xl font-bold ${
                      pred.accuracy > 0.8 ? 'text-green-500' : pred.accuracy < 0.5 ? 'text-red-500' : 'text-amber-500'
                    }`}>
                      {pred.accuracy > 0.8 ? <TrendingUp size={20} /> : <TrendingDown size={20} />}
                      <span>{(pred.accuracy * 100).toFixed(0)}%</span>
                    </div>
                  ) : (
                    <span className="text-gray-400 italic">Pending</span>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
