"""State writer for updating loop/state.md file."""
from pathlib import Path
from typing import Optional


class StateWriter:
    """Updates loop/state.md with new iteration data."""

    def update_state(
        self,
        file_path: str,
        goal: Optional[str] = None,
        current_task: Optional[str] = None,
        constraints: Optional[str] = None,
        iteration_history: Optional[str] = None,
        status: Optional[str] = None
    ) -> tuple[bool, Optional[str]]:
        """
        Update state file with new values.
        
        Only updates sections that are provided (not None).
        
        Args:
            file_path: Path to state file
            goal: New goal text (optional)
            current_task: New current task text (optional)
            constraints: New constraints text (optional)
            iteration_history: New iteration history text (optional)
            status: New status text (optional)
            
        Returns:
            Tuple of (success, error_message)
        """
        try:
            path = Path(file_path)
            if not path.exists():
                return False, f"State file not found: {file_path}"
            
            content = path.read_text(encoding='utf-8')
            
            # Update each section if provided
            if goal is not None:
                content = self._update_section(content, "Goal", goal)
            if current_task is not None:
                content = self._update_section(content, "Current task", current_task)
            if constraints is not None:
                content = self._update_section(content, "Constraints", constraints)
            if iteration_history is not None:
                content = self._update_section(content, "Iteration History", iteration_history)
            if status is not None:
                content = self._update_section(content, "Status", status)
            
            # Atomic write: write to temp file then rename
            temp_path = path.with_suffix('.tmp')
            temp_path.write_text(content, encoding='utf-8')
            temp_path.replace(path)
            
            return True, None
        except Exception as e:
            return False, f"Failed to update state file: {str(e)}"

    def _update_section(self, content: str, section_name: str, new_value: str) -> str:
        """Update a specific section in the markdown content."""
        import re
        
        # Pattern to match section header and content until next section or end
        pattern = rf'(^#\s+{re.escape(section_name)}\s*\n)(.*?)(?=\n#|\Z)'
        
        # Check if section exists
        if re.search(pattern, content, re.MULTILINE | re.DOTALL):
            # Replace existing section
            replacement = rf'\1{new_value}\n'
            return re.sub(pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)
        else:
            # Section doesn't exist, append it
            return content + f"\n# {section_name}\n{new_value}\n"
