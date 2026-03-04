import React from "react";
import GaugeCard from "../components/GaugeCard";
import TrendChart from "../components/TrendChart";

const styles = {
  container: { padding: 18, color: "#eafaf5", minHeight: "60vh" },
  title: { fontSize: 20, fontWeight: 800, marginBottom: 12, color: "#34d399" },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))",
    gap: 12
  },
  card: {
    background: "rgba(255,255,255,0.03)",
    padding: 14,
    borderRadius: 10,
    minHeight: 120,
    boxShadow: "0 6px 18px rgba(0,0,0,0.4)"
  },
  cardTitle: { fontSize: 14, fontWeight: 700, marginBottom: 6, color: "#dffbf2" },
  placeholder: { color: "rgba(255,255,255,0.6)", fontSize: 13 }
};

const sampleTyping = [
  { name: "T1", value: 40 },
  { name: "T2", value: 45 },
  { name: "T3", value: 52 },
  { name: "T4", value: 48 },
  { name: "T5", value: 55 }
];

const sampleSleep = [
  { name: "Mon", value: 6 },
  { name: "Tue", value: 7 },
  { name: "Wed", value: 5.5 },
  { name: "Thu", value: 7.5 },
  { name: "Fri", value: 6.2 }
];

export default function BehavioralPage() {
  return (
    <div style={styles.container}>
      <div style={styles.title}>Behavioral Intelligence</div>

      <div style={{ display: "flex", gap: 12, marginBottom: 12, flexWrap: "wrap" }}>
        <div style={styles.card}>
          <GaugeCard title="Behavioral Stability" value={72} size={140} />
        </div>
        <div style={{ flex: 1, minWidth: 280 }}>
          <div style={{ marginBottom: 12 }}>
            <TrendChart
              title="Typing Variability"
              data={sampleTyping}
              dataKey="value"
              color="#60a5fa"
            />
          </div>
          <TrendChart
            title="Sleep Duration"
            data={sampleSleep}
            dataKey="value"
            color="#34d399"
          />
        </div>
      </div>

      <div style={styles.grid}>
        <div style={styles.card}>
          <div style={styles.cardTitle}>Session Timeline</div>
          <div style={styles.placeholder}>
            Timeline of recorded sessions and notable events.
          </div>
        </div>
        <div style={styles.card}>
          <div style={styles.cardTitle}>Activity Overview</div>
          <div style={styles.placeholder}>
            Activity summary and quick KPIs.
          </div>
        </div>
        <div style={styles.card}>
          <div style={styles.cardTitle}>Keystroke Patterns</div>
          <div style={styles.placeholder}>
            Raw keystroke heatmap and timing gaps.
          </div>
        </div>
        <div style={styles.card}>
          <div style={styles.cardTitle}>Notes</div>
          <div style={styles.placeholder}>
            Analyst notes and session annotations.
          </div>
        </div>
      </div>
    </div>
  );
}
