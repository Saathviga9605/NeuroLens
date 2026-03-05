# NeuroLens Integration Guide

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Installation

1. **Install Python dependencies for all services:**
```bash
# Backend dependencies
cd backend
pip install -r requirements.txt
cd ..

# NLP service dependencies (uses same backend requirements)

# Voice service dependencies
cd neurolens-voice
pip install -r requirements.txt
cd ..

# Member4 service dependencies
cd member4_service
pip install -r requirements.txt
cd ..
```

2. **Install Frontend dependencies:**
```bash
npm install
```

### Running the System

#### Option 1: Automated Startup (Recommended)

**Windows (PowerShell):**
```powershell
.\start_all_services.ps1
```

**Linux/Mac:**
```bash
chmod +x start_all_services.sh
./start_all_services.sh
```

This will start all 5 services in separate terminal windows/processes.

#### Option 2: Manual Startup

Start each service in a separate terminal:

**Terminal 1 - Backend API Gateway (Port 8000):**
```bash
cd backend
python main.py
```

**Terminal 2 - NLP Service (Port 8001):**
```bash
cd backend/nlp_engine
python main.py
```

**Terminal 3 - Voice Service (Port 8002):**
```bash
cd neurolens-voice
python app.py
```

**Terminal 4 - Member4 Service (Port 8003):**
```bash
cd member4_service
python main.py
```

**Terminal 5 - Frontend (Port 5173):**
```bash
npm run dev
```

### Accessing the System

- **Frontend**: http://localhost:5173
- **API Gateway**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

### Service Architecture

```
┌─────────────────────────────────────────────┐
│   Frontend (React + Vite)                   │
│   Port: 5173                                │
└────────────────┬────────────────────────────┘
                 │ HTTP /api/*
                 ▼
┌─────────────────────────────────────────────┐
│   Backend API Gateway (FastAPI)             │
│   Port: 8000                                │
│   - Proxies to microservices                │
│   - SQLite database                         │
│   - /api/behavior, /api/assessment          │
└───┬─────────┬─────────┬─────────────────────┘
    │         │         │
    │         │         └──────────────┐
    │         │                        │
    ▼         ▼                        ▼
┌────────┐ ┌──────────┐  ┌─────────────────────┐
│  NLP   │ │  Voice   │  │    Member4          │
│ Service│ │ Service  │  │ Behavioral+Fusion   │
│ :8001  │ │  :8002   │  │      :8003          │
└────────┘ └──────────┘  └─────────────────────┘
```

### API Endpoints

#### Backend API Gateway (http://localhost:8000)

**Assessment & Behavior:**
- `POST /api/assessment/run` - Run cognitive assessment
- `GET /api/assessment/history` - Get assessment history
- `POST /api/behavior/analyze` - Analyze behavioral patterns

**Proxied Microservices:**
- `POST /api/nlp/analyze` - NLP sentiment analysis (→ NLP service)
- `POST /api/voice/analyze` - Voice stress analysis (→ Voice service)
- `POST /api/fusion/score` - Multimodal fusion (→ Member4 service)

**System:**
- `GET /api/health` - Check all services health
- `GET /` - Service information
- `GET /docs` - Interactive API documentation

#### NLP Service (http://localhost:8001)
- `POST /api/nlp/analyze` - Sentiment drift detection
- `GET /api/nlp/health` - Health check
- `GET /health` - Quick health check

#### Voice Service (http://localhost:8002)
- `POST /api/voice/analyze` - Voice stress analysis
- `GET /api/health` - Health check

#### Member4 Service (http://localhost:8003)
- `POST /api/v1/behavior/analyze` - Behavioral anomaly detection
- `POST /api/v1/fusion/score` - Multimodal risk fusion
- `GET /api/v1/health` - Health check

### Testing the Integration

#### 1. Check All Services Are Running
```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "gateway": "healthy",
  "services": {
    "nlp": "healthy",
    "voice": "healthy",
    "member4": "healthy"
  }
}
```

#### 2. Test NLP Analysis
```bash
curl -X POST http://localhost:8000/api/nlp/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "I am feeling great today!", "history_scores": [0.5], "previous_scores": [0.3]}'
```

#### 3. Test Voice Analysis
```bash
# Requires audio file
curl -X POST http://localhost:8000/api/voice/analyze \
  -F "file=@path/to/audio.wav" \
  -F "user_id=test_user"
```

#### 4. Open Frontend
Navigate to http://localhost:5173 in your browser.

### Troubleshooting

#### Services Won't Start

**Port already in use:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

**Python dependencies missing:**
```bash
pip install -r backend/requirements.txt
pip install -r neurolens-voice/requirements.txt
pip install -r member4_service/requirements.txt
```

**Node/npm issues:**
```bash
rm -rf node_modules package-lock.json
npm install
```

#### Service Can't Connect to Another Service

1. Check if the target service is running
2. Verify ports in configuration files
3. Check firewall settings
4. Review service logs

#### Frontend Shows Connection Errors

1. Ensure backend API gateway is running on port 8000
2. Check Vite proxy configuration in `vite.config.js`
3. Clear browser cache
4. Check browser console for specific errors

### Development Notes

- **Database**: Backend uses SQLite by default (`cognitive_data.db`)
- **CORS**: All services allow `*` origins (restrict in production)
- **Logs**: Check terminal output for each service
- **Hot Reload**: All services support hot reload during development

### Project Structure

```
NeuroLens/
├── backend/                 # Main API Gateway
│   ├── main.py             # Gateway with proxy routes
│   ├── api/                # Assessment & behavior routes
│   ├── database/           # SQLite database
│   ├── engines/            # Fusion & behavior engines
│   └── nlp_engine/         # NLP microservice code
│       └── main.py         # NLP service launcher
│
├── member4_service/        # Behavioral + Fusion microservice
│   ├── main.py             # Service launcher
│   ├── api/routes.py       # API endpoints
│   ├── core/               # Fusion logic
│   └── models/             # ML models
│
├── neurolens-voice/        # Voice analysis microservice
│   ├── app.py              # Service launcher
│   ├── routes/             # API endpoints
│   ├── models/             # Voice scoring
│   └── utils/              # Feature extraction
│
├── src/                    # React frontend
│   ├── components/         # UI components
│   ├── pages/              # Page components
│   └── services/           # API client
│
├── start_all_services.ps1  # Windows startup script
├── start_all_services.sh   # Linux/Mac startup script
└── stop_all_services.sh    # Linux/Mac stop script
```

### Next Steps

1. Configure production environment variables
2. Set up proper logging system
3. Add authentication/authorization
4. Configure production database (PostgreSQL/MongoDB)
5. Set up CI/CD pipeline
6. Add comprehensive tests
7. Configure reverse proxy (nginx)
8. Set up monitoring and alerting

### Support

For issues or questions:
1. Check service logs
2. Review API documentation at http://localhost:8000/docs
3. Verify service health at http://localhost:8000/api/health
4. Check INTEGRATION_ANALYSIS.md for detailed architecture info
