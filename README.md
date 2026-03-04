# Cognitive Dashboard (Offline)

This project is an offline-first React dashboard demonstrating multi-engine cognitive analysis (Behavioral, NLP, Voice, Fusion) using mock APIs.

Quick start

1. Install dependencies:

```bash
npm install
```

2. Run dev server:

```bash
npm run dev
```

Overview

- Offline UI demonstrating Behavioral / NLP / Voice / Fusion engines.
- Use the "Simulation" page to upload text, CSV, audio, or images.
- Engines can be run individually or use "Run All" to simulate a fusion score.

Mock APIs

- `src/services/mockApi.js` provides simple offline implementations for `nlpAnalyze`, `voiceAnalyze`, `behaviorAnalyze`, `fusionScore`.

Persistence

- History and fused results are stored in `localStorage` under keys `cd_history` and `cd_fused`.

Notes for judges

- This project is intentionally offline and privacy-first.
- Charts use `recharts` and are responsive.
