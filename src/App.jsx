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

  const SIDEBAR_WIDTH = 280;
  const styles = {
    root: {
      minHeight: "100vh",
      display: "flex",
      background: "linear-gradient(135deg, #0a0e1a 0%, #0f172a 100%)",
      color: "#e0f2fe",
      fontFamily: "Inter, system-ui, -apple-system, 'Segoe UI', Roboto, Arial"
    },
    sidebar: {
      width: SIDEBAR_WIDTH,
      padding: "32px 20px",
      borderRight: "1px solid rgba(52, 211, 153, 0.1)",
      boxSizing: "border-box",
      display: "flex",
      flexDirection: "column",
      gap: 8,
      background: "linear-gradient(180deg, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.2) 100%)",
      backdropFilter: "blur(10px)",
      flexShrink: 0,
      boxShadow: "4px 0 24px rgba(0,0,0,0.3)"
    },
    brand: { 
      fontSize: 24, 
      fontWeight: 900, 
      background: "linear-gradient(135deg, #34d399 0%, #10b981 100%)",
      WebkitBackgroundClip: "text",
      WebkitTextFillColor: "transparent",
      backgroundClip: "text",
      marginBottom: 32,
      letterSpacing: "-0.02em",
      display: "flex",
      alignItems: "center",
      gap: 12
    },
    navButton: {
      background: "transparent",
      border: "none",
      color: "#94a3b8",
      padding: "14px 16px",
      borderRadius: 12,
      textAlign: "left",
      cursor: "pointer",
      fontWeight: 600,
      fontSize: 14,
      width: "100%",
      transition: "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
      display: "flex",
      alignItems: "center",
      gap: 12,
      position: "relative",
      overflow: "hidden"
    },
    navButtonActive: {
      background: "linear-gradient(135deg, rgba(52,211,153,0.15) 0%, rgba(52,211,153,0.08) 100%)",
      color: "#34d399",
      boxShadow: "0 4px 12px rgba(52, 211, 153, 0.2), inset 0 0 0 1px rgba(52, 211, 153, 0.3)",
      transform: "translateX(4px)"
    },
    contentWrap: { 
      flex: 1, 
      minWidth: 0, 
      display: "flex", 
      flexDirection: "column",
      overflow: "hidden"
    },
    header: {
      padding: "20px 32px",
      borderBottom: "1px solid rgba(52, 211, 153, 0.1)",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      background: "linear-gradient(135deg, rgba(0,0,0,0.2) 0%, rgba(0,0,0,0.1) 100%)",
      backdropFilter: "blur(10px)"
    },
    headerTitle: { 
      fontWeight: 800, 
      fontSize: 18,
      background: "linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%)",
      WebkitBackgroundClip: "text",
      WebkitTextFillColor: "transparent",
      backgroundClip: "text"
    },
    status: { 
      fontSize: 12, 
      color: "#34d399",
      background: "rgba(52, 211, 153, 0.1)",
      padding: "6px 12px",
      borderRadius: 20,
      fontWeight: 600,
      display: "flex",
      alignItems: "center",
      gap: 6
    },
    main: { 
      padding: 0, 
      overflow: "auto", 
      flex: 1,
      background: "transparent"
    }
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
        <div style={styles.brand}>
          <span style={{ 
            width: 32, 
            height: 32, 
            display: "inline-flex",
            alignItems: "center",
            justifyContent: "center",
            background: "linear-gradient(135deg, #34d399 0%, #10b981 100%)",
            borderRadius: 8,
            fontSize: 18,
            fontWeight: 900
          }}>N</span>
          <span>NeuroLens</span>
        </div>

        <div style={{ fontSize: 10, color: "#64748b", textTransform: "uppercase", letterSpacing: 1.5, marginBottom: 8, paddingLeft: 16, fontWeight: 700 }}>
          Overview
        </div>
        <button style={navBtn("dashboard")} onClick={() => setPage("dashboard")}>
          Dashboard
        </button>
        <button style={navBtn("simulation")} onClick={() => setPage("simulation")}>
          User Simulation
        </button>

        <div style={{ fontSize: 10, color: "#64748b", textTransform: "uppercase", letterSpacing: 1.5, margin: "20px 0 8px", paddingLeft: 16, fontWeight: 700 }}>
          AI Engines
        </div>
        <button style={navBtn("behavior")} onClick={() => setPage("behavior")}>
          Behavioral
        </button>
        <button style={navBtn("voice")} onClick={() => setPage("voice")}>
          Voice
        </button>
        <button style={navBtn("nlp")} onClick={() => setPage("nlp")}>
          NLP
        </button>
        <button style={navBtn("fusion")} onClick={() => setPage("fusion")}>
          Fusion Results
        </button>

        <div style={{ fontSize: 10, color: "#64748b", textTransform: "uppercase", letterSpacing: 1.5, margin: "20px 0 8px", paddingLeft: 16, fontWeight: 700 }}>
          System
        </div>
        <button style={navBtn("alerts")} onClick={() => setPage("alerts")}>
          Alerts
        </button>
        <button style={navBtn("privacy")} onClick={() => setPage("privacy")}>
          Privacy & Ethics
        </button>

        <div style={{ flex: 1 }} />
        <div style={{ 
          fontSize: 11, 
          color: "#34d399",
          background: "rgba(52, 211, 153, 0.1)",
          padding: "10px 14px",
          borderRadius: 10,
          display: "flex",
          alignItems: "center",
          gap: 8,
          border: "1px solid rgba(52, 211, 153, 0.2)"
        }}>
          <span style={{ 
            width: 6, 
            height: 6, 
            borderRadius: "50%", 
            background: "#34d399",
            boxShadow: "0 0 8px #34d399",
            animation: "pulse 2s ease-in-out infinite"
          }} />
          <span style={{ fontWeight: 600 }}>Offline · Secure Processing</span>
        </div>
      </aside>

      <div style={styles.contentWrap}>
        <header style={styles.header}>
          <div style={styles.headerTitle}>{pageTitles[page] || "NeuroLens"}</div>
          <div style={styles.status}>
            <span style={{ 
              width: 8, 
              height: 8, 
              borderRadius: "50%", 
              background: "#34d399",
              display: "inline-block",
              marginRight: 8
            }} />
            All Systems Operational
          </div>
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
