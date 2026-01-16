"""Tests for breakdown data models."""
import pytest
from src.models.breakdown import (
    Breakdown, BreakdownEntry, ProductionElement, LocationType, TimeOfDay
)


class TestProductionElement:
    """Test suite for ProductionElement."""

    def test_create_production_element(self):
        """Should create production element."""
        element = ProductionElement(
            element_type="prop",
            description="Coffee cup",
            quantity=2,
            notes="Disposable"
        )
        
        assert element.element_type == "prop"
        assert element.description == "Coffee cup"
        assert element.quantity == 2
        assert element.notes == "Disposable"


class TestBreakdownEntry:
    """Test suite for BreakdownEntry."""

    def test_valid_breakdown_entry(self):
        """Should create valid breakdown entry."""
        entry = BreakdownEntry(
            scene_number=1,
            scene_description="Opening scene",
            location="Coffee Shop",
            location_type=LocationType.INTERIOR,
            time_of_day=TimeOfDay.DAY,
            characters=["Alice", "Bob"]
        )
        
        valid, error = entry.validate()
        assert valid is True
        assert error is None

    def test_invalid_scene_number(self):
        """Should reject invalid scene number."""
        entry = BreakdownEntry(
            scene_number=0,
            scene_description="Test",
            location="Location",
            location_type=LocationType.INTERIOR,
            time_of_day=TimeOfDay.DAY,
            characters=["Alice"]
        )
        
        valid, error = entry.validate()
        assert valid is False
        assert "Scene number" in error

    def test_missing_characters(self):
        """Should reject entry without characters."""
        entry = BreakdownEntry(
            scene_number=1,
            scene_description="Test",
            location="Location",
            location_type=LocationType.INTERIOR,
            time_of_day=TimeOfDay.DAY,
            characters=[]
        )
        
        valid, error = entry.validate()
        assert valid is False
        assert "character" in error.lower()

    def test_to_dict(self):
        """Should convert to dictionary."""
        entry = BreakdownEntry(
            scene_number=1,
            scene_description="Test scene",
            location="Location",
            location_type=LocationType.INTERIOR,
            time_of_day=TimeOfDay.DAY,
            characters=["Alice"],
            props=[ProductionElement("prop", "Cup", 1)]
        )
        
        data = entry.to_dict()
        assert data["scene_number"] == 1
        assert data["location_type"] == "INT"
        assert len(data["props"]) == 1


class TestBreakdown:
    """Test suite for Breakdown."""

    def test_valid_breakdown(self):
        """Should create valid breakdown."""
        entry = BreakdownEntry(
            scene_number=1,
            scene_description="Scene 1",
            location="Location",
            location_type=LocationType.INTERIOR,
            time_of_day=TimeOfDay.DAY,
            characters=["Alice"]
        )
        
        breakdown = Breakdown(
            script_title="Test Script",
            entries=[entry]
        )
        
        valid, error = breakdown.validate()
        assert valid is True
        assert error is None

    def test_empty_breakdown(self):
        """Should reject empty breakdown."""
        breakdown = Breakdown(
            script_title="Test",
            entries=[]
        )
        
        valid, error = breakdown.validate()
        assert valid is False
        assert "at least one entry" in error

    def test_duplicate_scene_numbers(self):
        """Should reject duplicate scene numbers."""
        entry1 = BreakdownEntry(
            scene_number=1,
            scene_description="Scene 1",
            location="Location",
            location_type=LocationType.INTERIOR,
            time_of_day=TimeOfDay.DAY,
            characters=["Alice"]
        )
        entry2 = BreakdownEntry(
            scene_number=1,
            scene_description="Scene 1 duplicate",
            location="Location",
            location_type=LocationType.INTERIOR,
            time_of_day=TimeOfDay.DAY,
            characters=["Bob"]
        )
        
        breakdown = Breakdown(
            script_title="Test",
            entries=[entry1, entry2]
        )
        
        valid, error = breakdown.validate()
        assert valid is False
        assert "Duplicate" in error

    def test_non_sequential_scenes(self):
        """Should reject non-sequential scene numbers."""
        entry1 = BreakdownEntry(
            scene_number=1,
            scene_description="Scene 1",
            location="Location",
            location_type=LocationType.INTERIOR,
            time_of_day=TimeOfDay.DAY,
            characters=["Alice"]
        )
        entry2 = BreakdownEntry(
            scene_number=3,
            scene_description="Scene 3",
            location="Location",
            location_type=LocationType.INTERIOR,
            time_of_day=TimeOfDay.DAY,
            characters=["Bob"]
        )
        
        breakdown = Breakdown(
            script_title="Test",
            entries=[entry1, entry2]
        )
        
        valid, error = breakdown.validate()
        assert valid is False
        assert "sequential" in error.lower()

    def test_json_serialization(self):
        """Should serialize to and from JSON."""
        entry = BreakdownEntry(
            scene_number=1,
            scene_description="Test scene",
            location="Location",
            location_type=LocationType.INTERIOR,
            time_of_day=TimeOfDay.DAY,
            characters=["Alice"],
            props=[ProductionElement("prop", "Cup", 1)]
        )
        
        breakdown = Breakdown(
            script_title="Test",
            entries=[entry]
        )
        
        json_str = breakdown.to_json()
        restored = Breakdown.from_json(json_str)
        
        assert restored.script_title == breakdown.script_title
        assert len(restored.entries) == 1
        assert restored.entries[0].scene_number == 1
        assert len(restored.entries[0].props) == 1

    def test_csv_export(self):
        """Should export to CSV format."""
        entry = BreakdownEntry(
            scene_number=1,
            scene_description="Test scene",
            location="Coffee Shop",
            location_type=LocationType.INTERIOR,
            time_of_day=TimeOfDay.DAY,
            characters=["Alice", "Bob"],
            props=[ProductionElement("prop", "Cup", 2)]
        )
        
        breakdown = Breakdown(
            script_title="Test",
            entries=[entry]
        )
        
        csv_str = breakdown.to_csv()
        
        assert "Scene Number" in csv_str
        assert "Coffee Shop" in csv_str
        assert "Alice" in csv_str
        assert "Cup (2)" in csv_str
