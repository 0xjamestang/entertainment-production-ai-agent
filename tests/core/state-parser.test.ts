import { describe, it, expect } from 'vitest';
import { StateParser } from '../../src/core/state-parser.js';

describe('StateParser', () => {
  const parser = new StateParser();

  describe('parseContent', () => {
    it('should parse valid state content', () => {
      const content = `# Goal
Build a production-ready agent

# Current task
Implement feature X

# Constraints
- No breaking changes
- Add tests

# Iteration History
- Iteration 1: Setup

# Status
- Requirements: Complete`;

      const result = parser.parseContent(content);

      expect(result.success).toBe(true);
      expect(result.state).toBeDefined();
      expect(result.state?.goal).toBe('Build a production-ready agent');
      expect(result.state?.currentTask).toBe('Implement feature X');
      expect(result.state?.constraints).toContain('No breaking changes');
      expect(result.state?.iterationHistory).toContain('Iteration 1');
      expect(result.state?.status).toContain('Requirements: Complete');
    });

    it('should handle missing sections', () => {
      const content = `# Goal
Build something

# Current task
Do work`;

      const result = parser.parseContent(content);

      expect(result.success).toBe(true);
      expect(result.state?.goal).toBe('Build something');
      expect(result.state?.currentTask).toBe('Do work');
      expect(result.state?.constraints).toBe('');
      expect(result.state?.iterationHistory).toBe('');
      expect(result.state?.status).toBe('');
    });

    it('should handle empty content', () => {
      const result = parser.parseContent('');

      expect(result.success).toBe(true);
      expect(result.state?.goal).toBe('');
      expect(result.state?.currentTask).toBe('');
    });

    it('should handle malformed markdown', () => {
      const content = 'Not a valid markdown structure';

      const result = parser.parseContent(content);

      expect(result.success).toBe(true);
      expect(result.state?.goal).toBe('');
    });

    it('should handle special characters', () => {
      const content = `# Goal
Build agent with **bold** and *italic*

# Current task
Task with \`code\` and [links](url)`;

      const result = parser.parseContent(content);

      expect(result.success).toBe(true);
      expect(result.state?.goal).toContain('**bold**');
      expect(result.state?.currentTask).toContain('`code`');
    });
  });

  describe('parseFile', () => {
    it('should return error for non-existent file', async () => {
      const result = await parser.parseFile('non-existent-file.md');

      expect(result.success).toBe(false);
      expect(result.error).toContain('not found');
    });
  });
});
