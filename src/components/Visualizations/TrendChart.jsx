import React from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from 'recharts';

const TrendChart = ({ data = [], dataKey = 'score', height = 220 }) => {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" strokeOpacity={0.06} />
        <XAxis dataKey="day" tick={{ fill: 'rgba(255,255,255,0.7)' }} />
        <YAxis tick={{ fill: 'rgba(255,255,255,0.7)' }} />
        <Tooltip />
        <Line type="monotone" dataKey={dataKey} stroke="var(--accent)" strokeWidth={2} dot={false} />
      </LineChart>
    </ResponsiveContainer>
  );
};

export default TrendChart;
