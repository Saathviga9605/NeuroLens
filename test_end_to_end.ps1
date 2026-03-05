# NeuroLens - End-to-End Integration Test
# Tests the complete pipeline: Frontend → Backend → Microservices → Results

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  NeuroLens - End-to-End Integration Test" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

$testsPassed = 0
$testsFailed = 0

# Test 1: NLP Analysis
Write-Host "[Test 1] Testing NLP Analysis Pipeline..." -ForegroundColor Yellow
try {
    $nlpRequest = @{
        text = "I'm feeling really great today! Everything is wonderful."
        history_scores = @(0.5, 0.3, 0.2)
        previous_scores = @(0.4, 0.3)
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/nlp/analyze" -Method Post -Body $nlpRequest -ContentType "application/json" -TimeoutSec 10
    
    if ($response.sentiment_score -and $response.risk_flag -ne $null) {
        Write-Host "  [PASS] NLP Analysis Working" -ForegroundColor Green
        Write-Host "    Sentiment Score: $($response.sentiment_score)" -ForegroundColor Gray
        Write-Host "    Risk Flag: $($response.risk_flag)" -ForegroundColor Gray
        $testsPassed++
    } else {
        Write-Host "  [FAIL] NLP Analysis - Invalid Response" -ForegroundColor Red
        $testsFailed++
    }
} catch {
    Write-Host "  [FAIL] NLP Analysis - Error: $($_.Exception.Message)" -ForegroundColor Red
    $testsFailed++
}
Write-Host ""

# Test 2: Behavioral Analysis
Write-Host "[Test 2] Testing Behavioral Analysis Pipeline..." -ForegroundColor Yellow
try {
    $behaviorRequest = @{
        sleep_hours = 7.5
        wpm = 45.2
        error_rate = 0.12
        rhythm_std = 0.8
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/behavior/analyze" -Method Post -Body $behaviorRequest -ContentType "application/json" -TimeoutSec 10
    
    if ($response.behavioral_score -and $response.csi_score) {
        Write-Host "  [PASS] Behavioral Analysis Working" -ForegroundColor Green
        Write-Host "    Behavioral Score: $($response.behavioral_score)" -ForegroundColor Gray
        Write-Host "    CSI Score: $($response.csi_score)" -ForegroundColor Gray
        $testsPassed++
    } else {
        Write-Host "  [FAIL] Behavioral Analysis - Invalid Response" -ForegroundColor Red
        $testsFailed++
    }
} catch {
    Write-Host "  [FAIL] Behavioral Analysis - Error: $($_.Exception.Message)" -ForegroundColor Red
    $testsFailed++
}
Write-Host ""

# Test 3: Assessment Run
Write-Host "[Test 3] Testing Full Assessment Pipeline..." -ForegroundColor Yellow
try {
    $assessmentRequest = @{
        sleep_hours = 6.5
        wpm = 42.0
        error_rate = 0.15
        rhythm_std = 1.2
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/assessment/run" -Method Post -Body $assessmentRequest -ContentType "application/json" -TimeoutSec 10
    
    if ($response.behavioral_score -and $response.csi_score) {
        Write-Host "  [PASS] Full Assessment Working" -ForegroundColor Green
        Write-Host "    Behavioral Score: $($response.behavioral_score)" -ForegroundColor Gray
        Write-Host "    Voice Score: $($response.voice_score)" -ForegroundColor Gray
        Write-Host "    NLP Score: $($response.nlp_score)" -ForegroundColor Gray
        Write-Host "    CSI Score: $($response.csi_score)" -ForegroundColor Gray
        Write-Host "    Risk Flag: $($response.risk_flag)" -ForegroundColor Gray
        $testsPassed++
    } else {
        Write-Host "  [FAIL] Full Assessment - Invalid Response" -ForegroundColor Red
        $testsFailed++
    }
} catch {
    Write-Host "  [FAIL] Full Assessment - Error: $($_.Exception.Message)" -ForegroundColor Red
    $testsFailed++
}
Write-Host ""

# Test 4: Assessment History
Write-Host "[Test 4] Testing Assessment History..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/assessment/history" -Method Get -TimeoutSec 10
    
    if ($response -is [Array]) {
        Write-Host "  [PASS] Assessment History Working" -ForegroundColor Green
        Write-Host "    History Records: $($response.Count)" -ForegroundColor Gray
        $testsPassed++
    } else {
        Write-Host "  [FAIL] Assessment History - Invalid Response" -ForegroundColor Red
        $testsFailed++
    }
} catch {
    Write-Host "  [FAIL] Assessment History - Error: $($_.Exception.Message)" -ForegroundColor Red
    $testsFailed++
}
Write-Host ""

# Summary
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Test Results Summary" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Tests Passed: $testsPassed" -ForegroundColor Green
Write-Host "Tests Failed: $testsFailed" -ForegroundColor Red
Write-Host ""

$totalTests = $testsPassed + $testsFailed
$passRate = if ($totalTests -gt 0) { [math]::Round(($testsPassed / $totalTests) * 100, 2) } else { 0 }

Write-Host "Pass Rate: $passRate%" -ForegroundColor $(if ($passRate -eq 100) { "Green" } elseif ($passRate -ge 75) { "Yellow" } else { "Red" })
Write-Host ""

if ($testsFailed -eq 0) {
    Write-Host "ALL TESTS PASSED [OK]" -ForegroundColor Green
    Write-Host ""
    Write-Host "The NeuroLens system is fully operational!" -ForegroundColor Cyan
    Write-Host "You can now access:" -ForegroundColor White
    Write-Host "  Frontend:     http://localhost:5173" -ForegroundColor Yellow
    Write-Host "  API Gateway:  http://localhost:8000" -ForegroundColor Yellow
    Write-Host "  API Docs:     http://localhost:8000/docs" -ForegroundColor Yellow
} else {
    Write-Host "SOME TESTS FAILED [ERROR]" -ForegroundColor Red
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
