# PowerShell script to initialize beads and create all tasks from PoC.md
# Run with: ./setup_beads_simple.ps1

Write-Host "=" -ForegroundColor Cyan
Write-Host "Initializing Beads and Creating PoC Tasks" -ForegroundColor Cyan
Write-Host "="  -ForegroundColor Cyan

# Initialize beads
Write-Host "`nInitializing beads..." -ForegroundColor Yellow
& .\bin\bd.exe init 2>&1 | Out-Null

Start-Sleep -Seconds 2

# Check if initialization worked
$status = & .\bin\bd.exe version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "Beads initialized successfully" -ForegroundColor Green
} else {
    Write-Host "Failed to initialize beads" -ForegroundColor Red
    exit 1
}

Write-Host "`nCreating task structure..." -ForegroundColor Yellow

# Day 1
Write-Host "`n[Day 1: Environment Setup & Foundation]" -ForegroundColor Cyan
$day1 = & .\bin\bd.exe create "Day 1: Environment Setup & Foundation" -p 0 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "Created epic: $day1"

$story11 = & .\bin\bd.exe create "Story 1.1: Development Environment Setup" --parent $day1 -p 1 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "  - Story 1.1: $story11"

$story12 = & .\bin\bd.exe create "Story 1.2: Project Structure Creation" --parent $day1 -p 1 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "  - Story 1.2: $story12"

$story13 = & .\bin\bd.exe create "Story 1.3: Sample Document Collection" --parent $day1 -p 1 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "  - Story 1.3: $story13"

$story14 = & .\bin\bd.exe create "Story 1.4: Frontend & API Setup" --parent $day1 -p 1 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "  - Story 1.4: $story14"

# Day 2
Write-Host "`n[Day 2: Preprocessing Pipeline]" -ForegroundColor Cyan
$day2 = & .\bin\bd.exe create "Day 2: Preprocessing Pipeline" -p 0 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "Created epic: $day2"

$story21 = & .\bin\bd.exe create "Story 2.1: Image Loading & Quality Assessment" --parent $day2 -p 1 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "  - Story 2.1: $story21"

$story22 = & .\bin\bd.exe create "Story 2.2: Preprocessing Operations" --parent $day2 -p 1 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "  - Story 2.2: $story22"

$story23 = & .\bin\bd.exe create "Story 2.3: Preprocessing Pipeline Integration" --parent $day2 -p 1 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "  - Story 2.3: $story23"

# Day 3
Write-Host "`n[Day 3: Multi-Engine OCR Integration]" -ForegroundColor Cyan
$day3 = & .\bin\bd.exe create "Day 3: Multi-Engine OCR Integration" -p 0 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "Created epic: $day3"

$story31 = & .\bin\bd.exe create "Story 3.1: Tesseract Integration" --parent $day3 -p 1 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "  - Story 3.1: $story31"

$story32 = & .\bin\bd.exe create "Story 3.2: PaddleOCR Integration" --parent $day3 -p 1 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "  - Story 3.2: $story32"

$story33 = & .\bin\bd.exe create "Story 3.3: EasyOCR Integration" --parent $day3 -p 1 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "  - Story 3.3: $story33"

$story34 = & .\bin\bd.exe create "Story 3.4: Multi-Engine Orchestration" --parent $day3 -p 1 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "  - Story 3.4: $story34"

# Day 4
Write-Host "`n[Day 4: Result Ensemble & Confidence Scoring]" -ForegroundColor Cyan
$day4 = & .\bin\bd.exe create "Day 4: Result Ensemble & Confidence Scoring" -p 0 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "Created epic: $day4"

$story41 = & .\bin\bd.exe create "Story 4.1: Text Comparison & Voting" --parent $day4 -p 1 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "  - Story 4.1: $story41"

$story42 = & .\bin\bd.exe create "Story 4.2: Confidence Score Calculation" --parent $day4 -p 1 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "  - Story 4.2: $story42"

$story43 = & .\bin\bd.exe create "Story 4.3: Error Handling & Fallback" --parent $day4 -p 1 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "  - Story 4.3: $story43"

$story44 = & .\bin\bd.exe create "Story 4.4: Baseline Testing" --parent $day4 -p 1 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "  - Story 4.4: $story44"

# Day 5
Write-Host "`n[Day 5: Entity Extraction & API]" -ForegroundColor Cyan
$day5 = & .\bin\bd.exe create "Day 5: Entity Extraction & API" -p 0 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "Created epic: $day5"

$story51 = & .\bin\bd.exe create "Story 5.1: Regex Pattern Library" --parent $day5 -p 1 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "  - Story 5.1: $story51"

$story52 = & .\bin\bd.exe create "Story 5.2: NER Model Integration" --parent $day5 -p 1 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "  - Story 5.2: $story52"

$story53 = & .\bin\bd.exe create "Story 5.3: Schema Mapping" --parent $day5 -p 1 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "  - Story 5.3: $story53"

$story54 = & .\bin\bd.exe create "Story 5.4: Local LLM Integration (Optional)" --parent $day5 -p 2 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "  - Story 5.4: $story54 (Optional)"

$story55 = & .\bin\bd.exe create "Story 5.5: FastAPI Endpoints Implementation" --parent $day5 -p 1 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "  - Story 5.5: $story55"

# Day 6
Write-Host "`n[Day 6: Output Formatting & Frontend]" -ForegroundColor Cyan
$day6 = & .\bin\bd.exe create "Day 6: Output Formatting & Frontend" -p 0 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "Created epic: $day6"

$story61 = & .\bin\bd.exe create "Story 6.1: CSV Generation" --parent $day6 -p 1 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "  - Story 6.1: $story61"

$story62 = & .\bin\bd.exe create "Story 6.2: Validation Rules" --parent $day6 -p 1 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "  - Story 6.2: $story62"

$story63 = & .\bin\bd.exe create "Story 6.3: Confidence-Based Review Flagging" --parent $day6 -p 1 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "  - Story 6.3: $story63"

$story64 = & .\bin\bd.exe create "Story 6.4: Logging & Metadata" --parent $day6 -p 1 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "  - Story 6.4: $story64"

$story65 = & .\bin\bd.exe create "Story 6.5: Next.js Frontend UI Development" --parent $day6 -p 1 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "  - Story 6.5: $story65"

# Day 7
Write-Host "`n[Day 7: Integration Testing & Documentation]" -ForegroundColor Cyan
$day7 = & .\bin\bd.exe create "Day 7: Integration Testing & Documentation" -p 0 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "Created epic: $day7"

$story71 = & .\bin\bd.exe create "Story 7.1: End-to-End Pipeline & Frontend Testing" --parent $day7 -p 1 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "  - Story 7.1: $story71"

$story72 = & .\bin\bd.exe create "Story 7.2: Edge Case Testing" --parent $day7 -p 1 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "  - Story 7.2: $story72"

$story73 = & .\bin\bd.exe create "Story 7.3: Performance Benchmarking" --parent $day7 -p 1 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "  - Story 7.3: $story73"

$story74 = & .\bin\bd.exe create "Story 7.4: Documentation & Lessons Learned" --parent $day7 -p 1 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "  - Story 7.4: $story74"

$story75 = & .\bin\bd.exe create "Story 7.5: Demo Preparation" --parent $day7 -p 1 --status open 2>&1 | Select-String -Pattern "bd-\w+" | ForEach-Object { $_.Matches.Value }
Write-Host "  - Story 7.5: $story75"

Write-Host "`n" -ForegroundColor Green
Write-Host "=" -ForegroundColor Green
Write-Host "Setup complete! All tasks created." -ForegroundColor Green
Write-Host "=" -ForegroundColor Green
Write-Host "`nView tasks with:" -ForegroundColor Yellow
Write-Host "  .\bin\bd.exe status" -ForegroundColor White
Write-Host "  .\bin\bd.exe ready" -ForegroundColor White
Write-Host "  .\bin\bd.exe list" -ForegroundColor White
