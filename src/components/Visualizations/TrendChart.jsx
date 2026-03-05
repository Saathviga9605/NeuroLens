import React from "react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid
} from "recharts";

/**
 * TrendChart — inside components/Visualizations/
 * Props: title, data [{day, value}], dataKey, color, height
 */
export default function TrendChart({
  title = "Trend",
  data = [],
  dataKey = "value",
  color = "#34d399",
  height = 160
}) {
  return (
    <div
      style={{
        background: "rgba(255,255,255,0.02)",
        padding: 12,
        borderRadius: 10,
        color: "#eafaf5"
      }}
    >
      {title && (
        <div
          style={{
            fontSize: 13,
            fontWeight: 700,
            marginBottom: 8,
            color: "#dffbf2"
          }}
        >
          {title}
        </div>
      )}
      <div style={{ width: "100%", height }}>
        <ResponsiveContainer>
          <LineChart
            data={data}
            margin={{ top: 4, right: 8, left: 0, bottom: 0 }}
          >
            <CartesianGrid
              stroke="rgba(255,255,255,0.04)"
              vertical={false}
            />
            <XAxis
              dataKey="day"
              tick={{ fill: "rgba(255,255,255,0.5)", fontSize: 11 }}
            />
            <YAxis
              tick={{ fill: "rgba(255,255,255,0.5)", fontSize: 11 }}
              width={32}
            />
            <Tooltip
              contentStyle={{
                background: "#021726",
                border: "1px solid rgba(255,255,255,0.08)",
                color: "#eafaf5",
                borderRadius: 8
              }}
            />
            <Line
              type="monotone"
              dataKey={dataKey}
              stroke={color}
              strokeWidth={2.5}
              dot={false}
              activeDot={{ r: 4, fill: color }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
