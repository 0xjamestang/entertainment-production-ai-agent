"""Breakdown data models for production planning."""
from dataclasses import dataclass, field, asdict
from typing import List, Optional
from enum import Enum
import json
import csv
from io import StringIO


class LocationType(Enum):
    """Location type for scenes."""
    INTERIOR = "INT"
    EXTERIOR = "EXT"


class TimeOfDay(Enum):
    """Time of day for scenes."""
    DAY = "DAY"
    NIGHT = "NIGHT"
    DAWN = "DAWN"
    DUSK = "DUSK"


@dataclass
class ProductionElement:
    """Represents a production element (prop, wardrobe, etc.)."""
    element_type: str  # "prop", "wardrobe", "makeup", "sfx", "vehicle", "animal", etc.
    description: str
    quantity: int = 1
    notes: Optional[str] = None


@dataclass
class BreakdownEntry:
    """Represents a breakdown entry for a single scene."""
    scene_number: int
    scene_description: str
    location: str
    location_type: LocationType
    time_of_day: TimeOfDay
    characters: List[str] = field(default_factory=list)
    props: List[ProductionElement] = field(default_factory=list)
    wardrobe: List[ProductionElement] = field(default_factory=list)
    makeup: List[ProductionElement] = field(default_factory=list)
    special_requirements: List[ProductionElement] = field(default_factory=list)
    estimated_setup_time_minutes: Optional[int] = None
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """Validate breakdown entry."""
        if self.scene_number < 1:
            return False, "Scene number must be positive"
        if not self.location or not self.location.strip():
            return False, "Location cannot be empty"
        if not self.scene_description or not self.scene_description.strip():
            return False, "Scene description cannot be empty"
        if not self.characters:
            return False, f"Scene {self.scene_number} must have at least one character"
        return True, None
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "scene_number": self.scene_number,
            "scene_description": self.scene_description,
            "location": self.location,
            "location_type": self.location_type.value,
            "time_of_day": self.time_of_day.value,
            "characters": self.characters,
            "props": [asdict(p) for p in self.props],
            "wardrobe": [asdict(w) for w in self.wardrobe],
            "makeup": [asdict(m) for m in self.makeup],
            "special_requirements": [asdict(s) for s in self.special_requirements],
            "estimated_setup_time_minutes": self.estimated_setup_time_minutes
        }


@dataclass
class Breakdown:
    """Represents a complete script breakdown."""
    script_title: str
    entries: List[BreakdownEntry] = field(default_factory=list)
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """Validate breakdown."""
        if not self.script_title or not self.script_title.strip():
            return False, "Script title cannot be empty"
        
        if not self.entries:
            return False, "Breakdown must have at least one entry"
        
        # Validate all entries
        for entry in self.entries:
            valid, error = entry.validate()
            if not valid:
                return False, error
        
        # Check for duplicate scene numbers
        scene_numbers = [entry.scene_number for entry in self.entries]
        if len(scene_numbers) != len(set(scene_numbers)):
            return False, "Duplicate scene numbers found in breakdown"
        
        # Check scene numbers are sequential
        sorted_numbers = sorted(scene_numbers)
        if sorted_numbers != list(range(1, len(sorted_numbers) + 1)):
            return False, "Scene numbers must be sequential starting from 1"
        
        return True, None
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "script_title": self.script_title,
            "entries": [entry.to_dict() for entry in self.entries]
        }
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    def to_csv(self) -> str:
        """Convert to CSV string."""
        output = StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow([
            "Scene Number",
            "Location",
            "Location Type",
            "Time of Day",
            "Characters",
            "Props",
            "Wardrobe",
            "Makeup",
            "Special Requirements",
            "Setup Time (min)",
            "Description"
        ])
        
        # Data rows
        for entry in self.entries:
            writer.writerow([
                entry.scene_number,
                entry.location,
                entry.location_type.value,
                entry.time_of_day.value,
                "; ".join(entry.characters),
                "; ".join([f"{p.description} ({p.quantity})" for p in entry.props]),
                "; ".join([f"{w.description} ({w.quantity})" for w in entry.wardrobe]),
                "; ".join([f"{m.description} ({m.quantity})" for m in entry.makeup]),
                "; ".join([f"{s.description}" for s in entry.special_requirements]),
                entry.estimated_setup_time_minutes or "",
                entry.scene_description
            ])
        
        return output.getvalue()
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Breakdown':
        """Create from dictionary."""
        return cls(
            script_title=data["script_title"],
            entries=[
                BreakdownEntry(
                    scene_number=e["scene_number"],
                    scene_description=e["scene_description"],
                    location=e["location"],
                    location_type=LocationType(e["location_type"]),
                    time_of_day=TimeOfDay(e["time_of_day"]),
                    characters=e.get("characters", []),
                    props=[ProductionElement(**p) for p in e.get("props", [])],
                    wardrobe=[ProductionElement(**w) for w in e.get("wardrobe", [])],
                    makeup=[ProductionElement(**m) for m in e.get("makeup", [])],
                    special_requirements=[ProductionElement(**s) for s in e.get("special_requirements", [])],
                    estimated_setup_time_minutes=e.get("estimated_setup_time_minutes")
                )
                for e in data.get("entries", [])
            ]
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> 'Breakdown':
        """Create from JSON string."""
        return cls.from_dict(json.loads(json_str))
