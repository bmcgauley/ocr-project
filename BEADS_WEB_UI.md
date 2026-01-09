# Beads Web UI - Quick Access Guide

## ✅ Web Interface Running

**Access URL:** http://127.0.0.1:3001

The beads web UI is currently running and connected to your project database.

---

## 📊 Current Status

**Tasks Created:**
- ✅ 7 Epics (Days 1-7)
- ✅ 30 Stories (all tasks from PoC.md)
- ✅ **Total: 37 tasks**

**Database Location:** `c:\GitHub\ocr-project\.beads\beads.db`

---

## 🎯 Task Breakdown by Day

### Day 1: Environment Setup & Foundation (ocr-project-a3z)
- Story 1.1: Development Environment Setup
- Story 1.2: Project Structure Creation
- Story 1.3: Sample Document Collection
- Story 1.4: Frontend & API Setup

### Day 2: Preprocessing Pipeline (ocr-project-jt6)
- Story 2.1: Image Loading & Quality Assessment
- Story 2.2: Preprocessing Operations
- Story 2.3: Preprocessing Pipeline Integration

### Day 3: Multi-Engine OCR Integration (ocr-project-m6u)
- Story 3.1: Tesseract Integration
- Story 3.2: PaddleOCR Integration
- Story 3.3: EasyOCR Integration
- Story 3.4: Multi-Engine Orchestration

### Day 4: Result Ensemble & Confidence Scoring (ocr-project-80k)
- Story 4.1: Text Comparison & Voting
- Story 4.2: Confidence Score Calculation
- Story 4.3: Error Handling & Fallback
- Story 4.4: Baseline Testing

### Day 5: Entity Extraction & API (ocr-project-bke)
- Story 5.1: Regex Pattern Library
- Story 5.2: NER Model Integration
- Story 5.3: Schema Mapping
- Story 5.4: Local LLM Integration (Optional) [P2]
- Story 5.5: FastAPI Endpoints Implementation

### Day 6: Output Formatting & Frontend (ocr-project-22c)
- Story 6.1: CSV Generation
- Story 6.2: Validation Rules
- Story 6.3: Confidence-Based Review Flagging
- Story 6.4: Logging & Metadata
- Story 6.5: Next.js Frontend UI Development

### Day 7: Integration Testing & Documentation (ocr-project-88k)
- Story 7.1: End-to-End Pipeline & Frontend Testing
- Story 7.2: Edge Case Testing
- Story 7.3: Performance Benchmarking
- Story 7.4: Documentation & Lessons Learned
- Story 7.5: Demo Preparation (CLI + Web UI)

---

## 🚀 Starting/Stopping the Web UI

### Start the Web UI
```bash
npx beads-ui start --port 3001
```

Or run in background:
```bash
npx beads-ui start --port 3001 &
```

### Access the UI
Open in your browser:
```
http://127.0.0.1:3001
```

### Stop the Web UI
Find the process and kill it:
```powershell
# Find the process
Get-Process -Name node | Where-Object {$_.Path -like "*beads-ui*"}

# Kill it
Stop-Process -Name node -Force
```

Or simply close the terminal/PowerShell window where it's running.

---

## 💻 CLI Commands (Alternative to Web UI)

```bash
# View all tasks
.\bin\bd.exe list

# View tasks ready to work on (no blockers)
.\bin\bd.exe ready

# View specific task
.\bin\bd.exe show ocr-project-a3z.1

# Start working on a task
.\bin\bd.exe update ocr-project-a3z.1 --assignee "Your Name"

# Mark task as completed
.\bin\bd.exe close ocr-project-a3z.1

# View status summary
.\bin\bd.exe status
```

---

## 📋 Quick Workflow

### Starting Day 1

**Via Web UI:**
1. Open http://127.0.0.1:3001
2. Click on "Day 1: Environment Setup & Foundation"
3. Click on "Story 1.1: Development Environment Setup"
4. Update status and add notes

**Via CLI:**
```bash
# View Day 1 tasks
.\bin\bd.exe show ocr-project-a3z

# Start Story 1.1
.\bin\bd.exe update ocr-project-a3z.1 --assignee "claude"

# Add notes
.\bin\bd.exe update ocr-project-a3z.1 --notes "Setting up virtual environment and installing dependencies"

# Complete the task
.\bin\bd.exe close ocr-project-a3z.1
```

---

## 🔧 Troubleshooting

### Web UI won't start
```bash
# Check if port 3001 is in use
netstat -ano | findstr :3001

# Use a different port
npx beads-ui start --port 3002
```

### Can't see tasks in Web UI
```bash
# Refresh the database
.\bin\bd.exe list

# Check database location
ls .beads/beads.db
```

### Web UI is slow
The first load may download and install beads-ui. Subsequent loads will be faster.

---

## 📚 Additional Resources

- **Beads CLI Help:** `.\bin\bd.exe --help`
- **beads-ui Documentation:** https://github.com/mantoni/beads-ui
- **Project PoC Plan:** [ref/PoC.md](ref/PoC.md)
- **Development Workflow:** [CLAUDE.md](CLAUDE.md)

---

## 🎯 Next Steps

1. **Open the Web UI:** http://127.0.0.1:3001
2. **Review Day 1 tasks**
3. **Start Story 1.1** when ready to begin development
4. **Follow [CLAUDE.md](CLAUDE.md) workflow** for all implementation

---

**Happy tracking! 🚀**
