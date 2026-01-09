# OCR Agent System - Historical Document Extraction
## Proof of Concept Implementation

---

## 📋 Project Overview

This project implements an AI-powered, multi-agent OCR system designed to extract structured data from historical documents (1950s-1960s) and convert them to CSV format. The system uses intelligent preprocessing, multiple OCR engines, and confidence-based validation to handle degraded documents, handwriting, and mixed content.

**Timeline:** 7-day PoC (January 11-17, 2026)
**Budget:** $0 (100% free and open-source tools)

---

## 🗂️ Project Structure

```
ocr-project/
├── README.md                    # This file
├── CLAUDE.md                    # AI agent development workflow & rules
├── BEADS_SETUP.md              # Task tracking system guide
├── .gitignore                   # Git ignore rules
│
├── ref/                         # Project documentation
│   ├── PoC.md                  # 7-day implementation plan & task tracking
│   ├── OCR_Agent_Research_Brief_1.md  # Research & technology analysis
│   ├── OCR_Architecture_Diagrams.md   # System architecture diagrams
│   └── Competitive_Strategy.md        # Competition strategy & differentiation
│
├── src/                         # Source code (to be created)
│   ├── agents/                  # Agent modules
│   │   ├── intake.py           # Document intake & classification
│   │   ├── preprocessor.py     # Image preprocessing
│   │   ├── ocr_engine.py       # Multi-engine OCR
│   │   ├── entity_extractor.py # Structured data extraction
│   │   └── output_formatter.py # CSV generation
│   ├── utils/                   # Utility functions
│   │   ├── image_utils.py      # Image loading & manipulation
│   │   └── validation.py       # Data validation
│   └── orchestrator.py          # Main pipeline coordinator
│
├── tests/                       # Test suite (to be created)
│   ├── test_*.py               # Unit tests
│   └── sample_documents/        # Test documents
│
├── output/                      # Generated outputs
│
├── bin/                         # Binary tools
│   └── bd.exe                  # Beads task tracker
│
├── bd.ps1                       # Beads wrapper script (Windows)
└── requirements.txt             # Python dependencies (to be created)
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **Git**
- **npm** (for optional tools)

### Initial Setup

```bash
# 1. Clone or navigate to project directory
cd ocr-project

# 2. Read essential documentation
# - CLAUDE.md for development workflow
# - ref/PoC.md for 7-day implementation plan
# - BEADS_SETUP.md for task tracking

# 3. Create Python virtual environment
python -m venv venv

# 4. Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
.\venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# 5. Install dependencies (once requirements.txt is created)
pip install -r requirements.txt

# 6. Initialize beads (task tracking)
./bin/bd.exe init

# 7. Create first task
./bin/bd.exe create "Day 1: Environment Setup" -p 0 --status in-progress
```

---

## 📚 Essential Documentation

### For AI Agents (Claude)

**MUST READ ON EVERY SESSION START:**
1. **[CLAUDE.md](CLAUDE.md)** - Development workflow, coding standards, quality gates
2. **[ref/PoC.md](ref/PoC.md)** - 7-day plan, current progress, task breakdown
3. **[BEADS_SETUP.md](BEADS_SETUP.md)** - Task tracking commands and workflow

### For Humans

1. **[ref/OCR_Agent_Research_Brief_1.md](ref/OCR_Agent_Research_Brief_1.md)** - Technology research, model comparisons, benchmarks
2. **[ref/OCR_Architecture_Diagrams.md](ref/OCR_Architecture_Diagrams.md)** - System architecture, flowcharts, decision trees
3. **[ref/Competitive_Strategy.md](ref/Competitive_Strategy.md)** - Competition strategy, risk analysis, winning approach

---

## 🛠️ Technology Stack

### OCR Engines (All Free)
- **Tesseract 5.x** - Baseline for clean printed text
- **PaddleOCR** - Primary engine for rotated text and mixed content
- **EasyOCR** - Fallback for handwriting and multilingual documents
- **TrOCR (Hugging Face)** - Transformer-based handwriting recognition

### Image Processing
- **OpenCV** - Image manipulation, deskewing, enhancement
- **PIL/Pillow** - Image I/O and basic operations
- **NumPy** - Array operations
- **scikit-image** - Advanced image processing

### Entity Extraction & NLP
- **Python regex** - Pattern matching for structured data
- **spaCy** - Named Entity Recognition (NER)
- **Ollama + Llama 3.2 3B** (Optional) - Local LLM for complex extraction

### Testing & Quality
- **pytest** - Test framework
- **pytest-cov** - Coverage reporting
- **mypy** - Type checking
- **ruff** - Fast linting
- **black** - Code formatting

### Progress Tracking
- **Beads (bd)** - Distributed task tracking
- **Git** - Version control

---

## 🎯 Development Workflow

### Session Initialization (MANDATORY)
```bash
# 1. Read CLAUDE.md (rules and workflow)
# 2. Read ref/PoC.md (current progress)
# 3. Check beads status
./bin/bd.exe status

# 4. Identify current task from PoC.md
# 5. Create/update bead
./bin/bd.exe create "Story X.X: Task Name" --status in-progress

# 6. Begin work
```

### Implementation Cycle
```bash
# 1. Research (if confidence < 90%)
# 2. Write code with type hints and documentation
# 3. Write unit tests (>=80% coverage)
# 4. Run quality gates:
pytest tests/ -v --cov=src
mypy src/
ruff check src/
black src/ tests/

# 5. Update beads:
./bin/bd.exe update <id> --status completed

# 6. Update PoC.md (check off task)
# 7. Git commit with conventional format
```

### Quality Gates (ALL MUST PASS)
- ✅ Tests: 100% passing, >=80% coverage
- ✅ Type Check: mypy clean
- ✅ Linting: ruff clean
- ✅ Formatting: black applied
- ✅ Manual Validation: Code runs correctly

---

## 📊 Progress Tracking (Dual System)

### System 1: PoC.md (Human-Readable)
- Daily stories with task checkboxes
- Estimated times and acceptance criteria
- Updated by checking off completed tasks

### System 2: Beads (Structured)
- Git-backed task tracking
- Dependencies and blocking relationships
- Detailed notes and audit trail

**RULE:** Both systems must stay synchronized!

### Example Workflow
```bash
# Create bead when starting story
./bin/bd.exe create "Story 2.1: Image Loading" -p 0 --status in-progress

# Work on implementation...

# Mark complete in beads
./bin/bd.exe update bd-a1b2 --status completed

# Check off in PoC.md
# [x] Implement `image_utils.py`

# Commit both
git commit -m "feat(utils): implement image loading

Closes: Story 2.1
Beads: bd-a1b2 completed
Tests: 6/6 passing (95% coverage)"
```

---

## 🧪 Testing Strategy

### Unit Testing Requirements
- Every function must have tests
- Minimum 80% coverage overall
- 100% coverage for critical paths
- Test happy path AND edge cases
- Test error handling

### Test Structure
```python
# tests/test_module.py
import pytest
from src.module import function

class TestModule:
    @pytest.fixture
    def sample_data(self):
        """Fixture for test data."""
        return load_sample()

    def test_function_success(self, sample_data):
        """Test normal operation."""
        result = function(sample_data)
        assert result is not None

    def test_function_error_handling(self):
        """Test error handling."""
        with pytest.raises(ValueError):
            function(invalid_input)
```

---

## 🎨 Code Style Guidelines

### Modern Python Syntax (REQUIRED)
```python
# ✅ GOOD - Modern Python 3.11+
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Result:
    """Result container."""
    text: str
    confidence: float

def process_file(file_path: Path) -> Optional[Result]:
    """Process file with type hints."""
    if not file_path.exists():
        return None

    with file_path.open('r') as f:
        text = f.read()

    return Result(text=text, confidence=0.95)

# ❌ BAD - Old Python style
import os

def process_file(file_path):
    if not os.path.exists(file_path):
        return None

    f = open(file_path, 'r')
    text = f.read()
    f.close()

    return {'text': text, 'confidence': 0.95}
```

### File Size Limit: 500 Lines
- Any file exceeding 500 lines MUST be refactored
- Use component approach and orchestration pattern
- Split into logical modules

---

## 🚦 Success Metrics

### Minimum PoC Success Criteria

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Extraction Success Rate** | ≥80% | 4/5 test documents extract text |
| **Printed Text Accuracy** | ≥85% | CER on clean printed document |
| **Handwriting Accuracy** | ≥50% | CER on handwritten document |
| **Processing Time** | <30 sec/page | Average across all documents |
| **No Crashes** | 100% | System handles all edge cases |
| **CSV Output Valid** | 100% | All outputs are valid CSV |
| **Confidence Calibration** | >0.7 correlation | High confidence = high accuracy |

---

## 📅 7-Day Timeline

- **Day 1 (Jan 11):** Environment setup, project structure, sample documents
- **Day 2 (Jan 12):** Preprocessing pipeline (deskew, enhance, denoise)
- **Day 3 (Jan 13):** Multi-engine OCR integration (Tesseract, PaddleOCR, EasyOCR)
- **Day 4 (Jan 14):** Result ensemble & confidence scoring
- **Day 5 (Jan 15):** Entity extraction & structuring
- **Day 6 (Jan 16):** Output formatting & validation
- **Day 7 (Jan 17):** Integration testing & documentation

See [ref/PoC.md](ref/PoC.md) for detailed task breakdown.

---

## 🔧 Common Commands

### Development
```bash
# Run tests
pytest tests/ -v --cov=src --cov-report=html

# Type check
mypy src/

# Lint
ruff check src/

# Format code
black src/ tests/

# Run all quality checks
pytest tests/ && mypy src/ && ruff check src/ && black --check src/
```

### Task Tracking
```bash
# View ready tasks
./bin/bd.exe ready

# Create task
./bin/bd.exe create "Task name" -p 0 --status in-progress

# Update task
./bin/bd.exe update <id> --status completed

# Daily summary
./bin/bd.exe summary --today
```

### Git
```bash
# Conventional commit format
git commit -m "feat(scope): description

- Bullet point 1
- Bullet point 2

Closes: Story X.X
Tests: X/X passing (XX% coverage)"
```

---

## 🐛 Troubleshooting

### Python Environment Issues
```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Beads Not Working
```bash
# Check if beads is installed
./bin/bd.exe version

# Reinitialize if needed
./bin/bd.exe init

# See BEADS_SETUP.md for detailed troubleshooting
```

### Test Failures
```bash
# Run specific test
pytest tests/test_module.py::TestClass::test_function -v

# Run with debugging
pytest tests/ -v -s

# Check coverage details
pytest tests/ --cov=src --cov-report=html
# Open htmlcov/index.html
```

---

## 📖 Additional Resources

### Official Documentation
- **Tesseract:** https://github.com/tesseract-ocr/tesseract
- **PaddleOCR:** https://github.com/PaddlePaddle/PaddleOCR
- **EasyOCR:** https://github.com/JaidedAI/EasyOCR
- **Beads:** https://github.com/steveyegge/beads

### Research Papers
- TrOCR: Transformer-based OCR (Microsoft, 2023)
- Document Understanding in the Age of LLMs (2024)
- Benchmarking VLMs on Historical Documents (2024)

---

## 🤝 Contributing

This is a proof of concept project. Follow the workflow defined in [CLAUDE.md](CLAUDE.md):
1. Read CLAUDE.md for rules
2. Check PoC.md for current progress
3. Create beads for tasks
4. Write code with tests
5. Pass all quality gates
6. Update both tracking systems
7. Commit with conventional format

---

## 📄 License

[To be determined]

---

## 🎯 Project Goals

### Hypothesis to Validate
> A systematic, multi-stage pipeline using free OCR engines with intelligent preprocessing and fallback chains can achieve 70%+ accuracy on historical documents.

### Success Definition
- Working demo of full pipeline
- Structured CSV output with confidence scores
- Graceful handling of edge cases
- Clear documentation of accuracy and limitations
- Validated multi-agent architecture concept

### Next Steps After PoC
- Expand test set to 20+ documents
- Evaluate free vs paid API trade-offs
- Decide on production technology stack
- Plan full system implementation

---

*Last Updated: 2026-01-09*
*Project Start: 2026-01-11 (Saturday)*
*Target Completion: 2026-01-17 (Friday)*
