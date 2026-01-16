"""Tests for storyboard data models."""
import pytest
from src.models.storyboard import Storyboard, Shot, ShotSize, CameraMovement


class TestShot:
    """Test suite for Shot model."""

    def test_valid_shot(self):
        """Should create valid shot."""
        shot = Shot(
            shot_id="1A",
            scene_number=1,
            shot_size=ShotSize.WIDE,
            camera_position="Eye level",
            camera_movement=CameraMovement.STATIC,
            visual_description="Opening shot",
            suggested_duration_seconds=3
        )
        
        valid, error = shot.validate()
        assert valid is True
        assert error is None

    def test_invalid_duration(self):
        """Should reject invalid duration."""
        shot = Shot(
            shot_id="1A",
            scene_number=1,
            shot_size=ShotSize.WIDE,
            camera_position="Eye level",
            camera_movement=CameraMovement.STATIC,
            visual_description="Test",
            suggested_duration_seconds=0
        )
        
        valid, error = shot.validate()
        assert valid is False
        assert "duration" in error.lower()


class TestStoryboard:
    """Test suite for Storyboard model."""

    def test_valid_storyboard(self):
        """Should create valid storyboard."""
        shot = Shot(
            shot_id="1A",
            scene_number=1,
            shot_size=ShotSize.WIDE,
            camera_position="Eye level",
            camera_movement=CameraMovement.STATIC,
            visual_description="Opening",
            suggested_duration_seconds=30
        )
        
        storyboard = Storyboard(
            script_title="Test",
            target_duration_seconds=30,
            shots=[shot]
        )
        
        valid, error = storyboard.validate()
        assert valid is True
        assert error is None

    def test_duration_tolerance(self):
        """Should enforce 20% duration tolerance."""
        shot = Shot(
            shot_id="1A",
            scene_number=1,
            shot_size=ShotSize.WIDE,
            camera_position="Eye level",
            camera_movement=CameraMovement.STATIC,
            visual_description="Test",
            suggested_duration_seconds=100
        )
        
        storyboard = Storyboard(
            script_title="Test",
            target_duration_seconds=60,
            shots=[shot]
        )
        
        valid, error = storyboard.validate()
        assert valid is False
        assert "20%" in error

    def test_duplicate_shot_ids(self):
        """Should reject duplicate shot IDs."""
        shot1 = Shot(
            shot_id="1A",
            scene_number=1,
            shot_size=ShotSize.WIDE,
            camera_position="Eye level",
            camera_movement=CameraMovement.STATIC,
            visual_description="Shot 1",
            suggested_duration_seconds=15
        )
        shot2 = Shot(
            shot_id="1A",
            scene_number=1,
            shot_size=ShotSize.CLOSE_UP,
            camera_position="Eye level",
            camera_movement=CameraMovement.STATIC,
            visual_description="Shot 2",
            suggested_duration_seconds=15
        )
        
        storyboard = Storyboard(
            script_title="Test",
            target_duration_seconds=30,
            shots=[shot1, shot2]
        )
        
        valid, error = storyboard.validate()
        assert valid is False
        assert "Duplicate" in error

    def test_json_serialization(self):
        """Should serialize to and from JSON."""
        shot = Shot(
            shot_id="1A",
            scene_number=1,
            shot_size=ShotSize.WIDE,
            camera_position="Eye level",
            camera_movement=CameraMovement.STATIC,
            visual_description="Test",
            suggested_duration_seconds=30
        )
        
        storyboard = Storyboard(
            script_title="Test",
            target_duration_seconds=30,
            shots=[shot]
        )
        
        json_str = storyboard.to_json()
        restored = Storyboard.from_json(json_str)
        
        assert restored.script_title == storyboard.script_title
        assert len(restored.shots) == 1
        assert restored.shots[0].shot_id == "1A"

    def test_markdown_export(self):
        """Should export to markdown format."""
        shot = Shot(
            shot_id="1A",
            scene_number=1,
            shot_size=ShotSize.WIDE,
            camera_position="Eye level",
            camera_movement=CameraMovement.STATIC,
            visual_description="Opening shot",
            suggested_duration_seconds=30
        )
        
        storyboard = Storyboard(
            script_title="Test",
            target_duration_seconds=30,
            shots=[shot]
        )
        
        md = storyboard.to_markdown()
        
        assert "# Storyboard: Test" in md
        assert "Shot 1A" in md
        assert "Opening shot" in md

    def test_csv_export(self):
        """Should export to CSV shot list."""
        shot = Shot(
            shot_id="1A",
            scene_number=1,
            shot_size=ShotSize.WIDE,
            camera_position="Eye level",
            camera_movement=CameraMovement.STATIC,
            visual_description="Opening",
            suggested_duration_seconds=30
        )
        
        storyboard = Storyboard(
            script_title="Test",
            target_duration_seconds=30,
            shots=[shot]
        )
        
        csv_str = storyboard.to_csv()
        
        assert "Shot ID" in csv_str
        assert "1A" in csv_str
        assert "Opening" in csv_str
