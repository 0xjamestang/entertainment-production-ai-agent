#!/usr/bin/env python3
"""CLI for running the Ralph Wiggum autonomous loop."""
import sys
from src.loop_controller import LoopController


def main():
    """Run the autonomous loop."""
    print("=" * 60)
    print("Ralph Wiggum Autonomous Loop System")
    print("=" * 60)
    print()
    
    controller = LoopController()
    
    # Read current state
    print("Reading loop state...")
    success, state, error = controller.read_state()
    if not success:
        print(f"ERROR: Failed to read state: {error}")
        return 1
    
    print(f"Goal: {state.goal[:50]}...")
    print(f"Current Task: {state.current_task[:50]}...")
    print(f"Mode: {controller.detect_mode(state)}")
    print()
    
    # Execute single iteration
    print("Executing iteration...")
    success, error = controller.execute_iteration()
    if not success:
        print(f"ERROR: Iteration failed: {error}")
        return 1
    
    print(f"✓ Iteration {controller.get_current_iteration()} completed successfully")
    print(f"✓ Report saved to loop/last_output.md")
    print()
    
    # Read updated state
    success, state, error = controller.read_state()
    if success:
        print("Updated state:")
        print(f"  Current Task: {state.current_task[:60]}...")
        print(f"  Status: {state.status[:60]}...")
    
    print()
    print("=" * 60)
    print("Loop iteration complete. Check loop/last_output.md for details.")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
