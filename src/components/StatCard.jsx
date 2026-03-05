import React from "react";

const StatCard = ({ title, value, hint, color = "var(--accent)", children }) => {
  return (
    <div className="card glass">
      <div className="card-body">
        <div className="card-top">
          <div className="card-icon" style={{ background: color }}>
            {children}
          </div>
          <div className="card-meta">
            <div className="card-value">{value}</div>
            <div className="card-title">{title}</div>
          </div>
        </div>
        {hint && <div className="card-hint">{hint}</div>}
      </div>
    </div>
  );
};

export default StatCard;
