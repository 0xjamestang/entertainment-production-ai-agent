# Ralph Wiggum Autonomous Loop System - Requirements

## Feature Overview
An autonomous agent loop system that continuously iterates on tasks, runs tests, and self-corrects until all tests pass. The system operates without user intervention and maintains state across iterations.

## User Stories

### 1. As a developer, I want the agent to loop autonomously
**Acceptance Criteria:**
- 1.1 Agent reads `loop/state.md` at the start of each iteration
- 1.2 Agent continues automatically without asking for confirmation
- 1.3 Agent updates state file after each iteration
- 1.4 Agent maintains full context and history across iterations

### 2. As a developer, I want automatic test enforcement
**Acceptance Criteria:**
- 2.1 Agent runs tests after every code change
- 2.2 Agent does not proceed if any test fails
- 2.3 Agent debugs and fixes failing tests in subsequent iterations
- 2.4 Agent loops until all tests pass (zero failures)

### 3. As a developer, I want structured iteration reports
**Acceptance Criteria:**
- 3.1 Each iteration produces a report in `loop/last_output.md`
- 3.2 Report includes: actions taken, changes made, test results, next steps
- 3.3 Report follows consistent structure defined in `loop/agent-prompt.md`
- 3.4 Report is echoed to chat for visibility

### 4. As a developer, I want incremental engineering changes
**Acceptance Criteria:**
- 4.1 Agent makes small, safe changes per iteration
- 4.2 Agent fixes root causes, not workarounds
- 4.3 Agent fixes one logical issue per iteration when debugging
- 4.4 Agent reads `loop/ci.md` to understand test failures

### 5. As a developer, I want creative mode support
**Acceptance Criteria:**
- 5.1 When tests are green, agent can work on creative tasks
- 5.2 Creative outputs (scripts, storyboards) are saved to repository
- 5.3 Creative work is still reported in iteration output
- 5.4 Creative mode is described in `loop/state.md`

## Technical Requirements

### File Structure
- `loop/state.md` - Single source of truth for loop state
- `loop/agent-prompt.md` - Output structure and behavior definition
- `loop/last_output.md` - Most recent iteration report
- `loop/ci.md` - Test/CI results (optional, created by hooks)

### Loop Phases
1. **Read State**: Load context from `loop/state.md`
2. **Execute Work**: Make changes based on current task
3. **Validate**: Run tests/checks
4. **Report**: Write structured output to `loop/last_output.md`
5. **Update State**: Update `loop/state.md` with new status
6. **Continue**: Automatically proceed to next iteration

### Engineering Mode Rules
- Make incremental changes
- Run tests after every change
- Fix failures before proceeding
- Loop until green

### Creative Mode Rules
- Only enter when tests are passing
- Save all outputs to repository
- Maintain same reporting structure
- Follow tasks in `loop/state.md`

## Non-Functional Requirements
- Agent operates autonomously without user prompts
- State persists across iterations
- Full traceability of actions and decisions
- Clear separation between engineering and creative modes
