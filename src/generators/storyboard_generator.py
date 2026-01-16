"""Storyboard and shot list generator."""
from src.models.script import Script
from src.models.breakdown import Breakdown
from src.models.storyboard import Storyboard, Shot, ShotSize, CameraMovement


class StoryboardGenerator:
    """Generates storyboards and shot lists from scripts."""

    def generate(self, script: Script, breakdown: Breakdown) -> Storyboard:
        """
        Generate storyboard from script and breakdown.
        
        Args:
            script: Script to visualize
            breakdown: Breakdown with production details
            
        Returns:
            Storyboard with shot list
        """
        # Validate inputs
        valid, error = script.validate()
        if not valid:
            raise ValueError(f"Invalid script: {error}")
        
        valid, error = breakdown.validate()
        if not valid:
            raise ValueError(f"Invalid breakdown: {error}")
        
        shots = []
        shot_counter = 0
        
        for scene in script.scenes:
            # Generate shots for this scene
            scene_shots = self._generate_shots_for_scene(scene, script, shot_counter)
            shots.extend(scene_shots)
            shot_counter += len(scene_shots)
        
        storyboard = Storyboard(
            script_title=script.title,
            target_duration_seconds=script.target_duration_seconds,
            shots=shots
        )
        
        return storyboard

    def _generate_shots_for_scene(self, scene, script, start_counter: int) -> list[Shot]:
        """Generate shots for a single scene with improved timing and pacing."""
        shots = []
        shot_num = start_counter
        
        # Use scene's estimated duration
        scene_duration = scene.estimated_duration_seconds or (script.target_duration_seconds // len(script.scenes))
        
        # Determine shot strategy based on scene type and genre
        is_hook = getattr(scene, 'is_hook', False)
        num_dialogues = len(scene.dialogues)
        genre_lower = script.genre.lower()
        
        # Hook scenes: Quick, energetic cuts for immediate engagement
        if is_hook:
            # For comedy: Faster cuts, reaction-focused
            if "comedy" in genre_lower:
                # Quick establishing (1s) + tight reaction (4s)
                shot_num += 1
                establishing = Shot(
                    shot_id=f"{scene.scene_number}A",
                    scene_number=scene.scene_number,
                    shot_size=ShotSize.MEDIUM,
                    camera_position="Eye level, centered on moment of chaos",
                    camera_movement=CameraMovement.STATIC,
                    visual_description=f"{scene.location}: {scene.description}. Beat before disaster.",
                    suggested_duration_seconds=1
                )
                shots.append(establishing)
                
                if scene.dialogues:
                    shot_num += 1
                    dialogue = scene.dialogues[0]
                    reaction_shot = Shot(
                        shot_id=f"{scene.scene_number}B",
                        scene_number=scene.scene_number,
                        shot_size=ShotSize.CLOSE_UP,
                        camera_position=f"Tight on {dialogue.character}'s face for comedic timing",
                        camera_movement=CameraMovement.STATIC,
                        visual_description=f"{dialogue.character}: \"{dialogue.text}\" - {dialogue.action}. Hold for reaction.",
                        suggested_duration_seconds=4,
                        audio_notes=f"Dialogue: {dialogue.character}"
                    )
                    shots.append(reaction_shot)
            
            # For drama: Slower build, emotional weight
            elif "drama" in genre_lower:
                # Medium establishing (2s) + slow push to close-up (3s)
                shot_num += 1
                establishing = Shot(
                    shot_id=f"{scene.scene_number}A",
                    scene_number=scene.scene_number,
                    shot_size=ShotSize.MEDIUM,
                    camera_position="Eye level, emotional distance closing",
                    camera_movement=CameraMovement.STATIC,
                    visual_description=f"{scene.location}: {scene.description}. Tension builds.",
                    suggested_duration_seconds=2
                )
                shots.append(establishing)
                
                if scene.dialogues:
                    shot_num += 1
                    dialogue = scene.dialogues[0]
                    reaction_shot = Shot(
                        shot_id=f"{scene.scene_number}B",
                        scene_number=scene.scene_number,
                        shot_size=ShotSize.CLOSE_UP,
                        camera_position=f"Close on {dialogue.character}, capturing vulnerability",
                        camera_movement=CameraMovement.STATIC,
                        visual_description=f"{dialogue.character}: \"{dialogue.text}\" - {dialogue.action}. Let emotion land.",
                        suggested_duration_seconds=3,
                        audio_notes=f"Dialogue: {dialogue.character}"
                    )
                    shots.append(reaction_shot)
            
            # Default hook: Balanced approach
            else:
                shot_num += 1
                establishing = Shot(
                    shot_id=f"{scene.scene_number}A",
                    scene_number=scene.scene_number,
                    shot_size=ShotSize.MEDIUM,
                    camera_position="Eye level, centered on action",
                    camera_movement=CameraMovement.STATIC,
                    visual_description=f"{scene.location}: {scene.description}. Immediate visual impact.",
                    suggested_duration_seconds=2
                )
                shots.append(establishing)
                
                if scene.dialogues:
                    shot_num += 1
                    dialogue = scene.dialogues[0]
                    reaction_shot = Shot(
                        shot_id=f"{scene.scene_number}B",
                        scene_number=scene.scene_number,
                        shot_size=ShotSize.CLOSE_UP,
                        camera_position=f"Eye level, tight on {dialogue.character}'s face",
                        camera_movement=CameraMovement.STATIC,
                        visual_description=f"{dialogue.character} reacts: \"{dialogue.text}\" - {dialogue.action}",
                        suggested_duration_seconds=scene_duration - 2,
                        audio_notes=f"Dialogue: {dialogue.character}"
                    )
                    shots.append(reaction_shot)
        
        # Regular scenes: Genre-appropriate pacing
        else:
            # Calculate shots needed
            num_shots = 1 + num_dialogues  # Establishing + dialogue shots
            duration_per_shot = max(2, scene_duration // num_shots)
            
            # Establishing shot with genre-specific approach
            shot_num += 1
            if "comedy" in genre_lower:
                camera_note = "Wide enough to capture physical comedy"
            elif "drama" in genre_lower:
                camera_note = "Composed for emotional weight"
            else:
                camera_note = f"showing {scene.location} context"
            
            establishing = Shot(
                shot_id=f"{scene.scene_number}A",
                scene_number=scene.scene_number,
                shot_size=ShotSize.WIDE,
                camera_position=f"Eye level, {camera_note}",
                camera_movement=CameraMovement.STATIC,
                visual_description=f"Wide: {scene.location}. {scene.description}",
                suggested_duration_seconds=duration_per_shot
            )
            shots.append(establishing)
            
            # Dialogue/action shots with pacing variety
            if scene.dialogues:
                for idx, dialogue in enumerate(scene.dialogues):
                    shot_num += 1
                    shot_letter = chr(66 + idx)  # B, C, D, etc.
                    
                    # Vary shot sizes for visual rhythm
                    if idx == 0:
                        shot_size = ShotSize.MEDIUM
                        position = f"Medium shot, {dialogue.character} in frame"
                    elif idx % 2 == 1:
                        shot_size = ShotSize.CLOSE_UP
                        position = f"Close-up on {dialogue.character}'s expression"
                    else:
                        shot_size = ShotSize.MEDIUM
                        position = f"Over-shoulder or medium on {dialogue.character}"
                    
                    # Add pacing notes for comedy vs drama
                    if "comedy" in genre_lower:
                        timing_note = " - timing is key, hold for laugh"
                    elif "drama" in genre_lower:
                        timing_note = " - let emotion breathe"
                    else:
                        timing_note = ""
                    
                    # More descriptive visual descriptions
                    action_desc = f" - {dialogue.action}" if dialogue.action else ""
                    visual_desc = f"{dialogue.character}: \"{dialogue.text}\"{action_desc}{timing_note}"
                    
                    dialogue_shot = Shot(
                        shot_id=f"{scene.scene_number}{shot_letter}",
                        scene_number=scene.scene_number,
                        shot_size=shot_size,
                        camera_position=position,
                        camera_movement=CameraMovement.STATIC,
                        visual_description=visual_desc,
                        suggested_duration_seconds=duration_per_shot,
                        audio_notes=f"Dialogue: {dialogue.character}"
                    )
                    shots.append(dialogue_shot)
            else:
                # No dialogue, create descriptive action shot
                shot_num += 1
                action_shot = Shot(
                    shot_id=f"{scene.scene_number}B",
                    scene_number=scene.scene_number,
                    shot_size=ShotSize.MEDIUM,
                    camera_position="Eye level, following action",
                    camera_movement=CameraMovement.STATIC,
                    visual_description=f"Action: {scene.description}",
                    suggested_duration_seconds=scene_duration - duration_per_shot
                )
                shots.append(action_shot)
        
        return shots


class ContinuityChecker:
    """Checks storyboard for continuity issues."""

    def check_continuity(self, storyboard: Storyboard, script: Script) -> tuple[bool, list[str]]:
        """
        Check storyboard for continuity issues.
        
        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []
        
        # Basic validation
        valid, error = storyboard.validate()
        if not valid:
            issues.append(error)
            return False, issues
        
        # Check all shots map to valid scenes
        script_scene_numbers = {scene.scene_number for scene in script.scenes}
        for shot in storyboard.shots:
            if shot.scene_number not in script_scene_numbers:
                issues.append(f"Shot {shot.shot_id}: References non-existent scene {shot.scene_number}")
        
        # Check for spatial continuity (no illogical transitions)
        prev_shot = None
        for shot in storyboard.shots:
            if prev_shot and prev_shot.scene_number == shot.scene_number:
                # Check for jump cuts (same size, same angle)
                if (prev_shot.shot_size == shot.shot_size and 
                    prev_shot.camera_position == shot.camera_position):
                    issues.append(
                        f"Shots {prev_shot.shot_id} and {shot.shot_id}: "
                        f"Potential jump cut (same size and position)"
                    )
            prev_shot = shot
        
        # Check duration tolerance
        total_duration = storyboard.get_total_duration()
        deviation = abs(total_duration - storyboard.target_duration_seconds) / storyboard.target_duration_seconds
        if deviation > 0.20:
            issues.append(
                f"Total duration ({total_duration}s) deviates {deviation*100:.1f}% "
                f"from target ({storyboard.target_duration_seconds}s), exceeds 20% tolerance"
            )
        
        # Check for missing coverage
        scene_shot_counts = {}
        for shot in storyboard.shots:
            scene_shot_counts[shot.scene_number] = scene_shot_counts.get(shot.scene_number, 0) + 1
        
        for scene in script.scenes:
            if scene.scene_number not in scene_shot_counts:
                issues.append(f"Scene {scene.scene_number}: No shots defined")
            elif scene_shot_counts[scene.scene_number] < 2:
                issues.append(f"Scene {scene.scene_number}: Insufficient coverage (only 1 shot)")
        
        return len(issues) == 0, issues
