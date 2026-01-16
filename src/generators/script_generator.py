"""Script generator for entertainment production."""
from typing import Optional
from src.models.script import (
    Script, Scene, Character, Dialogue, CostFlag, Platform
)


class ScriptGenerator:
    """Generates scripts based on inputs."""

    def generate(
        self,
        title: str,
        genre: str,
        platform: Platform,
        target_duration_seconds: int,
        target_audience: str,
        concept: Optional[str] = None
    ) -> Script:
        """
        Generate a script based on inputs.
        
        Args:
            title: Script title
            genre: Genre/style
            platform: Target platform
            target_duration_seconds: Target duration (30-120s)
            target_audience: Target audience description
            concept: Optional story concept
            
        Returns:
            Generated Script object
        """
        # Create characters based on genre
        characters = self._generate_characters(genre, target_audience)
        
        # Generate scenes with hook
        scenes = self._generate_scenes(
            genre, target_duration_seconds, characters, concept
        )
        
        # Identify cost flags
        cost_flags = self._identify_cost_flags(scenes)
        
        script = Script(
            title=title,
            genre=genre,
            platform=platform,
            target_duration_seconds=target_duration_seconds,
            target_audience=target_audience,
            characters=characters,
            scenes=scenes,
            cost_flags=cost_flags
        )
        
        return script

    def _generate_characters(self, genre: str, target_audience: str) -> list[Character]:
        """Generate characters based on genre and audience."""
        genre_lower = genre.lower()
        
        # Romantic comedy characters
        if "romantic" in genre_lower and "comedy" in genre_lower:
            return [
                Character(name="Maya", description="Barista with a secret talent", age_range="22-28"),
                Character(name="Alex", description="Regular customer, tech startup founder", age_range="25-30")
            ]
        # General comedy
        elif "comedy" in genre_lower:
            return [
                Character(name="Jordan", description="Optimistic dreamer", age_range="20-28"),
                Character(name="Sam", description="Sarcastic best friend", age_range="20-28")
            ]
        # Drama
        elif "drama" in genre_lower:
            return [
                Character(name="Elena", description="Determined protagonist", age_range="25-35"),
                Character(name="Marcus", description="Mysterious stranger", age_range="30-40")
            ]
        # Horror/Thriller
        elif "horror" in genre_lower or "thriller" in genre_lower:
            return [
                Character(name="Riley", description="Skeptical investigator", age_range="25-32")
            ]
        # Default
        else:
            return [
                Character(name="Taylor", description="Relatable protagonist", age_range="22-30")
            ]

    def _generate_scenes(
        self,
        genre: str,
        target_duration: int,
        characters: list[Character],
        concept: Optional[str]
    ) -> list[Scene]:
        """Generate scenes with hook and genre-specific content."""
        scenes = []
        genre_lower = genre.lower()
        
        # Get character names
        char1 = characters[0].name if len(characters) > 0 else "Character"
        char2 = characters[1].name if len(characters) > 1 else None
        
        # Scene 1: Hook (first 3-5 seconds) - Genre-specific
        hook_dialogue, hook_action = self._generate_hook(genre_lower, char1)
        hook_description = self._get_scene_description(genre_lower, "hook")
        
        hook_scene = Scene(
            scene_number=1,
            location=self._get_location_for_genre(genre_lower, "hook"),
            time_of_day="DAY",
            interior_exterior="INT",
            description=hook_description,
            dialogues=[
                Dialogue(
                    character=char1,
                    text=hook_dialogue,
                    action=hook_action
                )
            ],
            estimated_duration_seconds=5,
            is_hook=True
        )
        scenes.append(hook_scene)
        
        remaining_duration = target_duration - 5
        
        # Scene 2: Development (if duration allows)
        if target_duration >= 45:
            dev_duration = remaining_duration // 2
            dev_dialogue, dev_action = self._generate_development(genre_lower, char1, char2)
            dev_description = self._get_scene_description(genre_lower, "development")
            
            # Add second character dialogue if available
            dialogues = [
                Dialogue(
                    character=char1,
                    text=dev_dialogue,
                    action=dev_action
                )
            ]
            
            dev_scene = Scene(
                scene_number=2,
                location=self._get_location_for_genre(genre_lower, "development"),
                time_of_day="DAY",
                interior_exterior="INT",
                description=dev_description,
                dialogues=dialogues,
                estimated_duration_seconds=dev_duration
            )
            scenes.append(dev_scene)
            remaining_duration -= dev_duration
        
        # Scene 3: Resolution
        res_dialogue, res_action = self._generate_resolution(genre_lower, char1, char2)
        res_description = self._get_scene_description(genre_lower, "resolution")
        
        resolution_scene = Scene(
            scene_number=len(scenes) + 1,
            location=self._get_location_for_genre(genre_lower, "resolution"),
            time_of_day="DAY",
            interior_exterior="INT",
            description=res_description,
            dialogues=[
                Dialogue(
                    character=char1,
                    text=res_dialogue,
                    action=res_action
                )
            ],
            estimated_duration_seconds=remaining_duration
        )
        scenes.append(resolution_scene)
        
        return scenes
    
    def _get_scene_description(self, genre: str, scene_type: str) -> str:
        """Get genre-specific scene descriptions with emotional context."""
        descriptions = {
            "romantic comedy": {
                "hook": "The moment everything shifts - a simple mistake becomes a catalyst",
                "development": "Vulnerability surfaces through nervous explanation, walls coming down",
                "resolution": "Mutual recognition - what seemed wrong was exactly right"
            },
            "comedy": {
                "hook": "Disaster strikes in the most mundane moment - chaos begins",
                "development": "Attempting damage control while digging deeper into absurdity",
                "resolution": "Acceptance of chaos, finding humor in the wreckage"
            },
            "drama": {
                "hook": "The past collides with present - no more running",
                "development": "Truth emerges after years of silence, courage to speak",
                "resolution": "Catharsis - the weight of unspoken words finally lifted"
            },
            "horror": {
                "hook": "Something's wrong - instinct screams danger",
                "development": "Dread builds, rational mind fights primal fear",
                "resolution": "Confrontation with the unknown, survival instinct takes over"
            },
            "thriller": {
                "hook": "The first crack in normalcy - something's off",
                "development": "Paranoia or perception? Trust erodes",
                "resolution": "Truth revealed, reality shifts permanently"
            }
        }
        
        # Find matching genre
        for key in descriptions:
            if key in genre:
                return descriptions[key].get(scene_type, "Scene unfolds")
        
        # Default
        return {
            "hook": "Opening moment - immediate engagement",
            "development": "Story deepens, stakes rise",
            "resolution": "Emotional payoff, transformation complete"
        }.get(scene_type, "Scene unfolds")
    
    def _generate_hook(self, genre: str, character: str) -> tuple[str, str]:
        """Generate genre-specific hook dialogue with subtext and emotional nuance."""
        if "romantic" in genre and "comedy" in genre:
            # Subtext: Confusion masking attraction, playful tension
            return ("Wait, you ordered a what?!", "freezes mid-pour, eyes wide with genuine surprise")
        elif "comedy" in genre:
            # Subtext: Denial of obvious disaster, comedic self-awareness
            return ("This is NOT how I planned my morning.", "stares at chaos, deadpan delivery")
        elif "drama" in genre:
            # Subtext: Years of unspoken emotion, vulnerability breaking through
            return ("I can't believe you're actually here.", "voice cracks slightly, frozen in doorway")
        elif "horror" in genre or "thriller" in genre:
            # Subtext: Primal fear, instinct overriding logic
            return ("Did you hear that?", "stops dead, breath held, listening intently")
        else:
            # Subtext: Determination masking fear, point of no return
            return ("Everything changes right now.", "locks eyes with camera, jaw set")
    
    def _generate_development(self, genre: str, char1: str, char2: Optional[str]) -> tuple[str, str]:
        """Generate genre-specific development dialogue with emotional layers."""
        if "romantic" in genre and "comedy" in genre:
            # Subtext: Vulnerability disguised as explanation, hope mixed with fear of rejection
            return (
                "You've been ordering the same drink for three months. I thought I'd surprise you.",
                "nervous laugh, fidgets with cup sleeve, can't quite meet their eyes"
            )
        elif "comedy" in genre:
            # Subtext: Deflection through humor, avoiding responsibility
            return (
                "Okay, so maybe I should have read the instructions first.",
                "awkward laugh that trails off, realizes the magnitude"
            )
        elif "drama" in genre:
            # Subtext: Rehearsed words finally spoken, weight of unsaid things
            return (
                "I've been trying to find the right words for weeks.",
                "takes a shaky breath, steps closer with purpose"
            )
        else:
            # Subtext: Burden of truth, courage to speak
            return (
                "There's something I need to tell you.",
                "steadies voice, gathering courage"
            )
    
    def _generate_resolution(self, genre: str, char1: str, char2: Optional[str]) -> tuple[str, str]:
        """Generate genre-specific resolution with emotional payoff."""
        if "romantic" in genre and "comedy" in genre:
            # Subtext: Acceptance, mutual understanding, beginning of something new
            return (
                "Best wrong order ever.",
                "genuine smile breaks through, eyes soften with warmth"
            )
        elif "comedy" in genre:
            # Subtext: Finding silver lining, growth through chaos
            return (
                "Well, at least it's a good story now.",
                "laughs genuinely, tension releases"
            )
        elif "drama" in genre:
            # Subtext: Relief, catharsis, weight lifted
            return (
                "I'm glad I finally said it.",
                "exhales deeply, shoulders drop, relieved smile"
            )
        else:
            # Subtext: Transformation complete, new reality accepted
            return (
                "And that's how everything changed.",
                "looks directly at camera, knowing smile"
            )
    
    def _get_location_for_genre(self, genre: str, scene_type: str) -> str:
        """Get appropriate location based on genre and scene type."""
        if "romantic" in genre and "comedy" in genre:
            locations = {
                "hook": "Coffee Shop - Counter",
                "development": "Coffee Shop - Corner Table",
                "resolution": "Coffee Shop - Window Seat"
            }
            return locations.get(scene_type, "Coffee Shop")
        elif "comedy" in genre:
            locations = {
                "hook": "Apartment - Kitchen",
                "development": "Apartment - Living Room",
                "resolution": "Apartment - Balcony"
            }
            return locations.get(scene_type, "Apartment")
        elif "drama" in genre:
            locations = {
                "hook": "Train Station Platform",
                "development": "Train Station Bench",
                "resolution": "Train Station Exit"
            }
            return locations.get(scene_type, "Station")
        else:
            return f"Location - {scene_type.title()}"

    def _identify_cost_flags(self, scenes: list[Scene]) -> list[CostFlag]:
        """Identify high-cost production elements."""
        cost_flags = []
        
        for scene in scenes:
            # Check for night scenes
            if scene.time_of_day == "NIGHT":
                cost_flags.append(CostFlag(
                    element_type="night_scene",
                    description=f"Scene {scene.scene_number}: Night shooting requires additional lighting",
                    estimated_complexity="MEDIUM"
                ))
            
            # Check for exterior scenes
            if scene.interior_exterior == "EXT":
                cost_flags.append(CostFlag(
                    element_type="location",
                    description=f"Scene {scene.scene_number}: Exterior location may require permits",
                    estimated_complexity="LOW"
                ))
            
            # Check for multiple characters (extras)
            if len(scene.dialogues) > 3:
                cost_flags.append(CostFlag(
                    element_type="extras",
                    description=f"Scene {scene.scene_number}: Multiple speaking characters increase complexity",
                    estimated_complexity="MEDIUM"
                ))
        
        return cost_flags


class ScriptValidator:
    """Validates scripts for production readiness."""

    def validate_for_production(self, script: Script) -> tuple[bool, list[str]]:
        """
        Validate script for production readiness.
        
        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []
        
        # Basic validation
        valid, error = script.validate()
        if not valid:
            issues.append(error)
            return False, issues
        
        # Check dialogue is conversational
        for scene in script.scenes:
            for dialogue in scene.dialogues:
                if len(dialogue.text.split()) > 50:
                    issues.append(
                        f"Scene {scene.scene_number}: Dialogue too long for {dialogue.character} "
                        f"(>50 words may not be conversational)"
                    )
        
        # Check total estimated duration
        total_duration = sum(
            scene.estimated_duration_seconds or 0
            for scene in script.scenes
        )
        if total_duration > 0:
            deviation = abs(total_duration - script.target_duration_seconds) / script.target_duration_seconds
            if deviation > 0.3:  # More than 30% deviation
                issues.append(
                    f"Total estimated duration ({total_duration}s) deviates significantly "
                    f"from target ({script.target_duration_seconds}s)"
                )
        
        return len(issues) == 0, issues
