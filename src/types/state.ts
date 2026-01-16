/**
 * Represents the state of the autonomous loop
 */
export interface LoopState {
  goal: string;
  currentTask: string;
  constraints: string;
  iterationHistory: string;
  status: string;
}

/**
 * Result of parsing a state file
 */
export interface ParseResult {
  success: boolean;
  state?: LoopState;
  error?: string;
}
