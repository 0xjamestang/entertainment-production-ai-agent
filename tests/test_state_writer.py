"""Tests for state writer."""
import pytest
from pathlib import Path
from src.state_writer import StateWriter


class TestStateWriter:
    """Test suite for StateWriter."""

    def setup_method(self):
        """Set up test fixtures."""
        self.writer = StateWriter()
        self.test_file = "test_state.md"

    def teardown_method(self):
        """Clean up test files."""
        if Path(self.test_file).exists():
            Path(self.test_file).unlink()
        if Path(self.test_file).with_suffix('.tmp').exists():
            Path(self.test_file).with_suffix('.tmp').unlink()

    def test_update_single_section(self):
        """Should update a single section."""
        initial_content = """# Goal
Old goal

# Current task
Old task

# Status
Old status"""
        
        Path(self.test_file).write_text(initial_content, encoding='utf-8')
        
        success, error = self.writer.update_state(
            self.test_file,
            goal="New goal"
        )
        
        assert success is True
        assert error is None
        
        updated_content = Path(self.test_file).read_text(encoding='utf-8')
        assert "New goal" in updated_content
        assert "Old task" in updated_content  # Other sections unchanged
        assert "Old status" in updated_content

    def test_update_multiple_sections(self):
        """Should update multiple sections."""
        initial_content = """# Goal
Old goal

# Current task
Old task

# Status
Old status"""
        
        Path(self.test_file).write_text(initial_content, encoding='utf-8')
        
        success, error = self.writer.update_state(
            self.test_file,
            goal="New goal",
            current_task="New task",
            status="New status"
        )
        
        assert success is True
        updated_content = Path(self.test_file).read_text(encoding='utf-8')
        assert "New goal" in updated_content
        assert "New task" in updated_content
        assert "New status" in updated_content
        assert "Old" not in updated_content

    def test_update_nonexistent_file(self):
        """Should return error for non-existent file."""
        success, error = self.writer.update_state(
            "nonexistent.md",
            goal="New goal"
        )
        
        assert success is False
        assert "not found" in error

    def test_update_preserves_other_content(self):
        """Should preserve content in non-updated sections."""
        initial_content = """# Goal
Original goal with **formatting**

# Current task
Original task with `code`

# Constraints
- Constraint 1
- Constraint 2"""
        
        Path(self.test_file).write_text(initial_content, encoding='utf-8')
        
        success, error = self.writer.update_state(
            self.test_file,
            current_task="Updated task"
        )
        
        assert success is True
        updated_content = Path(self.test_file).read_text(encoding='utf-8')
        assert "Original goal with **formatting**" in updated_content
        assert "Updated task" in updated_content
        assert "Constraint 1" in updated_content

    def test_update_adds_missing_section(self):
        """Should add section if it doesn't exist."""
        initial_content = """# Goal
Some goal"""
        
        Path(self.test_file).write_text(initial_content, encoding='utf-8')
        
        success, error = self.writer.update_state(
            self.test_file,
            status="New status section"
        )
        
        assert success is True
        updated_content = Path(self.test_file).read_text(encoding='utf-8')
        assert "# Status" in updated_content
        assert "New status section" in updated_content

    def test_update_with_multiline_content(self):
        """Should handle multiline section content."""
        initial_content = """# Goal
Old goal

# Status
Old status"""
        
        Path(self.test_file).write_text(initial_content, encoding='utf-8')
        
        new_history = """- Iteration 1: Setup
- Iteration 2: Implementation
- Iteration 3: Testing"""
        
        success, error = self.writer.update_state(
            self.test_file,
            iteration_history=new_history
        )
        
        assert success is True
        updated_content = Path(self.test_file).read_text(encoding='utf-8')
        assert "Iteration 1: Setup" in updated_content
        assert "Iteration 2: Implementation" in updated_content
        assert "Iteration 3: Testing" in updated_content
