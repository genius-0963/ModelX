"use client";

import React, { useState } from 'react';

const mockGenomes = [
  { id: 'gen-8-a1b2', parent: 'gen-7-c3d4', mutationType: 'Crossover + Param Tuning', fitness: 0.94, status: 'Active Baseline' },
  { id: 'gen-8-e5f6', parent: 'gen-7-c3d4', mutationType: 'Network Pruning', fitness: 0.91, status: 'Archived' },
  { id: 'gen-7-c3d4', parent: 'gen-6-a1b2', mutationType: 'Activation Function Swap', fitness: 0.93, status: 'Previous Baseline' },
  { id: 'gen-6-a1b2', parent: 'gen-5-x9y0', mutationType: 'Layer Addition', fitness: 0.91, status: 'Archived' },
];

export default function GenomesPage() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Genomes Lineage</h1>
      
      <div className="bg-white rounded-lg shadow overflow-hidden border border-gray-200 mb-8">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Genome ID</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Parent ID</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Mutation</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fitness</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {mockGenomes.map((genome) => (
              <tr key={genome.id}>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-blue-600">{genome.id}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{genome.parent}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{genome.mutationType}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-green-600">{genome.fitness.toFixed(2)}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">
                  <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                    genome.status.includes('Baseline') ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                  }`}>
                    {genome.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
        <h2 className="text-lg font-semibold mb-4">Genome Mutation Tree (Visualization)</h2>
        <div className="flex flex-col items-center justify-center p-8 bg-gray-50 rounded border border-dashed border-gray-300">
          <div className="text-center">
            <div className="bg-blue-100 border-2 border-blue-500 text-blue-800 px-4 py-2 rounded-lg inline-block">gen-5-x9y0</div>
            <div className="h-6 border-l-2 border-gray-400 mx-auto w-0"></div>
            <div className="bg-blue-100 border-2 border-blue-500 text-blue-800 px-4 py-2 rounded-lg inline-block">gen-6-a1b2</div>
            <div className="h-6 border-l-2 border-gray-400 mx-auto w-0"></div>
            <div className="bg-blue-100 border-2 border-blue-500 text-blue-800 px-4 py-2 rounded-lg inline-block">gen-7-c3d4</div>
            <div className="flex justify-center mt-2">
              <div className="flex flex-col items-center mx-4">
                <div className="h-6 border-l-2 border-gray-400 w-0"></div>
                <div className="bg-green-100 border-2 border-green-500 text-green-800 px-4 py-2 rounded-lg font-bold">gen-8-a1b2 (Active)</div>
              </div>
              <div className="flex flex-col items-center mx-4">
                <div className="h-6 border-l-2 border-gray-400 w-0"></div>
                <div className="bg-gray-100 border-2 border-gray-400 text-gray-600 px-4 py-2 rounded-lg">gen-8-e5f6</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
