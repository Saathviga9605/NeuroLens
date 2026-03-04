import React, { useState, useRef, useEffect } from "react";
import { runAssessment } from "../services/api";
import GaugeCard from "../components/GaugeCard";

const referenceText = `
Cognitive stability reflects the ability of an individual to maintain consistent attention, emotional regulation,
and behavioral control under varying internal and external conditions. It involves coordinated neural processes
that regulate executive functioning, impulse modulation, working memory stability, and sustained cognitive focus.
In daily life, cognitive stability supports productivity, learning efficiency, emotional resilience,
and adaptive decision-making. Variations in sleep patterns, stress levels, psychomotor speed,
and linguistic coherence may indicate temporary fluctuations in stability.
Continuous micro-assessments using behavioral, voice, and linguistic signals
allow early detection of deviations from baseline cognitive patterns.
`;

const Simulation = ({ onResult }) => {
  const [sleepStart, setSleepStart] = useState("");
  const [sleepEnd, setSleepEnd] = useState("");
  const [sleepHours, setSleepHours] = useState(null);

  const [typingText, setTypingText] = useState("");
  const [typingRunning, setTypingRunning] = useState(false);
  const [timeLeft, setTimeLeft] = useState(60);
  const [typingWpm, setTypingWpm] = useState(null);
  const [keyTimestamps, setKeyTimestamps] = useState([]);

  const typingTimerRef = useRef(null);

  const [typingMetrics, setTypingMetrics] = useState(null);
  const [status, setStatus] = useState("");
  const [error, setError] = useState("");
  const [lastResult, setLastResult] = useState(null);

  // ---------------- Sleep ----------------
  const parseSleepHours = (start, end) => {
    if (!start || !end) return null;

    const [sh, sm] = start.split(":").map(Number);
    const [eh, em] = end.split(":").map(Number);

    const s = sh * 60 + sm;
    const e = eh * 60 + em;

    let minutes = e - s;
    if (minutes <= 0) minutes += 24 * 60;

    return +(minutes / 60).toFixed(2);
  };

  const submitSleep = () => {
    const hrs = parseSleepHours(sleepStart, sleepEnd);
    if (hrs == null) {
      setError("Please provide both sleep and wake times");
      return;
    }

    setSleepHours(hrs);
    setError("");
    setStatus(`Recorded ${hrs} hours sleep`);
  };

  // ---------------- Typing ----------------
  const startTypingTest = () => {
    setTypingText("");
    setTypingMetrics(null);
    setKeyTimestamps([]);
    setTimeLeft(60);
    setTypingRunning(true);

    typingTimerRef.current = setInterval(() => {
      setTimeLeft((t) => t - 1);
    }, 1000);
  };

  const finishTypingTest = () => {
    // --- Helper to normalize words ---
    const clean = (word) =>
      word.toLowerCase().replace(/[^a-z0-9]/g, "");

    // --- Clean and split words ---
    const typedWords = typingText
      .trim()
      .split(/\s+/)
      .map(clean)
      .filter(Boolean);

    const refWords = referenceText
      .split(/\s+/)
      .map(clean)
      .filter(Boolean);

    // --- Accuracy Calculation ---
    let correct = 0;

    for (let i = 0; i < typedWords.length; i++) {
      if (typedWords[i] === refWords[i]) {
        correct++;
      }
    }

    // IMPORTANT:
    // Compare only against what user typed,
    // not entire reference length.
    const totalTyped = typedWords.length || 1;
    const errorRate = 1 - correct / totalTyped;

    // --- WPM ---
    const wpm = typedWords.length;

    // --- Rhythm Calculation ---
    let intervals = [];
    for (let i = 1; i < keyTimestamps.length; i++) {
      intervals.push(keyTimestamps[i] - keyTimestamps[i - 1]);
    }

    let rhythmStd = 0;

    if (intervals.length > 1) {
      const mean =
        intervals.reduce((a, b) => a + b, 0) / intervals.length;

      const variance =
        intervals.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) /
        intervals.length;

      rhythmStd = Math.sqrt(variance);
    }

    setTypingWpm(wpm);

    setTypingMetrics({
      wpm,
      error_rate: +errorRate.toFixed(2),
      rhythm_std: +rhythmStd.toFixed(2),
    });
  };
  useEffect(() => {
    if (timeLeft <= 0 && typingRunning) {
      clearInterval(typingTimerRef.current);
      setTypingRunning(false);
      finishTypingTest();
    }
  }, [timeLeft]);

  // ---------------- Backend Call ----------------
  const runFullAssessment = async () => {
    if (sleepHours == null) {
      setError("Please save sleep data first");
      return;
    }

    if (!typingMetrics) {
      setError("Please complete typing test first");
      return;
    }

    try {
      setStatus("Running assessment...");
      setError("");

      const response = await runAssessment({
        sleep_hours: sleepHours,
        wpm: typingMetrics.wpm,
        error_rate: typingMetrics.error_rate,
        rhythm_std: typingMetrics.rhythm_std
      });

      setLastResult(response);
      setStatus("Assessment complete");

      if (onResult) onResult(response);

    } catch (err) {
      console.error(err);
      setError("Backend connection failed");
    }
  };

  // ---------------- UI ----------------
  return (
    <div style={{ maxWidth: 920, margin: "0 auto", padding: 24 }}>
      <h2>User Simulation — Cognitive Assessment</h2>

      <section>
        <h4>Sleep Times</h4>
        <input type="time" value={sleepStart} onChange={(e) => setSleepStart(e.target.value)} />
        <input type="time" value={sleepEnd} onChange={(e) => setSleepEnd(e.target.value)} />
        <button onClick={submitSleep}>Save Sleep</button>
      </section>

      <section style={{ marginTop: 20 }}>
        <h4>Typing Speed Test (60s)</h4>

        <div style={{ marginBottom: 10, background: "#122", padding: 10, borderRadius: 6 }}>
          {referenceText}
        </div>

        <div>Time left: {timeLeft}s</div>

        <textarea
          value={typingText}
          onChange={(e) => {
            if (typingRunning) {
              setKeyTimestamps((prev) => [...prev, Date.now()]);
            }
            setTypingText(e.target.value);
          }}
          disabled={!typingRunning}
          style={{ width: "100%", height: 120 }}
        />

        {!typingRunning && <button onClick={startTypingTest}>Start 60s Test</button>}
        {typingRunning && (
          <button
            onClick={() => {
              clearInterval(typingTimerRef.current);
              setTypingRunning(false);
              finishTypingTest();
            }}
          >
            Stop
          </button>
        )}

        {typingMetrics && (
          <div style={{ marginTop: 10 }}>
            <div>WPM: {typingMetrics.wpm}</div>
            <div>Error Rate: {typingMetrics.error_rate}</div>
            <div>Rhythm Std: {typingMetrics.rhythm_std}</div>
          </div>
        )}
      </section>

      <section style={{ marginTop: 20 }}>
        <button onClick={runFullAssessment}>
          Run Full Cognitive Assessment
        </button>
      </section>

      {status && <div style={{ marginTop: 10 }}>{status}</div>}
      {error && <div style={{ color: "red" }}>{error}</div>}

      {lastResult && (
        <section style={{ marginTop: 20 }}>
          <GaugeCard
            title="Cognitive Stability Index"
            value={lastResult.csi_score || 0}
            size={140}
          />
        </section>
      )}
    </div>
  );
};

export default Simulation;
