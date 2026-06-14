"use client";

import React from 'react';

const mockRollbacks = [
  { date: '2026-06-13T16:45:00Z', variant: 'gen-8-fail1', fallbackTo: 'gen-7-c3d4', reason: 'High error rate in canary' },
  { date: '2026-06-09T11:20:00Z', variant: 'gen-5-fail2', fallbackTo: 'gen-4-k2m3', reason: 'OOM after 2 hours' },
];

export default function RollbacksPage() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Deployment Rollbacks</h1>
      <p className="text-gray-600 mb-6">History of deployments rolled back due to regressions or runtime failures.</p>

      <div className="bg-white rounded-lg shadow overflow-hidden border border-gray-200">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Failed Variant</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fallback To</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Regression Reason</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {mockRollbacks.map((rollback, idx) => (
              <tr key={idx}>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{new Date(rollback.date).toLocaleString()}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-red-600">{rollback.variant}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-green-600">{rollback.fallbackTo}</td>
                <td className="px-6 py-4 text-sm text-gray-900">{rollback.reason}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
