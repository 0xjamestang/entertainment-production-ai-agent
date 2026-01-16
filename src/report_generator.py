"""Report generator for iteration reports."""
from datetime import datetime
from pathlib import Path
from typing import List


class ReportGenerator:
    """Generates structured iteration reports."""

    def generate_report(
        self,
        iteration: int,
        status: str,
        what_i_did: str,
        changes_made: List[str],
        tests_run: List[str],
        tests_passing: bool,
        blockers: str = "NONE",
        next_plan: str = "",
        notes: str = ""
    ) -> str:
        """
        Generate a structured iteration report.
        
        Args:
            iteration: Iteration number
            status: Status (ENGINEERING/CREATIVE/BLOCKED)
            what_i_did: Description of actions taken
            changes_made: List of changes made
            tests_run: List of tests run
            tests_passing: Whether all tests are passing
            blockers: Description of blockers (default: "NONE")
            next_plan: Plan for next iteration
            notes: Additional notes
            
        Returns:
            Formatted report string
        """
        date = datetime.now().strftime("%Y-%m-%d")
        
        changes_section = "\n".join(changes_made) if changes_made else "No changes made"
        tests_section = "\n".join(tests_run) if tests_run else "No tests run"
        
        ready_for_next = "YES" if tests_passing and blockers == "NONE" else "NO"
        tests_passing_str = "YES" if tests_passing else "NO"
        
        report = f"""# Loop Iteration Report

## Iteration: {iteration}
## Date: {date}
## Status: {status}

---

## What I Did
{what_i_did}

---

## Changes Made
{changes_section}

---

## Tests Run
{tests_section}

---

## Current State
- Tests Passing: {tests_passing_str}
- Blockers: {blockers}
- Ready for Next: {ready_for_next}

---

## Next Iteration Plan
{next_plan}

---

## Notes
{notes}
"""
        return report

    def save_report(self, report: str, file_path: str = "loop/last_output.md") -> tuple[bool, Optional[str]]:
        """
        Save report to file.
        
        Args:
            report: Report content
            file_path: Path to save report (default: loop/last_output.md)
            
        Returns:
            Tuple of (success, error_message)
        """
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(report, encoding='utf-8')
            return True, None
        except Exception as e:
            return False, f"Failed to save report: {str(e)}"


from typing import Optional
