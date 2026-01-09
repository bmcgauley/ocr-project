# Beads Setup & Usage Guide
## Task Tracking System for OCR Project

---

## Overview

This project uses [Beads](https://github.com/steveyegge/beads) (command: `bd`) for distributed, git-backed task tracking. Beads provides persistent memory for AI agents and humans working on long-horizon tasks.

---

## Installation Status

✅ **Beads v0.46.0** is installed in [bin/bd.exe](bin/bd.exe)

### Quick Access

**Windows PowerShell:**
```powershell
# Use wrapper script
./bd.ps1 <command>

# Or use directly
./bin/bd.exe <command>
```

**Bash/Git Bash:**
```bash
# Use directly
./bin/bd.exe <command>

# Or create alias
alias bd='./bin/bd.exe'
```

---

## Initialization

Beads requires a Git repository (✅ initialized) and will create a `.beads/` directory for task storage.

### Initialize Beads (First Time)

```bash
# Standard initialization (with SQLite database)
./bin/bd.exe init

# Or no-database mode (JSONL only)
./bin/bd.exe init --no-db

# Stealth mode (local use only, not committed to repo)
./bin/bd.exe init --stealth
```

---

## Essential Commands

### View Tasks

```bash
# List all ready tasks (no blockers)
./bin/bd.exe ready

# Show all open tasks
./bin/bd.exe list

# Show specific task details
./bin/bd.exe show <task-id>

# Show status summary
./bin/bd.exe status
```

### Create Tasks

```bash
# Create a new task
./bin/bd.exe create "Task title"

# Create with priority (0-3, 0 is highest)
./bin/bd.exe create "Critical task" -p 0

# Create with description
./bin/bd.exe create "Task title" -d "Detailed description"

# Create with status
./bin/bd.exe create "Task title" --status in-progress
```

### Update Tasks

```bash
# Update task status
./bin/bd.exe update <task-id> --status in-progress
./bin/bd.exe update <task-id> --status completed
./bin/bd.exe update <task-id> --status blocked

# Add notes to task
./bin/bd.exe update <task-id> --note "Progress update"

# Change priority
./bin/bd.exe update <task-id> -p 1
```

### Dependencies

```bash
# Add dependency (task1 blocks task2)
./bin/bd.exe dep add <task2-id> <task1-id>

# Remove dependency
./bin/bd.exe dep rm <task2-id> <task1-id>

# Show task dependencies
./bin/bd.exe dep show <task-id>
```

### Close/Archive Tasks

```bash
# Close a completed task
./bin/bd.exe close <task-id>

# Close with reason
./bin/bd.exe close <task-id> -r "Completed successfully"

# Archive old closed tasks
./bin/bd.exe archive --older-than 30d
```

---

## Integration with PoC.md

This project uses **DUAL PROGRESS TRACKING**:
1. **Beads** - For structured task management and dependencies
2. **PoC.md** - For human-readable progress tracking

### Workflow

**When starting a task from PoC.md:**
```bash
# 1. Find the story/task in ref/PoC.md
# Example: Day 2, Story 2.1 - Image Loading & Quality Assessment

# 2. Create corresponding bead
./bin/bd.exe create "Story 2.1: Image Loading & Quality Assessment" \
  --status in-progress \
  -p 0 \
  -d "Implement image_utils.py with loading and quality assessment"

# This returns a task ID, e.g., bd-a1b2
```

**During implementation:**
```bash
# Add progress notes
./bin/bd.exe update bd-a1b2 --note "Implemented load_image function"
./bin/bd.exe update bd-a1b2 --note "Added quality scoring, ready for tests"
```

**When completing:**
```bash
# Mark as completed
./bin/bd.exe update bd-a1b2 --status completed

# Also update PoC.md checkbox
# [x] Implement `image_utils.py`
```

---

## Hierarchical Task Structure

Beads supports epic → task → subtask hierarchy:

```bash
# Create epic for a day's work
./bin/bd.exe create "Day 2: Preprocessing Pipeline" -p 0

# This creates: bd-abc1

# Create tasks under the epic
./bin/bd.exe create "Story 2.1: Image Loading" --parent bd-abc1
# Creates: bd-abc1.1

./bin/bd.exe create "Story 2.2: Preprocessing Operations" --parent bd-abc1
# Creates: bd-abc1.2

# Create subtasks
./bin/bd.exe create "Implement deskewing" --parent bd-abc1.2
# Creates: bd-abc1.2.1
```

---

## Typical Daily Workflow

### Morning (Session Start)

```bash
# Check current status
./bin/bd.exe status

# List ready tasks
./bin/bd.exe ready

# Read project docs
# 1. Read CLAUDE.md (rules)
# 2. Read ref/PoC.md (current progress)
# 3. Check beads status
```

### During Work

```bash
# Start a task
./bin/bd.exe update bd-a1b2 --status in-progress

# Add progress notes as you go
./bin/bd.exe update bd-a1b2 --note "Tests passing, coverage at 85%"

# If blocked
./bin/bd.exe update bd-a1b2 --status blocked
./bin/bd.exe update bd-a1b2 --note "Waiting for human review"
```

### Evening (End of Day)

```bash
# Generate daily summary
./bin/bd.exe summary --today

# Review open tasks
./bin/bd.exe list --status in-progress

# Sync to git (if not in stealth mode)
git add .beads/
git commit -m "chore(beads): update task progress - Day 2"
```

---

## JSON Output (For Agents)

All commands support `--json` flag for structured output:

```bash
# Get task details as JSON
./bin/bd.exe show bd-a1b2 --json

# List tasks as JSON
./bin/bd.exe list --json

# Ready tasks as JSON
./bin/bd.exe ready --json
```

**Example JSON output:**
```json
{
  "id": "bd-a1b2",
  "title": "Story 2.1: Image Loading & Quality Assessment",
  "status": "in-progress",
  "priority": 0,
  "created": "2026-01-11T10:00:00Z",
  "updated": "2026-01-11T14:30:00Z",
  "notes": [
    "Implemented load_image function",
    "Added quality scoring, ready for tests"
  ]
}
```

---

## Task Status Values

| Status | Meaning | Next Steps |
|--------|---------|------------|
| `open` | Ready to start | Begin work, change to `in-progress` |
| `in-progress` | Currently working | Continue work, add notes |
| `blocked` | Waiting on something | Note blocker, work on other tasks |
| `review` | Ready for human review | Wait for feedback |
| `completed` | Finished and validated | Close the task |
| `closed` | Archived | No action needed |

---

## Priority Levels

| Priority | Description | Use For |
|----------|-------------|---------|
| 0 | Critical | Blockers, current sprint tasks |
| 1 | High | Important, next-up tasks |
| 2 | Normal | Regular tasks (default) |
| 3 | Low | Nice-to-have, future work |

---

## Tips for AI Agents

### Starting a Session
```bash
# Always check status first
./bin/bd.exe status

# Find ready tasks (no blockers)
./bin/bd.exe ready

# If no ready tasks, list all open
./bin/bd.exe list --status open
```

### During Implementation
```bash
# Mark task as in-progress BEFORE starting
./bin/bd.exe update <id> --status in-progress

# Add notes frequently (every major milestone)
./bin/bd.exe update <id> --note "Completed X, starting Y"

# If stuck or needs review
./bin/bd.exe update <id> --status blocked
./bin/bd.exe update <id> --note "Need human input on approach"
```

### Completing Tasks
```bash
# Only after ALL quality gates pass:
# - Tests passing
# - Type checking clean
# - Linting clean
# - Manual validation done

./bin/bd.exe update <id> --status completed
./bin/bd.exe update <id> --note "All tests pass (12/12), 95% coverage"

# Then close it
./bin/bd.exe close <id>
```

---

## Synchronization with PoC.md

**RULE: Both systems must stay in sync**

### Example Sync Workflow

**PoC.md:**
```markdown
### Day 2 (Sunday, Jan 12): Preprocessing Pipeline

**Story 2.1: Image Loading & Quality Assessment**
- [x] Implement `image_utils.py`
- [x] Create quality scoring function
- [x] Test with sample documents
```

**Beads:**
```bash
# Create bead when starting story
./bin/bd.exe create "Story 2.1: Image Loading & Quality Assessment" \
  -p 0 --status in-progress

# Mark completed when story is done
./bin/bd.exe update bd-a1b2 --status completed
```

**Git Commit:**
```bash
git add src/utils/image_utils.py tests/test_image_utils.py ref/PoC.md
git commit -m "feat(utils): implement image loading and quality assessment

- Add load_image function with format detection
- Add assess_quality with blur and contrast checks
- Add comprehensive unit tests (95% coverage)

Closes: Story 2.1
Beads: bd-a1b2 completed
Tests: 6/6 passing
"
```

---

## Troubleshooting

### Beads not found
```bash
# Check if binary exists
ls -la bin/bd.exe

# If missing, download again
mkdir -p bin
cd bin
curl -L -o beads.zip https://github.com/steveyegge/beads/releases/download/v0.46.0/beads_0.46.0_windows_amd64.zip
powershell -Command "Expand-Archive -Path beads.zip -DestinationPath . -Force"
cd ..
```

### Beads not initialized
```bash
# Initialize in current directory
./bin/bd.exe init

# Or in stealth mode (local only)
./bin/bd.exe init --stealth
```

### Permission errors
```bash
# On Windows, unblock the file
powershell -Command "Unblock-File bin\bd.exe"
```

### Git not initialized
```bash
# Beads requires git
git init
git add .
git commit -m "Initial commit"

# Then initialize beads
./bin/bd.exe init
```

---

## Advanced Features

### Filtering Tasks
```bash
# Filter by status
./bin/bd.exe list --status in-progress

# Filter by priority
./bin/bd.exe list --priority 0

# Filter by assignee
./bin/bd.exe list --actor "claude"
```

### Bulk Operations
```bash
# Close multiple tasks
./bin/bd.exe close bd-a1b2 bd-a1b3 bd-a1b4

# Update multiple tasks
for task in bd-a1b2 bd-a1b3; do
  ./bin/bd.exe update $task --status completed
done
```

### Reporting
```bash
# Daily summary
./bin/bd.exe summary --today

# Weekly summary
./bin/bd.exe summary --week

# Custom date range
./bin/bd.exe summary --since "2026-01-11" --until "2026-01-17"
```

---

## References

- **Official Repo:** https://github.com/steveyegge/beads
- **Documentation:** https://github.com/steveyegge/beads/tree/main/docs
- **Agent Instructions:** https://github.com/steveyegge/beads/blob/main/AGENT_INSTRUCTIONS.md

---

## Quick Reference Card

```
┌──────────────────────────────────────────────────────────────┐
│                     BEADS QUICK REFERENCE                    │
├──────────────────────────────────────────────────────────────┤
│ CREATE TASK:                                                 │
│   ./bin/bd.exe create "Title" -p 0 --status in-progress     │
│                                                              │
│ VIEW TASKS:                                                  │
│   ./bin/bd.exe ready          # Tasks with no blockers      │
│   ./bin/bd.exe list           # All open tasks              │
│   ./bin/bd.exe status         # Summary                     │
│                                                              │
│ UPDATE TASK:                                                 │
│   ./bin/bd.exe update <id> --status in-progress            │
│   ./bin/bd.exe update <id> --note "Progress update"        │
│                                                              │
│ COMPLETE TASK:                                               │
│   ./bin/bd.exe update <id> --status completed              │
│   ./bin/bd.exe close <id>                                   │
│                                                              │
│ DEPENDENCIES:                                                │
│   ./bin/bd.exe dep add <child> <parent>                     │
│                                                              │
│ STATUS VALUES:                                               │
│   open | in-progress | blocked | review | completed | closed│
│                                                              │
│ PRIORITY LEVELS:                                             │
│   0=Critical | 1=High | 2=Normal | 3=Low                    │
└──────────────────────────────────────────────────────────────┘
```

---

*Last Updated: 2026-01-09*
