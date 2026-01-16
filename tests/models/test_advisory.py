"""Tests for advisory data models."""
import pytest
from src.models.advisory import AdvisoryItem, ProductionNotes, PostProductionNotes


class TestAdvisoryItem:
    """Test suite for AdvisoryItem."""

    def test_valid_advisory_item(self):
        """Should create valid advisory item."""
        item = AdvisoryItem(
            category="continuity",
            priority="HIGH",
            description="Wardrobe continuity risk",
            actionable_steps=["Document wardrobe", "Take photos"]
        )
        
        valid, error = item.validate()
        assert valid is True
        assert error is None

    def test_invalid_priority(self):
        """Should reject invalid priority."""
        item = AdvisoryItem(
            category="continuity",
            priority="CRITICAL",
            description="Test",
            actionable_steps=["Step 1"]
        )
        
        valid, error = item.validate()
        assert valid is False
        assert "priority" in error.lower()

    def test_missing_actionable_steps(self):
        """Should reject item without actionable steps."""
        item = AdvisoryItem(
            category="continuity",
            priority="HIGH",
            description="Test",
            actionable_steps=[]
        )
        
        valid, error = item.validate()
        assert valid is False
        assert "actionable" in error.lower()


class TestProductionNotes:
    """Test suite for ProductionNotes."""

    def test_valid_production_notes(self):
        """Should create valid production notes."""
        item1 = AdvisoryItem("continuity", "HIGH", "Risk 1", ["Step 1"])
        item2 = AdvisoryItem("audio", "MEDIUM", "Audio rec", ["Step 1"])
        item3 = AdvisoryItem("coverage", "LOW", "Coverage", ["Step 1"])
        
        notes = ProductionNotes(
            script_title="Test",
            continuity_risks=[item1],
            audio_recommendations=[item2],
            coverage_suggestions=[item3]
        )
        
        valid, error = notes.validate()
        assert valid is True
        assert error is None

    def test_minimum_items_requirement(self):
        """Should require minimum 3 actionable items."""
        item1 = AdvisoryItem("continuity", "HIGH", "Risk 1", ["Step 1"])
        
        notes = ProductionNotes(
            script_title="Test",
            continuity_risks=[item1]
        )
        
        valid, error = notes.validate()
        assert valid is False
        assert "3 actionable items" in error

    def test_json_serialization(self):
        """Should serialize to JSON."""
        item = AdvisoryItem("continuity", "HIGH", "Test", ["Step 1"])
        notes = ProductionNotes(
            script_title="Test",
            continuity_risks=[item, item, item]
        )
        
        json_str = notes.to_json()
        assert "Test" in json_str
        assert "continuity" in json_str

    def test_markdown_export(self):
        """Should export to markdown."""
        item = AdvisoryItem("continuity", "HIGH", "Test risk", ["Step 1", "Step 2"])
        notes = ProductionNotes(
            script_title="Test",
            continuity_risks=[item, item, item]
        )
        
        md = notes.to_markdown()
        assert "# Production Notes: Test" in md
        assert "## Continuity Risks" in md
        assert "Step 1" in md


class TestPostProductionNotes:
    """Test suite for PostProductionNotes."""

    def test_valid_postproduction_notes(self):
        """Should create valid post-production notes."""
        item1 = AdvisoryItem("editing", "HIGH", "Pacing", ["Step 1"])
        item2 = AdvisoryItem("platform", "MEDIUM", "Format", ["Step 1"])
        item3 = AdvisoryItem("revision", "LOW", "Pitfall", ["Step 1"])
        
        notes = PostProductionNotes(
            script_title="Test",
            editing_suggestions=[item1],
            platform_guidelines=[item2],
            revision_pitfalls=[item3]
        )
        
        valid, error = notes.validate()
        assert valid is True
        assert error is None

    def test_minimum_items_requirement(self):
        """Should require minimum 3 actionable items."""
        item1 = AdvisoryItem("editing", "HIGH", "Test", ["Step 1"])
        
        notes = PostProductionNotes(
            script_title="Test",
            editing_suggestions=[item1]
        )
        
        valid, error = notes.validate()
        assert valid is False
        assert "3 actionable items" in error

    def test_markdown_export(self):
        """Should export to markdown."""
        item = AdvisoryItem("editing", "HIGH", "Test suggestion", ["Step 1"])
        notes = PostProductionNotes(
            script_title="Test",
            editing_suggestions=[item, item, item]
        )
        
        md = notes.to_markdown()
        assert "# Post-Production Notes: Test" in md
        assert "## Editing Rhythm & Pacing" in md
        assert "Step 1" in md
