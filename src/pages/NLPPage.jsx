import React from "react";
import GaugeCard from "../components/GaugeCard";
import TrendChart from "../components/TrendChart";

const styles = {
  container: { padding: 18, color: "#eafaf5", minHeight: "60vh" },
  title: { fontSize: 20, fontWeight: 800, marginBottom: 12, color: "#34d399" },
  grid: { display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))", gap: 12 },
  card: { background: "rgba(255,255,255,0.03)", padding: 14, borderRadius: 10, minHeight: 120, boxShadow: "0 6px 18px rgba(0,0,0,0.4)" },
  cardTitle: { fontSize: 14, fontWeight: 700, marginBottom: 6, color: "#dffbf2" },
  placeholder: { color: "rgba(255,255,255,0.6)", fontSize: 13 }
};

const sampleSentiment = [
  { name: "Day 1", value: 0.1 },
  { name: "Day 2", value: -0.2 },
  { name: "Day 3", value: 0.3 },
  { name: "Day 4", value: 0.05 }
];

export default function NLPPage() {
  return (
    <div style={styles.container}>
      <div style={styles.title}>NLP Intelligence</div>

      <div style={{ display: "flex", gap: 12, marginBottom: 12 }}>
        <div style={styles.card}>
          <GaugeCard title="Text Stability" value={78} size={140} />
        </div>

        <div style={{ flex: 1 }}>
          <TrendChart title="Sentiment Trend" data={sampleSentiment} dataKey="value" color="#f59e0b" />
        </div>
      </div>

      <div style={styles.grid}>
        <div style={styles.card}>
          <div style={styles.cardTitle}>Keyword Extraction</div>
          <div style={styles.placeholder}>Placeholder for top keywords and frequency.</div>
        </div>

        <div style={styles.card}>
          <div style={styles.cardTitle}>Topic Trends</div>
          <div style={styles.placeholder}>Placeholder for topic modeling trends over time.</div>
        </div>

        <div style={styles.card}>
          <div style={styles.cardTitle}>Conversation Flow</div>
          <div style={styles.placeholder}>Placeholder for conversation structure and turns overview.</div>
        </div>

        <div style={styles.card}>
          <div style={styles.cardTitle}>Transcripts</div>
          <div style={styles.placeholder}>Placeholder for transcript snippets and highlights.</div>
        </div>
      </div>
    </div>
  );
}
