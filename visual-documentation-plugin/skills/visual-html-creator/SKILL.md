---
name: visual-html-creator
description: Create stunning, interactive visual HTML documentation files with modern UI design, SVG diagrams, flowcharts, dashboards, and timelines. Use when users explicitly request visual HTML documentation, process flow diagrams, metric dashboards, API workflow guides, deployment process visuals, or project roadmaps. Generates standalone HTML files with embedded CSS and SVG graphics optimized for technical documentation and data visualization.
---

# Visual HTML Creator

## Overview

Create professional, standalone HTML documentation files with modern visual design, featuring SVG diagrams, interactive flowcharts, metric dashboards, timelines, and technical documentation. Generate self-contained HTML files that combine elegant styling with information-rich visualizations for processes, workflows, data, and technical guides.

## When to Use This Skill

Activate this skill when users request:
- "Create a visual HTML for [topic]"
- "Generate a visual guide for [process]"
- "Make a dashboard showing [metrics]"
- "Build a timeline for [project]"
- "Create an HTML flowchart for [workflow]"
- "Visualize [data/process] as an HTML document"

## Core Capabilities

### 1. Process Flow Diagrams

Create visual flowcharts showing step-by-step processes with decision trees, arrows, and color-coded stages.

**Components:**
- Input/output boxes with rounded corners
- Decision diamonds with branching paths
- Process steps with status indicators
- Arrow markers and connectors
- Color-coded modules/categories

**Example SVG structure from templates:**
```xml
<!-- Decision node -->
<path d="M 600 130 L 700 130 L 750 180 L 700 230 L 500 230 L 450 180 Z"
      fill="#fbbf24" stroke="#d97706" stroke-width="3"/>
<text x="600" y="175" text-anchor="middle">Decision Point?</text>

<!-- Arrow with marker -->
<path d="M 750 180 L 900 180" stroke="#2d3748" stroke-width="3"
      marker-end="url(#arrowhead)"/>
```

### 2. Metric Dashboards

Display statistics, KPIs, and numerical data with visually appealing metric cards and charts.

**Components:**
- Gradient-styled metric cards
- Large numeric displays with labels
- Bar charts and distribution graphs
- Color-coded categories
- Responsive grid layouts

**Example metric card pattern:**
```html
<div class="metric-card">
    <div class="metric-value">1,064</div>
    <div class="metric-label">Unique Problems<br>(Output)</div>
</div>
```

### 3. Technical Documentation

Present code examples, API workflows, system architecture, and technical guides with syntax highlighting and clear organization.

**Components:**
- Code blocks with syntax highlighting
- Example boxes with colored borders
- Tabbed sections for organization
- Legend/key displays
- Collapsible content areas

**Example code block styling:**
```html
<div class="code-block">
<span class="highlight">Key term:</span> Regular text explanation
    Indented code or data
</div>
```

### 4. Project Timelines & Roadmaps

Visualize project phases, milestones, dependencies, and schedules.

**Components:**
- Horizontal/vertical timeline bars
- Milestone markers
- Phase groupings with color coding
- Dependency arrows
- Date labels and legends

## Design System

### Color Palette

Use the reference color schemes from `references/design_patterns.md`:

**Primary gradient:**
- Background: `linear-gradient(135deg, #667eea 0%, #764ba2 100%)`
- Accent colors: `#667eea` (purple-blue), `#764ba2` (purple)

**Semantic colors:**
- Success/Confirmed: `#48bb78` (green)
- Warning/Uncertain: `#f59e0b` (amber)
- Info/Primary: `#4299e1` (blue)
- Process/Action: `#ed8936` (orange)
- Special/Highlight: `#9f7aea` (purple)
- Error/Critical: `#f56565` (red)

**Neutral palette:**
- Dark text: `#2d3748`
- Medium text: `#718096`
- Light text: `#a0aec0`
- Borders: `#e2e8f0`, `#cbd5e0`
- Backgrounds: `#f7fafc`, `#edf2f7`

### Typography

**Font stack:** `'Segoe UI', Tahoma, Geneva, Verdana, sans-serif`

**Size scale:**
- Headings (h1): 2.5em with gradient text effect
- Section titles (h2): 1.8em
- Subsections (h3): 1.4em
- Body text: 1em (base)
- Labels/captions: 0.9-0.95em
- Small text: 0.85em

**Code font:** `'Courier New', monospace`

### Layout Patterns

**Container structure:**
```html
<body>
    <div class="container">
        <h1>Document Title</h1>
        <p class="subtitle">Descriptive subtitle</p>

        <div class="metric-grid"><!-- Metrics --></div>

        <div class="section">
            <h2 class="section-title">Section Name</h2>
            <div class="diagram-container"><!-- SVG --></div>
        </div>
    </div>
</body>
```

**Responsive design:**
- Max container width: 1400px
- Padding: 40px desktop, 20px mobile
- Grid: `repeat(auto-fit, minmax(200px, 1fr))`
- Media query breakpoint: 768px

## Workflow

### Step 1: Understand the Content

Analyze the user's request to determine:
- **Content type:** Process flow, metrics, technical docs, timeline
- **Key information:** Data points, process steps, relationships
- **Audience:** Technical depth and presentation style
- **Output goals:** What insights should the visualization convey?

### Step 2: Select Template Components

Choose appropriate building blocks from `assets/templates/`:

**For process flows:**
- Use `flowchart_components.html` for decision trees and flow diagrams
- Include arrow markers, decision diamonds, process boxes
- Add legends for color-coded categories

**For dashboards:**
- Use `dashboard_components.html` for metric cards and charts
- Include bar charts, pie charts, or custom visualizations
- Add metric grids for key statistics

**For technical documentation:**
- Use `base_template.html` with code blocks and example boxes
- Include syntax-highlighted code samples
- Add tabbed or collapsible sections for organization

**For timelines:**
- Use `timeline_components.html` for roadmap visualizations
- Include milestone markers and phase groupings
- Add horizontal or vertical timeline layouts

### Step 3: Structure the Document

Organize content into logical sections:

1. **Header area:** Title, subtitle, overview metrics
2. **Main sections:** Each with clear section title and diagram/content
3. **Supporting details:** Examples, legends, code blocks
4. **Footer:** Summary, metadata, generation details

**Section template:**
```html
<div class="section">
    <h2 class="section-title">Section Number. Section Title</h2>

    <div class="diagram-container">
        <svg viewBox="0 0 1200 600">
            <!-- SVG content -->
        </svg>
    </div>

    <div class="example-box">
        <div class="example-title">Example Title</div>
        <!-- Example content -->
    </div>
</div>
```

### Step 4: Create SVG Visualizations

Build SVG diagrams using reusable patterns from `references/svg_library.md`:

**SVG best practices:**
- Use `viewBox` for responsive scaling: `<svg viewBox="0 0 1200 800">`
- Define reusable elements in `<defs>` (markers, gradients, patterns)
- Group related elements with `<g id="groupName">`
- Use semantic IDs and classes
- Add text labels with `text-anchor` for alignment
- Include stroke-width="2-3" for visibility

**Common SVG patterns:**
```xml
<!-- Rounded rectangle (box) -->
<rect x="50" y="50" width="200" height="100" rx="10"
      fill="#4299e1" stroke="#2b6cb0" stroke-width="3"/>

<!-- Diamond (decision) -->
<path d="M 600 130 L 700 130 L 750 180 L 700 230 L 500 230 L 450 180 Z"
      fill="#fbbf24" stroke="#d97706" stroke-width="3"/>

<!-- Circle (node/marker) -->
<circle cx="300" cy="200" r="15"
        fill="#48bb78" stroke="#2f855a" stroke-width="3"/>

<!-- Arrow marker definition -->
<defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="10"
            refX="9" refY="3" orient="auto">
        <polygon points="0 0, 10 3, 0 6" fill="#2d3748"/>
    </marker>
</defs>

<!-- Line with arrow -->
<path d="M 150 150 L 400 150" stroke="#2d3748" stroke-width="3"
      marker-end="url(#arrowhead)"/>
```

### Step 5: Apply Styling

Use the embedded CSS patterns from `assets/templates/base_template.html`:

**Key CSS classes:**
- `.container` - Main content wrapper with centering and shadow
- `.section` - Logical content section with bottom margin
- `.section-title` - Section heading with bottom border
- `.diagram-container` - SVG wrapper with background and padding
- `.metric-grid` - Responsive grid for metric cards
- `.metric-card` - Gradient card for displaying statistics
- `.code-block` - Dark themed code display
- `.example-box` - Bordered content box for examples
- `.legend` - Flexible legend/key display

**Gradient text effect:**
```css
h1 {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
```

### Step 6: Generate Complete HTML

Combine all elements into a single, standalone HTML file:

**File structure:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Document Title]</title>
    <style>
        /* Embedded CSS - all styles inline */
    </style>
</head>
<body>
    <div class="container">
        <!-- Content -->
    </div>
</body>
</html>
```

**Quality checklist:**
- [ ] All CSS embedded in `<style>` tags (no external files)
- [ ] All SVG inline (no external image references)
- [ ] Responsive design with mobile breakpoints
- [ ] Semantic HTML structure
- [ ] Accessible color contrast (WCAG AA minimum)
- [ ] Clear visual hierarchy
- [ ] Consistent spacing and alignment
- [ ] Browser compatibility (modern browsers)

## Best Practices

### Content Organization

**Prioritize progressive disclosure:**
1. Start with high-level overview/summary
2. Present key metrics or findings upfront
3. Provide detailed diagrams in logical sections
4. Include examples and supporting details last
5. Add footer with metadata and context

**Use visual hierarchy:**
- Larger elements = more important information
- Color intensity = semantic meaning (green=good, red=critical, amber=warning)
- Position: top-left to bottom-right reading flow
- Whitespace: generous padding between sections (40-60px)

### SVG Design

**Optimize for readability:**
- Minimum font size: 11px for labels, 14px for primary text
- Stroke width: 2-3px for visibility
- Icon/shape size: minimum 30×30px for interactive elements
- Line spacing: 20-25px between text lines in diagrams
- Contrast: use stroke colors darker than fill colors

**Performance considerations:**
- Keep SVG viewBox proportional (e.g., 1200×800, 1000×600)
- Avoid overly complex paths (use simplified shapes)
- Reuse definitions with `<use>` tags when appropriate
- Keep total SVG nodes under 1000 per diagram

### Accessibility

**Ensure usability:**
- Color is not the only indicator (use shapes, labels, patterns)
- Include text labels for all visual elements
- Use semantic HTML tags (`<section>`, `<article>`, `<header>`)
- Provide alt text context in surrounding HTML if needed
- Ensure 4.5:1 contrast ratio for text (use dark text on light backgrounds)

### Responsive Design

**Mobile-friendly patterns:**
```css
@media (max-width: 768px) {
    .container { padding: 20px; }
    h1 { font-size: 1.8em; }
    .section-title { font-size: 1.4em; }
    .metric-grid { grid-template-columns: 1fr; }
}
```

## Resources

### assets/templates/

Ready-to-use HTML templates with embedded CSS and example SVG components:

- **`base_template.html`** - Core document structure with complete CSS framework
- **`flowchart_components.html`** - Process flow and decision tree patterns
- **`dashboard_components.html`** - Metric cards, charts, and data visualizations
- **`timeline_components.html`** - Project timeline and roadmap layouts

**Usage:** Copy relevant sections from templates and customize content.

### references/

Detailed reference documentation:

- **`design_patterns.md`** - Complete design system with color palettes, typography scales, spacing guidelines, and layout patterns
- **`svg_library.md`** - Comprehensive SVG component library with shapes, arrows, icons, and connector patterns including viewBox calculations and coordinate systems

**Usage:** Consult when making design decisions or building custom SVG diagrams.

## Example Outputs

### Process Flow Example

**User request:** "Create a visual guide for our deployment process"

**Output includes:**
- Decision tree showing deployment paths (production/staging/development)
- Status indicators for each stage (pending/in-progress/completed)
- Color-coded boxes for different deployment types
- Arrow flow showing sequential and parallel steps
- Legend explaining status colors and symbols

### Dashboard Example

**User request:** "Make a dashboard showing project metrics"

**Output includes:**
- Metric cards displaying: total tasks, completed, in progress, blocked
- Bar chart showing task distribution by category
- Timeline visualization of milestone completion
- Color-coded status indicators
- Summary statistics in footer

### API Workflow Example

**User request:** "Create visual HTML showing our API workflow"

**Output includes:**
- Sequential flow diagram: Client → API Gateway → Services → Database
- Request/response boxes with sample JSON
- Authentication flow decision tree
- Error handling paths in red
- Code examples in dark-themed blocks
- Legend for HTTP methods (GET/POST/PUT/DELETE)

### Timeline Example

**User request:** "Build a timeline for our product roadmap"

**Output includes:**
- Horizontal timeline with quarters marked
- Milestone markers with descriptions
- Phase groupings (Planning, Development, Testing, Launch)
- Dependency arrows between related items
- Color-coded priorities (critical/high/medium/low)
- Current date indicator

## Troubleshooting

**Issue:** SVG not displaying correctly
- **Solution:** Check viewBox dimensions match content bounds, ensure all paths are closed

**Issue:** Colors look different than expected
- **Solution:** Use hex colors consistently, avoid color names, check gradient definitions

**Issue:** Mobile layout broken
- **Solution:** Verify media query at 768px, use flexible units (%, em), test responsive grid

**Issue:** Large file size
- **Solution:** Minimize whitespace in SVG, avoid base64 images, simplify complex paths

**Issue:** Overlapping text in diagrams
- **Solution:** Increase viewBox size, adjust text-anchor and positioning, use smaller font sizes
