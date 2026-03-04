import React from "react";
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

// TrendChart
// Props:
// - title: string
// - data: array of objects [{name: 'T1', value: 10}, ...]
// - dataKey: string (defaults to 'value')
// - color: stroke color

export default function TrendChart({ title = "Trend", data = [], dataKey = "value", color = "#34d399" }) {
  const container = { background: "rgba(255,255,255,0.02)", padding: 12, borderRadius: 10, color: "#eafaf5" };
  const titleStyle = { fontSize: 14, fontWeight: 700, marginBottom: 8, color: "#dffbf2" };

  return (
    <div style={container}>
      <div style={titleStyle}>{title}</div>
      <div style={{ width: "100%", height: 160 }}>
        <ResponsiveContainer>
          <LineChart data={data} margin={{ top: 8, right: 8, left: 0, bottom: 0 }}>
            <CartesianGrid stroke="rgba(255,255,255,0.03)" vertical={false} />
            <XAxis dataKey="name" tick={{ fill: "rgba(255,255,255,0.6)", fontSize: 12 }} />
            <YAxis tick={{ fill: "rgba(255,255,255,0.6)", fontSize: 12 }} />
            <Tooltip contentStyle={{ background: "#021726", border: "1px solid rgba(255,255,255,0.04)", color: "#eafaf5" }} />
            <Line type="monotone" dataKey={dataKey} stroke={color} strokeWidth={2.5} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
