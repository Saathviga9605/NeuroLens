// Offline mock API — simulates /api endpoints with realistic delays.
// Result shape matches what Dashboard.jsx expects:
// { csi_score, behavioral_score, drift_flag, risk_flag, risk_level, reasons }

const wait = (ms) => new Promise((res) => setTimeout(res, ms));

const toResult = (score, reasons = [], extras = {}) => ({
  stability_score: score,
  csi_score: score,
  behavioral_score: score,
  drift_flag: score < 60 ? 1 : 0,
  risk_flag: score < 50 ? 1 : 0,
  risk_level: score < 50 ? "High" : score < 70 ? "Moderate" : "Low",
  reasons,
  ...extras
});

const mockApi = {
  nlpAnalyze: async ({ text }) => {
    await wait(600);
    const pos = ["good", "happy", "great", "positive", "love", "excellent"];
    const neg = ["bad", "sad", "angry", "negative", "hate", "poor"];
    let score = 80;
    const t = (text || "").toLowerCase();
    pos.forEach((w) => { if (t.includes(w)) score += 3; });
    neg.forEach((w) => { if (t.includes(w)) score -= 4; });
    const reasons = [];
    if (score < 70) reasons.push("Negative sentiment detected");
    score = Math.max(10, Math.min(99, Math.round(score)));
    return toResult(score, reasons, { breakdown: { textSample: text } });
  },

  voiceAnalyze: async () => {
    await wait(900);
    const score = Math.max(
      10,
      Math.min(99, 70 + Math.round(Math.random() * 20 - 10))
    );
    return toResult(score);
  },

  behaviorAnalyze: async ({ csv }) => {
    await wait(700);
    const rows = (csv || "").split("\n").filter(Boolean);
    let avg = 0;
    if (rows.length) {
      const nums = rows
        .map((r) => Number((r.split(",")[1] || "").trim()))
        .filter((n) => !isNaN(n));
      if (nums.length) avg = nums.reduce((a, b) => a + b, 0) / nums.length;
    }
    let score = 75;
    if (avg > 8) score -= 10;
    if (avg < 4) score += 5;
    const reasons = [];
    if (avg > 8) reasons.push("High screen/time values in CSV");
    score = Math.max(10, Math.min(99, score));
    return toResult(score, reasons, { breakdown: { avg } });
  },

  fusionScore: async ({ parts = [] }) => {
    await wait(400);
    const vals = parts.map(
      (p) => p.csi_score ?? p.stability_score ?? 70
    );
    const avg = Math.max(
      10,
      Math.min(
        99,
        Math.round(vals.reduce((a, b) => a + b, 0) / Math.max(1, vals.length))
      )
    );
    const reasons = parts.flatMap((p) => p.reasons || []).slice(0, 5);
    return toResult(avg, reasons);
  }
};

export default mockApi;
