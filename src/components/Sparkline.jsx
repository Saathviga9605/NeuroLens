import React from "react";
import { AreaChart, Area, ResponsiveContainer } from "recharts";

const Sparkline = ({ dataKey = "value", data = [] }) => (
  <div style={{ width: 120, height: 36 }}>
    <ResponsiveContainer>
      <AreaChart data={data} margin={{ top: 0, right: 0, left: 0, bottom: 0 }}>
        <Area type="monotone" dataKey={dataKey} stroke="var(--accent)" fill="var(--accent-light)" strokeWidth={2} />
      </AreaChart>
    </ResponsiveContainer>
  </div>
);

export default Sparkline;
