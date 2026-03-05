import React, { useState, useRef, useEffect } from "react";
import { runAssessment } from "../services/api";
import mockApi from "../services/mockApi";
import GaugeCard from "../components/GaugeCard";

// ─── Reference text for typing test ───────────────────────────────────────────
const referenceText = `Cognitive stability reflects the ability of an individual to maintain consistent attention, emotional regulation, and behavioral control under varying internal and external conditions. It involves coordinated neural processes that regulate executive functioning, impulse modulation, working memory stability, and sustained cognitive focus. In daily life, cognitive stability supports productivity, learning efficiency, emotional resilience, and adaptive decision-making. Variations in sleep patterns, stress levels, psychomotor speed, and linguistic coherence may indicate temporary fluctuations in stability. Continuous micro-assessments using behavioral, voice, and linguistic signals allow early detection of deviations from baseline cognitive patterns.`;

// ─── NLP prompts ──────────────────────────────────────────────────────────────
const NLP_PROMPTS = [
  "How was your day today? Describe what you did, how you felt, and anything that stood out.",
  "Walk me through your mood over the last 24 hours. What affected it most?",
  "Describe any challenges or highlights from today in as much detail as you like."
];

// ─── Styles ───────────────────────────────────────────────────────────────────
const s = {
  wrap: { maxWidth: 940, margin: "0 auto", padding: 24 },
  section: {
    marginTop: 20,
    background: "rgba(255,255,255,0.02)",
    border: "1px solid rgba(255,255,255,0.06)",
    borderRadius: 12,
    padding: 20
  },
  sectionTitle: {
    fontSize: 15,
    fontWeight: 800,
    color: "#34d399",
    marginBottom: 14,
    display: "flex",
    alignItems: "center",
    gap: 10
  },
  badge: (color) => ({
    fontSize: 11,
    fontWeight: 700,
    padding: "2px 8px",
    borderRadius: 20,
    background: `${color}22`,
    color: color,
    border: `1px solid ${color}44`
  }),
  input: {
    background: "rgba(255,255,255,0.05)",
    border: "1px solid rgba(255,255,255,0.1)",
    color: "#eafaf5",
    borderRadius: 6,
    padding: "8px 12px",
    marginRight: 8,
    fontSize: 14
  },
  btn: (color = "#34d399") => ({
    padding: "8px 16px",
    background: `${color}18`,
    border: `1px solid ${color}`,
    color: color,
    borderRadius: 6,
    fontWeight: 600,
    cursor: "pointer",
    fontSize: 14
  }),
  btnPrimary: {
    padding: "11px 26px",
    background: "#34d399",
    border: "none",
    color: "#021726",
    borderRadius: 8,
    fontWeight: 800,
    fontSize: 15,
    cursor: "pointer"
  },
  refText: {
    background: "rgba(255,255,255,0.03)",
    border: "1px solid rgba(255,255,255,0.06)",
    borderRadius: 8,
    padding: 14,
    fontSize: 13,
    lineHeight: 1.75,
    color: "rgba(255,255,255,0.65)",
    marginBottom: 12,
    maxHeight: 120,
    overflowY: "auto"
  },
  textarea: {
    width: "100%",
    background: "rgba(255,255,255,0.04)",
    border: "1px solid rgba(255,255,255,0.1)",
    color: "#eafaf5",
    borderRadius: 8,
    padding: 12,
    fontSize: 14,
    resize: "vertical",
    boxSizing: "border-box",
    lineHeight: 1.6,
    fontFamily: "inherit"
  },
  metricRow: {
    display: "flex",
    gap: 16,
    marginTop: 10,
    flexWrap: "wrap"
  },
  metric: {
    background: "rgba(52,211,153,0.08)",
    border: "1px solid rgba(52,211,153,0.2)",
    borderRadius: 8,
    padding: "6px 14px",
    fontSize: 13,
    color: "#34d399"
  },
  statusBar: (color) => ({
    marginTop: 10,
    fontSize: 13,
    color: color,
    display: "flex",
    alignItems: "center",
    gap: 6
  }),
  waveBar: (active, i) => ({
    width: 4,
    borderRadius: 4,
    background: active ? "#34d399" : "rgba(255,255,255,0.15)",
    height: active ? `${14 + Math.sin(i * 1.2) * 10}px` : "8px",
    transition: "height 0.15s ease",
    animation: active ? `wave ${0.4 + i * 0.07}s ease-in-out infinite alternate` : "none"
  })
};

// ─── Component ────────────────────────────────────────────────────────────────
const Simulation = ({ onResult }) => {

  // ── Sleep state ──
  const [sleepStart, setSleepStart]   = useState("");
  const [sleepEnd, setSleepEnd]       = useState("");
  const [sleepHours, setSleepHours]   = useState(null);

  // ── Typing state ──
  const [typingText, setTypingText]       = useState("");
  const [typingRunning, setTypingRunning] = useState(false);
  const [timeLeft, setTimeLeft]           = useState(60);
  const [keyTimestamps, setKeyTimestamps] = useState([]);
  const [typingMetrics, setTypingMetrics] = useState(null);
  const typingTimerRef = useRef(null);

  // ── Voice state ──
  const [voicePhase, setVoicePhase]         = useState("idle"); // idle | recording | done
  const [voiceTimeLeft, setVoiceTimeLeft]   = useState(60);
  const [voiceBlob, setVoiceBlob]           = useState(null);
  const [voiceTranscript, setVoiceTranscript] = useState("");
  const [voiceWave, setVoiceWave]           = useState(false);
  const mediaRecorderRef  = useRef(null);
  const audioChunksRef    = useRef([]);
  const voiceTimerRef     = useRef(null);
  const waveIntervalRef   = useRef(null);

  // ── NLP state ──
  const [nlpPrompt]         = useState(NLP_PROMPTS[Math.floor(Math.random() * NLP_PROMPTS.length)]);
  const [nlpText, setNlpText]           = useState("");
  const [nlpWordCount, setNlpWordCount] = useState(0);
  const [nlpDone, setNlpDone]           = useState(false);

  // ── Result state ──
  const [status, setStatus]     = useState("");
  const [error, setError]       = useState("");
  const [offline, setOffline]   = useState(false);
  const [lastResult, setLastResult] = useState(null);

  // ─────────────────────────────────────────────────────────────────────────
  // SLEEP
  // ─────────────────────────────────────────────────────────────────────────
  const submitSleep = () => {
    if (!sleepStart || !sleepEnd) { setError("Please provide both sleep and wake times."); return; }
    const [sh, sm] = sleepStart.split(":").map(Number);
    const [eh, em] = sleepEnd.split(":").map(Number);
    let minutes = (eh * 60 + em) - (sh * 60 + sm);
    if (minutes <= 0) minutes += 24 * 60;
    setSleepHours(+(minutes / 60).toFixed(2));
    setError("");
  };

  // ─────────────────────────────────────────────────────────────────────────
  // TYPING TEST
  // ─────────────────────────────────────────────────────────────────────────
  const startTypingTest = () => {
    setTypingText("");
    setTypingMetrics(null);
    setKeyTimestamps([]);
    setTimeLeft(60);
    setTypingRunning(true);
    typingTimerRef.current = setInterval(() => setTimeLeft((t) => t - 1), 1000);
  };

  const finishTypingTest = () => {
    const clean   = (w) => w.toLowerCase().replace(/[^a-z0-9]/g, "");
    const typed   = typingText.trim().split(/\s+/).map(clean).filter(Boolean);
    const ref     = referenceText.split(/\s+/).map(clean).filter(Boolean);
    let correct   = 0;
    typed.forEach((w, i) => { if (w === ref[i]) correct++; });
    const errorRate = +(1 - correct / Math.max(typed.length, 1)).toFixed(2);
    const wpm       = typed.length;
    const intervals = [];
    for (let i = 1; i < keyTimestamps.length; i++)
      intervals.push(keyTimestamps[i] - keyTimestamps[i - 1]);
    let rhythmStd = 0;
    if (intervals.length > 1) {
      const mean = intervals.reduce((a, b) => a + b, 0) / intervals.length;
      rhythmStd  = +Math.sqrt(intervals.reduce((s, v) => s + (v - mean) ** 2, 0) / intervals.length).toFixed(2);
    }
    setTypingMetrics({ wpm, error_rate: errorRate, rhythm_std: rhythmStd });
  };

  useEffect(() => {
    if (timeLeft <= 0 && typingRunning) {
      clearInterval(typingTimerRef.current);
      setTypingRunning(false);
      finishTypingTest();
    }
  }, [timeLeft]);

  // ─────────────────────────────────────────────────────────────────────────
  // VOICE RECORDING
  // ─────────────────────────────────────────────────────────────────────────
  const startVoiceRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      audioChunksRef.current = [];

      const recorder = new MediaRecorder(stream);
      mediaRecorderRef.current = recorder;

      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) audioChunksRef.current.push(e.data);
      };

      recorder.onstop = () => {
        const blob = new Blob(audioChunksRef.current, { type: "audio/webm" });
        setVoiceBlob(blob);
        setVoicePhase("done");
        stream.getTracks().forEach((t) => t.stop());
        setVoiceWave(false);
        clearInterval(waveIntervalRef.current);
        setVoiceTranscript("Recording saved. Audio analysis will run on assessment.");
      };

      recorder.start();
      setVoicePhase("recording");
      setVoiceTimeLeft(60);
      setVoiceWave(true);

      // Countdown
      voiceTimerRef.current = setInterval(() => {
        setVoiceTimeLeft((t) => {
          if (t <= 1) {
            clearInterval(voiceTimerRef.current);
            recorder.stop();
            return 0;
          }
          return t - 1;
        });
      }, 1000);

    } catch (err) {
      setError("Microphone access denied. Please allow microphone permissions and try again.");
    }
  };

  const stopVoiceEarly = () => {
    clearInterval(voiceTimerRef.current);
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== "inactive") {
      mediaRecorderRef.current.stop();
    }
  };

  const redoVoice = () => {
    setVoicePhase("idle");
    setVoiceBlob(null);
    setVoiceTranscript("");
    setVoiceTimeLeft(60);
  };

  // ─────────────────────────────────────────────────────────────────────────
  // NLP TEXT
  // ─────────────────────────────────────────────────────────────────────────
  const handleNlpChange = (e) => {
    const text = e.target.value;
    setNlpText(text);
    setNlpWordCount(text.trim() === "" ? 0 : text.trim().split(/\s+/).length);
    setNlpDone(false);
  };

  const submitNlp = () => {
    if (nlpWordCount < 10) { setError("Please write at least 10 words."); return; }
    setNlpDone(true);
    setError("");
  };

  // ─────────────────────────────────────────────────────────────────────────
  // FULL ASSESSMENT
  // ─────────────────────────────────────────────────────────────────────────
  const runFullAssessment = async () => {
    if (sleepHours == null) { setError("① Please save your sleep schedule first."); return; }
    if (!typingMetrics)     { setError("② Please complete the typing test first."); return; }

    setError("");
    setStatus("Running assessment…");

    try {
      let response;

      try {
        response = await runAssessment({
          sleep_hours: sleepHours,
          wpm:         typingMetrics.wpm,
          error_rate:  typingMetrics.error_rate,
          rhythm_std:  typingMetrics.rhythm_std
        });
        setOffline(false);
      } catch {
        console.warn("Backend unavailable — using mock API");
        setOffline(true);

        // Run mock NLP analysis if text was provided
        let nlpResult = null;
        if (nlpDone && nlpText.trim()) {
          nlpResult = await mockApi.nlpAnalyze({ text: nlpText });
        }

        // Run mock voice analysis if recording exists
        let voiceResult = null;
        if (voiceBlob) {
          voiceResult = await mockApi.voiceAnalyze({ audioBlob: voiceBlob });
        }

        // Fuse all available results
        const parts = [await mockApi.behaviorAnalyze({ csv: "" })];
        if (nlpResult)   parts.push(nlpResult);
        if (voiceResult) parts.push(voiceResult);
        response = await mockApi.fusionScore({ parts });
      }

      setLastResult(response);
      setStatus("Assessment complete ✓");
      if (onResult) onResult(response);

    } catch (err) {
      console.error(err);
      setError("Assessment failed. Please try again.");
      setStatus("");
    }
  };

  // ─────────────────────────────────────────────────────────────────────────
  // RENDER
  // ─────────────────────────────────────────────────────────────────────────
  return (
    <div style={s.wrap}>
      <h2 style={{ marginBottom: 4 }}>User Simulation</h2>
      <p style={{ color: "#9ecbd8", marginTop: 4, marginBottom: 0, fontSize: 14 }}>
        Complete all four steps for the most accurate cognitive assessment.
        Voice and text sections are optional but improve accuracy.
      </p>

      {/* ── STEP 1: SLEEP ─────────────────────────────────────────────────── */}
      <div style={s.section}>
        <div style={s.sectionTitle}>
          <span>① Sleep Schedule</span>
          {sleepHours !== null && <span style={s.badge("#34d399")}>✓ {sleepHours}h saved</span>}
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" }}>
          <span style={{ color: "#9ecbd8", fontSize: 13 }}>Slept at</span>
          <input type="time" value={sleepStart} onChange={(e) => setSleepStart(e.target.value)} style={s.input} />
          <span style={{ color: "#9ecbd8", fontSize: 13 }}>Woke at</span>
          <input type="time" value={sleepEnd} onChange={(e) => setSleepEnd(e.target.value)} style={s.input} />
          <button onClick={submitSleep} style={s.btn()}>Save Sleep</button>
        </div>
      </div>

      {/* ── STEP 2: TYPING TEST ───────────────────────────────────────────── */}
      <div style={s.section}>
        <div style={s.sectionTitle}>
          <span>② Typing Speed Test</span>
          {typingRunning && (
            <span style={s.badge(timeLeft < 10 ? "#ef4444" : "#f59e0b")}>
              {timeLeft}s remaining
            </span>
          )}
          {typingMetrics && !typingRunning && (
            <span style={s.badge("#34d399")}>✓ Complete</span>
          )}
        </div>

        <div style={s.refText}>{referenceText}</div>

        <textarea
          value={typingText}
          placeholder={typingRunning ? "Type the passage above as accurately as you can…" : "Start the test to begin typing"}
          onChange={(e) => {
            if (typingRunning) setKeyTimestamps((p) => [...p, Date.now()]);
            setTypingText(e.target.value);
          }}
          disabled={!typingRunning}
          style={{ ...s.textarea, height: 100, opacity: typingRunning ? 1 : 0.5 }}
        />

        <div style={{ marginTop: 10, display: "flex", gap: 10, alignItems: "center", flexWrap: "wrap" }}>
          {!typingRunning && !typingMetrics && (
            <button onClick={startTypingTest} style={s.btn()}>Start 60s Test</button>
          )}
          {typingRunning && (
            <button onClick={() => { clearInterval(typingTimerRef.current); setTypingRunning(false); finishTypingTest(); }} style={s.btn("#f59e0b")}>
              Stop Early
            </button>
          )}
          {typingMetrics && !typingRunning && (
            <button onClick={startTypingTest} style={s.btn("#9ecbd8")}>Redo Test</button>
          )}
        </div>

        {typingMetrics && (
          <div style={s.metricRow}>
            <div style={s.metric}>WPM: {typingMetrics.wpm}</div>
            <div style={s.metric}>Error Rate: {(typingMetrics.error_rate * 100).toFixed(0)}%</div>
            <div style={s.metric}>Rhythm Std: {typingMetrics.rhythm_std}ms</div>
          </div>
        )}
      </div>

      {/* ── STEP 3: VOICE RECORDING ───────────────────────────────────────── */}
      <div style={s.section}>
        <div style={s.sectionTitle}>
          <span>③ Voice Check</span>
          <span style={{ fontSize: 12, color: "rgba(255,255,255,0.4)", fontWeight: 400 }}></span>
          {voicePhase === "done" && <span style={s.badge("#34d399")}>✓ Recorded</span>}
        </div>

        <p style={{ color: "#9ecbd8", fontSize: 14, marginTop: 0, marginBottom: 16 }}>
          Press record and answer out loud for up to 60 seconds:
          <br />
          <strong style={{ color: "#eafaf5" }}>
            "Tell me about your day! What you did, how you felt, and how you're doing right now."
          </strong>
        </p>

        {/* Waveform visualiser */}
        {voicePhase === "recording" && (
          <div style={{ display: "flex", alignItems: "center", gap: 4, marginBottom: 14, height: 36 }}>
            {Array.from({ length: 20 }).map((_, i) => (
              <div key={i} style={{
                width: 4,
                borderRadius: 4,
                background: "#34d399",
                height: `${10 + Math.abs(Math.sin((Date.now() / 200 + i) * 0.8)) * 22}px`,
                opacity: 0.7 + (i % 3) * 0.1,
                transition: "height 0.1s ease",
                animation: `waveAnim ${0.3 + (i % 5) * 0.08}s ease-in-out infinite alternate`
              }} />
            ))}
            <span style={{ marginLeft: 10, color: "#ef4444", fontSize: 13, fontWeight: 700 }}>
              ● REC {voiceTimeLeft}s
            </span>
          </div>
        )}

        <div style={{ display: "flex", gap: 10, alignItems: "center", flexWrap: "wrap" }}>
          {voicePhase === "idle" && (
            <button onClick={startVoiceRecording} style={s.btn("#f472b6")}>
              🎙 Start Recording
            </button>
          )}
          {voicePhase === "recording" && (
            <button onClick={stopVoiceEarly} style={s.btn("#ef4444")}>
              ■ Stop Recording
            </button>
          )}
          {voicePhase === "done" && (
            <>
              <button onClick={redoVoice} style={s.btn("#9ecbd8")}>↺ Redo</button>
              {voiceBlob && (
                <audio
                  controls
                  src={URL.createObjectURL(voiceBlob)}
                  style={{ height: 32, filter: "invert(0.8) hue-rotate(100deg)" }}
                />
              )}
            </>
          )}
        </div>

        {voiceTranscript && (
          <div style={{ marginTop: 12, fontSize: 13, color: "#9ecbd8", fontStyle: "italic" }}>
            {voiceTranscript}
          </div>
        )}
      </div>

      {/* ── STEP 4: NLP TEXT ──────────────────────────────────────────────── */}
      <div style={s.section}>
        <div style={s.sectionTitle}>
          <span>④ Daily Check-in</span>
          <span style={{ fontSize: 12, color: "rgba(255,255,255,0.4)", fontWeight: 400 }}></span>
          {nlpDone && <span style={s.badge("#34d399")}>✓ Saved</span>}
        </div>

        <p style={{ color: "#9ecbd8", fontSize: 14, marginTop: 0, marginBottom: 12 }}>
          {nlpPrompt}
        </p>

        <textarea
          value={nlpText}
          onChange={handleNlpChange}
          placeholder="Write freely, minimum 10 words. Your response is processed locally."
          style={{ ...s.textarea, height: 130 }}
        />

        <div style={{ marginTop: 8, display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: 8 }}>
          <span style={{ fontSize: 12, color: nlpWordCount < 10 ? "#f59e0b" : "#34d399" }}>
            {nlpWordCount} word{nlpWordCount !== 1 ? "s" : ""}
            {nlpWordCount < 10 ? ` (${10 - nlpWordCount} more needed)` : " ✓"}
          </span>
          <button
            onClick={submitNlp}
            disabled={nlpWordCount < 10}
            style={{
              ...s.btn("#60a5fa"),
              opacity: nlpWordCount < 10 ? 0.4 : 1,
              cursor: nlpWordCount < 10 ? "not-allowed" : "pointer"
            }}
          >
            Save Response
          </button>
        </div>

        <div style={{ marginTop: 10, fontSize: 12, color: "rgba(255,255,255,0.3)" }}>
          All text is processed locally. Nothing is sent to external servers.
        </div>
      </div>

      {/* ── RUN ASSESSMENT ────────────────────────────────────────────────── */}
      <div style={{ marginTop: 24, display: "flex", alignItems: "center", gap: 16, flexWrap: "wrap" }}>
        <button onClick={runFullAssessment} style={s.btnPrimary}>
          Run Full Cognitive Assessment
        </button>
        <div style={{ fontSize: 13, color: "rgba(255,255,255,0.35)" }}>
          {[
            sleepHours !== null ? "✓ Sleep" : "✗ Sleep",
            typingMetrics      ? "✓ Typing" : "✗ Typing",
            voicePhase === "done" ? "✓ Voice" : "○ Voice",
            nlpDone            ? "✓ Check-in" : "○ Check-in"
          ].join("  ·  ")}
        </div>
      </div>

      {offline && (
        <div style={{ marginTop: 8, fontSize: 12, color: "#f59e0b" }}>
          ⚡ Offline mode — using mock results (backend not reachable)
        </div>
      )}

      {status && <div style={s.statusBar("#34d399")}><span>●</span>{status}</div>}
      {error  && <div style={s.statusBar("#ff8b8b")}><span>⚠</span>{error}</div>}

      {/* ── RESULT ────────────────────────────────────────────────────────── */}
      {lastResult && (
        <div style={{ ...s.section, marginTop: 24 }}>
          <div style={s.sectionTitle}>Assessment Result</div>
          <div style={{ display: "flex", gap: 32, alignItems: "center", flexWrap: "wrap" }}>
            <GaugeCard
              title="Cognitive Stability Index"
              value={lastResult.csi_score ?? lastResult.stability_score ?? 0}
              size={160}
            />
            <div>
              <div style={{ fontSize: 42, fontWeight: 800, color: "#34d399" }}>
                {lastResult.csi_score ?? lastResult.stability_score}%
              </div>
              <div style={{ color: "#9ecbd8", marginTop: 6, fontSize: 15 }}>
                Risk Level: <strong style={{
                  color: lastResult.risk_level === "High" ? "#ef4444"
                       : lastResult.risk_level === "Moderate" ? "#f59e0b"
                       : "#34d399"
                }}>
                  {lastResult.risk_level ?? (lastResult.risk_flag ? "Elevated" : "Normal")}
                </strong>
              </div>
              <div style={{ color: "#9ecbd8", marginTop: 4, fontSize: 14 }}>
                Drift: {lastResult.drift_flag === 1 ? "⚠ Detected" : "✓ Stable"}
              </div>
              {lastResult.behavioral_score !== undefined && (
                <div style={{ color: "#9ecbd8", marginTop: 4, fontSize: 14 }}>
                  Behavioral Score: {lastResult.behavioral_score}
                </div>
              )}
              {lastResult.reasons?.length > 0 && (
                <ul style={{ marginTop: 12, paddingLeft: 18, color: "#bcd7e6", fontSize: 13, lineHeight: 1.8 }}>
                  {lastResult.reasons.map((r, i) => <li key={i}>{r}</li>)}
                </ul>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Waveform keyframe animation */}
      <style>{`
        @keyframes waveAnim {
          from { transform: scaleY(1); }
          to   { transform: scaleY(1.8); }
        }
      `}</style>
    </div>
  );
};

export default Simulation;
