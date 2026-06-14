"use client";

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const growthData = [
  { epoch: 'E-10', reasoning: 40, coding: 30, math: 20 },
  { epoch: 'E-20', reasoning: 55, coding: 45, math: 35 },
  { epoch: 'E-30', reasoning: 70, coding: 65, math: 50 },
  { epoch: 'E-40', reasoning: 85, coding: 80, math: 75 },
  { epoch: 'E-50', reasoning: 95, coding: 92, math: 88 },
];

export default function CapabilityGrowth() {
  return (
    <div className="p-8 space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Capability Growth</h1>
        <p className="text-muted-foreground mt-2">Tracking capability evolution over training epochs.</p>
      </div>
      
      <Card>
        <CardHeader>
          <CardTitle>Multi-Domain Growth</CardTitle>
          <CardDescription>Stacked area chart showing cumulative growth across domains</CardDescription>
        </CardHeader>
        <CardContent className="h-[500px]">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={growthData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="epoch" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Area type="monotone" dataKey="math" stackId="1" stroke="#ffc658" fill="#ffc658" />
              <Area type="monotone" dataKey="coding" stackId="1" stroke="#82ca9d" fill="#82ca9d" />
              <Area type="monotone" dataKey="reasoning" stackId="1" stroke="#8884d8" fill="#8884d8" />
            </AreaChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Reasoning Velocity</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-indigo-600">+15.2% / epoch</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Coding Velocity</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">+12.8% / epoch</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Math Velocity</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-yellow-600">+18.5% / epoch</div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
