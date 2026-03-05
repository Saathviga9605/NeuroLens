# NeuroLens - AI for Early Mental Health Collapse Detection

> **Status**: ✅ Integration Complete - Ready for Testing

A comprehensive AI-powered system for early detection of mental health deterioration using multimodal analysis: behavioral patterns, voice stress, and natural language processing.

---

## 🚀 Quick Start

### Automated Startup (Recommended)
```powershell
# Windows
.\start_all_services.ps1

# Linux/Mac
./start_all_services.sh
```

### Access the System
- **Frontend**: http://localhost:5173
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

📖 **Full Instructions**: See [QUICKSTART.md](QUICKSTART.md)

---

## 📋 System Architecture

NeuroLens is built as a **microservices architecture**:

```
Frontend (React) → API Gateway (FastAPI) → AI Microservices
                                           ├─ NLP Service
                                           ├─ Voice Service
                                           └─ Behavioral+Fusion Service
```

### Components

| Component | Technology | Port | Purpose |
|-----------|-----------|------|---------|
| **Frontend** | React + Vite | 5173 | User interface & visualizations |
| **API Gateway** | FastAPI | 8000 | Central API & request routing |
| **NLP Service** | FastAPI + Transformers | 8001 | Sentiment drift analysis |
| **Voice Service** | FastAPI + Audio Analysis | 8002 | Voice stress detection |
| **Member4 Service** | FastAPI + ML | 8003 | Behavioral patterns & fusion |

---

## 🎯 Features

### 📊 **Multi-Engine Analysis**
- **Behavioral Engine**: Typing patterns, sleep quality, activity regularity
- **NLP Engine**: Sentiment drift, emotional volatility, linguistic stability
- **Voice Engine**: Stress levels, cognitive load, speech variability
- **Fusion Engine**: Multimodal risk scoring with adaptive weights

### 🔍 **Key Capabilities**
- Real-time cognitive assessment
- Temporal drift detection
- Personalized baseline tracking
- Risk flag identification
- Privacy-first design (local processing)

### 📈 **Visualizations**
- Interactive dashboards
- Trend analysis charts
- Anomaly detection plots
- Multi-dimensional risk scoring

---

## 📦 Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Install Dependencies

**Python Services:**
```bash
# Backend API Gateway
cd backend
pip install -r requirements.txt

# Voice Service
cd ../neurolens-voice
pip install -r requirements.txt

# Member4 Service
cd ../member4_service
pip install -r requirements.txt
```

**Frontend:**
```bash
# From project root
npm install
```

---

## 🏃 Running the System

### Option 1: Automated
Use the startup scripts (recommended):
- Windows: `.\start_all_services.ps1`
- Linux/Mac: `./start_all_services.sh`

### Option 2: Manual
Start each service in separate terminals:

```bash
# Terminal 1: API Gateway
cd backend
python main.py

# Terminal 2: NLP Service
cd backend/nlp_engine
python main.py

# Terminal 3: Voice Service
cd neurolens-voice
python app.py

# Terminal 4: Member4 Service
cd member4_service
python main.py

# Terminal 5: Frontend
npm run dev
```

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [QUICKSTART.md](QUICKSTART.md) | Quick reference for starting and using the system |
| [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) | Complete installation, configuration, and usage guide |
| [INTEGRATION_ANALYSIS.md](INTEGRATION_ANALYSIS.md) | Technical architecture and integration details |
| [INTEGRATION_COMPLETION.md](INTEGRATION_COMPLETION.md) | Integration status and what was fixed |
| [backend/README.md](backend/README.md) | Backend architecture and file structure |

---

## 🔌 API Endpoints

### Core Endpoints
- `POST /api/assessment/run` - Run full cognitive assessment
- `GET /api/assessment/history` - Get historical data
- `POST /api/behavior/analyze` - Behavioral pattern analysis
- `POST /api/nlp/analyze` - NLP sentiment analysis
- `POST /api/voice/analyze` - Voice stress analysis
- `POST /api/fusion/score` - Multimodal fusion scoring

### System
- `GET /api/health` - Check all services health
- `GET /docs` - Interactive API documentation (Swagger)

---

## 🧪 Testing

### Health Check
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

### Test NLP Analysis
```bash
curl -X POST http://localhost:8000/api/nlp/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I feel great today!",
    "history_scores": [0.5, 0.3],
    "previous_scores": [0.4, 0.2]
  }'
```

---

## 🏗️ Project Structure

```
NeuroLens/
├── backend/                    # API Gateway + NLP Service
│   ├── main.py                # ⭐ API Gateway (port 8000)
│   ├── api/                   # Assessment & behavior routes
│   ├── database/              # SQLite database
│   └── nlp_engine/            # NLP microservice
│       └── main.py            # ⭐ NLP Service (port 8001)
│
├── member4_service/           # Behavioral + Fusion microservice
│   ├── main.py                # ⭐ Service launcher (port 8003)
│   ├── api/                   # API endpoints
│   ├── core/                  # Fusion logic
│   └── models/                # ML models
│
├── neurolens-voice/           # Voice analysis microservice
│   ├── app.py                 # ⭐ Service launcher (port 8002)
│   ├── routes/                # API endpoints
│   ├── models/                # Voice scoring
│   └── utils/                 # Feature extraction
│
├── src/                       # React frontend
│   ├── components/            # Reusable UI components
│   ├── pages/                 # Page components
│   └── services/              # API client
│
├── start_all_services.ps1     # Windows startup script
├── start_all_services.sh      # Linux/Mac startup script
└── stop_all_services.sh       # Service shutdown script
```

---

## 🎨 Frontend Features

- **Dashboard**: Overview of all metrics and alerts
- **Behavioral Analysis**: Input typing patterns, sleep data
- **NLP Analysis**: Text analysis with sentiment tracking
- **Voice Analysis**: Audio upload and stress scoring
- **Fusion Dashboard**: Combined risk assessment
- **History & Trends**: Historical data visualization
- **Alerts**: Risk notifications and flags

---

## 🔧 Technology Stack

### Frontend
- React 19
- Vite 7
- Recharts (charts/graphs)
- Axios (API client)
- Tailwind CSS

### Backend Services
- FastAPI (all microservices)
- SQLite (main database)
- SQLAlchemy (ORM)
- Transformers (NLP models)
- NumPy/SciPy (ML algorithms)
- Audio processing libraries

---

## 🛡️ Privacy & Security

- **Local Processing**: All analysis runs locally, no cloud dependencies
- **No External APIs**: Complete offline capability
- **Data Storage**: Local SQLite database
- **User Control**: Data never leaves the system

---

## ⚠️ Current Limitations

1. **Database**: Uses SQLite (upgrade to PostgreSQL for production)
2. **Authentication**: Not implemented (add before production)
3. **CORS**: Currently allows all origins (restrict in production)
4. **Environment Variables**: Hardcoded service URLs
5. **Monitoring**: Console logging only

See [INTEGRATION_COMPLETION.md](INTEGRATION_COMPLETION.md) for full list.

---

## 🚀 Next Steps

### For Development
1. Run the system using automated script
2. Test each feature page in the frontend
3. Review API documentation at `/docs`
4. Check service logs for errors

### For Production
1. Add authentication (JWT)
2. Configure production database
3. Set up proper logging system
4. Add monitoring (Prometheus/Grafana)
5. Configure reverse proxy (nginx)
6. Set up CI/CD pipeline

See [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) for details.

---

## 📞 Support

### Troubleshooting
1. Check service logs in terminal
2. Visit http://localhost:8000/docs for API docs
3. Check http://localhost:8000/api/health
4. See [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) troubleshooting section

### Common Issues
- **Port in use**: See QUICKSTART.md for how to kill processes
- **Dependencies**: Run `pip install -r requirements.txt`
- **Services not connecting**: Verify all 5 services are running

---

## 📄 License

[Add your license here]

---

## 👥 Contributors

- Member 1: NLP Engine
- Member 2: Voice Analysis Engine  
- Member 3: Behavioral Engine
- Member 4: Fusion Engine + Integration
- Frontend Team: React Dashboard

---

## 🎯 Project Goals

NeuroLens aims to provide **early detection** of mental health deterioration through:
- Passive behavioral monitoring
- Natural language analysis
- Voice stress detection
- Privacy-preserving architecture
- Actionable risk insights

---

**Status**: ✅ Fully Integrated & Ready for Testing
**Last Updated**: March 5, 2026
**Integration**: Completed by Senior Software Architect
