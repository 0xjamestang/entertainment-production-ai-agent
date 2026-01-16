# Ralph Wiggum Autonomous Loop System + Entertainment Production Agent

## Overview
A production-ready autonomous agent system combining:
1. **Ralph Wiggum Loop**: Autonomous iteration framework with test-driven development and self-correction
2. **Entertainment Production Agent**: Complete short-form video production pipeline from script to post-production advisory

## Current Status
**✅ PRODUCTION READY - All 114 Tests Passing**

Both systems are fully implemented, tested, and operational.

## System Architecture

### Ralph Wiggum Autonomous Loop
File-based autonomous iteration system that continuously works toward goals, enforces testing, and self-corrects.

**Core Components:**
- `loop/state.md` - Single source of truth for loop state
- `loop/agent-prompt.md` - Output structure and behavior rules
- `loop/last_output.md` - Most recent iteration report
- `src/loop_controller.py` - Loop orchestration and mode detection
- `src/state_parser.py` - State file parsing
- `src/state_writer.py` - Atomic state updates
- `src/report_generator.py` - Iteration report generation

**Operating Modes:**
- **Engineering Mode**: Make incremental changes, run tests, fix failures, loop until green
- **Creative Mode**: Execute creative tasks when all tests pass
- **Blocked Mode**: Stop when critical issues prevent progress

### Entertainment Production Agent
Complete workflow for short-form video production (TikTok, YouTube Shorts, etc.)

**Pipeline Stages:**
1. **Script Generation** (`src/models/script.py`, `src/generators/script_generator.py`)
   - Genre-aware script creation
   - Platform-specific pacing (hook in first 3-5 seconds)
   - Character, scene, and dialogue modeling
   - Production cost flagging (night scenes, VFX, extras)

2. **Script Breakdown** (`src/models/breakdown.py`, `src/generators/breakdown_generator.py`)
   - Production element extraction (cast, props, wardrobe, locations)
   - Setup time estimation
   - CSV and JSON export
   - 1:1 scene-to-breakdown mapping validation

3. **Storyboard & Shot List** (`src/models/storyboard.py`, `src/generators/storyboard_generator.py`)
   - Shot-by-shot visual planning
   - Camera angles and movements
   - Duration distribution
   - Spatial continuity checking
   - Markdown and CSV export

4. **Production Advisory** (`src/models/advisory.py`, `src/generators/advisory_generator.py`)
   - Continuity risk identification
   - Audio capture recommendations
   - Coverage suggestions
   - Actionable production guidance

5. **Post-Production Advisory**
   - Editing rhythm and pacing
   - Platform-specific optimization (TikTok, YouTube Shorts)
   - Common revision pitfalls
   - Sound, color, and subtitle guidelines

**Workflow Orchestration:**
- `src/workflow/entertainment_workflow.py` - End-to-end pipeline execution
- Validation at each stage
- Graceful error handling
- Complete file output package

## Quick Start

### Run Demo Production
```bash
py demo_production.py
```

This generates a complete production package:
- Script (JSON)
- Breakdown (JSON + CSV)
- Storyboard (Markdown)
- Shot List (CSV)
- Production Notes (Markdown)
- Post-Production Notes (Markdown)

### Run Tests
```bash
# All tests
py -m pytest tests/ -v

# Specific component
py -m pytest tests/workflow/ -v
py -m pytest tests/generators/ -v
py -m pytest tests/models/ -v
```

### Execute Autonomous Loop
```bash
py run_loop.py
```

## Test Coverage

**114 Tests - 100% Passing**

- Loop System: 29 tests
  - State parsing: 7 tests
  - Report generation: 6 tests
  - State writing: 6 tests
  - Loop controller: 10 tests

- Script Generation: 23 tests
  - Script models: 15 tests
  - Script generator: 8 tests

- Breakdown: 21 tests
  - Breakdown models: 11 tests
  - Breakdown generator: 10 tests

- Storyboard: 16 tests
  - Storyboard models: 8 tests
  - Storyboard generator: 8 tests

- Advisory: 19 tests
  - Advisory models: 10 tests
  - Advisory generators: 9 tests

- Workflow: 6 tests
  - End-to-end integration: 6 tests

## File Structure

```
.kiro/
├── specs/
│   ├── ralph-wiggum-loop/          # Loop system spec
│   │   ├── requirements.md
│   │   ├── design.md
│   │   └── tasks.md
│   └── entertainment-production/    # Production agent spec
│       ├── requirements.md
│       ├── design.md
│       └── tasks.md
├── loop/
│   ├── state.md                     # Loop state (single source of truth)
│   ├── agent-prompt.md              # Agent behavior rules
│   └── last_output.md               # Latest iteration report
├── src/
│   ├── loop_controller.py           # Loop orchestration
│   ├── state_parser.py              # State file parsing
│   ├── state_writer.py              # Atomic state updates
│   ├── report_generator.py          # Report generation
│   ├── models/                      # Data models
│   │   ├── script.py
│   │   ├── breakdown.py
│   │   ├── storyboard.py
│   │   └── advisory.py
│   ├── generators/                  # Content generators
│   │   ├── script_generator.py
│   │   ├── breakdown_generator.py
│   │   ├── storyboard_generator.py
│   │   └── advisory_generator.py
│   └── workflow/                    # Workflow orchestration
│       └── entertainment_workflow.py
├── tests/                           # Complete test suite
├── demo_production.py               # Demo script
└── run_loop.py                      # Loop CLI runner
```

## User Stories Implemented

### Ralph Wiggum Loop
- ✅ US-1: State Management
- ✅ US-2: Iteration Execution
- ✅ US-3: Test Enforcement
- ✅ US-4: Report Generation
- ✅ US-5: Mode Detection

### Entertainment Production
- ✅ US-1: Script Authoring & Polishing
- ✅ US-2: Script Breakdown for Production
- ✅ US-3: Storyboard & Shot List Generation
- ✅ US-4: Production & Post-production Advisory
- ✅ US-5: Autonomous Loop & Engineering Quality

## Correctness Properties

Both systems implement formal correctness properties validated through property-based testing:

**Loop System:**
1. State persistence across iterations
2. Test enforcement before progression
3. Report completeness and structure
4. Incremental change atomicity
5. Mode consistency rules

**Production Agent:**
1. Script hook requirement (first 3-5 seconds)
2. Scene-to-breakdown 1:1 mapping
3. Shot-to-scene continuity
4. Duration tolerance (±20%)
5. Minimum actionable advisory items

## Environment

- **Python**: 3.14.2
- **Testing**: pytest 9.0.2, hypothesis 6.150.2
- **Platform**: Windows (cmd shell)

## Demo Output Example

Running `py demo_production.py` generates:

```
demo_output/
├── The_Coffee_Shop_Catastrophe_script.json
├── The_Coffee_Shop_Catastrophe_breakdown.json
├── The_Coffee_Shop_Catastrophe_breakdown.csv
├── The_Coffee_Shop_Catastrophe_storyboard.md
├── The_Coffee_Shop_Catastrophe_shotlist.csv
├── The_Coffee_Shop_Catastrophe_production_notes.md
└── The_Coffee_Shop_Catastrophe_postproduction_notes.md
```

## Development Workflow

The system follows its own autonomous loop methodology:

1. Read `loop/state.md` for current task
2. Make small, safe, incremental changes
3. Run tests after every change
4. Fix failures immediately (no progression while tests fail)
5. Write iteration report to `loop/last_output.md`
6. Update `loop/state.md` with new status
7. Continue automatically

## Documentation

Complete specifications available in `.kiro/specs/`:
- Requirements documents with user stories and acceptance criteria
- Design documents with architecture and correctness properties
- Task breakdowns with implementation plans

## License
MIT
