#!/bin/bash
# NeuroLens - Start All Services
# Bash script for Linux/Mac
# Usage: ./start_all_services.sh

echo "================================================"
echo "  NeuroLens - Starting All Services"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python not found. Please install Python 3.8+"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js not found. Please install Node.js"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "ERROR: npm not found. Please install Node.js with npm"
    exit 1
fi

echo "Starting services in background..."
echo ""

# Service 1: Backend API Gateway (Port 8000)
echo "[1/5] Starting Backend API Gateway (Port 8000)..."
cd backend && python3 main.py &> ../logs/backend.log &
BACKEND_PID=$!
cd ..
sleep 3

# Service 2: NLP Microservice (Port 8001)
echo "[2/5] Starting NLP Microservice (Port 8001)..."
cd backend/nlp_engine && python3 main.py &> ../../logs/nlp.log &
NLP_PID=$!
cd ../..
sleep 3

# Service 3: Voice Microservice (Port 8002)
echo "[3/5] Starting Voice Microservice (Port 8002)..."
cd neurolens-voice && python3 app.py &> ../logs/voice.log &
VOICE_PID=$!
cd ..
sleep 3

# Service 4: Member4 Behavioral + Fusion (Port 8003)
echo "[4/5] Starting Member4 Service (Port 8003)..."
cd member4_service && python3 main.py &> ../logs/member4.log &
MEMBER4_PID=$!
cd ..
sleep 3

# Service 5: Frontend (Port 5173)
echo "[5/5] Starting Frontend (Port 5173)..."
npm run dev &> logs/frontend.log &
FRONTEND_PID=$!
sleep 2

echo ""
echo "================================================"
echo "  All Services Started!"
echo "================================================"
echo ""
echo "Services running on:"
echo "  Frontend:          http://localhost:5173"
echo "  API Gateway:       http://localhost:8000"
echo "  NLP Service:       http://localhost:8001"
echo "  Voice Service:     http://localhost:8002"
echo "  Member4 Service:   http://localhost:8003"
echo ""
echo "API Documentation:   http://localhost:8000/docs"
echo "Health Check:        http://localhost:8000/api/health"
echo ""
echo "Process IDs:"
echo "  Backend:    $BACKEND_PID"
echo "  NLP:        $NLP_PID"
echo "  Voice:      $VOICE_PID"
echo "  Member4:    $MEMBER4_PID"
echo "  Frontend:   $FRONTEND_PID"
echo ""
echo "To stop all services, run: ./stop_all_services.sh"
echo "Or manually: kill $BACKEND_PID $NLP_PID $VOICE_PID $MEMBER4_PID $FRONTEND_PID"
echo ""

# Save PIDs to file for stop script
echo "$BACKEND_PID" > .pids
echo "$NLP_PID" >> .pids
echo "$VOICE_PID" >> .pids
echo "$MEMBER4_PID" >> .pids
echo "$FRONTEND_PID" >> .pids
