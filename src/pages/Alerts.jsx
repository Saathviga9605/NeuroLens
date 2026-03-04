import React from "react";

const AlertCard = ({ level = "Info", title, detail }) => {
  const color = level === "High" ? "#dc2626" : level === "Moderate" ? "#f59e0b" : "#06b6d4";
  return (
    <div style={{ borderLeft: `4px solid ${color}`, padding: 12, background: 'rgba(255,255,255,0.02)', borderRadius: 8, marginBottom: 12 }}>
      <div style={{ fontWeight: 700 }}>{title} <small style={{ color: color, marginLeft: 8 }}>{level}</small></div>
      <div style={{ color: '#bcd7e6' }}>{detail}</div>
    </div>
  );
};

const Alerts = () => {
  // placeholder alerts
  const alerts = [
    { level: 'High', title: 'Sharp Drift Detected', detail: 'Sentiment drift increased 28% in last 24h' },
    { level: 'Moderate', title: 'Sleep Decrease', detail: 'Average sleep decreased by 1.8 hrs' },
    { level: 'Info', title: 'Local Mode', detail: 'All processing occurring offline' }
  ];

  return (
    <div style={{ maxWidth: 1000, margin: '0 auto', padding: 24 }}>
      <h2>Alerts & Warnings</h2>
      <div style={{ marginTop: 16 }}>
        {alerts.map((a, i) => <AlertCard key={i} {...a} />)}
      </div>
    </div>
  );
};

export default Alerts;
