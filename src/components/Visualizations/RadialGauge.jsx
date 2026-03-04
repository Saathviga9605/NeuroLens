import React, { useMemo } from "react";

/**
 * RadialGauge — inside components/Visualizations/
 * SVG-based radial gauge (avoids recharts RadialBarChart quirks).
 * Props: value (0-100), size
 */
const RadialGauge = ({ value = 0, size = 240 }) => {
  const normalized = Math.max(0, Math.min(100, Number(value) || 0));
  const strokeWidth = size * 0.09;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const dashOffset = circumference * (1 - normalized / 100);

  const color =
    normalized >= 70 ? "#34d399" : normalized >= 40 ? "#f59e0b" : "#ef4444";

  const gradId = useMemo(
    () => `radialGrad_${Math.random().toString(36).slice(2, 7)}`,
    []
  );

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        position: "relative"
      }}
    >
      <svg
        width={size}
        height={size}
        style={{ transform: "rotate(-90deg)" }}
        aria-label={`Stability: ${Math.round(normalized)}%`}
      >
        <defs>
          <linearGradient id={gradId} x1="0%" x2="100%">
            <stop offset="0%" stopColor={color} stopOpacity="0.9" />
            <stop offset="100%" stopColor={color} stopOpacity="1" />
          </linearGradient>
        </defs>

        {/* Track */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="rgba(255,255,255,0.07)"
          strokeWidth={strokeWidth}
          fill="none"
        />

        {/* Progress */}
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
          style={{ transition: "stroke-dashoffset 0.6s ease" }}
        />
      </svg>

      {/* Center label */}
      <div
        style={{
          position: "absolute",
          textAlign: "center",
          pointerEvents: "none"
        }}
      >
        <div style={{ fontSize: size * 0.18, fontWeight: 800, color }}>
          {Math.round(normalized)}%
        </div>
        <div
          style={{
            fontSize: size * 0.07,
            color: "rgba(255,255,255,0.5)",
            marginTop: 2
          }}
        >
          CSI
        </div>
      </div>
    </div>
  );
};

export default RadialGauge;

