"""Advisory generator for production and post-production guidance."""
from src.models.script import Script
from src.models.breakdown import Breakdown
from src.models.storyboard import Storyboard
from src.models.advisory import (
    ProductionNotes, PostProductionNotes, AdvisoryItem
)


class ProductionAdvisoryGenerator:
    """Generates production guidance notes."""

    def generate(
        self,
        script: Script,
        breakdown: Breakdown,
        storyboard: Storyboard
    ) -> ProductionNotes:
        """
        Generate production notes from script, breakdown, and storyboard.
        
        Args:
            script: Script being produced
            breakdown: Production breakdown
            storyboard: Storyboard with shot list
            
        Returns:
            ProductionNotes with actionable guidance
        """
        continuity_risks = self._analyze_continuity_risks(script, breakdown, storyboard)
        audio_recommendations = self._generate_audio_recommendations(script, breakdown, storyboard)
        coverage_suggestions = self._generate_coverage_suggestions(script, storyboard)
        
        notes = ProductionNotes(
            script_title=script.title,
            continuity_risks=continuity_risks,
            audio_recommendations=audio_recommendations,
            coverage_suggestions=coverage_suggestions
        )
        
        return notes

    def _analyze_continuity_risks(
        self,
        script: Script,
        breakdown: Breakdown,
        storyboard: Storyboard
    ) -> list[AdvisoryItem]:
        """Analyze continuity risks."""
        risks = []
        
        # Check for wardrobe continuity
        wardrobe_items = {}
        for entry in breakdown.entries:
            for char in entry.characters:
                if char not in wardrobe_items:
                    wardrobe_items[char] = []
                wardrobe_items[char].append(entry.scene_number)
        
        for char, scenes in wardrobe_items.items():
            if len(scenes) > 1:
                risks.append(AdvisoryItem(
                    category="continuity",
                    priority="HIGH",
                    description=f"Wardrobe continuity for {char} across {len(scenes)} scenes",
                    actionable_steps=[
                        f"Document {char}'s wardrobe in detail before shooting",
                        "Take reference photos of wardrobe from multiple angles",
                        f"Maintain wardrobe consistency across scenes {', '.join(map(str, scenes))}"
                    ]
                ))
        
        # Check for prop continuity
        prop_scenes = {}
        for entry in breakdown.entries:
            for prop in entry.props:
                if prop.description not in prop_scenes:
                    prop_scenes[prop.description] = []
                prop_scenes[prop.description].append(entry.scene_number)
        
        for prop, scenes in prop_scenes.items():
            if len(scenes) > 1:
                risks.append(AdvisoryItem(
                    category="continuity",
                    priority="MEDIUM",
                    description=f"Prop continuity: {prop} appears in multiple scenes",
                    actionable_steps=[
                        f"Track {prop} placement and condition",
                        "Take continuity photos between takes",
                        "Designate a continuity supervisor for props"
                    ]
                ))
        
        # Check for location/time continuity
        location_changes = []
        prev_entry = None
        for entry in breakdown.entries:
            if prev_entry and (entry.location != prev_entry.location or 
                             entry.time_of_day != prev_entry.time_of_day):
                location_changes.append((prev_entry.scene_number, entry.scene_number))
            prev_entry = entry
        
        if location_changes:
            risks.append(AdvisoryItem(
                category="continuity",
                priority="MEDIUM",
                description=f"Location/time transitions require careful continuity",
                actionable_steps=[
                    "Document lighting conditions for each location",
                    "Note exact camera positions for matching shots",
                    "Review footage before moving to next location"
                ]
            ))
        
        return risks

    def _generate_audio_recommendations(
        self,
        script: Script,
        breakdown: Breakdown,
        storyboard: Storyboard
    ) -> list[AdvisoryItem]:
        """Generate audio capture recommendations."""
        recommendations = []
        
        # Dialogue recording
        has_dialogue = any(scene.dialogues for scene in script.scenes)
        if has_dialogue:
            recommendations.append(AdvisoryItem(
                category="audio",
                priority="HIGH",
                description="Dialogue recording and backup",
                actionable_steps=[
                    "Use lavalier mics for all speaking characters",
                    "Record backup audio with boom mic",
                    "Capture room tone for each location (30 seconds minimum)",
                    "Monitor audio levels continuously during takes"
                ]
            ))
        
        # Location-specific audio
        for entry in breakdown.entries:
            if entry.location_type.value == "EXT":
                recommendations.append(AdvisoryItem(
                    category="audio",
                    priority="MEDIUM",
                    description=f"Exterior audio challenges for Scene {entry.scene_number}",
                    actionable_steps=[
                        "Scout location for ambient noise issues",
                        "Plan shooting schedule around noise patterns",
                        "Bring wind protection for microphones",
                        "Record wild sound for atmosphere"
                    ]
                ))
                break  # Only add once for exterior scenes
        
        # Coverage audio
        recommendations.append(AdvisoryItem(
            category="audio",
            priority="MEDIUM",
            description="Audio coverage and wild sound",
            actionable_steps=[
                "Record wild sound for each location",
                "Capture ambient sound separately",
                "Record foley reference sounds on set",
                "Document all audio takes with detailed notes"
            ]
        ))
        
        return recommendations

    def _generate_coverage_suggestions(
        self,
        script: Script,
        storyboard: Storyboard
    ) -> list[AdvisoryItem]:
        """Generate coverage suggestions."""
        suggestions = []
        
        # B-roll coverage
        suggestions.append(AdvisoryItem(
            category="coverage",
            priority="HIGH",
            description="B-roll and cutaway coverage",
            actionable_steps=[
                "Shoot establishing shots from multiple angles",
                "Capture insert shots of key props and details",
                "Record environmental B-roll for each location",
                "Get cutaways for editing flexibility"
            ]
        ))
        
        # Scene-specific coverage
        scene_shot_counts = {}
        for shot in storyboard.shots:
            scene_shot_counts[shot.scene_number] = scene_shot_counts.get(shot.scene_number, 0) + 1
        
        for scene_num, shot_count in scene_shot_counts.items():
            if shot_count < 3:
                suggestions.append(AdvisoryItem(
                    category="coverage",
                    priority="MEDIUM",
                    description=f"Scene {scene_num} has limited coverage ({shot_count} shots)",
                    actionable_steps=[
                        "Consider additional angles for editing flexibility",
                        "Shoot safety coverage from different perspectives",
                        "Capture reaction shots if multiple characters present"
                    ]
                ))
        
        # Safety coverage
        suggestions.append(AdvisoryItem(
            category="coverage",
            priority="MEDIUM",
            description="Safety coverage and protection shots",
            actionable_steps=[
                "Shoot master shots for each scene",
                "Get clean plates of locations without actors",
                "Record additional takes of critical moments",
                "Capture coverage for potential reshoots"
            ]
        ))
        
        return suggestions


class PostProductionAdvisoryGenerator:
    """Generates post-production guidance notes."""

    def generate(
        self,
        script: Script,
        storyboard: Storyboard
    ) -> PostProductionNotes:
        """
        Generate post-production notes.
        
        Args:
            script: Script being edited
            storyboard: Storyboard with timing
            
        Returns:
            PostProductionNotes with actionable guidance
        """
        editing_suggestions = self._generate_editing_suggestions(script, storyboard)
        platform_guidelines = self._generate_platform_guidelines(script)
        revision_pitfalls = self._generate_revision_pitfalls(script)
        
        notes = PostProductionNotes(
            script_title=script.title,
            editing_suggestions=editing_suggestions,
            platform_guidelines=platform_guidelines,
            revision_pitfalls=revision_pitfalls
        )
        
        return notes

    def _generate_editing_suggestions(
        self,
        script: Script,
        storyboard: Storyboard
    ) -> list[AdvisoryItem]:
        """Generate editing rhythm and pacing suggestions."""
        suggestions = []
        
        # Hook retention
        if script.scenes and script.scenes[0].is_hook:
            suggestions.append(AdvisoryItem(
                category="editing",
                priority="HIGH",
                description="Hook optimization for retention",
                actionable_steps=[
                    "Ensure hook appears within first 3 seconds",
                    "Use quick cuts to maintain energy",
                    "Add sound effects or music to enhance impact",
                    "Test multiple hook variations for engagement"
                ]
            ))
        
        # Pacing for short-form
        total_duration = script.target_duration_seconds
        if total_duration <= 60:
            suggestions.append(AdvisoryItem(
                category="editing",
                priority="HIGH",
                description="Short-form pacing and rhythm",
                actionable_steps=[
                    "Keep cuts dynamic (2-4 seconds per shot average)",
                    "Use jump cuts to compress time",
                    "Add transitions sparingly (cuts are faster)",
                    "Maintain momentum throughout - no dead air"
                ]
            ))
        
        # Scene transitions
        suggestions.append(AdvisoryItem(
            category="editing",
            priority="MEDIUM",
            description="Scene transitions and flow",
            actionable_steps=[
                "Use audio bridges between scenes",
                "Match action across cuts when possible",
                "Consider L-cuts and J-cuts for smooth transitions",
                "Test pacing by watching without sound"
            ]
        ))
        
        return suggestions

    def _generate_platform_guidelines(self, script: Script) -> list[AdvisoryItem]:
        """Generate platform-specific guidelines."""
        guidelines = []
        
        platform = script.platform.value
        
        # Platform-specific aspect ratio and framing
        if platform in ["tiktok", "instagram_reels"]:
            guidelines.append(AdvisoryItem(
                category="platform",
                priority="HIGH",
                description=f"{platform.upper()} vertical format optimization",
                actionable_steps=[
                    "Export in 9:16 vertical aspect ratio",
                    "Frame for mobile viewing (faces in upper 2/3)",
                    "Ensure text is readable on small screens",
                    "Test on actual mobile device before publishing"
                ]
            ))
        
        # Subtitles and captions
        guidelines.append(AdvisoryItem(
            category="platform",
            priority="HIGH",
            description="Subtitles and captions for accessibility",
            actionable_steps=[
                "Add burned-in subtitles (many watch without sound)",
                "Use large, high-contrast text (white with black outline)",
                "Sync subtitles precisely with dialogue",
                "Keep subtitle duration readable (1-2 seconds per line)"
            ]
        ))
        
        # Sound design
        guidelines.append(AdvisoryItem(
            category="platform",
            priority="MEDIUM",
            description="Sound design and music",
            actionable_steps=[
                "Use trending audio if appropriate for platform",
                "Balance music and dialogue levels carefully",
                "Add sound effects to enhance key moments",
                "Ensure audio is clear even on phone speakers"
            ]
        ))
        
        # Color grading
        guidelines.append(AdvisoryItem(
            category="platform",
            priority="MEDIUM",
            description="Color grading for mobile viewing",
            actionable_steps=[
                "Increase contrast for mobile screens",
                "Boost saturation slightly for impact",
                "Ensure skin tones are natural",
                "Test color on multiple devices"
            ]
        ))
        
        return guidelines

    def _generate_revision_pitfalls(self, script: Script) -> list[AdvisoryItem]:
        """Generate common revision pitfalls to avoid."""
        pitfalls = []
        
        # Over-editing
        pitfalls.append(AdvisoryItem(
            category="revision",
            priority="MEDIUM",
            description="Over-editing and loss of natural flow",
            actionable_steps=[
                "Don't cut too frequently - allow moments to breathe",
                "Preserve natural pauses in dialogue",
                "Avoid excessive effects or transitions",
                "Get fresh eyes - show to someone unfamiliar with project"
            ]
        ))
        
        # Audio issues
        pitfalls.append(AdvisoryItem(
            category="revision",
            priority="HIGH",
            description="Audio quality and consistency",
            actionable_steps=[
                "Check audio levels are consistent across cuts",
                "Remove background noise without losing dialogue clarity",
                "Ensure music doesn't overpower dialogue",
                "Add room tone to fill gaps and smooth transitions"
            ]
        ))
        
        # Pacing problems
        pitfalls.append(AdvisoryItem(
            category="revision",
            priority="MEDIUM",
            description="Pacing and retention issues",
            actionable_steps=[
                "Cut ruthlessly - remove anything that doesn't serve the story",
                "Test with target audience for engagement",
                "Watch for drop-off points and tighten those sections",
                "Ensure payoff matches the hook's promise"
            ]
        ))
        
        return pitfalls
