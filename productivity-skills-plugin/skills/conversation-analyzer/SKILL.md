---
name: conversation-analyzer
description: Analyzes your Claude Code conversation history to identify patterns, common mistakes, and opportunities for workflow improvement. Use when user wants to understand usage patterns, optimize workflow, identify automation opportunities, or check if they're following best practices.
---

# Conversation Analyzer

Analyzes your Claude Code conversation history to identify patterns, common mistakes, and workflow improvement opportunities.

## When to Use

- "analyze my conversations"
- "review my Claude Code history"
- "what patterns do you see in my usage"
- "how can I improve my workflow"
- "am I using Claude Code effectively"

## What It Analyzes

1. **Request type distribution** (bug fixes, features, refactoring, queries, testing)
2. **Most active projects**
3. **Common error keywords**
4. **Time-of-day patterns**
5. **Repetitive tasks** (automation opportunities)
6. **Vague requests** causing back-and-forth
7. **Complex tasks** attempted without planning
8. **Recurring bugs/errors**

## Analysis Scope

Default: **Last 200 conversations** for recency and relevance.

## Methodology

### 1. Request Type Distribution
Categorizes by: bug fixes, feature additions, refactoring, information queries, testing, other.

### 2. Project Activity
Tracks which projects consume most time, identifies project-specific patterns.

### 3. Time Patterns
Hour-of-day usage distribution, identifies peak productivity times.

### 4. Common Mistakes
- **Vague requests**: Initial requests lacking context vs. acceptable follow-ups
- **Repeated fixes**: Same issues occurring multiple times
- **Complex tasks**: Multi-step requests without planning
- **Repetitive commands**: Manual tasks that could be automated

### 5. Error Analysis
Frequency of error-related requests, common error keywords, recurring problems.

### 6. Automation Opportunities
Identifies repeated exact requests, suggests skills, slash commands, or scripts.

## Output

Structured report with:
- **Statistics**: Request types, active projects, timing patterns
- **Patterns**: Common tasks, repetitive commands, complexity indicators
- **Issues**: Specific problems with examples
- **Recommendations**: Prioritized, actionable improvements

## Tools Used

- **Read**: Load history file (`~/.claude/history.jsonl`)
- **Write**: Create analysis reports if requested
- **Bash**: Execute Python analysis script
- **Direct analysis**: Parse JSON programmatically

## Analysis Script

Uses `scripts/analyze_history.py` for comprehensive analysis:

**Capabilities:**
- Loads and parses `~/.claude/history.jsonl`
- Analyzes patterns across multiple dimensions
- Identifies common mistakes and inefficiencies
- Generates actionable recommendations
- Outputs detailed reports

**Usage within skill:**
Runs automatically when user requests analysis.

**Standalone usage:**
```bash
cd ~/.claude/plugins/*/productivity-skills/conversation-analyzer/scripts
python3 analyze_history.py
```

Outputs:
- `conversation_analysis.txt` - Detailed pattern analysis
- `recommendations.txt` - Specific improvement suggestions

## Example Output

```
Analyzed last 200 conversations:
- 60% general tasks, 15% bug fixes, 13% feature additions
- Project "ultramerge" dominates 58% of activity
- Same test-fixing request made 8 times
- 19 multi-step requests without planning
- Peak productivity: 13:00-15:00

Recommendations:
- Use test-fixing skill for recurring test failures
- Create project-specific utilities for ultramerge
- Use feature-planning skill for complex requests
- Add tests to prevent recurring bugs
- Schedule complex work during peak hours
```

## Success Criteria

- User understands usage patterns
- Concrete, actionable recommendations
- Specific examples from history
- Prioritized by impact (quick wins vs long-term)
- User can immediately apply improvements

## Integration

- **feature-planning**: Implement recommended improvements
- **test-fixing**: Address recurring test failures
- **git-pushing**: Commit workflow improvements

## Privacy Note

All analysis happens locally. Conversation history never leaves user's machine.
