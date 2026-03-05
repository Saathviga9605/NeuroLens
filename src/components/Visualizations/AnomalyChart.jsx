import React, { useMemo } from "react";
import { AreaChart, Area, XAxis, Tooltip, ResponsiveContainer } from "recharts";

/**
 * AnomalyChart — inside components/Visualizations/
 * Area chart that highlights spike anomalies with red dots.
 */
const SpikeDot = (props) => {
  const { cx, cy, payload } = props;
  if (cx == null || cy == null) return null;
  const isSpike = payload && payload.__spike;
  return (
    <circle
      cx={cx}
      cy={cy}
      r={isSpike ? 5 : 2}
      fill={isSpike ? "#ef4444" : "var(--accent)"}
      stroke={isSpike ? "rgba(255,255,255,0.2)" : "none"}
      strokeWidth={isSpike ? 2 : 0}
    />
  );
};

const AnomalyChart = ({ data = [], dataKey = "value", height = 80 }) => {
  const processed = useMemo(() => {
    const vals = data.map((d) => Number(d[dataKey] || 0));
    const mean =
      vals.reduce((a, b) => a + b, 0) / Math.max(1, vals.length);
    const std = Math.sqrt(
      vals.reduce((s, v) => s + (v - mean) * (v - mean), 0) /
        Math.max(1, vals.length)
    );
    return data.map((d, i) => {
      const v = Number(d[dataKey] || 0);
      const prev = i > 0 ? Number(data[i - 1][dataKey] || 0) : v;
      const isSpike =
        v > mean + 1.2 * std || (prev > 0 && v > prev * 1.35);
      return { ...d, __spike: isSpike };
    });
  }, [data, dataKey]);

  return (
    <div style={{ width: "100%", height }}>
      <ResponsiveContainer>
        <AreaChart
          data={processed}
          margin={{ top: 4, right: 0, left: 0, bottom: 0 }}
        >
          <defs>
            <linearGradient id="anomalyGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#34d399" stopOpacity={0.25} />
              <stop offset="95%" stopColor="#34d399" stopOpacity={0} />
            </linearGradient>
          </defs>
          <XAxis dataKey="day" hide />
          <Tooltip
            formatter={(v) => [v, dataKey]}
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
            stroke="var(--accent)"
            fill="url(#anomalyGrad)"
            dot={<SpikeDot />}
            strokeWidth={2}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};

export default AnomalyChart;

