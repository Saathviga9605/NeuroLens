import React from 'react';
import { RadialBarChart, RadialBar, ResponsiveContainer } from 'recharts';

const RadialGauge = ({ value = 75, label = 'Score' }) => {
  const data = [{ name: label, value }];
  return (
    <div style={{ width: '100%', height: '100%', minHeight: 120, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <ResponsiveContainer width="100%" height="100%">
        <RadialBarChart
          innerRadius="70%"
          outerRadius="100%"
          data={data}
          startAngle={90}
          endAngle={-270}
          cx="50%"
          cy="50%"
        >
          <RadialBar dataKey="value" fill="var(--accent)" />
        </RadialBarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default RadialGauge;
