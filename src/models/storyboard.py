"""Storyboard and shot list data models."""
from dataclasses import dataclass, field, asdict
from typing import List, Optional
from enum import Enum
import json
import csv
from io import StringIO


class ShotSize(Enum):
    """Shot size classifications."""
    EXTREME_WIDE = "EWS"
    WIDE = "WS"
    MEDIUM = "MS"
    CLOSE_UP = "CU"
    EXTREME_CLOSE_UP = "ECU"


class CameraMovement(Enum):
    """Camera movement types."""
    STATIC = "Static"
    PAN = "Pan"
    TILT = "Tilt"
    DOLLY = "Dolly"
    TRACKING = "Tracking"
    HANDHELD = "Handheld"
    CRANE = "Crane"


@dataclass
class Shot:
    """Represents a single shot in the storyboard."""
    shot_id: str  # e.g., "1A", "2B"
    scene_number: int
    shot_size: ShotSize
    camera_position: str
    camera_movement: CameraMovement
    visual_description: str
    suggested_duration_seconds: int
    audio_notes: Optional[str] = None
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """Validate shot."""
        if not self.shot_id or not self.shot_id.strip():
            return False, "Shot ID cannot be empty"
        if self.scene_number < 1:
            return False, "Scene number must be positive"
        if not self.camera_position or not self.camera_position.strip():
            return False, "Camera position cannot be empty"
        if not self.visual_description or not self.visual_description.strip():
            return False, "Visual description cannot be empty"
        if self.suggested_duration_seconds < 1:
            return False, "Duration must be at least 1 second"
        return True, None
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "shot_id": self.shot_id,
            "scene_number": self.scene_number,
            "shot_size": self.shot_size.value,
            "camera_position": self.camera_position,
            "camera_movement": self.camera_movement.value,
            "visual_description": self.visual_description,
            "suggested_duration_seconds": self.suggested_duration_seconds,
            "audio_notes": self.audio_notes
        }


@dataclass
class Storyboard:
    """Represents a complete storyboard."""
    script_title: str
    target_duration_seconds: int
    shots: List[Shot] = field(default_factory=list)
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """Validate storyboard."""
        if not self.script_title or not self.script_title.strip():
            return False, "Script title cannot be empty"
        
        if not self.shots:
            return False, "Storyboard must have at least one shot"
        
        # Validate all shots
        for shot in self.shots:
            valid, error = shot.validate()
            if not valid:
                return False, f"Shot {shot.shot_id}: {error}"
        
        # Check shot IDs are unique
        shot_ids = [shot.shot_id for shot in self.shots]
        if len(shot_ids) != len(set(shot_ids)):
            return False, "Duplicate shot IDs found"
        
        # Check total duration is within tolerance (±20%)
        total_duration = sum(shot.suggested_duration_seconds for shot in self.shots)
        deviation = abs(total_duration - self.target_duration_seconds) / self.target_duration_seconds
        if deviation > 0.20:
            return False, (
                f"Total duration ({total_duration}s) deviates more than 20% "
                f"from target ({self.target_duration_seconds}s)"
            )
        
        return True, None
    
    def get_total_duration(self) -> int:
        """Get total estimated duration."""
        return sum(shot.suggested_duration_seconds for shot in self.shots)
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "script_title": self.script_title,
            "target_duration_seconds": self.target_duration_seconds,
            "shots": [shot.to_dict() for shot in self.shots]
        }
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    def to_markdown(self) -> str:
        """Convert to markdown format."""
        lines = [
            f"# Storyboard: {self.script_title}",
            f"",
            f"**Target Duration:** {self.target_duration_seconds}s",
            f"**Total Estimated Duration:** {self.get_total_duration()}s",
            f"",
            "---",
            ""
        ]
        
        current_scene = None
        for shot in self.shots:
            if shot.scene_number != current_scene:
                current_scene = shot.scene_number
                lines.append(f"## Scene {current_scene}")
                lines.append("")
            
            lines.append(f"### Shot {shot.shot_id}")
            lines.append(f"- **Size:** {shot.shot_size.value}")
            lines.append(f"- **Camera:** {shot.camera_position}")
            lines.append(f"- **Movement:** {shot.camera_movement.value}")
            lines.append(f"- **Duration:** {shot.suggested_duration_seconds}s")
            lines.append(f"- **Description:** {shot.visual_description}")
            if shot.audio_notes:
                lines.append(f"- **Audio:** {shot.audio_notes}")
            lines.append("")
        
        return "\n".join(lines)
    
    def to_csv(self) -> str:
        """Convert to CSV shot list."""
        output = StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow([
            "Shot ID",
            "Scene",
            "Shot Size",
            "Camera Position",
            "Camera Movement",
            "Duration (s)",
            "Visual Description",
            "Audio Notes"
        ])
        
        # Data rows
        for shot in self.shots:
            writer.writerow([
                shot.shot_id,
                shot.scene_number,
                shot.shot_size.value,
                shot.camera_position,
                shot.camera_movement.value,
                shot.suggested_duration_seconds,
                shot.visual_description,
                shot.audio_notes or ""
            ])
        
        return output.getvalue()
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Storyboard':
        """Create from dictionary."""
        return cls(
            script_title=data["script_title"],
            target_duration_seconds=data["target_duration_seconds"],
            shots=[
                Shot(
                    shot_id=s["shot_id"],
                    scene_number=s["scene_number"],
                    shot_size=ShotSize(s["shot_size"]),
                    camera_position=s["camera_position"],
                    camera_movement=CameraMovement(s["camera_movement"]),
                    visual_description=s["visual_description"],
                    suggested_duration_seconds=s["suggested_duration_seconds"],
                    audio_notes=s.get("audio_notes")
                )
                for s in data.get("shots", [])
            ]
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> 'Storyboard':
        """Create from JSON string."""
        return cls.from_dict(json.loads(json_str))
