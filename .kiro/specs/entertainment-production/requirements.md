# Entertainment Production Agent - Requirements

## Feature Overview
An AI-powered entertainment production agent for short drama and short-form video creation. Supports the complete workflow from script generation to post-production guidance.

## User Stories

### US-1: Script Authoring & Polishing
**As a** short drama / short-form video creator  
**I want** the AI to generate or polish scripts based on genre, platform, and target audience  
**So that** I can quickly obtain shootable, high-retention scripts optimized for short-form platforms

**Acceptance Criteria:**
- 1.1 System accepts inputs: genre/style, target platform, episode duration (30-120s), target audience
- 1.2 Output includes clear scene breakdown with character list, dialogue, and actions
- 1.3 Script contains explicit hook within first 3-5 seconds
- 1.4 Dialogue is conversational and performable
- 1.5 System flags high-cost elements (locations, extras, night scenes, VFX)
- 1.6 Script is parsable by downstream Script Breakdown modules
- 1.7 No missing scenes or characters allowed

### US-2: Script Breakdown for Production
**As a** producer or director  
**I want** the AI to automatically break down scripts into production elements  
**So that** I can quickly assess feasibility, cost, and shooting complexity

**Acceptance Criteria:**
- 2.1 System accepts valid script from US-1 as input
- 2.2 Output generates breakdown.csv or breakdown.json
- 2.3 Each scene includes: characters, location (int/ext, day/night), props, wardrobe/makeup, special requirements
- 2.4 One-to-one mapping between scenes and breakdown entries maintained
- 2.5 No character or critical production element omitted
- 2.6 Every scene has at least one breakdown record
- 2.7 All breakdown outputs are serializable and state-safe

### US-3: Storyboard & Shot List Generation
**As a** director or cinematographer  
**I want** the AI to convert scripts into storyboards and shot lists  
**So that** shooting can be executed with clear visual guidance

**Acceptance Criteria:**
- 3.1 System accepts script + breakdown as input
- 3.2 Output generates storyboard.md and shotlist.csv
- 3.3 Each shot includes: shot ID, shot size, camera position/movement, visual description, suggested duration
- 3.4 System preserves narrative and spatial continuity
- 3.5 No illogical shot transitions without justification
- 3.6 Each shot maps back to valid scene
- 3.7 Total estimated duration within ±20% of target runtime

### US-4: Production & Post-production Advisory
**As a** producer or editor  
**I want** the AI to provide actionable guidance for shooting and post-production  
**So that** rework risk is reduced and final output quality is improved

**Acceptance Criteria:**
- 4.1 System accepts script, storyboard, and shot list as input
- 4.2 Output generates production_notes.md and postproduction_notes.md
- 4.3 Production guidance includes: continuity risks, audio capture recommendations, coverage suggestions
- 4.4 Post-production guidance includes: editing rhythm/pacing, subtitle/sound/color guidelines, revision pitfalls
- 4.5 Each output contains minimum number of concrete, actionable items
- 4.6 No generic or purely high-level advice allowed

### US-5: Autonomous Loop & Engineering Quality
**As a** system owner  
**I want** the AI to iterate autonomously, fix errors, and continuously improve outputs  
**So that** the system remains stable, production-ready, and scalable

**Acceptance Criteria:**
- 5.1 System runs tests after every iteration
- 5.2 System enters debug → fix → retest loop when tests fail
- 5.3 System blocks progression to new features while CI is red
- 5.4 Each iteration generates complete loop/last_output.md report
- 5.5 System never advances functionality with failing tests
- 5.6 System performs only atomic writes to state file
- 5.7 LoopController correctly handles retries and failures
- 5.8 State file remains parseable at all times

## Technical Requirements

### Data Models
- Script: scenes, characters, dialogue, actions, timing
- Breakdown: scene mapping, production elements, cost indicators
- Storyboard: visual descriptions, shot specifications
- Shot List: shot details, camera specs, duration estimates
- Production Notes: continuity, audio, coverage guidance
- Post-production Notes: editing, platform optimization

### File Formats
- Scripts: Markdown or JSON
- Breakdowns: CSV or JSON
- Storyboards: Markdown with structured format
- Shot Lists: CSV
- Notes: Markdown

### Validation Rules
- All outputs must be parseable and serializable
- Scene-to-breakdown mapping must be 1:1
- Shot-to-scene mapping must be valid
- Duration estimates must be within tolerance
- No missing required fields

## Non-Functional Requirements
- Performance: Generate script breakdown in < 5 seconds
- Reliability: 99% uptime for autonomous loop
- Maintainability: Clear separation of concerns, modular design
- Testability: 100% test coverage for core logic
- Security: No secret exfiltration, path sanitization
