"""End-to-end entertainment production workflow."""
from pathlib import Path
from src.models.script import Script, Platform
from src.generators.script_generator import ScriptGenerator, ScriptValidator
from src.generators.breakdown_generator import BreakdownGenerator, BreakdownValidator
from src.generators.storyboard_generator import StoryboardGenerator, ContinuityChecker
from src.generators.advisory_generator import (
    ProductionAdvisoryGenerator, PostProductionAdvisoryGenerator
)


class EntertainmentWorkflow:
    """Orchestrates the complete entertainment production workflow."""

    def __init__(self):
        """Initialize workflow with all generators."""
        self.script_gen = ScriptGenerator()
        self.script_validator = ScriptValidator()
        self.breakdown_gen = BreakdownGenerator()
        self.breakdown_validator = BreakdownValidator()
        self.storyboard_gen = StoryboardGenerator()
        self.continuity_checker = ContinuityChecker()
        self.production_advisory_gen = ProductionAdvisoryGenerator()
        self.postprod_advisory_gen = PostProductionAdvisoryGenerator()

    def execute_full_workflow(
        self,
        title: str,
        genre: str,
        platform: Platform,
        target_duration_seconds: int,
        target_audience: str,
        output_dir: str = "output"
    ) -> tuple[bool, list[str], dict]:
        """
        Execute complete workflow from script to advisory.
        
        Args:
            title: Script title
            genre: Genre/style
            platform: Target platform
            target_duration_seconds: Target duration (30-120s)
            target_audience: Target audience
            output_dir: Output directory for files
            
        Returns:
            Tuple of (success, errors, output_files)
        """
        errors = []
        output_files = {}
        
        try:
            # Step 1: Generate script
            script = self.script_gen.generate(
                title=title,
                genre=genre,
                platform=platform,
                target_duration_seconds=target_duration_seconds,
                target_audience=target_audience
            )
            
            # Validate script
            valid, issues = self.script_validator.validate_for_production(script)
            if not valid:
                errors.extend(issues)
                return False, errors, output_files
            
            # Save script
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            script_file = output_path / f"{title.replace(' ', '_')}_script.json"
            script_file.write_text(script.to_json(), encoding='utf-8')
            output_files['script'] = str(script_file)
            
            # Step 2: Generate breakdown
            breakdown = self.breakdown_gen.generate(script)
            
            # Validate breakdown
            valid, issues = self.breakdown_validator.validate_against_script(breakdown, script)
            if not valid:
                errors.extend(issues)
                return False, errors, output_files
            
            # Save breakdown
            breakdown_json = output_path / f"{title.replace(' ', '_')}_breakdown.json"
            breakdown_json.write_text(breakdown.to_json(), encoding='utf-8')
            output_files['breakdown_json'] = str(breakdown_json)
            
            breakdown_csv = output_path / f"{title.replace(' ', '_')}_breakdown.csv"
            breakdown_csv.write_text(breakdown.to_csv(), encoding='utf-8')
            output_files['breakdown_csv'] = str(breakdown_csv)
            
            # Step 3: Generate storyboard
            storyboard = self.storyboard_gen.generate(script, breakdown)
            
            # Check continuity
            valid, issues = self.continuity_checker.check_continuity(storyboard, script)
            if not valid:
                errors.extend(issues)
                return False, errors, output_files
            
            # Save storyboard
            storyboard_md = output_path / f"{title.replace(' ', '_')}_storyboard.md"
            storyboard_md.write_text(storyboard.to_markdown(), encoding='utf-8')
            output_files['storyboard'] = str(storyboard_md)
            
            shotlist_csv = output_path / f"{title.replace(' ', '_')}_shotlist.csv"
            shotlist_csv.write_text(storyboard.to_csv(), encoding='utf-8')
            output_files['shotlist'] = str(shotlist_csv)
            
            # Step 4: Generate production advisory
            production_notes = self.production_advisory_gen.generate(
                script, breakdown, storyboard
            )
            
            # Validate production notes
            valid, error = production_notes.validate()
            if not valid:
                errors.append(error)
                return False, errors, output_files
            
            # Save production notes
            prod_notes_md = output_path / f"{title.replace(' ', '_')}_production_notes.md"
            prod_notes_md.write_text(production_notes.to_markdown(), encoding='utf-8')
            output_files['production_notes'] = str(prod_notes_md)
            
            # Step 5: Generate post-production advisory
            postprod_notes = self.postprod_advisory_gen.generate(script, storyboard)
            
            # Validate post-production notes
            valid, error = postprod_notes.validate()
            if not valid:
                errors.append(error)
                return False, errors, output_files
            
            # Save post-production notes
            postprod_notes_md = output_path / f"{title.replace(' ', '_')}_postproduction_notes.md"
            postprod_notes_md.write_text(postprod_notes.to_markdown(), encoding='utf-8')
            output_files['postproduction_notes'] = str(postprod_notes_md)
            
            return True, errors, output_files
            
        except Exception as e:
            errors.append(f"Workflow error: {str(e)}")
            return False, errors, output_files

    def validate_workflow_state(self, output_dir: str) -> tuple[bool, list[str]]:
        """
        Validate that workflow output is complete and correct.
        
        Args:
            output_dir: Directory containing workflow outputs
            
        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []
        output_path = Path(output_dir)
        
        if not output_path.exists():
            issues.append(f"Output directory does not exist: {output_dir}")
            return False, issues
        
        # Check required files exist
        required_patterns = [
            "*_script.json",
            "*_breakdown.json",
            "*_breakdown.csv",
            "*_storyboard.md",
            "*_shotlist.csv",
            "*_production_notes.md",
            "*_postproduction_notes.md"
        ]
        
        for pattern in required_patterns:
            files = list(output_path.glob(pattern))
            if not files:
                issues.append(f"Missing required file matching pattern: {pattern}")
        
        return len(issues) == 0, issues
