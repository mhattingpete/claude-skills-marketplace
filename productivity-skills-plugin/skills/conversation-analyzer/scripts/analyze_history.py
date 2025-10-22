#!/usr/bin/env python3
"""
Analyze Claude Code conversation history to identify patterns and common mistakes.
"""

import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

def load_history(history_path):
    """Load and parse history.jsonl file."""
    conversations = []
    with open(history_path, 'r') as f:
        for line in f:
            try:
                conversations.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return conversations

def extract_patterns(conversations):
    """Extract patterns from conversations."""
    patterns = {
        'common_tasks': Counter(),
        'projects': Counter(),
        'error_keywords': Counter(),
        'request_types': Counter(),
        'time_distribution': defaultdict(int),
        'complexity_indicators': Counter(),
    }

    error_keywords = ['error', 'fix', 'bug', 'issue', 'problem', 'fail', 'broken', 'wrong', 'incorrect', 'merge conflict']
    complexity_indicators = ['refactor', 'implement', 'add feature', 'create', 'build', 'migrate', 'optimize', 'analyze']

    for conv in conversations:
        display = conv.get('display', '').lower()
        project = conv.get('project', '')

        # Count projects
        if project:
            patterns['projects'][project] += 1

        # Count error-related requests
        for keyword in error_keywords:
            if keyword in display:
                patterns['error_keywords'][keyword] += 1

        # Count complexity indicators
        for indicator in complexity_indicators:
            if indicator in display:
                patterns['complexity_indicators'][indicator] += 1

        # Categorize request types
        if any(kw in display for kw in ['fix', 'error', 'bug', 'issue', 'problem']):
            patterns['request_types']['bug_fix'] += 1
        elif any(kw in display for kw in ['add', 'create', 'implement', 'build', 'new']):
            patterns['request_types']['feature_addition'] += 1
        elif any(kw in display for kw in ['refactor', 'improve', 'optimize', 'clean']):
            patterns['request_types']['refactoring'] += 1
        elif any(kw in display for kw in ['explain', 'what', 'how', 'why', 'analyze', 'understand']):
            patterns['request_types']['information_query'] += 1
        elif any(kw in display for kw in ['test', 'run', 'build', 'deploy']):
            patterns['request_types']['testing_deployment'] += 1
        else:
            patterns['request_types']['other'] += 1

        # Time distribution (hour of day)
        if 'timestamp' in conv:
            dt = datetime.fromtimestamp(conv['timestamp'] / 1000)
            hour = dt.hour
            patterns['time_distribution'][hour] += 1

        # Track all tasks
        patterns['common_tasks'][display] += 1

    return patterns

def identify_common_mistakes(conversations):
    """Identify patterns that might indicate common mistakes."""
    mistakes = {
        'repeated_fixes': [],
        'merge_conflicts': [],
        'repeated_requests': [],
        'vague_requests': [],
        'multi_step_without_planning': [],
    }

    # Track repeated similar requests
    task_groups = defaultdict(list)
    for i, conv in enumerate(conversations):
        display = conv.get('display', '')

        # Group similar tasks
        normalized = re.sub(r'\d+', '#', display.lower())
        normalized = re.sub(r'[^\w\s]', '', normalized)
        task_groups[normalized].append((i, display, conv))

    # Identify repeated fixes
    for task, occurrences in task_groups.items():
        if len(occurrences) > 2 and any(kw in task for kw in ['fix', 'error', 'bug']):
            mistakes['repeated_fixes'].append({
                'pattern': task,
                'count': len(occurrences),
                'examples': [occ[1] for occ in occurrences[:3]]
            })

    # Identify merge conflicts
    for conv in conversations:
        display = conv.get('display', '')
        if 'merge conflict' in display.lower():
            mistakes['merge_conflicts'].append(display)

    # Identify repeated requests (exact matches)
    for task, occurrences in task_groups.items():
        if len(occurrences) > 3:
            mistakes['repeated_requests'].append({
                'pattern': occurrences[0][1],
                'count': len(occurrences)
            })

    # Identify vague requests (very short or unclear)
    vague_keywords = ['this', 'that', 'it', 'the thing', 'stuff']
    for conv in conversations:
        display = conv.get('display', '')
        if len(display.split()) < 4 or any(vk in display.lower() for vk in vague_keywords):
            if len(display) < 30:
                mistakes['vague_requests'].append(display)

    # Identify complex multi-step requests
    multi_step_indicators = [' and ', ', ', 'then ', 'also ', 'plus ']
    for conv in conversations:
        display = conv.get('display', '')
        if sum(indicator in display.lower() for indicator in multi_step_indicators) >= 2:
            mistakes['multi_step_without_planning'].append(display)

    return mistakes

def generate_report(patterns, mistakes):
    """Generate a comprehensive analysis report."""
    report = []

    report.append("=" * 80)
    report.append("CLAUDE CODE CONVERSATION ANALYSIS REPORT")
    report.append("=" * 80)
    report.append("")

    # Overall statistics
    report.append("## OVERALL STATISTICS")
    report.append(f"Total conversations: {sum(patterns['request_types'].values())}")
    report.append("")

    # Request type distribution
    report.append("## REQUEST TYPE DISTRIBUTION")
    for req_type, count in patterns['request_types'].most_common():
        percentage = (count / sum(patterns['request_types'].values())) * 100
        report.append(f"  {req_type.replace('_', ' ').title()}: {count} ({percentage:.1f}%)")
    report.append("")

    # Most active projects
    report.append("## MOST ACTIVE PROJECTS")
    for project, count in patterns['projects'].most_common(10):
        report.append(f"  {count:3d}x {project}")
    report.append("")

    # Common error keywords
    report.append("## COMMON ERROR KEYWORDS")
    for keyword, count in patterns['error_keywords'].most_common(10):
        report.append(f"  {keyword}: {count}")
    report.append("")

    # Complexity indicators
    report.append("## COMPLEXITY INDICATORS")
    for indicator, count in patterns['complexity_indicators'].most_common(10):
        report.append(f"  {indicator}: {count}")
    report.append("")

    # Time distribution
    report.append("## TIME DISTRIBUTION (BY HOUR)")
    for hour in sorted(patterns['time_distribution'].keys()):
        count = patterns['time_distribution'][hour]
        bar = '█' * (count // 5)
        report.append(f"  {hour:02d}:00 {bar} ({count})")
    report.append("")

    # Common mistakes
    report.append("=" * 80)
    report.append("## IDENTIFIED COMMON MISTAKES AND PATTERNS")
    report.append("=" * 80)
    report.append("")

    if mistakes['merge_conflicts']:
        report.append(f"### 1. MERGE CONFLICTS ({len(mistakes['merge_conflicts'])} occurrences)")
        report.append("These indicate potential git workflow issues:")
        for mc in mistakes['merge_conflicts'][:5]:
            report.append(f"  - {mc}")
        report.append("")

    if mistakes['repeated_fixes']:
        report.append(f"### 2. REPEATED FIX PATTERNS ({len(mistakes['repeated_fixes'])} patterns)")
        report.append("Similar fixes requested multiple times - may indicate recurring issues:")
        for fix in sorted(mistakes['repeated_fixes'], key=lambda x: x['count'], reverse=True)[:5]:
            report.append(f"  - Pattern: '{fix['pattern']}' (occurred {fix['count']} times)")
            for example in fix['examples'][:2]:
                report.append(f"    Example: {example}")
        report.append("")

    if mistakes['repeated_requests']:
        report.append(f"### 3. REPEATED EXACT REQUESTS ({len(mistakes['repeated_requests'])} patterns)")
        report.append("Exact same requests multiple times - could be automated:")
        for req in sorted(mistakes['repeated_requests'], key=lambda x: x['count'], reverse=True)[:5]:
            report.append(f"  - '{req['pattern']}' (x{req['count']})")
        report.append("")

    if mistakes['vague_requests']:
        report.append(f"### 4. VAGUE REQUESTS ({len(mistakes['vague_requests'])} found)")
        report.append("Short or unclear requests that might benefit from more context:")
        for vague in mistakes['vague_requests'][:10]:
            report.append(f"  - '{vague}'")
        report.append("")

    if mistakes['multi_step_without_planning']:
        report.append(f"### 5. COMPLEX MULTI-STEP REQUESTS ({len(mistakes['multi_step_without_planning'])} found)")
        report.append("Requests with multiple steps that could benefit from planning:")
        for multi in mistakes['multi_step_without_planning'][:10]:
            report.append(f"  - {multi}")
        report.append("")

    # Most common tasks
    report.append("## TOP 20 MOST COMMON TASKS")
    for task, count in patterns['common_tasks'].most_common(20):
        if count > 1:
            report.append(f"  {count:3d}x {task}")
    report.append("")

    return "\n".join(report)

def generate_recommendations(patterns, mistakes):
    """Generate specific recommendations based on analysis."""
    recommendations = []

    recommendations.append("=" * 80)
    recommendations.append("RECOMMENDATIONS FOR IMPROVEMENT")
    recommendations.append("=" * 80)
    recommendations.append("")

    rec_num = 1

    # Merge conflict recommendations
    if mistakes['merge_conflicts']:
        recommendations.append(f"{rec_num}. GIT WORKFLOW IMPROVEMENTS")
        recommendations.append("   Problem: Multiple merge conflicts detected")
        recommendations.append("   Solutions:")
        recommendations.append("   - Create a pre-commit hook to check for conflicts")
        recommendations.append("   - Add a git alias for safe rebasing")
        recommendations.append("   - Document merge conflict resolution workflow")
        recommendations.append("   - Consider using git hooks to prevent pushing conflicted files")
        recommendations.append("")
        rec_num += 1

    # Repeated fixes recommendations
    if mistakes['repeated_fixes']:
        recommendations.append(f"{rec_num}. PREVENT RECURRING BUGS")
        recommendations.append("   Problem: Same types of fixes requested repeatedly")
        recommendations.append("   Solutions:")
        recommendations.append("   - Add linting rules to catch common errors")
        recommendations.append("   - Create test cases for frequently fixed bugs")
        recommendations.append("   - Document common pitfalls in CLAUDE.md")
        recommendations.append("   - Consider pre-commit hooks for validation")
        recommendations.append("")
        rec_num += 1

    # Repeated requests
    if mistakes['repeated_requests']:
        recommendations.append(f"{rec_num}. AUTOMATE REPETITIVE TASKS")
        recommendations.append("   Problem: Same requests made multiple times")
        recommendations.append("   Solutions:")
        recommendations.append("   - Create slash commands for common tasks")
        recommendations.append("   - Add shell aliases or scripts")
        recommendations.append("   - Consider creating Claude Code skills for workflows")
        recommendations.append("   - Document common patterns in CLAUDE.md")
        recommendations.append("")
        rec_num += 1

    # Vague requests
    if mistakes['vague_requests']:
        recommendations.append(f"{rec_num}. IMPROVE REQUEST CLARITY")
        recommendations.append("   Problem: Many vague or unclear requests")
        recommendations.append("   Solutions:")
        recommendations.append("   - Create request templates in CLAUDE.md")
        recommendations.append("   - Add examples of good vs. bad requests")
        recommendations.append("   - Use more specific language and context")
        recommendations.append("   - Break down complex requests into steps")
        recommendations.append("")
        rec_num += 1

    # Multi-step planning
    if mistakes['multi_step_without_planning']:
        recommendations.append(f"{rec_num}. BETTER TASK PLANNING")
        recommendations.append("   Problem: Complex multi-step requests without planning")
        recommendations.append("   Solutions:")
        recommendations.append("   - Use 'plan mode' for complex tasks")
        recommendations.append("   - Break down requests into discrete steps")
        recommendations.append("   - Create checklists for common workflows")
        recommendations.append("   - Consider using the feature-planning skill")
        recommendations.append("")
        rec_num += 1

    # Error-heavy workflow
    error_ratio = sum(patterns['error_keywords'].values()) / max(sum(patterns['request_types'].values()), 1)
    if error_ratio > 0.3:
        recommendations.append(f"{rec_num}. REDUCE ERROR RATE")
        recommendations.append(f"   Problem: High error rate detected ({error_ratio*100:.1f}% of requests)")
        recommendations.append("   Solutions:")
        recommendations.append("   - Implement comprehensive testing before changes")
        recommendations.append("   - Add validation hooks (pre-commit, pre-push)")
        recommendations.append("   - Create a testing checklist in CLAUDE.md")
        recommendations.append("   - Consider TDD approach for new features")
        recommendations.append("")
        rec_num += 1

    return "\n".join(recommendations)

def main():
    history_path = Path.home() / '.claude' / 'history.jsonl'

    print("Loading conversation history...")
    all_conversations = load_history(history_path)

    # Focus on recent conversations (last 200)
    recent_conversations = all_conversations[-200:]

    print(f"Analyzing {len(all_conversations)} total conversations...")
    print(f"Deep analysis on {len(recent_conversations)} recent conversations...")

    patterns = extract_patterns(recent_conversations)
    mistakes = identify_common_mistakes(recent_conversations)

    print("\nGenerating reports...")
    report = generate_report(patterns, mistakes)
    recommendations = generate_recommendations(patterns, mistakes)

    # Save reports
    output_dir = Path.cwd()

    # Add header with analysis scope
    header = f"""
ANALYSIS SCOPE
==============
Total conversations in history: {len(all_conversations)}
Recent conversations analyzed: {len(recent_conversations)}
Time period: Last 200 interactions

"""

    with open(output_dir / 'conversation_analysis.txt', 'w') as f:
        f.write(header)
        f.write(report)

    with open(output_dir / 'recommendations.txt', 'w') as f:
        f.write(recommendations)

    print("\n" + "=" * 80)
    print("Analysis complete! Reports saved to:")
    print(f"  - {output_dir / 'conversation_analysis.txt'}")
    print(f"  - {output_dir / 'recommendations.txt'}")
    print("=" * 80)

    # Print summary to console
    print("\n" + report)
    print("\n" + recommendations)

if __name__ == '__main__':
    main()
