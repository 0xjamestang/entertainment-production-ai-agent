"""State parser for loop/state.md file."""
import re
from pathlib import Path
from typing import Optional
from dataclasses import dataclass


@dataclass
class LoopState:
    """Represents the state of the autonomous loop."""
    goal: str
    current_task: str
    constraints: str
    iteration_history: str
    status: str


class StateParser:
    """Parses loop/state.md and extracts structured data."""

    def parse_file(self, file_path: str) -> tuple[bool, Optional[LoopState], Optional[str]]:
        """
        Parse state file from given path.
        
        Returns:
            Tuple of (success, state, error_message)
        """
        try:
            path = Path(file_path)
            if not path.exists():
                return False, None, f"State file not found: {file_path}"
            
            content = path.read_text(encoding='utf-8')
            return self.parse_content(content)
        except Exception as e:
            return False, None, f"Failed to read state file: {str(e)}"

    def parse_content(self, content: str) -> tuple[bool, Optional[LoopState], Optional[str]]:
        """
        Parse state content from markdown string.
        
        Returns:
            Tuple of (success, state, error_message)
        """
        try:
            state = LoopState(
                goal=self._extract_section(content, "Goal"),
                current_task=self._extract_section(content, "Current task"),
                constraints=self._extract_section(content, "Constraints"),
                iteration_history=self._extract_section(content, "Iteration History"),
                status=self._extract_section(content, "Status")
            )
            return True, state, None
        except Exception as e:
            return False, None, f"Failed to parse state content: {str(e)}"

    def _extract_section(self, content: str, section_name: str) -> str:
        """Extract a section from markdown content."""
        pattern = rf'^#\s+{re.escape(section_name)}\s*\n(.*?)(?=\n#|\Z)'
        match = re.search(pattern, content, re.MULTILINE | re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else ""
