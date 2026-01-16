# Goal
Build a production-ready **Entertainment Production Agent** (short drama / short-form video) that can:

- **Ingest requirements and repo context** (specs, scripts, assets, tests), maintain state across iterations, and generate production artifacts as files.
- **Generate / polish scripts**: story concept → outline → scenes → dialogue, with platform-aware pacing (hook, reversal, retention) and “shootability” checks.
- **Break down scripts for production**: produce script breakdown sheets (cast, props, wardrobe, locations, SFX/stunts), plus storyboard + shot list for each scene.
- **Advise across the end-to-end workflow**: pre-production (schedule/budget/risk), production (shooting & continuity guidance), post-production (edit workflow, sound/color/titles), and delivery optimization for short-form platforms.
- **Implement features in small, safe patches** with clear diffs, strong typing/validation, and minimal dependencies.
- **Run tests after every change** and **auto-debug/fix** until there are **zero failing tests** (no progression to new features while CI is red).
- **Maintain CI and quality gates** (lint/typecheck/unit tests/property-based tests) and keep iteration reports.
- **Enforce security and style guardrails** (safe shell allowlist, path sanitization, no secret exfiltration, consistent formatting & file conventions).

# User Stories

## US-1: Script Authoring & Polishing
As a short drama / short-form video creator,
I want the AI to generate or polish scripts based on genre, platform, and target audience,
so that I can quickly obtain shootable, high-retention scripts optimized for short-form platforms.
Acceptance Criteria
•	Inputs must support:
o	Genre / style
o	Target platform (TikTok, Kuaishou, YouTube Shorts, etc.)
o	Episode duration (30–120 seconds)
o	Target audience profile
•	Output must include:
o	Clear scene breakdown
o	Character list with dialogue and actions
o	An explicit hook within the first 3–5 seconds
•	The system must:
o	Ensure dialogue is conversational and performable
o	Flag elements that increase production cost or complexity (locations, extras, night scenes, VFX)
•	Automated checks:
o	The script must be parsable by downstream Script Breakdown modules
o	No missing scenes or characters are allowed


## US-2: Script Breakdown for Production
User Story
As a producer or director,
I want the AI to automatically break down scripts into production elements,
so that I can quickly assess feasibility, cost, and shooting complexity.
Acceptance Criteria
•	Input: a valid script produced by US-1
•	Output:
o	breakdown.csv or breakdown.json
•	Each scene must include:
o	Characters
o	Location (interior/exterior, day/night)
o	Props
o	Wardrobe / makeup
o	Special requirements (stunts, VFX, vehicles, animals, etc.)
•	The system must:
o	Maintain a one-to-one mapping between scenes and breakdown entries
o	Never omit any character or critical production element
•	Automated checks:
o	Every scene has at least one breakdown record
o	All breakdown outputs are serializable and state-safe


## US-3: Storyboard & Shot List Generation
User Story
As a director or cinematographer,
I want the AI to convert scripts into storyboards and shot lists,
so that shooting can be executed with clear visual guidance.
Acceptance Criteria
•	Input:
o	Script + corresponding breakdown
•	Output:
o	storyboard.md
o	shotlist.csv
•	Each shot must include:
o	Shot ID
o	Shot size (wide / medium / close-up / extreme close-up)
o	Camera position or movement
o	Visual description
o	Suggested duration
•	The system must:
o	Preserve narrative and spatial continuity
o	Avoid illogical shot transitions without justification
•	Automated checks:
o	Each shot maps back to a valid scene
o	Total estimated duration is within ±20% of target runtime


## US-4: Production & Post-production Advisory
User Story
As a producer or editor,
I want the AI to provide actionable guidance for shooting and post-production,
so that rework risk is reduced and final output quality is improved.
Acceptance Criteria
•	Input:
o	Script, storyboard, and shot list
•	Output:
o	production_notes.md
o	postproduction_notes.md
•	Production guidance must include:
o	Continuity risks (wardrobe, props, blocking)
o	Audio capture and coverage recommendations (B-roll, room tone)
•	Post-production guidance must include:
o	Editing rhythm and pacing suggestions
o	Subtitle, sound, and color guidelines for short-form platforms
o	A list of common revision pitfalls
•	Automated checks:
o	Each output contains a minimum number of concrete, actionable items
o	No generic or purely high-level advice is allowed


## US-5: Autonomous Loop & Engineering Quality
User Story
As a system owner,
I want the AI to iterate autonomously, fix errors, and continuously improve outputs,
so that the system remains stable, production-ready, and scalable.
Acceptance Criteria
•	The system must:
o	Run tests after every iteration
o	Enter a debug → fix → retest loop whenever any test fails
o	Block progression to new features while CI is red
•	Each iteration must generate:
o	A complete loop/last_output.md iteration report
•	The system must not:
o	Advance functionality with failing tests
o	Perform non-atomic writes to the state file
•	Automated checks:
o	The LoopController correctly handles retries and failures
o	The state file remains parseable at all times



# Current task
System production-ready. All user stories complete (US-1 through US-5 for both Ralph Wiggum Loop and Entertainment Production Agent).
Demo production workflow operational. 114/114 tests passing.
Ready for creative production work or feature expansion.

# Iteration History
- Iteration 10: ENGINEERING mode - Advanced quality enhancement: added dialogue subtext, emotional nuance, genre-specific scene descriptions, comedic timing and dramatic pacing notes, all 114 tests passing
- Iteration 9: ENGINEERING mode - Enhanced script generator (genre-specific characters, natural dialogue), improved storyboard generator (better shot descriptions, hook optimization), all 114 tests passing
- Iteration 8: CREATIVE mode - Created demo production script, executed complete workflow, generated sample production package, updated README documentation
- Iteration 7: Implemented entertainment production data models (Script, Scene, Character, Dialogue) and script generator with validation, all 52 tests passing
- Iteration 6: Implemented LoopController with mode detection and iteration orchestration, created CLI runner, executed first autonomous iteration, all 29 tests passing
- Iteration 5: Python environment ready, implemented core modules (state_parser, report_generator, state_writer), all 19 tests passing
- Iteration 4: Created tasks.md, attempted TypeScript implementation, pivoted to PowerShell due to environment constraints, created core modules and documentation
- Iteration 3: Created comprehensive design.md with architecture, correctness properties, and testing strategy
- Iteration 2: Created loop infrastructure and requirements.md
- Iteration 1: Initial setup

# Constraints
- Prefer TypeScript/Node OR Python (pick one based on repo)
- No breaking changes
- Add tests for any new behavior
- **Environment**: Python 3.14.2 available, pip 25.3 available

# Status
- Requirements: ✅ Complete (Ralph Wiggum Loop + Entertainment Production)
- Design: ✅ Complete
- Tasks: ✅ Complete
- Implementation: ✅ All Systems Complete
- Tests: ✅ 114/114 passing (100%)
- Documentation: ✅ Complete
- Demo: ✅ Operational
- Loop Execution: ✅ Operational
