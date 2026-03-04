import React from "react";

// AlertBanner
// Props:
// - message: string
// - severity: 'low' | 'moderate' | 'high' (defaults to 'moderate')

const severityMap = {
  low: { bg: "rgba(52,211,153,0.09)", border: "#34d399", text: "#dffbf2", label: "Low" },
  moderate: { bg: "rgba(245,158,11,0.08)", border: "#f59e0b", text: "#fff3d1", label: "Moderate" },
  high: { bg: "rgba(239,68,68,0.08)", border: "#ef4444", text: "#ffd1d1", label: "High" }
};

export default function AlertBanner({ message = "", severity = "moderate" }) {
  const s = severityMap[severity] || severityMap.moderate;
  const container = { background: s.bg, borderLeft: `4px solid ${s.border}`, padding: "10px 12px", borderRadius: 8, color: s.text, display: "flex", gap: 12, alignItems: "center" };
  const labelStyle = { fontWeight: 800, fontSize: 13 };
  const msgStyle = { fontSize: 13, color: s.text };

  return (
    <div style={container} role="status" aria-live="polite">
      <div style={labelStyle}>{s.label}</div>
      <div style={msgStyle}>{message}</div>
    </div>
  );
}
