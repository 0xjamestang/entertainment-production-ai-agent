# Ralph Wiggum Autonomous Loop System - Design

## Overview
The Ralph Wiggum system is an autonomous agent loop that continuously iterates on tasks, enforces test-driven development, and self-corrects until all tests pass. It operates without user intervention and maintains full state across iterations.

## Architecture

### Core Components

#### 1. State Management (`loop/state.md`)
**Purpose**: Single source of truth for loop state and context

**Structure**:
```markdown
# Goal
[High-level objective]

# Current task
[Specific task being worked on]

# Constraints
[Technical and operational constraints]
```

**Responsibilities**:
- Maintain iteration history
- Track current task and status
- Store test results
- Record blockers
- Preserve context across iterations

#### 2. Agent Prompt (`loop/agent-prompt.md`)
**Purpose**: Define output structure contract and behavior rules

**Contents**:
- Output structure template for `loop/last_output.md`
- Loop behavior rules
- Engineering mode guidelines
- Creative mode guidelines

#### 3. Iteration Report (`loop/last_output.md`)
**Purpose**: Structured report of each iteration

**Required Sections**:
- Iteration number and date
- Status (ENGINEERING/CREATIVE/BLOCKED)
- Actions taken
- Changes made (files created/modified)
- Tests run (commands and results)
- Current state (tests passing, blockers, readiness)
- Next iteration plan
- Notes

#### 4. CI Results (`loop/ci.md`) [Optional]
**Purpose**: Store test/CI output for debugging

**Created by**: External hooks or test runners
**Used by**: Agent when debugging test failures

### Loop Flow

```
┌─────────────────────────────────────────┐
│  1. Read loop/state.md                  │
│     - Load context and history          │
│     - Identify current task             │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  2. Execute Work                        │
│     - Make incremental changes          │
│     - Update code/artifacts             │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  3. Validate                            │
│     - Run tests/checks                  │
│     - Capture results                   │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  4. Report                              │
│     - Write loop/last_output.md         │
│     - Echo to chat                      │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  5. Update State                        │
│     - Update loop/state.md              │
│     - Increment iteration               │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  6. Continue                            │
│     - Automatically proceed             │
│     - No user confirmation needed       │
└─────────────────────────────────────────┘
```

## Operating Modes

### Engineering Mode
**Trigger**: When there are code/test tasks or tests are failing

**Behavior**:
- Make SMALL, SAFE, incremental changes
- Run tests after EVERY code change
- If tests fail:
  - Read `loop/ci.md` for failure details
  - Identify most likely root cause
  - Fix ONE logical issue per iteration
  - Loop again
- Never proceed with failing tests
- Prefer root cause fixes over workarounds

**Exit Condition**: All tests passing (zero failures)

### Creative Mode
**Trigger**: When tests are green and creative tasks are defined

**Behavior**:
- Work on creative tasks from `loop/state.md`
- Generate scripts, storyboards, scene descriptions
- Create pipelines for video/image generation
- Save all outputs to repository (e.g., `scripts/`, `storyboards/`)
- Maintain same reporting structure

**Exit Condition**: Creative task complete or new engineering task appears

## Design Decisions

### 1. File-Based State Management
**Decision**: Use markdown files for state persistence
**Rationale**: 
- Human-readable and editable
- Version control friendly
- No database dependencies
- Easy to inspect and debug

### 2. Autonomous Continuation
**Decision**: Agent continues automatically without user confirmation
**Rationale**:
- Enables true autonomous operation
- Reduces friction in iteration loop
- Allows overnight/background execution
- User can stop via hooks or manual intervention

### 3. Strict Test Enforcement
**Decision**: Block progression on any test failure
**Rationale**:
- Ensures code quality
- Prevents cascading failures
- Forces proper debugging
- Maintains production-ready state

### 4. Incremental Changes
**Decision**: One logical change per iteration
**Rationale**:
- Easier to debug failures
- Clear cause-and-effect relationship
- Safer for production code
- Better traceability

### 5. Structured Reporting
**Decision**: Mandatory structured output every iteration
**Rationale**:
- Consistent documentation
- Easy to parse and analyze
- Clear audit trail
- Supports automation and tooling

## Implementation Strategy

### Phase 1: Infrastructure (Complete)
- ✅ Create `loop/state.md`
- ✅ Create `loop/agent-prompt.md`
- ✅ Create `loop/last_output.md`
- ✅ Create requirements spec

### Phase 2: Validation & Testing
- Create validation script to check loop structure
- Add tests for state file parsing
- Add tests for report generation
- Verify autonomous continuation

### Phase 3: Engineering Mode
- Implement test runner integration
- Add CI result parsing
- Implement failure detection
- Add debugging workflow

### Phase 4: Creative Mode
- Add creative task detection
- Implement output directory management
- Add creative artifact validation
- Test mode switching

## Correctness Properties

### Property 1: State Persistence
**Validates: Requirements 1.1, 1.3, 1.4**
```
For all iterations i:
  state_after(i) == state_before(i+1)
```
Every iteration must preserve state for the next iteration.

### Property 2: Test Enforcement
**Validates: Requirements 2.1, 2.2, 2.4**
```
For all code changes c:
  tests_run_after(c) == true
  AND
  if any_test_fails(c):
    next_iteration_fixes(c) == true
```
Tests must run after changes, and failures must be addressed.

### Property 3: Report Completeness
**Validates: Requirements 3.1, 3.2, 3.3**
```
For all iterations i:
  has_all_sections(report(i)) == true
  AND
  follows_structure(report(i), agent_prompt) == true
```
Every report must be complete and follow the defined structure.

### Property 4: Incremental Changes
**Validates: Requirements 4.1, 4.3**
```
For all iterations i in engineering_mode:
  logical_changes(i) <= 1
  AND
  change_size(i) <= SMALL_THRESHOLD
```
Engineering changes must be small and focused.

### Property 5: Mode Consistency
**Validates: Requirements 5.1, 5.2, 5.3**
```
For all iterations i:
  if mode(i) == CREATIVE:
    all_tests_passing(i) == true
  AND
  if mode(i) == ENGINEERING:
    exists(failing_test) OR exists(incomplete_task)
```
Creative mode only when tests pass; engineering mode when work remains.

## Testing Strategy

### Unit Tests
- State file parsing and validation
- Report structure validation
- Mode detection logic
- File path handling

### Integration Tests
- Full iteration cycle
- State persistence across iterations
- Test runner integration
- Report generation

### Property-Based Tests
- State persistence property (Property 1)
- Test enforcement property (Property 2)
- Report completeness property (Property 3)
- Incremental changes property (Property 4)
- Mode consistency property (Property 5)

### Manual Tests
- Autonomous continuation behavior
- User interruption handling
- Error recovery
- Long-running loop stability

## Technology Choices

### Language: TypeScript
**Rationale**:
- Strong typing for reliability
- Excellent tooling and IDE support
- Node.js ecosystem for file operations
- Easy to test and maintain

### Testing Framework: Vitest
**Rationale**:
- Fast execution
- Built-in property-based testing support (via fast-check)
- Good TypeScript integration
- Modern and actively maintained

### File Operations: Node.js fs/promises
**Rationale**:
- Native Node.js support
- Promise-based async API
- No external dependencies
- Cross-platform compatibility

## Security Considerations

1. **File System Access**: Limit operations to loop/ and .kiro/ directories
2. **Command Execution**: Validate and sanitize test commands
3. **State Validation**: Verify state file integrity before use
4. **Output Sanitization**: Prevent injection in reports

## Performance Considerations

1. **File I/O**: Use async operations to avoid blocking
2. **State Size**: Keep state files under 100KB
3. **Report History**: Archive old reports after 100 iterations
4. **Test Execution**: Timeout long-running tests (5 min default)

## Error Handling

1. **Missing Files**: Create with defaults if missing
2. **Corrupted State**: Restore from last known good state
3. **Test Failures**: Capture full output for debugging
4. **Infinite Loops**: Detect and alert after 50 iterations on same failure

## Future Enhancements

1. **Web Dashboard**: Real-time loop monitoring
2. **Metrics**: Track iteration time, success rate, test coverage
3. **Parallel Loops**: Support multiple concurrent loops
4. **Cloud Integration**: Remote execution and monitoring
5. **AI Improvements**: Better failure diagnosis and fix suggestions
