// Simple offline mock API to simulate /api endpoints with delays
const wait = (ms) => new Promise((res) => setTimeout(res, ms));

const mockApi = {
  nlpAnalyze: async ({ text }) => {
    await wait(600);
    // naive sentiment calculation: count positive/negative words
    const pos = ["good","happy","great","positive","love","excellent"];
    const neg = ["bad","sad","angry","negative","hate","poor"];
    let score = 80;
    const t = (text || "").toLowerCase();
    pos.forEach(w => { if (t.includes(w)) score += 3; });
    neg.forEach(w => { if (t.includes(w)) score -= 4; });

    const reasons = [];
    if (score < 70) reasons.push('Negative sentiment detected');

    return {
      stability_score: Math.max(10, Math.min(99, Math.round(score))),
      risk_level: score < 50 ? 'High' : score < 70 ? 'Moderate' : 'Low',
      breakdown: { textSample: text },
      reasons
    };
  },

  voiceAnalyze: async ({ audioBlob }) => {
    await wait(900);
    // placeholder: random slight influence
    const score = 70 + Math.round(Math.random() * 20 - 10);
    return { stability_score: score, risk_level: score < 50 ? 'High' : score < 70 ? 'Moderate' : 'Low', reasons: [] };
  },

  behaviorAnalyze: async ({ csv }) => {
    await wait(700);
    // parse simple numbers from CSV and derive a score
    const rows = (csv || '').split('\n').filter(Boolean);
    let avg = 0;
    if (rows.length) {
      const nums = rows.map(r => Number((r.split(',')[1]||'').trim())).filter(n => !isNaN(n));
      if (nums.length) avg = nums.reduce((a,b)=>a+b,0)/nums.length;
    }
    let score = 75;
    if (avg > 8) score -= 10;
    if (avg < 4) score += 5;
    const reasons = [];
    if (avg > 8) reasons.push('High screen/time values in CSV');
    return { stability_score: Math.max(10, score), risk_level: score < 50 ? 'High' : score < 70 ? 'Moderate' : 'Low', breakdown: { avg }, reasons };
  },

  fusionScore: async ({ parts = [] }) => {
    await wait(400);
    // simple average fusion
    const vals = parts.map(p => p.stability_score||70);
    const avg = Math.round(vals.reduce((a,b)=>a+b,0)/Math.max(1,vals.length));
    const reasons = parts.flatMap(p => p.reasons||[]).slice(0,5);
    return { stability_score: avg, risk_level: avg < 50 ? 'High' : avg < 70 ? 'Moderate' : 'Low', reasons };
  }
};

export default mockApi;
