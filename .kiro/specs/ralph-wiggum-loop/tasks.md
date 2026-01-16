# Ralph Wiggum Autonomous Loop System - Implementation Tasks

## Phase 1: Project Setup & Infrastructure

- [ ] 1.1 Initialize TypeScript project
  - Create package.json with dependencies
  - Configure TypeScript (tsconfig.json)
  - Add Vitest for testing
  - Add fast-check for property-based testing

- [ ] 1.2 Create source directory structure
  - Create src/ directory
  - Create src/types/ for type definitions
  - Create src/core/ for core logic
  - Create src/utils/ for utilities

- [ ] 1.3 Set up test infrastructure
  - Create tests/ directory
  - Configure Vitest config
  - Add test scripts to package.json

## Phase 2: Core State Management

- [ ] 2.1 Implement state file parser
  - Create src/core/state-parser.ts
  - Parse loop/state.md markdown structure
  - Extract goal, task, constraints, history
  - Handle missing or malformed files

- [ ] 2.2 Write unit tests for state parser
  - Test valid state file parsing
  - Test missing file handling
  - Test malformed content handling
  - Test edge cases (empty sections, special characters)

- [ ] 2.3 Implement state writer
  - Create src/core/state-writer.ts
  - Update state file with new iteration data
  - Preserve existing content structure
  - Atomic file writes for safety

- [ ] 2.4 Write unit tests for state writer
  - Test state update operations
  - Test file write safety
  - Test concurrent write handling

## Phase 3: Report Generation

- [ ] 3.1 Implement report generator
  - Create src/core/report-generator.ts
  - Generate structured loop/last_output.md
  - Follow agent-prompt.md structure
  - Include all required sections

- [ ] 3.2 Write unit tests for report generator
  - Test complete report generation
  - Test section formatting
  - Test data sanitization

- [ ] 3.3 Implement report validator
  - Create src/core/report-validator.ts
  - Validate report structure completeness
  - Check required sections present
  - Verify format compliance

- [ ] 3.4 Write unit tests for report validator
  - Test valid report detection
  - Test missing section detection
  - Test format violation detection

## Phase 4: Test Runner Integration

- [ ] 4.1 Implement test runner
  - Create src/core/test-runner.ts
  - Execute test commands
  - Capture stdout/stderr
  - Parse test results

- [ ] 4.2 Write unit tests for test runner
  - Test command execution
  - Test output capture
  - Test result parsing
  - Test timeout handling

- [ ] 4.3 Implement CI result parser
  - Create src/core/ci-parser.ts
  - Parse loop/ci.md if exists
  - Extract failure information
  - Identify root causes

- [ ] 4.4 Write unit tests for CI parser
  - Test CI file parsing
  - Test failure extraction
  - Test missing file handling

## Phase 5: Loop Controller

- [ ] 5.1 Implement main loop controller
  - Create src/core/loop-controller.ts
  - Orchestrate iteration cycle
  - Handle mode switching (engineering/creative)
  - Implement autonomous continuation

- [ ] 5.2 Write unit tests for loop controller
  - Test iteration cycle
  - Test mode detection
  - Test state transitions

- [ ] 5.3 Implement failure detector
  - Create src/core/failure-detector.ts
  - Detect test failures
  - Detect infinite loops (50+ iterations on same failure)
  - Alert on critical issues

- [ ] 5.4 Write unit tests for failure detector
  - Test failure detection
  - Test infinite loop detection
  - Test alert triggering

## Phase 6: Property-Based Tests

- [ ] 6.1 Property test: State Persistence (Property 1)
  - **Validates: Requirements 1.1, 1.3, 1.4**
  - Create tests/properties/state-persistence.test.ts
  - Verify state_after(i) == state_before(i+1)
  - Use fast-check generators for state variations

- [ ] 6.2 Property test: Test Enforcement (Property 2)
  - **Validates: Requirements 2.1, 2.2, 2.4**
  - Create tests/properties/test-enforcement.test.ts
  - Verify tests run after changes
  - Verify failures trigger fixes

- [ ] 6.3 Property test: Report Completeness (Property 3)
  - **Validates: Requirements 3.1, 3.2, 3.3**
  - Create tests/properties/report-completeness.test.ts
  - Verify all sections present
  - Verify structure compliance

- [ ] 6.4 Property test: Incremental Changes (Property 4)
  - **Validates: Requirements 4.1, 4.3**
  - Create tests/properties/incremental-changes.test.ts
  - Verify change size limits
  - Verify single logical change per iteration

- [ ] 6.5 Property test: Mode Consistency (Property 5)
  - **Validates: Requirements 5.1, 5.2, 5.3**
  - Create tests/properties/mode-consistency.test.ts
  - Verify creative mode only when tests pass
  - Verify engineering mode when work remains

## Phase 7: Integration & End-to-End

- [ ] 7.1 Create integration test suite
  - Create tests/integration/full-loop.test.ts
  - Test complete iteration cycle
  - Test multi-iteration scenarios
  - Test error recovery

- [ ] 7.2 Add CLI interface
  - Create src/cli.ts
  - Support start/stop/status commands
  - Display iteration progress
  - Handle user interruption

- [ ] 7.3 Write CLI tests
  - Test command parsing
  - Test output formatting
  - Test error handling

## Phase 8: Documentation & Polish

- [ ] 8.1 Add inline documentation
  - JSDoc comments for all public APIs
  - Usage examples in comments
  - Type documentation

- [ ] 8.2 Create README.md
  - Installation instructions
  - Usage guide
  - Configuration options
  - Examples

- [ ] 8.3 Add error messages
  - User-friendly error messages
  - Debugging hints
  - Recovery suggestions

## Acceptance Criteria

Each task is complete when:
- Code is implemented and follows TypeScript best practices
- Unit tests are written and passing
- No lint errors
- Code is documented
- Changes are committed

Property-based test tasks are complete when:
- Property is correctly encoded
- Generators produce valid test cases
- Tests pass consistently
- Failures are meaningful and actionable
