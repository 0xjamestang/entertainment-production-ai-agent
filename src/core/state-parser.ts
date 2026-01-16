import { readFile } from 'fs/promises';
import { LoopState, ParseResult } from '../types/state.js';

/**
 * Parses the loop/state.md file and extracts structured data
 */
export class StateParser {
  /**
   * Parse state file from given path
   */
  async parseFile(filePath: string): Promise<ParseResult> {
    try {
      const content = await readFile(filePath, 'utf-8');
      return this.parseContent(content);
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code === 'ENOENT') {
        return {
          success: false,
          error: `State file not found: ${filePath}`
        };
      }
      return {
        success: false,
        error: `Failed to read state file: ${(error as Error).message}`
      };
    }
  }

  /**
   * Parse state content from markdown string
   */
  parseContent(content: string): ParseResult {
    try {
      const state: LoopState = {
        goal: this.extractSection(content, 'Goal'),
        currentTask: this.extractSection(content, 'Current task'),
        constraints: this.extractSection(content, 'Constraints'),
        iterationHistory: this.extractSection(content, 'Iteration History'),
        status: this.extractSection(content, 'Status')
      };

      return {
        success: true,
        state
      };
    } catch (error) {
      return {
        success: false,
        error: `Failed to parse state content: ${(error as Error).message}`
      };
    }
  }

  /**
   * Extract a section from markdown content
   */
  private extractSection(content: string, sectionName: string): string {
    const regex = new RegExp(`#\\s+${sectionName}\\s*\\n([\\s\\S]*?)(?=\\n#|$)`, 'i');
    const match = content.match(regex);
    return match ? match[1].trim() : '';
  }
}
