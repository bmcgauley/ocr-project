# Create all beads tasks for 7-day PoC
# Fixed version without --status flag

Write-Host "Creating all tasks from 7-day PoC plan..." -ForegroundColor Cyan
Write-Host ""

# Day 1: Environment Setup & Foundation
Write-Host "[Day 1: Environment Setup & Foundation]" -ForegroundColor Yellow
$day1 = & .\bin\bd.exe create "Day 1: Environment Setup & Foundation" -p 0 -t epic --silent
Write-Host "Created epic: $day1"

& .\bin\bd.exe create "Story 1.1: Development Environment Setup" --parent $day1 -p 1 -t task --silent | Out-Null
& .\bin\bd.exe create "Story 1.2: Project Structure Creation" --parent $day1 -p 1 -t task --silent | Out-Null
& .\bin\bd.exe create "Story 1.3: Sample Document Collection" --parent $day1 -p 1 -t task --silent | Out-Null
& .\bin\bd.exe create "Story 1.4: Frontend & API Setup" --parent $day1 -p 1 -t task --silent | Out-Null
Write-Host "  Created 4 stories" -ForegroundColor Green

# Day 2: Preprocessing Pipeline
Write-Host "`n[Day 2: Preprocessing Pipeline]" -ForegroundColor Yellow
$day2 = & .\bin\bd.exe create "Day 2: Preprocessing Pipeline" -p 0 -t epic --silent
Write-Host "Created epic: $day2"

& .\bin\bd.exe create "Story 2.1: Image Loading & Quality Assessment" --parent $day2 -p 1 -t task --silent | Out-Null
& .\bin\bd.exe create "Story 2.2: Preprocessing Operations" --parent $day2 -p 1 -t task --silent | Out-Null
& .\bin\bd.exe create "Story 2.3: Preprocessing Pipeline Integration" --parent $day2 -p 1 -t task --silent | Out-Null
Write-Host "  Created 3 stories" -ForegroundColor Green

# Day 3: Multi-Engine OCR Integration
Write-Host "`n[Day 3: Multi-Engine OCR Integration]" -ForegroundColor Yellow
$day3 = & .\bin\bd.exe create "Day 3: Multi-Engine OCR Integration" -p 0 -t epic --silent
Write-Host "Created epic: $day3"

& .\bin\bd.exe create "Story 3.1: Tesseract Integration" --parent $day3 -p 1 -t task --silent | Out-Null
& .\bin\bd.exe create "Story 3.2: PaddleOCR Integration" --parent $day3 -p 1 -t task --silent | Out-Null
& .\bin\bd.exe create "Story 3.3: EasyOCR Integration" --parent $day3 -p 1 -t task --silent | Out-Null
& .\bin\bd.exe create "Story 3.4: Multi-Engine Orchestration" --parent $day3 -p 1 -t task --silent | Out-Null
Write-Host "  Created 4 stories" -ForegroundColor Green

# Day 4: Result Ensemble & Confidence Scoring
Write-Host "`n[Day 4: Result Ensemble & Confidence Scoring]" -ForegroundColor Yellow
$day4 = & .\bin\bd.exe create "Day 4: Result Ensemble & Confidence Scoring" -p 0 -t epic --silent
Write-Host "Created epic: $day4"

& .\bin\bd.exe create "Story 4.1: Text Comparison & Voting" --parent $day4 -p 1 -t task --silent | Out-Null
& .\bin\bd.exe create "Story 4.2: Confidence Score Calculation" --parent $day4 -p 1 -t task --silent | Out-Null
& .\bin\bd.exe create "Story 4.3: Error Handling & Fallback" --parent $day4 -p 1 -t task --silent | Out-Null
& .\bin\bd.exe create "Story 4.4: Baseline Testing" --parent $day4 -p 1 -t task --silent | Out-Null
Write-Host "  Created 4 stories" -ForegroundColor Green

# Day 5: Entity Extraction & API
Write-Host "`n[Day 5: Entity Extraction & API]" -ForegroundColor Yellow
$day5 = & .\bin\bd.exe create "Day 5: Entity Extraction & API" -p 0 -t epic --silent
Write-Host "Created epic: $day5"

& .\bin\bd.exe create "Story 5.1: Regex Pattern Library" --parent $day5 -p 1 -t task --silent | Out-Null
& .\bin\bd.exe create "Story 5.2: NER Model Integration" --parent $day5 -p 1 -t task --silent | Out-Null
& .\bin\bd.exe create "Story 5.3: Schema Mapping" --parent $day5 -p 1 -t task --silent | Out-Null
& .\bin\bd.exe create "Story 5.4: Local LLM Integration (Optional)" --parent $day5 -p 2 -t task --silent | Out-Null
& .\bin\bd.exe create "Story 5.5: FastAPI Endpoints Implementation" --parent $day5 -p 1 -t task --silent | Out-Null
Write-Host "  Created 5 stories" -ForegroundColor Green

# Day 6: Output Formatting & Frontend
Write-Host "`n[Day 6: Output Formatting & Frontend]" -ForegroundColor Yellow
$day6 = & .\bin\bd.exe create "Day 6: Output Formatting & Frontend" -p 0 -t epic --silent
Write-Host "Created epic: $day6"

& .\bin\bd.exe create "Story 6.1: CSV Generation" --parent $day6 -p 1 -t task --silent | Out-Null
& .\bin\bd.exe create "Story 6.2: Validation Rules" --parent $day6 -p 1 -t task --silent | Out-Null
& .\bin\bd.exe create "Story 6.3: Confidence-Based Review Flagging" --parent $day6 -p 1 -t task --silent | Out-Null
& .\bin\bd.exe create "Story 6.4: Logging & Metadata" --parent $day6 -p 1 -t task --silent | Out-Null
& .\bin\bd.exe create "Story 6.5: Next.js Frontend UI Development" --parent $day6 -p 1 -t task --silent | Out-Null
Write-Host "  Created 5 stories" -ForegroundColor Green

# Day 7: Integration Testing & Documentation
Write-Host "`n[Day 7: Integration Testing & Documentation]" -ForegroundColor Yellow
$day7 = & .\bin\bd.exe create "Day 7: Integration Testing & Documentation" -p 0 -t epic --silent
Write-Host "Created epic: $day7"

& .\bin\bd.exe create "Story 7.1: End-to-End Pipeline & Frontend Testing" --parent $day7 -p 1 -t task --silent | Out-Null
& .\bin\bd.exe create "Story 7.2: Edge Case Testing" --parent $day7 -p 1 -t task --silent | Out-Null
& .\bin\bd.exe create "Story 7.3: Performance Benchmarking" --parent $day7 -p 1 -t task --silent | Out-Null
& .\bin\bd.exe create "Story 7.4: Documentation & Lessons Learned" --parent $day7 -p 1 -t task --silent | Out-Null
& .\bin\bd.exe create "Story 7.5: Demo Preparation (CLI + Web UI)" --parent $day7 -p 1 -t task --silent | Out-Null
Write-Host "  Created 5 stories" -ForegroundColor Green

Write-Host "`n" -ForegroundColor Cyan
Write-Host "=" -ForegroundColor Green
Write-Host "Setup complete! Created 7 epics and 30 stories" -ForegroundColor Green
Write-Host "=" -ForegroundColor Green
Write-Host "`nView tasks:" -ForegroundColor Yellow
Write-Host "  .\bin\bd.exe list" -ForegroundColor White
Write-Host "  .\bin\bd.exe ready" -ForegroundColor White
