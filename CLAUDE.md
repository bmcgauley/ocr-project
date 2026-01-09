# CLAUDE.md - Development Workflow & Programming Guidelines
## AI Agent Instructions for OCR Project Development

---

## 🚨 CRITICAL: SESSION INITIALIZATION PROTOCOL

### Every New Session MUST Follow This Sequence:

1. **READ THIS FILE FIRST** - [CLAUDE.md](CLAUDE.md)
   - Understand all rules and constraints
   - Review tech stack
   - Understand workflow requirements

2. **READ PROJECT STATUS** - [ref/PoC.md](ref/PoC.md)
   - Review current progress on 7-day plan
   - Identify what day/story we're on
   - Understand completed vs pending tasks

3. **CHECK PROGRESS TRACKING**
   - Read beads status: `beads status`
   - Review open beads
   - Identify current active task

4. **ONLY THEN** - Begin work following the workflow below

---

## 📋 DEFINED TECH STACK (DO NOT DEVIATE)

### Core Languages & Versions
- **Python**: 3.11+ (use modern syntax: type hints, match statements, dataclasses)
- **Package Manager**: pip with virtual environment
- **Version Control**: Git with conventional commits

### Required Libraries (From requirements.txt)

#### OCR Engines
```python
pytesseract>=0.3.10      # Tesseract wrapper
paddleocr>=2.7.0         # Primary OCR engine
easyocr>=1.7.0           # Fallback OCR engine
transformers>=4.30.0     # For TrOCR models
```

#### Image Processing
```python
opencv-python>=4.8.0     # Primary CV library
Pillow>=10.0.0           # Image I/O
numpy>=1.24.0            # Array operations
scikit-image>=0.21.0     # Advanced processing
```

#### NLP & Entity Extraction
```python
spacy>=3.6.0             # NER and linguistic features
```

#### Data Handling
```python
pandas>=2.0.0            # CSV and dataframes
```

#### Testing
```python
pytest>=7.4.0            # Test framework
pytest-cov>=4.1.0        # Coverage reporting
pytest-mock>=3.11.0      # Mocking utilities
```

#### Utilities
```python
python-Levenshtein>=0.21.0  # Text similarity
tqdm>=4.65.0                # Progress bars
loguru>=0.7.0               # Better logging
```

### Code Style & Quality Tools
```python
black>=23.0.0            # Code formatter
ruff>=0.1.0              # Fast linter (replaces flake8, pylint)
mypy>=1.5.0              # Type checking
```

### Modern Python Syntax Requirements

**ALWAYS USE:**
- Type hints for all functions
- Dataclasses for data structures
- Context managers (with statements)
- Pathlib for file operations (not os.path)
- f-strings for formatting (not % or .format())
- Match statements (Python 3.10+) where appropriate
- List/dict comprehensions where readable
- Type annotations from `typing` module

**EXAMPLE:**
```python
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional, Tuple

@dataclass
class OCRResult:
    """Result from OCR engine."""
    text: str
    confidence: float
    engine: str
    processing_time: float

def process_image(
    image_path: Path,
    engines: List[str]
) -> Tuple[OCRResult, Optional[str]]:
    """Process image with specified OCR engines.

    Args:
        image_path: Path to image file
        engines: List of engine names to use

    Returns:
        Tuple of (result, error_message)
    """
    try:
        # Implementation
        result = OCRResult(
            text="extracted text",
            confidence=0.87,
            engine="tesseract",
            processing_time=1.2
        )
        return result, None
    except Exception as e:
        return None, str(e)
```

---

## 🔄 MANDATORY DEVELOPMENT WORKFLOW

### Phase 1: Task Initialization (BEFORE ANY CODE)

```
1. READ PoC.md - Identify current story/task
2. CHECK beads status
3. CREATE or UPDATE bead for this task:
   beads create "Story X.X: Task Name" --status in-progress
4. ANNOUNCE to user what you're working on
5. ONLY THEN start coding
```

### Phase 2: Implementation (WITH SUB-AGENTS)

#### Step 2.1: Research & Reference (If Confidence < 90%)

**TRIGGER:** Anytime you are less than 90% confident in approach

**ACTION:**
- Use Explore sub-agent to research best practices
- Search for reference implementations
- Review documentation
- Search for common pitfalls

**EXAMPLE:**
```
User: Implement deskewing algorithm
Claude: [Confidence check: 75% - RESEARCH REQUIRED]
        [Launching Explore agent to research OpenCV deskewing techniques]
```

#### Step 2.2: Code Implementation

**RULES:**
- Write clean, documented code
- Follow type hints religiously
- Keep functions under 50 lines
- Keep files under 500 lines (see refactoring rules below)
- Use descriptive variable names
- Add docstrings to all functions/classes

**USE SUB-AGENTS FOR:**
- Complex algorithms → Plan agent first
- New modules → Explore agent for structure
- API integrations → Explore agent for docs

#### Step 2.3: Unit Test Creation (MANDATORY)

**EVERY FUNCTION MUST HAVE TESTS**

**Test Structure:**
```python
# tests/test_preprocessor.py
import pytest
from pathlib import Path
from src.agents.preprocessor import deskew_image, enhance_contrast

class TestPreprocessor:
    """Test suite for preprocessing functions."""

    @pytest.fixture
    def sample_image(self):
        """Load sample test image."""
        return cv2.imread("tests/fixtures/sample.jpg")

    def test_deskew_image_success(self, sample_image):
        """Test deskew on normal image."""
        result = deskew_image(sample_image)
        assert result is not None
        assert result.shape == sample_image.shape

    def test_deskew_image_invalid_input(self):
        """Test deskew with invalid input."""
        with pytest.raises(ValueError):
            deskew_image(None)

    def test_enhance_contrast_improves_quality(self, sample_image):
        """Test contrast enhancement increases variance."""
        enhanced = enhance_contrast(sample_image)
        assert enhanced.var() > sample_image.var()
```

**Test Coverage Requirements:**
- Minimum 80% coverage for all modules
- 100% coverage for critical paths (OCR engines, entity extraction)
- Test happy path AND edge cases
- Test error handling

#### Step 2.4: Validation & Debugging (MANDATORY)

**BEFORE MARKING TASK COMPLETE:**

1. **Run Tests:**
   ```bash
   pytest tests/ -v --cov=src --cov-report=term-missing
   ```

2. **Check Type Hints:**
   ```bash
   mypy src/
   ```

3. **Lint Code:**
   ```bash
   ruff check src/
   ```

4. **Format Code:**
   ```bash
   black src/ tests/
   ```

5. **Fix ALL Errors and Warnings:**
   - No test failures allowed
   - No type errors allowed
   - No linting errors allowed (warnings OK if documented)

6. **Manual Validation:**
   - Run the code with sample data
   - Verify output is correct
   - Check performance is acceptable

### Phase 3: Human Review Checkpoint

**TRIGGER HUMAN REVIEW FOR:**
- ✅ Completion of any user story
- ✅ Major architectural decisions
- ✅ Before refactoring existing code
- ✅ When tests fail and fix is non-obvious
- ✅ When confidence < 90% and research doesn't help
- ✅ Before marking a day's work complete

**DO NOT TRIGGER HUMAN REVIEW FOR:**
- ❌ Minor bug fixes
- ❌ Formatting changes
- ❌ Documentation updates
- ❌ Adding tests to untested code

**HOW TO REQUEST REVIEW:**
```markdown
## 🔍 Human Review Required

**Task:** Story X.X - Task Name
**Reason:** [Completion | Architectural Decision | Confidence Issue]

**What was implemented:**
- Item 1
- Item 2

**Tests:** ✅ All passing (X/X)
**Coverage:** X%
**Type Check:** ✅ No errors
**Lint:** ✅ Clean

**Questions/Concerns:**
1. [Any specific concerns]

**Ready to proceed?** [Yes/No]
```

### Phase 4: Task Completion (ONLY AFTER VALIDATION)

**COMPLETION CHECKLIST:**
- [ ] Code implemented and working
- [ ] Unit tests written and passing (100%)
- [ ] Type checking passes (mypy)
- [ ] Linting passes (ruff)
- [ ] Code formatted (black)
- [ ] Manual validation completed
- [ ] Documentation updated (if needed)
- [ ] Human review completed (if required)

**THEN AND ONLY THEN:**
```bash
# Update bead status
beads update <bead-id> --status completed

# Update PoC.md task checkbox
# Check off completed task in appropriate story

# Commit code with conventional commit
git add .
git commit -m "feat(preprocessor): implement deskewing algorithm

- Add deskew_image function with Hough transform
- Add unit tests with 95% coverage
- Fix angle detection for rotations >45 degrees

Closes: Story 2.2
Tests: All passing (12/12)
"
```

**INFORM USER:**
```markdown
✅ **Story X.X Completed: Task Name**

**Implemented:**
- Feature 1
- Feature 2

**Tests:** 12/12 passing (95% coverage)
**Validation:** All checks passed

**Next Task:** Story X.Y - Next Task Name
```

---

## 🔧 REFACTORING RULES (MANDATORY)

### File Size Limit: 500 Lines

**TRIGGER:** Any file exceeds 500 lines

**ACTION:** Immediate refactoring required before proceeding

### Refactoring Strategy

**For Large Modules:**
```
BEFORE (preprocessor.py - 800 lines):
├── All preprocessing functions in one file

AFTER:
src/agents/preprocessing/
├── __init__.py           # Public API
├── deskew.py            # Deskewing functions
├── enhancement.py       # Contrast/brightness
├── denoising.py         # Noise removal
├── segmentation.py      # Region segmentation
└── utils.py             # Shared utilities
```

**For Large Classes:**
```python
# BEFORE - Monolithic class (600 lines)
class OCREngine:
    def preprocess(self): ...
    def extract_text(self): ...
    def validate(self): ...
    def format_output(self): ...

# AFTER - Component approach
class OCREngine:
    """Main orchestrator."""
    def __init__(self):
        self.preprocessor = ImagePreprocessor()
        self.extractor = TextExtractor()
        self.validator = ResultValidator()
        self.formatter = OutputFormatter()

    def process(self, image: np.ndarray) -> OCRResult:
        """Orchestrate full pipeline."""
        preprocessed = self.preprocessor.process(image)
        text = self.extractor.extract(preprocessed)
        validated = self.validator.validate(text)
        return self.formatter.format(validated)
```

### Component Design Principles

1. **Single Responsibility:** Each file/class does ONE thing
2. **Dependency Injection:** Pass dependencies, don't create them
3. **Composition Over Inheritance:** Prefer composition
4. **Clear Interfaces:** Define protocols/abstract classes
5. **Orchestration Pattern:** One coordinator, many workers

---

## 🐛 DEBUGGING PROTOCOL

### When Errors Occur (MANDATORY STEPS)

**NEVER IGNORE ERRORS OR WARNINGS**

#### Step 1: Identify Error Type
```python
# Categorize:
# - Syntax Error → Fix immediately
# - Type Error → Check type hints
# - Runtime Error → Add error handling
# - Logic Error → Add tests and debug
# - Import Error → Check dependencies
```

#### Step 2: Research (If Non-Obvious)
```
- Use Explore agent to research error message
- Check official documentation
- Search for common solutions
- Review stack trace carefully
```

#### Step 3: Fix with Tests
```python
# 1. Write test that reproduces error
def test_bug_reproduction():
    """Reproduce the bug."""
    with pytest.raises(ValueError):
        buggy_function(invalid_input)

# 2. Fix the bug
def buggy_function(input_data):
    if input_data is None:
        raise ValueError("Input cannot be None")
    # ... rest of function

# 3. Verify test now passes
def test_bug_fixed():
    """Verify fix works."""
    result = buggy_function(valid_input)
    assert result is not None
```

#### Step 4: Prevent Recurrence
- Add type hints if type error
- Add validation if input error
- Add logging for debugging
- Document the fix

### Warning Handling

**MUST ADDRESS:**
- DeprecationWarnings (update code)
- SecurityWarnings (fix immediately)
- Performance warnings (optimize or document)

**MAY DEFER:**
- Style warnings (if not breaking code style rules)
- Info-level warnings (document why ignored)

---

## 📊 PROGRESS TRACKING (DUAL SYSTEM)

### System 1: PoC.md Task Tracking

**UPDATE AFTER EACH TASK:**
```markdown
# In PoC.md

**Story 2.1: Image Loading & Quality Assessment**
- [x] Implement `image_utils.py`
- [x] Create quality scoring function
- [x] Test with sample documents
```

### System 2: Beads Progress Tracking

**BEADS WORKFLOW:**

#### Creating a Bead
```bash
# Start new task
beads create "Story 2.1: Image Loading & Quality Assessment" \
  --status in-progress \
  --priority high \
  --estimate 2h

# This returns a bead ID, e.g., BEAD-001
```

#### Updating a Bead
```bash
# Add progress notes
beads update BEAD-001 --note "Implemented image loading, testing quality scorer"

# Change status
beads update BEAD-001 --status in-review

# After human review
beads update BEAD-001 --status completed
```

#### Viewing Beads
```bash
# See all open beads
beads status

# See specific bead
beads show BEAD-001

# See completed beads
beads list --status completed
```

#### Daily Summary
```bash
# End of day report
beads summary --today
```

### Synchronization Rule

**ALWAYS KEEP BOTH SYSTEMS IN SYNC:**
- When task starts → Create bead + mark PoC.md task in-progress
- When task completes → Complete bead + check PoC.md checkbox
- End of day → Verify both systems match

---

## 🎯 SUB-AGENT USAGE GUIDELINES

### When to Launch Sub-Agents

**ALWAYS USE SUB-AGENTS FOR:**

1. **Research & Exploration (Explore Agent)**
   - Finding best practices
   - Understanding new libraries
   - Investigating error messages
   - Comparing implementation approaches

2. **Architecture Planning (Plan Agent)**
   - Before implementing complex features
   - When refactoring large files
   - For multi-file changes
   - When creating new modules

3. **Testing & Validation**
   - Generating comprehensive test cases
   - Coverage analysis
   - Integration testing

**EXAMPLE:**
```
User: Implement the preprocessing pipeline

Claude:
1. [Launching Plan agent to design preprocessing architecture]
   ... agent returns plan ...

2. [Launching Explore agent to research OpenCV best practices]
   ... agent returns research ...

3. [Beginning implementation based on plan and research]
   ... implement code ...

4. [Creating unit tests]
   ... write tests ...

5. [Validation complete, marking task as done]
```

### Sub-Agent Orchestration

**PARALLEL vs SEQUENTIAL:**

**Parallel (if independent):**
```python
# Launch multiple research agents at once
- Research deskewing algorithms
- Research CLAHE implementation
- Research angle detection methods
```

**Sequential (if dependent):**
```python
# Must happen in order
1. Plan architecture (Plan agent)
2. Research components (Explore agent)
3. Implement code (main)
4. Test and validate (main)
```

---

## 📝 DOCUMENTATION REQUIREMENTS

### Code Documentation

**EVERY MODULE MUST HAVE:**
```python
"""Module description.

This module handles image preprocessing for OCR, including
deskewing, contrast enhancement, and noise removal.

Typical usage:
    from src.agents.preprocessing import preprocess_image

    result = preprocess_image(image, enhance=True)
"""
```

**EVERY FUNCTION MUST HAVE:**
```python
def deskew_image(
    image: np.ndarray,
    max_angle: float = 45.0
) -> Tuple[np.ndarray, float]:
    """Correct image rotation using Hough line detection.

    Detects lines in the image and calculates rotation angle,
    then applies rotation transform to straighten the image.

    Args:
        image: Input image as numpy array (grayscale or BGR)
        max_angle: Maximum rotation angle to correct in degrees

    Returns:
        Tuple of (corrected_image, detected_angle)

    Raises:
        ValueError: If image is None or empty

    Example:
        >>> img = cv2.imread("skewed.jpg")
        >>> corrected, angle = deskew_image(img)
        >>> print(f"Corrected {angle:.2f} degrees")
    """
```

### README Updates

**UPDATE README WHEN:**
- Adding new modules
- Changing setup process
- Adding new dependencies
- Changing usage patterns

---

## 🚦 CONFIDENCE THRESHOLD RULES

### When Confidence < 90%: RESEARCH REQUIRED

**CONFIDENCE ASSESSMENT:**
```
✅ >90%: Proceed with implementation
⚠️  70-90%: Quick research (5-10 min documentation review)
🔴 <70%: Deep research (Explore agent + reference implementations)
```

**WHAT TO RESEARCH:**
- Official documentation
- Best practices articles
- Reference implementations (GitHub)
- Academic papers (if algorithmic)
- Stack Overflow (for common issues)

**DOCUMENT RESEARCH:**
```markdown
## Research Notes: Deskewing Implementation

**Confidence Before:** 65%
**Research Method:** Explore agent + OpenCV docs

**Findings:**
1. Hough Line Transform is standard approach
2. minAreaRect provides good angle detection
3. Edge detection improves accuracy

**Selected Approach:** OpenCV minAreaRect method
**Confidence After:** 95%
```

---

## 🔒 QUALITY GATES (MUST PASS)

### Before Completing ANY Task

**AUTOMATED CHECKS:**
```bash
# All must pass
✅ pytest tests/ -v --cov=src --cov-report=term-missing
✅ mypy src/
✅ ruff check src/
✅ black --check src/ tests/
```

**MANUAL CHECKS:**
- [ ] Code runs without errors
- [ ] Output is correct
- [ ] Performance is acceptable (<30s for test documents)
- [ ] No security issues (no hardcoded secrets, safe file operations)
- [ ] Documentation is up to date

### Code Review Checklist

**BEFORE REQUESTING HUMAN REVIEW:**
- [ ] All tests pass
- [ ] Coverage ≥80%
- [ ] Type checking clean
- [ ] Linting clean
- [ ] Code formatted
- [ ] Documentation complete
- [ ] No TODOs or FIXMEs in code
- [ ] Git commit ready with conventional message

---

## 🎬 WORKFLOW EXAMPLE (FULL CYCLE)

### Example: Implementing Story 2.1

```
=== SESSION START ===

1. READ CLAUDE.md ✅
2. READ PoC.md → Currently on Day 2, Story 2.1
3. CHECK beads status → No active beads

=== TASK START ===

4. CREATE BEAD:
   beads create "Story 2.1: Image Loading & Quality Assessment" --status in-progress

5. ANNOUNCE TO USER:
   "Starting Story 2.1: Image Loading & Quality Assessment"

=== IMPLEMENTATION ===

6. CONFIDENCE CHECK: 85% → Quick documentation review needed

7. RESEARCH (Explore agent):
   "Research OpenCV image loading best practices"

8. IMPLEMENT CODE:
   - Create src/utils/image_utils.py
   - Add load_image() function
   - Add assess_quality() function
   - Add type hints and docstrings

9. CREATE TESTS:
   - Create tests/test_image_utils.py
   - Write test_load_image_success()
   - Write test_load_image_invalid_path()
   - Write test_assess_quality_ranges()

10. RUN TESTS:
    pytest tests/test_image_utils.py -v --cov=src/utils
    → 6/6 passing, 95% coverage ✅

11. TYPE CHECK:
    mypy src/utils/image_utils.py
    → Success: no issues ✅

12. LINT:
    ruff check src/utils/image_utils.py
    → All checks passed ✅

13. FORMAT:
    black src/utils/image_utils.py tests/test_image_utils.py
    → 2 files reformatted ✅

14. MANUAL VALIDATION:
    - Run with test images
    - Verify quality scores make sense
    → All working ✅

=== COMPLETION ===

15. UPDATE BEAD:
    beads update BEAD-001 --status completed

16. UPDATE PoC.md:
    [x] Implement `image_utils.py`
    [x] Create quality scoring function
    [x] Test with sample documents

17. GIT COMMIT:
    git add .
    git commit -m "feat(utils): implement image loading and quality assessment

    - Add load_image function with format detection
    - Add assess_quality with blur and contrast checks
    - Add comprehensive unit tests (95% coverage)
    - All type checking and linting passes

    Closes: Story 2.1
    Tests: 6/6 passing
    "

18. INFORM USER:
    "✅ Story 2.1 Completed: Image Loading & Quality Assessment

    Implemented:
    - Image loading with multiple format support
    - Quality assessment (blur, contrast, resolution)
    - Comprehensive error handling

    Tests: 6/6 passing (95% coverage)
    Validation: All checks passed

    Next Task: Story 2.2 - Preprocessing Operations"

=== WAIT FOR USER CONFIRMATION ===

User: "Looks good, proceed"

=== CONTINUE TO NEXT TASK ===
```

---

## 🚨 ANTI-PATTERNS (NEVER DO THIS)

### ❌ PROHIBITED BEHAVIORS

**NEVER:**
- ❌ Skip writing tests "I'll add tests later"
- ❌ Ignore type errors "It works anyway"
- ❌ Leave warnings unfixed "It's just a warning"
- ❌ Mark task complete before validation
- ❌ Proceed with <70% confidence without research
- ❌ Let files exceed 500 lines without refactoring
- ❌ Use deprecated syntax
- ❌ Hardcode paths or secrets
- ❌ Commit code that doesn't pass quality gates
- ❌ Move to next task without human review (when required)

**ALWAYS:**
- ✅ Write tests BEFORE marking complete
- ✅ Fix ALL errors and warnings
- ✅ Research when confidence is low
- ✅ Use sub-agents for complex tasks
- ✅ Update both PoC.md AND beads
- ✅ Request human review at checkpoints
- ✅ Follow the tech stack (no deviations)
- ✅ Use modern Python syntax
- ✅ Refactor when needed
- ✅ Document everything

---

## 📖 COMMIT MESSAGE CONVENTION

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code refactoring
- `test`: Adding tests
- `docs`: Documentation updates
- `style`: Code formatting
- `perf`: Performance improvements
- `chore`: Maintenance tasks

### Example
```
feat(ocr): implement multi-engine ensemble

- Add Tesseract, PaddleOCR, EasyOCR integration
- Implement voting mechanism for text comparison
- Add confidence scoring based on agreement
- Handle engine failures gracefully

Closes: Story 3.4
Tests: 15/15 passing (92% coverage)
Performance: 12.3s per document
```

---

## 🎯 SUCCESS CRITERIA

### You're Following This Guide If:

- ✅ Every session starts with reading CLAUDE.md and PoC.md
- ✅ Every task has a bead and is tracked in PoC.md
- ✅ Every function has tests before completion
- ✅ All quality gates pass before marking complete
- ✅ Human reviews happen at appropriate checkpoints
- ✅ Research happens when confidence < 90%
- ✅ Files never exceed 500 lines
- ✅ Modern Python syntax is used throughout
- ✅ Sub-agents are used for complex tasks
- ✅ Progress is tracked in both systems

### Red Flags (You're Not Following This Guide If):

- 🚨 Marked task complete without running tests
- 🚨 Ignored type errors or warnings
- 🚨 Implemented something with <70% confidence without research
- 🚨 File grew beyond 500 lines without refactoring
- 🚨 Used old Python syntax (os.path, %, etc.)
- 🚨 Skipped human review checkpoint
- 🚨 Updated only one tracking system
- 🚨 Proceeded to next task without completing current one

---

## 📞 COMMUNICATION TEMPLATES

### Starting a Task
```markdown
## 🔵 Starting: Story X.X - Task Name

**Bead ID:** BEAD-XXX
**Estimated Time:** Xh
**Dependencies:** [None | Story X.X]

**Plan:**
1. Step 1
2. Step 2
3. Step 3

**Beginning implementation...**
```

### Requesting Research
```markdown
## 🔍 Research Required

**Confidence:** XX%
**Topic:** [What needs research]

**Launching Explore agent to research...**
```

### Requesting Human Review
```markdown
## 🔍 Human Review Required

**Task:** Story X.X - Task Name
**Bead ID:** BEAD-XXX
**Reason:** [Completion | Decision | Issue]

**Summary:**
[What was done]

**Quality Checks:**
✅ Tests: X/X passing (XX% coverage)
✅ Type Check: Clean
✅ Lint: Clean
✅ Format: Applied
✅ Manual Test: Verified

**Ready to proceed to next task?**
```

### Completing a Task
```markdown
## ✅ Completed: Story X.X - Task Name

**Bead ID:** BEAD-XXX (marked completed)
**Time:** Xh (estimated Xh)

**Implemented:**
- Feature 1
- Feature 2
- Feature 3

**Quality Metrics:**
- Tests: X/X passing (XX% coverage)
- Type Check: ✅ Clean
- Lint: ✅ Clean
- Performance: Xs per document

**Git Commit:** [commit hash]

**Next Task:** Story X.Y - Next Task Name
```

---

## 🔄 VERSION HISTORY

- **v1.0** (2026-01-09): Initial version with full workflow specification

---

## 📌 QUICK REFERENCE CARD

```
┌─────────────────────────────────────────────────────────────┐
│                    WORKFLOW CHECKLIST                       │
├─────────────────────────────────────────────────────────────┤
│ SESSION START:                                              │
│  □ Read CLAUDE.md                                           │
│  □ Read PoC.md (check current day/story)                    │
│  □ Check beads status                                       │
│                                                             │
│ TASK START:                                                 │
│  □ Create bead (in-progress)                                │
│  □ Announce to user                                         │
│  □ Research if confidence < 90%                             │
│                                                             │
│ IMPLEMENTATION:                                             │
│  □ Write code (modern syntax, type hints)                   │
│  □ Write tests (≥80% coverage)                              │
│  □ Run pytest ✅                                            │
│  □ Run mypy ✅                                              │
│  □ Run ruff ✅                                              │
│  □ Run black ✅                                             │
│  □ Manual validation ✅                                     │
│                                                             │
│ COMPLETION:                                                 │
│  □ Request human review (if needed)                         │
│  □ Update bead (completed)                                  │
│  □ Update PoC.md (check box)                                │
│  □ Git commit (conventional format)                         │
│  □ Inform user                                              │
│                                                             │
│ REFACTORING:                                                │
│  □ File > 500 lines? → Refactor immediately                 │
│  □ Use component/orchestration pattern                      │
│                                                             │
│ ERROR HANDLING:                                             │
│  □ Never ignore errors or warnings                          │
│  □ Research if non-obvious                                  │
│  □ Add tests that reproduce the bug                         │
│  □ Fix and verify                                           │
└─────────────────────────────────────────────────────────────┘
```

---

*This document is the source of truth for all development work on the OCR project. All AI agents must follow these guidelines without deviation.*
