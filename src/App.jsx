import { useState, useEffect } from "react";
import Dashboard from "./pages/Dashboard";
import InputPage from "./pages/InputPage";
import PrivacyPage from "./pages/PrivacyPage";
import Simulation from "./pages/Simulation";
import Alerts from "./pages/Alerts";
import FusionResults from "./pages/FusionResults";
import EnginesPanel from "./components/EnginesPanel";

function App() {
  const [page, setPage] = useState("simulation");
  const [analysisResult, setAnalysisResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [fused, setFused] = useState(null);

  // load persisted state on startup
  useEffect(() => {
    try {
      const h = localStorage.getItem("cd_history");
      const f = localStorage.getItem("cd_fused");
      if (h) setHistory(JSON.parse(h));
      if (f) setFused(JSON.parse(f));
    } catch (e) {}
  }, []);

  // persist history and fused results
  useEffect(() => {
    try {
      localStorage.setItem("cd_history", JSON.stringify(history));
    } catch (e) {}
  }, [history]);

  useEffect(() => {
    try {
      localStorage.setItem("cd_fused", JSON.stringify(fused));
    } catch (e) {}
  }, [fused]);

  // Called by pages/components when a new analysis result is produced
  const handleNewResult = (result) => {
    if (!result) return;
    setAnalysisResult(result);

    setHistory((prev) => [
      ...prev,
      {
        day: `Entry ${prev.length + 1}`,
        score: result.stability_score,
        breakdown: result.breakdown || {}
      }
    ]);
  };

  // keep fused state managed here (can be set by EnginesPanel or Simulation)
  const handleFusionResult = (fusion) => {
    if (!fusion) return;
    setFused(fusion);
    // also treat fused result as a primary analysis result (optional)
    handleNewResult(fusion);
  };

  // Auto-navigate to dashboard when a new result arrives
  useEffect(() => {
    if (analysisResult) {
      setPage("dashboard");
    }
  }, [analysisResult]);

  // Layout styles (inline for simplicity)
  const SIDEBAR_WIDTH = 240; // fixed width as requested
  const styles = {
    root: { minHeight: "100vh", display: "flex", background: "#021726", color: "#eafaf5", fontFamily: "Inter, system-ui, -apple-system, 'Segoe UI', Roboto, Arial" },
    sidebar: { width: SIDEBAR_WIDTH, padding: 20, borderRight: "1px solid rgba(255,255,255,0.03)", boxSizing: "border-box", display: "flex", flexDirection: "column", gap: 10, background: "rgba(0,0,0,0.02)" },
    brand: { fontSize: 16, fontWeight: 800, color: "#34d399", marginBottom: 8 },
    navButton: { background: "transparent", border: "none", color: "#dffbf2", padding: "10px 12px", borderRadius: 8, textAlign: "left", cursor: "pointer", fontWeight: 600 },
    navButtonActive: { background: "rgba(52,211,153,0.08)", color: "#34d399", boxShadow: "inset 4px 0 0 #34d399" },
    contentWrap: { flex: 1, minWidth: 0, display: "flex", flexDirection: "column" },
    header: { padding: "10px 20px", borderBottom: "1px solid rgba(255,255,255,0.02)", display: "flex", alignItems: "center", justifyContent: "space-between" },
    status: { fontSize: 13, color: "rgba(255,255,255,0.78)" },
    main: { padding: 18, overflow: "auto", flex: 1 }
  };

  // Page renderers (only restructure; logic unchanged)
  const renderMain = () => {
    switch (page) {
      case "dashboard":
        return <Dashboard data={analysisResult} history={history} />;
      case "behavior":
        return <div>
          <h2>Behavioral Intelligence</h2>
          <p style={{ color: "#9fd8c9" }}>Behavioral engine outputs and metrics.</p>
          <div style={{ marginTop: 12 }}>
            <EnginesPanel onPartResult={handleNewResult} onFusion={handleFusionResult} onNavigate={setPage} />
          </div>
        </div>;
      case "voice":
        return <div>
          <h2>Voice Intelligence</h2>
          <p style={{ color: "#9fd8c9" }}>Voice analysis tools and summaries will appear here.</p>
        </div>;
      case "nlp":
        return <div>
          <h2>NLP Intelligence</h2>
          <p style={{ color: "#9fd8c9" }}>Text analytics and sentiment insights will appear here.</p>
        </div>;
      case "simulation":
        return <Simulation onResult={handleNewResult} />;
      case "privacy":
        return <PrivacyPage />;
      default:
        return <Dashboard data={analysisResult} history={history} />;
    }
  };

  return (
    <div style={styles.root}>
      <aside style={styles.sidebar}>
        <div style={styles.brand}>Cognitive Monitoring</div>

        <button style={page === "dashboard" ? { ...styles.navButton, ...styles.navButtonActive } : styles.navButton} onClick={() => setPage("dashboard")}>Dashboard</button>

        <button style={page === "behavior" ? { ...styles.navButton, ...styles.navButtonActive } : styles.navButton} onClick={() => setPage("behavior")}>Behavioral Intelligence</button>

        <button style={page === "voice" ? { ...styles.navButton, ...styles.navButtonActive } : styles.navButton} onClick={() => setPage("voice")}>Voice Intelligence</button>

        <button style={page === "nlp" ? { ...styles.navButton, ...styles.navButtonActive } : styles.navButton} onClick={() => setPage("nlp")}>NLP Intelligence</button>

        <button style={page === "simulation" ? { ...styles.navButton, ...styles.navButtonActive } : styles.navButton} onClick={() => setPage("simulation")}>User Simulation</button>

        <button style={page === "privacy" ? { ...styles.navButton, ...styles.navButtonActive } : styles.navButton} onClick={() => setPage("privacy")}>Privacy & Ethics</button>

        <div style={{ flex: 1 }} />
        <div style={{ fontSize: 12, color: "rgba(255,255,255,0.6)" }}>Status: Offline • Local processing</div>
      </aside>

      <div style={styles.contentWrap}>
        <header style={styles.header}>
          <div style={{ fontWeight: 800 }}>{page === 'dashboard' ? 'Dashboard' : page === 'behavior' ? 'Behavioral Intelligence' : page === 'voice' ? 'Voice Intelligence' : page === 'nlp' ? 'NLP Intelligence' : page === 'simulation' ? 'User Simulation' : 'Privacy & Ethics'}</div>
          <div style={styles.status}>Demo — for research use only</div>
        </header>

        <main style={styles.main}>
          {renderMain()}
        </main>
      </div>

      <style>{`
        @media (max-width: 900px) {
          div[style*="width: 240px"] { width: 100% !important; }
          div[style*="display: flex"][style*="flex-direction: row"] { flex-direction: column; }
        }
      `}</style>
    </div>
  );
}

export default App;