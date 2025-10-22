---
name: conversation-analyzer
description: Analyzes your Claude Code conversation history to identify patterns, common mistakes, and opportunities for workflow improvement. Use when user wants to understand usage patterns, optimize workflow, identify automation opportunities, or check if they're following best practices. Also activates when user says "analyze my conversations", "review my history", "how can I improve my workflow", or similar usage analysis requests.
---

# Conversation Analyzer Skill

## Purpose

Analyzes your Claude Code conversation history to identify patterns, common mistakes, and opportunities for workflow improvement. Provides actionable recommendations for optimizing your development workflow.

## When to Use

This skill automatically activates when users want to:
- Understand their Claude Code usage patterns
- Identify repetitive tasks that could be automated
- Optimize their workflow
- Check if they're following best practices
- Find opportunities for creating custom skills or slash commands

**Activation phrases:**
- "analyze my conversations"
- "review my Claude Code history"
- "what patterns do you see in my usage"
- "how can I improve my workflow"
- "am I using Claude Code effectively"

## What It Does

1. **Loads conversation history** from `~/.claude/history.jsonl`
2. **Analyzes patterns** including:
   - Request type distribution
   - Most active projects
   - Common error keywords
   - Time-of-day patterns
   - Repetitive tasks
3. **Identifies issues** such as:
   - Vague requests that cause back-and-forth
   - Complex tasks attempted without planning
   - Repeated similar requests (automation opportunities)
   - Recurring bugs or errors
4. **Generates recommendations** for:
   - Skills you should use more
   - Workflows to streamline
   - Custom skills or commands to create
   - Best practices to adopt

## Approach

### Analysis Scope

By default, analyzes the **last 200 conversations** for recency and relevance. Can be adjusted based on user preference.

### Methodology

The analysis examines:

1. **Request Type Distribution**
   - Categorizes by: bug fixes, feature additions, refactoring, information queries, testing, other
   - Identifies dominant request types

2. **Project Activity**
   - Tracks which projects consume most time
   - Identifies project-specific patterns
   - Suggests project-specific optimizations

3. **Time Patterns**
   - Hour-of-day usage distribution
   - Identifies peak productivity times

4. **Common Mistakes**
   - **Vague requests**: Initial requests lacking context vs. acceptable follow-ups
   - **Repeated fixes**: Same issues occurring multiple times
   - **Complex tasks**: Multi-step requests without planning
   - **Repetitive commands**: Manual tasks that could be automated

5. **Error Analysis**
   - Frequency of error-related requests
   - Common error keywords
   - Recurring problems

6. **Automation Opportunities**
   - Identifies repeated exact requests
   - Suggests skills, slash commands, or scripts

### Output Format

Provides a structured report with:
- **Statistics**: Request types, active projects, timing patterns
- **Patterns**: Common tasks, repetitive commands, complexity indicators
- **Issues**: Specific problems identified with examples
- **Recommendations**: Prioritized, actionable improvements

### Tools Used

- **Read**: Load history file (`~/.claude/history.jsonl`) and analysis scripts
- **Write**: Create analysis reports if requested
- **Bash**: Execute Python analysis script for comprehensive analysis
- **Direct analysis**: Parse JSON and analyze programmatically for quick insights

### Analysis Implementation

The skill uses a Python script (`scripts/analyze_history.py`) for comprehensive analysis:

**Script capabilities:**
- Loads and parses `~/.claude/history.jsonl`
- Analyzes patterns across multiple dimensions
- Identifies common mistakes and inefficiencies
- Generates actionable recommendations
- Outputs detailed reports

**How to use the script:**

1. **Within the skill (automatic):**
   ```
   User: "Analyze my conversations"
   → Skill runs the script automatically
   → Presents findings in conversational format
   ```

2. **Standalone (advanced users):**
   ```bash
   cd ~/.claude/plugins/*/productivity-skills/conversation-analyzer/scripts
   python3 analyze_history.py
   ```

   Outputs:
   - `conversation_analysis.txt` - Detailed pattern analysis
   - `recommendations.txt` - Specific improvement suggestions

**Script location:** `productivity-skills-plugin/conversation-analyzer/scripts/analyze_history.py`

## Example Interaction

```
User: "Analyze my recent conversations and tell me how to improve"

Skill:
1. Loads ~/.claude/history.jsonl
2. Runs analysis script (scripts/analyze_history.py)
3. Analyzes last 200 conversations
4. Identifies:
   - 60% general tasks, 15% bug fixes, 13% feature additions
   - Project "ultramerge" dominates 58% of activity
   - Same test-fixing request made 8 times
   - 19 multi-step requests without planning
   - Peak productivity: 13:00-15:00
5. Recommends:
   - Use test-fixing skill for recurring test failures
   - Create project-specific utilities for ultramerge data processing
   - Use feature-planning skill for complex multi-step requests
   - Add tests to prevent recurring bugs
   - Schedule complex work during peak hours
6. Provides specific examples from history to illustrate patterns
```

## Success Criteria

- User understands their usage patterns
- Concrete, actionable recommendations provided
- Specific examples from their history
- Prioritized by impact (quick wins vs long-term)
- User can immediately apply improvements

## Integration

Works well with:
- **feature-planning**: For implementing recommended improvements
- **test-fixing**: For addressing recurring test failures identified
- **git-pushing**: For committing workflow improvements

## Privacy Note

All analysis happens locally. Conversation history never leaves the user's machine.
