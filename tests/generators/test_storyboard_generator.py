"""Tests for storyboard generator."""
import pytest
from src.generators.storyboard_generator import StoryboardGenerator, ContinuityChecker
from src.generators.script_generator import ScriptGenerator
from src.generators.breakdown_generator import BreakdownGenerator
from src.models.script import Platform


class TestStoryboardGenerator:
    """Test suite for StoryboardGenerator."""

    def setup_method(self):
        """Set up test fixtures."""
        self.generator = StoryboardGenerator()
        self.script_generator = ScriptGenerator()
        self.breakdown_generator = BreakdownGenerator()

    def test_generate_storyboard(self):
        """Should generate storyboard from script and breakdown."""
        script = self.script_generator.generate(
            title="Test",
            genre="Drama",
            platform=Platform.TIKTOK,
            target_duration_seconds=60,
            target_audience="Adults"
        )
        breakdown = self.breakdown_generator.generate(script)
        
        storyboard = self.generator.generate(script, breakdown)
        
        assert storyboard.script_title == "Test"
        assert len(storyboard.shots) > 0
        
        # Validate storyboard
        valid, error = storyboard.validate()
        assert valid is True

    def test_shots_map_to_scenes(self):
        """Should create shots that map to script scenes."""
        script = self.script_generator.generate(
            title="Test",
            genre="Drama",
            platform=Platform.TIKTOK,
            target_duration_seconds=60,
            target_audience="Adults"
        )
        breakdown = self.breakdown_generator.generate(script)
        
        storyboard = self.generator.generate(script, breakdown)
        
        # Check all shots reference valid scenes
        script_scene_numbers = {scene.scene_number for scene in script.scenes}
        for shot in storyboard.shots:
            assert shot.scene_number in script_scene_numbers

    def test_duration_within_tolerance(self):
        """Should generate storyboard with duration within ±20%."""
        script = self.script_generator.generate(
            title="Test",
            genre="Drama",
            platform=Platform.TIKTOK,
            target_duration_seconds=60,
            target_audience="Adults"
        )
        breakdown = self.breakdown_generator.generate(script)
        
        storyboard = self.generator.generate(script, breakdown)
        
        total_duration = storyboard.get_total_duration()
        deviation = abs(total_duration - script.target_duration_seconds) / script.target_duration_seconds
        
        assert deviation <= 0.20

    def test_multiple_shots_per_scene(self):
        """Should generate multiple shots per scene for coverage."""
        script = self.script_generator.generate(
            title="Test",
            genre="Drama",
            platform=Platform.TIKTOK,
            target_duration_seconds=60,
            target_audience="Adults"
        )
        breakdown = self.breakdown_generator.generate(script)
        
        storyboard = self.generator.generate(script, breakdown)
        
        # Count shots per scene
        scene_shot_counts = {}
        for shot in storyboard.shots:
            scene_shot_counts[shot.scene_number] = scene_shot_counts.get(shot.scene_number, 0) + 1
        
        # Each scene should have multiple shots
        for count in scene_shot_counts.values():
            assert count >= 2

    def test_markdown_export(self):
        """Should export storyboard to markdown."""
        script = self.script_generator.generate(
            title="Test",
            genre="Drama",
            platform=Platform.TIKTOK,
            target_duration_seconds=60,
            target_audience="Adults"
        )
        breakdown = self.breakdown_generator.generate(script)
        
        storyboard = self.generator.generate(script, breakdown)
        md = storyboard.to_markdown()
        
        assert "# Storyboard: Test" in md
        assert "Scene" in md

    def test_csv_shot_list_export(self):
        """Should export shot list to CSV."""
        script = self.script_generator.generate(
            title="Test",
            genre="Drama",
            platform=Platform.TIKTOK,
            target_duration_seconds=60,
            target_audience="Adults"
        )
        breakdown = self.breakdown_generator.generate(script)
        
        storyboard = self.generator.generate(script, breakdown)
        csv_str = storyboard.to_csv()
        
        assert "Shot ID" in csv_str
        assert "Scene" in csv_str
        assert "Duration" in csv_str


class TestContinuityChecker:
    """Test suite for ContinuityChecker."""

    def setup_method(self):
        """Set up test fixtures."""
        self.checker = ContinuityChecker()
        self.script_generator = ScriptGenerator()
        self.breakdown_generator = BreakdownGenerator()
        self.storyboard_generator = StoryboardGenerator()

    def test_check_valid_storyboard(self):
        """Should validate correct storyboard."""
        script = self.script_generator.generate(
            title="Test",
            genre="Drama",
            platform=Platform.TIKTOK,
            target_duration_seconds=60,
            target_audience="Adults"
        )
        breakdown = self.breakdown_generator.generate(script)
        storyboard = self.storyboard_generator.generate(script, breakdown)
        
        valid, issues = self.checker.check_continuity(storyboard, script)
        assert valid is True
        assert len(issues) == 0

    def test_detect_invalid_scene_reference(self):
        """Should detect shots referencing non-existent scenes."""
        script = self.script_generator.generate(
            title="Test",
            genre="Drama",
            platform=Platform.TIKTOK,
            target_duration_seconds=60,
            target_audience="Adults"
        )
        breakdown = self.breakdown_generator.generate(script)
        storyboard = self.storyboard_generator.generate(script, breakdown)
        
        # Add shot with invalid scene number
        from src.models.storyboard import Shot, ShotSize, CameraMovement
        invalid_shot = Shot(
            shot_id="99Z",
            scene_number=999,
            shot_size=ShotSize.WIDE,
            camera_position="Test",
            camera_movement=CameraMovement.STATIC,
            visual_description="Invalid",
            suggested_duration_seconds=5
        )
        storyboard.shots.append(invalid_shot)
        
        valid, issues = self.checker.check_continuity(storyboard, script)
        assert valid is False
        assert any("non-existent scene" in issue.lower() for issue in issues)
