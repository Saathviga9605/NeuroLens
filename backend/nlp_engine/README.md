# NLP Microservice - Temporal Sentiment Drift Detection

Production-ready NLP microservice for analyzing sentiment, drift, volatility, and linguistic stability using DistilBERT.

## Features

- **Sentiment Analysis**: DistilBERT-based sentiment scoring normalized to [-1, +1]
- **Drift Detection**: Calculate sentiment drift between time periods
- **Volatility Measurement**: Emotional volatility via standard deviation
- **Linguistic Stability**: Lexical diversity and sentence variance analysis
- **Risk Flagging**: Automatic risk detection based on drift and volatility thresholds

## Architecture

```
nlp_engine/
├── model/              # Sentiment analysis models
├── drift/              # Drift and volatility calculators
├── features/           # Linguistic feature extraction
├── api/                # FastAPI endpoints
├── schemas/            # Pydantic request/response models
└── utils/              # Utility functions
```

## Installation

### Prerequisites

- Python 3.9+
- pip or conda

### Install Dependencies

```bash
cd /app/backend
pip install -r requirements.txt
```

### Required Packages

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `transformers` - HuggingFace models
- `torch` - PyTorch for model inference
- `pydantic` - Data validation
- `scipy` - Statistical calculations

## Running the Service

### Development Mode

```bash
cd /app/backend
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

### Production Mode

```bash
uvicorn server:app --host 0.0.0.0 --port 8001 --workers 4
```

The service will be available at `http://localhost:8001`

## API Documentation

### Endpoints

#### POST /api/nlp/analyze

Analyze text for sentiment and temporal patterns.

**Request Body:**

```json
{
  "text": "I am feeling much better today after a good night's sleep.",
  "history_scores": [0.2, 0.1, -0.05, 0.0],
  "previous_scores": [0.4, 0.35, 0.3, 0.25]
}
```

**Response:**

```json
{
  "sentiment_score": 0.62,
  "sentiment_drift": -0.18,
  "emotional_volatility": 0.21,
  "linguistic_stability": 0.74,
  "risk_flag": true
}
```

**Fields:**

- `sentiment_score`: Current sentiment [-1 to +1]
- `sentiment_drift`: Change from previous period (can be negative)
- `emotional_volatility`: Standard deviation of recent scores
- `linguistic_stability`: Text consistency score [0 to 1]
- `risk_flag`: True if drift < -0.15 OR volatility > 0.5

#### GET /api/nlp/health

Health check endpoint.

**Response:**

```json
{
  "status": "healthy",
  "model_loaded": true
}
```

## Example Usage

### cURL

```bash
curl -X POST "http://localhost:8001/api/nlp/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Current text sample",
    "history_scores": [0.2, 0.1, -0.05, 0.0],
    "previous_scores": [0.4, 0.35, 0.3, 0.25]
  }'
```

### Python

```python
import requests

url = "http://localhost:8001/api/nlp/analyze"
payload = {
    "text": "I feel great today!",
    "history_scores": [0.2, 0.1, -0.05, 0.0],
    "previous_scores": [0.4, 0.35, 0.3, 0.25]
}

response = requests.post(url, json=payload)
result = response.json()
print(result)
```

### JavaScript

```javascript
fetch('http://localhost:8001/api/nlp/analyze', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: 'I feel great today!',
    history_scores: [0.2, 0.1, -0.05, 0.0],
    previous_scores: [0.4, 0.35, 0.3, 0.25]
  })
})
.then(res => res.json())
.then(data => console.log(data));
```

## Interactive API Documentation

Visit `http://localhost:8001/docs` for interactive Swagger documentation.

## Configuration

### Model Settings

- Model: `distilbert-base-uncased-finetuned-sst-2-english`
- Device: CPU (set `device=0` in model code for GPU)
- Max tokens: 512

### Risk Thresholds

- Drift threshold: -0.15
- Volatility threshold: 0.5

Modify these in `/api/app.py` `determine_risk_flag()` function.

## Error Handling

- **400 Bad Request**: Invalid input (empty text, out-of-range scores)
- **500 Internal Server Error**: Model loading or inference failures

Detailed errors are logged internally; minimal messages returned to clients.

## Logging

Logs are configured with:
- Level: INFO
- Format: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`

View logs in your terminal or configure file logging as needed.

## Testing

Run tests using pytest:

```bash
pytest tests/
```

## Docker Support

### Build Image

```bash
docker build -t nlp-microservice .
```

### Run Container

```bash
docker run -p 8001:8001 nlp-microservice
```

## Production Considerations

- **Model Caching**: Model loads on startup for fast inference
- **Concurrency**: Use multiple workers for production
- **GPU**: Enable GPU by changing `device=-1` to `device=0` in model code
- **Rate Limiting**: Add rate limiting middleware for production
- **Authentication**: Add API key authentication if needed
- **Monitoring**: Integrate with monitoring tools (Prometheus, Grafana)

## License

MIT License

## Support

For issues and questions, please open an issue on the project repository.
