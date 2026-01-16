"""Tests for script data models."""
import pytest
import json
from src.models.script import (
    Script, Scene, Character, Dialogue, CostFlag, Platform
)


class TestDialogue:
    """Test suite for Dialogue model."""

    def test_valid_dialogue(self):
        """Should create valid dialogue."""
        dialogue = Dialogue(
            character="Alice",
            text="Hello, world!",
            action="smiling"
        )
        
        valid, error = dialogue.validate()
        assert valid is True
        assert error is None

    def test_empty_character(self):
        """Should reject empty character name."""
        dialogue = Dialogue(character="", text="Hello")
        
        valid, error = dialogue.validate()
        assert valid is False
        assert "Character name" in error

    def test_empty_text(self):
        """Should reject empty dialogue text."""
        dialogue = Dialogue(character="Alice", text="")
        
        valid, error = dialogue.validate()
        assert valid is False
        assert "Dialogue text" in error

    def test_text_too_long(self):
        """Should reject dialogue text that's too long."""
        dialogue = Dialogue(character="Alice", text="x" * 501)
        
        valid, error = dialogue.validate()
        assert valid is False
        assert "too long" in error


class TestCharacter:
    """Test suite for Character model."""

    def test_valid_character(self):
        """Should create valid character."""
        character = Character(
            name="Alice",
            description="Protagonist",
            age_range="25-30"
        )
        
        valid, error = character.validate()
        assert valid is True
        assert error is None

    def test_empty_name(self):
        """Should reject empty character name."""
        character = Character(name="")
        
        valid, error = character.validate()
        assert valid is False
        assert "Character name" in error


class TestScene:
    """Test suite for Scene model."""

    def test_valid_scene(self):
        """Should create valid scene."""
        scene = Scene(
            scene_number=1,
            location="Coffee Shop",
            time_of_day="DAY",
            interior_exterior="INT",
            description="A busy coffee shop",
            is_hook=True
        )
        
        valid, error = scene.validate()
        assert valid is True
        assert error is None

    def test_invalid_scene_number(self):
        """Should reject invalid scene number."""
        scene = Scene(
            scene_number=0,
            location="Coffee Shop",
            time_of_day="DAY",
            interior_exterior="INT",
            description="Test"
        )
        
        valid, error = scene.validate()
        assert valid is False
        assert "Scene number" in error

    def test_invalid_time_of_day(self):
        """Should reject invalid time of day."""
        scene = Scene(
            scene_number=1,
            location="Coffee Shop",
            time_of_day="AFTERNOON",
            interior_exterior="INT",
            description="Test"
        )
        
        valid, error = scene.validate()
        assert valid is False
        assert "time_of_day" in error

    def test_invalid_interior_exterior(self):
        """Should reject invalid interior/exterior."""
        scene = Scene(
            scene_number=1,
            location="Coffee Shop",
            time_of_day="DAY",
            interior_exterior="BOTH",
            description="Test"
        )
        
        valid, error = scene.validate()
        assert valid is False
        assert "interior_exterior" in error


class TestScript:
    """Test suite for Script model."""

    def test_valid_script(self):
        """Should create valid script."""
        character = Character(name="Alice")
        dialogue = Dialogue(character="Alice", text="Hello!")
        scene = Scene(
            scene_number=1,
            location="Coffee Shop",
            time_of_day="DAY",
            interior_exterior="INT",
            description="Hook scene",
            dialogues=[dialogue],
            is_hook=True
        )
        
        script = Script(
            title="Test Script",
            genre="Drama",
            platform=Platform.TIKTOK,
            target_duration_seconds=60,
            target_audience="Young adults",
            characters=[character],
            scenes=[scene]
        )
        
        valid, error = script.validate()
        assert valid is True
        assert error is None

    def test_missing_hook(self):
        """Should reject script without hook."""
        character = Character(name="Alice")
        scene = Scene(
            scene_number=1,
            location="Coffee Shop",
            time_of_day="DAY",
            interior_exterior="INT",
            description="Regular scene",
            is_hook=False
        )
        
        script = Script(
            title="Test Script",
            genre="Drama",
            platform=Platform.TIKTOK,
            target_duration_seconds=60,
            target_audience="Young adults",
            characters=[character],
            scenes=[scene]
        )
        
        valid, error = script.validate()
        assert valid is False
        assert "hook" in error.lower()

    def test_invalid_duration(self):
        """Should reject invalid duration."""
        script = Script(
            title="Test Script",
            genre="Drama",
            platform=Platform.TIKTOK,
            target_duration_seconds=200,
            target_audience="Young adults"
        )
        
        valid, error = script.validate()
        assert valid is False
        assert "duration" in error.lower()

    def test_character_not_in_list(self):
        """Should reject dialogue from unlisted character."""
        character = Character(name="Alice")
        dialogue = Dialogue(character="Bob", text="Hello!")
        scene = Scene(
            scene_number=1,
            location="Coffee Shop",
            time_of_day="DAY",
            interior_exterior="INT",
            description="Hook scene",
            dialogues=[dialogue],
            is_hook=True
        )
        
        script = Script(
            title="Test Script",
            genre="Drama",
            platform=Platform.TIKTOK,
            target_duration_seconds=60,
            target_audience="Young adults",
            characters=[character],
            scenes=[scene]
        )
        
        valid, error = script.validate()
        assert valid is False
        assert "Bob" in error
        assert "not in character list" in error

    def test_serialization(self):
        """Should serialize and deserialize correctly."""
        character = Character(name="Alice")
        dialogue = Dialogue(character="Alice", text="Hello!")
        scene = Scene(
            scene_number=1,
            location="Coffee Shop",
            time_of_day="DAY",
            interior_exterior="INT",
            description="Hook scene",
            dialogues=[dialogue],
            is_hook=True
        )
        
        script = Script(
            title="Test Script",
            genre="Drama",
            platform=Platform.TIKTOK,
            target_duration_seconds=60,
            target_audience="Young adults",
            characters=[character],
            scenes=[scene]
        )
        
        # To JSON and back
        json_str = script.to_json()
        restored = Script.from_json(json_str)
        
        assert restored.title == script.title
        assert restored.genre == script.genre
        assert restored.platform == script.platform
        assert len(restored.characters) == 1
        assert len(restored.scenes) == 1
        assert restored.scenes[0].dialogues[0].text == "Hello!"
