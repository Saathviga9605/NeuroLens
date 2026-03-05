import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";
import AnimatedBackground from "../components/AnimatedBackground";
import StatCard from "../components/StatCard";
import TrendChart from "../components/Visualizations/TrendChart";
import DriftChart from "../components/Visualizations/DriftChart";
import RadialGauge from "../components/Visualizations/RadialGauge";
import AlertCard from "../components/AlertCard";
import MiniTrend from "../components/Visualizations/MiniTrend";
import AnomalyChart from "../components/Visualizations/AnomalyChart";
import "./Dashboard.css";

const Dashboard = ({ data, history = [] }) => {
  const hasData = Boolean(data);

  const riskText = hasData
    ? data.risk_flag === 1
      ? "High"
      : "Low"
    : "Pending";

  const getRiskColor = (level) => {
    if (level === "Low") return "#16a34a";
    if (level === "Moderate") return "#f59e0b";
    if (level === "High") return "#dc2626";
    return "#999";
  };

  const trendData = history.map((h, i) => ({
    day: `S${i + 1}`,
    value: h.csi_score ?? 0
  }));

  const MiniLineChart = ({ data, height = 60 }) => (
    <div style={{ width: "100%", height }}>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <XAxis dataKey="day" hide />
          <YAxis hide />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="value"
            stroke="var(--accent)"
            strokeWidth={2}
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );

  return (
    <div className="dashboard-wrap">
      <AnimatedBackground />
      <div className="dashboard-inner">

        <h2 style={{ fontSize: 20, fontWeight: 800 }}>
          Cognitive Stability Dashboard
        </h2>

        {!hasData && (
          <div className="glass" style={{ padding: 24, marginTop: 20 }}>
            No assessment available. Run a simulation first.
          </div>
        )}

        {hasData && (
          <>
            {/* KPI CARDS */}
            <div className="kpis glass">
              <StatCard
                title="Cognitive Stability Index"
                value={`${data.csi_score}%`}
                color="var(--accent)"
              />

              <StatCard
                title="Risk Level"
                value={riskText}
                color={getRiskColor(riskText)}
              />

              <StatCard
                title="Behavioral Score"
                value={`${data.behavioral_score ?? "--"}`}
                color="var(--accent)"
              />
            </div>

            {/* MAIN PANEL */}
            <div className="main-panels">

              <div className="panel-large glass">
                <h3>Overall Stability</h3>

                <div style={{ display: "flex", gap: 30, alignItems: "center" }}>
                  <div style={{ width: 260, height: 260 }}>
                    <RadialGauge value={data.csi_score ?? 0} />
                  </div>

                  <div>
                    <div style={{ fontSize: 42, fontWeight: 800 }}>
                      {data.csi_score}%
                    </div>
                    <div style={{ color: "#9ecbd8" }}>
                      Combined Fusion Score
                    </div>

                    <div style={{ marginTop: 12 }}>
                      Drift Flag:{" "}
                      <strong>
                        {data.drift_flag === 1 ? "Detected" : "Stable"}
                      </strong>
                    </div>
                  </div>
                </div>
              </div>

              <div className="panel-right">
                <div className="glass" style={{ padding: 12 }}>
                  <h4>Stability Trend</h4>
                  <TrendChart data={trendData} height={160} />
                </div>
              </div>
            </div>

            {/* ENGINES */}
            <div style={{ marginTop: 20 }}>
              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "repeat(4,1fr)",
                  gap: 12
                }}
              >
                <div className="glass" style={{ padding: 14 }}>
                  <h4>Behavioral Engine</h4>
                  <div style={{ fontSize: 28, fontWeight: 700 }}>
                    {data.behavioral_score ?? "--"}
                  </div>
                </div>

                <div className="glass" style={{ padding: 14 }}>
                  <h4>NLP Engine</h4>
                  <div style={{ opacity: 0.6 }}>Awaiting Data</div>
                </div>

                <div className="glass" style={{ padding: 14 }}>
                  <h4>Voice Engine</h4>
                  <div style={{ opacity: 0.6 }}>Awaiting Data</div>
                </div>

                <div className="glass" style={{ padding: 14 }}>
                  <h4>Fusion Engine</h4>
                  <div style={{ fontSize: 28, fontWeight: 700 }}>
                    {data.csi_score}%
                  </div>
                </div>
              </div>
            </div>

            {/* DRIFT + ALERTS */}
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "1fr 360px",
                gap: 12,
                marginTop: 20
              }}
            >
              <div className="glass" style={{ padding: 12 }}>
                <h4>Drift Visualization</h4>
                <DriftChart data={trendData} />
              </div>

              <div className="glass" style={{ padding: 12 }}>
                <h4>System Alerts</h4>

                {data.drift_flag === 1 && (
                  <AlertCard
                    level="Moderate"
                    title="Cognitive Drift Detected"
                    detail="Recent score deviates from historical baseline."
                  />
                )}

                {data.risk_flag === 1 && (
                  <AlertCard
                    level="High"
                    title="Elevated Risk Pattern"
                    detail="Stability index crossed threshold."
                  />
                )}
              </div>
            </div>

            {/* MINI TRENDS */}
            <div
              style={{
                gridColumn: "1/13",
                display: "grid",
                gridTemplateColumns: "repeat(3,1fr)",
                gap: 12,
                marginTop: 20
              }}
            >
              <div className="glass" style={{ padding: 12 }}>
                <div style={{ fontSize: 12, marginBottom: 8 }}>
                  CSI Mini Trend
                </div>
                <MiniLineChart data={trendData} />
              </div>

              <div className="glass" style={{ padding: 12 }}>
                <div style={{ fontSize: 12, marginBottom: 8 }}>
                  Drift Indicator
                </div>
                <AnomalyChart data={trendData} height={60} />
              </div>

              <div className="glass" style={{ padding: 12 }}>
                <div style={{ fontSize: 12, marginBottom: 8 }}>
                  Historical Overview
                </div>
                <MiniTrend data={trendData} dataKey="value" />
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
