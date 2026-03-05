# NeuroLens Integration Analysis & Fixes

## Executive Summary
The integration branch has been merged, but several critical integration issues prevent the system from running end-to-end. This document outlines identified problems and implemented solutions.

## Architecture Overview

### Intended Architecture
```
Frontend (React, Port 5173)
    ↓ HTTP requests to /api/*
Backend API Gateway (FastAPI, Port 8000)
    ↓ Proxies requests to microservices
    ├→ NLP Service (Port 8001)
    ├→ Voice Service (Port 8002)
    └→ Member4 Service (Port 8003)
```

### Current Issues

#### 1. **Missing Backend Proxy Routes**
- **Problem**: Frontend calls `/api/voice/analyze` and `/api/nlp/analyze`, but backend doesn't have these routes
- **Impact**: Frontend features cannot reach AI microservices
- **Fix**: Add proxy endpoints in backend/main.py that forward to microservices

#### 2. **Port Configuration Inconsistencies**
- **Problem**: 
  - Voice service runs on 8003
  - Member4 service runs on 8004
  - NLP service has no standalone launcher
- **Expected**:
  - NLP → 8001
  - Voice → 8002
  - Member4 → 8003
- **Fix**: Standardize all port configurations

#### 3. **Duplicate Backend Files**
- **Problem**: `backend/server.py` exists alongside `backend/main.py`
- `server.py` appears to be an NLP service test/demo file
- Creates confusion about which backend to run
- **Fix**: Rename server.py or clarify its purpose; it's actually for NLP microservice

#### 4. **NLP Service Missing Launcher**
- **Problem**: NLP service code exists in `backend/nlp_engine/` but no standalone app
- **Fix**: Create `backend/nlp_engine/main.py` to run NLP service independently

#### 5. **Request/Response Format Mismatches**
- **Problem**: 
  - Frontend sends simple text for NLP analysis
  - NLP service expects complex input with `history_scores`, `previous_scores`
  - Voice service expects file upload (multipart/form-data)
- **Fix**: Backend proxy must adapt request/response formats

#### 6. **Database Inconsistency**
- **Problem**: 
  - backend/main.py uses SQLite
  - backend/server.py references MongoDB
- **Decision**: Keep SQLite for main backend (simpler for local dev)

#### 7. **Placeholder AI Scores**
- **Problem**: `/api/assessment/run` and `/api/behavior/analyze` use hardcoded scores (50) instead of calling microservices
- **Fix**: Update these endpoints to call actual microservices

## Implementation Plan

### Phase 1: Port Standardization ✓
- [x] Update NLP service to port 8001
- [x] Update Voice service to port 8002
- [x] Update Member4 service to port 8003

### Phase 2: Backend Proxy Routes ✓
- [x] Add `/api/nlp/analyze` proxy endpoint
- [x] Add `/api/voice/analyze` proxy endpoint
- [x] Add `/api/fusion/score` proxy endpoint
- [x] Implement request/response adapters

### Phase 3: Service Launchers ✓
- [x] Create NLP service standalone launcher
- [x] Fix Member4 service endpoints
- [x] Verify Voice service configuration

### Phase 4: Startup Automation ✓
- [x] Create master startup script
- [x] Document startup sequence
- [x] Add health check endpoints

### Phase 5: Integration Testing
- [ ] Test frontend → backend → NLP flow
- [ ] Test frontend → backend → Voice flow
- [ ] Test frontend → backend → Member4 flow
- [ ] Test full assessment pipeline

## Final Port Configuration

| Service | Port | Base Path |
|---------|------|-----------|
| Frontend (Vite dev) | 5173 | / |
| Backend API Gateway | 8000 | /api |
| NLP Microservice | 8001 | /api/nlp |
| Voice Microservice | 8002 | /api/voice |
| Member4 Microservice | 8003 | /api/v1 |

## Startup Sequence

1. Start Backend API Gateway: `cd backend && uvicorn main:app --port 8000 --reload`
2. Start NLP Service: `cd backend/nlp_engine && python -m api.app`
3. Start Voice Service: `cd neurolens-voice && python app.py`
4. Start Member4 Service: `cd member4_service && python main.py`
5. Start Frontend: `npm run dev`

## Files Modified/Created

### Modified:
- `backend/main.py` - Added proxy routes for voice, NLP, fusion
- `neurolens-voice/app.py` - Changed port to 8002
- `member4_service/main.py` - Changed port to 8003
- `vite.config.js` - Verified proxy configuration

### Created:
- `backend/nlp_engine/main.py` - Standalone NLP service launcher
- `start_all_services.ps1` - PowerShell startup script
- `start_all_services.sh` - Bash startup script
- `INTEGRATION_ANALYSIS.md` - This document

## Notes

- All microservices remain independent
- Microservice structure preserved
- No functionality removed
- Database remains SQLite for simplicity
- MongoDB support available if needed via environment variables
