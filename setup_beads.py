#!/usr/bin/env python3
"""
Setup beads tasks from PoC.md plan.
Creates hierarchical task structure for the 7-day PoC.
"""

import subprocess
import time
from typing import List, Dict

# Define all tasks from PoC.md
TASKS = {
    "Day 1": {
        "title": "Day 1: Environment Setup & Foundation",
        "priority": 0,
        "stories": [
            {
                "title": "Story 1.1: Development Environment Setup",
                "tasks": [
                    "Create virtual environment",
                    "Install core dependencies",
                    "Test OCR engines",
                    "Verify libraries",
                ]
            },
            {
                "title": "Story 1.2: Project Structure Creation",
                "tasks": [
                    "Create directory structure",
                    "Create stub files",
                    "Write basic README",
                ]
            },
            {
                "title": "Story 1.3: Sample Document Collection",
                "tasks": [
                    "Find/create 5 test documents",
                    "Organize in tests/sample_documents",
                    "Create ground truth files",
                ]
            },
            {
                "title": "Story 1.4: Frontend & API Setup",
                "tasks": [
                    "Initialize Next.js project",
                    "Install FastAPI dependencies",
                    "Create FastAPI server structure",
                    "Create Next.js app structure",
                    "Test servers running",
                ]
            },
        ]
    },
    "Day 2": {
        "title": "Day 2: Preprocessing Pipeline",
        "priority": 0,
        "stories": [
            {
                "title": "Story 2.1: Image Loading & Quality Assessment",
                "tasks": [
                    "Implement image_utils.py",
                    "Create quality scoring function",
                    "Test with sample documents",
                ]
            },
            {
                "title": "Story 2.2: Preprocessing Operations",
                "tasks": [
                    "Implement deskewing",
                    "Implement contrast enhancement",
                    "Implement noise removal",
                    "Implement binarization",
                    "Create visualization function",
                ]
            },
            {
                "title": "Story 2.3: Preprocessing Pipeline Integration",
                "tasks": [
                    "Create preprocessing decision logic",
                    "Integrate with intake agent",
                    "Test all paths",
                ]
            },
        ]
    },
    "Day 3": {
        "title": "Day 3: Multi-Engine OCR Integration",
        "priority": 0,
        "stories": [
            {
                "title": "Story 3.1: Tesseract Integration",
                "tasks": [
                    "Implement TesseractOCR class",
                    "Configure PSM modes",
                    "Extract confidence scores",
                    "Test and log performance",
                ]
            },
            {
                "title": "Story 3.2: PaddleOCR Integration",
                "tasks": [
                    "Implement PaddleOCR class",
                    "Configure angle detection",
                    "Test on rotated document",
                    "Compare with Tesseract",
                ]
            },
            {
                "title": "Story 3.3: EasyOCR Integration",
                "tasks": [
                    "Implement EasyOCR class",
                    "Test on handwritten sample",
                    "Compare with other engines",
                ]
            },
            {
                "title": "Story 3.4: Multi-Engine Orchestration",
                "tasks": [
                    "Create run_all_engines function",
                    "Implement parallel execution",
                    "Collect results with metadata",
                    "Test on all samples",
                ]
            },
        ]
    },
    "Day 4": {
        "title": "Day 4: Result Ensemble & Confidence Scoring",
        "priority": 0,
        "stories": [
            {
                "title": "Story 4.1: Text Comparison & Voting",
                "tasks": [
                    "Implement text similarity comparison",
                    "Create voting mechanism",
                    "Handle merging logic",
                    "Test with disagreements",
                ]
            },
            {
                "title": "Story 4.2: Confidence Score Calculation",
                "tasks": [
                    "Implement confidence calculation",
                    "Create field-level tracking",
                    "Test calibration",
                ]
            },
            {
                "title": "Story 4.3: Error Handling & Fallback",
                "tasks": [
                    "Add try-catch blocks",
                    "Implement fallback chain",
                    "Return partial results",
                    "Log errors",
                ]
            },
            {
                "title": "Story 4.4: Baseline Testing",
                "tasks": [
                    "Implement accuracy calculation",
                    "Compare vs ground truth",
                    "Create accuracy report",
                    "Identify best engines",
                ]
            },
        ]
    },
    "Day 5": {
        "title": "Day 5: Entity Extraction & API",
        "priority": 0,
        "stories": [
            {
                "title": "Story 5.1: Regex Pattern Library",
                "tasks": [
                    "Implement patterns for dates",
                    "Implement patterns for licenses",
                    "Implement patterns for names",
                    "Implement patterns for locations",
                    "Test patterns",
                ]
            },
            {
                "title": "Story 5.2: NER Model Integration",
                "tasks": [
                    "Install spaCy",
                    "Download model",
                    "Implement NER extraction",
                    "Compare with regex",
                ]
            },
            {
                "title": "Story 5.3: Schema Mapping",
                "tasks": [
                    "Define CSV schema",
                    "Create mapping logic",
                    "Handle missing entities",
                    "Test mapping",
                ]
            },
            {
                "title": "Story 5.4: Local LLM Integration (Optional)",
                "tasks": [
                    "Install Ollama",
                    "Pull model",
                    "Create extraction prompt",
                    "Test on document",
                ]
            },
            {
                "title": "Story 5.5: FastAPI Endpoints Implementation",
                "tasks": [
                    "Implement upload endpoint",
                    "Implement status endpoint",
                    "Implement results endpoint",
                    "Add CORS middleware",
                    "Write API tests",
                ]
            },
        ]
    },
    "Day 6": {
        "title": "Day 6: Output Formatting & Frontend",
        "priority": 0,
        "stories": [
            {
                "title": "Story 6.1: CSV Generation",
                "tasks": [
                    "Implement output_formatter.py",
                    "Create CSV writer",
                    "Add confidence scores",
                    "Test with samples",
                ]
            },
            {
                "title": "Story 6.2: Validation Rules",
                "tasks": [
                    "Implement validation checks",
                    "Create validation report",
                    "Add review flags",
                ]
            },
            {
                "title": "Story 6.3: Confidence-Based Review Flagging",
                "tasks": [
                    "Implement flagging logic",
                    "Create review queue",
                    "Prioritize by confidence",
                ]
            },
            {
                "title": "Story 6.4: Logging & Metadata",
                "tasks": [
                    "Implement structured logging",
                    "Log each stage",
                    "Create summary report",
                ]
            },
            {
                "title": "Story 6.5: Next.js Frontend UI Development",
                "tasks": [
                    "Create upload page",
                    "Create results page",
                    "Create API client",
                    "Add state management",
                    "Style with Tailwind",
                    "Add error handling",
                ]
            },
        ]
    },
    "Day 7": {
        "title": "Day 7: Integration Testing & Documentation",
        "priority": 0,
        "stories": [
            {
                "title": "Story 7.1: End-to-End Pipeline & Frontend Testing",
                "tasks": [
                    "Create orchestrator script",
                    "Run CLI on all documents",
                    "Test web UI workflow",
                    "Calculate accuracy metrics",
                    "Test API endpoints",
                    "Verify CORS",
                ]
            },
            {
                "title": "Story 7.2: Edge Case Testing",
                "tasks": [
                    "Test blank page",
                    "Test illegible document",
                    "Test large document",
                    "Test wrong format",
                    "Test corrupted image",
                ]
            },
            {
                "title": "Story 7.3: Performance Benchmarking",
                "tasks": [
                    "Measure processing time",
                    "Identify bottlenecks",
                    "Create performance report",
                ]
            },
            {
                "title": "Story 7.4: Documentation & Lessons Learned",
                "tasks": [
                    "Update README",
                    "Create lessons learned doc",
                    "Document accuracy comparison",
                ]
            },
            {
                "title": "Story 7.5: Demo Preparation",
                "tasks": [
                    "Create demo script",
                    "Prepare demo documents",
                    "Record demo workflow",
                    "Prepare talking points",
                ]
            },
        ]
    },
}


def run_bd_command(args: List[str]) -> str:
    """Run bd command and return output."""
    try:
        result = subprocess.run(
            ["./bin/bd.exe"] + args,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"Error running bd command: {e}")
        return ""


def create_epic(day: str, title: str, priority: int) -> str:
    """Create a day epic and return its ID."""
    print(f"\nCreating epic: {title}")
    output = run_bd_command([
        "create",
        title,
        "-p", str(priority),
        "--status", "open"
    ])

    # Extract ID from output
    if "Created" in output:
        # Format: "Created bd-xxxx: Title"
        parts = output.split()
        for part in parts:
            if part.startswith("bd-"):
                bead_id = part.rstrip(":")
                print(f"  ✓ Created {bead_id}")
                return bead_id

    print(f"  ✗ Failed to create epic")
    return ""


def create_story(story_title: str, parent_id: str) -> str:
    """Create a story under an epic and return its ID."""
    print(f"  Creating story: {story_title}")

    if parent_id:
        output = run_bd_command([
            "create",
            story_title,
            "--parent", parent_id,
            "-p", "1",
            "--status", "open"
        ])
    else:
        output = run_bd_command([
            "create",
            story_title,
            "-p", "1",
            "--status", "open"
        ])

    # Extract ID
    if "Created" in output:
        parts = output.split()
        for part in parts:
            if part.startswith("bd-"):
                bead_id = part.rstrip(":")
                print(f"    ✓ Created {bead_id}")
                return bead_id

    print(f"    ✗ Failed to create story")
    return ""


def create_task(task_title: str, parent_id: str) -> str:
    """Create a task under a story and return its ID."""
    if not parent_id:
        return ""

    output = run_bd_command([
        "create",
        task_title,
        "--parent", parent_id,
        "-p", "2",
        "--status", "open"
    ])

    # Extract ID
    if "Created" in output:
        parts = output.split()
        for part in parts:
            if part.startswith("bd-"):
                return part.rstrip(":")

    return ""


def setup_all_beads():
    """Create all beads from PoC plan."""
    print("=" * 60)
    print("Setting up beads tasks from 7-day PoC plan")
    print("=" * 60)

    created_count = 0

    for day_key in [f"Day {i}" for i in range(1, 8)]:
        if day_key not in TASKS:
            continue

        day_data = TASKS[day_key]

        # Create epic for the day
        epic_id = create_epic(day_key, day_data["title"], day_data["priority"])
        if not epic_id:
            print(f"Skipping {day_key} due to epic creation failure")
            continue

        created_count += 1
        time.sleep(0.5)  # Rate limiting

        # Create stories under the epic
        for story_data in day_data["stories"]:
            story_id = create_story(story_data["title"], epic_id)
            if not story_id:
                continue

            created_count += 1
            time.sleep(0.3)

            # Create tasks under the story (optional detail level)
            if "tasks" in story_data and len(story_data["tasks"]) <= 5:
                for task_title in story_data["tasks"]:
                    task_id = create_task(task_title, story_id)
                    if task_id:
                        created_count += 1
                    time.sleep(0.2)

    print("\n" + "=" * 60)
    print(f"✓ Setup complete! Created {created_count} beads")
    print("=" * 60)
    print("\nRun './bin/bd.exe status' to see all tasks")
    print("Run './bin/bd.exe ready' to see tasks ready to work on")


if __name__ == "__main__":
    setup_all_beads()
