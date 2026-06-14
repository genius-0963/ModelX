"use client";

import React, { useState, useEffect } from 'react';

const mockEnvNodes = [
  { id: 'env-1', name: 'Production Cluster', type: 'Infrastructure', health: 'Healthy', load: 45 },
  { id: 'env-2', name: 'Staging Database', type: 'Data', health: 'Warning', load: 85 },
  { id: 'env-3', name: 'Worker Pool A', type: 'Compute', health: 'Healthy', load: 60 },
  { id: 'env-4', name: 'Edge Nodes', type: 'Network', health: 'Healthy', load: 30 },
  { id: 'env-5', name: 'Legacy API', type: 'Service', health: 'Critical', load: 98 }
];

export default function EnvironmentMapping() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null;

  return (
    <div className="p-8 space-y-8 bg-gray-50 min-h-screen text-gray-900">
      <h1 className="text-3xl font-bold">Environment Mapping</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow border-l-4 border-green-500">
          <h3 className="text-gray-500 text-sm font-semibold uppercase">Healthy Nodes</h3>
          <p className="text-3xl font-bold mt-2">
            {mockEnvNodes.filter(n => n.health === 'Healthy').length}
          </p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow border-l-4 border-yellow-500">
          <h3 className="text-gray-500 text-sm font-semibold uppercase">Warnings</h3>
          <p className="text-3xl font-bold mt-2">
            {mockEnvNodes.filter(n => n.health === 'Warning').length}
          </p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow border-l-4 border-red-500">
          <h3 className="text-gray-500 text-sm font-semibold uppercase">Critical Issues</h3>
          <p className="text-3xl font-bold mt-2">
            {mockEnvNodes.filter(n => n.health === 'Critical').length}
          </p>
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-semibold mb-4">Topology & Status Map</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {mockEnvNodes.map(node => (
            <div key={node.id} className="border rounded-lg p-4 flex flex-col justify-between">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h4 className="font-bold text-lg">{node.name}</h4>
                  <p className="text-xs text-gray-500">{node.type}</p>
                </div>
                <span className={`w-3 h-3 rounded-full ${
                  node.health === 'Healthy' ? 'bg-green-500' :
                  node.health === 'Warning' ? 'bg-yellow-500' : 'bg-red-500'
                }`}></span>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>Load</span>
                  <span>{node.load}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-1.5">
                  <div 
                    className={`h-1.5 rounded-full ${
                      node.load < 60 ? 'bg-blue-500' :
                      node.load < 90 ? 'bg-yellow-500' : 'bg-red-500'
                    }`} 
                    style={{ width: `${node.load}%` }}
                  ></div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
