"""Loop controller for orchestrating iteration cycles."""
from pathlib import Path
from typing import Optional, Callable
from src.state_parser import StateParser, LoopState
from src.state_writer import StateWriter
from src.report_generator import ReportGenerator


class LoopController:
    """Orchestrates the autonomous loop iteration cycle."""

    def __init__(
        self,
        state_file: str = "loop/state.md",
        report_file: str = "loop/last_output.md"
    ):
        """
        Initialize loop controller.
        
        Args:
            state_file: Path to state file
            report_file: Path to report file
        """
        self.state_file = state_file
        self.report_file = report_file
        self.parser = StateParser()
        self.writer = StateWriter()
        self.generator = ReportGenerator()
        self.current_iteration = 0

    def read_state(self) -> tuple[bool, Optional[LoopState], Optional[str]]:
        """
        Read current loop state.
        
        Returns:
            Tuple of (success, state, error_message)
        """
        return self.parser.parse_file(self.state_file)

    def detect_mode(self, state: LoopState) -> str:
        """
        Detect operating mode based on state.
        
        Args:
            state: Current loop state
            
        Returns:
            Mode string: "ENGINEERING", "CREATIVE", or "BLOCKED"
        """
        # Check for blockers in status
        if "blocker" in state.status.lower() or "blocked" in state.status.lower():
            return "BLOCKED"
        
        # Check if tests are passing
        if "tests" in state.status.lower() and "passing" in state.status.lower():
            # If tests passing and no engineering work, enter creative mode
            if "complete" in state.status.lower():
                return "CREATIVE"
        
        # Default to engineering mode
        return "ENGINEERING"

    def execute_iteration(
        self,
        work_function: Optional[Callable[[LoopState], tuple[list[str], list[str], bool]]] = None
    ) -> tuple[bool, Optional[str]]:
        """
        Execute a single iteration of the loop.
        
        Args:
            work_function: Optional function to execute work.
                          Should return (changes_made, tests_run, tests_passing)
                          
        Returns:
            Tuple of (success, error_message)
        """
        # Step 1: Read state
        success, state, error = self.read_state()
        if not success:
            return False, f"Failed to read state: {error}"
        
        # Step 2: Detect mode
        mode = self.detect_mode(state)
        
        # Step 3: Execute work (if work function provided)
        changes_made = []
        tests_run = []
        tests_passing = True
        what_i_did = "Executed iteration cycle"
        
        if work_function:
            try:
                changes_made, tests_run, tests_passing = work_function(state)
                what_i_did = f"Executed work in {mode} mode"
            except Exception as e:
                return False, f"Work function failed: {str(e)}"
        
        # Step 4: Generate report
        self.current_iteration += 1
        report = self.generator.generate_report(
            iteration=self.current_iteration,
            status=mode,
            what_i_did=what_i_did,
            changes_made=changes_made,
            tests_run=tests_run,
            tests_passing=tests_passing,
            blockers="NONE" if tests_passing else "Test failures detected",
            next_plan="Continue to next iteration" if tests_passing else "Fix failing tests",
            notes=f"Current task: {state.current_task}"
        )
        
        # Step 5: Save report
        success, error = self.generator.save_report(report, self.report_file)
        if not success:
            return False, f"Failed to save report: {error}"
        
        # Step 6: Update state (increment iteration in history)
        new_history = state.iteration_history
        if new_history:
            new_history += f"\n- Iteration {self.current_iteration}: {mode} mode executed"
        else:
            new_history = f"- Iteration {self.current_iteration}: {mode} mode executed"
        
        success, error = self.writer.update_state(
            self.state_file,
            iteration_history=new_history
        )
        if not success:
            return False, f"Failed to update state: {error}"
        
        return True, None

    def run_loop(
        self,
        max_iterations: int = 50,
        work_function: Optional[Callable[[LoopState], tuple[list[str], list[str], bool]]] = None
    ) -> tuple[bool, Optional[str]]:
        """
        Run the autonomous loop for multiple iterations.
        
        Args:
            max_iterations: Maximum number of iterations (default: 50)
            work_function: Optional function to execute work each iteration
            
        Returns:
            Tuple of (success, error_message)
        """
        for i in range(max_iterations):
            success, error = self.execute_iteration(work_function)
            if not success:
                return False, f"Iteration {i+1} failed: {error}"
            
            # Check if we should continue
            success, state, error = self.read_state()
            if not success:
                return False, f"Failed to read state after iteration {i+1}: {error}"
            
            # Stop if in blocked mode
            mode = self.detect_mode(state)
            if mode == "BLOCKED":
                return True, f"Loop stopped: System is blocked after {i+1} iterations"
        
        return True, None

    def get_current_iteration(self) -> int:
        """Get current iteration number."""
        return self.current_iteration
