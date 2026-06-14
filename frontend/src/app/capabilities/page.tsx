"use client";

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, BarChart, Bar } from 'recharts';

const overallScores = [
  { month: 'Jan', score: 85, target: 80 },
  { month: 'Feb', score: 88, target: 82 },
  { month: 'Mar', score: 92, target: 85 },
  { month: 'Apr', score: 95, target: 88 },
  { month: 'May', score: 98, target: 90 },
];

const capabilityDistribution = [
  { category: 'Reasoning', score: 95 },
  { category: 'Coding', score: 92 },
  { category: 'Mathematics', score: 88 },
  { category: 'Creative', score: 85 },
  { category: 'Knowledge', score: 98 },
];

export default function CapabilitiesDashboard() {
  return (
    <div className="p-8 space-y-8">
      <h1 className="text-3xl font-bold tracking-tight">Capabilities Overview</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Overall Capability Score</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">98.2</div>
            <p className="text-xs text-green-500 mt-1">+2.5% from last month</p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Capability Growth Rate</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">1.4x</div>
            <p className="text-xs text-green-500 mt-1">+0.1x acceleration</p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Transfer Learning Score</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">94.5</div>
            <p className="text-xs text-green-500 mt-1">+5.2% cross-domain</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Discovery Index</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">142</div>
            <p className="text-xs text-muted-foreground mt-1">Novel concepts identified</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <Card>
          <CardHeader>
            <CardTitle>Overall Score Trajectory</CardTitle>
            <CardDescription>Historical capability scores against targets</CardDescription>
          </CardHeader>
          <CardContent className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={overallScores}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis domain={['auto', 'auto']} />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="score" stroke="#8884d8" strokeWidth={2} name="Actual Score" />
                <Line type="monotone" dataKey="target" stroke="#82ca9d" strokeWidth={2} strokeDasharray="5 5" name="Target" />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Capability Distribution</CardTitle>
            <CardDescription>Current scores across primary capability domains</CardDescription>
          </CardHeader>
          <CardContent className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={capabilityDistribution} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" domain={[0, 100]} />
                <YAxis dataKey="category" type="category" width={100} />
                <Tooltip />
                <Bar dataKey="score" fill="#3b82f6" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
