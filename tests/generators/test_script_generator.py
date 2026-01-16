"""Tests for script generator."""
import pytest
from src.generators.script_generator import ScriptGenerator, ScriptValidator
from src.models.script import Platform


class TestScriptGenerator:
    """Test suite for ScriptGenerator."""

    def setup_method(self):
        """Set up test fixtures."""
        self.generator = ScriptGenerator()

    def test_generate_basic_script(self):
        """Should generate a basic script."""
        script = self.generator.generate(
            title="Test Drama",
            genre="Drama",
            platform=Platform.TIKTOK,
            target_duration_seconds=60,
            target_audience="Young adults 18-25"
        )
        
        assert script.title == "Test Drama"
        assert script.genre == "Drama"
        assert len(script.characters) > 0
        assert len(script.scenes) > 0
        
        # Check for hook
        assert any(scene.is_hook for scene in script.scenes)
        assert script.scenes[0].is_hook  # Hook should be first scene

    def test_generate_validates(self):
        """Generated script should pass validation."""
        script = self.generator.generate(
            title="Test Script",
            genre="Comedy",
            platform=Platform.YOUTUBE_SHORTS,
            target_duration_seconds=45,
            target_audience="Teens"
        )
        
        valid, error = script.validate()
        assert valid is True
        assert error is None

    def test_generate_different_genres(self):
        """Should generate different characters for different genres."""
        drama_script = self.generator.generate(
            title="Drama",
            genre="Drama",
            platform=Platform.TIKTOK,
            target_duration_seconds=60,
            target_audience="Adults"
        )
        
        comedy_script = self.generator.generate(
            title="Comedy",
            genre="Comedy",
            platform=Platform.TIKTOK,
            target_duration_seconds=60,
            target_audience="Adults"
        )
        
        # Different genres should have different character setups
        assert drama_script.characters[0].name != comedy_script.characters[0].name

    def test_generate_respects_duration(self):
        """Should generate appropriate number of scenes for duration."""
        short_script = self.generator.generate(
            title="Short",
            genre="Drama",
            platform=Platform.TIKTOK,
            target_duration_seconds=30,
            target_audience="Adults"
        )
        
        long_script = self.generator.generate(
            title="Long",
            genre="Drama",
            platform=Platform.TIKTOK,
            target_duration_seconds=90,
            target_audience="Adults"
        )
        
        # Longer scripts should have more scenes
        assert len(long_script.scenes) >= len(short_script.scenes)

    def test_identify_cost_flags(self):
        """Should identify cost flags in generated scripts."""
        script = self.generator.generate(
            title="Test",
            genre="Drama",
            platform=Platform.TIKTOK,
            target_duration_seconds=60,
            target_audience="Adults"
        )
        
        # Cost flags should be identified
        assert isinstance(script.cost_flags, list)


class TestScriptValidator:
    """Test suite for ScriptValidator."""

    def setup_method(self):
        """Set up test fixtures."""
        self.validator = ScriptValidator()
        self.generator = ScriptGenerator()

    def test_validate_generated_script(self):
        """Should validate generated scripts."""
        script = self.generator.generate(
            title="Test",
            genre="Drama",
            platform=Platform.TIKTOK,
            target_duration_seconds=60,
            target_audience="Adults"
        )
        
        valid, issues = self.validator.validate_for_production(script)
        assert valid is True
        assert len(issues) == 0

    def test_detect_long_dialogue(self):
        """Should detect overly long dialogue."""
        script = self.generator.generate(
            title="Test",
            genre="Drama",
            platform=Platform.TIKTOK,
            target_duration_seconds=60,
            target_audience="Adults"
        )
        
        # Add a very long dialogue
        script.scenes[0].dialogues[0].text = " ".join(["word"] * 60)
        
        valid, issues = self.validator.validate_for_production(script)
        assert valid is False
        assert any("too long" in issue.lower() for issue in issues)

    def test_detect_duration_deviation(self):
        """Should detect significant duration deviation."""
        script = self.generator.generate(
            title="Test",
            genre="Drama",
            platform=Platform.TIKTOK,
            target_duration_seconds=60,
            target_audience="Adults"
        )
        
        # Set unrealistic durations
        for scene in script.scenes:
            scene.estimated_duration_seconds = 100
        
        valid, issues = self.validator.validate_for_production(script)
        assert valid is False
        assert any("duration" in issue.lower() for issue in issues)
