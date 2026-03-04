import React from "react";

const FusionResults = ({ result }) => {
  if (!result) {
    return (
      <div style={{ padding: 24 }}>
        <h2>Fusion Results</h2>
        <div style={{ marginTop: 12, color: '#bcd7e6' }}>No fused result yet. Run an analysis from Simulation.</div>
      </div>
    );
  }

  return (
    <div style={{ padding: 24 }}>
      <h2>Fusion Results</h2>
      <div style={{ marginTop: 12 }}>
        <div style={{ fontSize: 36, fontWeight: 800 }}>{result.stability_score}%</div>
        <div style={{ color: '#cfeaf6', marginTop: 8 }}>Risk: {result.risk_level}</div>
        <div style={{ marginTop: 12 }}>
          <strong>Reasons</strong>
          <ul>
            {result.reasons?.map((r, i) => <li key={i}>{r}</li>)}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default FusionResults;
