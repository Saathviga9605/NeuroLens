import React, { useMemo } from 'react';
import { AreaChart, Area, XAxis, Tooltip, ResponsiveContainer } from 'recharts';

const SpikeDot = (props) => {
  const { cx, cy, payload } = props;
  if (cx == null || cy == null) return null;
  const isSpike = payload && payload.__spike;
  return (
    <circle cx={cx} cy={cy} r={isSpike ? 5 : 2} fill={isSpike ? '#ff4d4f' : 'var(--accent)'} stroke={isSpike ? '#ffffff22' : 'none'} />
  );
};

const AnomalyChart = ({ data = [], dataKey = 'value', height = 80 }) => {
  // detect spikes: value > mean + 1.2*std OR > previous*1.35
  const processed = useMemo(() => {
    const vals = data.map(d => Number(d[dataKey] || 0));
    const mean = vals.reduce((a,b)=>a+b,0) / Math.max(1, vals.length);
    const std = Math.sqrt(vals.reduce((s,v)=>s+(v-mean)*(v-mean),0) / Math.max(1, vals.length));
    return data.map((d,i)=>{
      const v = Number(d[dataKey]||0);
      const prev = i>0 ? Number(data[i-1][dataKey]||0) : v;
      const isSpike = v > mean + 1.2*std || (prev>0 && v > prev*1.35);
      return { ...d, __spike: isSpike };
    });
  }, [data, dataKey]);

  return (
    <div style={{ width: '100%', height }}>
      <ResponsiveContainer>
        <AreaChart data={processed} margin={{ top: 4, right: 0, left: 0, bottom: 0 }}>
          <XAxis dataKey="day" hide />
          <Tooltip formatter={(value, name) => [value, dataKey]} />
          <Area type="monotone" dataKey={dataKey} stroke="var(--accent)" fill="var(--accent-light)" dot={<SpikeDot/>} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};

export default AnomalyChart;
