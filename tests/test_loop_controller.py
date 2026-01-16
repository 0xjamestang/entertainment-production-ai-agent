"""Tests for loop controller."""
import pytest
from pathlib import Path
from src.loop_controller import LoopController
from src.state_parser import LoopState


class TestLoopController:
    """Test suite for LoopController."""

    def setup_method(self):
        """Set up test fixtures."""
        self.test_state_file = "test_loop_state.md"
        self.test_report_file = "test_loop_report.md"
        self.controller = LoopController(
            state_file=self.test_state_file,
            report_file=self.test_report_file
        )
        
        # Create a test state file
        initial_state = """# Goal
Test goal

# Current task
Test task

# Constraints
Test constraints

# Iteration History
- Iteration 1: Initial

# Status
- Tests: passing
- Implementation: complete"""
        
        Path(self.test_state_file).write_text(initial_state, encoding='utf-8')

    def teardown_method(self):
        """Clean up test files."""
        for file in [self.test_state_file, self.test_report_file]:
            if Path(file).exists():
                Path(file).unlink()
        if Path(self.test_state_file).with_suffix('.tmp').exists():
            Path(self.test_state_file).with_suffix('.tmp').unlink()

    def test_read_state(self):
        """Should read state successfully."""
        success, state, error = self.controller.read_state()
        
        assert success is True
        assert state is not None
        assert error is None
        assert state.goal == "Test goal"
        assert state.current_task == "Test task"

    def test_detect_mode_engineering(self):
        """Should detect engineering mode."""
        state = LoopState(
            goal="Test",
            current_task="Implement feature",
            constraints="",
            iteration_history="",
            status="Implementation in progress"
        )
        
        mode = self.controller.detect_mode(state)
        assert mode == "ENGINEERING"

    def test_detect_mode_creative(self):
        """Should detect creative mode when tests passing and complete."""
        state = LoopState(
            goal="Test",
            current_task="Write docs",
            constraints="",
            iteration_history="",
            status="Tests passing, implementation complete"
        )
        
        mode = self.controller.detect_mode(state)
        assert mode == "CREATIVE"

    def test_detect_mode_blocked(self):
        """Should detect blocked mode."""
        state = LoopState(
            goal="Test",
            current_task="Fix issue",
            constraints="",
            iteration_history="",
            status="Blocked by environment issue"
        )
        
        mode = self.controller.detect_mode(state)
        assert mode == "BLOCKED"

    def test_execute_iteration_without_work(self):
        """Should execute iteration without work function."""
        success, error = self.controller.execute_iteration()
        
        assert success is True
        assert error is None
        assert Path(self.test_report_file).exists()
        assert self.controller.get_current_iteration() == 1

    def test_execute_iteration_with_work(self):
        """Should execute iteration with work function."""
        def mock_work(state: LoopState):
            changes = ["Created file.py", "Updated test.py"]
            tests = ["pytest passed"]
            passing = True
            return changes, tests, passing
        
        success, error = self.controller.execute_iteration(work_function=mock_work)
        
        assert success is True
        assert error is None
        
        # Check report was created
        report_content = Path(self.test_report_file).read_text(encoding='utf-8')
        assert "Created file.py" in report_content
        assert "pytest passed" in report_content

    def test_execute_iteration_updates_state(self):
        """Should update state with iteration history."""
        success, error = self.controller.execute_iteration()
        
        assert success is True
        
        # Read updated state
        state_content = Path(self.test_state_file).read_text(encoding='utf-8')
        assert "Iteration 1" in state_content

    def test_run_loop_multiple_iterations(self):
        """Should run multiple iterations."""
        success, error = self.controller.run_loop(max_iterations=3)
        
        assert success is True
        assert self.controller.get_current_iteration() == 3

    def test_run_loop_stops_on_blocked(self):
        """Should stop loop when blocked."""
        # Update state to blocked
        blocked_state = """# Goal
Test goal

# Current task
Test task

# Constraints
Test constraints

# Iteration History
- Iteration 1: Initial

# Status
Blocked by critical issue"""
        
        Path(self.test_state_file).write_text(blocked_state, encoding='utf-8')
        
        success, error = self.controller.run_loop(max_iterations=10)
        
        assert success is True
        assert "blocked" in error.lower()
        assert self.controller.get_current_iteration() == 1

    def test_execute_iteration_handles_work_failure(self):
        """Should handle work function failures."""
        def failing_work(state: LoopState):
            raise Exception("Work failed")
        
        success, error = self.controller.execute_iteration(work_function=failing_work)
        
        assert success is False
        assert "Work function failed" in error
