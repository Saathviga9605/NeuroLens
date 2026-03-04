import React from "react";
import GaugeCard from "../components/GaugeCard";
import TrendChart from "../components/TrendChart";
import AlertBanner from "../components/AlertBanner";

const styles = {
  container: { padding: 18, color: "#eafaf5", minHeight: "60vh" },
  title: { fontSize: 20, fontWeight: 800, marginBottom: 12, color: "#34d399" },
  grid: { display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))", gap: 12 },
  card: { background: "rgba(255,255,255,0.03)", padding: 14, borderRadius: 10, minHeight: 120, boxShadow: "0 6px 18px rgba(0,0,0,0.4)" },
  cardTitle: { fontSize: 14, fontWeight: 700, marginBottom: 6, color: "#dffbf2" },
  placeholder: { color: "rgba(255,255,255,0.6)", fontSize: 13 }
};

const sampleProsody = [
  { name: "S1", value: 0.6 },
  { name: "S2", value: 0.7 },
  { name: "S3", value: 0.5 },
  { name: "S4", value: 0.8 }
];

export default function VoicePage() {
  return (
    <div style={styles.container}>
      <div style={styles.title}>Voice Intelligence</div>

      <div style={{ marginBottom: 12 }}>
        <AlertBanner message="No recent audio uploads" severity="low" />
      </div>

      <div style={{ display: "flex", gap: 12, marginBottom: 12 }}>
        <div style={styles.card}>
          <GaugeCard title="Vocal Stability" value={65} size={140} />
        </div>

        <div style={{ flex: 1 }}>
          <TrendChart title="Prosody Metric" data={sampleProsody} dataKey="value" color="#f472b6" />
        </div>
      </div>

      <div style={styles.grid}>
        <div style={styles.card}>
          <div style={styles.cardTitle}>Speech Rate</div>
          <div style={styles.placeholder}>Placeholder for speaking rate, pauses, and articulation metrics.</div>
        </div>

        <div style={styles.card}>
          <div style={styles.cardTitle}>Emotion Timeline</div>
          <div style={styles.placeholder}>Placeholder for emotion detection timeline across sessions.</div>
        </div>

        <div style={styles.card}>
          <div style={styles.cardTitle}>Audio Samples</div>
          <div style={styles.placeholder}>Placeholder for recent audio clips and playback controls.</div>
        </div>

        <div style={styles.card}>
          <div style={styles.cardTitle}>Notes</div>
          <div style={styles.placeholder}>Placeholder for annotations and transcription snippets.</div>
        </div>
      </div>
    </div>
  );
}
