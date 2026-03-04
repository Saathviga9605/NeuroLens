import React from 'react';

const AlertCard = ({ level = 'Info', title, detail }) => {
  const color = level === 'High' ? '#ff4d4f' : level === 'Moderate' ? '#ffbd2e' : 'var(--accent)';
  return (
    <div style={{ borderLeft: `4px solid ${color}`, padding: 12, background: 'rgba(255,255,255,0.02)', borderRadius: 8, marginBottom: 12 }}>
      <div style={{ fontWeight: 700 }}>{title} <small style={{ color }}>{level}</small></div>
      <div style={{ color: '#bcd7e6' }}>{detail}</div>
    </div>
  );
};

export default AlertCard;
