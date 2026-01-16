"""Tests for entertainment workflow."""
import pytest
from pathlib import Path
import shutil
from src.workflow.entertainment_workflow import EntertainmentWorkflow
from src.models.script import Platform


class TestEntertainmentWorkflow:
    """Test suite for EntertainmentWorkflow."""

    def setup_method(self):
        """Set up test fixtures."""
        self.workflow = EntertainmentWorkflow()
        self.test_output_dir = "test_output"

    def teardown_method(self):
        """Clean up test files."""
        if Path(self.test_output_dir).exists():
            shutil.rmtree(self.test_output_dir)

    def test_execute_full_workflow(self):
        """Should execute complete workflow successfully."""
        success, errors, output_files = self.workflow.execute_full_workflow(
            title="Test Drama",
            genre="Drama",
            platform=Platform.TIKTOK,
            target_duration_seconds=60,
            target_audience="Young adults",
            output_dir=self.test_output_dir
        )
        
        assert success is True
        assert len(errors) == 0
        assert len(output_files) == 7  # script, breakdown (json+csv), storyboard, shotlist, prod notes, postprod notes

    def test_workflow_creates_all_files(self):
        """Should create all required output files."""
        success, errors, output_files = self.workflow.execute_full_workflow(
            title="Test",
            genre="Drama",
            platform=Platform.TIKTOK,
            target_duration_seconds=60,
            target_audience="Adults",
            output_dir=self.test_output_dir
        )
        
        assert success is True
        
        # Check all files exist
        for file_path in output_files.values():
            assert Path(file_path).exists()

    def test_workflow_output_validation(self):
        """Should validate workflow output."""
        success, errors, output_files = self.workflow.execute_full_workflow(
            title="Test",
            genre="Drama",
            platform=Platform.TIKTOK,
            target_duration_seconds=60,
            target_audience="Adults",
            output_dir=self.test_output_dir
        )
        
        assert success is True
        
        # Validate workflow state
        valid, issues = self.workflow.validate_workflow_state(self.test_output_dir)
        assert valid is True
        assert len(issues) == 0

    def test_workflow_handles_errors_gracefully(self):
        """Should handle errors gracefully."""
        # Test with invalid duration
        success, errors, output_files = self.workflow.execute_full_workflow(
            title="Test",
            genre="Drama",
            platform=Platform.TIKTOK,
            target_duration_seconds=200,  # Invalid (>120)
            target_audience="Adults",
            output_dir=self.test_output_dir
        )
        
        assert success is False
        assert len(errors) > 0

    def test_workflow_creates_output_directory(self):
        """Should create output directory if it doesn't exist."""
        output_dir = "test_new_output"
        
        try:
            success, errors, output_files = self.workflow.execute_full_workflow(
                title="Test",
                genre="Drama",
                platform=Platform.TIKTOK,
                target_duration_seconds=60,
                target_audience="Adults",
                output_dir=output_dir
            )
            
            assert success is True
            assert Path(output_dir).exists()
        finally:
            if Path(output_dir).exists():
                shutil.rmtree(output_dir)

    def test_workflow_file_content_valid(self):
        """Should generate valid file content."""
        success, errors, output_files = self.workflow.execute_full_workflow(
            title="Test",
            genre="Drama",
            platform=Platform.TIKTOK,
            target_duration_seconds=60,
            target_audience="Adults",
            output_dir=self.test_output_dir
        )
        
        assert success is True
        
        # Check script file
        script_file = Path(output_files['script'])
        script_content = script_file.read_text()
        assert "Test" in script_content
        assert "Drama" in script_content
        
        # Check storyboard file
        storyboard_file = Path(output_files['storyboard'])
        storyboard_content = storyboard_file.read_text()
        assert "# Storyboard" in storyboard_content
        assert "Scene" in storyboard_content
