# Member 4 Service: Behavioral Intelligence & Multimodal Fusion Engine

## Overview

This microservice is part of the **NeuroLens** distributed AI system, responsible for:

1. **Behavioral Anomaly Detection** - Detects deviations from personal behavioral baselines using autoencoder-based deep learning
2. **Multimodal Risk Fusion** - Combines outputs from multiple AI engines (sentiment, voice, behavioral) into a unified risk assessment

## Architecture

### Components

```
member4_service/
├── models/
│   ├── autoencoder.py      # PyTorch-based autoencoder for pattern learning
│   └── anomaly.py          # Behavioral anomaly detection logic
├── core/
│   ├── feature_processing.py  # Input validation and feature engineering
│   └── fusion_logic.py        # Multimodal risk fusion algorithms
├── api/
│   └── routes.py           # FastAPI REST endpoints
└── main.py                 # Application entry point
```

## Technology Stack

- **Framework**: FastAPI
- **ML Libraries**: PyTorch, scikit-learn, numpy
- **Language**: Python 3.9+
- **Model Architecture**: Autoencoder (9 → 6 → 3 → 6 → 9)
- **Deployment**: Microservice (REST API)

## Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Setup

```bash
# Navigate to service directory
cd member4_service

# Install dependencies
pip install -r requirements.txt

# Run the service
python main.py
```

The service will start on `http://0.0.0.0:8004`

## API Endpoints

### 1. Behavioral Analysis

**POST** `/api/v1/behavior/analyze`

Analyzes behavioral patterns for anomalies.

**Input:**
```json
{
    "typing_speed": 3.5,
    "error_rate": 0.15,
    "backspace_frequency": 0.25,
    "pause_variability": 1.2,
    "sleep_duration": 6.5,
    "sleep_drift": -1.5,
    "app_usage_entropy": 2.3,
    "session_frequency": 12.0,
    "activity_regularity": 0.75
}
```

**Output:**
```json
{
    "behavioral_anomaly_score": 0.42,
    "typing_instability": 0.31,
    "sleep_irregularity": 0.28,
    "usage_entropy_change": 0.19,
    "risk_flag": false
}
```

### 2. Multimodal Fusion

**POST** `/api/v1/fusion/score`

Combines multiple modality scores into unified risk assessment.

**Input:**
```json
{
    "sentiment_drift": 0.65,
    "voice_stress": 0.45,
    "behavioral_anomaly": 0.72
}
```

**Output:**
```json
{
    "overall_risk_score": 0.61,
    "collapse_probability": "MODERATE",
    "dominant_factor": "behavioral_anomaly",
    "alert_level": "ELEVATED"
}
```

### 3. Additional Endpoints

- **GET** `/api/v1/health` - Health check
- **GET** `/api/v1/info` - Service information
- **POST** `/api/v1/behavior/train` - Train detector on baseline data
- **POST** `/api/v1/fusion/configure` - Configure fusion weights

## Behavioral Features

The system analyzes 9 behavioral dimensions:

| Feature | Range | Description |
|---------|-------|-------------|
| `typing_speed` | 0-10 | Keystrokes per second |
| `error_rate` | 0-1 | Proportion of typing errors |
| `backspace_frequency` | 0-1 | Backspace usage frequency |
| `pause_variability` | 0-10 | Variability in typing pauses (sec) |
| `sleep_duration` | 0-24 | Sleep duration (hours) |
| `sleep_drift` | -12 to 12 | Deviation from normal sleep schedule |
| `app_usage_entropy` | 0-5 | Shannon entropy of app usage |
| `session_frequency` | 0-100 | Sessions per day |
| `activity_regularity` | 0-1 | Daily activity regularity score |

## Anomaly Detection

### Method

- **Primary**: Autoencoder reconstruction error
- **Secondary**: Isolation Forest (backup/validation)

### Process

1. **Training**: Learn normal behavioral baseline using autoencoder
2. **Detection**: Compute reconstruction error for new data
3. **Scoring**: Convert to anomaly score [0, 1] using percentile ranking
4. **Interpretation**: Generate sub-scores for specific dimensions

### Sub-Scores

- **Typing Instability**: Combines typing speed, error rate, backspace usage
- **Sleep Irregularity**: Combines sleep duration and drift
- **Usage Entropy Change**: Measures app usage pattern changes

## Multimodal Fusion

### Fusion Strategies

1. **Weighted**: Linear combination with configurable weights
2. **Geometric**: Geometric mean (sensitive to agreement)
3. **Max Agreement**: Emphasizes maximum score with agreement factor

### Alert Levels

- **NORMAL**: Overall risk < 0.3
- **ELEVATED**: 0.3 ≤ risk < 0.5
- **HIGH**: 0.5 ≤ risk < 0.7
- **CRITICAL**: risk ≥ 0.7

### Collapse Probability

- **MINIMAL**: Very low risk
- **LOW**: Minor concerns
- **MODERATE**: Notable risk indicators
- **HIGH**: Significant risk
- **SEVERE**: Critical intervention recommended

## Configuration

### Fusion Weights

Default weights (normalized to sum = 1.0):

```python
sentiment_weight = 0.35
voice_weight = 0.30
behavioral_weight = 0.35
```

Update via API:

```bash
curl -X POST "http://localhost:8004/api/v1/fusion/configure" \
  -H "Content-Type: application/json" \
  -d '{
    "sentiment_weight": 0.4,
    "voice_weight": 0.3,
    "behavioral_weight": 0.3
  }'
```

### Anomaly Threshold

Default: `0.65`

Can be adjusted when initializing the detector:

```python
detector = BehavioralAnomalyDetector(
    autoencoder_model=autoencoder,
    anomaly_threshold=0.70  # More strict
)
```

## Example Usage

### Python Client

```python
import requests

# Behavioral analysis
response = requests.post(
    "http://localhost:8004/api/v1/behavior/analyze",
    json={
        "typing_speed": 2.8,
        "error_rate": 0.32,
        "backspace_frequency": 0.45,
        "pause_variability": 2.1,
        "sleep_duration": 4.5,
        "sleep_drift": -3.2,
        "app_usage_entropy": 3.8,
        "session_frequency": 8.0,
        "activity_regularity": 0.42
    }
)
print(response.json())

# Multimodal fusion
fusion_response = requests.post(
    "http://localhost:8004/api/v1/fusion/score",
    json={
        "sentiment_drift": 0.75,
        "voice_stress": 0.68,
        "behavioral_anomaly": 0.82
    }
)
print(fusion_response.json())
```

### cURL

```bash
# Health check
curl http://localhost:8004/api/v1/health

# Behavioral analysis
curl -X POST http://localhost:8004/api/v1/behavior/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "typing_speed": 3.5,
    "error_rate": 0.15,
    "backspace_frequency": 0.25,
    "pause_variability": 1.2,
    "sleep_duration": 6.5,
    "sleep_drift": -1.5,
    "app_usage_entropy": 2.3,
    "session_frequency": 12.0,
    "activity_regularity": 0.75
  }'
```

## Integration with NeuroLens

This service is designed to:

1. **Receive** behavioral data from data collection agents
2. **Process** features and detect anomalies
3. **Integrate** with other Member services (sentiment, voice)
4. **Provide** unified risk scores to the main system

### Communication Flow

```
Data Sources → Member 4 (Behavioral) ─┐
Member 1 (Sentiment) ─────────────────┤
Member 2/3 (Voice) ───────────────────┴→ Fusion Engine → Risk Score
```

## Model Training

### Initial Setup

The service includes synthetic baseline generation for demonstration:

```python
# Generates realistic baseline behavioral data
baseline_data = generate_synthetic_baseline_data(n_samples=200)
detector.fit_baseline(baseline_data, epochs=30)
```

### Production Training

Replace synthetic data with real user baselines:

```python
# Collect normal behavioral data over 2-4 weeks
user_baseline = collect_user_baseline_data(user_id)

# Train personalized detector
detector.fit_baseline(user_baseline, epochs=50, verbose=True)
```

## Performance Considerations

- **Latency**: < 50ms for behavioral analysis
- **Throughput**: ~1000 requests/second (single instance)
- **Memory**: ~200-300MB with autoencoder loaded
- **CPU**: Optimized for CPU inference (GPU optional)

## Security & Privacy

- No data persistence (stateless by default)
- Input validation via Pydantic models
- CORS configured (update for production)
- Recommendation: Add rate limiting, authentication in production

## Deployment

### Docker (Recommended)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8004
CMD ["python", "main.py"]
```

### Docker Compose (with other services)

```yaml
services:
  member4:
    build: ./member4_service
    ports:
      - "8004:8004"
    environment:
      - LOG_LEVEL=INFO
```

## Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/
```

## Documentation

- **Interactive API Docs**: http://localhost:8004/docs
- **OpenAPI Schema**: http://localhost:8004/openapi.json

## Troubleshooting

### Service won't start

```bash
# Check port availability
netstat -an | grep 8004

# Verify dependencies
pip install -r requirements.txt --upgrade
```

### High anomaly scores for normal data

- Retrain detector with more baseline samples
- Adjust `anomaly_threshold` parameter
- Check input feature ranges

### Fusion scores seem incorrect

- Verify all input scores are in [0, 1] range
- Check fusion weights configuration
- Review alert thresholds

## Contributing

This service is part of the NeuroLens project. Follow the team's contribution guidelines.

## License

[Specify License]

## Contact

NeuroLens Team - Member 4
Project: NeuroLens Distributed AI System

---

**Version**: 1.0.0  
**Last Updated**: February 2026
