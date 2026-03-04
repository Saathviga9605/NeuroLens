import React from 'react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

const DriftChart = ({ data = [], dataKey = 'value', height = 140 }) => (
  <ResponsiveContainer width="100%" height={height}>
    <AreaChart data={data}>
      <XAxis dataKey="label" tick={{ fill: 'rgba(255,255,255,0.7)' }} />
      <YAxis tick={{ fill: 'rgba(255,255,255,0.7)' }} />
      <Tooltip />
      <Area type="monotone" dataKey={dataKey} stroke="var(--accent)" fill="var(--accent-light)" />
    </AreaChart>
  </ResponsiveContainer>
);

export default DriftChart;
