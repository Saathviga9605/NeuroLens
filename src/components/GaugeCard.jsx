import React, { useMemo } from "react";

function getColor(value) {
  if (value >= 70) return "#34d399"; // green
  if (value >= 40) return "#f59e0b"; // amber
  return "#ef4444"; // red
}

export default function GaugeCard({ title = "Stability", value = 0, size = 120 }) {
  const normalized = Math.max(0, Math.min(100, Number(value || 0)));
  const strokeWidth = Math.max(6, Math.round(size * 0.08));
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const dashOffset = circumference * (1 - normalized / 100);
  const color = getColor(normalized);

  // unique id for gradient to avoid collisions when multiple gauges render
  const gradId = useMemo(() => `gaugeGrad_${Math.random().toString(36).slice(2, 9)}`, []);

  const container = {
    width: size,
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: 8,
    color: "#eafaf5"
  };

  const titleStyle = { fontSize: 13, fontWeight: 700, color: "#dffbf2", textAlign: "center" };
  const valueStyle = { fontSize: 18, fontWeight: 800, color };

  return (
    <div style={container} aria-label={`${title}: ${Math.round(normalized)}%`} role="group">
      <div style={titleStyle}>{title}</div>

      <svg width={size} height={size} style={{ transform: "rotate(-90deg)" }} aria-hidden>
        <defs>
          <linearGradient id={gradId} x1="0%" x2="100%">
            <stop offset="0%" stopColor={color} stopOpacity="0.95" />
            <stop offset="100%" stopColor={color} stopOpacity="0.9" />
          </linearGradient>
        </defs>

        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="rgba(255,255,255,0.06)"
          strokeWidth={strokeWidth}
          fill="none"
        />

        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={`url(#${gradId})`}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          fill="none"
          strokeDasharray={circumference}
          strokeDashoffset={dashOffset}
        />
      </svg>

      <div style={valueStyle}>{Math.round(normalized)}%</div>
    </div>
  );
}
