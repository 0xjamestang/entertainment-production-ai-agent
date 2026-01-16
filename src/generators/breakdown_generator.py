"""Breakdown generator for production planning."""
from src.models.script import Script
from src.models.breakdown import (
    Breakdown, BreakdownEntry, ProductionElement, LocationType, TimeOfDay
)


class BreakdownGenerator:
    """Generates production breakdowns from scripts."""

    def generate(self, script: Script) -> Breakdown:
        """
        Generate breakdown from script.
        
        Args:
            script: Script to break down
            
        Returns:
            Breakdown object with production elements
        """
        # Validate script first
        valid, error = script.validate()
        if not valid:
            raise ValueError(f"Invalid script: {error}")
        
        entries = []
        for scene in script.scenes:
            entry = self._create_breakdown_entry(scene, script)
            entries.append(entry)
        
        breakdown = Breakdown(
            script_title=script.title,
            entries=entries
        )
        
        return breakdown

    def _create_breakdown_entry(self, scene, script) -> BreakdownEntry:
        """Create breakdown entry for a scene."""
        # Extract characters from dialogue
        characters = list(set(d.character for d in scene.dialogues))
        
        # Infer props from scene description and dialogue
        props = self._extract_props(scene)
        
        # Infer wardrobe needs
        wardrobe = self._extract_wardrobe(scene, characters)
        
        # Infer makeup needs
        makeup = self._extract_makeup(scene)
        
        # Identify special requirements
        special_requirements = self._extract_special_requirements(scene)
        
        # Estimate setup time
        setup_time = self._estimate_setup_time(scene)
        
        entry = BreakdownEntry(
            scene_number=scene.scene_number,
            scene_description=scene.description,
            location=scene.location,
            location_type=LocationType(scene.interior_exterior),
            time_of_day=TimeOfDay(scene.time_of_day),
            characters=characters,
            props=props,
            wardrobe=wardrobe,
            makeup=makeup,
            special_requirements=special_requirements,
            estimated_setup_time_minutes=setup_time
        )
        
        return entry

    def _extract_props(self, scene) -> list[ProductionElement]:
        """Extract props from scene."""
        props = []
        
        # Simple keyword-based extraction
        description_lower = scene.description.lower()
        
        if "phone" in description_lower or "mobile" in description_lower:
            props.append(ProductionElement("prop", "Mobile phone", 1))
        if "coffee" in description_lower or "cup" in description_lower:
            props.append(ProductionElement("prop", "Coffee cup", 1))
        if "table" in description_lower:
            props.append(ProductionElement("prop", "Table", 1))
        if "chair" in description_lower:
            props.append(ProductionElement("prop", "Chair", 2))
        if "car" in description_lower or "vehicle" in description_lower:
            props.append(ProductionElement("prop", "Vehicle", 1, "Requires driver/permit"))
        
        # Check dialogue for prop mentions
        for dialogue in scene.dialogues:
            text_lower = dialogue.text.lower()
            if "drink" in text_lower and not any(p.description == "Coffee cup" for p in props):
                props.append(ProductionElement("prop", "Beverage", 1))
        
        return props

    def _extract_wardrobe(self, scene, characters: list[str]) -> list[ProductionElement]:
        """Extract wardrobe needs."""
        wardrobe = []
        
        # Basic wardrobe for each character
        for character in characters:
            wardrobe.append(ProductionElement(
                "wardrobe",
                f"{character} costume",
                1,
                "Character-appropriate attire"
            ))
        
        # Check for special wardrobe needs
        description_lower = scene.description.lower()
        if "formal" in description_lower or "suit" in description_lower:
            wardrobe.append(ProductionElement("wardrobe", "Formal attire", 1))
        if "uniform" in description_lower:
            wardrobe.append(ProductionElement("wardrobe", "Uniform", 1))
        
        return wardrobe

    def _extract_makeup(self, scene) -> list[ProductionElement]:
        """Extract makeup needs."""
        makeup = []
        
        description_lower = scene.description.lower()
        
        # Basic makeup for all scenes
        makeup.append(ProductionElement("makeup", "Basic makeup", 1, "For all characters"))
        
        # Special makeup needs
        if "blood" in description_lower or "injury" in description_lower:
            makeup.append(ProductionElement("makeup", "Special effects makeup", 1, "Injury/blood effects"))
        if "age" in description_lower or "old" in description_lower:
            makeup.append(ProductionElement("makeup", "Aging makeup", 1))
        
        return makeup

    def _extract_special_requirements(self, scene) -> list[ProductionElement]:
        """Extract special requirements."""
        special = []
        
        description_lower = scene.description.lower()
        
        if "stunt" in description_lower or "fight" in description_lower:
            special.append(ProductionElement("sfx", "Stunt coordinator", 1, "Safety required"))
        if "explosion" in description_lower or "fire" in description_lower:
            special.append(ProductionElement("sfx", "Pyrotechnics", 1, "Permit and safety officer required"))
        if "rain" in description_lower or "water" in description_lower:
            special.append(ProductionElement("sfx", "Water effects", 1))
        if "animal" in description_lower or "dog" in description_lower or "cat" in description_lower:
            special.append(ProductionElement("sfx", "Animal wrangler", 1, "Trained animals required"))
        
        # Check for VFX needs
        if "vfx" in description_lower or "cgi" in description_lower or "green screen" in description_lower:
            special.append(ProductionElement("sfx", "Visual effects", 1, "Post-production VFX required"))
        
        return special

    def _estimate_setup_time(self, scene) -> int:
        """Estimate setup time in minutes."""
        base_time = 15  # Base setup time
        
        # Add time for complexity
        if scene.interior_exterior == "EXT":
            base_time += 10  # Exterior locations take longer
        
        if scene.time_of_day == "NIGHT":
            base_time += 20  # Night scenes require lighting setup
        
        # Add time for number of characters
        num_characters = len(set(d.character for d in scene.dialogues))
        base_time += num_characters * 5
        
        return base_time


class BreakdownValidator:
    """Validates breakdowns for completeness."""

    def validate_against_script(self, breakdown: Breakdown, script: Script) -> tuple[bool, list[str]]:
        """
        Validate breakdown against original script.
        
        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []
        
        # Basic validation
        valid, error = breakdown.validate()
        if not valid:
            issues.append(error)
            return False, issues
        
        # Check 1:1 scene mapping
        if len(breakdown.entries) != len(script.scenes):
            issues.append(
                f"Scene count mismatch: script has {len(script.scenes)} scenes, "
                f"breakdown has {len(breakdown.entries)} entries"
            )
        
        # Check all script scenes are in breakdown
        script_scene_numbers = {scene.scene_number for scene in script.scenes}
        breakdown_scene_numbers = {entry.scene_number for entry in breakdown.entries}
        
        missing_scenes = script_scene_numbers - breakdown_scene_numbers
        if missing_scenes:
            issues.append(f"Missing breakdown entries for scenes: {sorted(missing_scenes)}")
        
        extra_scenes = breakdown_scene_numbers - script_scene_numbers
        if extra_scenes:
            issues.append(f"Extra breakdown entries for non-existent scenes: {sorted(extra_scenes)}")
        
        # Check all characters in breakdown exist in script
        script_characters = {char.name for char in script.characters}
        for entry in breakdown.entries:
            for character in entry.characters:
                if character not in script_characters:
                    issues.append(
                        f"Scene {entry.scene_number}: Character '{character}' not in script character list"
                    )
        
        # Check no critical elements are missing
        for entry in breakdown.entries:
            if not entry.characters:
                issues.append(f"Scene {entry.scene_number}: No characters listed")
            if not entry.wardrobe:
                issues.append(f"Scene {entry.scene_number}: No wardrobe elements listed")
        
        return len(issues) == 0, issues
