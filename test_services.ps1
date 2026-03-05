# NeuroLens - Test All Services
# PowerShell script to verify all services are running correctly

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  NeuroLens - Service Health Check" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

$allHealthy = $true

# Test Backend API Gateway (Port 8000)
Write-Host "Testing Backend API Gateway (Port 8000)..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/health" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "  [OK] Backend API Gateway: HEALTHY" -ForegroundColor Green
        $content = $response.Content | ConvertFrom-Json
        Write-Host "    Services: $($content.services | ConvertTo-Json -Compress)" -ForegroundColor Gray
    }
} catch {
    Write-Host "  [FAIL] Backend API Gateway: FAILED" -ForegroundColor Red
    Write-Host "    Error: $($_.Exception.Message)" -ForegroundColor Red
    $allHealthy = $false
}
Write-Host ""

#Test NLP Service (Port 8001)
Write-Host "Testing NLP Service (Port 8001)..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8001/health" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "  [OK] NLP Service: HEALTHY" -ForegroundColor Green
        $content = $response.Content | ConvertFrom-Json
        Write-Host "    Model Loaded: $($content.model_loaded)" -ForegroundColor Gray
    }
} catch {
    Write-Host "  [FAIL] NLP Service: FAILED" -ForegroundColor Red
    Write-Host "    Error: $($_.Exception.Message)" -ForegroundColor Red
    $allHealthy = $false
}
Write-Host ""

# Test Voice Service (Port 8002)
Write-Host "Testing Voice Service (Port 8002)..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8002/api/health" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "  [OK] Voice Service: HEALTHY" -ForegroundColor Green
    }
} catch {
    Write-Host "  [FAIL] Voice Service: FAILED" -ForegroundColor Red
    Write-Host "    Error: $($_.Exception.Message)" -ForegroundColor Red
    $allHealthy = $false
}
Write-Host ""

# Test Member4 Service (Port 8003)
Write-Host "Testing Member4 Service (Port 8003)..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8003/api/v1/health" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "  [OK] Member4 Service: HEALTHY" -ForegroundColor Green
    }
} catch {
    Write-Host "  [FAIL] Member4 Service: FAILED" -ForegroundColor Red
    Write-Host "    Error: $($_.Exception.Message)" -ForegroundColor Red
    $allHealthy = $false
}
Write-Host ""

Write-Host "================================================" -ForegroundColor Cyan
if ($allHealthy) {
    Write-Host "  ALL SERVICES HEALTHY [OK]" -ForegroundColor Green
} else {
    Write-Host "  SOME SERVICES FAILED [ERROR]" -ForegroundColor Red
}
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
