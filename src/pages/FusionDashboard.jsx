import { useEffect, useState } from "react";
import { getHistory } from "../services/api";
import GaugeCard from "../components/GaugeCard";
import TrendChart from "../components/TrendChart";

const FusionDashboard = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchHistory = async () => {
    try {
      const data = await getHistory();
      setHistory(data);
    } catch (err) {
      console.error("Failed to load history", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const latest = history.length > 0 ? history[history.length - 1] : null;

  const chartData = history.map((item, index) => ({
    name: `S${index + 1}`,
    value: item.csi_score
  }));

  return (
    <div style={{ padding: 30 }}>
      <h2>Fusion Dashboard</h2>

      {loading && <div>Loading...</div>}

      {!loading && latest && (
        <>
          <div style={{ marginBottom: 20 }}>
            <GaugeCard
              title="Cognitive Stability Index"
              value={latest.csi_score}
              size={160}
            />
          </div>

          <TrendChart
            title="CSI Trend"
            data={chartData}
            dataKey="value"
          />

          <div style={{ marginTop: 15 }}>
            <strong>Drift:</strong> {latest.drift_flag}
          </div>

          <div>
            <strong>Risk:</strong> {latest.risk_flag}
          </div>
        </>
      )}

      {!loading && history.length === 0 && (
        <div>No sessions recorded yet.</div>
      )}
    </div>
  );
};

export default FusionDashboard;