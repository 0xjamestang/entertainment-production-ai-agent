"""Tests for state parser."""
import pytest
from pathlib import Path
from src.state_parser import StateParser, LoopState


class TestStateParser:
    """Test suite for StateParser."""

    def setup_method(self):
        """Set up test fixtures."""
        self.parser = StateParser()

    def test_parse_valid_content(self):
        """Should parse valid state content."""
        content = """# Goal
Build a production-ready agent

# Current task
Implement feature X

# Constraints
- No breaking changes
- Add tests

# Iteration History
- Iteration 1: Setup

# Status
- Requirements: Complete"""

        success, state, error = self.parser.parse_content(content)

        assert success is True
        assert state is not None
        assert error is None
        assert state.goal == "Build a production-ready agent"
        assert state.current_task == "Implement feature X"
        assert "No breaking changes" in state.constraints
        assert "Iteration 1" in state.iteration_history
        assert "Requirements: Complete" in state.status

    def test_parse_missing_sections(self):
        """Should handle missing sections."""
        content = """# Goal
Build something

# Current task
Do work"""

        success, state, error = self.parser.parse_content(content)

        assert success is True
        assert state is not None
        assert state.goal == "Build something"
        assert state.current_task == "Do work"
        assert state.constraints == ""
        assert state.iteration_history == ""
        assert state.status == ""

    def test_parse_empty_content(self):
        """Should handle empty content."""
        success, state, error = self.parser.parse_content("")

        assert success is True
        assert state is not None
        assert state.goal == ""
        assert state.current_task == ""

    def test_parse_malformed_markdown(self):
        """Should handle malformed markdown."""
        content = "Not a valid markdown structure"

        success, state, error = self.parser.parse_content(content)

        assert success is True
        assert state is not None
        assert state.goal == ""

    def test_parse_special_characters(self):
        """Should handle special characters."""
        content = """# Goal
Build agent with **bold** and *italic*

# Current task
Task with `code` and [links](url)"""

        success, state, error = self.parser.parse_content(content)

        assert success is True
        assert state is not None
        assert "**bold**" in state.goal
        assert "`code`" in state.current_task

    def test_parse_nonexistent_file(self):
        """Should return error for non-existent file."""
        success, state, error = self.parser.parse_file("non-existent-file.md")

        assert success is False
        assert state is None
        assert "not found" in error

    def test_parse_actual_state_file(self):
        """Should parse the actual loop/state.md file."""
        success, state, error = self.parser.parse_file("loop/state.md")

        assert success is True
        assert state is not None
        assert len(state.goal) > 0
