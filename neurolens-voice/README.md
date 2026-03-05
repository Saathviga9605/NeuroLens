# 🎙 NeuroLens — Voice & Paralinguistic Analysis Engine
**Member 3 | Voice Stress · Cognitive Load · Emotional Tone**

---

## What This Does

Analyzes uploaded or recorded audio to detect early signs of mental health decline via paralinguistic features — *how* someone speaks, not *what* they say.

### Signals Detected
| Signal | Mental Health Marker |
|---|---|
| Flat pitch / low variation | Emotional numbing, depression |
| Slow speech rate | Cognitive fatigue, depression |
| High pause ratio | Word-finding difficulty, cognitive load |
| Low vocal energy | Low affect, burnout |
| Voice tremor (ZCR) | Anxiety, stress |
| MFCC instability | General cognitive/emotional instability |

---

## Project Structure
```
neurolens-voice/
├── app.py                        ← FastAPI entry point
├── requirements.txt
├── routes/
│   ├── analyze.py                ← All API endpoints
│   └── health.py                 ← Health check
├── utils/
│   └── feature_extractor.py      ← Librosa feature extraction
├── models/
│   ├── stress_scorer.py          ← Risk score computation
│   └── baseline_manager.py       ← Per-user baseline tracking
├── tests/
│   └── test_pipeline.py          ← Unit tests
└── data/
    └── baselines.json            ← Auto-created at runtime
```

---

## Setup

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the API server
python app.py
# → API running at http://localhost:8003
# → Docs at http://localhost:8003/docs
```

---

## API Endpoints

### `POST /api/voice/analyze`
Upload an audio file and get back voice stress scores.

**Request:**
```
Content-Type: multipart/form-data
file: <audio file (.wav / .mp3 / .ogg / .webm)>
user_id: "user123"          (optional — enables personalized scoring)
update_baseline: true        (default true)
```

**Response (Team Contract):**
```json
{
  "voice_stress": 0.44,
  "speech_variability": 0.29,
  "cognitive_load_estimate": 0.51,
  "risk_flag": false,

  "severity": "moderate",
  "sub_scores": {
    "pitch_flatness_risk": 0.12,
    "speech_rate_risk": 0.08,
    "energy_risk": 0.31,
    "pause_risk": 0.18,
    "vocal_stability_risk": 0.05
  },
  "baseline_drift": 0.0,
  "raw_features": {
    "speech_rate_sps": 4.2,
    "pitch_mean_hz": 172.5,
    "pitch_variation": 0.38,
    "energy_mean": 0.042,
    "pause_ratio": 0.28,
    "duration_seconds": 8.4
  },
  "personalized": false
}
```

---

### `POST /api/voice/baseline/update`
Submit a healthy-state audio sample to build personalized baseline.
Call 3+ times when user is known to be well.

```bash
curl -X POST "http://localhost:8003/api/voice/baseline/update?user_id=user123" \
     -F "file=@healthy_sample.wav"
```

---

### `GET /api/voice/baseline/status?user_id=user123`
Check how many baseline samples collected.

```json
{
  "samples_collected": 2,
  "samples_needed_for_baseline": 1,
  "baseline_ready": false
}
```

---

### `GET /api/voice/history?user_id=user123`
Retrieve historical voice data for trend graphs (used by Member 1 dashboard).

---

### `GET /api/health`
Service health check.

---

## Running Tests

```bash
pip install pytest soundfile
pytest tests/test_pipeline.py -v
```

---

## How to Integrate (Member 1 - Frontend)

```javascript
// Record audio from browser mic, then:
const formData = new FormData();
formData.append("file", audioBlob, "recording.wav");

const response = await fetch(
  "http://localhost:8003/api/voice/analyze?user_id=user123",
  { method: "POST", body: formData }
);
const scores = await response.json();
// Use scores.voice_stress, scores.cognitive_load_estimate, etc.
```

---

## Upgrade Path (After Hackathon)

| Current | Upgrade |
|---|---|
| Librosa rule-based scoring | Fine-tuned wav2vec2 on DAIC-WoZ depression dataset |
| File-based baseline storage | MongoDB (Member 2's backend) |
| Local inference | GPU-accelerated inference server |

---

## References
- Moore et al. (2007) — Vocal features in depression detection
- Cummins et al. (2015) — Review: depression and speech
- DAIC-WoZ Dataset — Distress Analysis Interview Corpus
- openSMILE feature set documentation
