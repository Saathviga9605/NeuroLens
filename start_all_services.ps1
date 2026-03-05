# NeuroLens - Start All Services
# PowerShell script for Windows
# Usage: .\start_all_services.ps1

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  NeuroLens - Starting All Services" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python virtual environment exists
if (Test-Path "D:\NEUROLENS\.venv\Scripts\python.exe") {
    $PYTHON_CMD = "D:\NEUROLENS\.venv\Scripts\python.exe"
    Write-Host "Using virtual environment Python: $PYTHON_CMD" -ForegroundColor Green
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $PYTHON_CMD = "python"
    Write-Host "Using system Python" -ForegroundColor Yellow
} else {
    Write-Host "ERROR: Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Check if Node.js is installed
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Node.js not found. Please install Node.js" -ForegroundColor Red
    exit 1
}

Write-Host "Starting services in background..." -ForegroundColor Yellow
Write-Host ""

# Service 1: Backend API Gateway (Port 8000)
Write-Host "[1/5] Starting Backend API Gateway (Port 8000)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd D:\NEUROLENS\NeuroLens\backend; $PYTHON_CMD main.py" -WindowStyle Normal
Start-Sleep -Seconds 3

# Service 2: NLP Microservice (Port 8001)
Write-Host "[2/5] Starting NLP Microservice (Port 8001)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd D:\NEUROLENS\NeuroLens\backend\nlp_engine; $PYTHON_CMD main.py" -WindowStyle Normal
Start-Sleep -Seconds 3

# Service 3: Voice Microservice (Port 8002)
Write-Host "[3/5] Starting Voice Microservice (Port 8002)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd D:\NEUROLENS\NeuroLens\neurolens-voice; $PYTHON_CMD app.py" -WindowStyle Normal
Start-Sleep -Seconds 3

# Service 4: Member4 Behavioral + Fusion (Port 8003)
Write-Host "[4/5] Starting Member4 Service (Port 8003)..." -ForegroundColor Green  
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd D:\NEUROLENS\NeuroLens\member4_service; $PYTHON_CMD main.py" -WindowStyle Normal
Start-Sleep -Seconds 3

# Service 5: Frontend (Port 5173)
Write-Host "[5/5] Starting Frontend (Port 5173)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd D:\NEUROLENS\NeuroLens; npm run dev" -WindowStyle Normal
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  All Services Started!" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Services running on:" -ForegroundColor White
Write-Host "  Frontend:          http://localhost:5173" -ForegroundColor Yellow
Write-Host "  API Gateway:       http://localhost:8000" -ForegroundColor Yellow
Write-Host "  NLP Service:       http://localhost:8001" -ForegroundColor Yellow
Write-Host "  Voice Service:     http://localhost:8002" -ForegroundColor Yellow
Write-Host "  Member4 Service:   http://localhost:8003" -ForegroundColor Yellow
Write-Host ""
Write-Host "API Documentation:   http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "Health Check:        http://localhost:8000/api/health" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C in each terminal window to stop services" -ForegroundColor Gray
Write-Host ""
