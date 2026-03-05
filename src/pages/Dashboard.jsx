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

        <h2>Cognitive Stability Dashboard</h2>

        {!hasData && (
          <div className="glass" style={{ padding: 48, marginTop: 32, textAlign: "center" }}>
            <div style={{ 
              width: 64, 
              height: 64, 
              margin: "0 auto 16px",
              borderRadius: 16,
              background: "linear-gradient(135deg, rgba(52, 211, 153, 0.1), rgba(52, 211, 153, 0.05))",
              border: "2px dashed rgba(52, 211, 153, 0.3)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 24,
              fontWeight: 900,
              color: "#34d399"
            }}>—</div>
            <div style={{ fontSize: 18, color: "#94a3b8", marginBottom: 8 }}>
              No assessment available
            </div>
            <div style={{ fontSize: 14, color: "#64748b" }}>
              Run a simulation to generate cognitive analysis data
            </div>
          </div>
        )}

        {hasData && (
          <>
            {/* KPI CARDS */}
            <div className="kpis">
              <StatCard
                title="Cognitive Stability Index"
                value={`${data.csi_score}%`}
                color="#34d399"
                hint="Overall cognitive wellness score"
              />

              <StatCard
                title="Risk Level"
                value={riskText}
                color={getRiskColor(riskText)}
                hint={`Current mental health risk assessment`}
              />

              <StatCard
                title="Behavioral Score"
                value={`${data.behavioral_score ?? "--"}`}
                color="#60a5fa"
                hint="Activity pattern analysis"
              />
            </div>

            {/* MAIN PANEL */}
            <div className="main-panels">

              <div className="panel-large glass">
                <h3 style={{ marginBottom: 24 }}>Overall Stability Analysis</h3>

                <div style={{ display: "flex", gap: 40, alignItems: "center" }}>
                  <div style={{ 
                    width: 280, 
                    height: 280,
                    position: "relative"
                  }}>
                    <RadialGauge value={data.csi_score ?? 0} />
                  </div>

                  <div style={{ flex: 1 }}>
                    <div style={{ 
                      fontSize: 64, 
                      fontWeight: 900,
                      background: "linear-gradient(135deg, #34d399 0%, #10b981 100%)",
                      WebkitBackgroundClip: "text",
                      WebkitTextFillColor: "transparent",
                      backgroundClip: "text",
                      lineHeight: 1,
                      letterSpacing: "-0.03em"
                    }}>
                      {data.csi_score}%
                    </div>
                    <div style={{ 
                      color: "#94a3b8",
                      fontSize: 16,
                      marginTop: 8,
                      marginBottom: 24
                    }}>
                      Combined Fusion Score
                    </div>

                    <div style={{ 
                      display: "flex", 
                      gap: 16,
                      flexWrap: "wrap"
                    }}>
                      <div style={{
                        background: data.drift_flag === 1 
                          ? "rgba(251, 191, 36, 0.1)" 
                          : "rgba(52, 211, 153, 0.1)",
                        border: `1px solid ${data.drift_flag === 1 ? "rgba(251, 191, 36, 0.3)" : "rgba(52, 211, 153, 0.3)"}`,
                        padding: "12px 20px",
                        borderRadius: 10,
                        fontSize: 14,
                        position: "relative",
                        paddingLeft: 28
                      }}>
                        <div style={{
                          position: "absolute",
                          left: 12,
                          top: "50%",
                          transform: "translateY(-50%)",
                          width: 3,
                          height: 24,
                          background: data.drift_flag === 1 
                            ? "linear-gradient(180deg, #fbbf24, #f59e0b)"
                            : "linear-gradient(180deg, #34d399, #10b981)",
                          borderRadius: 2
                        }} />
                        <div style={{ 
                          fontSize: 11, 
                          color: "#64748b",
                          textTransform: "uppercase",
                          letterSpacing: 1,
                          marginBottom: 4
                        }}>
                          Drift Status
                        </div>
                        <div style={{ 
                          fontWeight: 700,
                          color: data.drift_flag === 1 ? "#fbbf24" : "#34d399"
                        }}>
                          {data.drift_flag === 1 ? "Detected" : "Stable"}
                        </div>
                      </div>

                      <div style={{
                        background: data.risk_flag === 1 
                          ? "rgba(239, 68, 68, 0.1)" 
                          : "rgba(52, 211, 153, 0.1)",
                        border: `1px solid ${data.risk_flag === 1 ? "rgba(239, 68, 68, 0.3)" : "rgba(52, 211, 153, 0.3)"}`,
                        padding: "12px 20px",
                        borderRadius: 10,
                        fontSize: 14,
                        position: "relative",
                        paddingLeft: 28
                      }}>
                        <div style={{
                          position: "absolute",
                          left: 12,
                          top: "50%",
                          transform: "translateY(-50%)",
                          width: 3,
                          height: 24,
                          background: data.risk_flag === 1 
                            ? "linear-gradient(180deg, #ef4444, #dc2626)"
                            : "linear-gradient(180deg, #34d399, #10b981)",
                          borderRadius: 2
                        }} />
                        <div style={{ 
                          fontSize: 11, 
                          color: "#64748b",
                          textTransform: "uppercase",
                          letterSpacing: 1,
                          marginBottom: 4
                        }}>
                          Risk Assessment
                        </div>
                        <div style={{ 
                          fontWeight: 700,
                          color: data.risk_flag === 1 ? "#ef4444" : "#34d399"
                        }}>
                          {data.risk_flag === 1 ? "High" : "Low"}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="panel-right">
                <div className="glass" style={{ padding: 24 }}>
                  <h3 style={{ marginBottom: 16 }}>Stability Trend</h3>
                  <TrendChart data={trendData} height={180} />
                </div>
              </div>
            </div>

            {/* ENGINES */}
            <div style={{ marginTop: 32 }}>
              <h3 style={{ marginBottom: 16, fontSize: 16 }}>AI Engine Status</h3>
              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
                  gap: 20
                }}
              >
                <div className="glass" style={{ padding: 24, textAlign: "center" }}>
                  <div style={{ 
                    width: 48, 
                    height: 48, 
                    margin: "0 auto 12px",
                    borderRadius: 12,
                    background: "linear-gradient(135deg, #34d399 0%, #10b981 100%)",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: 16,
                    fontWeight: 900,
                    color: "#0a0e1a"
                  }}>BE</div>
                  <h4 style={{ color: "#e0f2fe" }}>Behavioral Engine</h4>
                  <div style={{ 
                    fontSize: 36, 
                    fontWeight: 800,
                    background: "linear-gradient(135deg, #34d399 0%, #10b981 100%)",
                    WebkitBackgroundClip: "text",
                    WebkitTextFillColor: "transparent",
                    backgroundClip: "text",
                    marginTop: 12
                  }}>
                    {data.behavioral_score ?? "--"}
                  </div>
                  <div style={{ 
                    fontSize: 11, 
                    color: "#34d399", 
                    marginTop: 8,
                    fontWeight: 600,
                    textTransform: "uppercase",
                    letterSpacing: 1
                  }}>Active</div>
                </div>

                <div className="glass" style={{ padding: 24, textAlign: "center", opacity: 0.6 }}>
                  <div style={{ 
                    width: 48, 
                    height: 48, 
                    margin: "0 auto 12px",
                    borderRadius: 12,
                    background: "linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%)",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: 16,
                    fontWeight: 900,
                    color: "#0a0e1a"
                  }}>NL</div>
                  <h4 style={{ color: "#e0f2fe" }}>NLP Engine</h4>
                  <div style={{ fontSize: 14, color: "#64748b", marginTop: 20 }}>
                    Awaiting Data
                  </div>
                  <div style={{ 
                    fontSize: 11, 
                    color: "#64748b", 
                    marginTop: 8,
                    fontWeight: 600,
                    textTransform: "uppercase",
                    letterSpacing: 1
                  }}>Standby</div>
                </div>

                <div className="glass" style={{ padding: 24, textAlign: "center", opacity: 0.6 }}>
                  <div style={{ 
                    width: 48, 
                    height: 48, 
                    margin: "0 auto 12px",
                    borderRadius: 12,
                    background: "linear-gradient(135deg, #a78bfa 0%, #8b5cf6 100%)",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: 16,
                    fontWeight: 900,
                    color: "#0a0e1a"
                  }}>VO</div>
                  <h4 style={{ color: "#e0f2fe" }}>Voice Engine</h4>
                  <div style={{ fontSize: 14, color: "#64748b", marginTop: 20 }}>
                    Awaiting Data
                  </div>
                  <div style={{ 
                    fontSize: 11, 
                    color: "#64748b", 
                    marginTop: 8,
                    fontWeight: 600,
                    textTransform: "uppercase",
                    letterSpacing: 1
                  }}>Standby</div>
                </div>

                <div className="glass" style={{ padding: 24, textAlign: "center" }}>
                  <div style={{ 
                    width: 48, 
                    height: 48, 
                    margin: "0 auto 12px",
                    borderRadius: 12,
                    background: "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: 16,
                    fontWeight: 900,
                    color: "#0a0e1a"
                  }}>FU</div>
                  <h4 style={{ color: "#e0f2fe" }}>Fusion Engine</h4>
                  <div style={{ 
                    fontSize: 36, 
                    fontWeight: 800,
                    background: "linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%)",
                    WebkitBackgroundClip: "text",
                    WebkitTextFillColor: "transparent",
                    backgroundClip: "text",
                    marginTop: 12
                  }}>
                    {data.csi_score}%
                  </div>
                  <div style={{ 
                    fontSize: 11, 
                    color: "#60a5fa", 
                    marginTop: 8,
                    fontWeight: 600,
                    textTransform: "uppercase",
                    letterSpacing: 1
                  }}>Active</div>
                </div>
              </div>
            </div>

            {/* DRIFT + ALERTS */}
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "1.5fr 1fr",
                gap: 20,
                marginTop: 32
              }}
            >
              <div className="glass" style={{ padding: 24 }}>
                <h3 style={{ marginBottom: 16 }}>Drift Visualization</h3>
                <DriftChart data={trendData} />
              </div>

              <div className="glass" style={{ padding: 24 }}>
                <h3 style={{ marginBottom: 16 }}>System Alerts</h3>

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
