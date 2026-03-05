import React from "react";

const StatCard = ({ title, value, hint, color = "var(--accent)", icon, trend }) => {
  return (
    <div className="card glass">
      <div className="card-body">
        <div className="card-top">
          <div 
            className="card-icon" 
            style={{ 
              background: color ? `linear-gradient(135deg, ${color}40, ${color}20)` : undefined,
              boxShadow: color ? `0 4px 12px ${color}40` : undefined,
              position: "relative",
              overflow: "hidden"
            }}
          >
            <div style={{
              position: "absolute",
              inset: 0,
              background: `linear-gradient(135deg, ${color}, transparent)`,
              opacity: 0.3
            }} />
          </div>
          <div className="card-meta">
            <div className="card-value" style={{ color: color }}>
              {value}
              {trend && (
                <span style={{ 
                  fontSize: '0.5em', 
                  marginLeft: '8px',
                  color: trend > 0 ? '#34d399' : '#f87171'
                }}>
                  {trend > 0 ? '↑' : '↓'} {Math.abs(trend)}%
                </span>
              )}
            </div>
            <div className="card-title">{title}</div>
          </div>
        </div>
        {hint && (
          <div className="card-hint">
            <div style={{
              width: 3,
              height: 3,
              borderRadius: "50%",
              background: color,
              display: "inline-block",
              marginRight: 8,
              opacity: 0.6
            }} />
            {hint}
          </div>
        )}
      </div>
    </div>
  );
};

export default StatCard;
