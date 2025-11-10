---
name: timeline-creator
description: Create HTML timelines and project roadmaps with Gantt charts, milestones, phase groupings, and progress indicators. Use when users request timelines, roadmaps, Gantt charts, project schedules, or milestone visualizations.
---

# Timeline Creator

Create interactive HTML timelines and project roadmaps with Gantt charts and milestones.

## When to Use

- "Create timeline for [project]"
- "Generate roadmap for Q1-Q4"
- "Make Gantt chart for schedule"
- "Show project milestones"

## Components

1. **Timeline Header**: project name, date range, completion %
2. **Phase Groups**: Q1, Q2, Q3, Q4 or custom phases
3. **Timeline Items**: tasks with start/end dates, progress, status
4. **Milestones**: key deliverables with dates
5. **Gantt Visualization**: horizontal bars showing duration

## HTML Structure

```html
<!DOCTYPE html>
<html>
<head>
  <title>[Project] Timeline</title>
  <style>
    body { font-family: system-ui; max-width: 1400px; margin: 0 auto; }
    .timeline-bar { background: linear-gradient(90deg, #4299e1, #48bb78); height: 20px; border-radius: 4px; }
    .milestone { border-left: 3px solid #e53e3e; padding-left: 10px; }
    /* Status colors: #48bb78 (done), #4299e1 (in-progress), #718096 (planned) */
  </style>
</head>
<body>
  <h1>[Project] Timeline</h1>
  <!-- Phase sections with timeline bars -->
  <!-- Milestones list -->
</body>
</html>
```

## Timeline Bar Pattern

```html
<div class="timeline-item">
  <span>Task Name</span>
  <div class="timeline-bar" style="width: [percentage]%; background: [status-color];"></div>
  <span>[start] - [end]</span>
</div>
```

## Workflow

1. Extract tasks, dates, phases from project
2. Calculate duration percentages
3. Group by phases (quarters or custom)
4. Create HTML with Gantt-style bars
5. Add milestones section
6. Write to `[project]-timeline.html`

Use semantic colors for status, keep layout responsive.
