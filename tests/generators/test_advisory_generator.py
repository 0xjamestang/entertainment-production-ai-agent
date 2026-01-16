"""Tests for advisory generators."""
import pytest
from src.generators.advisory_generator import (
    ProductionAdvisoryGenerator, PostProductionAdvisoryGenerator
)
from src.generators.script_generator import ScriptGenerator
from src.generators.breakdown_generator import BreakdownGenerator
from src.generators.storyboard_generator import StoryboardGenerator
from src.models.script import Platform


class TestProductionAdvisoryGenerator:
    """Test suite for ProductionAdvisoryGenerator."""

    def setup_method(self):
        """Set up test fixtures."""
        self.generator = ProductionAdvisoryGenerator()
        self.script_gen = ScriptGenerator()
        self.breakdown_gen = BreakdownGenerator()
        self.storyboard_gen = StoryboardGenerator()

    def test_generate_production_notes(self):
        """Should generate production notes."""
        script = self.script_gen.generate(
            "Test", "Drama", Platform.TIKTOK, 60, "Adults"
        )
        breakdown = self.breakdown_gen.generate(script)
        storyboard = self.storyboard_gen.generate(script, breakdown)
        
        notes = self.generator.generate(script, breakdown, storyboard)
        
        assert notes.script_title == "Test"
        valid, error = notes.validate()
        assert valid is True

    def test_minimum_actionable_items(self):
        """Should generate minimum 3 actionable items."""
        script = self.script_gen.generate(
            "Test", "Drama", Platform.TIKTOK, 60, "Adults"
        )
        breakdown = self.breakdown_gen.generate(script)
        storyboard = self.storyboard_gen.generate(script, breakdown)
        
        notes = self.generator.generate(script, breakdown, storyboard)
        
        total_items = (len(notes.continuity_risks) + 
                      len(notes.audio_recommendations) + 
                      len(notes.coverage_suggestions))
        assert total_items >= 3

    def test_no_generic_advice(self):
        """Should provide specific, actionable advice."""
        script = self.script_gen.generate(
            "Test", "Drama", Platform.TIKTOK, 60, "Adults"
        )
        breakdown = self.breakdown_gen.generate(script)
        storyboard = self.storyboard_gen.generate(script, breakdown)
        
        notes = self.generator.generate(script, breakdown, storyboard)
        
        # Check all items have actionable steps
        all_items = (notes.continuity_risks + 
                    notes.audio_recommendations + 
                    notes.coverage_suggestions)
        for item in all_items:
            assert len(item.actionable_steps) > 0
            assert all(len(step) > 10 for step in item.actionable_steps)  # Not generic

    def test_markdown_export(self):
        """Should export to markdown."""
        script = self.script_gen.generate(
            "Test", "Drama", Platform.TIKTOK, 60, "Adults"
        )
        breakdown = self.breakdown_gen.generate(script)
        storyboard = self.storyboard_gen.generate(script, breakdown)
        
        notes = self.generator.generate(script, breakdown, storyboard)
        md = notes.to_markdown()
        
        assert "# Production Notes" in md
        assert "## Continuity Risks" in md
        assert "## Audio" in md


class TestPostProductionAdvisoryGenerator:
    """Test suite for PostProductionAdvisoryGenerator."""

    def setup_method(self):
        """Set up test fixtures."""
        self.generator = PostProductionAdvisoryGenerator()
        self.script_gen = ScriptGenerator()
        self.breakdown_gen = BreakdownGenerator()
        self.storyboard_gen = StoryboardGenerator()

    def test_generate_postproduction_notes(self):
        """Should generate post-production notes."""
        script = self.script_gen.generate(
            "Test", "Drama", Platform.TIKTOK, 60, "Adults"
        )
        breakdown = self.breakdown_gen.generate(script)
        storyboard = self.storyboard_gen.generate(script, breakdown)
        
        notes = self.generator.generate(script, storyboard)
        
        assert notes.script_title == "Test"
        valid, error = notes.validate()
        assert valid is True

    def test_minimum_actionable_items(self):
        """Should generate minimum 3 actionable items."""
        script = self.script_gen.generate(
            "Test", "Drama", Platform.TIKTOK, 60, "Adults"
        )
        breakdown = self.breakdown_gen.generate(script)
        storyboard = self.storyboard_gen.generate(script, breakdown)
        
        notes = self.generator.generate(script, storyboard)
        
        total_items = (len(notes.editing_suggestions) + 
                      len(notes.platform_guidelines) + 
                      len(notes.revision_pitfalls))
        assert total_items >= 3

    def test_platform_specific_guidance(self):
        """Should provide platform-specific guidance."""
        script = self.script_gen.generate(
            "Test", "Drama", Platform.TIKTOK, 60, "Adults"
        )
        breakdown = self.breakdown_gen.generate(script)
        storyboard = self.storyboard_gen.generate(script, breakdown)
        
        notes = self.generator.generate(script, storyboard)
        
        # Should have platform-specific guidelines
        assert len(notes.platform_guidelines) > 0
        
        # Check for platform-specific content
        all_text = " ".join([
            item.description + " ".join(item.actionable_steps)
            for item in notes.platform_guidelines
        ])
        assert "tiktok" in all_text.lower() or "vertical" in all_text.lower()

    def test_no_generic_advice(self):
        """Should provide specific, actionable advice."""
        script = self.script_gen.generate(
            "Test", "Drama", Platform.TIKTOK, 60, "Adults"
        )
        breakdown = self.breakdown_gen.generate(script)
        storyboard = self.storyboard_gen.generate(script, breakdown)
        
        notes = self.generator.generate(script, storyboard)
        
        # Check all items have actionable steps
        all_items = (notes.editing_suggestions + 
                    notes.platform_guidelines + 
                    notes.revision_pitfalls)
        for item in all_items:
            assert len(item.actionable_steps) > 0
            assert all(len(step) > 10 for step in item.actionable_steps)

    def test_markdown_export(self):
        """Should export to markdown."""
        script = self.script_gen.generate(
            "Test", "Drama", Platform.TIKTOK, 60, "Adults"
        )
        breakdown = self.breakdown_gen.generate(script)
        storyboard = self.storyboard_gen.generate(script, breakdown)
        
        notes = self.generator.generate(script, storyboard)
        md = notes.to_markdown()
        
        assert "# Post-Production Notes" in md
        assert "## Editing" in md
        assert "## Platform" in md
