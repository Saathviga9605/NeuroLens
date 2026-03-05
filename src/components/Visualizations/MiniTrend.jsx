import React from "react";
import { AreaChart, Area, XAxis, Tooltip, ResponsiveContainer } from "recharts";

/**
 * MiniTrend — inside components/Visualizations/
 * Compact sparkline-style trend area chart.
 */
const MiniTrend = ({
  data = [],
  dataKey = "value",
  height = 60,
  color = "var(--accent)"
}) => (
  <div style={{ width: "100%", height }}>
    <ResponsiveContainer>
      <AreaChart data={data} margin={{ top: 2, right: 0, left: 0, bottom: 0 }}>
        <defs>
          <linearGradient id="miniGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#34d399" stopOpacity={0.3} />
            <stop offset="95%" stopColor="#34d399" stopOpacity={0} />
          </linearGradient>
        </defs>
        <XAxis dataKey="day" hide />
        <Tooltip
          contentStyle={{
            background: "#021726",
            border: "1px solid rgba(255,255,255,0.08)",
            color: "#eafaf5",
            borderRadius: 6,
            fontSize: 12
          }}
        />
        <Area
          type="monotone"
          dataKey={dataKey}
          stroke={color}
          fill="url(#miniGrad)"
          strokeWidth={2}
          dot={false}
        />
      </AreaChart>
    </ResponsiveContainer>
  </div>
);

export default MiniTrend;

