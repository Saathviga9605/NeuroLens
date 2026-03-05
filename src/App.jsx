import { useState, useEffect } from "react";
import './App.css';
import Dashboard from "./pages/Dashboard";
import InputPage from "./pages/InputPage";
import PrivacyPage from "./pages/PrivacyPage";
import Simulation from "./pages/Simulation";
import Alerts from "./pages/Alerts";
import FusionResults from "./pages/FusionResults";
import BehavioralPage from "./pages/BehavioralPage";
import VoicePage from "./pages/VoicePage";
import NLPPage from "./pages/NLPPage";
import EnginesPanel from "./components/EnginesPanel";

function App() {
  const [page, setPage] = useState("simulation");
  const [analysisResult, setAnalysisResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [fused, setFused] = useState(null);

  // Load persisted state on startup
  useEffect(() => {
    try {
      const h = localStorage.getItem("cd_history");
      const f = localStorage.getItem("cd_fused");
      if (h) setHistory(JSON.parse(h));
      if (f) setFused(JSON.parse(f));
    } catch (e) {}
  }, []);

  // Persist history
  useEffect(() => {
    try { localStorage.setItem("cd_history", JSON.stringify(history)); } catch (e) {}
  }, [history]);

  // Persist fused result
  useEffect(() => {
    try { localStorage.setItem("cd_fused", JSON.stringify(fused)); } catch (e) {}
  }, [fused]);

  const handleNewResult = (result) => {
    if (!result) return;
    setAnalysisResult(result);
    setHistory((prev) => [
      ...prev,
      {
        day: `Entry ${prev.length + 1}`,
        csi_score: result.csi_score ?? result.stability_score ?? 0,
        score: result.csi_score ?? result.stability_score ?? 0,
        breakdown: result.breakdown || {}
      }
    ]);
  };

  const handleFusionResult = (fusion) => {
    if (!fusion) return;
    setFused(fusion);
    handleNewResult(fusion);
  };

  // Auto-navigate to dashboard when a new result arrives
  useEffect(() => {
    if (analysisResult) setPage("dashboard");
  }, [analysisResult]);

  const SIDEBAR_WIDTH = 240;
  const styles = {
    root: {
      minHeight: "100vh",
      display: "flex",
      background: "#021726",
      color: "#eafaf5",
      fontFamily: "Inter, system-ui, -apple-system, 'Segoe UI', Roboto, Arial"
    },
    sidebar: {
      width: SIDEBAR_WIDTH,
      padding: 20,
      borderRight: "1px solid rgba(255,255,255,0.04)",
      boxSizing: "border-box",
      display: "flex",
      flexDirection: "column",
      gap: 4,
      background: "rgba(0,0,0,0.15)",
      flexShrink: 0
    },
    brand: { fontSize: 16, fontWeight: 800, color: "#34d399", marginBottom: 12 },
    navButton: {
      background: "transparent",
      border: "none",
      color: "#dffbf2",
      padding: "10px 12px",
      borderRadius: 8,
      textAlign: "left",
      cursor: "pointer",
      fontWeight: 600,
      fontSize: 14,
      width: "100%"
    },
    navButtonActive: {
      background: "rgba(52,211,153,0.08)",
      color: "#34d399",
      boxShadow: "inset 3px 0 0 #34d399"
    },
    contentWrap: { flex: 1, minWidth: 0, display: "flex", flexDirection: "column" },
    header: {
      padding: "12px 20px",
      borderBottom: "1px solid rgba(255,255,255,0.04)",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      background: "rgba(0,0,0,0.08)"
    },
    headerTitle: { fontWeight: 800, fontSize: 15 },
    status: { fontSize: 13, color: "rgba(255,255,255,0.5)" },
    main: { padding: 18, overflow: "auto", flex: 1 }
  };

  const navBtn = (key) => ({
    ...styles.navButton,
    ...(page === key ? styles.navButtonActive : {})
  });

  const pageTitles = {
    dashboard: "Dashboard",
    behavior: "Behavioral Intelligence",
    voice: "Voice Intelligence",
    nlp: "NLP Intelligence",
    simulation: "User Simulation",
    alerts: "Alerts & Warnings",
    fusion: "Fusion Results",
    privacy: "Privacy & Ethics"
  };

  const renderMain = () => {
    switch (page) {
      case "dashboard":
        return <Dashboard data={analysisResult} history={history} />;
      case "behavior":
        return (
          <div>
            <BehavioralPage />
            <div style={{ marginTop: 12 }}>
              <EnginesPanel
                onPartResult={handleNewResult}
                onFusion={handleFusionResult}
                onNavigate={setPage}
              />
            </div>
          </div>
        );
      case "voice":
        return <VoicePage />;
      case "nlp":
        return <NLPPage />;
      case "simulation":
        return <Simulation onResult={handleNewResult} />;
      case "alerts":
        return <Alerts />;
      case "fusion":
        return <FusionResults result={fused} />;
      case "privacy":
        return <PrivacyPage />;
      default:
        return <Dashboard data={analysisResult} history={history} />;
    }
  };

  return (
    <div style={styles.root}>
      <aside style={styles.sidebar}>
        <div style={styles.brand}>⬡ NeuroLens</div>

        <div style={{ fontSize: 10, color: "rgba(255,255,255,0.3)", textTransform: "uppercase", letterSpacing: 1, marginBottom: 4, paddingLeft: 12 }}>
          Overview
        </div>
        <button style={navBtn("dashboard")} onClick={() => setPage("dashboard")}>Dashboard</button>
        <button style={navBtn("simulation")} onClick={() => setPage("simulation")}>User Simulation</button>

        <div style={{ fontSize: 10, color: "rgba(255,255,255,0.3)", textTransform: "uppercase", letterSpacing: 1, margin: "10px 0 4px", paddingLeft: 12 }}>
          Engines
        </div>
        <button style={navBtn("behavior")} onClick={() => setPage("behavior")}>Behavioral</button>
        <button style={navBtn("voice")} onClick={() => setPage("voice")}>Voice</button>
        <button style={navBtn("nlp")} onClick={() => setPage("nlp")}>NLP</button>
        <button style={navBtn("fusion")} onClick={() => setPage("fusion")}>Fusion Results</button>

        <div style={{ fontSize: 10, color: "rgba(255,255,255,0.3)", textTransform: "uppercase", letterSpacing: 1, margin: "10px 0 4px", paddingLeft: 12 }}>
          System
        </div>
        <button style={navBtn("alerts")} onClick={() => setPage("alerts")}>Alerts</button>
        <button style={navBtn("privacy")} onClick={() => setPage("privacy")}>Privacy & Ethics</button>

        <div style={{ flex: 1 }} />
        <div style={{ fontSize: 11, color: "rgba(255,255,255,0.35)", paddingLeft: 4 }}>
          ● Offline · Local processing
        </div>
      </aside>

      <div style={styles.contentWrap}>
        <header style={styles.header}>
          <div style={styles.headerTitle}>{pageTitles[page] || "NeuroLens"}</div>
          <div style={styles.status}>Research use only · Not medical advice</div>
        </header>
        <main style={styles.main}>
          {renderMain()}
        </main>
      </div>
    </div>
  );
}

export default App;
