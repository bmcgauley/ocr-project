# Proof of Concept (PoC) Plan
## Free & Open-Source OCR Agent System for Historical Documents

---

## EXECUTIVE SUMMARY

This document outlines a **minimal viable PoC** using **100% free and open-source** tools to validate our hypothesis: that a systematic, agentic approach to OCR can effectively extract structured data from historical documents without relying on paid APIs.

**Timeline:** 7 days (completion target: Friday, January 17, 2026)

**Budget:** $0 (all free tools and local models)

**Success Criteria:**
- Successfully extract text from 3 different document types
- Produce structured CSV output with confidence scoring
- Demonstrate graceful handling of edge cases
- Validate the multi-agent architecture concept
- Working local web UI for document upload and result viewing

---

## HYPOTHESIS TO TEST

**Core Hypothesis:**
> A systematic, multi-stage pipeline using free OCR engines with intelligent preprocessing and fallback chains can achieve 70%+ accuracy on historical documents, sufficient to validate the approach before investing in paid APIs.

**What We're Testing:**
1. Can free OCR tools handle 1950s handwritten documents?
2. Does preprocessing significantly improve extraction quality?
3. Is the multi-agent architecture valuable, or is it over-engineered?
4. Can we extract structured entities from raw OCR output?
5. Will confidence scoring help identify review-needed documents?

**What We're NOT Testing Yet:**
- Production-scale performance
- Handling 100+ document types
- Cost optimization (everything is free)
- API reliability and fallbacks
- Full validation and human-in-the-loop workflows

---

## FREE TECHNOLOGY STACK

### Core OCR Engines (All Free)

| Tool | Use Case | Installation | Hardware Req |
|------|----------|--------------|--------------|
| **Tesseract 5.x** | Clean printed text baseline | `pip install pytesseract` | CPU only |
| **PaddleOCR** | Rotated text, mixed content | `pip install paddleocr` | CPU/GPU optional |
| **EasyOCR** | Multilingual, handwriting fallback | `pip install easyocr` | CPU/GPU optional |
| **TrOCR (Hugging Face)** | Handwritten text | `pip install transformers` | 4GB+ RAM |

### Preprocessing & CV Tools

| Tool | Purpose | Installation |
|------|---------|--------------|
| **OpenCV** | Image manipulation, deskewing | `pip install opencv-python` |
| **PIL/Pillow** | Image loading, basic ops | `pip install Pillow` |
| **NumPy** | Array operations | `pip install numpy` |
| **scikit-image** | Advanced image processing | `pip install scikit-image` |

### Entity Extraction & NLP (Free Options)

| Approach | Tool | Installation |
|----------|------|--------------|
| **Pattern Matching** | Python regex + custom rules | Built-in |
| **Local LLM (Optional)** | Ollama + Llama 3.2 3B | `brew install ollama` (Mac) or download |
| **NER Model** | spaCy (en_core_web_sm) | `pip install spacy` |

### Data & Output

| Tool | Purpose | Installation |
|------|---------|--------------|
| **Pandas** | CSV manipulation | `pip install pandas` |
| **JSON** | Structured output | Built-in |

### Frontend & API (All Free)

| Tool | Purpose | Installation | Notes |
|------|---------|--------------|-------|
| **Next.js 15** | Frontend framework | `npx create-next-app@latest` | React-based, serverless-ready |
| **FastAPI** | Python REST API | `pip install fastapi uvicorn` | Async, auto-docs, type hints |
| **Tailwind CSS** | UI styling | Included with Next.js | Utility-first CSS |
| **shadcn/ui** | Component library | `npx shadcn-ui@latest init` | Accessible, customizable |
| **Zustand** | State management | `npm install zustand` | Lightweight React state |

### Optional: Local Vision Model (If Hardware Permits)

| Model | Size | Hardware Req | Installation |
|-------|------|--------------|--------------|
| **Florence-2** | 2GB | 8GB RAM, GPU optional | Hugging Face `transformers` |
| **Qwen2-VL 7B** | 14GB | 16GB+ RAM, GPU recommended | `ollama pull qwen2-vl:7b` |

---

## SIMPLIFIED POC ARCHITECTURE

### Minimal Agent System (Not Over-Engineered)

```
┌─────────────────────────────────────────────────────────┐
│                    WEB UI (Next.js 15)                  │
│  • Document upload  • Status display  • Results viewer  │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼ (REST API)
┌─────────────────────────────────────────────────────────┐
│                    FastAPI SERVER                        │
│         • Upload endpoint  • Status  • Results           │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                    MAIN ORCHESTRATOR                    │
│              (Python script coordinator)                │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   INTAKE     │   │  EXTRACTION  │   │    OUTPUT    │
│              │   │              │   │              │
│ • Load image │   │ • Preprocess │   │ • Structure  │
│ • Classify   │   │ • Multi-OCR  │   │ • CSV export │
│ • Route      │   │ • Ensemble   │   │ • Confidence │
└──────────────┘   └──────────────┘   └──────────────┘
```

### Processing Pipeline (7 Stages)

**Stage 1: Document Intake**
- Load image (PIL/OpenCV)
- Basic quality check (resolution, format)
- Simple classification (printed vs handwritten vs mixed)

**Stage 2: Preprocessing**
- Grayscale conversion
- Deskewing (if needed)
- Contrast enhancement (CLAHE)
- Noise removal (bilateral filter)

**Stage 3: Multi-Engine OCR**
- Run in parallel:
  - Tesseract (baseline)
  - PaddleOCR (primary)
  - EasyOCR (fallback)
- Capture confidence scores from each

**Stage 4: Result Ensemble**
- Compare outputs from multiple engines
- Use voting mechanism for disagreements
- Calculate aggregate confidence score

**Stage 5: Entity Extraction**
- Regex patterns for common entities (dates, numbers, names)
- Optional: spaCy NER for person/location extraction
- Optional: Local Ollama LLM for complex extraction

**Stage 6: Schema Mapping**
- Map extracted entities to CSV columns
- Handle missing data
- Flag low-confidence fields

**Stage 7: Output & Validation**
- Generate CSV with confidence scores
- Create review flags for uncertain extractions
- Log processing metadata

**Stage 8: API Layer (FastAPI)**
- REST endpoints for document upload
- Status checking endpoints
- Results retrieval endpoints
- WebSocket for real-time progress updates

**Stage 9: Web UI (Next.js)**
- Document upload interface with drag-and-drop
- Processing status dashboard with real-time updates
- Results viewer with confidence visualization
- CSV download and review queue management

---

## 1-WEEK POC IMPLEMENTATION PLAN

### Project Management Approach: Agile Sprint Format

**Sprint Duration:** 7 days
**Daily Standup:** End of each day (self-review)
**Deliverables:** Working PoC + test results + lessons learned doc

---

### **DAY 1 (Saturday, Jan 11): Environment Setup & Foundation**

#### Epic: Project Infrastructure
**Goal:** Get all tools installed and create basic project structure

**User Stories:**

**Story 1.1: Development Environment Setup**
- **As a** developer
- **I want** all dependencies installed and tested
- **So that** I can build the pipeline without blockers
- **Tasks:**
  - [ ] Create virtual environment (`python -m venv venv`)
  - [ ] Install core dependencies (see requirements.txt below)
  - [ ] Test each OCR engine with a simple image
  - [ ] Verify OpenCV and image processing libraries
- **Acceptance Criteria:**
  - All imports work without errors
  - Sample OCR test produces text output
- **Estimated Time:** 3 hours

**Story 1.2: Project Structure Creation**
- **As a** developer
- **I want** organized code structure
- **So that** components are modular and maintainable
- **Tasks:**
  - [ ] Create directory structure:
    ```
    ocr-project/
    ├── src/
    │   ├── agents/
    │   │   ├── intake.py
    │   │   ├── preprocessor.py
    │   │   ├── ocr_engine.py
    │   │   ├── entity_extractor.py
    │   │   └── output_formatter.py
    │   ├── utils/
    │   │   ├── image_utils.py
    │   │   └── validation.py
    │   └── orchestrator.py
    ├── tests/
    │   └── sample_documents/
    ├── output/
    ├── requirements.txt
    └── README.md
    ```
  - [ ] Create stub files for each module
  - [ ] Write basic README with setup instructions
- **Acceptance Criteria:**
  - Clean project structure exists
  - All modules can be imported
- **Estimated Time:** 1 hour

**Story 1.3: Sample Document Collection**
- **As a** tester
- **I want** diverse test documents
- **So that** I can validate different scenarios
- **Tasks:**
  - [ ] Find/create 5 test documents:
    1. Clean printed text
    2. Handwritten note
    3. Mixed content
    4. Degraded/faded document
    5. Rotated text
  - [ ] Organize in `tests/sample_documents/`
  - [ ] Create ground truth text files for validation
- **Acceptance Criteria:**
  - 5 test documents ready
  - Ground truth files created
- **Estimated Time:** 2 hours

**Story 1.4: Frontend & API Setup**
- **As a** developer
- **I want** Next.js and FastAPI boilerplate ready
- **So that** I can build the web UI in parallel with backend
- **Tasks:**
  - [ ] Initialize Next.js project: `npx create-next-app@latest frontend --typescript --tailwind --app`
  - [ ] Install FastAPI and dependencies: `pip install fastapi uvicorn python-multipart`
  - [ ] Create basic FastAPI server structure:
    ```
    src/
    ├── api/
    │   ├── main.py              # FastAPI app
    │   ├── routes/
    │   │   ├── upload.py        # Document upload
    │   │   ├── status.py        # Processing status
    │   │   └── results.py       # Results retrieval
    │   └── models/
    │       └── schemas.py       # Pydantic models
    ```
  - [ ] Create Next.js app structure:
    ```
    frontend/
    ├── src/
    │   ├── app/
    │   │   ├── page.tsx         # Home/upload page
    │   │   ├── results/
    │   │   │   └── page.tsx     # Results page
    │   │   └── layout.tsx       # Root layout
    │   ├── components/          # Reusable components
    │   └── lib/                 # Utilities
    ```
  - [ ] Test FastAPI server runs: `uvicorn src.api.main:app --reload`
  - [ ] Test Next.js runs: `npm run dev`
- **Acceptance Criteria:**
  - FastAPI server starts on http://localhost:8000
  - Next.js app runs on http://localhost:3000
  - Both have basic "Hello World" responses
- **Estimated Time:** 2 hours

**Daily Goal:** ✅ Fully functional development environment with test data and running frontend/API

---

### **DAY 2 (Sunday, Jan 12): Preprocessing Pipeline**

#### Epic: Image Preprocessing
**Goal:** Build robust preprocessing that improves OCR quality

**User Stories:**

**Story 2.1: Image Loading & Quality Assessment**
- **As a** preprocessor
- **I want** to load and assess image quality
- **So that** I can decide preprocessing strategy
- **Tasks:**
  - [ ] Implement `image_utils.py`:
    - Load image (handle multiple formats)
    - Check resolution
    - Assess quality (blur detection, contrast check)
  - [ ] Create quality scoring function (0-10 scale)
  - [ ] Test with sample documents
- **Acceptance Criteria:**
  - All test images load successfully
  - Quality scores seem reasonable
- **Estimated Time:** 2 hours

**Story 2.2: Preprocessing Operations**
- **As a** preprocessor
- **I want** image enhancement functions
- **So that** OCR engines get optimal input
- **Tasks:**
  - [ ] Implement in `preprocessor.py`:
    - Grayscale conversion
    - Deskewing (Hough transform + rotation)
    - Contrast enhancement (CLAHE)
    - Noise removal (bilateral filter)
    - Binarization (adaptive thresholding)
  - [ ] Create before/after visualization function
  - [ ] Test each operation individually
- **Acceptance Criteria:**
  - Each preprocessing step works
  - Visual improvements visible
- **Estimated Time:** 4 hours

**Story 2.3: Preprocessing Pipeline Integration**
- **As a** system
- **I want** adaptive preprocessing based on image quality
- **So that** processing is efficient and effective
- **Tasks:**
  - [ ] Create preprocessing decision logic:
    - High quality (>7) → minimal processing
    - Medium quality (4-7) → standard pipeline
    - Low quality (<4) → full enhancement
  - [ ] Integrate with intake agent
  - [ ] Test all three paths
- **Acceptance Criteria:**
  - Different quality images get appropriate processing
  - Pipeline completes without errors
- **Estimated Time:** 2 hours

**Daily Goal:** ✅ Working preprocessing pipeline that visibly improves image quality

---

### **DAY 3 (Monday, Jan 13): Multi-Engine OCR Integration**

#### Epic: OCR Engine Layer
**Goal:** Integrate multiple free OCR engines and capture outputs

**User Stories:**

**Story 3.1: Tesseract Integration**
- **As a** OCR agent
- **I want** Tesseract working with confidence scores
- **So that** I have a baseline OCR engine
- **Tasks:**
  - [ ] Implement `ocr_engine.py` - TesseractOCR class
  - [ ] Configure for best quality (psm modes)
  - [ ] Extract confidence scores per word/line
  - [ ] Test on all 5 sample documents
  - [ ] Log performance metrics
- **Acceptance Criteria:**
  - Text extraction works
  - Confidence scores captured
  - Performance logged
- **Estimated Time:** 2 hours

**Story 3.2: PaddleOCR Integration**
- **As a** OCR agent
- **I want** PaddleOCR for rotated/mixed content
- **So that** I can handle complex layouts
- **Tasks:**
  - [ ] Implement PaddleOCR class in `ocr_engine.py`
  - [ ] Configure angle detection
  - [ ] Test on rotated document
  - [ ] Compare results with Tesseract
- **Acceptance Criteria:**
  - PaddleOCR extracts text
  - Handles rotation automatically
- **Estimated Time:** 2 hours

**Story 3.3: EasyOCR Integration**
- **As a** OCR agent
- **I want** EasyOCR as fallback for handwriting
- **So that** I have multiple extraction attempts
- **Tasks:**
  - [ ] Implement EasyOCR class
  - [ ] Test on handwritten sample
  - [ ] Compare with other engines
- **Acceptance Criteria:**
  - EasyOCR provides alternative extraction
- **Estimated Time:** 1 hour

**Story 3.4: Multi-Engine Orchestration**
- **As a** system
- **I want** to run all engines and collect results
- **So that** I can ensemble the outputs
- **Tasks:**
  - [ ] Create `run_all_engines()` function
  - [ ] Parallel execution (threading or async)
  - [ ] Collect results with metadata:
    ```python
    {
      "engine": "tesseract",
      "text": "extracted text...",
      "confidence": 0.87,
      "processing_time": 1.2
    }
    ```
  - [ ] Test on all samples
- **Acceptance Criteria:**
  - All engines run on each document
  - Results properly structured
- **Estimated Time:** 3 hours

**Daily Goal:** ✅ Three OCR engines working and producing comparable outputs

---

### **DAY 4 (Tuesday, Jan 14): Result Ensemble & Confidence Scoring**

#### Epic: OCR Output Processing
**Goal:** Combine multiple OCR results intelligently

**User Stories:**

**Story 4.1: Text Comparison & Voting**
- **As a** ensemble agent
- **I want** to compare outputs from multiple engines
- **So that** I can select the most reliable text
- **Tasks:**
  - [ ] Implement text similarity comparison (Levenshtein distance)
  - [ ] Create voting mechanism:
    - If 2+ engines agree → use agreed text
    - If all disagree → use highest confidence
  - [ ] Handle word-level vs line-level merging
  - [ ] Test with documents where engines disagree
- **Acceptance Criteria:**
  - Ensemble output is as good or better than individual engines
  - Confidence scores reflect agreement level
- **Estimated Time:** 3 hours

**Story 4.2: Confidence Score Calculation**
- **As a** validation agent
- **I want** meaningful confidence scores
- **So that** users know what to trust
- **Tasks:**
  - [ ] Implement confidence calculation:
    ```python
    confidence = (
      engine_confidence * 0.4 +
      agreement_score * 0.3 +
      pattern_match_score * 0.3
    )
    ```
  - [ ] Create field-level confidence tracking
  - [ ] Test confidence calibration (do high scores = accurate?)
- **Acceptance Criteria:**
  - Confidence scores range 0-1
  - Higher scores correlate with accuracy
- **Estimated Time:** 2 hours

**Story 4.3: Error Handling & Fallback**
- **As a** system
- **I want** graceful handling of OCR failures
- **So that** the pipeline never crashes
- **Tasks:**
  - [ ] Add try-catch blocks for each engine
  - [ ] Implement fallback chain (if one fails, try next)
  - [ ] Return partial results if needed
  - [ ] Log all errors
- **Acceptance Criteria:**
  - System handles engine failures
  - Always produces some output
- **Estimated Time:** 2 hours

**Story 4.4: Baseline Testing**
- **As a** tester
- **I want** to measure accuracy vs ground truth
- **So that** I know how well the system works
- **Tasks:**
  - [ ] Implement accuracy calculation (character error rate)
  - [ ] Compare against ground truth files
  - [ ] Create accuracy report per document
  - [ ] Identify which engine works best for each type
- **Acceptance Criteria:**
  - Accuracy metrics calculated
  - Report generated
- **Estimated Time:** 1 hour

**Daily Goal:** ✅ Ensemble system that combines OCR outputs intelligently with confidence scoring

---

### **DAY 5 (Wednesday, Jan 15): Entity Extraction & Structuring**

#### Epic: Structured Data Extraction
**Goal:** Extract structured entities from raw OCR text

**User Stories:**

**Story 5.1: Regex Pattern Library**
- **As a** entity extractor
- **I want** patterns for common entity types
- **So that** I can extract structured data
- **Tasks:**
  - [ ] Implement `entity_extractor.py` with patterns for:
    - Dates (MM/DD/YYYY, Month DD, YYYY, etc.)
    - License/permit numbers
    - Names (Title + First + Last)
    - Locations (City, County, State)
    - Quantities (numbers + units)
  - [ ] Test each pattern individually
  - [ ] Create pattern testing suite
- **Acceptance Criteria:**
  - Patterns extract entities from test documents
  - False positives minimized
- **Estimated Time:** 3 hours

**Story 5.2: NER Model Integration (Optional)**
- **As a** entity extractor
- **I want** spaCy NER for person/location extraction
- **So that** I have ML-based entity recognition
- **Tasks:**
  - [ ] Install spaCy: `pip install spacy`
  - [ ] Download model: `python -m spacy download en_core_web_sm`
  - [ ] Implement NER extraction
  - [ ] Compare with regex patterns
- **Acceptance Criteria:**
  - NER extracts persons and locations
  - Combines with regex results
- **Estimated Time:** 2 hours

**Story 5.3: Schema Mapping**
- **As a** output formatter
- **I want** to map entities to CSV columns
- **So that** output is structured
- **Tasks:**
  - [ ] Define CSV schema (based on water rights example):
    ```csv
    document_id,license_number,issue_date,licensee_name,
    location,water_source,quantity,confidence,review_flag
    ```
  - [ ] Create mapping logic (entity type → column)
  - [ ] Handle missing entities (empty fields)
  - [ ] Test mapping with extracted entities
- **Acceptance Criteria:**
  - Entities map to correct columns
  - Missing data handled gracefully
- **Estimated Time:** 2 hours

**Story 5.4: Local LLM Integration (Stretch Goal)**
- **As a** entity extractor
- **I want** local LLM for complex extraction
- **So that** I can handle ambiguous cases
- **Tasks:**
  - [ ] Install Ollama
  - [ ] Pull Llama 3.2 3B model
  - [ ] Create structured extraction prompt
  - [ ] Test on complex document
- **Acceptance Criteria:**
  - LLM extracts entities from prompt
  - Results comparable to regex/NER
- **Estimated Time:** 2 hours (if hardware permits)

**Story 5.5: FastAPI Endpoints Implementation**
- **As a** API developer
- **I want** REST endpoints for document processing
- **So that** the frontend can interact with the OCR pipeline
- **Tasks:**
  - [ ] Implement upload endpoint (`POST /api/upload`)
    - Accept file upload (multipart/form-data)
    - Validate file type and size
    - Return document ID and status
  - [ ] Implement status endpoint (`GET /api/status/{doc_id}`)
    - Return processing status (queued/processing/completed/failed)
    - Return progress percentage
  - [ ] Implement results endpoint (`GET /api/results/{doc_id}`)
    - Return extracted data as JSON
    - Include confidence scores
    - Include CSV download link
  - [ ] Add CORS middleware for Next.js frontend
  - [ ] Write API tests with pytest
- **Acceptance Criteria:**
  - All endpoints work and return correct data
  - CORS allows frontend requests
  - API auto-docs available at /docs
- **Estimated Time:** 3 hours

**Daily Goal:** ✅ Entity extraction working with structured CSV output + API endpoints ready

---

### **DAY 6 (Thursday, Jan 16): Output Formatting & Validation**

#### Epic: Output Layer
**Goal:** Generate production-quality CSV output with validation

**User Stories:**

**Story 6.1: CSV Generation**
- **As a** output formatter
- **I want** clean CSV output with confidence scores
- **So that** results are immediately usable
- **Tasks:**
  - [ ] Implement `output_formatter.py`
  - [ ] Create CSV writer with pandas
  - [ ] Add confidence scores per field
  - [ ] Add document-level metadata
  - [ ] Test with all sample documents
- **Acceptance Criteria:**
  - CSV format is correct
  - Opens in Excel/Google Sheets
  - All fields populated or marked as missing
- **Estimated Time:** 2 hours

**Story 6.2: Validation Rules**
- **As a** validator
- **I want** to check data quality
- **So that** I can flag issues
- **Tasks:**
  - [ ] Implement validation checks:
    - Date format validation
    - Number range checks
    - Required field checks
    - Cross-field validation (e.g., date logic)
  - [ ] Create validation report
  - [ ] Add review flags to output
- **Acceptance Criteria:**
  - Invalid data is flagged
  - Validation report is helpful
- **Estimated Time:** 2 hours

**Story 6.3: Confidence-Based Review Flagging**
- **As a** system
- **I want** to flag low-confidence extractions
- **So that** humans know what to review
- **Tasks:**
  - [ ] Implement flagging logic:
    - Field confidence < 0.7 → flag field
    - Document confidence < 0.6 → flag document
    - Any validation failure → flag
  - [ ] Create review queue output (separate CSV or JSON)
  - [ ] Prioritize by confidence (lowest first)
- **Acceptance Criteria:**
  - Review flags are accurate
  - Priority ordering makes sense
- **Estimated Time:** 2 hours

**Story 6.4: Logging & Metadata**
- **As a** developer
- **I want** detailed processing logs
- **So that** I can debug and improve the system
- **Tasks:**
  - [ ] Implement structured logging (JSON format)
  - [ ] Log for each stage:
    - Document ID
    - Processing time
    - Engines used
    - Confidence scores
    - Errors/warnings
  - [ ] Create processing summary report
- **Acceptance Criteria:**
  - Logs are detailed and useful
  - Summary report shows key metrics
- **Estimated Time:** 2 hours

**Story 6.5: Next.js Frontend UI Development**
- **As a** user
- **I want** a web interface to upload documents and view results
- **So that** I can easily interact with the OCR system
- **Tasks:**
  - [ ] Create upload page (`app/page.tsx`):
    - Drag-and-drop file upload component
    - File preview before processing
    - Submit button to start OCR
  - [ ] Create results page (`app/results/[id]/page.tsx`):
    - Display processing status with progress indicator
    - Show extracted data in readable format
    - Display confidence scores with visual indicators (green/yellow/red)
    - Show review flags and warnings
    - CSV download button
  - [ ] Create API client (`lib/api.ts`):
    - Upload function
    - Status polling function
    - Results fetching function
  - [ ] Add state management with Zustand:
    - Upload state
    - Processing status
    - Results data
  - [ ] Style with Tailwind CSS and shadcn/ui components
  - [ ] Add error handling and loading states
- **Acceptance Criteria:**
  - Can upload documents via web UI
  - Processing status updates in real-time
  - Results display correctly with confidence visualization
  - CSV downloads work
  - UI is responsive and user-friendly
- **Estimated Time:** 4 hours

**Daily Goal:** ✅ Complete pipeline producing validated CSV output + working web UI

---

### **DAY 7 (Friday, Jan 17): Integration Testing & Documentation**

#### Epic: Final Testing & Deliverables
**Goal:** End-to-end testing and documentation of PoC

**User Stories:**

**Story 7.1: End-to-End Pipeline & Frontend Integration Testing**
- **As a** tester
- **I want** to run the full pipeline on all test documents via both CLI and web UI
- **So that** I can verify everything works end-to-end
- **Tasks:**
  - [ ] Create main orchestrator script
  - [ ] Run on all 5 test documents via CLI
  - [ ] Test full workflow via web UI:
    - Upload document through UI
    - Monitor processing status
    - View results in browser
    - Download CSV
  - [ ] Compare outputs with ground truth
  - [ ] Calculate accuracy metrics:
    - Character error rate (CER)
    - Word error rate (WER)
    - Entity extraction accuracy
    - Processing time per document
  - [ ] Test API endpoints with curl/Postman
  - [ ] Verify CORS and error handling
  - [ ] Document any failures
- **Acceptance Criteria:**
  - All documents process successfully via CLI
  - Web UI successfully uploads and displays results
  - API endpoints work correctly
  - Metrics documented
  - Failure cases understood
- **Estimated Time:** 3 hours

**Story 7.2: Edge Case Testing**
- **As a** tester
- **I want** to test edge cases
- **So that** I know system limitations
- **Tasks:**
  - [ ] Test edge cases:
    - Blank page
    - Completely illegible document
    - Very large document
    - Wrong file format
    - Corrupted image
  - [ ] Verify graceful handling
  - [ ] Document behavior for each case
- **Acceptance Criteria:**
  - No crashes on edge cases
  - Appropriate error messages/outputs
- **Estimated Time:** 2 hours

**Story 7.3: Performance Benchmarking**
- **As a** developer
- **I want** performance metrics
- **So that** I can identify bottlenecks
- **Tasks:**
  - [ ] Measure processing time per stage
  - [ ] Identify slowest components
  - [ ] Calculate cost per document (all free, but time matters)
  - [ ] Create performance report
- **Acceptance Criteria:**
  - Performance data collected
  - Bottlenecks identified
- **Estimated Time:** 1 hour

**Story 7.4: Documentation & Lessons Learned**
- **As a** team member
- **I want** comprehensive documentation
- **So that** others can use and improve the system
- **Tasks:**
  - [ ] Update README with:
    - Setup instructions
    - Usage examples
    - Architecture overview
    - Known limitations
  - [ ] Create "Lessons Learned" document:
    - What worked well
    - What didn't work
    - Comparison: free vs paid APIs
    - Recommendations for next phase
  - [ ] Document accuracy comparison:
    - Per engine
    - Ensemble vs individual
    - Per document type
- **Acceptance Criteria:**
  - Documentation is clear and complete
  - Lessons learned captured
  - Recommendations actionable
- **Estimated Time:** 2 hours

**Story 7.5: Demo Preparation (CLI + Web UI)**
- **As a** presenter
- **I want** a working demo via both CLI and web interface
- **So that** I can showcase the full PoC capabilities
- **Tasks:**
  - [ ] Create demo script for both interfaces
  - [ ] Prepare demo documents (1 easy, 1 hard)
  - [ ] Create before/after visuals
  - [ ] Record or prepare live demo workflow:
    - Start FastAPI server
    - Start Next.js frontend
    - Upload document via web UI
    - Show real-time status updates
    - Display results with confidence scores
    - Download CSV
  - [ ] Prepare talking points:
    - Full-stack architecture (Next.js + FastAPI + OCR pipeline)
    - What we built in 7 days
    - What we learned
    - Free vs paid trade-offs
    - Next steps (serverless deployment, GitHub Actions, etc.)
- **Acceptance Criteria:**
  - Demo runs smoothly on both CLI and web UI
  - Key points are clear
  - Web UI demo is impressive and user-friendly
- **Estimated Time:** 1 hour

**Daily Goal:** ✅ Fully tested PoC with documentation and demo ready

---

## REQUIREMENTS.TXT

```txt
# Core Dependencies
python>=3.9

# OCR Engines
pytesseract>=0.3.10
paddleocr>=2.7.0
easyocr>=1.7.0
transformers>=4.30.0  # For TrOCR

# Image Processing
opencv-python>=4.8.0
Pillow>=10.0.0
numpy>=1.24.0
scikit-image>=0.21.0

# NLP & Entity Extraction
spacy>=3.6.0
# Run after install: python -m spacy download en_core_web_sm

# Data Handling
pandas>=2.0.0

# API & Web Server
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
python-multipart>=0.0.6  # For file uploads
pydantic>=2.5.0

# Testing
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-mock>=3.12.0
pytest-asyncio>=0.23.0  # For async API tests
httpx>=0.26.0  # For API testing

# Code Quality
black>=23.12.0
ruff>=0.1.11
mypy>=1.8.0

# Logging
loguru>=0.7.2

# Utilities
python-Levenshtein>=0.21.0  # For text comparison
tqdm>=4.65.0  # Progress bars

# Optional: Local LLM
# ollama (install separately: https://ollama.ai)
```

**Frontend Dependencies (package.json):**
```json
{
  "dependencies": {
    "next": "^15.0.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "zustand": "^4.5.0",
    "axios": "^1.6.5"
  },
  "devDependencies": {
    "@types/node": "^20",
    "@types/react": "^19",
    "@types/react-dom": "^19",
    "typescript": "^5",
    "tailwindcss": "^3.4.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0"
  }
}
```

---

## SUCCESS METRICS

### Minimum Viable PoC Success Criteria

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| **Extraction Success Rate** | ≥80% | 4/5 test documents extract text |
| **Printed Text Accuracy** | ≥85% | CER on clean printed document |
| **Handwriting Accuracy** | ≥50% | CER on handwritten document (baseline) |
| **Processing Time** | <30 sec/page | Average across all documents |
| **No Crashes** | 100% | System handles all edge cases |
| **CSV Output Valid** | 100% | All outputs are valid CSV format |
| **Confidence Calibration** | Correlation >0.7 | High confidence = high accuracy |

### Qualitative Success Indicators

**Backend:**
- [ ] Preprocessing visibly improves image quality
- [ ] Ensemble results are better than single-engine
- [ ] Entity extraction finds key data (dates, names, numbers)
- [ ] Review flags correctly identify low-quality extractions
- [ ] System is understandable and maintainable

**Frontend & API:**
- [ ] Web UI is intuitive and easy to use
- [ ] File upload works smoothly with drag-and-drop
- [ ] Processing status updates in real-time
- [ ] Results display is clear and informative
- [ ] Confidence visualization helps identify issues
- [ ] API endpoints are well-documented and functional

---

## EXPECTED OUTCOMES & LEARNINGS

### What We Expect to Learn

**1. Free Tool Viability**
- Can Tesseract/PaddleOCR/EasyOCR handle historical documents?
- How does accuracy compare to paid APIs (from research)?
- What are the hard limits of free tools?

**2. Preprocessing Value**
- Does preprocessing significantly improve accuracy?
- Which preprocessing steps have biggest impact?
- Is it worth the added complexity?

**3. Architecture Validation**
- Does multi-agent approach provide value?
- Is it over-engineered for the task?
- Would a simpler script suffice?

**4. Entity Extraction Approach**
- Are regex patterns sufficient?
- Do we need NER models?
- Is a local LLM necessary?

**5. Confidence Scoring**
- Can we calculate meaningful confidence without paid APIs?
- Do confidence scores help identify errors?
- What threshold should trigger human review?

### Likely Discoveries

**Expected Strengths:**
- Free tools will handle clean printed text well (≥85% accuracy)
- Preprocessing will significantly help degraded documents
- Ensemble approach will improve overall accuracy
- System will be more robust than single-engine approach

**Expected Weaknesses:**
- Handwriting accuracy will be poor (50-70% at best)
- No contextual reasoning (unlike GPT-4o/Mistral)
- Slower processing than cloud APIs
- Manual pattern creation is tedious

### Decision Points After PoC

Based on results, decide:

1. **If accuracy ≥70% on test set:**
   - ✅ Free approach is viable for certain document types
   - Continue with free tools, add more preprocessing
   - Consider paid APIs only for handwriting

2. **If accuracy 50-70%:**
   - ⚠️ Hybrid approach recommended
   - Use free tools for printed text
   - Use paid APIs (Mistral/GPT-4o) for handwriting only
   - Cost optimization strategy

3. **If accuracy <50%:**
   - ❌ Free tools insufficient
   - Pivot to paid API strategy
   - Use research document recommendations
   - Budget for Mistral OCR + GPT-4o fallback

---

## RISK MITIGATION

### PoC-Specific Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Free tools can't handle handwriting | High | Medium | Accept limitation, focus on printed text baseline |
| Installation issues with dependencies | Medium | Low | Use virtual environment, document all install steps |
| Processing too slow for demo | Medium | Low | Optimize or use smaller test set |
| Accuracy too low to validate hypothesis | Medium | High | Carefully select test documents (start easier) |
| Scope creep (trying to do too much) | High | Medium | Stick to minimal plan, defer features |
| One engine doesn't install | Low | Low | Have 2 working engines minimum |

### Scope Control

**In Scope (Must Have):**
- ✅ Basic preprocessing
- ✅ 2+ OCR engines working
- ✅ CSV output
- ✅ Confidence scoring

**Nice to Have (If Time Permits):**
- ⭐ Third OCR engine
- ⭐ NER model
- ⭐ Local LLM integration
- ⭐ Advanced preprocessing

**Out of Scope (Defer to Later):**
- ❌ Production deployment
- ❌ API development
- ❌ UI/web interface
- ❌ Batch processing optimization
- ❌ Full multi-agent framework (CrewAI/LangChain)

---

## DELIVERABLES CHECKLIST

### Code Deliverables
- [ ] Working Python pipeline (orchestrator + agents)
- [ ] All dependencies documented in requirements.txt
- [ ] Test suite with 5 sample documents
- [ ] Ground truth files for validation

### Documentation Deliverables
- [ ] Updated README with setup/usage instructions
- [ ] Architecture diagram (simple flowchart)
- [ ] Lessons Learned document
- [ ] Accuracy comparison report
- [ ] Recommendations for next phase

### Demonstration Deliverables
- [ ] Working demo (2-3 minutes)
- [ ] Before/after preprocessing examples
- [ ] CSV output examples
- [ ] Accuracy metrics slide/document

---

## POST-POC NEXT STEPS

### If PoC Succeeds

**Immediate Actions:**
1. Expand test set to 20+ documents
2. Fine-tune preprocessing for specific document types
3. Investigate TrOCR fine-tuning (with labeled data)
4. Test Florence-2 or Qwen2-VL if hardware available

**Medium-Term (Week 2-3):**
1. Implement proper agent framework (if validated)
2. Add more sophisticated entity extraction
3. Create human review interface
4. Test on competition sample documents (if available)

**Strategic Decision:**
- Compare PoC results with research benchmarks
- Decide on free vs paid API strategy
- Budget allocation if paid APIs needed

### If PoC Reveals Issues

**Pivot Strategies:**
1. **If handwriting is the main issue:**
   - Use free tools for printed text only
   - Budget for Mistral OCR specifically for handwriting

2. **If overall accuracy is low:**
   - Invest in better preprocessing
   - Consider fine-tuning TrOCR on domain data
   - Evaluate paid API necessity

3. **If complexity is too high:**
   - Simplify architecture
   - Focus on single best engine + preprocessing

---

## APPENDIX: DAILY STANDUP TEMPLATE

Use this at the end of each day to track progress:

### Daily Review Format

**Date:** [Day X]

**Completed Today:**
- [ ] Story X.X - Brief description

**Challenges Encountered:**
- Issue 1
- Issue 2

**Solutions Applied:**
- Solution to issue 1

**Tomorrow's Focus:**
- Top priority for next day

**Blockers:**
- Any impediments

**Learnings:**
- Key insights from today

---

## CONCLUSION

This PoC plan provides a **realistic, achievable path** to validate our hypothesis using **100% free tools** within **7 days**. By focusing on a minimal viable system and deferring nice-to-have features, we can test the core concepts without over-engineering.

**The key insight:** This PoC will tell us whether free tools are sufficient, or if we need to invest in paid APIs. Either way, we'll have validated the multi-engine, preprocessing-heavy approach before building the full system.

**Next Friday's Success:** A working demo showing that systematic OCR with free tools can extract structured data from historical documents, with clear documentation of accuracy, limitations, and recommendations for the production system.

---

*Document Version: 1.0*
*Created: January 9, 2026*
*Target Completion: January 17, 2026*
