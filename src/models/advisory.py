"""Advisory data models for production and post-production guidance."""
from dataclasses import dataclass, field
from typing import List
import json


@dataclass
class AdvisoryItem:
    """Represents a single advisory item."""
    category: str  # "continuity", "audio", "coverage", "editing", "platform", etc.
    priority: str  # "HIGH", "MEDIUM", "LOW"
    description: str
    actionable_steps: List[str] = field(default_factory=list)
    
    def validate(self) -> tuple[bool, str | None]:
        """Validate advisory item."""
        if not self.category or not self.category.strip():
            return False, "Category cannot be empty"
        if self.priority not in ["HIGH", "MEDIUM", "LOW"]:
            return False, f"Invalid priority: {self.priority}"
        if not self.description or not self.description.strip():
            return False, "Description cannot be empty"
        if not self.actionable_steps:
            return False, "Advisory must have at least one actionable step"
        return True, None


@dataclass
class ProductionNotes:
    """Production guidance notes."""
    script_title: str
    continuity_risks: List[AdvisoryItem] = field(default_factory=list)
    audio_recommendations: List[AdvisoryItem] = field(default_factory=list)
    coverage_suggestions: List[AdvisoryItem] = field(default_factory=list)
    
    def validate(self) -> tuple[bool, str | None]:
        """Validate production notes."""
        if not self.script_title or not self.script_title.strip():
            return False, "Script title cannot be empty"
        
        # Must have minimum actionable items
        total_items = (len(self.continuity_risks) + 
                      len(self.audio_recommendations) + 
                      len(self.coverage_suggestions))
        if total_items < 3:
            return False, "Production notes must have at least 3 actionable items"
        
        # Validate all items
        for item in (self.continuity_risks + self.audio_recommendations + 
                    self.coverage_suggestions):
            valid, error = item.validate()
            if not valid:
                return False, error
        
        return True, None
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "script_title": self.script_title,
            "continuity_risks": [
                {
                    "category": item.category,
                    "priority": item.priority,
                    "description": item.description,
                    "actionable_steps": item.actionable_steps
                }
                for item in self.continuity_risks
            ],
            "audio_recommendations": [
                {
                    "category": item.category,
                    "priority": item.priority,
                    "description": item.description,
                    "actionable_steps": item.actionable_steps
                }
                for item in self.audio_recommendations
            ],
            "coverage_suggestions": [
                {
                    "category": item.category,
                    "priority": item.priority,
                    "description": item.description,
                    "actionable_steps": item.actionable_steps
                }
                for item in self.coverage_suggestions
            ]
        }
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    def to_markdown(self) -> str:
        """Convert to markdown format."""
        lines = [
            f"# Production Notes: {self.script_title}",
            "",
            "## Continuity Risks",
            ""
        ]
        
        for item in self.continuity_risks:
            lines.append(f"### {item.description} [{item.priority}]")
            lines.append("**Action Steps:**")
            for step in item.actionable_steps:
                lines.append(f"- {step}")
            lines.append("")
        
        lines.extend([
            "## Audio Capture Recommendations",
            ""
        ])
        
        for item in self.audio_recommendations:
            lines.append(f"### {item.description} [{item.priority}]")
            lines.append("**Action Steps:**")
            for step in item.actionable_steps:
                lines.append(f"- {step}")
            lines.append("")
        
        lines.extend([
            "## Coverage Suggestions",
            ""
        ])
        
        for item in self.coverage_suggestions:
            lines.append(f"### {item.description} [{item.priority}]")
            lines.append("**Action Steps:**")
            for step in item.actionable_steps:
                lines.append(f"- {step}")
            lines.append("")
        
        return "\n".join(lines)


@dataclass
class PostProductionNotes:
    """Post-production guidance notes."""
    script_title: str
    editing_suggestions: List[AdvisoryItem] = field(default_factory=list)
    platform_guidelines: List[AdvisoryItem] = field(default_factory=list)
    revision_pitfalls: List[AdvisoryItem] = field(default_factory=list)
    
    def validate(self) -> tuple[bool, str | None]:
        """Validate post-production notes."""
        if not self.script_title or not self.script_title.strip():
            return False, "Script title cannot be empty"
        
        # Must have minimum actionable items
        total_items = (len(self.editing_suggestions) + 
                      len(self.platform_guidelines) + 
                      len(self.revision_pitfalls))
        if total_items < 3:
            return False, "Post-production notes must have at least 3 actionable items"
        
        # Validate all items
        for item in (self.editing_suggestions + self.platform_guidelines + 
                    self.revision_pitfalls):
            valid, error = item.validate()
            if not valid:
                return False, error
        
        return True, None
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "script_title": self.script_title,
            "editing_suggestions": [
                {
                    "category": item.category,
                    "priority": item.priority,
                    "description": item.description,
                    "actionable_steps": item.actionable_steps
                }
                for item in self.editing_suggestions
            ],
            "platform_guidelines": [
                {
                    "category": item.category,
                    "priority": item.priority,
                    "description": item.description,
                    "actionable_steps": item.actionable_steps
                }
                for item in self.platform_guidelines
            ],
            "revision_pitfalls": [
                {
                    "category": item.category,
                    "priority": item.priority,
                    "description": item.description,
                    "actionable_steps": item.actionable_steps
                }
                for item in self.revision_pitfalls
            ]
        }
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    def to_markdown(self) -> str:
        """Convert to markdown format."""
        lines = [
            f"# Post-Production Notes: {self.script_title}",
            "",
            "## Editing Rhythm & Pacing",
            ""
        ]
        
        for item in self.editing_suggestions:
            lines.append(f"### {item.description} [{item.priority}]")
            lines.append("**Action Steps:**")
            for step in item.actionable_steps:
                lines.append(f"- {step}")
            lines.append("")
        
        lines.extend([
            "## Platform-Specific Guidelines",
            ""
        ])
        
        for item in self.platform_guidelines:
            lines.append(f"### {item.description} [{item.priority}]")
            lines.append("**Action Steps:**")
            for step in item.actionable_steps:
                lines.append(f"- {step}")
            lines.append("")
        
        lines.extend([
            "## Common Revision Pitfalls",
            ""
        ])
        
        for item in self.revision_pitfalls:
            lines.append(f"### {item.description} [{item.priority}]")
            lines.append("**Action Steps:**")
            for step in item.actionable_steps:
                lines.append(f"- {step}")
            lines.append("")
        
        return "\n".join(lines)
