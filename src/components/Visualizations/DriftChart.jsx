import React from "react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine
} from "recharts";

/**
 * DriftChart — inside components/Visualizations/
 * Shows score drift as a filled area chart with a reference line at 70.
 */
const DriftChart = ({ data = [], dataKey = "value", height = 140 }) => (
  <ResponsiveContainer width="100%" height={height}>
    <AreaChart data={data} margin={{ top: 4, right: 4, left: 0, bottom: 0 }}>
      <defs>
        <linearGradient id="driftGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="5%" stopColor="#34d399" stopOpacity={0.25} />
          <stop offset="95%" stopColor="#34d399" stopOpacity={0} />
        </linearGradient>
      </defs>
      <XAxis
        dataKey="day"
        tick={{ fill: "rgba(255,255,255,0.5)", fontSize: 11 }}
      />
      <YAxis
        domain={[0, 100]}
        tick={{ fill: "rgba(255,255,255,0.5)", fontSize: 11 }}
        width={30}
      />
      <Tooltip
        contentStyle={{
          background: "#021726",
          border: "1px solid rgba(255,255,255,0.08)",
          color: "#eafaf5",
          borderRadius: 8
        }}
      />
      <ReferenceLine
        y={70}
        stroke="rgba(245,158,11,0.4)"
        strokeDasharray="4 4"
        label={{ value: "Baseline", fill: "rgba(245,158,11,0.7)", fontSize: 10 }}
      />
      <Area
        type="monotone"
        dataKey={dataKey}
        stroke="#34d399"
        strokeWidth={2}
        fill="url(#driftGrad)"
      />
    </AreaChart>
  </ResponsiveContainer>
);

export default DriftChart;


