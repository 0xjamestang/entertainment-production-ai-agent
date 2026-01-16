"""Tests for breakdown generator."""
import pytest
from src.generators.breakdown_generator import BreakdownGenerator, BreakdownValidator
from src.generators.script_generator import ScriptGenerator
from src.models.script import Platform


class TestBreakdownGenerator:
    """Test suite for BreakdownGenerator."""

    def setup_method(self):
        """Set up test fixtures."""
        self.generator = BreakdownGenerator()
        self.script_generator = ScriptGenerator()

    def test_generate_breakdown(self):
        """Should generate breakdown from script."""
        script = self.script_generator.generate(
            title="Test Script",
            genre="Drama",
            platform=Platform.TIKTOK,
            target_duration_seconds=60,
            target_audience="Young adults"
        )
        
        breakdown = self.generator.generate(script)
        
        assert breakdown.script_title == "Test Script"
        assert len(breakdown.entries) == len(script.scenes)
        
        # Validate breakdown
        valid, error = breakdown.validate()
        assert valid is True

    def test_one_to_one_scene_mapping(self):
        """Should maintain 1:1 scene-to-breakdown mapping."""
        script = self.script_generator.generate(
            title="Test",
            genre="Drama",
            platform=Platform.TIKTOK,
            target_duration_seconds=60,
            target_audience="Adults"
        )
        
        breakdown = self.generator.generate(script)
        
        # Check each scene has exactly one breakdown entry
        script_scene_numbers = {scene.scene_number for scene in script.scenes}
        breakdown_scene_numbers = {entry.scene_number for entry in breakdown.entries}
        
        assert script_scene_numbers == breakdown_scene_numbers

    def test_extract_characters(self):
        """Should extract characters from scenes."""
        script = self.script_generator.generate(
            title="Test",
            genre="Drama",
            platform=Platform.TIKTOK,
            target_duration_seconds=60,
            target_audience="Adults"
        )
        
        breakdown = self.generator.generate(script)
        
        # All entries should have characters
        for entry in breakdown.entries:
            assert len(entry.characters) > 0

    def test_extract_production_elements(self):
        """Should extract production elements."""
        script = self.script_generator.generate(
            title="Test",
            genre="Drama",
            platform=Platform.TIKTOK,
            target_duration_seconds=60,
            target_audience="Adults"
        )
        
        breakdown = self.generator.generate(script)
        
        # Check that wardrobe is extracted for all entries
        for entry in breakdown.entries:
            assert len(entry.wardrobe) > 0  # At least basic wardrobe

    def test_estimate_setup_time(self):
        """Should estimate setup time for scenes."""
        script = self.script_generator.generate(
            title="Test",
            genre="Drama",
            platform=Platform.TIKTOK,
            target_duration_seconds=60,
            target_audience="Adults"
        )
        
        breakdown = self.generator.generate(script)
        
        # All entries should have setup time
        for entry in breakdown.entries:
            assert entry.estimated_setup_time_minutes is not None
            assert entry.estimated_setup_time_minutes > 0

    def test_json_export(self):
        """Should export breakdown to JSON."""
        script = self.script_generator.generate(
            title="Test",
            genre="Drama",
            platform=Platform.TIKTOK,
            target_duration_seconds=60,
            target_audience="Adults"
        )
        
        breakdown = self.generator.generate(script)
        json_str = breakdown.to_json()
        
        assert "Test" in json_str
        assert "scene_number" in json_str

    def test_csv_export(self):
        """Should export breakdown to CSV."""
        script = self.script_generator.generate(
            title="Test",
            genre="Drama",
            platform=Platform.TIKTOK,
            target_duration_seconds=60,
            target_audience="Adults"
        )
        
        breakdown = self.generator.generate(script)
        csv_str = breakdown.to_csv()
        
        assert "Scene Number" in csv_str
        assert "Location" in csv_str
        assert "Characters" in csv_str


class TestBreakdownValidator:
    """Test suite for BreakdownValidator."""

    def setup_method(self):
        """Set up test fixtures."""
        self.validator = BreakdownValidator()
        self.script_generator = ScriptGenerator()
        self.breakdown_generator = BreakdownGenerator()

    def test_validate_generated_breakdown(self):
        """Should validate generated breakdown against script."""
        script = self.script_generator.generate(
            title="Test",
            genre="Drama",
            platform=Platform.TIKTOK,
            target_duration_seconds=60,
            target_audience="Adults"
        )
        
        breakdown = self.breakdown_generator.generate(script)
        
        valid, issues = self.validator.validate_against_script(breakdown, script)
        assert valid is True
        assert len(issues) == 0

    def test_detect_missing_scenes(self):
        """Should detect missing breakdown entries."""
        script = self.script_generator.generate(
            title="Test",
            genre="Drama",
            platform=Platform.TIKTOK,
            target_duration_seconds=60,
            target_audience="Adults"
        )
        
        breakdown = self.breakdown_generator.generate(script)
        
        # Remove an entry
        breakdown.entries = breakdown.entries[:-1]
        
        valid, issues = self.validator.validate_against_script(breakdown, script)
        assert valid is False
        assert any("missing" in issue.lower() for issue in issues)

    def test_detect_scene_count_mismatch(self):
        """Should detect scene count mismatch."""
        script = self.script_generator.generate(
            title="Test",
            genre="Drama",
            platform=Platform.TIKTOK,
            target_duration_seconds=60,
            target_audience="Adults"
        )
        
        breakdown = self.breakdown_generator.generate(script)
        
        # Add extra entry
        extra_entry = breakdown.entries[0]
        breakdown.entries.append(extra_entry)
        
        valid, issues = self.validator.validate_against_script(breakdown, script)
        assert valid is False
        assert any("mismatch" in issue.lower() or "duplicate" in issue.lower() for issue in issues)
