---
name: flowchart-creator
description: Create HTML flowcharts and process diagrams with decision trees, color-coded stages, arrows, and swimlanes. Use when users request flowcharts, process diagrams, workflow visualizations, or decision trees.
---

# Flowchart Creator

Create interactive HTML flowcharts and process diagrams.

## When to Use

- "Create flowchart for [process]"
- "Generate process flow diagram"
- "Make decision tree for [workflow]"
- "Show workflow visualization"

## Components

1. **Start/End nodes**: rounded rectangles (#48bb78 green, #e53e3e red)
2. **Process boxes**: rectangles (#4299e1 blue)
3. **Decision diamonds**: diamonds (#f59e0b orange)
4. **Arrows**: connecting paths with labels
5. **Swimlanes**: grouped sections (optional)

## HTML Structure

```html
<!DOCTYPE html>
<html>
<head>
  <title>[Process] Flowchart</title>
  <style>
    body { font-family: system-ui; }
    svg { max-width: 100%; }
    .start-end { fill: #48bb78; }
    .process { fill: #4299e1; }
    .decision { fill: #f59e0b; }
  </style>
</head>
<body>
  <h1>[Process Name] Flowchart</h1>
  <svg viewBox="0 0 800 600">
    <!-- flowchart nodes and connectors -->
  </svg>
</body>
</html>
```

## Node Patterns

```html
<!-- Start/End (rounded rect) -->
<rect x="350" y="50" width="100" height="50" rx="25" class="start-end"/>
<text x="400" y="80" text-anchor="middle">Start</text>

<!-- Process box -->
<rect x="350" y="150" width="100" height="60" class="process"/>
<text x="400" y="185" text-anchor="middle">Process</text>

<!-- Decision diamond -->
<path d="M400,250 L450,280 L400,310 L350,280 Z" class="decision"/>
<text x="400" y="285" text-anchor="middle">Decision?</text>

<!-- Arrow -->
<path d="M400,100 L400,150" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
```

## Workflow

1. Break down process into steps
2. Identify decision points
3. Layout nodes vertically or horizontally
4. Connect with arrows
5. Add labels to decision branches
6. Write to `[process]-flowchart.html`

Keep layout clean, use consistent spacing (100px between nodes).
