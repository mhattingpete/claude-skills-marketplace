---
name: architecture-diagram-creator
description: Create comprehensive HTML architecture diagrams showing data flows, business objectives, features, technical architecture, and deployment. Use when users request system architecture, project documentation, high-level overviews, or technical specifications.
---

# Architecture Diagram Creator

Create comprehensive HTML architecture diagrams with data flows, business context, and system architecture.

## When to Use

- "Create architecture diagram for [project]"
- "Generate high-level overview"
- "Document system architecture"
- "Show data flow and processing pipeline"

## Components to Include

1. **Business Context**: objectives, users, value, metrics
2. **Data Flow**: sources → processing → outputs with SVG diagram
3. **Processing Pipeline**: multi-stage visualization
4. **System Architecture**: layered components (data/processing/services/output)
5. **Features**: functional and non-functional requirements
6. **Deployment**: model, prerequisites, workflows

## HTML Structure

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Project] Architecture</title>
  <style>
    body { font-family: system-ui; max-width: 1200px; margin: 0 auto; padding: 20px; }
    h1 { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; }
    .section { margin: 30px 0; }
    svg { max-width: 100%; }
    /* Use semantic colors: #4299e1 (data), #ed8936 (processing), #9f7aea (AI), #48bb78 (success) */
  </style>
</head>
<body>
  <h1>[Project Name] - Architecture Overview</h1>

  <!-- Business Context Section -->
  <!-- Data Flow Diagram (SVG) -->
  <!-- Processing Pipeline (SVG) -->
  <!-- System Architecture Layers -->
  <!-- Features Grid -->
  <!-- Deployment Info -->
</body>
</html>
```

## SVG Pattern for Data Flow

```html
<svg viewBox="0 0 800 400">
  <!-- Data sources (left, blue) -->
  <rect x="50" y="150" width="120" height="80" fill="#4299e1"/>

  <!-- Processing (center, orange) -->
  <rect x="340" y="150" width="120" height="80" fill="#ed8936"/>

  <!-- Outputs (right, green) -->
  <rect x="630" y="150" width="120" height="80" fill="#48bb78"/>

  <!-- Arrows connecting -->
  <path d="M170,190 L340,190" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
</svg>
```

## Workflow

1. Analyze project (README, code structure)
2. Extract: purpose, data sources, processing, tech stack, outputs
3. Create HTML with all 6 sections
4. Use semantic colors for visual hierarchy
5. Write to `[project]-architecture.html`

Keep diagrams clear, use consistent styling, include real project details.
