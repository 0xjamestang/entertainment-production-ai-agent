"""Tests for report generator."""
import pytest
from pathlib import Path
from src.report_generator import ReportGenerator


class TestReportGenerator:
    """Test suite for ReportGenerator."""

    def setup_method(self):
        """Set up test fixtures."""
        self.generator = ReportGenerator()

    def test_generate_basic_report(self):
        """Should generate a basic report."""
        report = self.generator.generate_report(
            iteration=1,
            status="ENGINEERING",
            what_i_did="Implemented feature X",
            changes_made=["Created file.py", "Updated test.py"],
            tests_run=["pytest passed"],
            tests_passing=True,
            next_plan="Implement feature Y"
        )

        assert "## Iteration: 1" in report
        assert "## Status: ENGINEERING" in report
        assert "Implemented feature X" in report
        assert "Created file.py" in report
        assert "Updated test.py" in report
        assert "pytest passed" in report
        assert "Tests Passing: YES" in report
        assert "Blockers: NONE" in report
        assert "Ready for Next: YES" in report
        assert "Implement feature Y" in report

    def test_generate_report_with_failures(self):
        """Should generate report with test failures."""
        report = self.generator.generate_report(
            iteration=2,
            status="ENGINEERING",
            what_i_did="Fixed bugs",
            changes_made=["Fixed bug in module.py"],
            tests_run=["pytest failed: 2 tests"],
            tests_passing=False,
            blockers="Test failures in module",
            next_plan="Debug failing tests"
        )

        assert "Tests Passing: NO" in report
        assert "Blockers: Test failures in module" in report
        assert "Ready for Next: NO" in report

    def test_generate_report_with_empty_lists(self):
        """Should handle empty lists."""
        report = self.generator.generate_report(
            iteration=3,
            status="CREATIVE",
            what_i_did="Wrote documentation",
            changes_made=[],
            tests_run=[],
            tests_passing=True,
            next_plan="Continue documentation"
        )

        assert "No changes made" in report
        assert "No tests run" in report

    def test_generate_report_with_notes(self):
        """Should include notes when provided."""
        report = self.generator.generate_report(
            iteration=4,
            status="ENGINEERING",
            what_i_did="Refactored code",
            changes_made=["Refactored module.py"],
            tests_run=["All tests passed"],
            tests_passing=True,
            next_plan="Add new feature",
            notes="This was a major refactoring"
        )

        assert "This was a major refactoring" in report

    def test_save_report(self):
        """Should save report to file."""
        report = "# Test Report\n\nContent"
        test_file = "test_report.md"
        
        success, error = self.generator.save_report(report, test_file)
        
        assert success is True
        assert error is None
        assert Path(test_file).exists()
        
        # Cleanup
        Path(test_file).unlink()

    def test_save_report_creates_directory(self):
        """Should create directory if it doesn't exist."""
        report = "# Test Report"
        test_file = "test_dir/test_report.md"
        
        success, error = self.generator.save_report(report, test_file)
        
        assert success is True
        assert Path(test_file).exists()
        
        # Cleanup
        Path(test_file).unlink()
        Path("test_dir").rmdir()
