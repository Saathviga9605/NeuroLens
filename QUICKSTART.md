# NeuroLens - Quick Start Guide

## 🚀 Start Everything
```powershell
# Windows
.\start_all_services.ps1

# Linux/Mac
./start_all_services.sh
```

## 🌐 Access Points
| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend** | http://localhost:5173 | Main UI |
| **API Docs** | http://localhost:8000/docs | Swagger API |
| **Health Check** | http://localhost:8000/api/health | System status |

## 🔧 Ports
- **5173**: Frontend (React + Vite)
- **8000**: Backend API Gateway
- **8001**: NLP Microservice
- **8002**: Voice Microservice
- **8003**: Member4 (Behavioral + Fusion)

## 📋 API Endpoints

### Assessment & Behavior
```bash
# Run cognitive assessment
POST /api/assessment/run
{
  "sleep_hours": 7.5,
  "wpm": 45.2,
  "error_rate": 0.12,
  "rhythm_std": 0.8
}

# Get assessment history
GET /api/assessment/history

# Analyze behavior
POST /api/behavior/analyze
{
  "sleep_hours": 7.5,
  "wpm": 45.2,
  "error_rate": 0.12,
  "rhythm_std": 0.8
}
```

### NLP Analysis
```bash
POST /api/nlp/analyze
{
  "text": "I'm feeling great today!",
  "history_scores": [0.5, 0.3, 0.2],
  "previous_scores": [0.4, 0.3]
}
```

### Voice Analysis
```bash
POST /api/voice/analyze
Content-Type: multipart/form-data

file: <audio-file.wav>
user_id: "user123" (optional)
update_baseline: true (optional)
```

### Health Check
```bash
GET /api/health
```

## 🛠️ Manual Start (if needed)

### Terminal 1 - Backend Gateway
```bash
cd backend
python main.py
```

### Terminal 2 - NLP Service
```bash
cd backend/nlp_engine
python main.py
```

### Terminal 3 - Voice Service
```bash
cd neurolens-voice
python app.py
```

### Terminal 4 - Member4 Service
```bash
cd member4_service
python main.py
```

### Terminal 5 - Frontend
```bash
npm run dev
```

## ⚠️ Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Dependencies Missing
```bash
# Backend
cd backend
pip install -r requirements.txt

# Voice service
cd neurolens-voice
pip install -r requirements.txt

# Member4 service
cd member4_service
pip install -r requirements.txt

# Frontend
npm install
```

### Service Won't Connect
1. Check if target service is running
2. Verify port configuration
3. Check firewall settings
4. Review service logs

## 📚 More Info
- **Full Guide**: See `INTEGRATION_GUIDE.md`
- **Architecture**: See `INTEGRATION_ANALYSIS.md`
- **Status**: See `INTEGRATION_COMPLETION.md`

## ✅ Quick Test
```bash
curl http://localhost:8000/api/health
```

Should return:
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

---
**Need Help?** Check the logs in each service terminal or visit http://localhost:8000/docs
