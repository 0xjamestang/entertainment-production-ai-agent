"""Script data models for entertainment production."""
from dataclasses import dataclass, field, asdict
from typing import List, Optional
from enum import Enum
import json


class Platform(Enum):
    """Target platform for short-form content."""
    TIKTOK = "tiktok"
    KUAISHOU = "kuaishou"
    YOUTUBE_SHORTS = "youtube_shorts"
    INSTAGRAM_REELS = "instagram_reels"


@dataclass
class Dialogue:
    """Represents a line of dialogue."""
    character: str
    text: str
    action: Optional[str] = None  # Stage direction or action during dialogue
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """Validate dialogue."""
        if not self.character or not self.character.strip():
            return False, "Character name cannot be empty"
        if not self.text or not self.text.strip():
            return False, "Dialogue text cannot be empty"
        if len(self.text) > 500:
            return False, "Dialogue text too long (max 500 characters)"
        return True, None


@dataclass
class Character:
    """Represents a character in the script."""
    name: str
    description: Optional[str] = None
    age_range: Optional[str] = None
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """Validate character."""
        if not self.name or not self.name.strip():
            return False, "Character name cannot be empty"
        return True, None


@dataclass
class Scene:
    """Represents a scene in the script."""
    scene_number: int
    location: str
    time_of_day: str  # "DAY", "NIGHT", "DAWN", "DUSK"
    interior_exterior: str  # "INT", "EXT"
    description: str
    dialogues: List[Dialogue] = field(default_factory=list)
    estimated_duration_seconds: Optional[int] = None
    is_hook: bool = False  # True if this is the hook scene (first 3-5 seconds)
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """Validate scene."""
        if self.scene_number < 1:
            return False, "Scene number must be positive"
        if not self.location or not self.location.strip():
            return False, "Location cannot be empty"
        if self.time_of_day not in ["DAY", "NIGHT", "DAWN", "DUSK"]:
            return False, f"Invalid time_of_day: {self.time_of_day}"
        if self.interior_exterior not in ["INT", "EXT"]:
            return False, f"Invalid interior_exterior: {self.interior_exterior}"
        
        # Validate all dialogues
        for dialogue in self.dialogues:
            valid, error = dialogue.validate()
            if not valid:
                return False, f"Scene {self.scene_number}: {error}"
        
        return True, None


@dataclass
class CostFlag:
    """Flags for high-cost production elements."""
    element_type: str  # "location", "extras", "night_scene", "vfx", "stunts", etc.
    description: str
    estimated_complexity: str  # "LOW", "MEDIUM", "HIGH"


@dataclass
class Script:
    """Represents a complete script."""
    title: str
    genre: str
    platform: Platform
    target_duration_seconds: int  # 30-120 seconds
    target_audience: str
    characters: List[Character] = field(default_factory=list)
    scenes: List[Scene] = field(default_factory=list)
    cost_flags: List[CostFlag] = field(default_factory=list)
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """Validate script."""
        if not self.title or not self.title.strip():
            return False, "Title cannot be empty"
        if not self.genre or not self.genre.strip():
            return False, "Genre cannot be empty"
        if not (30 <= self.target_duration_seconds <= 120):
            return False, "Target duration must be between 30-120 seconds"
        if not self.target_audience or not self.target_audience.strip():
            return False, "Target audience cannot be empty"
        
        if not self.scenes:
            return False, "Script must have at least one scene"
        
        # Check for hook scene in first 3-5 seconds
        has_hook = any(scene.is_hook for scene in self.scenes[:2])
        if not has_hook:
            return False, "Script must have a hook in the first scene"
        
        # Validate all characters
        for character in self.characters:
            valid, error = character.validate()
            if not valid:
                return False, error
        
        # Validate all scenes
        for scene in self.scenes:
            valid, error = scene.validate()
            if not valid:
                return False, error
        
        # Check that all dialogue characters exist in character list
        character_names = {char.name for char in self.characters}
        for scene in self.scenes:
            for dialogue in scene.dialogues:
                if dialogue.character not in character_names:
                    return False, f"Character '{dialogue.character}' in scene {scene.scene_number} not in character list"
        
        return True, None
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "title": self.title,
            "genre": self.genre,
            "platform": self.platform.value,
            "target_duration_seconds": self.target_duration_seconds,
            "target_audience": self.target_audience,
            "characters": [asdict(char) for char in self.characters],
            "scenes": [asdict(scene) for scene in self.scenes],
            "cost_flags": [asdict(flag) for flag in self.cost_flags]
        }
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Script':
        """Create from dictionary."""
        return cls(
            title=data["title"],
            genre=data["genre"],
            platform=Platform(data["platform"]),
            target_duration_seconds=data["target_duration_seconds"],
            target_audience=data["target_audience"],
            characters=[Character(**char) for char in data.get("characters", [])],
            scenes=[
                Scene(
                    **{**scene, "dialogues": [Dialogue(**d) for d in scene.get("dialogues", [])]}
                )
                for scene in data.get("scenes", [])
            ],
            cost_flags=[CostFlag(**flag) for flag in data.get("cost_flags", [])]
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> 'Script':
        """Create from JSON string."""
        return cls.from_dict(json.loads(json_str))
