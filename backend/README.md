# Backend README

## Main Files

### `main.py` ⭐ **USE THIS**
**Purpose**: API Gateway for NeuroLens system

**What it does**:
- Acts as central entry point for all API requests
- Routes `/api/behavior` and `/api/assessment` endpoints
- **Proxies** requests to AI microservices:
  - `/api/nlp/analyze` → NLP Service (port 8001)
  - `/api/voice/analyze` → Voice Service (port 8002)
  - `/api/fusion/score` → Member4 Service (port 8003)
- Manages SQLite database for sessions
- Provides health check endpoint

**Port**: 8000

**How to run**:
```bash
python main.py
```

---

### `server_mongodb_example.py`
**Purpose**: Alternative NLP service example (NOT USED IN PRODUCTION)

**What it does**:
- Example implementation of NLP service using MongoDB
- Has demo endpoints for status checks
- Uses Motor (async MongoDB driver)
- Originally created as a test/demo file

**Status**: ⚠️ **NOT CURRENTLY USED**

This file is kept for reference but is **not part of the active system**.

The production NLP service is located at: `nlp_engine/main.py`

**If you want to use MongoDB** instead of SQLite for the main backend:
1. Set up MongoDB
2. Configure environment variables (MONGO_URL, DB_NAME)
3. Adapt the code from this example

---

## Directory Structure

```
backend/
├── main.py                          # ⭐ Main API Gateway (RUN THIS)
├── server_mongodb_example.py        # ⚠️  MongoDB example (reference only)
├── requirements.txt                 # Python dependencies
│
├── api/                             # API route modules
│   ├── assessment.py                # Assessment endpoints
│   └── behavior.py                  # Behavior endpoints
│
├── database/                        # SQLite database
│   ├── db.py                        # Database connection
│   └── schema.py                    # Data models
│
├── engines/                         # Processing engines
│   ├── behavior_engine.py           # Behavioral scoring
│   └── fusion_engine.py             # Fusion calculations
│
├── drift/                           # Drift detection
│   └── drift_detector.py            # Drift algorithms
│
└── nlp_engine/                      # NLP Microservice
    ├── main.py                      # ⭐ NLP Service Launcher
    ├── api/                         # NLP API endpoints
    ├── model/                       # Sentiment models
    ├── drift/                       # NLP drift calculations
    └── features/                    # Linguistic features

```

---

## Running the System

### Option 1: Automated (Recommended)
From project root:
```powershell
# Windows
.\start_all_services.ps1

# Linux/Mac
./start_all_services.sh
```

### Option 2: Manual

**Step 1**: Start API Gateway
```bash
cd backend
python main.py
```

**Step 2**: Start NLP Microservice
```bash
cd backend/nlp_engine
python main.py
```

**Step 3**: Start other services (see INTEGRATION_GUIDE.md)

---

## Database

**Current**: SQLite (`cognitive_data.db`)
- File-based database
- No setup required
- Perfect for development
- Tables created automatically

**Alternative**: MongoDB
- See `server_mongodb_example.py` for reference
- Requires MongoDB installation
- Better for production at scale
- Requires environment variables

---

## Configuration

### Environment Variables (Optional)
Create `.env` file in `backend/` directory:

```env
# For MongoDB (if using server_mongodb_example.py)
MONGO_URL=mongodb://localhost:27017
DB_NAME=neurolens
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Add other config as needed
```

### Port Configuration
Ports are set in the code:
- API Gateway: 8000 (in `main.py`)
- NLP Service: 8001 (in `nlp_engine/main.py`)

---

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/health

---

## Troubleshooting

### Import Errors
```bash
pip install -r requirements.txt
```

### Port Already in Use
```bash
# Find process on port 8000
netstat -ano | findstr :8000

# Kill it (Windows)
taskkill /PID <PID> /F

# Kill it (Linux/Mac)
lsof -ti:8000 | xargs kill -9
```

### Database Locked
```bash
# Delete and restart
rm cognitive_data.db
python main.py
```

---

## For More Information
- **Integration Guide**: `../INTEGRATION_GUIDE.md`
- **Quick Start**: `../QUICKSTART.md`
- **Architecture**: `../INTEGRATION_ANALYSIS.md`
