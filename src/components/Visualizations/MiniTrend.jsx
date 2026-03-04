import React from 'react';
import { AreaChart, Area, XAxis, Tooltip, ResponsiveContainer } from 'recharts';

const MiniTrend = ({ data = [], dataKey = 'value', height = 60, color = 'var(--accent)' }) => {
  return (
    <div style={{ width: '100%', height }}>
      <ResponsiveContainer>
        <AreaChart data={data} margin={{ top: 0, right: 0, left: 0, bottom: 0 }}>
          <XAxis dataKey="day" hide />
          <Tooltip />
          <Area type="monotone" dataKey={dataKey} stroke={color} fill="var(--accent-light)" strokeWidth={2} dot={false} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};

export default MiniTrend;
